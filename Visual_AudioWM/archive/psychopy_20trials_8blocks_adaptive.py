"""
PsychoPy 整合：20 trials × 8 blocks adaptive duration staircase
+ 聽覺基準線對照組 (40 組 b3/p3 純比較)

實驗結構：
  - 聽覺基準線(可選)：40 trials，純「一樣還是不一樣」判斷，無顏色、無記憶
  - Adaptive 主任務：20 trials × 8 blocks = 160 trials，動態調整 b3/p3 時長差異
      每 block 自動停止(20 trials 或達成 reversals 數)
      下一 block 從 30ms 重新開始(或接上前一 block 的收斂值)

使用方式：
  1. 在 PsychoPy Builder 的「Begin Experiment」code 區塊貼入「初始化」段
  2. 在 「Begin Routine」code 區塊貼入「試驗開始」段
  3. 在「End Routine」code 區塊貼入「試驗結束」段
"""

# ═══════════════════════════════════════════════════════════════
# 初始化（Begin Experiment code 區塊）
# ═══════════════════════════════════════════════════════════════

PSYCHOPY_BEGIN_EXPERIMENT_CODE = """
from adaptive_duration_staircase import AdaptiveStaircase, StaircaseConfig
from generate_b3_p3_auditory_baseline import AuditoryBaselineStimuli
import tempfile
import json

# ── Adaptive Staircase 設定 ──
staircase_config = StaircaseConfig(
    initial_duration_diff_ms=30.0,
    rule="1up1down",
    n_trials_per_block=20,
    n_blocks=8,
    n_reversals_per_block=3,  # 每 block 達 3 reversals 就結束
)
staircase = AdaptiveStaircase(
    participant_id=expInfo['participant'],
    config=staircase_config
)

# ── 暫存目錄用於動態生成音檔 ──
temp_audio_dir = tempfile.mkdtemp(prefix="psychopy_adaptive_")

# ── 快取對照用的聽覺基準線刺激(可選) ──
# auditory_baseline = AuditoryBaselineStimuli(output_dir=temp_audio_dir)
# auditory_csv = auditory_baseline.generate(n_trials=40)
# baseline_data = load_auditory_baseline(auditory_csv)  # 實作另外的載入函式

print(f"Adaptive staircase 已初始化: 20 trials × 8 blocks")
print(f"臨時音檔目錄: {temp_audio_dir}")
"""

# ═══════════════════════════════════════════════════════════════
# 試驗開始（Begin Routine code 區塊）
# ═══════════════════════════════════════════════════════════════

PSYCHOPY_BEGIN_ROUTINE_CODE = """
import subprocess
import os
import tempfile

# 1. 取得本試驗的時長差異
duration_diff_ms, current_block = staircase.next_trial()

# 2. 動態生成 b3 和 p3 音檔（用 MBROLA + GetAudioStim.py）
# ── 方法 A：呼叫 GetAudioStim.py 的修改版 ──
from generate_b3_p3_auditory_baseline import synthesize_single

# 假設有一個被隨機選中的 talker（可從條件檔或隨機選取）
talker_id = int(trial_idx % 18) + 1  # 簡化：迴圈選 talker
talker = staircase.state.trial_numbers  # 需要實作 talker 查詢邏輯

# 計算子音時長因子
# 基準：b3 = 60ms, p3 = 80ms（已乘以 SPEED_FACTOR × CONSONANT_FACTOR）
# 要造出 duration_diff_ms 的差異
base_diff_ms = 20.0  # p3 - b3 的基準差異(調整為實際值)
scale = duration_diff_ms / base_diff_ms
b3_consonant_factor = 1.0 / scale
p3_consonant_factor = 1.0 / scale

# 生成音檔
b3_wav = os.path.join(temp_audio_dir, f"trial_{len(staircase.state.trial_numbers)}_b3.wav")
p3_wav = os.path.join(temp_audio_dir, f"trial_{len(staircase.state.trial_numbers)}_p3.wav")

# 此處調用修改的 synthesize_single() —— 需要 GetAudioStim.py 支持
# success_b, _ = synthesize_single('b', talker, b3_wav, b3_consonant_factor)
# success_p, _ = synthesize_single('p', talker, p3_wav, p3_consonant_factor)

# 簡化版：暫時用預先生成的檔案（開發時用）
# b3_wav = f"stimuli/pre_generated_b3_talker{talker_id}.wav"
# p3_wav = f"stimuli/pre_generated_p3_talker{talker_id}.wav"

# 3. 將路徑指派給 PsychoPy 的 Sound 元件
soundB3.setSound(b3_wav)
soundP3.setSound(p3_wav)

# 4. 記錄試驗資訊（用於後續分析）
current_trial_duration_diff = duration_diff_ms
current_trial_block = current_block
"""

# ═══════════════════════════════════════════════════════════════
# 試驗結束（End Routine code 區塊）
# ═══════════════════════════════════════════════════════════════

PSYCHOPY_END_ROUTINE_CODE = """
# 1. 判斷被試者反應是否正確
# (假設 trial_response 已從你的反應收集邏輯設定)
is_correct = (trial_response == correct_answer)  # 例如正確答案可能來自條件檔

# 2. 記錄到 staircase
staircase.record_response(is_correct)

# 3. 記錄到實驗資料
thisExp.addData('adaptive_duration_diff_ms', current_trial_duration_diff)
thisExp.addData('adaptive_block', current_trial_block)
thisExp.addData('adaptive_response_correct', is_correct)
thisExp.addData('adaptive_jnd_estimate_ms', staircase.jnd_estimate)

# 4. 檢查是否完成（所有 blocks）
if staircase.is_finished:
    # 儲存 staircase 資料
    staircase.save_to_json(f"data/{expInfo['participant']}_adaptive_jnd.json")

    # 結束實驗迴圈
    adaptive_trials.finished = True

    print(f"Adaptive staircase 完成")
    print(f"最終 JND 估計: {staircase.jnd_estimate:.2f} ms")
"""

# ═══════════════════════════════════════════════════════════════
# CSV 條件檔例子（stimuli/adaptive_trials.csv）
# ═══════════════════════════════════════════════════════════════

CSV_TEMPLATE = """trial_num,trial_type,talker_id,correct_answer
1,color_speech_bind,T01,b3
2,color_speech_bind,T02,p3
3,color_speech_bind,T03,b3
...
160,color_speech_bind,T18,p3
"""

# ═══════════════════════════════════════════════════════════════
# 修改 GetAudioStim.py 需要的改動
# ═══════════════════════════════════════════════════════════════

GETAUDIOSTIM_MODIFICATIONS = """
# 在 GetAudioStim.py 的 make_pho() 函數中加上 consonant_factor 參數：

def make_pho(cons_sampa, base_pitch, vowel_dur=None, consonant_factor=1.0):
    \"\"\"產生 /Cɜ/ 的 .pho，全程 F0 完全平坦

    Parameters
    ----------
    consonant_factor : float
        子音時長倍數(1.0 = 基準, <1.0 = 縮短, >1.0 = 延長)
    \"\"\"
    if vowel_dur is None:
        vowel_dur = VOWEL_DUR

    base_cons_dur = CONS_DURATIONS.get(cons_sampa, int(100 * SPEED_FACTOR * CONSONANT_FACTOR))
    cons_dur = int(base_cons_dur * consonant_factor)  # ← 動態調整

    # ... 其餘邏輯不變 ...


# 並修改 synthesize() 函數簽名：

def synthesize(cons_sampa, talker, output_wav, consonant_factor=1.0):
    \"\"\"用 MBROLA 合成一個 /aCa/\"\"\"
    cfg = VOICES[talker['voice']]
    pho_content = make_pho(cons_sampa, cfg['base_pitch'], consonant_factor=consonant_factor)
    # ... 其餘邏輯不變 ...
"""

# ═══════════════════════════════════════════════════════════════
# 完整的 PsychoPy 迴圈結構建議
# ═══════════════════════════════════════════════════════════════

PSYCHOPY_LOOP_STRUCTURE = """
實驗結構（Builder 層級）：

Flow:
  ├─ 指示 (text_instructions)
  ├─ Routine: Auditory_Baseline  [可選]
  │  └─ Loop: auditory_baseline_trials (40 trials from CSV)
  │     └─ 純聽覺比較 routine (無顏色、無記憶)
  │
  └─ Routine: Adaptive_Main
     └─ Loop: adaptive_trials (20 × 8 blocks, 由 staircase 控制)
        └─ Color-Speech Binding Routine
           ├─ 呈現顏色 (vis.Rect)
           ├─ 呈現 b3/p3 (sound.Sound)
           ├─ 收集反應 (keyboard or mouse)
           └─ [End Routine code 更新 staircase]

CSV 結構：
  - auditory_baseline_trials.csv (40 列，條件檔)
    Columns: trial_num, trial_type, consonant1, consonant2, file1, file2, correct_answer

  - adaptive_trials.csv (160 列，條件檔 - 只用做流程控制)
    Columns: trial_num, trial_type, talker_id, correct_answer
"""

# ═══════════════════════════════════════════════════════════════
# 資料輸出格式
# ═══════════════════════════════════════════════════════════════

DATA_OUTPUT_SPEC = """
主實驗輸出 (adaptive_jnd.json，由 staircase.save_to_json() 產生):
{
  "participant_id": "P001",
  "trials": [
    {
      "trial_num": 1,
      "block": 1,
      "duration_diff_ms": 30.0,
      "is_correct": true
    },
    ...
  ],
  "jnd_estimate_ms": 11.25,
  "overall_accuracy": 0.71
}

PsychoPy CSV 輸出 (自動):
  - 每列一個 trial
  - Columns 包含: adaptive_duration_diff_ms, adaptive_block, adaptive_response_correct, ...
"""

if __name__ == "__main__":
    print("=== 20 trials × 8 blocks Adaptive Staircase ===\\n")
    print("1. 在 PsychoPy Builder Begin Experiment 貼上:")
    print(PSYCHOPY_BEGIN_EXPERIMENT_CODE)
    print("\\n2. 在 Begin Routine 貼上:")
    print(PSYCHOPY_BEGIN_ROUTINE_CODE)
    print("\\n3. 在 End Routine 貼上:")
    print(PSYCHOPY_END_ROUTINE_CODE)
