---
tags: [literature-note, double-pass, 內部雜訊, 反應一致性, 可重現噪音]
citekey: green1964
---

# Green (1964) — double-pass 的起源:重播同一段噪音來分離內部雜訊

**DOI / URL** https://doi.org/10.1037/h0044520 | PMID 14208857
**閱讀狀態** ⚠️ **原文未取得**。PubMed 與 Crossref 都沒有摘要;PsycNet 有 JS 牆。
下面的引句來自 **OpenAlex 的摘要索引**,而該索引的文字**可能源自同名的會議摘要**
而非 Psychological Review 正文。
**⚠️ 80% / 55% 這兩個數字在引用前必須對印刷版核對。**
double-pass 方法歸功於本篇這件事,由四份獨立的次級來源佐證。

```bibtex
@article{green1964consistency,
  author  = {Green, David M.},
  title   = {Consistency of auditory detection judgments},
  journal = {Psychological Review},
  volume  = {71}, number = {5}, pages = {392--407}, year = {1964},
  doi     = {10.1037/h0044520}
}
```

## 研究問題
偵測判斷的變異裡,有多少來自**外部**(哪一段波形被呈現),有多少來自**內部**
(神經系統當下的狀態)?

## 方法與族群
把 2AFC 試次序列的音訊**錄下來,稍後對同一位受試者重播一次**,
用兩次判斷的**一致率**當作內部雜訊的指標。

## 結果與限制

**⚠️ 以下引句出處存疑(見閱讀狀態)**:
> "**To achieve this end, the audio information presented during a sequence of
> two-alternative forced-choice trials was taped and repeated to the observer at a later
> time.** The consistency of the observer's judgments was measured by determining a percent
> agreement score… **Percent agreements range between 80% and 55%**, depending on the
> observer… **A simple linear model is used to establish a lower bound on the ratio of
> internal to external noise.**"

### ⭐ 對 AVWM 最重要的一點:double-pass 是**frozen** 方法,不是 running 方法

**方法的要求是**:
- **同一個 pass 之內**要有不同的噪音樣本(才有外部變異可以當參照)→ **running**
- **兩個 pass 之間**要重播**完全相同**的序列 → **frozen**

**→ 實務結論:必須把每一試次的噪音波形或 RNG 種子存下來。**
把 running noise 用過即丟,就**永遠失去**估計內部雜訊(以及做反向相關)的可能。

⚠️ 這個實作建議與 [[osses-varnet2024]] 的做法一致(他們把 4000 段噪音全存下來)。
**AVWM 的 `snr_audio.py` 目前是 `rng = np.random.default_rng()` 無種子,
用過即丟** —— 記錄種子的成本是零,但價值是保留一整條分析路線。(我的推論。)

**限制**:
- **原文未讀**,引句出處存疑。
- 純音偵測,不是語音。
- 1964 年,少數受試者。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]] §6
- 把噪音全存下來並做反向相關的現代版 —— [[osses-varnet2024]]
- 內部/外部雜訊比的實測 —— [[siegel-colburn1989]]、[[neri2010]]
- frozen vs rotating set 的直接比較 —— [[pfafflin1968]]
- AVWM 的噪音實作 —— [[snr_audio]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**怎麼把內部雜訊與外部雜訊分開?** → double-pass(重播同一序列),起源是本篇。
**它需要 running noise 還是 frozen noise?** → **兩個都要** —— pass 內 running、
pass 間 frozen。**所以必須存種子。**
