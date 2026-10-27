"""
即時生成語音刺激(b3, p3 等)的函式模組。
用於 PsychoPy 實驗中動態產生音檔，而不是依賴預先生成的靜態檔案。

使用方式：
  - 在 PsychoPy Builder 的 Begin Experiment code 區塊裡 import 這個模組
  - 在需要音檔的地方呼叫 generate_speech_wav() 產生音檔路徑
  - 將路徑傳給 psychopy.sound.Sound()

範例:
  from generate_speech_stimulus import generate_speech_wav
  wav_path = generate_speech_wav("[[b3:]]", output_dir="/tmp")
  sound = sound.Sound(wav_path)
"""

import subprocess
import os
import tempfile
from pathlib import Path


def generate_speech_wav(
    phoneme_or_word,
    output_dir=None,
    lang="en",
    voice_speed=1.0,
):
    """
    用 espeak-ng 即時生成單個語音刺激的 WAV 檔案。

    Parameters
    ----------
    phoneme_or_word : str
        要生成的輸入:
        - 普通英文單字: "bur", "per", "asha"
        - 直接音素序列(繞過字典): "[[b3:]]", "[[p3:]]"
          (參見 espeak-ng 說明文件,格式: [[音素1音素2:...]] )
    output_dir : str, optional
        輸出目錄。若 None 則用系統暫存目錄(會自動清理)。
        若指定,檔案會保留在該目錄。
    lang : str
        espeak-ng 語言代碼(default: "en")
    voice_speed : float
        語速倍數(default: 1.0 = 正常速度)

    Returns
    -------
    str
        生成的 WAV 檔案路徑。若指定 output_dir,路徑會持久；
        若用暫存目錄,檔案在程式結束時會被刪除,但在 PsychoPy 播放期間保持有效。

    Raises
    ------
    RuntimeError
        espeak-ng 呼叫失敗(通常是系統未安裝 espeak-ng)。
    """

    # 決定輸出位置
    if output_dir is None:
        # 用 Python 暫存目錄(會自動清理,但 WAV 在使用期間保持有效)
        temp_dir = tempfile.gettempdir()
        # 替 phoneme_or_word 產生檔名: 特殊字元用 _ 取代
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in phoneme_or_word)
        output_path = os.path.join(temp_dir, f"psychopy_speech_{safe_name}.wav")
    else:
        # 使用指定目錄
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in phoneme_or_word)
        output_path = os.path.join(output_dir, f"speech_{safe_name}.wav")

    # 構建 espeak-ng 命令
    cmd = ["espeak-ng", "-v", lang]
    if voice_speed != 1.0:
        cmd.extend(["-s", str(int(175 * voice_speed))])  # 詞/分鐘(default ~175)
    cmd.extend(["-w", output_path, phoneme_or_word])

    # 執行 espeak-ng
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        raise RuntimeError(
            "espeak-ng not found. Install it via: apt-get install espeak-ng (Debian/Ubuntu) "
            "or brew install espeak-ng (macOS)"
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"espeak-ng failed: {e.stderr}")

    if not os.path.exists(output_path):
        raise RuntimeError(f"Failed to generate WAV at {output_path}")

    return output_path


def get_phoneme_ipa(phoneme_or_word, lang="en"):
    """
    用 espeak-ng --ipa 查詢輸入的 IPA 轉錄。
    方便在實驗中顯示或記錄所使用的發音。

    Parameters
    ----------
    phoneme_or_word : str
        同 generate_speech_wav() 的輸入
    lang : str
        espeak-ng 語言代碼

    Returns
    -------
    str
        IPA 轉錄(e.g., "bˈɜː" 對於 "[[b3:]]")
    """
    cmd = ["espeak-ng", "--ipa", "-q", "-v", lang, phoneme_or_word]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"[IPA lookup failed: {e}]"


# ============================================================================
# 預設刺激集 (可直接在實驗中參考)
# ============================================================================

SPEECH_STIMULI = {
    "b3": {
        "phoneme": "[[b3:]]",
        "ipa_expected": "bˈɜː",
        "description": "b + ɜː (schwa-r vowel, pitch-matched)"
    },
    "p3": {
        "phoneme": "[[p3:]]",
        "ipa_expected": "pˈɜː",
        "description": "p + ɜː (schwa-r vowel, pitch-matched)"
    },
    "be": {
        "phoneme": "be",
        "ipa_expected": "bˈiː",
        "description": "English 'be' letter"
    },
    "pe": {
        "phoneme": "pe",
        "ipa_expected": "pˈiː",
        "description": "English 'pe' letter (hypothetical)"
    },
    "asha": {
        "phoneme": "asha",
        "ipa_expected": "ˈæʃə",
        "description": "Test syllable (original VAWM)"
    }
}


if __name__ == "__main__":
    # 測試: 生成常用刺激
    import tempfile
    test_dir = tempfile.mkdtemp(prefix="psychopy_test_")
    print(f"Generating test stimuli to {test_dir}\n")

    for name, config in SPEECH_STIMULI.items():
        try:
            path = generate_speech_wav(
                config["phoneme"],
                output_dir=test_dir
            )
            ipa = get_phoneme_ipa(config["phoneme"])
            size_kb = os.path.getsize(path) / 1024
            print(f"✓ {name:6} → {path}")
            print(f"  IPA: {ipa:15} (expected: {config['ipa_expected']})")
            print(f"  Size: {size_kb:.1f} KB\n")
        except Exception as e:
            print(f"✗ {name}: {e}\n")
