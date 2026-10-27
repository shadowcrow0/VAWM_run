"""
完整刺激產生 pipeline
- 18 talkers (3 base voices × 6 VTL/F0 combos)
- 所有 confusion_analysis.csv 裡的子音
- 音節結構為 /Cɜ/（子音 + rhotic 央元音 [ɜ]，MBROLA symbol 'r='）
- 每個 phone 都明確標註起訖音高 anchor，強制全程 F0 保持平坦，
  避免不同子音（尤其濁/清子音）因為沒有明確音高標記而在銜接處出現
  忽平忽揚的不一致（先前 p3.wav/b3.wav 測試就發現這個問題）
- 輸出 PsychoPy conditions.csv

使用方式：
  sudo apt-get install mbrola mbrola-us1 mbrola-us2 mbrola-us3
  python GetAudioStim.py
"""

import subprocess
import os
import csv

# ══════════════════════════════════════════════
#  設定
# ══════════════════════════════════════════════

# MBROLA voice paths
VOICES = {
    "us1": {"path": "/usr/share/mbrola/us1/us1", "base_pitch": 180, "label": "F"},
    "us2": {"path": "/usr/share/mbrola/us2/us2", "base_pitch": 115, "label": "M1"},
    "us3": {"path": "/usr/share/mbrola/us3/us3", "base_pitch": 125, "label": "M2"},
}

# 18 talkers: 每個 base voice × 6 個 (VTL, F0_ratio) 組合
# VTL 範圍: 15000-17000
# F0 ratio: 拉開差異
TALKER_GRID = {
    "us1": [
        # (voice_freq, pitch_ratio)
        (15000, 0.85),
        (15500, 0.95),
        (16000, 1.00),
        (16000, 1.10),
        (16500, 1.05),
        (17000, 1.15),
    ],
    "us2": [
        # 3 talkers — VTL 分散，F0 拉開
        (15000, 0.88),
        (16000, 1.00),
        (17000, 1.12),
    ],
    "us3": [
        # 3 talkers — 跟 us2 錯開，避免重疊
        (15500, 0.92),
        (16500, 1.05),
        (17000, 0.85),
    ],
}

# 子音名稱 → MBROLA SAMPA
CONS_SAMPA = {
    'p': 'p', 'b': 'b', 't': 't', 'd': 'd',
    'k': 'k', 'g': 'g', 'f': 'f', 'v': 'v',
    'theta': 'T', 'eth': 'D',
    's': 's', 'z': 'z', 'sh': 'S', 'zh': 'Z',
    'tch': 'tS', 'dj': 'dZ',
    'm': 'm', 'n': 'n',
    'l': 'l', 'r': 'r',
    'y': 'j', 'w': 'w'
}

# ── 速度控制 ──
SPEED_FACTOR = 1  # 1.0 = 原速, >1.0 = 較慢, <1.0 = 較快

# ── 延長控制 ──
VOWEL_STRESS_FACTOR = 1.5  # /Cɜ/ 只有一個母音，延長讓子音的辨識線索更清楚
CONSONANT_FACTOR = 1.5     # 子音延長倍數 (1.5 = 延長 50%)

# 基礎子音長度 (ms)，會乘上 SPEED_FACTOR 和 CONSONANT_FACTOR
_BASE_CONS_DUR = {
    'p': 80, 'b': 60, 't': 80, 'd': 60, 'k': 80, 'g': 60,
    'f': 130, 'v': 100, 'T': 130, 'D': 100,
    's': 140, 'z': 110, 'S': 140, 'Z': 110,
    'tS': 120, 'dZ': 100,
    'm': 90, 'n': 90,
    'l': 90, 'r': 90, 'j': 80, 'w': 80,
}
CONS_DURATIONS = {k: int(v * SPEED_FACTOR * CONSONANT_FACTOR) for k, v in _BASE_CONS_DUR.items()}

# 母音 [ɜ] 長度 (ms)
BASE_VOWEL_DUR = 250
VOWEL_DUR = int(BASE_VOWEL_DUR * SPEED_FACTOR * VOWEL_STRESS_FACTOR)

# 前後靜音 (ms)
SILENCE_DUR = int(50 * SPEED_FACTOR)  # 75ms at 1.5x

# MBROLA 音素符號：rhotic 央元音 [ɜ]（美式 us1/us2/us3 資料庫裡的 syllabic r）
VOWEL_SAMPA = "r="


# ══════════════════════════════════════════════
#  建立 talker list
# ══════════════════════════════════════════════

def build_talkers():
    """產生 18 個 talker 的定義"""
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
                'label': f"{VOICES[voice_name]['label']}_vf{vf}_fr{fr:.2f}",
            })
    return talkers


# ══════════════════════════════════════════════
#  PHO 產生 + 合成
# ══════════════════════════════════════════════

def make_pho(cons_sampa, base_pitch, vowel_dur=None, consonant_factor=1.0):
    """產生 /Cɜ/ 的 .pho，全程 F0 完全平坦（不升不降）

    每個 phone（子音、母音都算）都在起訖各給同一個音高 anchor，
    才能保證清子音／濁子音銜接到母音時 MBROLA 不會用各自 diphone
    的天然音高去內插出忽平忽揚的輪廓。

    Args:
        cons_sampa: MBROLA SAMPA 格式的子音 (e.g., 'p', 'T', 'S')
        base_pitch: 基頻 (Hz)，全程固定
        vowel_dur: 母音長度 (ms)，預設使用 VOWEL_DUR
        consonant_factor: 子音時長倍數 (1.0=基準, <1.0=縮短, >1.0=延長)，用於 adaptive 實驗
    """
    if vowel_dur is None:
        vowel_dur = VOWEL_DUR
    cons_dur = int(CONS_DURATIONS.get(cons_sampa, int(100 * SPEED_FACTOR * CONSONANT_FACTOR)) * consonant_factor)

    def flat(dur):
        return f"(0,{base_pitch}) (100,{base_pitch})"

    if cons_sampa in ('tS', 'dZ'):
        d1, d2 = cons_dur // 2, cons_dur // 2
        cons_line = f"{cons_sampa[0]} {d1} {flat(d1)}\n{cons_sampa[1]} {d2} {flat(d2)}"
    else:
        cons_line = f"{cons_sampa} {cons_dur} {flat(cons_dur)}"

    return (
        f"_ {SILENCE_DUR}\n"
        f"{cons_line}\n"
        f"{VOWEL_SAMPA} {vowel_dur} {flat(vowel_dur)}\n"
        f"_ {SILENCE_DUR}\n"
    )


def synthesize(cons_sampa, talker, output_wav, consonant_factor=1.0):
    """用 MBROLA 合成一個 /Cɜ/

    Args:
        cons_sampa: 子音 (e.g., 'p', 'b')
        talker: talker 字典
        output_wav: 輸出 WAV 路徑
        consonant_factor: 子音時長倍數，用於 adaptive 實驗
    """
    cfg = VOICES[talker['voice']]
    pho_content = make_pho(cons_sampa, cfg['base_pitch'], consonant_factor=consonant_factor)
    pho_file = "/tmp/_gen_stim.pho"

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


# ══════════════════════════════════════════════
#  主程式
# ══════════════════════════════════════════════

def main():
    # 1. 檢查 voices
    print("Checking MBROLA voices...")
    for name, cfg in VOICES.items():
        if os.path.exists(cfg['path']):
            print(f"  ✓ {name} ({cfg['label']})")
        else:
            print(f"  ✗ {name} — install: sudo apt-get install mbrola-{name}")
            return

    # 2. 讀 CSV
    csv_path = "confuse.csv"
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), "confuse.csv")

    with open(csv_path, "r") as f:
        rows = list(csv.DictReader(f))
    print(f"\nRead {len(rows)} rows from CSV")

    # 收集所有需要的子音
    all_cons = set()
    for row in rows:
        all_cons.add(row['sound'])
        all_cons.add(row['target'])
    all_cons = sorted(all_cons)
    print(f"Consonants to generate: {all_cons}")

    # 3. 建立 talkers
    talkers = build_talkers()
    print(f"\nTalkers: {len(talkers)}")
    for t in talkers:
        print(f"  {t['id']}: {t['voice']} vf={t['voice_freq']} fr={t['pitch_ratio']:.2f}")

    # 4. 產生所有 wav（扁平結構：T01_p3.wav，代表 /pɜ/）
    wav_dir = "stimuli"
    os.makedirs(wav_dir, exist_ok=True)
    total_files = len(all_cons) * len(talkers)
    print(f"\nGenerating {len(all_cons)} consonants × {len(talkers)} talkers = {total_files} wav files...")

    success = 0
    fail = 0

    for talker in talkers:
        tid = talker['id']
        for cons_name in all_cons:
            if cons_name not in CONS_SAMPA:
                print(f"  SKIP: {cons_name}")
                continue

            sampa = CONS_SAMPA[cons_name]
            wav_path = os.path.join(wav_dir, f"{tid}_{cons_name}3.wav")

            ok, err = synthesize(sampa, talker, wav_path)
            if ok:
                success += 1
            else:
                fail += 1
                print(f"  ✗ {tid}_a{cons_name}a: {err}")

    print(f"\nGenerated: {success} OK, {fail} failed")

    # 5. 產生 PsychoPy conditions.csv
    # 每個 CSV row × 每個 talker = 一個 trial
    conditions_path = "stimuli/conditions.csv"
    fieldnames = [
        'sound', 'target', 'confused', 'count',
        'sound_file', 'target_file',
        'talker', 'voice_base', 'condition',
    ]

    trial_count = 0
    with open(conditions_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            sound = row['sound']
            target = row['target']
            confused = int(row['confused'])
            count = int(row['count'])
            condition = "confusable" if confused == 0 else "distinct"

            for talker in talkers:
                tid = talker['id']
                sound_file = f"{tid}_{sound}3.wav"
                target_file = f"{tid}_{target}3.wav"

                writer.writerow({
                    'sound': sound,
                    'target': target,
                    'confused': confused,
                    'count': count,
                    'sound_file': sound_file,
                    'target_file': target_file,
                    'talker': tid,
                    'voice_base': talker['voice'],
                    'condition': condition,
                })
                trial_count += 1

    print(f"Conditions file: {conditions_path}")
    print(f"Total trials: {trial_count}")
    print(f"  = {len(rows)} pairs × {len(talkers)} talkers")

    # 6. 印出 talker 對照表
    talker_info_path = "stimuli/talker_info.csv"
    with open(talker_info_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['talker_id', 'base_voice', 'voice_freq', 'pitch_ratio'])
        writer.writeheader()
        for t in talkers:
            writer.writerow({
                'talker_id': t['id'],
                'base_voice': t['voice'],
                'voice_freq': t['voice_freq'],
                'pitch_ratio': t['pitch_ratio'],
            })
    print(f"Talker info: {talker_info_path}")

    # 7. PsychoPy 說明
    print(f"""
{'=' * 50}
PsychoPy 設定：

1. 把 stimuli/ 資料夾放進實驗目錄

2. Loop 設定：
   - conditions file: stimuli/conditions.csv
   - 如果 1728 trials 太多，可以：
     a. 用 nReps=1 但只選部分 talker
        （在 conditions.csv 裡 filter by talker）
     b. 或用 random sampling: Selected rows = 隨機取子集

3. Trial routine：
   - Sound component: $sound_file
   - 受試者做 identification: 聽到什麼子音？
   - Response: keyboard 或 button box

4. 分析時用 condition 欄位區分 confusable vs distinct

目錄結構（扁平格式）：
  stimuli/
    conditions.csv      ← PsychoPy loop 讀這個
    talker_info.csv     ← talker 參數對照表
    T01_p3.wav          ← 扁平檔名：{{talker}}_{{cons}}3.wav，音節為 /Cɜ/
    T01_b3.wav
    T02_p3.wav
    ...
""")


def generate_155_trials(rows, talkers, output_path="stimuli/audio_155trials.csv"):
    """產生 155 組雙音訊 (audio1 + audio2) 配對 CSV

    每組包含兩組獨立的音訊：
    - audio1_target, audio1_H, audio1_L (同一個 talker)
    - audio2_target, audio2_H, audio2_L (同一個 talker，但可與 audio1 不同)

    重要限制：
    1. 同一組內的 target/H/L 用同一個人講，不同 trial 用不同人
    2. 同一 trial 內：audio1_target ≠ audio2_target
    3. 前後 trial 之間：當前 trial 的 targets 要和前一個 trial 的 targets 不同
    """
    import random

    # 建立每個 sound 的 H/L 配對字典
    sound_pairs = {}
    for row in rows:
        sound = row['sound']
        target = row['target']
        confused = int(row['confused'])
        count = int(row['count'])

        if sound not in sound_pairs:
            sound_pairs[sound] = {'H': [], 'L': []}

        if confused == 1:  # H: 高辨識度 (不常混淆)
            sound_pairs[sound]['H'].append({'target': target, 'count': count})
        else:  # L: 低辨識度 (常混淆)
            sound_pairs[sound]['L'].append({'target': target, 'count': count})

    # 找出有 H 和 L 配對的 sounds
    valid_sounds = [s for s, pairs in sound_pairs.items()
                    if pairs['H'] and pairs['L']]
    print(f"\nValid sounds with both H and L pairs: {valid_sounds}")
    print(f"Talkers available: {len(talkers)}")
    print(f"Same talker for target/H/L within each audio set, different talkers across trials")
    print(f"Constraints: audio1_target ≠ audio2_target, and distinct from previous trial")

    def pick_one_set(sound_pairs, valid_sounds, talker_id, exclude_sounds=None):
        """產生一組 target/H/L，全部用同一個 talker

        Args:
            exclude_sounds: 要排除的 sound 列表（用於確保 distinct）
        """
        if exclude_sounds is None:
            exclude_sounds = []

        # 過濾掉要排除的 sounds
        available_sounds = [s for s in valid_sounds if s not in exclude_sounds]
        if not available_sounds:
            # 如果全部被排除，fallback 到原本的 valid_sounds
            available_sounds = valid_sounds

        sound = random.choice(available_sounds)
        l_choice = random.choice(sound_pairs[sound]['L'])
        h_choice = random.choice(sound_pairs[sound]['H'])
        return {
            'target': sound,
            'H': h_choice['target'],
            'L': l_choice['target'],
            'H_count': h_choice['count'],
            'L_count': l_choice['count'],
            'target_talker': talker_id,
            'H_talker': talker_id,
            'L_talker': talker_id,
            'target_file': f"stimuli/{talker_id}_{sound}3.wav",
            'H_file': f"stimuli/{talker_id}_{h_choice['target']}3.wav",
            'L_file': f"stimuli/{talker_id}_{l_choice['target']}3.wav",
        }

    # 產生 155 組雙音訊配對
    trials = []
    prev_targets = []  # 上一個 trial 的 targets，用於確保前後 trial distinct

    for trial_num in range(1, 156):
        # 為這個 trial 隨機選 2 個 talker（audio1 和 audio2 各一個）
        selected = random.sample(talkers, 2)
        talker1 = selected[0]['id']
        talker2 = selected[1]['id']

        # 產生 audio1：排除上一個 trial 的 targets
        set1 = pick_one_set(sound_pairs, valid_sounds, talker1, exclude_sounds=prev_targets)

        # 產生 audio2：排除上一個 trial 的 targets + audio1 的 target
        exclude_for_set2 = prev_targets + [set1['target']]
        set2 = pick_one_set(sound_pairs, valid_sounds, talker2, exclude_sounds=exclude_for_set2)

        # 更新 prev_targets 給下一個 trial 用
        prev_targets = [set1['target'], set2['target']]

        row = {'trial': trial_num}
        # audio1 欄位
        for k, v in set1.items():
            row[f'audio1_{k}'] = v
        # audio2 欄位
        for k, v in set2.items():
            row[f'audio2_{k}'] = v

        trials.append(row)

    # 寫入 CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=trials[0].keys())
        writer.writeheader()
        writer.writerows(trials)

    print(f"\n155 trials saved to: {output_path}")
    print(f"Columns: trial, audio1_target, audio1_H, audio1_L, ..., audio2_target, audio2_H, audio2_L, ...")

    return trials


def merge_color_audio(color_csv, audio_csv, output_path="stimuli/combined_80trials.csv"):
    """合併 color 和 audio 的 80 組配對 CSV"""

    # 讀取兩個 CSV
    with open(color_csv, 'r') as f:
        color_rows = list(csv.DictReader(f))

    with open(audio_csv, 'r') as f:
        audio_rows = list(csv.DictReader(f))

    # 確保都有 80 筆
    if len(color_rows) != 80 or len(audio_rows) != 80:
        print(f"Warning: color has {len(color_rows)} rows, audio has {len(audio_rows)} rows")

    # 合併
    combined = []
    for i in range(min(len(color_rows), len(audio_rows))):
        row = {'trial': i + 1}

        # 加入 color 欄位 (加上 prefix)
        for k, v in color_rows[i].items():
            if k != 'trial':
                row[k] = v

        # 加入 audio 欄位 (columns already have audio1_/audio2_ prefix)
        for k, v in audio_rows[i].items():
            if k != 'trial':
                row[k] = v

        combined.append(row)

    # 寫入合併的 CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=combined[0].keys())
        writer.writeheader()
        writer.writerows(combined)

    print(f"\nCombined CSV saved to: {output_path}")
    print(f"Total trials: {len(combined)}")
    return combined


def distinct_aware_shuffle(rows):
    """打亂順序但確保前後 trial 的 targets 不重複

    使用 greedy 演算法：
    1. 隨機選一個 trial 作為起點
    2. 每次從剩餘的 trials 中選一個不與前一個 trial 重疊的 trial
    3. 如果沒有符合條件的 trial，fallback 到任意剩餘 trial
    """
    import random

    if not rows:
        return []

    def get_targets(row):
        """取得一個 trial 的所有 targets"""
        return {row.get('audio1_target', ''), row.get('audio2_target', '')} - {''}

    remaining = list(rows)
    random.shuffle(remaining)  # 先打亂以增加隨機性
    result = [remaining.pop(0)]  # 隨機選第一個

    while remaining:
        prev_targets = get_targets(result[-1])

        # 找出所有不與前一個 trial 重疊的 trials
        valid_candidates = []
        for i, row in enumerate(remaining):
            curr_targets = get_targets(row)
            if not (prev_targets & curr_targets):  # 沒有交集
                valid_candidates.append(i)

        if valid_candidates:
            # 從符合條件的 trials 中隨機選一個
            idx = random.choice(valid_candidates)
        else:
            # Fallback: 沒有符合條件的，隨機選一個
            idx = random.randint(0, len(remaining) - 1)

        result.append(remaining.pop(idx))

    return result


def split_into_blocks(combined_csv, output_dir="stimuli"):
    """將 combined CSV 分割成 practice.csv 和 block1-6.csv

    分配方式：
    - practice.csv: 前 5 trials
    - block1.csv: trials 6-30 (25 trials)
    - block2.csv: trials 31-55 (25 trials)
    - block3.csv: trials 56-80 (25 trials)
    - block4.csv: trials 81-105 (25 trials)
    - block5.csv: trials 106-130 (25 trials)
    - block6.csv: trials 131-155 (25 trials)

    注意：使用 distinct-aware shuffle 確保前後 trial 的 targets 不重複
    """
    # 讀取 combined CSV
    with open(combined_csv, 'r') as f:
        rows = list(csv.DictReader(f))

    # 使用 distinct-aware shuffle 打亂順序
    rows = distinct_aware_shuffle(rows)

    # 重新編號
    for i, row in enumerate(rows):
        row['trial'] = i + 1

    fieldnames = rows[0].keys()

    # 分割
    practice = rows[0:5]
    blocks = [
        rows[5:30],    # block1: 25 trials
        rows[30:55],   # block2: 25 trials
        rows[55:80],   # block3: 25 trials
        rows[80:105],  # block4: 25 trials
        rows[105:130], # block5: 25 trials
        rows[130:155], # block6: 25 trials
    ]

    # 寫入 practice.csv
    practice_path = os.path.join(output_dir, "practice.csv")
    with open(practice_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # 重新編號 practice trials
        for i, row in enumerate(practice):
            row['trial'] = i + 1
        writer.writerows(practice)
    print(f"  practice.csv: {len(practice)} trials")

    # 寫入 block1-6.csv
    for i, block in enumerate(blocks):
        block_path = os.path.join(output_dir, f"block{i+1}.csv")
        with open(block_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            # 重新編號 block trials
            for j, row in enumerate(block):
                row['trial'] = j + 1
            writer.writerows(block)
        print(f"  block{i+1}.csv: {len(block)} trials")

    print(f"\nTotal: {len(practice) + sum(len(b) for b in blocks)} trials")


if __name__ == "__main__":
    main()

    # 額外產生 155 組 target/H/L 配對
    print("\n" + "=" * 50)
    print("Generating 155 target/H/L trials...")

    csv_path = "confuse.csv"
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), "confuse.csv")

    with open(csv_path, "r") as f:
        rows = list(csv.DictReader(f))

    talkers = build_talkers()
    generate_155_trials(rows, talkers)

    # 合併 color 和 audio CSV
    print("\n" + "=" * 50)
    print("Merging color and audio trials...")

    color_csv = "stimuli/color_155trials.csv"
    audio_csv = "stimuli/audio_155trials.csv"

    if not os.path.exists(color_csv):
        color_csv = os.path.join(os.path.dirname(__file__), "stimuli/color_155trials.csv")
    if not os.path.exists(audio_csv):
        audio_csv = os.path.join(os.path.dirname(__file__), "stimuli/audio_155trials.csv")

    if os.path.exists(color_csv) and os.path.exists(audio_csv):
        merge_color_audio(color_csv, audio_csv, "stimuli/combined_155trials.csv")

        # 分割成 practice + block1-6
        print("\n" + "=" * 50)
        print("Splitting into practice.csv and block1-6.csv...")
        split_into_blocks("stimuli/combined_155trials.csv")
    else:
        print(f"Missing files: color={os.path.exists(color_csv)}, audio={os.path.exists(audio_csv)}")