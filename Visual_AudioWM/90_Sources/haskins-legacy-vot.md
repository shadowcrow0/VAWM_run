---
tags: [literature-note, 刺激來源, 語音知覺, AVWM]
citekey: haskins-legacy-vot
---

# Haskins Labs "Legacy: Abramson/Lisker VOT Stimuli" — **/ba/–/pa/ 可直接下載,但是 1960 年代的共振峰合成**(列為對照,非候選)

**DOI / URL**
- https://www.haskinslaboratories.org/vot(2026-08-12 實際開啟)

**查證狀態**(2026-08-12)
- 上述頁面**實際開啟並讀到內容**。以下關於「合成」「/ba/–/pa/」「可下載格式」的敘述
  來自該頁。
- ⚠️ **我沒有實際下載任何音檔**,所以**取樣率、位元深度、步階數、實際 VOT 值一律查無**。
  頁面本身也沒寫。
- ⚠️ **授權:頁面沒有任何授權或引用要求。** 頁尾只有
  "© 2026, HaskinsLaboratories.org and Philip Rubin"。
  「可自由使用」是**沒有根據的推論,不要假設**。
- ⚠️ 搜尋結果另外提到 `http://www.haskins.yale.edu/featured/bdg.php`
  (bae–dae–gae 的 13 步 Pattern Playback 連續體)。
  **這個網址我沒有實際開啟**,標為未證實。

```bibtex
@misc{haskins_vot_legacy,
  author       = {{Haskins Laboratories}},
  title        = {Legacy: {Abramson}/{Lisker} {VOT} Stimuli},
  howpublished = {\url{https://www.haskinslaboratories.org/vot}},
  note         = {Accessed 2026-08-12. No license or citation format stated on page.},
  year         = {n.d.}
}
```
> **自組。頁面未提供任何建議引用格式。** 若要引用內容本身,
> 應引 Lisker & Abramson 的原始論文(見 [[abramson2017]])。

## 研究問題
這是 Lisker & Abramson 那條經典 VOT 研究線的**歷史刺激**上網公開的頁面。
不是新研究,是檔案性質的釋出。

## 方法與族群
- **合成方式**:頁面明說使用 **Haskins Laboratories formant synthesizer**,
  以 "control VOT in measured increments"。
- **內容**:**單一一條唇音連續體,/ba/ → /pa/,母音 [a]**。
  基本型態是「三條穩態共振峰的 [a] 類母音」。此頁只做唇音,沒有跨部位比較。
- **可下載**:
  - 個別檔案:**MP3**(頁面逐字 "All are in MP3 format")
  - 打包:**ZIP,MP3 格式與 WAV 格式兩種**
    (頁面逐字 "Download audio files as a Zip in: MP3 format or WAV format")

**→ 這是本次查證中唯一「/ba/–/pa/、孤立 CV、一鍵可下載、不需申請」的來源。
唯一的問題是它是合成的。**

## 結果與限制

### 對 AVWM 的判定:**列為對照,不作為候選**
| AVWM 規格 | Haskins Legacy | 判定 |
|---|---|---|
| 英語單一 CV 音節 | ✅ /ba/、/pa/ | ✅ |
| 子音 /b/ 與 /p/ | ✅ | ✅ |
| 母音優先 /i/,其次 /ɑ/ | **[a]** | ⚠️ 第二順位 |
| **自然語音(真人錄音)** | **❌ 共振峰合成** | ❌ **決定性不合** |
| 取樣率 ≥ 22.05 kHz | **查無** | ❓ |
| 能乾淨切出 | 已是獨立檔 | ✅ |
| 多語者 | 無語者概念(合成) | ❌ |
| 授權 | **查無明文** | ⚠️ |

### 為什麼合成在這個專案裡是決定性的否決
AVWM 尋找**自然語音**是有明確理由的,不是偏好問題:
- 合成語音會**同時抹掉 VOT 以外的共變線索**(F0 起始、第一共振峰起始頻率、
  burst 頻譜、母音時長),而這些線索正是 GRT 要測「維度是否可分離」時
  必須**存在且可控**的東西。用只有單一線索的合成刺激測 separability,
  等於預設了答案。相關討論見 [[burst-vot-tradeoff]]、[[kingston2008]]。
- 1960 年代共振峰合成器的自然度,遠低於現代標準;
  聽者對明顯合成音的反應策略可能與對自然語音不同
  —— 見 [[burton-blumstein-naturalness]]。
- 專案內既有的 [[mbrola-cannot-do-vot]] 已經記錄過合成路線的另一個死結。

### 它仍然值得留一張卡的三個理由
1. **它是 VOT 這整條研究線的原點。** 寫方法學或引言時要交代
   「經典刺激長什麼樣、為什麼我們不用它」,需要一個可指的實體。
2. **它是唯一零摩擦可取得的 /ba/–/pa/ 連續體。** 若只是要做 pilot、
   驗程式流程、或給人聽個「VOT 連續體大概是什麼感覺」,它最快。
3. **它提供了「自然 vs 合成」對照的現成材料。** 若審稿人質疑自然刺激的可控性,
   拿它做對照組是可行的。

### 限制
- **取樣率未知**且個別檔是 MP3(有損);要用至少該抓 WAV 的 ZIP。
- **授權不明**,重散布有風險。
- 步階數、每步的實際 VOT(ms)我**沒有下載驗證**。

## 可連結脈絡
- Lisker & Abramson 這條研究線的正文 —— [[abramson2017]]
- 為什麼自然語音優於合成 —— [[burton-blumstein-naturalness]]、[[burst-vot-tradeoff]]、[[mbrola-cannot-do-vot]]
- 現代的自然替代方案 —— [[osf-kapnoula-vot-f0-stimuli]]、[[osf-kutlu-mcmurray-continua]]、[[goldenberg2022]]
- 自己做自然連續體的工具 —— [[winn2020]]、[[listenlab]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**有沒有一鍵就能下載的 /ba/–/pa/ 連續體?** → **有,Haskins 的 legacy 頁**
(https://www.haskinslaboratories.org/vot),個別 MP3 + 整包 ZIP(MP3 或 WAV),
不需申請不需登入。**但它是 1960 年代的共振峰合成,不是自然語音。**

**它的取樣率多少?步階多少?** → **查無。** 頁面沒寫,我也沒下載驗證。

**可以自由使用嗎?** → **不知道。** 頁面沒有任何授權或引用要求,
頁尾只有 "© 2026, HaskinsLaboratories.org and Philip Rubin"。**不要假設可自由重散布。**

**為什麼不用它?** → 合成語音抹掉了 VOT 以外的共變線索(F0 起始、F1 起始、burst 頻譜),
而 GRT 測維度可分離性時,這些線索必須存在且可控。用單線索合成刺激測 separability
等於預設答案。
