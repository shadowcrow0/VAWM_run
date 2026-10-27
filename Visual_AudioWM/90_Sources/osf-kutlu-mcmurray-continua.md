---
tags: [literature-note, 刺激來源, 語音知覺, AVWM]
citekey: osf-kutlu-mcmurray-continua
---

# OSF `bwcz7`(Kutlu & McMurray 2024)— **CC0 授權、8 條 9 步自然連續體,含 beach–peach(母音 /i/)**

**DOI / URL**
- OSF 專案 https://osf.io/bwcz7/ (論文給的是含 view-only token 的版本,見下)
- 論文 https://pmc.ncbi.nlm.nih.gov/articles/PMC11582665/ ‧ https://www.nature.com/articles/s41598-024-80430-1
- 檔案直鏈範例 https://osf.io/download/tbvwe/ (`beachpeach4.wav`)

**查證狀態**(2026-08-12)
- 論文全文由 PMC 版讀取(PMC11582665),**Data availability 是逐字引句**。
- OSF 內容全部走 `https://api.osf.io/v2/nodes/bwcz7/...` 取得(網頁版是 SPA,讀不到)。
  `public: true`、`date_created: 2024-04-21`。
- **授權是我實際查 API 確認的**:`relationships.license` → id `563c1cf88c5e4a3877f9e96c`
  → 展開後 `name: "CC0 1.0 Universal"`。**這是官方明文的 metadata,不是推論。**
- **我實際下載了 `beachpeach4.wav` 並讀 header**,規格見下。
  其餘 71 個 wav **未下載**,規格是**假定與此檔一致**(未驗證)。
- **2026-08-13 更新:beachpeach 全部 9 檔已下載並逐檔驗證**,
  存於 repo 的 `stimuli/kutlu_mcmurray_2024/`。全部 mono / 44,100 Hz / 16-bit,
  時長 0.684–0.686 s(**幾乎等長 —— 原「9 步時長會不一致」的疑慮不成立**,
  拼接時已保持等長)。9 個 md5 相異。
  onset 後 20–80 ms 的週期性 step 1→9 為 0.757→0.660(step 3 起嚴格單調),
  峰值同步從 0.219 降到 0.197 —— 與送氣漸進取代嗓音一致。
  ⚠️ 每步與 step 1 的波形差異延伸到整段 ~540 ms,代表拼接後有整檔再處理
  (可能是位準正規化),不是只動開頭。
  **AVWM 已決定採用本刺激集**(選項 F,見 [[聽覺維度_嘗試與放棄紀錄]]);
  受試者為英語母語者,L2 詞彙編碼的疑慮不適用。
- ⚠️ OSF 專案標題(`Social Network Diversity Leads to More Flexible Speech Perception in
  School-aged Children`)與論文出版標題(`Linguistic diversity shapes flexible speech
  perception in school age children`)**不同** —— 應是投稿過程改名,但我未找到明文說明。
- ⚠️ 語者資訊(「一位美國中西部口音成年男性、mono、44,100 Hz」)**出現在搜尋摘要中,
  我沒有在原文裡直接讀到這句**。標為**未確認**。

```bibtex
@article{kutlu2024linguistic,
  author  = {Kutlu, Ethan and Baxelbaum, Keith and Sorensen, Eldon and
             Oleson, Jacob and McMurray, Bob},
  title   = {Linguistic diversity shapes flexible speech perception in school age children},
  journal = {Scientific Reports},
  volume  = {14}, pages = {28825}, year = {2024},
  url     = {https://www.nature.com/articles/s41598-024-80430-1}
}
```
> BibTeX 為**我自組**;DOI 我未逐字核對,只確認了 volume 14 / article 28825。

## 研究問題
論文問的是「語言環境多樣性會不會讓學齡兒童的語音知覺更有彈性」。
**與 AVWM 的研究問題無關**;本卡的價值在刺激檔與**授權**。

Data availability 逐字:
> "All data and scripts can be found on our OSF repository
> (https://osf.io/bwcz7/?view_only=2377429c7c6847feae8d6d0998644180)."

⚠️ 論文給的是 **view-only 連結**,但 API 顯示這個節點 **`public: true`**,
去掉 token 一樣讀得到、下載得到。（我兩種都試過。）

## 方法與族群

### `stimuli` 資料夾:88 個項目 = 72 個 wav + 16 個 png
**8 條連續體 × 9 步**,命名一律 `<配對><步數>.wav`:

| 連續體 | 對比 | 類型 | 對 AVWM 的相關性 |
|---|---|---|---|
| **`beachpeach1–9`** | **/b/–/p/ 送氣起始時間** | 自然 cross-splicing | ★ **直接相關** |
| `dimetime1–9` | /d/–/t/ | 自然 cross-splicing | 對照 |
| `batbet1–9` | /æ/–/ɛ/ | TANDEM-STRAIGHT morphing | — |
| `penpan1–9` | /ɛ/–/æ/ | TANDEM-STRAIGHT | — |
| `beetboot1–9` | /i/–/u/ | TANDEM-STRAIGHT | — |
| `hathot1–9` | /æ/–/ɑ/ | TANDEM-STRAIGHT | — |
| `netnut1–9` | /ɛ/–/ʌ/ | TANDEM-STRAIGHT | — |
| `shipsip1–9` | /s/–/ʃ/ | spectral averaging | — |

論文 Methods 對製作方式的說明:VOT 連續體用 "progressive cross splicing procedure";
擦音用 "spectral averaging procedure";母音用 **TANDEM-STRAIGHT** morphing;
全部 9 步。

### `beachpeach4.wav` 實測規格(我下載驗證)
| 項目 | 實測值 |
|---|---|
| 聲道 | mono |
| 取樣率 | **44,100 Hz** |
| 位元深度 | 16-bit |
| 時長 | 0.685 s |

### 專案其他資料夾
`scripts/`、`data/`(未展開;本卡只關心 `stimuli/`)。

## 結果與限制

### 最大優點:**CC0 1.0 Universal**
這是本次全部查證中,**唯一一個既有 /b/–/p/ 自然刺激、又是 CC0 的來源**。
CC0 = 公眾領域奉獻,**可以任意重製、改作、重散布,連署名都不強制**
(當然學術上仍應引用)。這意味著 AVWM 若拿它做二次加工,
**可以把加工後的刺激連同論文一起公開** —— 對照 [[osf-kapnoula-vot-f0-stimuli]] 完全沒有授權、
[[timit]] 明文禁止重散布、[[articulation-index-corpus]] 的 LDC 條款。

### 最大缺點:**beach/peach 是 CVC 詞,不是孤立 CV 音節**
`beach` = /biːtʃ/、`peach` = /piːtʃ/。要拿到 CV 得砍掉尾端的 /tʃ/。

- **好消息**:母音正好是 **/i/**,完全命中 AVWM 的第一順位母音。
- **壞消息**:從詞裡切 CV 會留下協同構音(coarticulation)的痕跡 ——
  /biː/ 在 `beach` 裡的母音已經被後接的 /tʃ/ 影響(至少是時長縮短,
  英語的 pre-fortis clipping)。這正是 [[silbert2012]]、[[timit]] 一再指出的問題。
- 而且 0.685 s 的詞切成 CV 後,9 個步階的**時長會不一致**(端看各步的切點),
  要另外做等長處理。

| AVWM 規格 | 本刺激集 | 判定 |
|---|---|---|
| 英語單一 CV 音節 | **CVC 單詞**,需自行切 | ❌ |
| 子音 /b/ 與 /p/ | ✅ `beachpeach` | ✅ |
| 母音優先 /i/ | **/i/** | ✅ **命中** |
| 取樣率 ≥ 22.05 kHz | 44,100 Hz | ✅ |
| 能乾淨切出 | 需切尾 /tʃ/,有 pre-fortis clipping 疑慮 | ⚠️ |
| 多語者 | **單一語者(未確認)** | ❌ |
| 授權 | **CC0 1.0** | ✅ **最佳** |

### 其他限制
- 只有一維(VOT),**沒有第二個正交維度**。若 AVWM 要 GRT 的二維格點,
  這批得自己加 F0 維度(可用 [[winn2020]] 的腳本 + PSOLA)。
- ~~我**只驗證了 1 個 wav**。其餘 71 檔的取樣率/時長是假定,未逐檔確認。~~
  **2026-08-13:全部 72 個 wav 已逐檔下載驗證(讀 RIFF header,非狀態碼)。**
  0 個損壞,規格完全一致:mono / 44,100 Hz / 16-bit。各連續體時長:

  | 連續體 | 時長範圍 (s) | 步內等長? |
  |---|---|---|
  | beachpeach | 0.684–0.686 | ✅ 幾乎等長 |
  | dimetime | 0.669–0.671 | ✅ 幾乎等長 |
  | shipsip | 0.610–0.610 | ✅ 完全等長 |
  | hathot | 0.605–0.625 | ⚠️ 差 20 ms |
  | netnut | 0.635–0.660 | ⚠️ 差 25 ms |
  | beetboot | 0.394–0.445 | ⚠️ 差 51 ms |
  | penpan | 0.482–0.542 | ⚠️ 差 60 ms |
  | batbet | 0.362–0.574 | ⛔ 差 212 ms |

  **兩條 VOT 連續體(beachpeach、dimetime)都幾乎等長** —— 若混淆查證偏向
  /d/–/t/,同一資料集內就有現成替代,不必換來源(但 dime/time 母音是 /aɪ/ 非 /i/)。
- 16 個 png 檔名是亂數(如 `-100161185105758799.png`),用途不明,我未開啟。

## 可連結脈絡
- 同為 McMurray 系、但有二維格點且母音為 /ʌ/ —— [[osf-kapnoula-vot-f0-stimuli]]
- 為什麼不該從詞裡切音節 —— [[silbert2012]]、[[timit]]、[[oscaar-speechbox]]
- cross-splicing 的方法學 —— [[winn2020]]、[[goldenberg2022]]
- 授權可否重散布的橫向比較 —— [[oscaar-speechbox]]、[[articulation-index-corpus]]、[[timit]]
- McMurray 的漸進性理論脈絡 —— [[mcmurray2008]]、[[mcmurray2022]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**有沒有 CC0 授權、可以連同論文公開的自然 /b/–/p/ 刺激?** → **有,只有這一個。**
OSF `bwcz7` 的 `beachpeach1–9.wav`,CC0 1.0 Universal,44.1 kHz/16-bit/mono。

**它的母音是 /i/ 嗎?** → **是**(beach /biːtʃ/、peach /piːtʃ/),完全命中 AVWM 的首選母音。
**但它是 CVC 單詞,不是孤立 CV**,要切掉尾端 /tʃ/,而且會帶 pre-fortis clipping。

**論文給的 OSF 連結有 view_only token,是不是私有的?** → **不是。**
API 顯示 `public: true`,把 `?view_only=...` 拿掉照樣讀得到、下載得到。

**這個 OSF 專案還有什麼?** → 另外 6 條母音連續體(TANDEM-STRAIGHT morphing)
+ 1 條擦音(spectral averaging)+ `dimetime`(/d/–/t/),全部 9 步。
