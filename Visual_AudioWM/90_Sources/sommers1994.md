---
tags: [literature-note, 刺激變異, within-talker變異, 語音相關性, 刺激設計]
citekey: sommers1994
---

# Sommers, Nygaard & Pisoni (1994) — 只有「語音上相關」的維度變異才有代價

**DOI / URL** https://doi.org/10.1121/1.411453 | PMC3499952
**閱讀狀態** **全文已讀**(subagent 由 PMC 取得)。
⚠️ **正確率的百分比只出現在圖裡,正文沒有數字** —— 本卡只引 F 值,**不可引百分比**。

```bibtex
@article{sommers1994stimulus,
  author  = {Sommers, Mitchell S. and Nygaard, Lynne C. and Pisoni, David B.},
  title   = {Stimulus variability and spoken word recognition. {I}. Effects of variability in
             speaking rate and overall amplitude},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {96}, number = {3}, pages = {1314--1324}, year = {1994},
  doi     = {10.1121/1.411453}
}
```

## 研究問題
刺激變異的代價是「任何變異都要付」,還是「只有某些維度的變異要付」?

## 方法與族群
**兩個 within-talker 操弄 —— 這正是 AVWM 需要的層次。**

- **語速變異**:同一位語者以慢/中/快三種語速錄同一批詞。方法段原文:
  > "Seven subjects in each group heard 100 items produced at a **single rate** (fast,
  > medium, or slow) **by a male talker** and eight subjects heard the items produced by a
  > female talker."

  混合語速條件從**同一位語者**的不同語速錄音抽取。
- **整體振幅變異**:35 / 50 / 65 dB rms,逐試次變動。

## 結果與限制

| 變異來源 | 層次 | 結果 |
|---|---|---|
| 語者變異 | between-talker | F(1,36) = 164.46, p < 0.001 **有害** |
| **語速變異** | **within-talker** | **F(1,88) = 28.83, p < 0.005 有害** |
| 語速 + 語者 | 混合 | F(2,57) = 47.21, p < 0.001 有害 |
| **整體振幅變異** | **within-talker** | **F(1,58) = 0.036, p > 0.1 —— 無效果** |

原文:
> "**Trial-to-trial variations in overall amplitude did not produce significant decrements in
> identification performance.**"

詮釋(原文):
> "**Alterations in overall amplitude, in contrast, do not have direct effects on phonetic
> identification** and, as a result, the obligatory processing demands for this dimension may
> be either absent or considerably attenuated."

### ⭐ 對 AVWM 的核心含意(我的推論,原文沒有這樣說)

**變異的代價不是按「物理變異量」收費,而是按「這個維度對當前語音判斷是否相關」收費。**

- 語速會改變時間結構 → **與 VOT 判斷相關** → 有代價
- 整體振幅不改變任何音段線索 → **不相關** → 零代價

**→ 這給 AVWM 一個可操作的篩選原則:token 之間若只在「與 /b/–/p/ 判斷無關」的維度上
不同(整體音量、絕對 F0 水平),代價可能接近零;若在 VOT、F1 起始、burst 頻譜上不同,
代價就會直接進到聽覺維度的知覺變異裡。**

⚠️ 但這也意味著:**AVWM 現行的 `TARGET_RMS` 音量對齊**([[snr_audio]])
在這條證據下是**必要但不足**的 —— 它處理的正好是那個**沒有代價**的維度。

**限制**:
- 詞辨識,不是 CV 音節辨識,不是 GRT。
- 百分比只在圖裡,不可引用。
- 語速變異是**誘發**的(要求語者換速),不是自然抖動。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- 同一個「語音相關性」原則的後續 —— [[sommers-barcroft2006]]
- 跨語者的基準 —— [[mullennix1989]]
- within-talker token 數的直接操弄 —— [[uchanski1998]]、[[kapadia2023]]
- AVWM 的音量對齊實作 —— [[snr_audio]]、[[consonant-pair-choice]] §8.4

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**是不是任何刺激變異都有代價?** → 不是。本篇:語速(相關)有代價,整體振幅(不相關)沒有。
**AVWM 對齊音量夠不夠?** → 不夠 —— 對齊的正好是零代價的那個維度(本篇)。
