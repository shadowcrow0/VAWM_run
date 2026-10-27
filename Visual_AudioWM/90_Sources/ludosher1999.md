---
tags: [literature-note, 外部雜訊, 內部雜訊, PTM, 變異可加分解, 心理物理]
citekey: ludosher1999
---

# Lu & Dosher (1999) — 「d′ = 訊號 / √(外部變異 + 內部變異)」的正式來源

**DOI / URL** https://doi.org/10.1364/JOSAA.16.000764
**閱讀狀態** **全文已由 subagent 取得並讀出公式**。⚠️ 我本人未通讀。

```bibtex
@article{ludosher1999characterizing,
  author  = {Lu, Zhong-Lin and Dosher, Barbara Anne},
  title   = {Characterizing human perceptual inefficiencies with equivalent internal noise},
  journal = {Journal of the Optical Society of America A},
  volume  = {16}, number = {3}, pages = {764--778}, year = {1999},
  doi     = {10.1364/JOSAA.16.000764}
}
```

## 研究問題
怎麼用「加外部噪音」的手段,把觀察者的表現分解成「模板效率」與「等效內在雜訊」兩個成分?

## 方法與族群
視覺對比偵測 + 外加高斯噪音;perceptual template model(PTM)的建立。

## 結果與限制

**⭐ 正式陳述(原文)**:
> "For a given input consisting of a signal stimulus with rms contrast *c* plus an
> **experimenter-controlled** random noise stimulus whose pixels are drawn from a Gaussian
> distribution with standard deviation *N*ext, the total amount of signal at the decision
> stage is
> **S = βc,   (1)**
> and the total variance of noise at the decision stage is **the summation of the variance of
> the external and the internal noise**:
> **N² = N²ext + N²add.   (2)**
> Thus signal discriminability, *d′*, determined by the signal-to-noise ratio at the decision
> stage is given by
> **d′ = S/N = βc / √(N²ext + N²add).   (3)**"

### 對 AVWM 的兩個用途

1. **這是「總變異可加」的權威、精確、可引用的形式陳述。**
   聽覺領域的等價陳述見 [[buss2006]] Eq. (1)(語音論文應優先引那一篇)。
2. **⭐ 注意 "experimenter-controlled" 這個修飾語。**
   PTM 的整套推導**預設外部噪音的分布是實驗者指定的、已知的**。
   **這正是 running noise 相對於自然 token 變異在形式上唯一站得住的優勢** ——
   不是「比較小」,而是「**N_ext 是一個你寫下來的數,不是一個你不知道的數**」。
   (這個對比是我做的;原文沒有討論刺激 token 變異。)

**限制**:
- **視覺**,不是聽覺,不是語音。
- 公式 (2) 假設兩個雜訊源獨立且高斯。
- 我未通讀全文。
- ⚠️ **相關但未取得**:Lu & Dosher (2008) *Psychological Review* 115(1), 44–82,
  doi 10.1037/0033-295X.115.1.44 —— 全文封閉(Unpaywall `is_oa: false`),
  subagent 只取得摘要。**完整標題含副標**:"Characterizing observers using external noise
  and observer models: Assessing internal representations with external noise"。
  **本卡的公式全部來自 1999/2001 版,不是 2008 版。**

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]] §6
- 聽覺領域的同一公式(語音論文優先引這篇)—— [[buss2006]]
- 外部雜訊佔比的實測 —— [[siegel-colburn1989]]、[[neri2010]]
- ⚠️ 外加噪音可能改變處理策略,使 PTM 的前提失效 —— [[allard2014]]
- 噪音樣本本身的 token 效應 —— [[osses-varnet2024]]
- 專案內結構相同的稀釋推導 —— [[決策脈絡_統計方法]] §4

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**「總變異 = 外部 + 內部」的正式來源?** → 本篇 Eq. (2)(視覺);聽覺版見 [[buss2006]]。
**外加噪音的形式優勢是什麼?** → 原文用 "**experimenter-controlled**" 這個字 ——
它的分布是已知且指定的,自然 token 的不是。
