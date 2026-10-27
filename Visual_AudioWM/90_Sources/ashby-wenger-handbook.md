---
tags: [literature-note, GRT, 訊號偵測論, 可辨識性, 雜訊分解, 手冊章節]
citekey: ashby-wenger-handbook
---

# Ashby & Wenger（手冊章節）— GRT 已經承認兩種雜訊分不開,只有「和」可估

**URL** 作者自存 PDF
https://labs.psych.ucsb.edu/ashby/gregory/sites/labs.psych.ucsb.edu.ashby.gregory/files/pubs/ashbywengerinpress.pdf
**閱讀狀態** **全文 PDF 已由 subagent 取得並閱讀**。
⚠️ **書目未定稿**:PDF 封面自署 "in press",卷冊最終出版資料**未經核實**。
引用時必須標明「章節草稿,出版資訊待確認」。

```bibtex
@incollection{ashby-wenger-sdt,
  author    = {Ashby, F. Gregory and Wenger, Michael J.},
  title     = {Statistical decision theory},
  booktitle = {The New Handbook of Mathematical Psychology, Volume 3},
  editor    = {Ashby, F. Gregory and Colonius, Hans and Dzhafarov, Ehtibar N.},
  publisher = {Cambridge University Press},
  note      = {in press（出版年與頁碼未核實）}
}
```

## 研究問題
手冊章節,系統整理統計決策理論(SDT / GRT)的形式結構。

## 結果與限制

**本卡只取兩段。**

### 1. ⭐ GRT 自己承認的不可辨識性 —— 這是本次論證最有力的槓桿(原文)

> "If the decision bound is linear, then it is straightforward to show that **perceptual and
> criterial noise are not separately identifiable** (Ashby & Maddox, 1993). Instead, **only
> the sum of the perceptual and criterial noise variances is estimable.** For this reason, it
> makes no difference whether we assume that the noise is perceptual or decisional (or some
> combination of the two)."

**→ GRT 已經**明文**接受:它估的是一個**和**,而不是某一個純粹的成分。而且框架的立場是
「反正分不開,所以假設是哪一種都無所謂」。**

**這對 AVWM 的意義(我的推論,原文沒有這一步)**:
刺激變異是**同一個和裡的第三項**。既然框架連知覺 vs 決策這兩項都不打算分,
**它在結構上也不會替你分出刺激那一項**。所以:

- ❌ 「用哪種刺激才能讓 β 變成純知覺雜訊」—— **這個目標在 GRT 裡達不到**,
  因為 β 從定義上就是一個和([[ashby2000]] 的 "stimulus and perceptual noise")。
- ✅ 可以達到的目標是:**讓和裡面「非知覺」的那幾項變小、或至少變成受控且可描述的。**
  這是一個量的問題,不是一個性質的問題。**這個改寫是本次回顧的核心轉折。**

### 2. GRT 教學傳統列出的難度操弄手段裡,沒有「多 token」(原文)

> "The most useful information in identification tasks is in the confusions that observers
> make, so experimental conditions are selected to guarantee errors. **This is usually
> accomplished by using highly similar stimuli, but sometimes brief exposure durations or
> noise masks are used instead.**"

對照 [[soto2017]] 列的三項(降低對比、縮短呈現時間、morphing)。
**兩份 GRT 教學來源列出的合法難度操弄手段,都不包含「增加刺激變異」。**
(⚠️ 這是「沒有提到」,不是「明文反對」。)

**限制**:
- 出版資訊未定稿。
- 手冊章節,無新資料。
- Ashby & Maddox (1993) 這個上游引用 subagent 未取得。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- 理論推論文章 —— [[自然音vs合成音_理論推論]]
- Ashby 並列 stimulus noise 與 perceptual noise —— [[ashby2000]]
- GRT 明說不模型化變異來源 —— [[silbert-hawkins2016]]
- 另一份列難度操弄手段的教學 —— [[soto2017]]
- item 聚合偏誤 —— [[rouder2007]]

---
標籤note:[[literature-note]] [[GRT]] [[AVWM]]

## 回查線索
**GRT 估到的變異數是「純」的嗎?** → 不是,而且框架**明文承認**:知覺雜訊與決策雜訊
不可分離,只有和可估(本篇)。
**這對「β 的純度」這個問題有什麼後果?** → 問題本身要改寫:不是「純不純」,
是「和裡面非知覺項有多大、受不受控」。
