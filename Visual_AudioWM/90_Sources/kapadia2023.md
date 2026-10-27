---
tags: [literature-note, 刺激變異, token變異, 語者變異, 反應時間, 正確率, 刺激設計]
citekey: kapadia2023
---

# Kapadia, Tin & Perrachione (2023) — ⭐ 唯一把「同語者多 token」當因子的現代因子設計

**DOI / URL** https://doi.org/10.1121/10.0016611 | PMID 36732274 | PMC9836727
**閱讀狀態** **全文 PDF 已讀**(subagent 由作者實驗室網站取得;Table II–V 的數值逐格讀出)。

```bibtex
@article{kapadia2023multiple,
  author  = {Kapadia, Ayesha M. and Tin, Jessica A. A. and Perrachione, Tyler K.},
  title   = {Multiple sources of acoustic variation affect speech processing efficiency},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {153}, number = {1}, pages = {209--223}, year = {2023},
  doi     = {10.1121/10.0016611}
}
```

## 研究問題

語音變異的處理代價,文獻幾乎只研究**跨語者**變異。**同一位語者不同 token 之間**的變異
會不會也有代價?代價的大小跟跨語者比起來如何?

**作者自己指認這是一個文獻缺口(全文原文)**:
> "In this literature, '**high variability**' is almost always implemented using stimuli
> produced by multiple different talkers, as opposed to any other kind of variability, such
> as **multiple tokens from a single talker**, in different coarticulatory configurations, in
> different kinds of reverberant environments, or with different kinds or levels of
> background noise."

摘要:
> "within-talker phonetic variation is a less well-understood source of variability in
> speech, and it is unknown how processing costs from within-talker variation compare to
> those from between-talker variation."

**→ 到 2023 年,作者仍認為這個比較是開放問題。這對 AVWM 是重要的文獻狀態資訊。**

## 方法與族群

**2×2×2 因子設計,within-talker token 變異是明確的一個因子。**設計原文:
> "Within-talker variability was operationalized as **the number of distinct recordings of
> each target word produced by each talker in a condition, with two levels: low variability
> (one exemplar per word per talker) and high variability (eight exemplars per word per
> talker).**"

- 刺激:6 個 /bVt/ 詞(bit, bet, bat, but, boat, boot)
- 4 位語者;N = 24 聽者
- 作業:速度化詞辨識(speeded word identification)

## 結果與限制

### within-talker token 變異(多 exemplar vs **單一** exemplar)的 RT 代價(Table V)

| 情境 | ΔRT | 干擾量 | 統計 |
|---|---|---|---|
| **單一語者、單一對比**(C>A) | **39.7 ms** | 5.10% | t = 3.128, p < 0.005 * |
| 單一語者、多重對比(D>B) | 26.2 ms | 2.46% | t = 2.985, p < 0.006 * |
| 多語者、單一對比(G>E) | 7.3 ms | 0.89% | t = −1.464, p = 0.154 n.s. |
| 多語者、多重對比(H>F) | 34.5 ms | 3.22% | t = 4.197, p < 0.001 * |

**跨語者對照(同表)**:E>A = **48.3 ms**(6.21%),t = 3.816, p < 0.001 *;
其餘三個跨語者對比不顯著(16.0、6.8、15.1 ms)。

主效果:within-talker RT β = −0.006, s.e. = 0.001, df = 32.449, t = −4.564, p ≪ 0.001 *。

**結論句(原文)**:
> "Response times were also significantly slower when listening to **multiple vs one exemplar
> per talker in the absence of other sources of variability** (conditions C vs A), revealing
> that **within-talker phonetic variability alone has a significantly detrimental effect on
> speech processing.**"

### ⭐ 對 AVWM 最關鍵的一格:**正確率不受影響**

Table III:within-talker 變異 β = 0.021, s.e. = 0.070, z = 0.300, **p = 0.764(n.s.)**;
跨語者變異**有**影響正確率(β = 0.177, s.e. = 0.088, z = 2.007, p = 0.045 *)。

摘要原文:
> "**Between-talker variability affected both word-identification accuracy and response time,
> but within-talker variability affected only response time.**"

**→ 這對 AVWM 極重要:GRT 的依變項是混淆矩陣(正確率與錯誤去向),不是 RT。
本篇最直接的證據說 within-talker token 變異在正確率上沒抓到效果。**

⚠️ **但「沒抓到」不等於「沒有」。**24 人、詞辨識、無噪音、天花板附近的作業,
偵測小效果的檢力有限。而且 AVWM 刻意把難度壓到 80% 左右,那正是正確率對
變異最敏感的區段。**(這一段是我的推論,不是原文。)**

### ⚠️ 一個必須知道的設計但書

那 8 個 exemplar **不是天真重複錄音**。原文:語者對每個詞用
> "with combinations of (i) low, medium, and high pitch (within the speakers' natural pitch
> range) and (ii) shorter and longer durations, as well as with rising or falling intonation"
> — "eight variations (3 pitches × 2 durations + 2 contours)."

**→ 這是刻意誘發的韻律變異,是自然 token 抖動的上限,不是下限。**
作者在摘要裡仍稱之為 "natural… within-talker variability"。
**引用時必須註明這一點,否則會高估自然 token 變異的代價。**

### 一個 subagent 做的比例推算(⚠️ 原文沒有做這個比較)
最乾淨的那一格裡,within-talker 代價(39.7 ms)約為跨語者代價(48.3 ms)的 **82%**。
**→ 從一個固定 token 換成同語者的 8 個 token,RT 代價幾乎等同於換一位語者。**
(這個比值是推算,不是作者的主張。)

### ⚠️ 作者轉述的一個對 GRT 特別致命的警告(原文)
> "subsequent work has shown that the degree of within- vs between-talker variability in
> segmental and voice contrasts **can reverse the apparent direction of this processing
> dependency** (Cutler et al., 2011). This underscores a critical limitation of Garner-like
> paradigms (Garner, 1974) more generally: that **the direction of processing dependency
> effects depends specifically on the magnitude of variation chosen for each dimension**,
> rather than something inherent about the processing order between dimensions."

**→ 這是說給 Garner 典範聽的,但 GRT 同樣是一個「兩個維度互動」的框架。
若維度互動的方向取決於實驗者為每個維度選了多少變異量,那麼 AVWM 的
「顏色 × 聽覺」互動也可能是刺激變異量的產物,而非知覺事實。**
⚠️ **Cutler et al. (2011) 我未取得,這是 Kapadia 等人的轉述。**

**限制**:
- 依變項以 RT 為主;正確率的虛無結果檢力未知。
- 詞辨識,不是 CV 音節辨識;不是 GRT。
- 8 exemplar 是誘發變異,見上。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- 理論推論文章 —— [[自然音vs合成音_理論推論]]
- 直接把 token 數當自變項的老前輩 —— [[uchanski1998]]
- 點名這三篇 within-talker 研究的回顧 —— [[luthra2023]]
- 跨語者變異的經典基準 —— [[mullennix1989]]、[[sommers1994]]
- 「變異代價其實是期待造成的」這個混淆 —— [[magnuson2007]]
- 用每類 4 個 token 的 GRT 前例 —— [[silbert2012]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**同語者多 token 的代價有多大?** → 本篇:RT 約 40 ms(最乾淨的那格),
是換語者代價的 82%;**但正確率沒有效果**(p = 0.764)。
**維度互動的方向會不會被刺激變異量決定?** → 本篇轉述 Cutler et al. (2011) 說會,
而且會**反轉**。這是 Garner 典範的批評,但對 GRT 同樣適用。
