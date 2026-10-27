---
tags: [literature-note, 工具, 刺激來源, AVWM]
citekey: torchaudio-datasets
---

# torchaudio.datasets — 22 個語料庫下載器,**沒有任何一個含孤立 CV 音節**

**DOI / URL**
- 官方 datasets 頁(stable = 2.11) https://docs.pytorch.org/audio/stable/datasets.html
- 同頁 2.11 固定版 https://docs.pytorch.org/audio/2.11/datasets.html
- 維護狀態公告 issue https://github.com/pytorch/audio/issues/3902
- CPU wheel 索引 https://download.pytorch.org/whl/cpu

**查證狀態**(**2026-08-12**,全部實測,非憑記憶)
- **真的裝了**:在隔離 venv 內 `pip install --index-url https://download.pytorch.org/whl/cpu torch torchaudio`
  → 得到 **torch 2.13.0+cpu(wheel 191.8 MB)+ torchaudio 2.11.0+cpu(wheel 341 kB)**,
  安裝後 site-packages 約 887 MB。**未動使用者的系統 Python**(該環境是 numpy 1.26.4 / scipy 1.11.4,
  且本來就沒有 torchaudio / librosa / datasets / parselmouth,我只做唯讀 import 檢查)。
- 資料集清單是用 `dir(torchaudio.datasets)` **實際列舉**的,不是抄文件。
- 下載連結是用 `curl -sIL`(HEAD)**逐一實測 HTTP 狀態碼與 Content-Length**。
- **實際下載並跑通了 YESNO**(4.5 MB,唯一小到值得下載的),證明 `download=True` 管線可用。
- ⚠️ **沒有**下載 LibriSpeech / VCTK / CMU ARCTIC / SPEECHCOMMANDS 本體(數百 MB–數 GB),
  它們的「內容是什麼」是讀文件,只有「連結活著、檔案多大」是實測。
- 測完已 `rm -rf` 整個 venv。

```bibtex
@misc{torchaudio,
  author       = {{PyTorch Team}},
  title        = {torchaudio: an audio library for PyTorch},
  year         = {2026},
  note         = {version 2.11.0; \url{https://github.com/pytorch/audio}},
  howpublished = {\url{https://docs.pytorch.org/audio/stable/datasets.html}}
}
```

## 研究問題
AVWM 需要**自然錄音的 /b/–/p/ CV 音節**。`torchaudio.datasets` 是 Python 生態裡最常被推薦的
「一行下載語料庫」入口 —— 它到底提供哪些語料庫,其中有沒有孤立 CV 音節?

## 方法與族群

### 安裝後 `dir(torchaudio.datasets)` 實際列出的 22 個類別

CMUARCTIC、CMUDict、COMMONVOICE、DR_VCTK、FluentSpeechCommands、GTZAN、IEMOCAP、
LIBRISPEECH、LIBRITTS、LJSPEECH、LibriLightLimited、LibriMix、**LibriSpeechBiasing**、
MUSDB_HQ、QUESST14、SPEECHCOMMANDS、Snips、TEDLIUM、VCTK_092、
VoxCeleb1Identification、VoxCeleb1Verification、YESNO

⚠️ **官方文件頁只列 21 個,少了 `LibriSpeechBiasing`。** 這是我比對「文件 vs 實際安裝」發現的
落差 —— 文件頁不是權威清單,以 `dir()` 為準。

其中 CMUDict 是**發音辭典(純文字)**、GTZAN 與 MUSDB_HQ 是**音樂**,實際的語音語料庫只有 19 個。

### 下載連結實測(curl HEAD,2026-08-12)

| 資料集 | URL | 狀態 | 大小 |
|---|---|---|---|
| LIBRISPEECH dev-clean | openslr.org/resources/12/dev-clean.tar.gz | 200 | 322.3 MB |
| LIBRISPEECH test-clean | openslr.org/resources/12/test-clean.tar.gz | 200 | 330.6 MB |
| LIBRISPEECH train-clean-100 | openslr.org/resources/12/train-clean-100.tar.gz | 200 | **5.9 GB** |
| LIBRITTS dev-clean | openslr.org/resources/60/dev-clean.tar.gz | 200 | 1.2 GB |
| CMUARCTIC (bdl,男) | festvox.org/cmu_arctic/packed/cmu_us_bdl_arctic.tar.bz2 | 200 | 70.2 MB |
| CMUARCTIC (slt,女) | festvox.org/cmu_arctic/packed/cmu_us_slt_arctic.tar.bz2 | 200 | 77.6 MB |
| VCTK_092 | datashare.**is**.ed.ac.uk/…/VCTK-Corpus-0.92.zip | **302** | 轉址到 datashare.ed.ac.uk(同路徑) |
| SPEECHCOMMANDS v0.02 | download.tensorflow.org/data/speech_commands_v0.02.tar.gz | 200 | 2.3 GB |
| LJSPEECH | data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2 | 200 | 2.6 GB |
| YESNO | openslr.org/resources/1/waves_yesno.tar.gz | 200 | 4.5 MB |
| **TEDLIUM release-3** | openslr.org/resources/51/TEDLIUM_release-3.tgz | **404** | — |

⚠️ **TEDLIUM release-3 的硬編碼 URL 已死**(http 與 https 都 404)。torchaudio 原始碼裡
還寫著這個連結,呼叫 `TEDLIUM(release="release3", download=True)` 會失敗。
⚠️ **VCTK_092 的硬編碼網域 `datashare.is.ed.ac.uk` 已改名**,靠 302 轉址才活著;
`torch.hub.download_url_to_file` 會跟轉址,所以目前仍可用,但這是隨時會斷的相依。

### YESNO 端到端實測(唯一真的下載的)
```
ds = YESNO(root, download=True)   →  n_items = 60
檔名: 0_0_0_0_1_1_1_1.wav, 0_0_0_1_0_0_0_1.wav, …
單檔: 8000 Hz, mono, 6.35 s
```
→ **每個檔是一位希伯來語者連說 8 個 yes/no 詞**,不是孤立音節,取樣率只有 8 kHz。
對 AVWM **完全不可用**(語言不對、不是 CV、8 kHz 連 burst 頻譜都保不住)。

## 結果與限制

### ⭐ 核心結論:22 個類別裡**沒有任何一個**含孤立 CV 音節

逐一對照 AVWM 的需求:

| 類別 | 實際內容 | 為何不能用 |
|---|---|---|
| LIBRISPEECH / LIBRITTS / LibriLightLimited / LibriSpeechBiasing | 有聲書**連續朗讀** | 句子層,無音素邊界標註 |
| CMUARCTIC | 每位語者 ~1132 **句** Arctic 句子 | 句子層 |
| VCTK_092 | 109 位語者 × ~400 **句** | 句子層 |
| LJSPEECH | 單一女聲有聲書**句子** | 句子層 |
| COMMONVOICE | 群眾外包**句子** | 句子層 |
| TEDLIUM | 演講 | 連續語音;且 r3 連結已死 |
| **SPEECHCOMMANDS** | 1 秒**孤立單詞**(yes/no/up/down/left/right/…) | **是孤立「詞」不是「音節」**;無 /ba/ /pa/;且無 VOT 標註 |
| **YESNO** | **希伯來語**,8 kHz,每檔 8 詞 | 語言錯、非孤立、取樣率太低 |
| FluentSpeechCommands / Snips | 口語指令**句** | 句子層 |
| IEMOCAP | 情緒對話 | 連續語音 |
| VoxCeleb1 ×2 | 名人訪談 | 連續語音、雜訊大 |
| QUESST14 | 口語檢索查詢 | 句子層 |
| LibriMix / DR_VCTK / MUSDB_HQ | 混音/去噪/音樂衍生集 | 衍生任務,非原始語音素材 |
| CMUDict / GTZAN | 文字辭典 / 音樂 | 不是語音音檔 |

**→ `torchaudio.datasets` 對 AVWM 的價值只有一個:當「自然連續語音的來源」,
再自己切音節。它本身不提供任何切好的 CV。** 切割要靠對齊器,見 [[montreal-forced-aligner]]。

### 其他限制
- ⚠️ **torchaudio 自 2.9 起進入「維護階段」(maintenance phase)**,2.8 標記棄用的 API 在 2.9 移除,
  `prototype` 模組(含 prototype datasets)在 2.9 移除;`load()`/`save()` 現在只是
  `load_with_torchcodec()`/`save_with_torchcodec()` 的別名,編解碼已移交 TorchCodec。
  **→ 為了下載語料庫而把 torchaudio 綁進 AVWM 是不划算的相依**(要拖 191.8 MB 的 torch)。
  同樣的 tar.gz 用 `requests` 直接抓即可。
- 這些 downloader **不做校驗以外的任何前處理**,也不提供音素邊界。
- 所有 CC 授權細節都在各語料庫官網,torchaudio 本身(BSD-2)不轉授權。

## 可連結脈絡
- 上位問題 —— [[natural-speech-sources]]
- 這些下載器指向的語料庫本身 —— [[librispeech]]、[[cmu-arctic]]
- 要從連續語音切出 CV 必須靠對齊 —— [[montreal-forced-aligner]]
- 另一條套件途徑(HF hub) —— [[huggingface-speech-datasets]]
- 切割與 VOT 量測的實作工具 —— [[speech-python-toolkits]]
- 為什麼 AVWM 要自然音而非合成音 —— [[silbert2012]]
- 有音素邊界但授權受限的替代 —— [[timit]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**`torchaudio.datasets` 到底有哪些?** → 22 個(`dir()` 實測),官方文件頁只列 21 個,漏掉 `LibriSpeechBiasing`。
**SPEECHCOMMANDS 能當 CV 音節用嗎?** → 不能。它是 1 秒**孤立單詞**(yes/no/up/down…),不是音節,也沒有 /ba/ /pa/。
**YESNO 是英語嗎?** → 不是,希伯來語,8 kHz,每檔 8 個詞連說。
**哪個 torchaudio 下載連結壞了?** → TEDLIUM release-3(openslr/51)404;VCTK_092 的網域改名了,靠 302 轉址才活著。
**為了抓語料庫值得裝 torchaudio 嗎?** → 不值得。要拖 191.8 MB 的 torch,而且 torchaudio 2.9 起已進入維護階段。直接 `requests` 抓 tar.gz 即可。
