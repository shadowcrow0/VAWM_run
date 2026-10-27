---
tags: [literature-note, 語音語料庫, 刺激來源, AVWM]
citekey: articulation-index-corpus
---

# Articulation Index Corpus (LDC2005S22 / LDC2015S12) — 20 位母語者、**孤立** CV 音節、**LSCP 版對非會員 $0**

**DOI / URL**
- 主目錄頁 https://catalog.ldc.upenn.edu/LDC2005S22 (DOI https://doi.org/10.35111/qmyb-6884)
- 加值版目錄頁 https://catalog.ldc.upenn.edu/LDC2015S12 (DOI https://doi.org/10.35111/rz6a-gd14)
- **原始語料庫說明書(公開、不需登入)** https://catalog.ldc.upenn.edu/docs/LDC2005S22/doc.txt
- **LSCP 版 readme(公開、不需登入)** https://catalog.ldc.upenn.edu/docs/LDC2015S12/readme.txt
- 授權書全文 PDF https://catalog.ldc.upenn.edu/license/ldc-non-members-agreement.pdf
- 取得流程 https://www.ldc.upenn.edu/language-resources/data/obtaining
- 免費 sampler(含本語料庫樣本) https://catalog.ldc.upenn.edu/LDC2017S16

**查證狀態**(全部於 **2026-08-12** 實際開啟)
- 上列 7 個 URL 全部**實際抓取並讀過全文**。`doc.txt`(337 行)與 `readme.txt` 都完整讀完,
  本卡所有引句逐字取自這兩份官方文件。
- **價格是我從目錄頁 HTML 內嵌的 `data-price-table` 直接讀出的**,不是登入後結帳頁。
  為排除「未登入一律顯示 $0」的可能,我做了對照:同一抓法下 LDC93S1 顯示 `$250.00`、
  LDC96S65-5 顯示 `$600.00`,LDC2015S12 顯示 `$0.00`。**故 $0 應為真實金額,
  但我未註冊 LDC 帳號、未實際走完結帳,無法 100% 確認**。下載前請自行覆核。
- **我沒有下載任何音檔**。「/bi/ 與 /pi/ 各 20 個 token」是我**從 readme 的編碼表與
  缺漏清單推導**的(見下),不是清點實際檔案的結果。這是本卡最需要落地驗證的一點。
- 目錄頁 metadata 欄位把 LDC2015S12 的 Sample Rate 印成 `1600`,**這是官網的錯字**;
  readme 與 LDC2005S22 頁面都寫 16 kHz。

```bibtex
@misc{wright2005articulation,
  author       = {Wright, Jonathan},
  title        = {Articulation Index {LDC2005S22}},
  howpublished = {Web Download},
  address      = {Philadelphia},
  publisher    = {Linguistic Data Consortium},
  year         = {2005},
  doi          = {10.35111/qmyb-6884}
}

@misc{schatz2015articulationlscp,
  author       = {Schatz, Thomas and Cao, Xuan-Nga and Kolesnikova, Anna and
                  Bergvelt, Tomas and Wright, Jonathan and Dupoux, Emmanuel},
  title        = {Articulation Index {LSCP} {LDC2015S12}},
  howpublished = {Web Download},
  address      = {Philadelphia},
  publisher    = {Linguistic Data Consortium},
  year         = {2015},
  doi          = {10.35111/rz6a-gd14}
}
```
> BibTeX 是**我自組**的。LDC 官方只給散文式 citation,逐字為:
> "Wright, Jonathan. Articulation Index LDC2005S22. Web Download. Philadelphia: Linguistic Data Consortium, 2005."
> "Schatz, Thomas, et al. Articulation Index LSCP LDC2015S12. Web Download. Philadelphia: Linguistic Data Consortium, 2015."

## 研究問題
這個語料庫**就是為了做 AVWM 這種實驗而建的**。`doc.txt` 開宗明義:

> "The Articulation Index Corpus was partly inspired by the work of Harvey Fletcher, who did
> a number of perceptual experiments involving English syllables during the first half of the
> 20th century. His term "articulation index" meant something like "perceptual index of
> syllables" where those syllables weren't necessarily words, and reflected how well speakers
> could correctly identify syllables in the presence of noise. This corpus was created to
> facilitate similar experiments, as well as to potentially facilitate new methods in speech
> recognition research."

**「在噪音中辨識無意義音節」正是 AVWM 聽覺維度的作業定義。** 致謝段還明列
Jont Allen 參與設計:

> "Mark Liberman, Jont Allen, Nelson Morgan, George Doddington, and others in the Novel
> Approaches group provided important conceptual advice in the design of the project."

→ 這回答了「Allen 實驗室的 CV 音節語料有沒有公開」:**Allen 實驗室用的就是這個。**
Allen 組的論文(如 Phatak, Lovitt & Allen 2008;Li & Allen 2011)取的是本語料庫中
Miller–Nicely 那 16 個 CV(子音 + /ɑ/)的子集。**Allen 沒有另外一份自建的公開語料庫。**

## 方法與族群

**錄音**(`doc.txt` 逐字):
> "The recordings were made in a small, sound-treated, anechoic room at the LDC."

- 語者:**20 位美式英語母語者(12 男、8 女)**,speaker ID `f101`…`m120`(readme 列全)
- 寬頻:Sennheiser HMD 410 headset → Symetrix 302 preamp → Sony PCM-R300 DAT
  → **16 kHz / 16-bit PCM**
- 窄頻:Nortel 無線電話 headset → 8 kHz / 8-bit u-law(電話頻寬,AVWM 用不到)
- 每場錄音約 15 分鐘;發音不正確的 prompt 會**重錄**

**音節涵蓋範圍 —— 這是關鍵**(readme §A 逐字):
> "All possible Consonant-Vowel (CV) and Vowel-Consonant (VC) combinations were recorded for
> each speaker twice: - once in isolation - once within a carrier-sentence with the following
> structure: WORD1 WORD2 SYLLABLE WORD3, for a total of 25768 recorded syllables."

`doc.txt` 補充:
> "First, all diphone (CV, VC) syllables which were considered valid English syllables were
> included in the common set... These syllables accounted for over 600 of the 2000."

**孤立音節是獨立音檔,不需自己切**(`doc.txt` 逐字):
> "Timestamps were used to mark the beginning and end of each prompt, as well as to separate
> the phrase from the isolated syllable. These timestamps were then used to divide the audio
> data into individual files that contain either a single phrase or a single isolated syllable."

錄音時語者被明確要求在逗號處停頓,讓第二次的音節真正孤立:
> "The speakers were instructed to say the phrase fluently, but to pause at the comma so that
> the second occurrence was truly isolated."
> "Generally, not pausing at the comma made the prompt invalid, since the second instance of
> the syllable wasn't truly isolated."

**LSCP 版(LDC2015S12)在原版之上做了三件對 AVWM 極有價值的事**(readme §B 逐字):
> "2 - Time-alignments for the onset and offset of each word and syllable were obtained through
> forced-alignment with a standard HMM-GMM ASR system.
> 3 - The time-alignments for the beginning and end of the syllables (whether in isolation or
> within a carrier sentence) were **manually adjusted**.
> 4 - The recordings of isolated syllables were **cut according to the manual time-alignments
> to remove the silent portions at the beginning and end**."

→ **孤立音節檔已經人工校過邊界、且已去掉頭尾靜音。切音工作幾乎是零。**
格式從 sphere 改成 `.wav`(mono 16 kHz 16-bit PCM),檔名對 Kaldi 友善。
標註檔 `data/annotations/alignments.txt` 給到**毫秒精度**的 onset/offset。

**檔名直接編碼音節**,readme §C 給了完整 ASCII↔IPA 對照表,其中:

| ASCII | IPA | 例字 |
|---|---|---|
| `b` | b | bee |
| `p` | p | pea |
| `i` | iː | beet |
| `a` | ɑː | bott |

檔名格式為 `<speaker>_<s|p>_<syllable>.wav`,`s` = 孤立音節。
→ **AVWM 要的檔案就是 `*_s_bi.wav` 與 `*_s_pi.wav`。**
(/ɑ/ 備案則是 `*_s_ba.wav` / `*_s_pa.wav`,正好對上 [[silbert2012]] 用的 [ba]/[pa]。)

**/bi/、/pi/ 是否齊全 —— 我的推導**:
readme §D 列出所有「設計上就沒錄」與「事後移除」的檔案。設計上排除的只有
> "V+h, V+w V+y, xg+V, V+r except for ar, er, ir, or, ur which are present in the corpus, rxr, yxu"

**都是 VC 或以 /ŋ/ 開頭,不影響 b+i 與 p+i。** 我再逐字比對了 n=146 的缺漏清單、
n=6 的移除清單與 n=52 的 weird 清單,**沒有任何 `*_s_bi.wav` 或 `*_s_pi.wav`**。
→ 推得 **/bi/ 與 /pi/ 各有 20 個 token(每位語者 1 個),20 位語者全齊**。
⚠️ 這是文件推導,**下載後務必實際 `ls` 清點**。

## 結果與限制

### 授權(逐字)
兩者皆為 **LDC User Agreement for Non-Members**。我下載了 PDF 全文,關鍵句逐字:

> "User agrees to use the LDC Databases received under this Agreement only for **non-commercial
> linguistic education, research and technology development**."

> "User and User's Research Group may include **limited excerpts** from the LDC Databases in
> articles, reports and other documents describing the results of User's non-commercial
> linguistic education, research and technology development."

> "Unless explicitly permitted herein, User shall **not otherwise publish, retransmit, disclose,
> display, copy, reproduce or redistribute** the LDC Databases to others outside of User's
> Research Group."

> "In the event that User's use of the LDC Databases results in the development of a commercial
> product, User must join LDC as a For-Profit Member and pay all applicable fees prior to
> release of said commercial product."

**對 AVWM 的三個實際後果:**
1. 學術用途完全沒問題。
2. **不能把切好的刺激音檔連同論文一起公開釋出**(OSF / 補充材料放音檔會違約)。
   只能放「limited excerpts」。可重製性要靠**寫清楚檔名清單 + 處理腳本**,讓別人自己去 LDC 取。
3. 授權書落款欄是 **"For the organization: ______"** —— 這是**機構級**協議,
   需要有權簽署的人簽名,不是個人點一點就好。LDC 取得頁明言:
   > "All necessary user licenses must be signed and payment made before an order is processed."
   → **行政前置時間才是真正的成本,不是錢。**

### 價格(2026-08-12 查證,USD)

| 語料庫 | 非會員 | Reduced-License | 當年度會員 |
|---|---|---|---|
| LDC2005S22 Articulation Index | **$1,500.00** | $750.00 | $0.00 |
| **LDC2015S12 Articulation Index LSCP** | **$0.00** | $0.00 | $0.00 |

**LSCP 版免費,而且它正是 AVWM 想要的那個版本**(已切好、已人工校邊界、wav 格式)。
原版 $1,500 只多給:三音節(CVC/CCV/VCC)、8 kHz 電話頻寬版、少量對話語料 ——
**AVWM 一項都用不到。不要買原版。**

另有 **LDC2017S16 (LDC Spoken Language Sampler – 4th Release)**,非會員也 $0.00,
頁面寫 "The sampler is available as a free download",內含 Articulation Index LSCP 的樣本。
→ **可以先抓這個免費 sampler 試聽,再決定要不要走完整授權流程。**

### 對 AVWM 能不能用
**能,而且這是我這輪查到最好的選項。** 逐項對規格:

| AVWM 規格 | AIC LSCP | 判定 |
|---|---|---|
| 英語 | 美式英語母語者 | ✅ |
| 單一 CV 音節 | 孤立 CV,獨立音檔 | ✅ |
| /b/ 與 /p/ | 都有 | ✅ |
| 母音優先 /i/ | `i` = iː,`*_s_bi` / `*_s_pi` | ✅ |
| 能乾淨切出音節 | **已經切好、頭尾靜音已去除、邊界人工校過** | ✅✅ |
| **取樣率 ≥ 22.05 kHz** | **16 kHz** | ❌ **不合規格** |
| 多語者加分 | **20 位(12M/8F)** | ✅✅ |

**唯一的硬傷是 16 kHz(Nyquist 8 kHz)。** 我的判斷是**這對 /b/–/p/ 影響有限**:
唇音爆破的頻譜是低頻主導的 diffuse-falling,VOT、F1 起始、爆破強度這些
voicing 線索全在 8 kHz 以下。若換成 /s/–/ʃ/ 這種靠高頻擦音譜的對比,16 kHz 就會是真傷。
**但這是我的推理,不是官方保證** —— 且若 AVWM 的 SNR 操弄要在寬頻噪音下比較,
刺激頻寬上限 8 kHz 會直接決定噪音濾波的設計,這點必須在方法段講明。
上取樣到 44.1 kHz 只是格式對齊,**不會增加任何資訊**。

### 工作量估計
- **行政(主要成本)**:註冊 LDC 帳號 → 取得機構簽名 → email/fax 回 LDC → 等審核。
  **抓不準,樂觀 3 天、保守 2–3 週。**
- **技術(次要)**:下載 → `grep` 出 40 個檔 → RMS 正規化 → 試聽挑語者。
  **半天到一天。**

### 限制
- 每位語者**每個音節只有 1 個 token**(`doc.txt`: "It was deemed sufficient to collect a
  single token of each particular syllable a speaker was to say.")。
  → 想要 [[silbert2012]] 那種「每類 4 個 token」的自然變異,**只能靠跨語者**,
  不能靠同一語者的多次發音。這會改變 GRT 分布的解釋(語者變異 vs. 發音變異混在一起)。
- 錄音年代久(2003–2005 錄製),麥克風/前級是當年規格。
- 有 113 個檔有削波(`doc/clipping.txt`,最嚴重 9 個 sample),需確認 bi/pi 不在其中。
- `doc.txt` 自陳 cot/caught 合併造成 [a]/[c] 的標註錯誤。**/i/ 不受此影響**,選 /i/ 反而更安全。
- 我沒有下載資料,音質好壞、語者間音量差異、是否有明顯口音,**全部未實聽驗證**。

## 可連結脈絡
- 為什麼要用自然音而非合成音,以及「在噪音中辨識 CV」的設計先例 —— [[silbert2012]]
- 同一個 SNR 路線的理由 —— [[natural-vs-synthetic-speech]]、[[snr_audio]]
- /b/–/p/ 這組對比的選擇理由 —— [[consonant-pair-choice]]、[[abramson2017]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]、[[timit]]、[[oscaar-speechbox]]
- 合成路線做不到 VOT 的證據 —— [[mbrola-cannot-do-vot]]
- Miller–Nicely 式子音混淆傳統 —— [[humes1993]]、[[winn2020]]
- **同一個語料庫在 [[phatak-allen2007]] / [[singh-allen2012]] 被用來做安靜下的 utterance 層級子音混淆分析** —— 見 [[子音混淆最小化]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**LDC 有沒有孤立 CV 音節的英語語料庫?** → 有,而且只有這一家:Articulation Index Corpus
(LDC2005S22),加值版 Articulation Index LSCP(LDC2015S12)。20 位語者 × 所有合法 CV/VC。

**Jont Allen 實驗室的 CV 音節語料公開嗎?** → 他們沒有自建公開語料庫;他們用的就是 LDC2005S22,
而 Allen 本人是這個語料庫的設計顧問之一。

**有沒有非會員免費、又有孤立 CV 音節的 LDC 語料庫?** → 有,LDC2015S12 非會員價 $0.00
(2026-08-12 查證)。仍需簽 LDC User Agreement for Non-Members。

**我要的 /bi/、/pi/ 檔名長什麼樣?** → `<speaker>_s_bi.wav`、`<speaker>_s_pi.wav`,
`s` 表 isolated,20 位語者各一。
