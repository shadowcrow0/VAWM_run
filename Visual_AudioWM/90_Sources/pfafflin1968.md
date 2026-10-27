---
tags: [literature-note, frozen噪音, running噪音, 可重現噪音, 遮蔽噪音, 記憶]
citekey: pfafflin1968
---

# Pfafflin (1968) — frozen 噪音**比較好偵測**,而且不是「不確定性」造成的

**DOI / URL** https://doi.org/10.1121/1.1910856 | PMID 5640955
**閱讀狀態** ⚠️ **僅讀摘要**(Crossref JATS 的完整原文摘要)。
AIP 全文頁面回 403,**全文未取得**;無 d′ 數值。
⚠️ 標題中的 "signal" 是**單數**(原刊如此)。

```bibtex
@article{pfafflin1968detection,
  author  = {Pfafflin, Sheila M.},
  title   = {Detection of auditory signal in restricted sets of reproducible noise},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {43}, number = {3}, pages = {487--490}, year = {1968},
  doi     = {10.1121/1.1910856}
}
```

## 研究問題
遮蔽噪音**每次都一樣**(frozen)與**在一組之間輪換**,對偵測表現有沒有差別?
若有,是「刺激不確定性」造成的,還是「對噪音的記憶」造成的?

## 方法與族群
可重現噪音中的聽覺訊號偵測。兩種條件:
(1) 整個 288 試次的 block 用**同一段噪音**;
(2) **12 段噪音**在 block 內隨機但等頻出現。
另有一個控制操弄:改變 block 內**訊號位準**的種類數。

## 結果與限制

**摘要原文(逐字)**:
> "The detectability of auditory signals in reproducible random noise was studied under two
> conditions: a single noise used throughout a block of 288 trials, and 12 noises occurring
> at random, but with equal frequency, throughout a block of trials. … **Signal detectability
> was found to be significantly better when a single noise was present in a block of
> trials.** Introducing variability in the stimulus by **altering the number of different
> signal levels presented during a block of trials did not affect detection.** The results
> support the importance of **memory for the noise from trial to trial** in the detection
> process."

### 三個對 AVWM 直接有用的點

1. **frozen 噪音顯著比 12 段輪換好。**
   → **running noise 不是免費的。**它確實會降低表現,亦即**確實增加了有效變異**。
   這與 AVWM 現行實作(`snr_audio.py` 的 `speech_shaped_noise()` 每次呼叫新樣本)
   的假設「換噪音樣本只是避免受試者學會圖樣」不完全一致 ——
   **代價是真的存在,而且被量到過。**
2. **⭐ 控制條件排除了「一般的刺激不確定性」解釋。**
   roving **訊號位準**(另一種刺激不確定性)**沒有**影響偵測。
   → 效果特定於**噪音波形的記憶**,不是泛泛的不確定性。
3. **這解釋了為什麼 running noise 仍然是對的選擇**(我的推論):
   frozen 的優勢**來自學習**。在一個跑數百試次的適應程序裡,
   受試者會持續學習那一段噪音,**閾值會隨時間漂移** ——
   對適應程序而言,可學習的優勢是有害的,因為它讓目標移動。

**限制**:
- 僅讀摘要,沒有效果量。
- 純音偵測,**不是語音辨識**。外推到語音要小心。
- 1968 年,受試者數與設備未知。
- **12 段輪換 ≠ 每試次全新樣本。**AVWM 用的是後者(近乎無限多樣本),
  它的效果**應該**比 12 段輪換更大或相當,但**沒有人測過那個極限**。(我的推論。)

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]] §6
- 同一系列、先一步的研究 —— [[pfafflin1966]](⚠️ 未建卡,書目見敘事回顧)
- 噪音樣本在音素辨識上的 token 效應 —— [[osses-varnet2024]]
- 內部/外部雜訊比 —— [[siegel-colburn1989]]
- double-pass 的起源 —— [[green1964]]
- AVWM 的 running noise 實作與其註解 —— [[snr_audio]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**frozen 噪音與 running 噪音哪個好偵測?** → **frozen**,顯著較好(本篇)。
**那是不是「刺激不確定性」造成的?** → **不是。** roving 訊號位準沒有效果;
作者歸因於**對噪音的記憶**。
