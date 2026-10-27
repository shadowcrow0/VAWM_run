"""跨電腦解析音訊輸出裝置 —— 用名稱比對,不用 index。

⚠ 2026-10-24 起實驗腳本改用 audio_pick.py(列裝置、實際試開、命令列指定);本檔保留給
  舊流程與 validate() 自我檢查。新版 PsychoPy 的 getAvailableDevices() 回傳的鍵是
  'deviceName'(舊版是 'name'),下面兩種都接受。

為什麼不能寫死 index
--------------------
PsychoPy 的 device manager 把裝置存在 `%APPDATA%/psychopy3/devices.json`,
那是**機器專屬**的檔案,不會跟著 repo 走。而且 index 連在同一台機器上都不穩定:

    本機實測(2026-08-12):
      devices.json 裡 'Laptop'  = Headphones (Realtek(R) Audio)  index 7.0
      devices.json 裡 'laptop'  = Speakers   (Realtek(R) Audio)  index 4.0
      但 SpeakerDevice.getAvailableDevices() 當下只回傳 index 4.0 一個 ——
      **耳機沒插著就不在列表裡**,index 7 是查不到的。

所以 index 會隨插拔、驅動更新、OS 列舉順序改變。office=7 / home=4 / lab=未知
這種對照表遲早會錯,而且錯的方式是**靜默的**。

做法
----
開場時列舉實際可用的裝置,依名稱樣式挑一個,然後用 psyexp 已經在用的那個 label
(`Laptop`)把它註冊進 DeviceManager。**psyexp 完全不用改** —— SoundComponent 的
`deviceLabel` 照樣寫 `Laptop`,只是現在指向的是這台機器上實際存在的裝置。

⚠️ 對本專案特別重要:聽覺維度是 SNR。用筆電喇叭播的話,頻率響應、房間殘響、
左右聲道串音都會污染訊噪比。所以預設**找不到耳機就直接報錯**,不靜默退回喇叭。

用法(PsychoPy Builder 的 Begin Experiment)
------------------------------------------
    from audio_device import setup_speaker
    speaker_info = setup_speaker(label='Laptop', require_headphones=True)
    thisExp.addData('audio_device', speaker_info['name'])
    thisExp.addData('audio_index',  speaker_info['index'])

命令列自我檢查(換到新電腦時先跑這個):
    python audio_device.py
"""

import platform
import re

# ──────────────────────────────────────────────────────────────
# 設定
# ──────────────────────────────────────────────────────────────

# 依優先順序比對裝置名稱(不分大小寫的子字串/正則)。
# 排在前面的先選中。新電腦如果名稱不同,在這裡加一條就好。
HEADPHONE_PATTERNS = [
    r"headphone",        # "Headphones (Realtek(R) Audio)" —— office
    r"head[\s_-]?set",
    r"耳機",
    r"\bhdmi\b.*head",
]

# 沒有耳機時可接受的後備(僅在 require_headphones=False 時使用)
FALLBACK_PATTERNS = [
    r"speaker",          # "Speakers (Realtek(R) Audio)" —— home
    r"realtek",
    r"喇叭",
]

# 逐機器覆寫:某台電腦的裝置名稱如果無法用上面的樣式抓到,
# 在這裡用 hostname 指定一條專屬樣式。lab 那台確定後補進來。
PER_HOST_PATTERNS = {
    # "LAB-PC-01": [r"USB Audio Device"],
}

SPEAKER_CLASS = "psychopy.hardware.speaker.SpeakerDevice"


# ──────────────────────────────────────────────────────────────
# 解析
# ──────────────────────────────────────────────────────────────

def list_devices():
    """回傳目前**實際可用**的輸出裝置清單。

    注意這是動態的 —— 耳機沒插著就不會出現在這裡。
    """
    from psychopy.hardware.speaker import SpeakerDevice
    return list(SpeakerDevice.getAvailableDevices())


def _match(devices, patterns):
    """依樣式順序找第一個符合的裝置。回傳 (device, 命中的樣式) 或 (None, None)。"""
    for pat in patterns:
        rx = re.compile(pat, re.IGNORECASE)
        for d in devices:
            if rx.search(str(d.get("deviceName") or d.get("name") or "")):
                return d, pat
    return None, None


def resolve_speaker(require_headphones=True, devices=None):
    """挑出這台機器上該用的輸出裝置。

    Returns
    -------
    dict: {'name', 'index', 'matched_pattern', 'is_headphones', 'candidates'}

    Raises
    ------
    RuntimeError
        完全沒有可用裝置,或 require_headphones=True 但找不到耳機。
        **這裡刻意用報錯而不是靜默退回喇叭** —— SNR 實驗用喇叭播出來的資料是廢的,
        寧可開場就停下來,也不要跑完一個受試者才發現。
    """
    devices = list_devices() if devices is None else devices
    if not devices:
        raise RuntimeError(
            "找不到任何音訊輸出裝置。檢查:音效卡驅動、耳機是否插好、"
            "以及 PsychoPy 的 audio library 設定(Settings > Audio lib,本專案用 ptb)。")

    host = platform.node()
    patterns = list(PER_HOST_PATTERNS.get(host, [])) + list(HEADPHONE_PATTERNS)

    dev, pat = _match(devices, patterns)
    is_hp = dev is not None

    if dev is None:
        if require_headphones:
            names = "\n".join(f"    - {d.get('deviceName') or d.get('name')!r} (index {d.get('index')})"
                              for d in devices)
            raise RuntimeError(
                f"在 {host} 上找不到耳機裝置。目前可用的是:\n{names}\n\n"
                "  本實驗的聽覺維度是 SNR,用喇叭播會讓訊噪比失效,所以不自動退回。\n"
                "  處理方式二選一:\n"
                "    1. 插上耳機後重跑\n"
                "    2. 若這台機器的耳機名稱不同,把樣式加進 audio_device.py 的\n"
                "       HEADPHONE_PATTERNS,或用 PER_HOST_PATTERNS 針對這台機器指定\n"
                f"       (本機 hostname = {host!r})")
        dev, pat = _match(devices, FALLBACK_PATTERNS)
        if dev is None:
            dev, pat = devices[0], "(第一個可用裝置)"

    return {
        "name": dev.get("deviceName") or dev.get("name"),
        "index": dev.get("index"),
        "matched_pattern": pat,
        "is_headphones": is_hp,
        "host": host,
        "candidates": [(d.get("deviceName") or d.get("name"), d.get("index")) for d in devices],
    }


def setup_speaker(label="Laptop", require_headphones=True, verbose=True):
    """解析裝置並用 `label` 註冊進 DeviceManager,psyexp 即可沿用原本的 deviceLabel。

    psyexp 裡五個 SoundComponent 的 deviceLabel 都是 'Laptop';這個函式讓那個
    label 在任何機器上都指向實際存在的裝置,所以 psyexp 一個字都不用改。

    回傳 resolve_speaker() 的結果 dict,建議把 name/index 寫進資料檔。
    """
    from psychopy.hardware import DeviceManager

    info = resolve_speaker(require_headphones=require_headphones)

    if DeviceManager.hasDevice(label):
        DeviceManager.removeDevice(label)          # 覆蓋 devices.json 的舊定義
    DeviceManager.addDevice(deviceClass=SPEAKER_CLASS,
                            deviceName=label,
                            index=info["index"])

    if verbose:
        print(f"[audio] {info['host']}: 使用 {info['name']!r} (index {info['index']}) "
              f"-> 註冊為 {label!r}"
              f"{'' if info['is_headphones'] else '  <<< 警告:不是耳機'}")
    return info


# ──────────────────────────────────────────────────────────────
# 自我檢查
# ──────────────────────────────────────────────────────────────

def validate():
    print("=" * 68)
    print("audio_device —— 音訊輸出裝置解析檢查")
    print("=" * 68)
    print(f"hostname: {platform.node()}")
    print(f"platform: {platform.system()} {platform.release()}")

    devs = list_devices()
    print(f"\n目前可用的輸出裝置({len(devs)} 個):")
    for d in devs:
        print(f"  index {str(d.get('index')):>6}  {d.get('deviceName') or d.get('name')!r}")
    if not devs:
        print("  (無)")

    print("\n-- 要求耳機 --")
    try:
        info = resolve_speaker(require_headphones=True)
        print(f"  選中: {info['name']!r} (index {info['index']})")
        print(f"  命中樣式: {info['matched_pattern']!r}")
    except RuntimeError as e:
        print(f"  找不到耳機:\n{e}")

    print("\n-- 允許後備 --")
    try:
        info = resolve_speaker(require_headphones=False)
        print(f"  選中: {info['name']!r} (index {info['index']})"
              f"{'  [耳機]' if info['is_headphones'] else '  [非耳機]'}")
        print(f"  命中樣式: {info['matched_pattern']!r}")
    except RuntimeError as e:
        print(f"  失敗: {e}")

    print("\n-- 註冊到 DeviceManager --")
    try:
        info = setup_speaker(label="Laptop", require_headphones=False, verbose=False)
        from psychopy.hardware import DeviceManager
        got = DeviceManager.getDevice("Laptop")
        print(f"  hasDevice('Laptop') = {DeviceManager.hasDevice('Laptop')}")
        print(f"  解析到的 index      = {getattr(got, 'index', None)}")
        print(f"  與挑選結果一致      = {getattr(got, 'index', None) == info['index']}")
    except Exception as e:
        print(f"  失敗: {type(e).__name__}: {e}")

    print("=" * 68)


if __name__ == "__main__":
    validate()
