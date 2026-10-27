---
tags: [literature-note, 內部雜訊, 外部雜訊, 可重現噪音, 雙耳偵測]
citekey: siegel-colburn1989
---

# Siegel & Colburn (1989) — 內部與外部雜訊的變異**量級相當**

**DOI / URL** https://doi.org/10.1121/1.398472 | PMID 2600302
**閱讀狀態** ⚠️ **僅讀摘要**(PubMed + Crossref JATS)。AIP 全文 403,**未取得**;
**無法取得參數模型算出的具體內部/外部比值**。

```bibtex
@article{siegel1989binaural,
  author  = {Siegel, Ronald A. and Colburn, H. Steven},
  title   = {Binaural processing of noisy stimuli: Internal/external noise ratios for
             diotic and dichotic stimuli},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {86}, number = {6}, pages = {2122--2128}, year = {1989},
  doi     = {10.1121/1.398472}
}
```

## 研究問題
在噪音中偵測純音時,受試者反應的變異裡,有多少來自**噪音樣本**(外部),
有多少來自**觀察者自己**(內部)?

## 方法與族群
10 段數位化、統計上相似的高斯遮蔽噪音;純音偵測,diotic(NoSo)與 dichotic(NoSπ)。

## 結果與限制

**摘要原文**:
> "nonparametric analyses show that **response probabilities and sensitivities vary
> significantly across noise waveforms, indicating a considerable external noise component in
> subject response variability.** A parametric model is developed that maps individual
> stimulus waveforms onto a decision axis, facilitating evaluation of internal/external noise
> variance ratios. **For both NoSo and NoSπ, internal and external noise variance are of
> similar magnitude.**"

### 對 AVWM 的意義

**「外部噪音只是把分布對稱地撐開一點」這個直覺是錯的。**
外部(噪音樣本)變異與內部(觀察者)變異**量級相當** —— 不是可忽略的小項。

**→ 在 GRT 的語言裡:σ_total² = σ_內在² + σ_噪音樣本²,而兩項大約一樣大。
所以在噪音路線下,估到的「知覺變異」裡大約有一半根本不是知覺的。**
(這個換算是我做的;原文沒有講 GRT。)

⚠️ **這對 [[決策脈絡_統計方法]] §4 的稀釋分析是獨立的佐證**:
該節已經推導過 σ_tot² = σ_int² + σ_ext² 會稀釋交互作用,並算出稀釋倍數。
**本篇提供的是那個 f 值的實測量級參考:f ≈ 0.5。**

**跨領域的對照數字**(⚠️ 皆為 subagent 由摘要/二手取得,我未讀全文):
- [[neri2010]]:>400 筆估計,內部雜訊 ≈ **1.3 倍**外部雜訊 SD
- Burgess & Colborne (1988),視覺:σi/σ0 = **0.75 ± 0.1**
- Shackleton & Palmer (2006) 的綜述句:內部雜訊約為外部的
  "**between one and three times greater**"

**→ 收斂區間:內部 ≈ 0.75–3 倍外部,中位在 1–1.4 倍。兩者同一量級。**

**限制**:
- 僅讀摘要;參數模型算出的實際比值我沒有。
- 純音偵測、雙耳,**不是語音辨識**。
- 10 段噪音,不是無限多樣本。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]] §6
- 專案內結構相同的稀釋推導 —— [[決策脈絡_統計方法]] §4
- 可加分解公式 —— [[buss2006]]、[[ludosher1999]]
- 內部雜訊量級的大樣本估計 —— [[neri2010]]
- 噪音樣本在音素辨識上的效應 —— [[osses-varnet2024]]
- frozen vs running —— [[pfafflin1968]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**外部噪音佔總變異多少?** → 與內部**量級相當**(本篇);跨研究收斂在內部 ≈ 0.75–3 倍外部。
**這對 SNR 路線有什麼後果?** → 估到的「知覺變異」裡約有一半是噪音樣本的變異。
