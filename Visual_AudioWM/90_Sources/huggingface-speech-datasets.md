---
tags: [literature-note, 工具, 刺激來源, 授權風險, AVWM]
citekey: huggingface-speech-datasets
---

# HuggingFace Hub 語音資料集 — TIMIT 有幾十個**盜傳副本**,但 CV 音節/VOT 連續體**一個都沒有**

**DOI / URL**(全部於 **2026-08-12** 實際查詢)
- 官方 TIMIT(需 LDC 授權) https://huggingface.co/datasets/timit-asr/timit_asr
- 搜尋介面 https://huggingface.co/datasets?search=timit
- 查詢用的 API endpoint `https://huggingface.co/api/datasets?search=<詞>&limit=N`
- 官方 Speech Commands https://huggingface.co/datasets/google/speech_commands
- LDC93S1 授權來源 https://catalog.ldc.upenn.edu/LDC93S1

**查證狀態**(**2026-08-12**)
- **實際打了 Hub search API**,關鍵詞:`timit`、`phoneme`(60 筆)、`syllable`(50 筆)、
  `voice onset time`、`consonant`(30 筆)、`speech commands`(25 筆)。清單如下,是 API 回傳原文。
- **實際開啟 `timit-asr/timit_asr` 的 dataset card**,確認授權文字與欄位結構。
- ⚠️ **一個資料集本體都沒下載**(避免踩授權地雷,也避免拉大檔)。
  「內容是什麼」來自 dataset card,不是我聽過音檔。
- ⚠️ **沒有裝 `datasets` 套件**,查詢全走 HTTP API。

```bibtex
@misc{lhoest2021datasets,
  author    = {Lhoest, Quentin and others},
  title     = {Datasets: A Community Library for Natural Language Processing},
  booktitle = {Proceedings of EMNLP 2021: System Demonstrations},
  pages     = {175--184},
  year      = {2021},
  url       = {https://aclanthology.org/2021.emnlp-demo.21}
}
```

## 研究問題
HF Hub 是目前最大的公開資料集聚合站。上面有沒有 (a) 能合法用的 TIMIT、
(b) 任何 CV 音節 / VOT 連續體 / 音素層切好的英語資料集?

## 方法與族群

### (a) TIMIT:官方 repo 是**空殼**,其餘是盜傳

`timit-asr/timit_asr`(618 downloads / 27 likes)—— dataset card 明寫:
> 授權為 **"LDC User Agreement for Non-Members"**;
> "The dataset needs to be downloaded manually from https://catalog.ldc.upenn.edu/LDC93S1",
> 要先 "create an account and download the dataset" 才能在本機載入。

→ **它只是一個 loading script,不含音檔。** 有 `phonetic_detail`(音素 + 起訖毫秒)
與 `word_detail` 欄位,但你得先自己有 LDC 的光碟。

⚠️ **但 search API 回傳了至少 30 個 TIMIT 相關 repo,其中多個下載量遠高於官方 repo**,
明顯是**連音檔一起重傳**的非官方副本:

| repo | downloads | likes |
|---|---|---|
| IParraMartin/TIMITPhones | **59.5k** | 156 |
| AminRafiei/timit_cleaned | **28.3k** | 57 |
| hadiqa123/ur_timit_asr | 9.24k | 22 |
| Siyong/speech_timit | 6.3k | **286** |
| nh0znoisung/timit、PhilSad/TIMIT_dataset、speech31/timit_english_ipa、m-aliabbas/idrak_timit… | 各 ~6.3k | — |
| kylelovesllms/timit_asr(+ _ipa) | 各 4.97k | 57 / 36 |
| macabdul9/TimitSI | 5.86k | 67 |
| patlee0208/TIMIT_v2 | 597 | 73 |

⚠️⚠️ **這些都是 LDC93S1 的重新散布,TIMIT 的授權不允許再散布。**
`IParraMartin/TIMITPhones` 從名稱看是**已切好的音素段**(正是 AVWM 想要的形狀),
但**用它等於使用未授權重製品**。學位論文/期刊投稿踩這個會出事。
**→ 要用 TIMIT 就走 LDC 正規取得,見 [[timit]]。**

### (b) CV 音節 / VOT:搜尋結果**全空**

**`voice onset time` → API 回傳 EMPTY(零筆)。**

`syllable`(50 筆上限,回傳 28 筆)—— 逐筆看過,**沒有一筆是英語 CV 音節音檔**:
越南語音節分詞(truongpdd、linhqyy、tmnam20、iambestfeed、MiuN2k3、namkuner)、
馬來語(mesolitica)、緬甸語合成字形(DatarrX)、烏茲別克(uznlp-uz)、
韓文 K-pop 歌詞對齊(nvlr)、古蘭經誦讀(Bisher)、重音標註文字(TigrulyaCat)、
`Hellisotherpeople/one_syllable`(單音節**詞表**,純文字)。
**→ 這些絕大多數是 NLP 的「音節切分」文字任務,不是聲學刺激。**

`phoneme`(60 筆)—— 同樣**沒有孤立 CV**。大宗是:
G2P 文字對(bookbot、lipishan、mrfakename、Respair、Carruto)、
IPA 語言模型訓練語料(phonemetransformers/IPA-CHILDES、IPA-BabyLM、bbunzeck/phoneme-babylm)、
`mstz/phoneme` 是 **UCI 表格資料集**(不是音檔)、
`yzhuang/autotree_pmlb_phoneme_*` 是決策樹 benchmark(不是音檔)。
唯一沾到聲學段落的是 `DynamicSuperb/PhonemeSegmentCounting_VoxAngeles` 與
`speech31/PhonemeSegmentCounting_Librispeech-words` —— 那是「**數**音素個數」的評測任務,
不是切好的音素刺激。

`consonant`(30 筆)—— 兩個值得記,但都不能用:
- **`ixxan/Uyghur-Consonant-Vowel-Combo-Pronunciations`** —— 真的是 CV 組合發音,
  但是**維吾爾語**。維吾爾語 /b/–/p/ 的 VOT 分布與英語不同,不能直接當英語刺激。
- **`Harmonic-Frontier-Audio/Plosives_and_Non_Lexical_Consonant_Bursts_Preview`** ——
  真人錄音、96 kHz/24-bit、CC BY-NC 4.0,但 card 明寫**只有 3 個檔、2.7 MB**,
  而且是「burst gesture」(爆破**姿勢**)不是 CV 音節;完整版要商業授權。
  ⚠️ CC BY-NC 的 **NC** 對學術用途通常可以,但要確認你的機構/期刊政策。
- 其餘是日文假名文字(oda-99 ×20+)、手寫字元圖像(kalixlouiis、DatarrX)、
  數母音子音個數的 NLP 任務(Lots-of-LoRAs、supergoose)。

`speech commands`(25 筆)—— `google/speech_commands` 是官方,其餘是加噪/編碼衍生版
(Codec-SUPERB、renumics、mazkooleg 等)。**都是孤立「詞」,不是音節**,
與 [[torchaudio-datasets]] 的 SPEECHCOMMANDS 同源。

## 結果與限制

### ⭐ 核心結論
1. **HF Hub 上沒有任何英語 /b/–/p/ CV 音節或 VOT 連續體資料集。** 這不是我沒搜到 ——
   `voice onset time` 的搜尋結果是**字面上的零筆**。
2. **HF 上的 TIMIT 「能用」是假象**:官方 repo 是要你自備 LDC 光碟的空殼;
   看起來能直接下載的那幾十個高下載量副本是**未授權重製**。
3. HF Hub 對 AVWM 的真正價值和 torchaudio 一樣,只是**連續語音的來源**,
   仍然要自己切 CV。

### 限制與風險
- ⚠️ **搜尋是關鍵詞比對,不是語意搜尋。** 若某個 CV 音節資料集用了完全不同的命名
  (例如上傳者只寫 "nonsense syllables" 或某實驗室代號),我這輪查不到。
  已試過的詞:timit / phoneme / syllable / voice onset time / consonant / speech commands。
  **未試**:nonsense syllable、CV、plosive、stop consonant、categorical perception。
- ⚠️ 授權欄位由**上傳者自填**,HF 不驗證。看到 "MIT" 或 "CC-BY" 不代表原始語料真的是那個授權
  ——上面那些 TIMIT 副本就是活生生的例子。
- 沒有實際下載任何音檔,所以取樣率、錄音品質、語者資訊都是照抄 card。

## 可連結脈絡
- 上位問題 —— [[natural-speech-sources]]
- TIMIT 正規取得途徑與授權全文 —— [[timit]]
- 另一條套件途徑(下載器) —— [[torchaudio-datasets]]
- 要自己切 CV 就得對齊 —— [[montreal-forced-aligner]]
- 切割/量測工具 —— [[speech-python-toolkits]]
- 免費且授權乾淨的替代語料 —— [[oscaar-speechbox]]、[[cmu-arctic]]、[[librispeech]]
- 已切好子音刺激的正規來源 —— [[shannon1999-consonant-recordings]]、[[articulation-index-corpus]]
- 為什麼要自然音 —— [[silbert2012]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**HF 上有 VOT 連續體嗎?** → **零筆。** `?search=voice+onset+time` 的 API 回傳是空的。
**HF 上的 TIMIT 能直接下載嗎?** → 官方 `timit-asr/timit_asr` 不行(空殼,要自備 LDC 光碟)。能直接下的那幾十個是**未授權重製**,學術發表不要碰。
**看起來最誘人的那個 TIMIT 副本是哪個?** → `IParraMartin/TIMITPhones`(59.5k 下載,疑似已切好音素段)——**正是因為太好用才更該避開**。
**HF 上最接近 CV 音節的是什麼?** → `ixxan/Uyghur-Consonant-Vowel-Combo-Pronunciations`(維吾爾語,語言不對)。
**HF 授權標籤可信嗎?** → 不可信,由上傳者自填、平台不驗證。
