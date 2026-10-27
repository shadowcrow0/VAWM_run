---
tags: [literature-note, 刺激變異, 語者變異, 噪音中辨識, 刺激設計]
citekey: mullennix1989
---

# Mullennix, Pisoni & Martin (1989) — 跨語者變異代價的量化基準

**DOI / URL** https://doi.org/10.1121/1.397688 | PMC3515846
**閱讀狀態** **全文已讀**(subagent 由 PMC 取得;所有數值以兩次獨立抓取交叉核對,一致)。

```bibtex
@article{mullennix1989some,
  author  = {Mullennix, John W. and Pisoni, David B. and Martin, Christopher S.},
  title   = {Some effects of talker variability on spoken word recognition},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {85}, number = {1}, pages = {365--378}, year = {1989},
  doi     = {10.1121/1.397688}
}
```

## 研究問題
講話的人一直換,會不會讓詞辨識變差?若會,是知覺層次還是後期處理層次的代價?

## 方法與族群
四個實驗。**15 位語者、68 個 CVC 詞。**單語者 block vs 混語者 block。
作業包含噪音中辨識(實驗 1、4)與命名(naming,實驗 2、3)。

## 結果與限制

| 實驗 | 作業 | 單語者 | 混語者 | 統計 |
|---|---|---|---|---|
| 1 | 噪音中辨識 | 40.6% | 33.9% | F(1,20) = 7.9, p < 0.02 |
| 2 | 命名潛時 | 608.4 ms | 678.3 ms | F(1,11) = 10.7, p < 0.01 |
| 2 | 命名正確率 | 95.8% | 91.4% | F(1,11) = 7.4, p < 0.02 |
| 3 | 命名潛時 | 834.2 ms | 868.9 ms | F(1,19) = 11.1, p < 0.01 |
| 3 | 命名正確率 | 97.8% | 92.9% | F(1,19) = 38.3, p < 0.01 |
| 4 | 辨識(退化) | 69.1% | 48.1% | F(1,28) = 91.6, p < 0.01 |

實驗 1 依 S/N 分列(單/混):+10 dB 66.5/62.1;0 dB 45.0/35.3;−10 dB 6.6/3.5。

**→ 正確率代價 6.7 至 21 個百分點;RT 代價 35–70 ms(約 5–10%)。**

**⚠️ 對 AVWM 最相關的一列是實驗 1 的 0 dB**:45.0% vs 35.3%,**差 9.7 個百分點**。
AVWM 的適應程序把難度校到約 80% 聯合正確率,同樣是在噪音中辨識。
**若跨語者能造成 10 個百分點的差距,變異量的問題就不是可忽略的量級。**
(這個外推是我做的:AVWM 不換語者,只可能換 token,而 token 變異 < 語者變異。)

**限制**:
- 這是**跨語者**變異,不是 within-talker token 變異。對 AVWM 是**上界**參考,
  不是直接證據。直接證據見 [[kapadia2023]]、[[uchanski1998]]。
- 詞辨識,不是 CV 音節;不是 GRT。
- 沒有分解「知覺變異增加」與「注意力/期待成本」;那個分解要看 [[magnuson2007]]。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- within-talker 的直接證據 —— [[kapadia2023]]、[[uchanski1998]]
- 同實驗室的 within-talker 操弄(語速、振幅)—— [[sommers1994]]
- 「代價其實來自期待」的反例 —— [[magnuson2007]]
- 綜合回顧 —— [[luthra2023]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**刺激變異的代價有多大?(上界)** → 本篇:跨語者在噪音中辨識掉 6.7–21 個百分點。
**噪音中辨識對語者變異特別敏感嗎?** → 是,實驗 4(退化條件)差距最大(21 個百分點)。
