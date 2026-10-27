---
tags: [literature-note, 統計方法, 配對設計, item分析, 刺激當隨機效果]
citekey: raaijmakers1999
---

# Raaijmakers et al. (1999) — 配對或平衡之後,**不需要** item 分析(但到不了 n = 1)

**這是三個選項裡最有利於「刺激高度受控」路線的一篇,而且它的條件是明文寫出來的。**

**DOI / URL** https://doi.org/10.1006/jmla.1999.2650 | 作者自存 PDF
https://raaijmakers.edu.fmg.uva.nl/PDFs/
**閱讀狀態** **全文 PDF 已由 subagent 取得並閱讀**。⚠️ 我本人未通讀。

```bibtex
@article{raaijmakers1999how,
  author  = {Raaijmakers, Jeroen G. W. and Schrijnemakers, Joseph M. C. and Gremmen, Frans},
  title   = {How to deal with ``The language-as-fixed-effect fallacy'':
             Common misconceptions and alternative solutions},
  journal = {Journal of Memory and Language},
  volume  = {41}, number = {3}, pages = {416--426}, year = {1999},
  doi     = {10.1006/jmla.1999.2650}
}
```

## 研究問題
[[clark1973]] 之後,「一律要做 item 分析 / min F′」變成了慣例。**這個慣例對嗎?**

## 結果與限制

### ⭐ 主張(摘要原文)
> "**contrary to current practice, in many cases there is no need to perform separate subject
> and item analyses since the traditional F₁ is the correct test statistic. In particular this
> is the case when item variability is experimentally controlled by matching or by
> counterbalancing.**"

### 條件寫得很明白(pp. 425–426 原文)
> "In many cases the design does not require separate analyses over subjects and items, yet
> such analyses are routinely run, without taking into account that this procedure was
> originally introduced for a very specific design, namely **a design where the items are
> nested under the treatment variable**. If this is not in fact the case, e.g., **when the
> materials have been matched on a number of variables or when the lists are counterbalanced
> over different groups of subjects, there is no need to compute (min)F′** and the simple
> subject analysis (averaging over items) will be correct."

**→ AVWM 的設計正是「配對」型的**:/b/ 與 /p/ 是配對的,不是從各自的類別裡獨立抽樣的。
**所以本篇對 AVWM 有利。**

### ⚠️⚠️ 但兩個限定,而且都很重要

**(1) 配對只是**減少**偏誤,不是消除(p. 422 原文)**:
> "Hence the bias in F₁ is now a function of **σ²_AB, the interaction between blocks and
> treatments**, and this **will usually be smaller** than σ²_W(A), the variability of items
> within treatments that is responsible for the bias in the case where items are sampled
> randomly (i.e., not matched)."

**"usually be smaller",不是零。** 而 σ²_AB 正是「配對沒配好的那部分」——
對 AVWM 而言就是 [[自然音vs合成音_理論推論]] §5.2 講的
「你只能對齊你想到要量的東西」。

**(2) ⭐ 他們的推導需要一個「配對區塊的母體」,而不是一對(p. 421 原文)**:
他們分析的是理想情形,兩個 item 完美配對,而
> "**The various blocks are still assumed to be sampled randomly from a larger population of
> blocks**"

**subagent 的推論(明確標為推論,作者沒說)**:
若只有**一對**配對刺激,q = 1,σ²_AB **估不出來**,也沒有區塊母體可以推論。
**他們的結果授權的是「對一組配對樣本做 F₁」,不是「對單一配對做 F₁」。
他們從未討論 q = 1 的情形。**

**→ 所以本篇**不能**用來替「單一自然 token 對」或「單一合成刺激對」背書。
它替的是「多對配對刺激」背書 —— 那是一個本專案還沒有考慮過的第四個選項。**

### 一個 Clark 自己承認的例外(p. 423)
item 對**每位受試者**隨機取樣時,F₁ 是對的 ——
> "This case was briefly mentioned by Clark (1973, p. 348) as one where the traditional
> analysis (F₁) is correct."

**限制**:
- 記憶與詞彙作業;不是語音,不是心理物理。
- 我未通讀。
- q = 1 的推論是 subagent 的,不是作者的。

## 可連結脈絡
- 本卡所屬的推論文章 —— [[自然音vs合成音_理論推論]] §5.3
- 證據回顧 —— [[token-variability-vs-perceptual-variance]] §7.1
- 被它修正的原始論證 —— [[clark1973]]
- 與它方向相反的現代論證 —— [[judd2012]]、[[westfall2014]]、[[barr2013]]
- 更早、更強硬的心理物理批判 —— [[brunswik1955]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**配對設計還需要 item 分析嗎?** → **不需要**,F₁ 就是對的(本篇摘要)。
**這能不能替單一刺激對背書?** → **不能。** 他們的推導需要「配對區塊的母體」,
從未討論 q = 1。
**配對能消除偏誤嗎?** → **不能,只能減少**(p. 422:"usually be smaller")。
