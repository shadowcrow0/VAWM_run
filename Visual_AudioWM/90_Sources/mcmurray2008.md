---
tags: [literature-note, VOT, 自然vs合成, 範疇知覺, 外推性, 眼動]
citekey: mcmurray2008
---

# McMurray et al. (2008) — 自然語音 VOT 連續體複製了合成音的漸進效果

**DOI / URL** https://doi.org/10.1037/a0011747 | PMC3011988 https://pmc.ncbi.nlm.nih.gov/articles/PMC3011988/ | PMID 19045996
**閱讀狀態** ⚠️ **未通讀全文**。摘要為 PMC 全文取回的完整原文;方法段與導論引句由 WebFetch **針對性檢索**取得,我未逐頁核對上下文。書目經 Crossref 核實。

```bibtex
@article{mcmurray2008gradient,
  author  = {McMurray, Bob and Aslin, Richard N. and Tanenhaus, Michael K. and
             Spivey, Michael J. and Subik, Dana},
  title   = {Gradient sensitivity to within-category variation in words and syllables},
  journal = {Journal of Experimental Psychology: Human Perception and Performance},
  volume  = {34}, number = {6}, pages = {1609--1631}, year = {2008},
  doi     = {10.1037/a0011747}
}
```

## 研究問題
表面問題是:類別內的次音位 VOT 變異會不會漸進地影響詞彙觸接?

**但對 AVWM 而言,真正的問題是實驗 1 的存在理由** —— 先前用**合成**語音得到的漸進效果(McMurray, Tanenhaus & Aslin, 2002, *Cognition*),換成**自然**語音做的連續體還在不在?這是本專案要的那種直接證據:同一個效果、同一個實驗室、兩種刺激來源。

## 方法與族群
五個實驗,眼動追蹤 + 音素/詞彙辨識作業。

**實驗 1 用自然語音連續體**,做法是 cross-splicing(方法段原文):
> "For each continuum step, a portion of the b-initial tokens (progressively larger
> portions in approximately 5 ms increments) was removed and replaced with corresponding
> material from the onset of the p-initial tokens (the burst and aspiration portions)."

端點選擇:有聲端 VOT 盡量接近 0 ms、無聲端 VOT > 40 ms,單一男性美語者。
**實驗 2–5 改用合成連續體**,以便系統操弄反應選項數(2 vs 4)、作業型態(詞彙 vs 音素判斷)、token 型態(詞 vs CV)。

## 結果與限制
**核心結果(摘要原文)**:
> "Experiment 1 demonstrated gradient effects along VOT continua made from natural
> speech, replicating results with synthetic speech (McMurray, Tanenhaus & Aslin,
> *Cognition*, 2002). ... A gradient effect of VOT in at least one half of the continuum
> was observed in all conditions."

**→ 效果本身跨刺激來源複製成功。這是 AVWM 最想要的那個結論。**

**但作者明說了為什麼需要做這個檢查**(導論原文):
> "A number of studies have suggested that some of the effects documented with single-cue
> variation, as studied in the laboratory with synthetic speech, may not generalize to
> natural speech stimuli, which have a richer set of correlated cues."

引 Shinn, Blumstein & Jongman (1985)、Miller & Wayland (1993)、Burton & Blumstein (1995)。

**以及一句方向明確的預期**(導論原文):
> "Most importantly for the present work, processing may be more categorical with natural
> speech than with synthesized speech."

引 Schouten & van Hessen (1992)。⚠️ **這個引用需注意** —— 見 [[schouten1992]],該篇只用自然刺激,並未在同一研究內比較自然 vs 合成。方向性的直接證據其實在 [[vanhessen1999]]。

**一個量化差異(對適應式程序有直接後果)**:
> "the variability in category boundaries for these items, both between participants and
> across items, was larger with natural speech continua than with synthetic speech
> continua."

同時報告 item 間的邊界變異大於受試者間變異(SD_item = 3.44,SD_participant = 2.20)。

**限制**:
- 我未通讀全文;引句需回查。
- 作者**沒有**在同一實驗內對同一批受試者做自然 vs 合成的正面對照;實驗 1 與 2002 年那篇是**跨研究**比較,受試者、年份、設備都不同。這是準複製,不是對照實驗。
- 沒有直接比較辨識函數**斜率**的句子(我特別找過,未找到)。
- 這是眼動 + 詞彙觸接典範,不是 GRT,也不是辨別作業。

## 可連結脈絡
- 綜合建議 —— [[natural-vs-synthetic-speech]]
- 「更自然 = 更範疇」的方向性證據 —— [[vanhessen1999]]、[[schouten1992]]
- 合成音單線索效果外推失敗的原始案例 —— [[shinn1985]]、[[burton-blumstein-naturalness]]
- 同作者對範疇知覺的立場 —— [[mcmurray2022]]
- cross-splicing 的方法學正解 —— [[winn2020]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**我在哪些研究看過「同一效果用自然與合成刺激各做一次」?** → 本篇(實驗 1 vs McMurray et al. 2002)。這是本專案目前找到最接近直接對照的一筆。
**自然刺激會讓什麼變大?** → 類別邊界的個體間與 item 間變異(本篇)。這對適應式程序的起始猜測與收斂速度有直接影響。
