---
tags: [literature-note, 工具, 刺激製作, AVWM]
citekey: montreal-forced-aligner
---

# Montreal Forced Aligner (MFA) 3.4.1 — 能切出音素邊界,但 **`pip install` 裝不起來**,只能走 conda

**DOI / URL**
- 安裝文件 https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html
- 原始碼 https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner
- PyPI(MFA 本體) https://pypi.org/project/montreal-forced-aligner/
- PyPI(Kaldi 綁定) https://pypi.org/project/kalpy-kaldi/

**查證狀態**(**2026-08-12**,關鍵結論全部實測)
- **真的 `pip install montreal-forced-aligner` 了**(在隔離 venv 內)→ **安裝成功**,
  拉進 Montreal_Forced_Aligner-3.4.1 + 28 個相依(SQLAlchemy、praatio、librosa、
  huggingface_hub、matplotlib、seaborn、pandas…),約 200 MB。
- **然後執行 `mfa version` → 直接 crash**。錯誤原文:
  ```
  File ".../montreal_forced_aligner/acoustic_modeling/base.py", line 12, in <module>
      from _kalpy.gmm import AccumAmDiagGmm
  ModuleNotFoundError: No module named '_kalpy'
  ```
  連 `import montreal_forced_aligner` 都同一個錯 —— **套件根本無法 import**。
- **追查 kalpy**:`pypi.org/pypi/kalpy/json` → **HTTP 404**(不存在);
  `kalpy-kaldi` → HTTP 200,v0.10.4,但 **只有 sdist(0.4 MB tar.gz),零個 wheel**。
- **真的試著從原始碼編 kalpy-kaldi**(`pip install --no-binary :all: kalpy-kaldi`)
  → **失敗**,錯誤原文:`running build_ext` → `error: [Errno 2] No such file or directory: 'cmake'`。
- 讀了官方安裝文件全文,確認 conda 是主推路徑。
- ⚠️ **沒有裝 conda / miniforge,所以「conda 路徑能不能成功」我沒有實測**,那部分僅讀文件。
- ⚠️ **沒有實際跑過一次對齊**(沒有聲學模型、沒有語料)。「MFA 能切出音素邊界」是讀文件 +
  它的輸出格式(TextGrid)推得,不是我親眼看到的對齊結果。
- 測完已 `rm -rf` 整個 venv。

```bibtex
@inproceedings{mcauliffe2017montreal,
  author    = {McAuliffe, Michael and Socolof, Michaela and Mihuc, Sarah and
               Wagner, Michael and Sonderegger, Morgan},
  title     = {Montreal Forced Aligner: Trainable Text-Speech Alignment Using Kaldi},
  booktitle = {Proceedings of Interspeech 2017},
  pages     = {498--502},
  year      = {2017},
  doi       = {10.21437/Interspeech.2017-1386}
}
```

## 研究問題
[[torchaudio-datasets]] 與 [[huggingface-speech-datasets]] 的結論都是「只有連續語音,沒有 CV 音節」。
那麼:**能不能用強制對齊(forced alignment)從連續語音自動切出音素邊界,再拼出 CV?**
MFA 是這條路上最主流的工具 —— 它裝得起來嗎?

## 方法與族群

### 它是什麼
MFA = **Kaldi 的 GMM-HMM 強制對齊器 + Python CLI 包裝**。
給它 (音檔 + 對應文字 + 發音辭典 + 預訓練聲學模型),它輸出 **Praat TextGrid**,
內含 word tier 與 **phone tier**(每個音素的起訖時間)。
版本 3.4.1,**MIT 授權**,`requires_python >=3.8`,官方支援 Linux / macOS / Windows。
3.4 起模型格式改走 HuggingFace 託管。

### ⭐ 安裝實測:pip 是個陷阱

官方文件同時列出 conda 與 pip 兩種指令,**但這兩者不對等**:

```
conda create -n aligner -c conda-forge montreal-forced-aligner   # 官方主推
pip install montreal-forced-aligner                              # 「裝得起來,但不能用」
```

文件自己寫了關鍵句:*"Kaldi and MFA are now built on Conda Forge, so installation of
third party binaries is wholly through conda"*,而 pip 路徑要求**先建好含 Kaldi 的 conda 環境**
才輪到 pip 上場。

⚠️ **PyPI metadata 上的 `requires_dist` 完全沒有列 kalpy / kaldi**:
click、huggingface-hub、kneed、librosa、matplotlib、numpy、praatio>=6.0.0、pyyaml、
requests、rich、rich-click、scikit-learn、seaborn、sqlalchemy>=2.0、tqdm。
**→ 所以 pip 會「安裝成功」而不報任何錯,直到你第一次執行才 `ModuleNotFoundError: No module named '_kalpy'`。
這是一個沉默失敗,很容易誤以為裝好了。**

補洞也補不起來:`kalpy` 在 PyPI 上 404;`kalpy-kaldi` 只有 sdist,
編譯需要 **cmake + 完整的 Kaldi / OpenFst toolchain**(我這台機器連 cmake 都沒有,
build_ext 第一步就死)。就算裝了 cmake,還要 OpenFst、BLAS 等一整串系統相依。

**→ 結論:MFA 實質上是 conda-only。** 要用它,必須先裝 miniforge/miniconda,
在**獨立的 conda 環境**裡建立(絕不要動到跑 PsychoPy 的那個 Python)。

## 結果與限制

### 對 AVWM 的可行性評估

**能做的**:給 LibriSpeech / CMU ARCTIC / VCTK 這類「有音檔 + 有逐字稿」的語料,
MFA 可以標出每個 /b/ /p/ 的起訖時間,讓你把 CV 段切出來。

**⚠️ 但對 AVWM 有四個結構性問題,而且每個都不小:**

1. **對齊精度 ≠ VOT 精度。**
   GMM-HMM 對齊的邊界誤差典型在**十幾到數十毫秒**量級,而 /b/–/p/ 的 VOT 界線本身
   就落在 20–40 ms。**用對齊邊界去定義 VOT,誤差和訊號同一個量級。**
   若 AVWM 需要精確的 VOT 數值,必須在對齊之後**人工用 Praat 校正 burst 與 voicing onset**
   ——那就回到手工,MFA 只是省了「大致定位」這一步。
2. **切出來的是連續語流中的 /b/ /p/,不是孤立音節。**
   會帶協同構音、句子語調、前後文韻律,而且音強/時長受語速影響。
   [[silbert2012]] 用的是**單獨錄製的無意義音節**,不是從句子裡剪的。這兩者不等價。
3. **語料裡的 /ba/ /pa/ 出現次數與語境不受控。** 你拿到的是「某個詞裡的 /pa/」,
   不是設計好的最小對立對。要湊齊平衡的 token 集合得篩過大量語料。
4. **安裝成本高**:要引入 conda 生態,只為了做一次性的刺激前處理。

### 什麼情況下值得裝 MFA
- 已經決定要走「從自然連續語音剪 CV」這條路,而且**素材量大到不能手工**。
- 只把 MFA 當**粗定位**,後續一律 Praat 手校 → 這時 [[speech-python-toolkits]] 的
  parselmouth 是必要搭檔。

### 什麼情況下不該裝
- 素材只有幾十個 token(AVWM 的規模)→ **直接請人錄 + Praat 手工切,更快也更準。**
  [[silbert2012]] 就是作者本人錄的 4 個 token × 4 類。

## 可連結脈絡
- 上位問題 —— [[natural-speech-sources]]
- 要對齊的素材從哪來 —— [[torchaudio-datasets]]、[[librispeech]]、[[cmu-arctic]]
- 對齊後的手工校正與 VOT 量測 —— [[speech-python-toolkits]](parselmouth 已實測可用)
- 已附音素邊界、不需自己對齊的替代 —— [[timit]](但授權受限)
- 為何 AVWM 需要自然而非合成刺激 —— [[silbert2012]]
- VOT 與 burst 的量測定義 —— [[chodroff2014]]、[[burst-vot-tradeoff]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**`pip install montreal-forced-aligner` 可以嗎?** → **不行。** 安裝會「成功」但套件 import 就炸:`ModuleNotFoundError: No module named '_kalpy'`。這是沉默失敗,最坑。
**為什麼 pip 不行?** → PyPI 的 `requires_dist` 根本沒列 kalpy;Kaldi 綁定只在 conda-forge。`kalpy` 在 PyPI 上 404,`kalpy-kaldi` 只有 sdist,編譯要 cmake + 完整 Kaldi/OpenFst toolchain。
**那要怎麼裝?** → `conda create -n aligner -c conda-forge montreal-forced-aligner`(官方主推;**我沒實測 conda 路徑**)。務必用獨立環境,別碰 PsychoPy 的 Python。
**MFA 能直接給我 VOT 嗎?** → 不能。GMM-HMM 對齊誤差是**數十毫秒**量級,和 /b/–/p/ 的 VOT 界線(20–40 ms)同一個數量級。只能當粗定位,之後要 Praat 手校。
**AVWM 該裝 MFA 嗎?** → 以 AVWM 的 token 規模(幾十個),**不值得**。手工錄 + Praat 切更快更準。
