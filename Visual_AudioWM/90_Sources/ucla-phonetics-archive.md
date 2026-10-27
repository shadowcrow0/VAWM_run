---
tags: [literature-note, 刺激來源, 語音知覺, AVWM]
citekey: ucla-phonetics-archive
---

# UCLA Phonetics Lab Archive — **628 種語言、CC 授權、44.1 kHz,但英語只有「整份詞表一個檔」,沒有孤立 CV 音節**

**DOI / URL**(全部於 2026-08-12 實際開啟)
- 首頁(frameset)http://archive.phonetics.ucla.edu/
- 說明 https://archive.phonetics.ucla.edu/intro.htm
- **使用與授權** https://archive.phonetics.ucla.edu/archive_instructions.htm
- 語言資料庫 https://archive.phonetics.ucla.edu/archive.htm
- **已上線語言清單** https://archive.phonetics.ucla.edu/Language%20Indices/index_available.htm
- **英語頁** https://archive.phonetics.ucla.edu/Language/ENG/eng.html

**查證狀態**(2026-08-12)
- ⚠️ **首頁是 1990 年代的 frameset**,直接 WebFetch 只會拿到 `<frameset>` 骨架,毫無內容。
  必須逐一開啟 `intro.htm`、`nav_bar.htm`、`archive.htm` 等內頁。導覽列在
  `main_frameset_files/nav_bar.htm`(注意:根目錄的 `nav_bar.htm` 是 **404**)。
- 上列六個 URL **我全部實際開啟並讀到內容**。
- **取樣率是我用 HTTP Range 請求驗證的**:對
  `https://archive.phonetics.ucla.edu/Language/ENG/eng_word-list_1964_01.wav`
  取前 200 bytes 並解 `fmt ` chunk → **mono / 44,100 Hz / 16-bit**。
  **官方頁面完全沒有寫取樣率**,這是我自己量的。
- ⚠️ **授權的確切 CC 版本我查無。** `archive_instructions.htm` 用**散文**描述條款
  (非商業、相同方式分享、須標示出處),**沒有 CC 版本號、沒有授權連結、沒有 CC 徽章**。
  「這等同 CC BY-NC-SA」是**我的推論**,不是官方明文。
- ⚠️ 語言總數 628 與「英語代碼 ENG」出自 `index_available.htm` 的 WebFetch 摘要,
  **我沒有自己數過那 628 個項目**。
- ⚠️ 個別錄音的 "Details" 頁我**沒開成功**(我猜的 URL 是 404),
  所以**錄音年代以外的 metadata、錄音設備、原始取樣率是否經過重取樣,查無**。

```bibtex
@misc{ucla_phonetics_archive,
  author       = {{UCLA Department of Linguistics}},
  title        = {The {UCLA} Phonetics Lab Archive},
  year         = {2007},
  address      = {Los Angeles, CA},
  howpublished = {\url{http://archive.phonetics.ucla.edu/}},
  note         = {Accessed 2026-08-12}
}
```
> **官方指定引用格式逐字**:
> "2007. The UCLA Phonetics Lab Archive. Los Angeles, CA: UCLA Department of Linguistics.
> http://archive.phonetics.ucla.edu/."
> BibTeX 包裝是我自組的。

## 研究問題
不是研究,是**田野語音學檔案庫**。`intro.htm` 逐字:

> "Welcome to the UCLA Phonetics Lab Archive. For over half a century, the UCLA Phonetics
> Laboratory has collected recordings of hundreds of languages from around the world,
> providing source materials for phonetic and phonological research."

> 館藏的音訊與其附帶文字 "is comprised mainly of recordings intended to illustrate the
> phonetic structures of languages."

定位:"open to everyone" 但 "primarily intended to be used by the linguistics community",
經費來自 NSF。

## 方法與族群

### 規模與範圍
- **628 種語言**上線(Abaza 到 Zulu),**含英語(代碼 ENG)**。
- 涵蓋 French、Spanish、Mandarin、Arabic 等大語言,以及 Pirahã、Juǀ'hoan、
  澳洲原住民語等田野語言。`!Xóõ` 這類以 `!` 開頭的語言按第二個字母排序。

### 每個語言頁的結構(以英語頁為例)
表格欄位:`Word List` / `Word List Entries` / `Additional Info` / `Audio Filename` /
**`WAV`** / **`MP3`** / `Scanned Word List (JPG)` / `JPG 2` / `(TIF)` / `TIF 2` / `Recording Details`

英語的前幾筆(逐項抄錄):

| # | 音檔名 | 詞條範圍 | 語者資訊 |
|---|---|---|---|
| 1 | `eng_word-list_1964_01` | **1–106** | unknown; American (not specified) |
| 2 | `eng_word-list_1966_01` | 1–46 | New York, New York, U.S.A.; American (New York) |
| 3 | `eng_word-list_1966_02` | 1–39 | unknown; American (Midwest) |
| 4 | `eng_word-list_1976_01` | 1–8 | unknown; American (not specified) |
| 5–11 | `eng_word-list_1976_02` ~ `_08` | 各 1–11 | unknown; American (not specified) |

**→ 這就是關鍵:一個 WAV = 一整份詞表(最多 106 個詞連續唸完)。**
不是一詞一檔,更不是一音節一檔。

### 授權與取得(`archive_instructions.htm`)
- 條款(該頁散文,非逐字):Creative Commons、**限非商業用途**、
  **衍生作品須採用相同授權**、須**標示出處為 UCLA Phonetics Lab Archive**。
- 音訊格式:**WAV 與 MP3 兩種**。頁面明說 WAV 檔較大但
  "of considerably higher quality"。
- 下載方式(逐字):
  > "right-click (Macintosh Control + Click) a link and select 'Save File As...'"
- 另有 Unicode 詞表文字檔 + 原始田野筆記掃描(JPG 壓縮 / TIF 未壓縮),
  掃描版常含 Unicode 版沒有的細節。
- 頁面**未載明取樣率**(我實測為 44.1 kHz,見上)。

## 結果與限制

### 對 AVWM 的判定:**不能當刺激來源**
| AVWM 規格 | UCLA Archive | 判定 |
|---|---|---|
| 英語 | ✅ 有(ENG) | ✅ |
| **英語單一 CV 音節** | **完全沒有**;最小單位是「整份詞表」 | ❌ **關鍵不合** |
| 子音 /b/ 與 /p/ | 詞表裡當然有,但埋在連續朗讀裡 | ❌ |
| 母音 /i/ / /ɑ/ | 詞表未逐一檢查 | ❓ |
| **能乾淨切出** | 要從 106 詞的連續錄音自行切,**比 [[timit]] 更糟**(至少 TIMIT 有音素層標註;這裡只有一份文字詞表) | ❌ |
| 取樣率 ≥ 22.05 kHz | **44,100 Hz(我實測)** | ✅ |
| 多語者 | 英語約十餘份錄音,但語者多半標 "unknown" | ⚠️ |
| 授權可重散布 | 非商業 + 相同方式分享 → **可以重散布,但會把 NC 條款傳染給 AVWM 的刺激集** | ⚠️ |

### 這個檔案庫真正的定位錯配
它的設計目的是**展示語言的音韻結構**給語言學家看,
所以錄的是**詞表**(用來對照 IPA 轉寫),不是**知覺實驗刺激**。
兩者對「切分粒度」的要求根本不同。這一點與 [[oscaar-speechbox]] 的失敗原因同型:
**語料庫的最小單位是詞或更大,而 AVWM 要的是音節。**

### 額外的實務問題
- 1964–1976 年的**類比母帶轉錄**。即使檔案是 44.1 kHz,
  **原始錄音的頻寬與訊噪比受限於當年的設備**,而且 "Details" 頁我打不開,無從確認。
  拿 1960 年代的田野錄音做需要精確 VOT 操弄的刺激,風險很高。
- 語者絕大多數標為 "unknown",**性別、年齡、口音都不可控** ——
  對「多語者加分」這個目標其實幫不上忙。
- **NC(非商業)條款有傳染性**:若 AVWM 從這裡取材,產出的刺激集也得掛 NC,
  這會比 [[osf-kutlu-mcmurray-continua]] 的 CC0 差很多。

### 保留價值
若 AVWM 之後需要**非英語**的對照材料(例如做跨語言 VOT 的討論),
628 種語言的覆蓋率無可取代。作為刺激來源不行,作為**參照與舉例**有價值。

## 可連結脈絡
- 同型失敗(語料庫最小單位是詞) —— [[oscaar-speechbox]]、[[timit]]
- 真正有孤立 CV 的來源 —— [[articulation-index-corpus]]、[[osf-kapnoula-vot-f0-stimuli]]
- 為什麼不能從連續朗讀裡切音節 —— [[silbert2012]]
- 跨語言 VOT 的分布 —— [[chodroff2017]]、[[chodroff2019]]、[[abramson2017]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**UCLA Phonetics Lab Archive 有英語嗎?** → **有**(代碼 ENG,628 種語言之一)。
**但英語只有「詞表」錄音,一個 WAV 裝一整份最多 106 個詞的連續朗讀。**
沒有孤立 CV 音節,沒有一詞一檔。

**它的取樣率多少?** → **44,100 Hz / 16-bit / mono**。
⚠️ **官方頁面沒寫**,這是我對 `eng_word-list_1964_01.wav` 用 HTTP Range 抓前 200 bytes
解 `fmt ` chunk 量出來的。

**它的授權是哪個 CC?** → **查無版本號。** 頁面只用散文寫「非商業 + 相同方式分享 + 標示出處」,
沒有 CC 徽章或版本連結。等同 CC BY-NC-SA 是**我的推論**。
⚠️ NC 條款會傳染給 AVWM 的產出。

**為什麼直接抓首頁什麼都沒有?** → 它是 **frameset**。內容在 `intro.htm`、
`archive_instructions.htm`、`archive.htm` 等內頁;導覽列在
`main_frameset_files/nav_bar.htm`(根目錄的 `nav_bar.htm` 是 404)。
