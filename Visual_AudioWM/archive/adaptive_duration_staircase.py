"""
Adaptive Duration Staircase for b3/p3 Time-Length JND Measurement in Working Memory

研究目標：
  測量每個被試者在「顏色-語音工作記憶綁定任務」中，對 b3/p3 時長差異的
  知覺閾值(JND, Just Noticeable Difference),填補文獻空白。

Adaptive 方法：
  - 開始：30ms 時長差異(目前設計值)
  - 規則：1-up-1-down staircase → 收斂到 ~70.7% 正確率
  - 終止：10 個 reversals 或達成收斂條件

輸出：
  - 每被試者個體的時長 JND 估計
  - 決策策略可視化(是被試者利用時長線索還是其他線索?)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
import json
from pathlib import Path
import tempfile


@dataclass
class StaircaseConfig:
    """Staircase 參數設定"""
    initial_duration_diff_ms: float = 30.0      # 開始差異(ms): b=90, p=120
    min_duration_diff_ms: float = 0.0            # 最小差異(ms),禁止下限
    max_duration_diff_ms: float = 100.0          # 最大差異(ms)

    step_size_ms: float = 5.0                    # 每次調整幅度(ms)
    step_size_reduction: float = 0.5             # reversal後步幅縮放

    rule: str = "1up1down"                       # "1up1down" (70.7%) 或 "2up1down" (79.4%)

    n_trials_per_block: int = 20                 # 每 block 20 trials
    n_blocks: int = 8                            # 總 8 blocks → 160 trials
    n_reversals_per_block: int = 3               # 每 block 停止條件

    reversal_window: int = 4                     # 計算收斂用的window size


@dataclass
class StaircaseState:
    """Staircase 狀態(每被試者)"""
    participant_id: str
    config: StaircaseConfig

    # 試驗序列（全部 blocks 合併）
    trial_numbers: List[int] = None              # 試驗編號(1~160)
    block_numbers: List[int] = None              # 各試驗所屬 block (1~8)
    duration_diffs: List[float] = None           # 各試驗的時長差異(ms)
    responses: List[bool] = None                 # 各試驗的正確/錯誤 (True=正確)
    reversals: List[int] = None                  # reversal 發生的試驗編號

    def __post_init__(self):
        if self.trial_numbers is None:
            self.trial_numbers = []
        if self.block_numbers is None:
            self.block_numbers = []
        if self.duration_diffs is None:
            self.duration_diffs = []
        if self.responses is None:
            self.responses = []
        if self.reversals is None:
            self.reversals = []

    @property
    def current_block(self) -> int:
        """目前在第幾個 block (1-indexed)"""
        if len(self.block_numbers) == 0:
            return 1
        return self.block_numbers[-1]

    @property
    def trials_in_current_block(self) -> int:
        """目前 block 已做幾個 trial"""
        if len(self.block_numbers) == 0:
            return 0
        return sum(1 for b in self.block_numbers if b == self.current_block)

    @property
    def is_block_finished(self) -> bool:
        """目前 block 是否完成"""
        if self.trials_in_current_block >= self.config.n_trials_per_block:
            return True
        # 或根據 reversal 數
        block_reversals = sum(1 for r in self.reversals if
                             len(self.block_numbers) > r - 1 and
                             self.block_numbers[r - 1] == self.current_block)
        if block_reversals >= self.config.n_reversals_per_block:
            return True
        return False

    @property
    def is_finished(self) -> bool:
        """是否所有 blocks 都完成"""
        return self.current_block > self.config.n_blocks and self.is_block_finished

    @property
    def jnd_estimate(self) -> float:
        """基於最後一個 block 計算 JND"""
        if len(self.reversals) < 2:
            return self.config.initial_duration_diff_ms
        # 取最後一個 block 內的差異值做平均
        last_block_trials = [i for i, b in enumerate(self.block_numbers) if b == self.current_block]
        if not last_block_trials:
            return self.config.initial_duration_diff_ms
        last_trial_idx = last_block_trials[-1]
        window_start = max(0, last_trial_idx - self.config.reversal_window)
        window_end = last_trial_idx + 1
        return np.mean(self.duration_diffs[window_start:window_end])


class AdaptiveStaircase:
    """Adaptive Staircase 控制器"""

    def __init__(self, participant_id: str, config: StaircaseConfig = None):
        self.config = config or StaircaseConfig()
        self.state = StaircaseState(participant_id, self.config)
        self._current_direction = None  # "up" or "down",用於偵測 reversal

    def next_trial(self) -> Tuple[float, int]:
        """
        取得下一次試驗的時長差異設定。
        呼叫時機：在每個試驗開始時

        Returns
        -------
        (float, int)
            (時長差異 ms, 目前 block 編號)
            時長差異用法：p3_duration = 375 + (diff/2), b3_duration = 375 - (diff/2)
            或保持原設計：b3=90ms, p3=120ms 為基準,然後按此比例調整。
        """
        # 檢查是否需要開始新 block
        if self.state.is_block_finished and not self.state.is_finished:
            # 進入下一個 block，重置 staircase 參數
            self._current_direction = None
            self.config.step_size_ms = 5.0  # 重置步長

        trial_num = len(self.state.trial_numbers) + 1
        current_block = self.state.current_block
        if len(self.state.block_numbers) < trial_num:
            self.state.block_numbers.append(current_block)
        self.state.trial_numbers.append(trial_num)

        if trial_num == 1 or len(self.state.duration_diffs) == 0:
            # 第一試驗或新 block 的第一試驗：用初始值
            duration_diff = self.config.initial_duration_diff_ms
        else:
            # 根據上一試驗結果調整
            last_correct = self.state.responses[-1]
            current_diff = self.state.duration_diffs[-1]

            if self._should_increase_difficulty(last_correct):
                # 難度上升(減少時長差異)
                new_diff = current_diff - self.config.step_size_ms
                direction = "down"
            else:
                # 難度下降(增加時長差異)
                new_diff = current_diff + self.config.step_size_ms
                direction = "up"

            # 偵測 reversal
            if self._current_direction is not None and self._current_direction != direction:
                self.state.reversals.append(trial_num - 1)
                # 減小步長
                self.config.step_size_ms *= self.config.step_size_reduction

            self._current_direction = direction

            # 確保在邊界內
            duration_diff = np.clip(new_diff,
                                     self.config.min_duration_diff_ms,
                                     self.config.max_duration_diff_ms)

        self.state.duration_diffs.append(duration_diff)
        return duration_diff, current_block

    def record_response(self, is_correct: bool):
        """
        記錄被試者在本試驗的反應。
        呼叫時機：在每個試驗結束、取得反應後

        Parameters
        ----------
        is_correct : bool
            被試者是否正確配對顏色-語音(或在你的設計中,是否正確辨識 b vs p)
        """
        self.state.responses.append(is_correct)

    def _should_increase_difficulty(self, last_correct: bool) -> bool:
        """根據 staircase 規則決定下一步"""
        if self.config.rule == "1up1down":
            # 正確時下一步難度上升(減少時長差異)
            return last_correct
        elif self.config.rule == "2up1down":
            # 需要連續2次正確才上升
            if len(self.state.responses) < 2:
                return last_correct
            return last_correct and self.state.responses[-2]
        else:
            raise ValueError(f"Unknown rule: {self.config.rule}")

    @property
    def is_finished(self) -> bool:
        return self.state.is_finished

    @property
    def jnd_estimate(self) -> float:
        return self.state.jnd_estimate

    def get_summary(self) -> dict:
        """取得目前狀態摘要"""
        if len(self.state.responses) == 0:
            accuracy = None
        else:
            accuracy = np.mean(self.state.responses)

        return {
            "participant_id": self.state.participant_id,
            "n_trials_completed": len(self.state.trial_numbers),
            "n_reversals": len(self.state.reversals),
            "current_duration_diff_ms": self.state.duration_diffs[-1] if self.state.duration_diffs else None,
            "jnd_estimate_ms": self.jnd_estimate,
            "overall_accuracy": accuracy,
            "is_finished": self.is_finished,
        }

    def save_to_json(self, output_path: str):
        """保存被試者資料"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        data = {
            "participant_id": self.state.participant_id,
            "config": {
                "initial_duration_diff_ms": self.config.initial_duration_diff_ms,
                "rule": self.config.rule,
            },
            "trials": [
                {
                    "trial_num": int(tn),
                    "duration_diff_ms": float(dd),
                    "is_correct": bool(resp),
                }
                for tn, dd, resp in zip(
                    self.state.trial_numbers,
                    self.state.duration_diffs,
                    self.state.responses
                )
            ],
            "reversals": [int(r) for r in self.state.reversals],
            "jnd_estimate_ms": float(self.jnd_estimate),
            "overall_accuracy": float(np.mean(self.state.responses)) if self.state.responses else None,
        }
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)


# ============================================================================
# PsychoPy 整合範例
# ============================================================================

PSYCHOPY_INTEGRATION_EXAMPLE = """
# 在 PsychoPy 的 Begin Experiment code 區塊：

from adaptive_duration_staircase import AdaptiveStaircase, StaircaseConfig

# 初始化 staircase
config = StaircaseConfig(
    initial_duration_diff_ms=30.0,
    rule="1up1down",  # 或 "2up1down"
    n_reversals_target=10,
)
staircase = AdaptiveStaircase(participant_id=expInfo['participant'], config=config)

# 在 Begin Routine code 區塊（每個試驗開始）：

# 1. 取得本試驗的時長差異
duration_diff_ms = staircase.next_trial()

# 2. 根據 duration_diff 生成/調整 b3 和 p3 音檔
from generate_speech_stimulus import generate_speech_wav
import tempfile

temp_dir = tempfile.gettempdir()

# 計算本試驗的實際時長(ms)
# 基線：b3=90ms, p3=120ms (差30ms)
# 調整：線性縮放
baseline_diff_ms = 30.0
scale_factor = duration_diff_ms / baseline_diff_ms
b3_duration_ms = 90 * scale_factor
p3_duration_ms = 120 * scale_factor

# 提示：此處需要修改 generate_speech_stimulus.py 或 GetAudioStim.py
# 以支持動態時長調整。簡單做法是用 espeak-ng 的速度參數近似：
voice_speed_b3 = 1.0 / scale_factor  # 反向:變快 -> 時長變短
voice_speed_p3 = 1.0 / scale_factor

b3_path = generate_speech_wav("[[b3:]]", output_dir=temp_dir, voice_speed=voice_speed_b3)
p3_path = generate_speech_wav("[[p3:]]", output_dir=temp_dir, voice_speed=voice_speed_p3)

# 3. 在試驗中播放、收集反應、記錄結果
# (標準 PsychoPy 流程...)

# End Routine code 區塊：
is_correct = (trial_response == correct_answer)
staircase.record_response(is_correct)

# 如果試驗已完成：
if staircase.is_finished:
    # 儲存資料
    staircase.save_to_json(f"data/{expInfo['participant']}_staircase.json")
    # 結束實驗迴圈
    trials.finished = True
"""


if __name__ == "__main__":
    # 測試：模擬一個被試者的完整 staircase
    print("=== Adaptive Staircase 模擬測試 ===\\n")

    config = StaircaseConfig(
        initial_duration_diff_ms=30.0,
        rule="1up1down",
        n_reversals_target=5,  # 模擬用較少 reversals
    )
    staircase = AdaptiveStaircase("test_participant", config)

    # 模擬被試者的反應序列：
    # (假設當時長差異 > 15ms 時,被試者很容易正確；< 10ms 時則容易錯誤)
    for trial_idx in range(20):
        duration_diff = staircase.next_trial()
        # 簡單的感知模型：差異越大、正確率越高
        accuracy_prob = 1.0 / (1.0 + np.exp(-0.5 * (duration_diff - 12)))  # sigmoid
        is_correct = np.random.rand() < accuracy_prob
        staircase.record_response(is_correct)

        print(f"Trial {staircase.state.trial_numbers[-1]:2d}  "
              f"Duration Diff: {duration_diff:6.2f}ms  "
              f"Response: {'✓' if is_correct else '✗'}  "
              f"Reversals: {len(staircase.state.reversals)}")

        if staircase.is_finished:
            break

    print(f"\\n=== 結果摘要 ===")
    summary = staircase.get_summary()
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key:30s}: {value:8.2f}")
        else:
            print(f"{key:30s}: {value}")

    # 儲存
    staircase.save_to_json("/tmp/test_staircase.json")
    print(f"\\n資料已儲存至 /tmp/test_staircase.json")
