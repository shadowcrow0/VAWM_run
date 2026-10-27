---
tags: [literature-note, 合成語音, 序列回憶, DECtalk, 老化, Pisoni]
citekey: humes1993
---

# Humes, Nelson, Pisoni & Lively (1993) — 換成 DECtalk 之後,合成劣勢只剩「slightly worse」

**DOI / URL** https://doi.org/10.1044/jshr.3603.634 | PMC3509355 https://pmc.ncbi.nlm.nih.gov/articles/PMC3509355/ | PMID 8331919
**閱讀狀態** ✅ **全文已讀**(PMC author manuscript,2026-08-12)。摘要、方法、
討論段皆逐字核對。統計表格數值我未逐格取用。

```bibtex
@article{humes1993effects,
  author  = {Humes, Larry E. and Nelson, Kathleen J. and Pisoni, David B. and
             Lively, Scott E.},
  title   = {Effects of age on serial recall of natural and synthetic speech},
  journal = {Journal of Speech and Hearing Research},
  volume  = {36}, number = {3}, pages = {634--639}, year = {1993},
  doi     = {10.1044/jshr.3603.634}
}
```

## 研究問題
表面上是「老化如何影響自然與合成語音的序列回憶」。**但對 AVWM 而言,本篇的價值在於它
是 [[luce1983]] 的十年後續,用的是更好的合成器(DECtalk 1.8 / DECPaul,而非 MITalk),
所以可以當作「合成器世代」這條軸上的第二個資料點。**

## 方法與族群
- 兩組:**年輕正常聽力(YNH)** 與 **年長正常聽力(ENH)**。
- 合成器:**DECtalk 1.8(DECPaul)**;自然語音由英語母語者錄製。
- 作業:**10 詞清單的序列回憶**(必須按呈現順序寫下),12 個清單 × 4 條件
  (2 速率 × 2 talker)。
- 三個受試者內變項:talker(自然/合成)、詞難度(易/難,以詞頻與音韻相似度定義)、
  速率(1 s / 2 s 詞間距)。
- 回憶後另做一次**清晰度測驗**(同 100 詞,逐詞聽寫)。

**方法學上的一個重要交代(原文)**:作者明說 talker 的主效果**不是本篇的興趣所在**,
自然/合成的納入是為了檢驗結論的可外推性:

> "the effects of talker per se were not of interest. Rather, we included natural and
> synthetic speech in this study to evaluate how readily conclusions drawn from the data
> with natural speech could be generalized to synthetic speech."

因此**本篇沒有對 talker 主效果做正式的統計檢驗**(四個 ANOVA 是分開跑的:
primacy/recency × natural/synthetic)。

## 結果與限制

**摘要逐字:**
> "Results indicated that age per se had little effect on short-term (working) memory as
> measured by the serial recall of monosyllabic words. Rate of presentation had little
> effect on recall for either subject group. Word difficulty, on the other hand, affected
> recall for both groups, with easy words being more readily recalled than hard words."

**對 AVWM 最關鍵的一句(討論段原文)**:

> "suggests that the recall of high-quality synthetic speech is **slightly worse** than
> that for natural speech. This is consistent with previous observations"

而且作者立刻自承**無法區分機制**:

> "Recall, however, that the intelligibility of the synthetic speech was significantly
> worse than that of natural speech for both subject groups. **It is unclear in this
> study, therefore, whether the poorer recall of synthetic speech is a consequence of the
> encoding of a degraded input (lower intelligibility) or deficient storage and retrieval
> of the synthetic speech.**"

**另一個有用的細節**:速率效應出現在**不同的曲線位置** —— 自然語音是 recency 段、
合成語音是 primacy 段。作者的解釋是速率操弄對兩種語音影響**不同的處理歷程**
(合成音的複誦被壓縮)。

### 這篇在「合成器世代」問題上說了什麼

| | [[luce1983]] | 本篇 |
|---|---|---|
| 合成器 | MITalk(1979 規則式 formant) | **DECtalk 1.8**(1980 年代末,品質高一級) |
| 作業 | 自由回憶 + preload + 序列回憶 | 序列回憶 |
| 合成劣勢 | 「large constant overall decrement」 | 「**slightly** worse」 |

**我的推論(非原文)**:兩篇的措辭差異暗示合成劣勢隨合成器品質下降,但**這是跨研究的
非正式比較,不是實驗操弄**,兩篇的作業、清單長度、族群都不同,不能當成效果量的證據。
本篇既未對 talker 主效果做正式檢驗,也未報告 talker 的效果量。

**限制**:
- **作者自承**:無法分辨低回憶是「編碼退化」還是「儲存/提取缺損」(見上引)。
- talker 主效果未正式檢驗,「slightly worse」是描述性判斷。
- 合成語音的清晰度在本研究中**確實顯著較差** —— 所以「高品質」是相對的。

## 可連結脈絡
- 十年前的原型研究 —— [[luce1983]]
- 「品質提升不等於負荷下降」的實驗檢驗 —— [[francis2009]]
- 現代合成器上的重測 —— [[govender2018]]、[[simantiraki2023]]
- 綜合回顧 —— [[synthetic-speech-cognitive-load]]

---
標籤note:[[literature-note]] [[speech-perception]] [[working-memory]] [[AVWM]]

## 回查線索
**我在哪些研究看過作者明說「這個主效果不是我要的,我放進來是為了檢驗可外推性」?** → 本篇。
這正是 AVWM 若加自然音對照 block 時可以引用的正當性論述。
**「清晰度退化 vs 儲存缺損」這個無法分辨的困境,我在哪些研究看過?** → 本篇、[[luce1983]]。
