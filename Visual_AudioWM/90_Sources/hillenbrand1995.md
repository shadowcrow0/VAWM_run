---
tags: [literature-note, 母音共振峰, 量測誤差, 語料庫, 產出數值]
citekey: hillenbrand1995
---

# Hillenbrand et al. (1995) — 共振峰量測的**雜訊底線**(而且它**不能**用來算語者內變異)

**DOI / URL** https://doi.org/10.1121/1.411872
**閱讀狀態** ⚠️ **未讀**;數值由 subagent 的 subagent 取得(兩層轉述),
中層 subagent 明確標為「未親自重讀」。**引用前須回原文核對。**

```bibtex
@article{hillenbrand1995acoustic,
  author  = {Hillenbrand, James and Getty, Laura A. and Clark, Michael J. and
             Wheeler, Kimberlee},
  title   = {Acoustic characteristics of {American English} vowels},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {97}, number = {5}, pages = {3099--3111}, year = {1995},
  doi     = {10.1121/1.411872}
}
```

## 研究問題
美式英語母音的聲學特徵(Peterson & Barney 1952 的現代重做)。

## 方法與族群
139 位語者 × 12 個母音 = **1668 個 token**。

## 結果與限制

**本卡有兩個用途,一個正面一個否定。**

### ❌ 否定用途:它**不能**算語者內變異

方法段原文(p. 3101):
> "**One token of each stimulus from each talker** was low-pass filtered at 7.2 kHz and
> digitized…"

**每位語者每個母音只有一個 token。N = 1668 = 139 × 12。
→ 結構上無法產生任何語者內 SD。**

⚠️ **這使得 [[kleinschmidt2019]] 那條「母音共振峰的語者內 ≈ 語者間的兩倍」的主張
失去支撐** —— 他引的是本篇,而本篇做不出那個分解。
(VOT 那一半的主張沒有問題,因為那是引 [[chodroff2015]] 的圖。)

### ✅ 正面用途:量測雜訊的底線

Table III,**重測的絕對差**:
**F1 11.7 Hz · F2 25.2 Hz · F3 28.7 Hz · F4 59.0 Hz**

> "The averaged absolute difference between the original and remeasured durations was
> **6.9 ms**"

f0 逐幀:"average absolute difference of **1.7 Hz**"

**→ 對照 [[heald-nusbaum2015]] 的語者內 SD(F1 24.6 Hz、F2 57.8 Hz):
表觀語者內共振峰變異裡,大約**一半是分析雜訊**。**
(這個比較是 subagent 做的;兩篇論文都沒有做這個對照。)

**⭐ 一個對 AVWM 的方法學提醒(我的推論)**:
若日後要「逐 token 聲學量測、把 token 變異當共變量校正」
([[token-variability-vs-perceptual-variance]] §10.1 的第 2 條路),
**量測誤差本身就有這個量級,校正的精度不會比它好。**
時長的重測誤差 6.9 ms **與 /b/–/p/ 邊界寬度(20–25 ms)同一量級**,尤其要注意。

**限制**:
- **未讀原文**,兩層轉述。
- 母音,不是塞音。
- 1995 年的共振峰追蹤技術;現代方法的誤差可能較小。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- 被本篇打掉支撐的那條主張 —— [[kleinschmidt2019]]
- 語者內共振峰 SD(要扣掉本篇的底線)—— [[heald-nusbaum2015]]
- /b/–/p/ 邊界寬度 —— [[winn2020]]、[[clayards2008]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**共振峰量測的雜訊底線?** → F1 11.7 Hz、F2 25.2 Hz、時長 6.9 ms(本篇 Table III)。
**這篇可以算語者內變異嗎?** → **不行**,每位語者每個母音只有一個 token。
引它做語者內/語者間分解是錯的。
