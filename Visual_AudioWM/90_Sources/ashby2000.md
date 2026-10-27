---
tags: [literature-note, GRT, 知覺變異來源, 決策雜訊, 可辨識性]
citekey: ashby2000
---

# Ashby (2000) — GRT 創始人自己把「stimulus noise」與「perceptual noise」並列

**DOI / URL** https://doi.org/10.1006/jmps.1999.1284(⚠️ **DOI 未經 Crossref 獨立核實**;
書目來自作者自存 PDF)| 作者自存 PDF
https://labs.psych.ucsb.edu/ashby/gregory/sites/labs.psych.ucsb.edu.ashby.gregory/files/pubs/ashby2000.pdf
**閱讀狀態** **全文 PDF 已由 subagent 取得並檢索**(非通讀)。引句逐字自 PDF。

```bibtex
@article{ashby2000stochastic,
  author  = {Ashby, F. Gregory},
  title   = {A stochastic version of general recognition theory},
  journal = {Journal of Mathematical Psychology},
  volume  = {44}, number = {2}, pages = {310--329}, year = {2000}
}
```
⚠️ **標題與 DOI 需回查**。subagent 取得的是卷期頁碼(44(2), 310–329)與全文 PDF;
標題我未獨立核實。**引用前務必核對。**

## 研究問題
把 GRT 從靜態模型擴充成隨機歷程版本(把 RT 納入),並檢查靜態 GRT 的參數在
速度—正確率權衡下還能不能解釋成純知覺量。

## 結果與限制

**本卡只取兩件事。**

### 1. ⭐ Ashby 自己把刺激雜訊寫進知覺變異的來源清單(原文)

> "Over trials, however, **stimulus and perceptual noise** are assumed to induce variability
> in the percept associated with every specific stimulus (e.g., Ashby & Lee, 1993;
> Green & Swets, 1966; Tanner, 1956; Tanner & Swets, 1954)."

> "**Because of stimulus and neural noise**, x*ᵢ* is assumed to be a random vector that
> varies across trials."

**→ 這回答了「GRT 把刺激變異當成模型內還是模型外」:是模型內,而且是明文的。
但兩者被**合併**成一個東西,沒有分離的機制。**

**這對 AVWM 的意義(我的推論)**:GRT 的知覺分布**在定義上**就吃下了刺激變異。
所以「β 是不是純知覺雜訊」這個問題,在 GRT 的框架裡**問法就錯了** ——
GRT 的 β 從來就不是純知覺雜訊,它是「刺激雜訊 + 知覺雜訊」的總和。
**能改變的不是「β 純不純」,而是「總和裡刺激那一項有多大、以及它是不是受控的」。**

### 2. 一個結構完全相同的警告(關於決策污染,不是刺激污染)

原文:
> "if a static GRT or signal detection model was fit to the data, **the noise variance
> estimates would be larger in the speed condition.** But does it really make sense to argue,
> for example, that the variability in the percept is affected by speed–accuracy
> instructions? **After all, the stimulus information is identical in the two conditions.**"

摘要:
> "These equivalence relations show that **traditional estimates of perceptual noise may often
> be corrupted by decisional influences.**"

**→ Ashby 已經寫過一次「估到的 perceptual noise 被非知覺來源污染」的論證,
只是他填進去的是**決策**,不是**刺激**。論證的形狀完全一樣。**
(⚠️ 把它換成刺激是我的類推,Ashby 沒有做這一步。)

**限制**:
- 標題與 DOI 未獨立核實(見上)。
- 未通讀全文,只有檢索到的段落。
- 本篇處理的是 RT 與速度—正確率權衡,主題不是刺激設計。

### ⚠️ 一個未取得、但最該取得的上游來源

**Ashby, F. G., & Lee, W. W. (1993). "Perceptual Variability as a Fundamental Axiom of
Perceptual Science." In S. C. Masin (Ed.), *Foundations of Perceptual Theory*
(Advances in Psychology), pp. 369–399. Elsevier. doi 10.1016/S0166-4115(08)62778-8,
ISBN 9780444894960.**

**這是 GRT 談「知覺變異的來源」的正典來源** —— Ashby (2000) 與
[[silbert-hawkins2016]] 都引它。ScienceDirect 有 captcha,無 OA 版本,**subagent 未取得**。
**若有 Elsevier 機構權限,這是本次查證中最該補的一筆。**

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- GRT 明說不模型化變異來源 —— [[silbert-hawkins2016]]
- 兩種雜訊不可分離、只有和可估 —— [[ashby-wenger-handbook]]
- item 聚合偏誤的形式結果 —— [[rouder2007]]
- 把 token 併掉的 GRT 語音實作 —— [[silbert2012]]

---
標籤note:[[literature-note]] [[GRT]] [[AVWM]]

## 回查線索
**GRT 把刺激變異當模型內還是模型外?** → 模型**內**,而且 Ashby 明文並列
"stimulus and perceptual noise"(本篇)。**但兩者合併,無分離機制。**
**有沒有人寫過「估到的 perceptual noise 被別的東西污染」?** → 有,本篇 —— 但填進去的是
**決策**污染,不是刺激污染。
