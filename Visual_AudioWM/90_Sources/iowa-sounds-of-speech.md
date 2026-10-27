---
tags: [literature-note, 刺激來源, 語音知覺, AVWM]
citekey: iowa-sounds-of-speech
---

# Iowa Sounds of Speech — **有 /p/ 與 /b/,但音訊包在 mp4 的有損 AAC 裡、是單詞不是孤立音節、授權查無**

**DOI / URL**(2026-08-12 實際開啟)
- 站台 https://soundsofspeech.uiowa.edu/
- JS bundle https://soundsofspeech.uiowa.edu/main-JLEEMS5I.js
- 實測有效的媒體路徑 https://soundsofspeech.uiowa.edu/assets/phonemes/p-sound/examples/sound.mp4
  ‧ `.../b-sound/examples/sound.mp4` ‧ `.../p-sound/examples/word1.mp4`

**查證狀態**(2026-08-12)
- ⚠️ **這是 Angular SPA**。`https://soundsofspeech.uiowa.edu/` 與 `/english` 的 HTML
  只有 26,772 bytes 的殼,裡面只有標題與 skip link,**WebFetch 兩次都讀不到任何內容**。
- **我改抓 JS bundle `main-JLEEMS5I.js`(1,022,912 bytes)並反推**。
  以下的路徑規則、資料夾名、語言清單,**是我從 bundle 的模板字串與環境設定抽出來的**,
  不是從渲染頁面複製,**格式與實際 UI 可能有落差**。
- **媒體 URL 我用 HEAD 實測回 200**(三個都是 `Content-Type: video/mp4`,
  Apache/2.4.52,`last-modified: Wed, 06 May 2026`):
  `p-sound/examples/sound.mp4` 35,126 B ‧ `b-sound/examples/sound.mp4` 42,594 B ‧
  `p-sound/examples/word1.mp4` 35,128 B。
- **我下載了 `p-sound/examples/word1.mp4`(35,128 B)並檢查 box 結構**:
  brands `mp42/isom/avc1`,同時含 **`avc1`(視訊)** 與 **`mp4a`(AAC 音訊)** 兩條軌
  (`vide` + `soun` handler)。→ **確實有音軌。**
- ⚠️ **我沒有解碼、也沒有聽過任何一個檔。**
  因此:**「這是不是真人錄音」我無法確認。**
  站台以動畫著稱,音軌**可能**是配合動畫的真人發音錄音,
  但**這是我的推測,不是查證結果**。這一點必須自己開來聽才算數。
- ⚠️ **取樣率查無。** 音訊是 mp4 裡的 AAC,環境沒有 `ffprobe`,我沒有解 `stsd` box。
- ⚠️ **授權查無。** 我對整份 bundle 做關鍵字掃描,唯一找到的授權相關字串是
  對第三方的致謝:
  > "IPA dictionaries from the Open-licensed dictionary data project, available at
  > https://open-dict-data.github.io/"
  **站台本身的音訊/影片授權,沒有任何明文。**

```bibtex
@misc{iowa_sounds_of_speech,
  author       = {{University of Iowa}},
  title        = {Sounds of Speech},
  howpublished = {\url{https://soundsofspeech.uiowa.edu/}},
  note         = {Accessed 2026-08-12. No citation format or license stated on site.},
  year         = {n.d.}
}
```
> **完全是我自組**。⚠️ **站上沒有任何建議引用格式**,我掃過 bundle 也沒找到。

## 研究問題
不是研究,是**語音學教學工具**(發音器官動畫 + 例音),另有 iOS / Android app
(bundle 內有 App Store 與 Google Play 的下載徽章圖檔)。

## 方法與族群

### 站台結構(從 bundle 的環境設定抽出,逐字)
```
{production:!0, assetsPath:"assets/phonemes", home:"https://soundsofspeech.uiowa.edu"}
```
```
supportedLanguages = ["de","en","es"]
```
→ **英語、德語、西班牙語**三種。

### 媒體路徑規則(從 bundle 的 `setVideo()` 反推)
```
/assets/phonemes/<folderName>/examples/sound.mp4        ← 該音素本身
/assets/phonemes/<folderName>/examples/<n>              ← 例詞(word1.mp4, word2.mp4 ...)
/assets/phonemes/[es/]<folderName>/annotated/annotation-1000n.png  ← 標註圖
```
特例:`ʔ` 的 `sound` 會導向 `word4.mp4`。

### 英語的 `folderName` 清單(逐項抄錄,順序即 bundle 內順序)
**`p-sound`**、**`b-sound`**、`t-sound`、`d-sound`、`k-sound`、`g-sound`、
`f-sound`、`v-sound`、`s-sound`、`z-sound`、`h-sound`、`ch-sound`、
`m-sound`、`n-sound`、`ng-sound`、`l-sound`、`r-sound`、`j-sound`、
`i-sound`、`long-e-sound`、`ae-sound`、`long-ae-sound`、`long-a-sound`、
`er-sound`、`long-u-sound`、`long-o-sound`、`oi-sound`
(另有若干空字串的 `-sound`,應為 IPA 字元在抽取時被吃掉)

德語與西班牙語另有各自的完整清單,兩者也都有 `p-sound` / `b-sound`。

**→ /p/ 與 /b/ 兩個目標子音確實都在,而且三種語言都有。**

## 結果與限制

### 對 AVWM 的判定:**不能用**
| AVWM 規格 | Sounds of Speech | 判定 |
|---|---|---|
| 英語 | ✅ | ✅ |
| 子音 /b/ 與 /p/ | ✅ `b-sound` / `p-sound` | ✅ |
| **單一 CV 音節** | 例音是 **`word1`…`wordN`**,即**單詞**;`sound.mp4` 是單一音素而非 CV | ❌ |
| 母音 /i/ 或 /ɑ/ | 例詞未逐一開啟,**未確認** | ❓ |
| **能乾淨切出** | 要 **demux mp4 → 解 AAC → 再切**,而且動畫音軌可能對過時間軸 | ❌ |
| **取樣率 ≥ 22.05 kHz** | **查無**;而且是 **AAC 有損壓縮** | ❌ **關鍵不合** |
| 多語者 | 推測單一發音者,**未確認** | ❌ |
| 授權 | **查無任何明文** | ❌ |

### 三個各自足以否決的理由
1. **有損壓縮。** 音訊是 mp4 容器裡的 AAC。VOT 操弄要動的是 burst 與送氣段的
   **毫秒級時間結構與高頻能量**,而 AAC 正是在高頻與暫態上做取捨的編碼。
   即使解出來重取樣到 44.1 kHz,**失去的資訊不會回來**。
   這與 [[timit]]、[[articulation-index-corpus]] 提供未壓縮 WAV 的來源不是同一個等級。
2. **粒度是「單詞」或「單一音素」,不是 CV 音節。** 與 [[ucla-phonetics-archive]]、
   [[oscaar-speechbox]] 同型的錯配。
3. **沒有授權。** 連建議引用格式都沒有。學術使用的法律狀態不明。

### ⚠️ 本卡最大的未確認項
**我沒有聽過任何一個檔,所以「這是真人錄音還是合成」我不知道。**
任務原本要求確認這一點,**我做不到**:環境沒有 `ffprobe`/`ffmpeg`,
我只能從 mp4 box 結構確認「有一條 AAC 音軌存在」。
若之後要確認,最省事的做法是直接在瀏覽器開
`https://soundsofspeech.uiowa.edu/assets/phonemes/p-sound/examples/word1.mp4` 聽。

**但這一點其實已經不影響結論** —— 就算是真人錄音,
上面三個否決理由(有損、粒度、無授權)任一個都足以排除它作為 AVWM 的刺激來源。

## 可連結脈絡
- 同型的粒度錯配 —— [[ucla-phonetics-archive]]、[[oscaar-speechbox]]、[[timit]]
- 真正有孤立 CV 的來源 —— [[articulation-index-corpus]]、[[osf-kapnoula-vot-f0-stimuli]]
- 有損壓縮為何不能用於 VOT 操弄 —— [[winn2020]]、[[burst-vot-tradeoff]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**Iowa Sounds of Speech 有 /b/ 和 /p/ 嗎?** → **有**(`b-sound`、`p-sound`,
英/德/西三語都有)。**但例音是「單詞」,不是孤立 CV 音節。**

**音檔能取出來嗎?** → 能抓到檔,但**是 mp4**
(`/assets/phonemes/<folder>/examples/word1.mp4`),裡面是 **AAC 有損音軌 + H.264 動畫**。
要用得先 demux + 解碼。**取樣率查無。**

**是不是真人錄音?** → ⚠️ **我無法確認。** 我只驗證了 mp4 裡確實有一條 `mp4a` 音軌
(`soun` handler),但沒有解碼、沒有聽。要確認請直接用瀏覽器開該 mp4。

**授權是什麼?** → **查無。** 整份 JS bundle 掃描下來,唯一的授權字串是對
open-dict-data 的第三方致謝;站台自身的音訊授權與建議引用格式都沒有明文。

**為什麼 WebFetch 讀不到這個網站?** → Angular SPA,HTML 只有殼。
要讀內容得抓 `main-*.js` bundle 反推。
