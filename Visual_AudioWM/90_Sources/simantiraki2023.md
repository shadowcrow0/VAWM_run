---
tags: [literature-note, 合成語音, 聆聽費力度, 瞳孔測量, 噪音, 現代TTS]
citekey: simantiraki2023
---

# Simantiraki, Wagner & Cooke (2023) — 清晰度與認知負荷不是簡單的反比

**DOI / URL** https://doi.org/10.3389/fnins.2023.1235911 | PMC10568627 | PMID 37841688
**閱讀狀態** ⚠️ **僅讀摘要**(2026-08-12 由 PubMed efetch 取得逐字摘要)。
**未讀全文** —— 因此**不知道用的是哪一種 TTS(是否為 neural)**、SNR 具體值、效果量。
這是引用本篇的最大不確定點。

```bibtex
@article{simantiraki2023impact,
  author  = {Simantiraki, Olympia and Wagner, Anita E. and Cooke, Martin},
  title   = {The impact of speech type on listening effort and intelligibility for
             native and non-native listeners},
  journal = {Frontiers in Neuroscience},
  volume  = {17}, pages = {1235911}, year = {2023},
  doi     = {10.3389/fnins.2023.1235911}
}
```

## 研究問題
不同「語音類型」(自然、Lombard、人工增強、合成)在噪音中的**清晰度**已經研究得很多,
但**認知處理需求**呢?清晰度最高的語音類型,是不是也就是最省力的?

摘要原文:
> "it is less clear how such types affect cognitive processing demands, and in particular
> whether those speech forms with the greatest intelligibility in noise have a
> commensurately lower listening effort."

**這對 AVWM 的意義**:AVWM 現在傾向的路線是「自然 token + speech-shaped noise」,
本篇正是在**噪音中**比較各種語音類型的認知負荷,是最貼近的現代文獻。

## 方法與族群
- 四種語音類型:(i) plain 自然語音;(ii) **Lombard 語音**(在噪音中說話自然產生的增強);
  (iii) 人工增強語音(頻譜塑形 + 動態範圍壓縮);(iv) **文字合成語音**。
- 三個依變項:清晰度、**自陳聆聽費力度**、**瞳孔測量的認知負荷**。
- 實驗 1:**26 名母語聽者**,三個等級的 speech-shaped noise。
- 實驗 2:**31 名非母語聽者**,較有利的 SNR。

⚠️ 摘要**沒有說明合成器是哪一個系統**。這對「現代合成是否仍有此效應」這個問題是關鍵缺口。

## 結果與限制

**摘要逐字:**
> "For both native and non-native listeners, artificially-enhanced speech was the most
> intelligible and led to the lowest subjective effort ratings, while **the reverse was
> true for synthetic speech**. However, **pupil data suggested that Lombard speech
> elicited the lowest processing demands overall**. These outcomes indicate that the
> relationship between intelligibility and cognitive processing demands is not a simple
> inverse, but is mediated by speech type."

### 對 AVWM 的三個結論

1. **合成語音在噪音中是四種類型裡最差的** —— 清晰度最低、**自陳費力度最高**。
   這是「現代合成仍有負荷代價」的正面證據,而且是在**噪音中**測的。
   (但**不知道是哪一個合成器**,所以「現代」的程度未知。)

2. **主觀費力度與瞳孔測量分歧** —— 主觀最省力的是人工增強語音,瞳孔最省力的卻是
   Lombard。這與 [[govender2018]] 的分歧模式一致:**認知負荷的不同指標不會一致收斂**。
   ⚠️ 這意味著任何「合成音的負荷有多大」的答案都**取決於用哪個指標**。

3. 作者的核心主張:清晰度與認知負荷**不是簡單反比**。
   → 因此不能用「我把 SNR 調到 75% 正確率,兩條路線的清晰度就等價了」來推論
   「兩條路線的認知負荷也等價」。**這條直接打到 AVWM 的適應式 SNR 程序的一個隱含假設。**

**限制**:
- **我只讀了摘要。** 合成器型號、效果量、SNR 值、統計細節全部未知,引用前必須回查全文。
- 刺激為句子層級,與 AVWM 的單音節作業結構不同。
- 摘要未報告合成語音與自然語音在瞳孔上的直接對比是否顯著。

## 可連結脈絡
- 另一份現代瞳孔測量 —— [[govender2018]]
- 1980 年代的原始發現 —— [[luce1983]]
- 噪音本身的記憶代價 —— [[rabbitt1968]]、[[guang2021]]、[[mccoy2005]]
- AVWM 的噪音路線 —— [[silbert2012]]
- 綜合回顧 —— [[synthetic-speech-cognitive-load]]

---
標籤note:[[literature-note]] [[speech-perception]] [[working-memory]] [[AVWM]]

## 回查線索
**我在哪些研究看過「清晰度等價不代表認知負荷等價」?** → 本篇。
這條是 AVWM 適應式 SNR 程序的隱含假設之反例,limitation 段應該引。
**認知負荷的主觀指標與生理指標分歧,我在哪裡看過?** → 本篇、[[govender2018]]。
