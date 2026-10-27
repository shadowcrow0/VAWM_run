"""
如何在 PsychoPy 實驗中使用即時生成的語音刺激

有三種整合方式:
1. 在 Begin Experiment code 初始化,預先生成所有音檔
2. 在 Begin Routine code 動態產生當次試驗的音檔
3. 在 Loop 層級設定,每個試驗動態產生

"""

# ============================================================================
# 方式 1: Begin Experiment (推薦用於預先計畫、穩定的刺激集)
# ============================================================================

# 貼進 PsychoPy Builder 的 "Begin Experiment" 程式碼區塊:

"""
from generate_speech_stimulus import generate_speech_wav, SPEECH_STIMULI
import os

# 初始化字典,儲存所有生成的音檔路徑
speech_audio_paths = {}

# 為每個預定義的刺激集生成音檔
for stim_name, config in SPEECH_STIMULI.items():
    try:
        path = generate_speech_wav(config["phoneme"])
        speech_audio_paths[stim_name] = path
        print(f"Pregenerated: {stim_name} → {path}")
    except Exception as e:
        print(f"Failed to generate {stim_name}: {e}")
"""


# ============================================================================
# 方式 2: Begin Routine (推薦用於動態、隨試驗變化的刺激)
# ============================================================================

# 假設你的 CSV 條件檔有欄位: speech_stimulus (值例如 "b3", "p3")
# 貼進 PsychoPy Builder 的 "Begin Routine" 程式碼區塊:

"""
from generate_speech_stimulus import generate_speech_wav

# 讀取本次試驗要用的語音刺激名稱(來自 CSV 條件欄位)
stimulus_name = speech_stimulus  # 這個變數由 PsychoPy 條件檔自動設定

# 即時生成音檔
try:
    wav_path = generate_speech_wav(f"[[{stimulus_name}:]]")
    # 將路徑指派給音聲元件的 setSound() 方法
    targetAud.setSound(wav_path)  # targetAud 是你在 Builder 裡定義的 Sound 元件名稱
    print(f"Generated and loaded: {stimulus_name}")
except Exception as e:
    print(f"Error generating {stimulus_name}: {e}")
"""


# ============================================================================
# 方式 3: 完整範例 - 修改 VAWM.py
# ============================================================================

# 在 VAWM.py 的最上面加上:

"""
from generate_speech_stimulus import generate_speech_wav, get_phoneme_ipa
import tempfile
import os
"""

# 然後在實驗初始化區塊(原本的 "create a temporary folder..." 之後):

"""
# 設定語音刺激暫存目錄
speech_temp_dir = tempfile.mkdtemp(prefix="psychopy_vawm_speech_")
print(f"Speech stimuli will be generated in: {speech_temp_dir}")

# 預先生成常用的 b3, p3
common_stimuli = {
    "b3": "[[b3:]]",
    "p3": "[[p3:]]"
}
speech_cache = {}
for name, phoneme in common_stimuli.items():
    try:
        path = generate_speech_wav(phoneme, output_dir=speech_temp_dir)
        speech_cache[name] = path
        print(f"Cached: {name} → {path}")
    except Exception as e:
        print(f"Warning: Failed to cache {name}: {e}")
"""

# 在試驗迴圈裡,當要播放 b3/p3 時:

"""
# 取得本次試驗的音檔(先檢查快取,沒有的話即時產生)
target_stim = "b3"  # 或從 CSV 條件欄位讀取
if target_stim in speech_cache:
    wav_path = speech_cache[target_stim]
else:
    # 動態產生尚未快取的刺激
    wav_path = generate_speech_wav(f"[[{target_stim}:]]", output_dir=speech_temp_dir)
    speech_cache[target_stim] = wav_path

# 將路徑指派給 PsychoPy 的 Sound 元件
targetAud.setSound(wav_path)
targetAud.play()
"""


# ============================================================================
# 方式 4: 進階 - 搭配 CSV 條件檔(推薦用於完整實驗)
# ============================================================================

# 在你的條件 CSV (e.g., stimuli/practice.csv) 中加入欄位:
# target_audio_phoneme | target_audio_ipa_label
# [[b3:]]              | b3
# [[p3:]]              | p3
# [[p3:]]              | p3
# ...

# 然後在 Begin Routine code 裡:

"""
from generate_speech_stimulus import generate_speech_wav, get_phoneme_ipa

# 假設 CSV 欄位名稱為 target_audio_phoneme
phoneme_to_play = target_audio_phoneme  # PsychoPy 會自動填入 CSV 的值

# 即時產生
try:
    wav_path = generate_speech_wav(phoneme_to_play, output_dir=speech_temp_dir)
    ipa = get_phoneme_ipa(phoneme_to_play)  # 可選:記錄實際生成的 IPA

    # 指派給音檔元件
    targetAud.setSound(wav_path)

    # 記到輸出資料(用於後續檢驗)
    thisExp.addData('audio_generated_file', wav_path)
    thisExp.addData('audio_ipa', ipa)

except Exception as e:
    print(f"Error: {e}")
    thisExp.addData('audio_error', str(e))
"""

# CSV 範例:
"""
target_audio_phoneme,target_audio_label
[[b3:]],b3
[[p3:]],p3
[[b3:]],b3
"""
