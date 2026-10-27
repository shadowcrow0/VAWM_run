"""
聽覺基準線刺激產生：40 組 b3/p3 純比較對

設計：
  - 無顏色、無視覺、無工作記憶延遲
  - 單純問受試者「兩個音一樣還是不一樣」
  - 目的：測量「無工作記憶負荷」下 b3 vs p3 的知覺 JND

配置：
  - 20 個 b-p 對比組（b3 vs p3 with 不同時長差異)
  - 20 個 control 組（同個音重複，例如 b3-b3 或 p3-p3）
  - 總 40 組

每組由 3 個 talker 隨機抽選，產生 40 個 wav 檔案
"""

import subprocess
import os
import csv
import tempfile
import json
from pathlib import Path
import numpy as np


# ──────────────────────────────────────────────
# 基本設定（與 GetAudioStim.py 同步）
# ──────────────────────────────────────────────

VOICES = {
    "us1": {"path": "/usr/share/mbrola/us1/us1", "base_pitch": 180, "label": "F"},
    "us2": {"path": "/usr/share/mbrola/us2/us2", "base_pitch": 115, "label": "M1"},
    "us3": {"path": "/usr/share/mbrola/us3/us3", "base_pitch": 125, "label": "M2"},
}

TALKER_GRID = {
    "us1": [(15000, 0.85), (15500, 0.95), (16000, 1.00), (16000, 1.10), (16500, 1.05), (17000, 1.15)],
    "us2": [(15000, 0.88), (16000, 1.00), (17000, 1.12)],
    "us3": [(15500, 0.92), (16500, 1.05), (17000, 0.85)],
}

SPEED_FACTOR = 1.0
CONSONANT_FACTOR = 1.5
VOWEL_STRESS_FACTOR = 1.5

BASE_VOWEL_DUR = 250
VOWEL_DUR = int(BASE_VOWEL_DUR * SPEED_FACTOR * VOWEL_STRESS_FACTOR)
SILENCE_DUR = int(50 * SPEED_FACTOR)
VOWEL_SAMPA = "r="

_BASE_CONS_DUR = {
    'p': 80, 'b': 60,
}
CONS_DURATIONS = {k: int(v * SPEED_FACTOR * CONSONANT_FACTOR) for k, v in _BASE_CONS_DUR.items()}

# 子音時長的中點與基準差異（b=90, p=120 -> 中點 105, 差 30）
CONS_MID_DUR = (CONS_DURATIONS['b'] + CONS_DURATIONS['p']) / 2.0
BASE_CONS_DIFF = CONS_DURATIONS['p'] - CONS_DURATIONS['b']

# 每個 wav 的固定總長度(ms)。尾端補靜音補到這個值，讓試次的時間結構
# 不隨時長操弄而改變（否則聽覺維度會跟呈現時間糾纏在一起）。
TOTAL_MS = 1000

# ──────────────────────────────────────────────
# Talker 生成
# ──────────────────────────────────────────────

def build_talkers():
    """產生所有 talker"""
    talkers = []
    idx = 0
    for voice_name, combos in TALKER_GRID.items():
        for vf, fr in combos:
            idx += 1
            talkers.append({
                'id': f'T{idx:02d}',
                'voice': voice_name,
                'voice_freq': vf,
                'pitch_ratio': fr,
            })
    return talkers


# ──────────────────────────────────────────────
# PHO 生成（支持動態子音時長因子）
# ──────────────────────────────────────────────

def make_pho_single(cons_sampa, base_pitch, cons_dur_ms=None, vowel_dur_ms=None,
                    total_ms=TOTAL_MS):
    """
    產生 /Cɜ/ 的 .pho，子音與母音時長都以**絕對毫秒**指定。

    以前的版本收 `cons_duration_factor`(倍數)。倍數在做適應性程序時很難用：
    你想要的是「這個試次的子音要 102.5 ms」，而不是「乘以 1.139 倍」。
    這裡改成直接給 ms，並在尾端補靜音把總長固定住。

    Parameters
    ----------
    cons_sampa : str
        SAMPA 子音代碼('p' 或 'b')
    base_pitch : int
        基頻 Hz
    cons_dur_ms : float, optional
        子音時長(ms)。None 則用 CONS_DURATIONS[cons_sampa]
    vowel_dur_ms : float, optional
        母音時長(ms)。None 則用 VOWEL_DUR
    total_ms : int
        整個 wav 的總長度(ms)。尾端靜音會補到這個值。

    Raises
    ------
    ValueError
        音段總長已經超過 total_ms，無法補靜音。
    """
    # MBROLA 的 .pho 只吃整數 ms，所以這裡一定會量化。用 floor(x+0.5) 而不是
    # round()：round() 是 banker's rounding，102.5->102 但 107.5->108，會讓
    # 對稱分配的兩端不對稱(要求差 5 ms 會變成 6 ms)。
    def _ms(x):
        return int(np.floor(x + 0.5))

    cons_dur = _ms(CONS_DURATIONS[cons_sampa] if cons_dur_ms is None else cons_dur_ms)
    vowel_dur = _ms(VOWEL_DUR if vowel_dur_ms is None else vowel_dur_ms)

    if cons_dur <= 0 or vowel_dur <= 0:
        raise ValueError(f"時長必須為正: cons={cons_dur} ms, vowel={vowel_dur} ms")

    lead = SILENCE_DUR
    tail = total_ms - lead - cons_dur - vowel_dur
    if tail < SILENCE_DUR:
        raise ValueError(
            f"總長不足: lead({lead}) + cons({cons_dur}) + vowel({vowel_dur}) "
            f"= {lead + cons_dur + vowel_dur} ms，超過 total_ms={total_ms} ms "
            f"扣掉尾端最小靜音 {SILENCE_DUR} ms 後的空間。請加大 total_ms。")

    flat = f"(0,{base_pitch}) (100,{base_pitch})"

    return (
        f"_ {lead}\n"
        f"{cons_sampa} {cons_dur} {flat}\n"
        f"{VOWEL_SAMPA} {vowel_dur} {flat}\n"
        f"_ {tail}\n"
    )


def synthesize_single(cons_sampa, talker, output_wav,
                      cons_dur_ms=None, vowel_dur_ms=None, total_ms=TOTAL_MS):
    """
    用 MBROLA 合成單個 /Cɜ/

    Parameters
    ----------
    cons_sampa : str
        子音 ('p' 或 'b')
    talker : dict
        Talker 信息
    output_wav : str
        輸出 WAV 路徑
    cons_dur_ms : float, optional
        子音時長(ms)，None 用預設
    vowel_dur_ms : float, optional
        母音時長(ms)，None 用預設
    total_ms : int
        wav 總長度(ms)
    """
    cfg = VOICES[talker['voice']]
    pho_content = make_pho_single(cons_sampa, cfg['base_pitch'],
                                  cons_dur_ms=cons_dur_ms,
                                  vowel_dur_ms=vowel_dur_ms,
                                  total_ms=total_ms)
    pho_file = tempfile.NamedTemporaryFile(mode='w', suffix='.pho', delete=False).name

    try:
        with open(pho_file, "w") as f:
            f.write(pho_content)

        cmd = [
            "mbrola",
            "-l", str(talker['voice_freq']),
            "-f", str(talker['pitch_ratio']),
            cfg['path'],
            pho_file,
            output_wav,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, ""
    finally:
        os.unlink(pho_file)


# ──────────────────────────────────────────────
# 聽覺基準線刺激集
# ──────────────────────────────────────────────

class AuditoryBaselineStimuli:
    """
    40 組 b3/p3 聽覺比較刺激集

    結構：
      - 20 個「不同」對(b3 vs p3，時長差異範圍 5-30ms)
      - 20 個「相同」對(b3-b3 或 p3-p3)
    """

    def __init__(self, output_dir: str = "stimuli/auditory_baseline",
                 compensate_vowel: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.talkers = build_talkers()
        self.rng = np.random.default_rng(42)  # 固定種子，可重現
        # True: 母音反向補償，讓「子音+母音」總長固定 -> 受試者只能用子音時長判斷，
        #       不能靠整個音節長短抄捷徑。
        self.compensate_vowel = compensate_vowel

    def _durations_for_diff(self, duration_diff_ms):
        """
        把「要求的子音時長差異」換算成 b 和 p 各自的絕對時長(ms)。

        以中點 CONS_MID_DUR(=105 ms) 為軸對稱分配：
            b = 中點 - diff/2   (較短)
            p = 中點 + diff/2   (較長)
        所以 p - b 恰好等於 duration_diff_ms，且要求 30 ms 時會回到
        原始基準 b=90 / p=120。

        若 compensate_vowel，母音反向調整，使 cons+vowel 恆為
        CONS_MID_DUR + VOWEL_DUR。
        """
        b_cons = CONS_MID_DUR - duration_diff_ms / 2.0
        p_cons = CONS_MID_DUR + duration_diff_ms / 2.0
        if b_cons <= 0:
            raise ValueError(
                f"duration_diff_ms={duration_diff_ms} 太大: b 的子音時長會變成 "
                f"{b_cons:.1f} ms。上限為 {2 * CONS_MID_DUR:.0f} ms。")
        if self.compensate_vowel:
            b_vowel = VOWEL_DUR + (CONS_MID_DUR - b_cons)
            p_vowel = VOWEL_DUR + (CONS_MID_DUR - p_cons)
        else:
            b_vowel = p_vowel = float(VOWEL_DUR)
        return (b_cons, b_vowel), (p_cons, p_vowel)

    def generate(self, n_trials: int = 40) -> str:
        """
        產生 40 組刺激並輸出 CSV

        Parameters
        ----------
        n_trials : int
            總刺激數（預設 40 = 20 不同對 + 20 相同對）

        Returns
        -------
        str
            輸出 CSV 路徑
        """
        n_different = n_trials // 2  # 20
        n_same = n_trials - n_different  # 20

        # 生成時長差異分佈（5–30ms）
        duration_diffs = self.rng.uniform(5, 30, n_different)

        # 生成隨機 talker 指派（每組獨立）
        talker_indices = self.rng.integers(0, len(self.talkers), n_trials)

        rows = []

        # ── 不同對 (b3 vs p3) ──
        for i in range(n_different):
            talker = self.talkers[talker_indices[i]]
            duration_diff = duration_diffs[i]

            # 以中點對稱分配，讓 p - b 恰好等於要求的差異。
            # (舊版把兩個時長同乘 1/scale，差異會變成 base_diff/scale，
            #  方向剛好相反 —— 要求 5 ms 會得到 180 ms。)
            (b3_cons, b3_vowel), (p3_cons, p3_vowel) = self._durations_for_diff(duration_diff)

            # 合成
            b3_path = self.output_dir / f"trial_{i+1:03d}_b3_{talker['id']}.wav"
            p3_path = self.output_dir / f"trial_{i+1:03d}_p3_{talker['id']}.wav"

            success_b, _ = synthesize_single('b', talker, str(b3_path),
                                             cons_dur_ms=b3_cons, vowel_dur_ms=b3_vowel)
            success_p, _ = synthesize_single('p', talker, str(p3_path),
                                             cons_dur_ms=p3_cons, vowel_dur_ms=p3_vowel)

            if success_b and success_p:
                rows.append({
                    'trial_num': i + 1,
                    'trial_type': 'different',
                    'consonant1': 'b',
                    'consonant2': 'p',
                    'talker_id': talker['id'],
                    'duration_diff_ms': round(duration_diff, 1),
                    'cons1_dur_ms': round(b3_cons, 1),
                    'cons2_dur_ms': round(p3_cons, 1),
                    'vowel1_dur_ms': round(b3_vowel, 1),
                    'vowel2_dur_ms': round(p3_vowel, 1),
                    'file1': str(b3_path.relative_to(self.output_dir.parent)),
                    'file2': str(p3_path.relative_to(self.output_dir.parent)),
                })

        # ── 相同對 (control) ──
        for i in range(n_same):
            talker = self.talkers[talker_indices[n_different + i]]
            # 隨機選 b 或 p
            cons = self.rng.choice(['b', 'p'])

            wav1_path = self.output_dir / f"trial_{n_different + i + 1:03d}_{cons}3_a_{talker['id']}.wav"
            wav2_path = self.output_dir / f"trial_{n_different + i + 1:03d}_{cons}3_b_{talker['id']}.wav"

            # 兩個檔案相同內容(同子音、同時長)。用中點時長，讓 control 的
            # 音節長度跟 different 條件一致，不會單憑長度就分辨出試次類型。
            ctrl_cons = CONS_MID_DUR
            ctrl_vowel = float(VOWEL_DUR)
            success1, _ = synthesize_single(cons, talker, str(wav1_path),
                                            cons_dur_ms=ctrl_cons, vowel_dur_ms=ctrl_vowel)
            success2, _ = synthesize_single(cons, talker, str(wav2_path),
                                            cons_dur_ms=ctrl_cons, vowel_dur_ms=ctrl_vowel)

            if success1 and success2:
                rows.append({
                    'trial_num': n_different + i + 1,
                    'trial_type': 'same',
                    'consonant1': cons,
                    'consonant2': cons,
                    'talker_id': talker['id'],
                    'duration_diff_ms': 0.0,
                    'cons1_dur_ms': round(ctrl_cons, 1),
                    'cons2_dur_ms': round(ctrl_cons, 1),
                    'vowel1_dur_ms': round(ctrl_vowel, 1),
                    'vowel2_dur_ms': round(ctrl_vowel, 1),
                    'file1': str(wav1_path.relative_to(self.output_dir.parent)),
                    'file2': str(wav2_path.relative_to(self.output_dir.parent)),
                })

        # ── 輸出 CSV ──
        csv_path = self.output_dir.parent / "auditory_baseline_trials.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
            writer.writeheader()
            writer.writerows(rows)

        print(f"✓ 已產生 {len(rows)} 個刺激")
        print(f"  - 不同對(b vs p): {n_different}")
        print(f"  - 相同對(control): {n_same}")
        print(f"  - 輸出 CSV: {csv_path}")

        return str(csv_path)


if __name__ == "__main__":
    print("=== 聽覺基準線刺激產生 ===\n")

    try:
        # 檢查 MBROLA voices
        for name, cfg in VOICES.items():
            if not os.path.exists(cfg['path']):
                print(f"✗ {name} 未安裝")
                print(f"  install: sudo apt-get install mbrola-{name}")
                exit(1)

        # 產生刺激
        baseline = AuditoryBaselineStimuli()
        csv_path = baseline.generate(n_trials=40)
        print(f"\n✓ 完成：{csv_path}")

    except Exception as e:
        print(f"✗ 錯誤: {e}")
        exit(1)
