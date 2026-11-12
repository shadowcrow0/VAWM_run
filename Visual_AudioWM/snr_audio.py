"""聽覺維度:把自然 [bi] 混進語音頻譜噪音,SNR 以 dB 指定。

設計(2026-08-25 變更)
---------------------
聲音刺激 = **單一自然 token [bi]**(Kutlu & McMurray beachpeach1 的 CV 剪裁版,
CC0),聲音維度 = **SNR(dB)**。不再是 b/p 端點對比 —— 受試者在校準階段
報告的類別就是「較吵 / 較清楚」,SNR 本身就是被判斷的維度,
因此可以直接餵給 AGRTHandler(舊 docstring「SNR 只是難度旋鈕、只能配
QuestHandler」的警告是針對「報告 be/pe 身分」的舊設計,已不適用)。

dB 本身已是對數尺度:音長要先取 log、色相角要換成 ΔE00 弧長才能滿足
「等物理間距 ≈ 等知覺間距」;dB 不需要任何變換。

噪音是 running noise(每 trial 新樣本,frozen noise 會被學會),
但每次的種子都可記錄(mix_at_snr_logged),事後可位元重建。

用法
----
    from snr_audio import mix_at_snr_logged, write_wav
    sr, y, seed = mix_at_snr_logged('bi', snr_db=-12.0)
    write_wav('trial.wav', sr, y)
"""

import wave
from pathlib import Path

import numpy as np

# ──────────────────────────────────────────────────────────────
# 設定
# ──────────────────────────────────────────────────────────────

SPEECH_FILES = {
    # 自然 [bi]:beachpeach1 剪除尾音 /tʃ/ 的 CV 版(單語者、44.1 kHz、CC0)。
    # LTAS(噪音的頻譜形狀)也由這個 token 估計。
    'bi': 'stimuli/kutlu_mcmurray_2024/cv/beachpeach1_cv.wav',
}
# Winn (2020) §II.D 建議用 /i/ 而非 /ɑ/:低母音的 F1 起始在有聲/無聲之間
# 差約 300 Hz,會變成與 VOT 共變的混淆線索。/i/ 的 F1 本來就低且穩定。
# 見 90_Sources/winn2020.md

TARGET_RMS = 0.05       # 兩個 token 對齊到相同的**有聲段** RMS。
                        # ⚠️ 不能用全檔 RMS:pe 的靜音/送氣段比 be 長,全檔 RMS
                        #   會低估它的有聲位準。實測用全檔 RMS 對齊之後,有聲段的
                        #   位準差反而從 1.07 dB 放大到 1.62 dB。
ONSET_LEAD_MS = 10.0    # 所有 token 的聲學起始都對齊到這個位置。
                        # ⚠️ 必要:實測 be 起始 9.0 ms、pe 起始 44.9 ms,差 35.9 ms
                        #   —— 比 /b/–/p/ 的整個 VOT 邊界區(約 20–25 ms)還大。
                        #   噪音蓋住頻譜細節之後,「什麼時候開始」會變成比 VOT 更強的
                        #   線索,受試者可以完全不聽語音就分辨出來。
ONSET_THRESH_DB = -40.0 # 聲學起始的判定門檻(相對於該檔峰值)
OUTPUT_RMS = 0.05       # 混音後整段再正規化到這個 RMS。
                        # ⚠ 這一步是必要的:若固定語音位準、只放大噪音,
                        #   SNR 越低整體就越大聲(實測 -30 dB 時峰值到 6.8,
                        #   會嚴重削波)。音量本身就會變成「這題很難」的線索,
                        #   而且低 SNR 試次會刺耳。固定輸出位準之後,
                        #   跨 SNR 的呈現音量一致,只有訊噪比在變。
NOISE_LEAD_MS = 200.0   # 噪音在語音之前先起來,否則噪音的起始點等於告訴
NOISE_TAIL_MS = 200.0   # 受試者語音在哪,變成額外線索
LTAS_NFFT = 1024        # 估長時平均頻譜用的窗長
PEAK_LIMIT = 0.95       # 輸出的峰值上限,避免削波


# ──────────────────────────────────────────────────────────────
# 基本工具
# ──────────────────────────────────────────────────────────────

def _rms(x):
    return float(np.sqrt(np.mean(np.asarray(x, dtype=float) ** 2)))


def _read_wav(path):
    with wave.open(str(path), 'rb') as w:
        if w.getsampwidth() != 2:
            raise ValueError(f"{path}:只支援 16-bit PCM,實際為 "
                             f"{w.getsampwidth() * 8}-bit")
        if w.getnchannels() != 1:
            raise ValueError(f"{path}:只支援單聲道,實際為 {w.getnchannels()} 聲道")
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return sr, x.astype(np.float64) / 32768.0


def write_wav(path, sr, y):
    """寫成 16-bit PCM。超過 PEAK_LIMIT 會等比壓下來並回報縮放量。"""
    y = np.asarray(y, dtype=float)
    peak = np.abs(y).max()
    scale = 1.0
    if peak > PEAK_LIMIT:
        scale = PEAK_LIMIT / peak
        y = y * scale
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    return scale


# ──────────────────────────────────────────────────────────────
# 語音:載入、RMS 正規化、時長對齊
# ──────────────────────────────────────────────────────────────

_SPEECH_CACHE = None


def _acoustic_onset(x, sr):
    """回傳聲學起始(樣本索引):短時能量首次超過峰值 ONSET_THRESH_DB 的位置。"""
    win = max(int(0.005 * sr), 1)
    hop = max(int(0.001 * sr), 1)
    e = np.array([10 * np.log10(np.mean(x[i:i + win] ** 2) + 1e-12)
                  for i in range(0, len(x) - win, hop)])
    if e.size == 0:
        return 0
    return int(np.argmax(e > e.max() + ONSET_THRESH_DB) * hop)


def _voiced_rms(x, sr, thr=0.5):
    """只取有週期性(有聲)的窗算 RMS。

    用它而非全檔 RMS,是因為各 token 的靜音/送氣比例不同,全檔 RMS 會
    系統性地低估送氣較長那一個的有聲位準。
    """
    win = int(0.025 * sr)
    hop = int(0.005 * sr)
    segs = []
    for i in range(0, len(x) - win, hop):
        f = x[i:i + win] - x[i:i + win].mean()
        if np.sqrt(np.mean(f ** 2)) < 1e-4:
            continue
        ac = np.correlate(f, f, 'full')[len(f) - 1:]
        ac = ac / (ac[0] + 1e-12)
        lo, hi = int(sr / 300), int(sr / 70)
        if hi < len(ac) and ac[lo:hi].max() > thr:
            segs.append(x[i:i + win])
    if not segs:
        raise ValueError("找不到有聲段 —— 檢查語音檔是否正常")
    return float(np.sqrt(np.mean(np.concatenate(segs) ** 2)))


def _load_speech():
    """載入全部 token,**對齊聲學起始**、對齊**有聲段** RMS、補到等長。

    三項對齊各自擋掉一個殘留線索:

    1. **聲學起始** —— 實測 be 起始 9.0 ms、pe 起始 44.9 ms,差 35.9 ms。
       這比 /b/–/p/ 的整個 VOT 邊界區還大,而且埋進噪音之後「什麼時候開始」
       比頻譜細節更容易聽出來。不對齊的話受試者可以不聽語音就作答。
    2. **有聲段 RMS** —— 不能用全檔 RMS(見 TARGET_RMS 的註解)。
    3. **總長** —— 補靜音到等長,避免長短本身成為線索。
    """
    global _SPEECH_CACHE
    if _SPEECH_CACHE is not None:
        return _SPEECH_CACHE

    here = Path(__file__).resolve().parent
    raw, sr0 = {}, None
    for name, fn in SPEECH_FILES.items():
        p = here / fn
        if not p.exists():
            raise FileNotFoundError(f"找不到語音檔:{p}")
        sr, x = _read_wav(p)
        if sr0 is None:
            sr0 = sr
        elif sr != sr0:
            raise ValueError(f"取樣率不一致:{fn} 是 {sr} Hz,其他是 {sr0} Hz")
        raw[name] = x

    # 1. 對齊聲學起始:把各 token 的起始都移到 ONSET_LEAD_MS
    lead = int(round(ONSET_LEAD_MS * sr0 / 1000.0))
    shifted = {}
    for name, x in raw.items():
        on = _acoustic_onset(x, sr0)
        if on >= lead:
            x = x[on - lead:]                       # 切掉多餘的前置靜音
        else:
            x = np.pad(x, (lead - on, 0))           # 前置靜音不足就補
        shifted[name] = x

    # 2. 補到等長  3. 依有聲段 RMS 正規化
    n = max(len(x) for x in shifted.values())
    out = {}
    for name, x in shifted.items():
        x = np.pad(x, (0, n - len(x)))
        out[name] = x * (TARGET_RMS / _voiced_rms(x, sr0))
    _SPEECH_CACHE = (sr0, out)
    return _SPEECH_CACHE


def speech_names():
    return tuple(SPEECH_FILES)


# ──────────────────────────────────────────────────────────────
# 噪音:語音頻譜噪音 (speech-shaped noise, SSN)
# ──────────────────────────────────────────────────────────────

_LTAS_CACHE = None


def _ltas():
    """所有 token 合併的長時平均頻譜。

    用 SSN 而非白噪音:白噪音對高頻過度遮蔽,SSN 讓遮蔽在各頻帶上與語音本身
    的能量分布相稱。
    """
    global _LTAS_CACHE
    if _LTAS_CACHE is not None:
        return _LTAS_CACHE

    sr, speech = _load_speech()
    win = np.hanning(LTAS_NFFT)
    hop = LTAS_NFFT // 2
    acc, cnt = np.zeros(LTAS_NFFT // 2 + 1), 0
    for x in speech.values():
        for i in range(0, len(x) - LTAS_NFFT, hop):
            acc += np.abs(np.fft.rfft(x[i:i + LTAS_NFFT] * win))
            cnt += 1
    if cnt == 0:
        raise ValueError("語音太短,不足一個 LTAS 分析窗")
    _LTAS_CACHE = (sr, acc / cnt, np.fft.rfftfreq(LTAS_NFFT, 1.0 / sr))
    return _LTAS_CACHE


def speech_shaped_noise(n_samples, rng=None):
    """產生 n_samples 點、頻譜形狀符合語音 LTAS 的噪音,RMS 正規化為 1。

    每次呼叫都用新的隨機樣本(running noise)。不要改成 frozen noise ——
    否則受試者會學會噪音圖樣。
    """
    rng = np.random.default_rng() if rng is None else rng
    sr, ltas, ltas_f = _ltas()

    w = rng.standard_normal(n_samples)
    W = np.fft.rfft(w)
    f = np.fft.rfftfreq(n_samples, 1.0 / sr)
    shape = np.interp(f, ltas_f, ltas)
    y = np.fft.irfft(W * shape, n=n_samples)
    return y / _rms(y)


# ──────────────────────────────────────────────────────────────
# 混音
# ──────────────────────────────────────────────────────────────

def mix_components(name, snr_db, rng=None):
    """回傳 (sr, speech_component, noise_component, lead_samples)。

    兩個成分都已經套用最終的輸出位準縮放,所以 speech + noise 就是要播的
    訊號,而兩者分別可以拿去量實際 SNR —— 不需要用「相減還原」的方式驗算
    (輸出正規化之後那樣算會錯)。
    """
    sr, speech = _load_speech()
    if name not in speech:
        raise KeyError(f"未知的 token:{name!r};可用的是 {tuple(speech)}")
    snr_db = float(snr_db)

    x = speech[name]
    lead = int(round(NOISE_LEAD_MS * sr / 1000.0))
    tail = int(round(NOISE_TAIL_MS * sr / 1000.0))
    total = lead + len(x) + tail

    noise = speech_shaped_noise(total, rng)
    # 只用語音重疊的那一段去定 SNR;前後的引導噪音不計入,
    # 否則 SNR 會隨引導長度改變。
    noise *= (_rms(x) / (10.0 ** (snr_db / 20.0))) / _rms(noise[lead:lead + len(x)])

    sp = np.zeros(total)
    sp[lead:lead + len(x)] = x

    gain = OUTPUT_RMS / _rms(sp + noise)      # 固定輸出位準
    return sr, sp * gain, noise * gain, lead


def mix_at_snr(name, snr_db, rng=None):
    """把 token `name` 以指定的 SNR(dB)混進語音頻譜噪音。

    回傳 (sample_rate, waveform)。waveform 為 float64。
    """
    sr, sp, nz, _ = mix_components(name, snr_db, rng)
    return sr, sp + nz


def realised_snr(name, snr_db, rng=None):
    """量實際做出來的 SNR,用來驗證 mix_at_snr 沒有算錯。"""
    sr, sp, nz, lead = mix_components(name, snr_db, rng)
    n = len(sp) - lead - int(round(NOISE_TAIL_MS * sr / 1000.0))
    seg = slice(lead, lead + n)
    return 20.0 * np.log10(_rms(sp[seg]) / _rms(nz[seg]))


def new_seed():
    """抽一個可記錄的噪音種子。"""
    return int(np.random.SeedSequence().entropy)


def mix_at_snr_logged(name, snr_db, seed=None):
    """與 mix_at_snr 相同,但額外回傳這一次用的噪音種子。

    回傳 (sample_rate, waveform, seed)。

    為什麼要記種子 —— running noise 每個 trial 都換新樣本,這是對的
    (frozen noise 會被學起來),但「每次都新」不等於「不可追溯」。
    噪音樣本本身不是中性的:在同型作業裡,單是噪音的隨機樣本就解釋了
    8-13% 的音素反應變異。不記種子的話,那部分變異就永遠只能當殘差,
    而且 double-pass 一致性(同一段噪音重播,看反應一不一致 -> 分離
    知覺雜訊與決策雜訊)與反向相關(哪些頻譜時間區域驅動了 /b/ 反應)
    這兩條分析路線會被永久關閉。

    成本是資料檔裡多一個整數欄位。把 seed 寫進 thisExp,日後用
    `speech_shaped_noise(n, np.random.default_rng(seed))` 就能重建
    出位元完全相同的那一段噪音。
    """
    if seed is None:
        seed = new_seed()
    seed = int(seed)
    sr, wav = mix_at_snr(name, snr_db, np.random.default_rng(seed))
    return sr, wav, seed


def render_at_snr(name, snr_db, path, seed=None):
    """混音後直接寫成 wav 檔;回傳實際使用的噪音種子。

    實驗執行期用這個:每 trial 新抽種子(seed=None),把回傳值記進資料檔;
    重建時把記下的 seed 傳回來,輸出位元完全相同。
    """
    sr, y, seed = mix_at_snr_logged(name, snr_db, seed)
    write_wav(path, sr, y)
    return seed


# ──────────────────────────────────────────────────────────────
# 自我檢查
# ──────────────────────────────────────────────────────────────

def validate():
    rng = np.random.default_rng(0)
    sr, speech = _load_speech()

    print("=" * 68)
    print("snr_audio —— 聽覺維度設定檢查")
    print("=" * 68)
    print(f"取樣率 {sr} Hz")
    for name, x in speech.items():
        print(f"  {name}: {len(x) / sr * 1000:7.1f} ms  RMS={_rms(x):.4f}  "
              f"peak={np.abs(x).max():.3f}")
    lens = {len(x) for x in speech.values()}
    rmss = [round(_rms(x), 6) for x in speech.values()]
    print(f"  時長已對齊:{'是' if len(lens) == 1 else '否 ✗'}"
          f"   RMS 已對齊:{'是' if len(set(rmss)) == 1 else '否 ✗'}")

    print("\n-- SNR 精度(要求值 vs 實際量回來的值)------------------")
    worst = 0.0
    for db in (-30, -20, -15, -12.5, -10, -6, -3, 0, 5, 10):
        got = [realised_snr(n, db, rng) for n in speech]
        err = max(abs(g - db) for g in got)
        worst = max(worst, err)
        print(f"  要求 {db:+6.1f} dB -> " +
              "  ".join(f"{n}={g:+7.3f}" for n, g in zip(speech, got)) +
              f"   誤差 {err:.2e}")
    print(f"  最大誤差 {worst:.2e} dB —— {'通過' if worst < 1e-6 else '不通過 ✗'}")

    print("\n-- 任意實數解析度 --------------------------------------")
    a = realised_snr('bi', -12.000, np.random.default_rng(1))
    b = realised_snr('bi', -12.001, np.random.default_rng(1))
    print(f"  -12.000 dB -> {a:.6f}    -12.001 dB -> {b:.6f}")
    print(f"  可分辨 0.001 dB 的差距:{'是' if abs(a - b) > 1e-4 else '否 ✗'}")

    print("\n-- Running noise(每次呼叫應為不同噪音樣本)-------------")
    _, y1 = mix_at_snr('bi', -10)
    _, y2 = mix_at_snr('bi', -10)
    print(f"  兩次呼叫的波形最大差異 {np.abs(y1 - y2).max():.4f} "
          f"—— {'不同(正確)' if np.abs(y1 - y2).max() > 1e-6 else '相同 ✗'}")

    print("\n-- 削波風險 --------------------------------------------")
    for db in (-30, -20, -10, 0):
        pk = max(np.abs(mix_at_snr(n, db, rng)[1]).max() for n in speech)
        print(f"  SNR {db:+4.0f} dB:峰值 {pk:.3f}"
              f"{'   ⚠ 會被壓縮' if pk > PEAK_LIMIT else ''}")

    print("\n-- 噪音頻譜形狀 ----------------------------------------")
    _, ltas, f = _ltas()
    nz = speech_shaped_noise(sr, rng)
    N = np.abs(np.fft.rfft(nz * np.hanning(len(nz))))
    fn = np.fft.rfftfreq(len(nz), 1.0 / sr)
    for lo, hi in ((100, 500), (500, 2000), (2000, 5000), (5000, 10000)):
        m1 = (f >= lo) & (f < hi)
        m2 = (fn >= lo) & (fn < hi)
        r = 20 * np.log10(ltas[m1].mean() / ltas.mean())
        s = 20 * np.log10(N[m2].mean() / N.mean())
        print(f"  {lo:5d}-{hi:5d} Hz: 語音 {r:+6.1f} dB   噪音 {s:+6.1f} dB   "
              f"差 {abs(r - s):.1f} dB")
    print("=" * 68)


if __name__ == '__main__':
    validate()
