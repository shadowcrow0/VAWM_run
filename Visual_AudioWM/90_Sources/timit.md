---
tags: [literature-note, 語音語料庫, 刺激來源, AVWM]
citekey: timit
---

# TIMIT (LDC93S1) — 630 位語者的**連續句子** + 音素層對齊;對 AVWM 是錯的工具

**DOI / URL**
- 目錄頁 https://catalog.ldc.upenn.edu/LDC93S1 (DOI https://doi.org/10.35111/17gk-bn40)
- 公開樣本(不需登入): https://catalog.ldc.upenn.edu/desc/addenda/LDC93S1.wav
  · https://catalog.ldc.upenn.edu/desc/addenda/LDC93S1.phn
  · https://catalog.ldc.upenn.edu/desc/addenda/LDC93S1.txt
  · https://catalog.ldc.upenn.edu/desc/addenda/LDC93S1.wrd
- 授權書全文 PDF https://catalog.ldc.upenn.edu/license/ldc-non-members-agreement.pdf
- 取得流程 https://www.ldc.upenn.edu/language-resources/data/obtaining

**查證狀態**(全部於 **2026-08-12** 實際開啟)
- 目錄頁全文抓取並讀過;授權 PDF 下載後轉文字讀過全文。
- **公開樣本我真的下載並檢查了**:`.wav` 經 `wave` 模組讀出 **16000 Hz / mono / 16-bit /
  46797 frames**;`.phn` 前 20 行逐行看過。故「16 kHz」「有音素層時間對齊」是**我親自驗證**的,
  不是只看網頁宣稱。
- **價格從目錄頁 HTML 的 `data-price-table` 讀出**,非登入後結帳頁。對照組見 [[articulation-index-corpus]]。
- **我沒有取得完整語料庫**,「TIMIT 裡有多少個可用的 /bi/、/pi/」我**沒有實際統計過**,
  下方相關敘述是根據語料庫設計(連續句子)的**推論**,必須標為未證實。
- **「openslr 上有免費 TIMIT」是錯的** —— 見下方「免費替代」節,我實際查了。

```bibtex
@misc{garofolo1993timit,
  author       = {Garofolo, John S. and Lamel, Lori F. and Fisher, William M. and
                  Fiscus, Jonathan G. and Pallett, David S. and Dahlgren, Nancy L. and
                  Zue, Victor},
  title        = {{TIMIT} Acoustic-Phonetic Continuous Speech Corpus {LDC93S1}},
  howpublished = {Web Download},
  address      = {Philadelphia},
  publisher    = {Linguistic Data Consortium},
  year         = {1993},
  doi          = {10.35111/17gk-bn40}
}
```
> BibTeX 是**我自組**的。LDC 官方 citation 逐字為:
> "Garofolo, John S., et al. TIMIT Acoustic-Phonetic Continuous Speech Corpus LDC93S1.
> Web Download. Philadelphia: Linguistic Data Consortium, 1993."

## 研究問題
不是為知覺實驗建的,是為**聲學-語音研究與 ASR 評測**建的。目錄頁逐字:

> "The TIMIT corpus of read speech is designed to provide speech data for acoustic-phonetic
> studies and for the development and evaluation of automatic speech recognition systems."

MIT / SRI International / Texas Instruments 三方合作,TI 錄音、MIT 轉寫、NIST 驗證。

## 方法與族群
目錄頁逐字:

> "TIMIT contains broadband recordings of 630 speakers of eight major dialects of American
> English, each reading ten phonetically rich sentences."

> "The TIMIT corpus includes time-aligned orthographic, phonetic and word transcriptions as
> well as a single channel, 16-bit, 16kHz speech waveform file for each utterance. The TIMIT
> corpus transcriptions have been hand verified."

- **語者數:630**(目錄頁:"Of the 630 speakers, about 70% are men and 30% are women.")
- **取樣率:16 kHz、16-bit、單聲道** —— 我下載樣本 wav 實測確認
- 每人 10 句 → 約 6,300 個 utterance,總長約 5 小時
- 語者 metadata 含 gender、dialect、birth date、height、race、education level
- 已切好 phonetic / dialectal 平衡的 train / test 子集

**錄的是句子,不是孤立音節。** 公開樣本的 transcript 逐字就是那句著名的 SA1:
> `0 46797 She had your dark suit in greasy wash water all year.`

**音素層標註的形式**(我實際讀的 `.phn` 前幾行,欄位為 起始sample、結束sample、phone):
```
0     3050  h#
3050  4559  sh
4559  5723  ix
...
8772  9190  dcl
9190  10337 jh
...
12500 12640 d
...
15870 16334 k
```
**注意:TIMIT 的 phone set 把塞音的閉鎖段與釋放段分開標**(`dcl`/`d`、`kcl`/`k`、`gcl`/`g`)。
→ 這對 VOT 研究其實很有用:閉鎖結束 = 釋放點,可直接讀出。
[[chodroff2014]]、[[chodroff2019]] 這類大規模 VOT 研究就是吃這種資料。
**但那是「測量 VOT」的用途,不是「當知覺刺激」的用途。**

時間單位是 **sample index**(16 kHz),不是秒,換算時別搞錯。

## 結果與限制

### 授權(逐字)
**LDC User Agreement for Non-Members**,與 [[articulation-index-corpus]] 同一份合約。關鍵句:

> "User agrees to use the LDC Databases received under this Agreement only for **non-commercial
> linguistic education, research and technology development**."

> "Unless explicitly permitted herein, User shall **not otherwise publish, retransmit, disclose,
> display, copy, reproduce or redistribute** the LDC Databases to others outside of User's
> Research Group."

落款欄為 "For the organization: ______",**機構級簽署**。

### 價格(2026-08-12 查證,USD)

| 級別 | 金額 |
|---|---|
| **Non-Member** | **$250.00** |
| Reduced-License | $125.00 |
| 1993 Member | $0.00 |

### 免費 / 合法替代 —— 我實際查證的結果
- **openslr 上沒有 TIMIT。** 我抓了 https://openslr.org/index.html 全文,
  **"TIMIT" 出現 0 次**。網路上把 https://www.openslr.org/18/ 說成 TIMIT 是**錯的** ——
  我開了該頁,那是 **THCHS-30**(清華中文語料庫,Apache License 2.0),與 TIMIT 無關。
- GitHub / Kaggle / HuggingFace 上流傳的完整 TIMIT 鏡像,**在 LDC 授權下屬於違約重散布**
  (見上引 "shall not... redistribute")。**不推薦、不使用。**
- **LDC 自己提供的合法免費樣本**:上列四個 `desc/addenda/` 檔(1 句 wav + phn + txt + wrd),
  不需登入即可下載。**只有 1 句**,只能用來看格式,不能當刺激來源。
- 若只是要「英語連續語音 + 發音人 + 免費」,**MOCHA-TIMIT** 是合法替代:
  https://data.cstr.ed.ac.uk/mocha/ ,直接下載無需申請。
  其 `LICENCE.txt` 逐字:
  > "Permission to use, copy, modify, distribute this data and its documentation for
  > **research, educational and individual use only**, is hereby granted without fee"
  > "This data may not be used for commercial purposes without specific prior written
  > permission from the authors."
  但 **MOCHA 唸的是 460 句 TIMIT 句子、只有 2–3 位語者、16 kHz、英式英語(fsew0 南英女聲、
  msak0 北英男聲)**,對 AVWM 比 TIMIT 更不合用。

### 對 AVWM 能不能用 —— **不建議**
| AVWM 規格 | TIMIT | 判定 |
|---|---|---|
| 英語 | 美式英語,8 種方言 | ✅ |
| **單一 CV 音節** | **連續句子**,無孤立音節 | ❌ **根本性不合** |
| /b/ 與 /p/ | 有,但都在詞內、有語境 | ⚠️ |
| 母音優先 /i/ | `iy` 有標,但 b/p + iy 的**數量未知** | ⚠️ 未證實 |
| 能乾淨切出音節 | 要從連續語音硬切 | ❌ |
| 取樣率 ≥ 22.05 kHz | **16 kHz** | ❌ |
| 多語者 | **630 位** | ✅✅ |

**核心問題不是價錢,是刺激類型錯了。** 從 TIMIT 切 /bi/ 會得到:
1. **詞內、有前後文的音節**,帶著共構(coarticulation)與跨詞邊界效應;
2. **重音、語速、語調位置全不受控**,而這些都會系統性改變 VOT;
3. 切出來的音節前後會殘留鄰音的 formant transition,**去掉會不自然,留著會引入額外維度** ——
   這正是 [[silbert2012]] 說要避開的「對相關聲學維度下強假設」的反面問題:
   你不但沒避開,還引入了一堆你沒控制的維度。

對 2×2 GRT 而言,刺激的**非目標維度變異必須可控**,否則估到的知覺相關會被混淆。
從連續語音切音節在這點上是最差的選擇。

### 工作量估計(若硬要做)
- 行政:同 AIC,機構簽署 + $250。
- 技術:寫腳本掃 630×10 個 `.phn`、找 `b`/`p` 後接 `iy` 的序列、切段、逐一試聽篩選、
  正規化、處理殘留 transition。**保守數天到一週**,
  而且**成品品質仍遠不如 AIC LSCP 的孤立音節**。
- → **投入更多、拿到更差。除非另有理由,不要走這條路。**

### 限制
- 我沒有統計 TIMIT 裡實際有多少 b/p + iy 的 token,**該數字未經證實**。
- 1993 年發行、更早錄製,音質是當年 CD-ROM 規格。
- 16 kHz Nyquist 8 kHz,與 AVWM 規格不符(同 [[articulation-index-corpus]] 的討論)。

## 可連結脈絡
- **真正該用的語料庫** —— [[articulation-index-corpus]](孤立 CV、非會員 $0)
- 為什麼刺激的非目標維度變異要可控 —— [[silbert2012]]
- 拿 TIMIT 做**VOT 測量**(而非刺激)的正當用法 —— [[chodroff2014]]、[[chodroff2019]]、[[chodroff2017]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]、[[oscaar-speechbox]]
- 合成路線的限制 —— [[mbrola-cannot-do-vot]]、[[klatt1980]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**TIMIT 非會員要多少錢?** → USD $250.00(2026-08-12 查證);Reduced-License $125.00。
授權是 LDC User Agreement for Non-Members,機構級簽署,僅限非商業研究。

**openslr 上有免費的合法 TIMIT 嗎?** → **沒有。** openslr 索引頁 "TIMIT" 出現 0 次;
openslr.org/18 是 THCHS-30 中文語料庫。網路上的完整 TIMIT 鏡像違反 LDC 的不得重散布條款。

**TIMIT 能不能拿來做 /bi/–/pi/ 刺激?** → 技術上可切,但**不該切**。它是連續句子,
切出來的音節帶著不受控的共構、重音與語速變異,對 2×2 GRT 是負面條件。
應改用 Articulation Index LSCP 的孤立音節。

**TIMIT 的 .phn 為什麼對 VOT 研究好用?** → 它把塞音閉鎖段與釋放段分開標(`dcl`/`d`、`kcl`/`k`),
釋放點可直接讀出。時間單位是 16 kHz 的 sample index,不是秒。
