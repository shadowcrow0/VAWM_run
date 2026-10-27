---
tags: [literature-note, VOT, 辨識函數斜率, 內在雜訊, 刺激分布變異, 統計學習]
citekey: clayards2008
---

# Clayards et al. (2008) — ⭐⭐ 聽者在 VOT 軸上的內在雜訊 ≈ 10.7 ms

**這是把「token 變異有多大」換算成「相對於知覺變異有多大」的關鍵基準,
而且它同時證明了聽者會**跟著刺激分布的變異調整辨識函數斜率**。**

**DOI / URL** https://doi.org/10.1016/j.cognition.2008.04.004 | PMC2582186
**閱讀狀態** **全文已由 subagent 取得並親自逐項核對**(參數、β 值、腳註 2 的函數式;
並自行用該式重建 σ_N,與作者印出的值吻合到 2% 以內)。⚠️ 我本人未通讀。

```bibtex
@article{clayards2008perception,
  author  = {Clayards, Meghan and Tanenhaus, Michael K. and Aslin, Richard N. and
             Jacobs, Robert A.},
  title   = {Perception of speech reflects optimal use of probabilistic speech cues},
  journal = {Cognition},
  volume  = {108}, number = {3}, pages = {804--809}, year = {2008},
  doi     = {10.1016/j.cognition.2008.04.004}
}
```

## 研究問題
聽者會不會依照**刺激分布本身的變異量**調整自己的辨識行為?
若聽到的 /b/–/p/ 類別分布比較寬,辨識函數會不會變淺?

## 方法與族群
兩組受試者聽同一條 VOT 連續體,但**類別分布的寬度不同**:
- narrow 條件:類別 SD = **8 ms**
- wide 條件:類別 SD = **14 ms**
兩個類別的中心固定在 0 與 50 ms,邊界 25 ms。

⚠️ **書目更正**:先前流傳的「8 與 24 ms」是錯的,正確是 **8 與 14 ms**。

## 結果與限制

### 1. 聽者跟著刺激分布調整斜率(原文)
> "the wide condition had **shallower slopes (mean = 6.2, sd = 0.89)** than functions in the
> narrow condition (**mean = 3.5, sd = 0.76**)."

擬合的心理計量函數(腳註 2 原文):
> "f(x) = (1 − γ − λ)(1/(1 + e^((α−x)/β))) + γ where **α corresponds to the boundary
> (50% point), β to the slope.**"

### 2. ⭐⭐ 25–75% 過渡寬度(**subagent 的算術**,用 2·ln3·β)

| 輸入變異 | β | **25–75% 寬度** | 20–80% 寬度 |
|---|---|---|---|
| narrow(類別 SD 8 ms) | 3.5 ms | **7.7 ms** | 9.7 ms |
| wide(類別 SD 14 ms) | 6.2 ms | **13.6 ms** | 17.2 ms |

### 3. ⭐⭐ 聽者的內在雜訊 ≈ **10.7 ms**(VOT 軸上)

subagent 用作者的式 (3) 獨立重建,得到 **σ_N ≈ 10.5 與 10.7 ms**,
與作者印出的 10.7 / 10.8 吻合到 2% 以內。這同時確認了三件事:
(i) "(8 ms)" / "(14 ms)" 確實是 SD(儘管原文用了 "variance" 一詞);
(ii) 原文的 "σ_N²" 其實是 σ_N 的 ms 值;(iii) β 的單位是 ms。

**→ 這是本次查證中最有用的單一數字:
一個典型聽者在 VOT 這條軸上的知覺 SD ≈ 10.7 ms。**

### ⭐ 對 AVWM 的核心換算(**我的算術**)

把 [[chodroff2017]] 的語者內 VOT SD 除以 10.7 ms,得到「以知覺 SD 為單位的 token 變異 s」:

| | 語者內 SD | s = SD / 10.7 | 變異膨脹 √(1+s²) | **β 降至** |
|---|---|---|---|---|
| **/b/**(孤立語 2–8 ms,取中點 5) | 5 ms | 0.47 | 1.10× | **91%** |
| **/pʰ/**(孤立語 12–27 ms,取中點 19.5) | 19.5 ms | 1.82 | **2.08×** | **48%** |

**→ 用多個自然 /p/ token,聽覺維度的有效變異會**超過兩倍**,β 掉到一半以下。
而 /b/ 幾乎不受影響。這個 3–4 倍的**不對稱**正是最危險的情形
(見 [[token-variability-vs-perceptual-variance]] §4.3)。**

⚠️ **這個換算有三層假設**:(a) 10.7 ms 適用於 AVWM 的受試者與 SNR 條件;
(b) [[chodroff2017]] 的語者內 SD 是「重複唸同一音節」的變異(**它不是** ——
它涵蓋 10 個母音脈絡,是上界);(c) token 位移與知覺雜訊獨立且可加。
**三者都不確定,所以上表是量級推估,不是定量預測。**

### 4. ⚠️ 一個對本專案的間接警告

**本篇證明了聽者的辨識函數斜率**跟著輸入分布的變異走**。**
→ **若 AVWM 用多 token,受試者可能不只是「被 token 變異加了雜訊」,
而是會**主動調整**自己的辨識函數,把它變淺。**
這是一個**適應性的**改變,不是被動的雜訊疊加 —— 而 §4.1 的可加模型
**沒有**涵蓋這種情形。(我的推論。)

**限制**:
- 合成連續體,不是自然 token。
- 我未通讀全文。
- 25–75% 寬度與 β→ms 的換算是 subagent 的算術,不是作者報告的統計量。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- 理論推論文章 —— [[自然音vs合成音_理論推論]]
- 語者內 VOT SD 的來源 —— [[chodroff2017]]、[[chodroff2015]]
- 「語者內變異約為語者間兩倍」 —— [[kleinschmidt2019]]
- /b/–/p/ 邊界位置 —— [[winn2020]]
- 自然 vs 合成連續體的邊界變異 —— [[mcmurray2008]]
- 辨識函數斜率的部位比較 —— [[goldenberg2022]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**聽者在 VOT 軸上的知覺 SD 是多少?** → 約 **10.7 ms**(本篇,經獨立重建確認)。
**/b/–/p/ 辨識函數的 25–75% 寬度?** → **7.7–13.6 ms**,依輸入分布寬度而定(本篇)。
**聽者會跟著刺激分布調整斜率嗎?** → **會**(本篇)。這對多 token 設計是額外的問題。
