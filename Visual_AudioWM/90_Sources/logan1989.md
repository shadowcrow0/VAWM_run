---
tags: [literature-note, 合成語音, 可辨識度, CV音節, Pisoni]
citekey: logan1989
---

# Logan, Greene & Pisoni (1989) — 合成 vs 自然的差距有多大,以及在哪裡最小

**DOI / URL** https://doi.org/10.1121/1.398236 | PMC3507386 https://pmc.ncbi.nlm.nih.gov/articles/PMC3507386/
**閱讀狀態** **全文已讀,Table II 直接取自 PMC 表格頁**(https://pmc.ncbi.nlm.nih.gov/articles/PMC3507386/table/T2/)。摘要為 Crossref 完整原文。表格數值與引句經 subagent 二次核對確認。

```bibtex
@article{logan1989segmental,
  author  = {Logan, John S. and Greene, Beth G. and Pisoni, David B.},
  title   = {Segmental intelligibility of synthetic speech produced by rule},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {86}, number = {2}, pages = {566--581}, year = {1989},
  doi     = {10.1121/1.398236}
}
```

## 研究問題
十套 text-to-speech 系統的**音段層次**可辨識度,跟自然語音差多少?用標準化的 Modified Rhyme Test (MRT) 量。

## 方法與族群
MRT(封閉式,六選一的單音節詞),十套 TTS 系統 + 自然語音對照。另用變體 MRT 測反應集大小對混淆的影響。受試者數我未確認。

## 結果與限制
**錯誤率(closed-format MRT,Table II,%,直接取自 PMC 表格頁)**:

| 系統 | **音節首** | 音節尾 | 整體 |
|---|---|---|---|
| **自然語音** | **0.50** | 0.56 | 0.53 |
| DECtalk 1.8 Paul | **1.56** | 4.94 | 3.25 |
| DECtalk 1.8 Betty | 3.39 | 7.89 | 5.72 |
| MITalk-79 | 4.61 | 9.39 | 7.00 |
| Prose 3.0 | 7.11 | 4.33 | 5.72 |
| Amiga | 13.89 | 10.61 | 12.25 |

⚠️ **注意音節首 / 音節尾的不對稱**:DECtalk-Paul 在音節**首**只差 1.56 vs 0.50%,在音節**尾**卻差 4.94 vs 0.56%。**一個 CV 音節整個落在有利的那一區。**

**統計檢定(內文原文)**:
> "**Comparisons of the error rates for consonants in initial position indicated no
> significant differences between natural speech and DECtalk 1.8 Paul**, DECtalk 1.8 Paul
> and Betty, ..."

**最關鍵的一句(摘要原文,Crossref 完整版)** —— 這一句直接回答「單一 CV 音節的差距有多大」:
> "The overall performance of the best system, DECtalk—Paul, **was equivalent to the data
> obtained with natural speech for consonants in syllable-initial position.**"

內文對應句(PMC 全文取回):
> "Only in comparing the error rates for initial consonants did any system display
> performance that was comparable to that obtained with natural speech."

**→ 在音節首子音這個最窄的層次上,最好的合成器與自然語音無異。合成語音的赤字是隨語言單位變長而增長的,不是在單一音段上就已經很大。**

**對 AVWM 直接相關**:AVWM 的聽覺刺激就是**單一 CV 音節的音節首塞音**,正是差距最小的那個位置。

**但有兩個必須標明的保留**:
1. DECtalk 是 **1989 年**的 Klatt 系共振峰合成器;AVWM 用的 Praat KlattGrid 屬同一家族,但**「DECtalk-Paul 等於自然」不能自動套到我自己手刻的 KlattGrid 參數上** —— DECtalk 的參數是多年調校的成果。這是**能力上限**的證據,不是**我的實作**的證據。
2. 摘要另一句直接針對本專案的顧慮:
   > "Recent work investigating the perception of synthetic speech under more severe
   > conditions in which greater demands are made on the listener's processing resources
   > is also considered. The wide range of intelligibility scores obtained in the present
   > study demonstrates important differences in perception and suggests that **not all
   > synthetic speech is perceptually equivalent to the listener.**"

**易錯音段(Table V/VI,經 WebFetch 取得,未核對)**:
> "The stops /k/, /g/, /b/, and /p/, the approximants /h/ and /w/, and the fricative /f/
> account for most of the errors across the different systems."

⚠️ **塞音正是最容易出錯的一類**,而且 **/k/ 與 /g/ 被列在最前面** —— 這與 [[consonant-pair-choice]] 的軟顎音顧慮方向一致。

**作者自承的限制(PMC 全文取回)**:
> "the MRT only provides information on segmental intelligibility of isolated monosyllabic
> words, limiting inferences regarding intelligibility of more complex words and words in
> sentences."
> "Substantial differences in performance can be anticipated with other populations of
> listeners or when synthetic speech...is presented in noise, under conditions of high
> cognitive load."

⚠️ 最後這句對 AVWM 是**直接警告**:MRT 是在安靜、低負荷下測的;AVWM 是**工作記憶作業**,而且若走 SNR 路線還要**加噪音**。作者明說在這兩個條件下差距會擴大。

**限制**:我未逐頁核對表格數字;引用具體數值前應回查 PDF。

## 可連結脈絡
- 綜合建議 —— [[natural-vs-synthetic-speech]]
- 合成語音的處理負荷(專門的回顧)—— [[synthetic-speech-cognitive-load]];個別卡見 [[luce1983]]、[[duffy1992]]、[[ralston1991]]
- 塞音發音部位的選擇 —— [[consonant-pair-choice]]
- Klatt 合成器家族 —— [[klatt1980]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**單一 CV 音節上,合成與自然的差距有多大?** → 本篇:最好的系統在音節首子音上**無差異**。這是 AVWM 選合成路線最強的一條支持證據。
**這條支持證據在什麼條件下失效?** → 噪音下、高認知負荷下(作者自承)。AVWM 兩者都佔。
