---
tags: [literature-note, 工具, 刺激製作, AVWM]
citekey: speech-python-toolkits
---

# 語音 Python 工具鏈(librosa / parselmouth / pyroomacoustics / slab / speechbrain·nemo·espnet)—— **全部是工具,零個是刺激來源**

**DOI / URL**
- librosa 範例音檔清單 https://librosa.org/doc/latest/recordings.html
- praat-parselmouth https://pypi.org/project/praat-parselmouth/ | https://parselmouth.readthedocs.io/
- pyroomacoustics https://pypi.org/project/pyroomacoustics/
- slab https://pypi.org/project/slab/ | https://slab.readthedocs.io/
- pychoacoustics https://pypi.org/project/pychoacoustics/
- SpeechBrain recipes https://github.com/speechbrain/speechbrain/tree/develop/recipes
- ESPnet egs2 https://github.com/espnet/espnet/tree/master/egs2
- NeMo ASR datasets https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/datasets.html

**查證狀態**(**2026-08-12**)
- **實際安裝並跑過**(隔離 venv):**librosa 1.0.0**、**praat-parselmouth 0.4.7**、
  **pyroomacoustics 0.10.1**、soundfile 0.14.0。
- librosa 範例清單是 `dir()` 進 internal registry **實際列舉**的,並**真的下載**了
  `libri1` 與 `pibble` 兩個檔,用 soundfile 讀出時長/取樣率。
- parselmouth 的 Praat scripting **實際跑通了**(見下),不是讀文件。
- pyroomacoustics 的 `datasets` 成員與 TimitCorpus/Sentence/Word 的 docstring 是
  `dir()` + `inspect.getdoc()` **實際讀出來**的。
- ⚠️ **slab / pychoacoustics 僅讀 PyPI 頁面,沒有安裝。**
- ⚠️ **speechbrain / nemo / espnet 完全沒有安裝**,只讀了 recipe 目錄清單與文件頁。
- ⚠️ **`python_speech_features` 完全沒查證**,本卡不作陳述。
- 測完已 `rm -rf` 整個 venv。

```bibtex
@inproceedings{mcfee2015librosa,
  author = {McFee, Brian and Raffel, Colin and Liang, Dawen and Ellis, Daniel P.W. and
            McVicar, Matt and Battenberg, Eric and Nieto, Oriol},
  title  = {librosa: Audio and Music Signal Analysis in Python},
  booktitle = {Proceedings of the 14th Python in Science Conference}, pages = {18--25},
  year = {2015}, doi = {10.25080/Majora-7b98e3ed-003}
}
@article{jadoul2018parselmouth,
  author  = {Jadoul, Yannick and Thompson, Bill and de Boer, Bart},
  title   = {Introducing Parselmouth: A Python interface to Praat},
  journal = {Journal of Phonetics}, volume = {71}, pages = {1--15}, year = {2018},
  doi     = {10.1016/j.wocn.2018.07.001}
}
@inproceedings{scheibler2018pyroomacoustics,
  author = {Scheibler, Robin and Bezzam, Eric and Dokmani\'c, Ivan},
  title  = {Pyroomacoustics: A Python package for audio room simulation and array processing algorithms},
  booktitle = {ICASSP 2018}, pages = {351--355}, year = {2018},
  doi = {10.1109/ICASSP.2018.8461310}
}
```

## 研究問題
除了下載器([[torchaudio-datasets]])與 hub([[huggingface-speech-datasets]]),
Python 生態裡還有哪些套件**自帶語音**或**能幫忙做出 CV 音節**?

## 方法與族群

### 1. librosa 1.0.0 —— 17 個範例,4 個有人聲,全是連續朗讀

`librosa.example(key)` 的完整 registry(**實際列舉,17 筆**):
brahms、choice、drese、drese2、fishin、humpback、**libri1**、**libri2**、**libri3**、
nutcracker、**pibble**、pistachio、robin、snare、sweetwaltz、trumpet、vibeace

有人聲的只有:
- `libri1` = *The Ashiel Mystery* ch. XVI / Garth Comira 朗讀
- `libri2` = *The Age of Chivalry* ch. IX / Anders Lankford 朗讀
- `libri3` = *Sense and Sensibility* ch. 18 / Heather Barnett 朗讀
- `pibble` = "Who's a good girl?"
- (`fishin` 是有唱歌的民謠流行曲)

**實測下載結果**:
```
libri1 -> 5703-47212-0000.ogg   14.84 s, 22050 Hz, mono
pibble -> pibble.ogg            46.95 s, 22050 Hz, mono
```
→ **libri1/2/3 就是 LibriSpeech 的片段**(檔名 `5703-47212-0000` 是標準 LibriSpeech
speaker-chapter-utterance 命名),**授權隨 LibriSpeech 為 CC BY 4.0**。
⚠️ 但 librosa 官方 recordings 頁**沒有逐檔標示授權**,上述授權是我從檔名推 LibriSpeech 來源得到的,
**不是 librosa 文件明寫的**。其餘音樂類例檔多來自 ccMixter/Freesound,授權各異。

**對 AVWM 的用處:零。** 都是 22 kHz 的連續朗讀 ogg,總長不到一分鐘,**不是 CV 音節**。
librosa 的價值在**分析**(STFT、MFCC、onset detection),不在資料。

### 2. ⭐ praat-parselmouth 0.4.7 —— 這條路上**最有用**的套件

GPLv3+,是 Praat 的 C/C++ 內核直接綁定(不是包 Praat script 語言),
所以演算法與 Praat 輸出**逐位元一致**。

⚠️ 有些說明會講「parselmouth 不暴露 Praat scripting」——**這是錯的**。
`parselmouth.praat.call()` 可以呼叫**任何** Praat 選單指令。我實測跑通:

```python
snd = parselmouth.Sound("....wav")            # 8000 Hz, 6.35 s
call(snd, "To TextGrid (silences)", 100, 0.0, -25.0, 0.1, 0.05, "silent", "sounding")
  →  Get number of intervals = 17          # 靜音切分,可自動找音節邊界
call(snd, "To PointProcess (periodic, cc)", 75, 500)
  →  Get number of points = 358            # 聲門脈衝 = voicing onset 的定位依據
```

**→ 這正是 VOT 量測需要的兩件機具:切段 + 找出 voicing onset。**
配合 burst 偵測(可用 librosa/自訂能量門檻),就能在 Python 裡半自動量 VOT,
而且結果與 Praat 手工量測可直接對照。**AVWM 若要自己錄音切 CV,這是核心工具。**
它**不含任何音檔**。

### 3. pyroomacoustics 0.10.1 —— 有 TIMIT 音素切割器,但你得自備 TIMIT

`pyroomacoustics.datasets` 實際成員:
`CMUArcticCorpus`、`CMUArcticSentence`、`GoogleSpeechCommands`、`GoogleSample`、
`TimitCorpus`、`Sentence`、`Word`、`AudioSample`、`SOFADatabase`、`Dataset`、`Meta`、`Sample`

⭐ **`TimitCorpus` 是這一輪唯一直接支援音素層切割的套件。** docstring 實錄:
> `Sentence` 的 `phonems`: *"List of phonems contained in the sentence. Each element is a
> dictionnary containing a **'bnd' with the limits of the phonem** and **'name'** that is
> the phonem transcription."*
> `Word` 的 `samples`: *"A view on the sentence samples containing the word"*

→ 也就是說,**只要你手上有 TIMIT,pyroomacoustics 可以直接依 `.PHN` 檔把每個音素切出來**,
不需要 MFA、不需要對齊(TIMIT 的邊界是**人工標的**,遠比強制對齊準)。
⚠️ **但 pyroomacoustics 不含任何音檔**,`CMUArcticCorpus` 也只是下載器。
TIMIT 的授權門檻不變,見 [[timit]]。
⚠️ 我**沒有**真的餵 TIMIT 進去跑(沒有 TIMIT 資料),這是讀 API 得到的判斷。

### 4. slab / pychoacoustics —— 心理聲學實驗框架,只合成不錄音
`slab` 的 `Sound` 只能**合成**:`tone()`、`vowel()`(合成母音)、`whitenoise()`、`pinknoise()`。
**沒有子音、沒有 CV 音節、沒有 VOT 相關 API,不含任何真人錄音。**
`pychoacoustics` 是實驗執行平台(同 PsychoPy 的定位),不是刺激庫。
(⚠️ 兩者僅讀 PyPI/文件頁,未安裝。)

### 5. speechbrain / NeMo / ESPnet —— recipe 指向的都是同一批語料庫
三者**都不隨 pip 套件散布任何音檔**,recipe 只是下載 + 前處理外部語料的腳本。
- **SpeechBrain** recipe 目錄(讀 GitHub):AISHELL-1、AMI、AudioMNIST、CommonVoice、
  ESC50、GigaSpeech、Google-speech-commands、IEMOCAP、LJSpeech、Libri-Light、LibriMix、
  LibriParty、**LibriSpeech**、LibriTTS、SLURP、Switchboard、**TIMIT**、Tedlium2、
  Voicebank、VoxCeleb、VoxPopuli、WSJ0Mix、fluent-speech-commands…(約 43 個)
- **ESPnet** egs2:**200+ 個** recipe(accentdb → zeroth_korean),涵蓋 ASR/TTS/SVS/SE/ST/SLU。
- **NeMo**:LibriSpeech、Fisher English、2000 HUB5、AN4、Aishell-1/2。
  (AN4 是「拼出地址、姓名」的錄音 —— 是**字母**朗讀,不是 CV 音節。)

**→ 交集就是 LibriSpeech / TIMIT / CommonVoice / VCTK 那批,和 [[torchaudio-datasets]] 完全一樣。
沒有任何一個 recipe 指向 CV 音節語料。**

## 結果與限制

### ⭐ 核心結論
**這五類套件沒有一個提供孤立 CV 音節。** 它們分成兩種:
- **分析/製作工具**(parselmouth、librosa、pyroomacoustics)→ 對 AVWM 有用,但要你自己有素材。
- **合成器/實驗框架**(slab、pychoacoustics)→ 只有合成聲,而 [[silbert2012]] 明說要避開合成。
- **訓練框架**(speechbrain/nemo/espnet)→ 純腳本,指向同一批連續語音語料庫。

### 對 AVWM 的實務建議(排序)
1. **parselmouth 是必裝的**(GPLv3+,純 Python wheel,不碰系統相依)——
   自己錄音切 CV、量 VOT、驗證刺激聲學性質都靠它。
   ⚠️ GPLv3 只約束**再散布程式碼**,不影響你用它產生的刺激或資料。
2. 若最後拿到 TIMIT,**pyroomacoustics 的 `TimitCorpus` 比 MFA 好用**——
   TIMIT 的 `.PHN` 是人工標註,精度遠勝強制對齊,見 [[montreal-forced-aligner]]。
3. **librosa 不必為了資料而裝**,但做 burst 偵測/頻譜分析會用到。
4. **slab、speechbrain、nemo、espnet 對 AVWM 都不必裝。**

### 限制
- slab / pychoacoustics / python_speech_features / speechbrain / nemo / espnet **都沒有實際安裝**,
  上述陳述來自文件頁與 repo 目錄,可能漏掉未文件化的功能。
- pyroomacoustics 的 TIMIT 切割能力**沒有實跑**(手上無 TIMIT)。
- librosa 例檔的授權是**我從檔名推得**,librosa 文件本身沒有逐檔標示。

## 可連結脈絡
- 上位問題 —— [[natural-speech-sources]]
- 素材來源 —— [[torchaudio-datasets]]、[[huggingface-speech-datasets]]、[[librispeech]]、[[cmu-arctic]]
- 對齊路線的可行性與陷阱 —— [[montreal-forced-aligner]]
- TIMIT 授權與音素標註 —— [[timit]]
- 為何不能走合成路線 —— [[silbert2012]]、[[mbrola-cannot-do-vot]]
- VOT / burst 的量測定義 —— [[chodroff2014]]、[[burst-vot-tradeoff]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**librosa 有語音範例嗎?** → 有 4 個人聲(libri1/2/3 是 LibriSpeech 朗讀片段、pibble),都是 22 kHz 連續朗讀 ogg,總長不到一分鐘。**不是 CV 音節。**
**parselmouth 能跑 Praat 指令嗎?** → **能**,`parselmouth.praat.call()` 可叫任何 Praat 選單指令。我實測跑過 "To TextGrid (silences)" 與 "To PointProcess (periodic, cc)" —— 後者正是 voicing onset 定位、也就是量 VOT 的關鍵。
**哪個套件能依音素邊界切檔?** → `pyroomacoustics.datasets.TimitCorpus`,`Sentence.phonems` 有 `'bnd'` 邊界 + `'name'`。**但要自備 TIMIT。**
**slab 有子音刺激嗎?** → 沒有。只能合成 tone / vowel / whitenoise / pinknoise,無子音、無 CV、無 VOT。
**speechbrain / nemo / espnet 自帶音檔嗎?** → 都不帶。recipe 指向的就是 LibriSpeech / TIMIT / CommonVoice 那批,和 torchaudio 一模一樣。
**AVWM 最後該裝哪個?** → **只有 parselmouth 是必要的**(加上 librosa 做頻譜分析)。其餘都不必。
