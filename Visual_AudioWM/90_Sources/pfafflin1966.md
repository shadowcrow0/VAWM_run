---
tags: [literature-note, 可重現噪音, 遮蔽噪音, 噪音樣本效應]
citekey: pfafflin1966
---

# Pfafflin & Mathews (1966) — 個別噪音樣本會造成**偏差**,而且不只是能量差異

**DOI / URL** https://doi.org/10.1121/1.1909895 | PMID 5907165
**閱讀狀態** ⚠️ **僅讀摘要**(Crossref JATS + OpenAlex)。AIP 全文 403,**未取得**;無數值。

```bibtex
@article{pfafflin1966detection,
  author  = {Pfafflin, Sheila M. and Mathews, Max V.},
  title   = {Detection of auditory signals in reproducible noise},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {39}, number = {2}, pages = {340--345}, year = {1966},
  doi     = {10.1121/1.1909895}
}
```

## 研究問題
用**可重現**(reproducible)的噪音樣本做偵測時,不同的噪音樣本之間表現會不會不同?
若會,能不能用「訊號頻率附近的能量差異」解釋?

## 方法與族群
12 段可重現噪音;two-interval forced-choice 偵測。

## 結果與限制

**摘要原文**:
> "Twelve reproducible noises were used as stimuli in a two-interval forced-choice
> signal-detection experiment. … On nonsignal trials, **biases to particular noises were
> found** that could be explained in part, but not entirely, by differences between the noise
> pairs in energy around the signal frequency. Performance on signal trials was related to the
> energy difference between the stimuli in the region near the signal frequency, but was
> **not entirely accounted for by this variable.**"

### 對 AVWM 的意義

**兩個重點**:
1. **個別噪音樣本會造成系統性的**偏差**(bias),不只是變異。**
   在 GRT 的語彙裡,偏差落在**決策界線**上,不是變異數上。
   ⚠️ 這與 [[token-variability-vs-perceptual-variance]] §4.3 模擬出的
   「不對稱 token 變異 → 決策界線位移」是同一類問題。
2. **用簡單的能量指標解釋不完** —— 所以「只要對齊 RMS/SNR 就控制住了」不成立。
   (這個推論是我的。)

**限制**:
- 僅讀摘要;無數值。
- 純音偵測,不是語音辨識。
- 1966 年,12 段噪音,受試者數未知。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]] §6
- 同作者兩年後的 frozen vs rotating 直接比較 —— [[pfafflin1968]]
- 現代、語音作業上的噪音 token 效應 —— [[osses-varnet2024]]
- 內部/外部雜訊比 —— [[siegel-colburn1989]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**個別噪音樣本會造成什麼?** → **偏差**(bias),而且**能量差異解釋不完**(本篇)。
