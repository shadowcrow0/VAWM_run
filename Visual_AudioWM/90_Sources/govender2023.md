---
tags: [literature-note, 合成語音, 認知負荷, 瞳孔測量, 神經TTS, 現代重測]
citekey: govender2023
---

# Govender & King (2018, 2023) — 用瞳孔測量重測:現代 TTS 追近了,但還沒追平

**DOI / URL** 2018: https://www.isca-archive.org/interspeech_2018/govender18_interspeech.pdf | 2023: https://ceur-ws.org/Vol-3644/IJCLR2023_paper_33_new.pdf
**閱讀狀態** **兩篇全文皆已讀**(subagent 取得 PDF 並抽取文字)。⚠️ 2018 的頁碼(2838–2842)取自 2023 那篇的參考書目,**非**直接來自 ISCA 頁面,屬二手。

```bibtex
@inproceedings{govender2018pupillometry,
  author    = {Govender, Avashna and King, Simon},
  title     = {Using pupillometry to measure the cognitive load of synthetic speech},
  booktitle = {Proc. Interspeech 2018}, pages = {2838--2842}, year = {2018}
}
@inproceedings{govender2023cognitive,
  author    = {Govender, Avashna and King, Simon},
  title     = {Cognitive load of modern {TTS} systems under noisy conditions},
  booktitle = {Proc. Workshop on Cognitive AI 2023 (co-located with IJCLR 2023)},
  series    = {CEUR Workshop Proceedings}, volume = {3644}, year = {2023}
}
```

## 研究問題
Pisoni 年代的認知負荷結論,是不是只適用於當年那些規則式合成器?**現代 TTS 的品質據稱與人聲難以分辨,認知負荷是否也追平了?**

## 方法與族群
瞳孔測量(pupillometry)作為認知負荷的生理指標。

- **2018**:Blizzard Challenge 2010 與 2011 的系統。⚠️ 摘要寫 "state-of-the-art",但實際上是 **HMM / unit-selection 時代,前神經網路**。材料為**語意不可預測句(SUS)**。
- **2023**:Tacotron 2、FastSpeech 2 等現代系統 + vocoded speech + 人聲。材料為**約 8 詞的句子**,噪音條件 **0 / −5 dB SNR**,依系統分區塊。

## 結果與限制
**2018 摘要原文**:
> "Our results show that pupil dilation is sensitive to the quality of synthetic speech.
> **In all cases, synthetic speech imposes a higher cognitive load than natural speech.**"

**2023 摘要原文(方向改變了)**:
> "**Results show that the gap of cognitive load demanded by TTS and human speech is
> reducing when listening to systems such as Tacotron 2 and Fastspeech 2. However,
> differences in cognitive load between these systems are still present.** ...
> Interestingly, results suggest that **vocoded speech demands the same cognitive load as
> human speech**..."

**2023 結論**:
> "**Modern TTS systems are therefore moving in the direction of being equivalent to human
> speech but not all systems will provide the same user experience.**"

---

## 對 AVWM 的意義
**好消息**:合成語音的認知負荷赤字**不是不可撼動的常數**,它隨合成品質縮小。1983 年的結論不能直接套到 2026 年的刺激上。

**壞消息 / 兩個必須標明的限制**:
1. **殘餘差異仍在**,即使是 Tacotron 2 / FastSpeech 2。
2. ⚠️ **AVWM 用的 Praat KlattGrid 不是神經 TTS,而是參數式共振峰合成 —— 它在譜系上更接近本研究裡「舊」的那一端,而不是新的那一端。** 因此「現代 TTS 已追近」這個結論**不能**直接用來替 KlattGrid 辯護。這是本卡最重要的一條保留。
3. 材料是 **8 詞句子在噪音中**,不是孤立 CV 音節。

**一個順帶但相關的發現**:vocoded speech(分析-重合成的自然語音)的認知負荷**等同人聲**。⚠️ **這是我認為對 AVWM 最有啟發的一條** —— 它暗示以**自然語音為基底**的處理(cross-splicing、STRAIGHT morphing、vocoding)可能不承擔合成語音的負荷代價,而純參數合成則可能承擔。**但這是我從單一結果做的外推,原文沒有做這個論證,vocoding 與 cross-splicing 也不是同一回事。**

**限制**:瞳孔測量是生理代理指標;2018 的「state-of-the-art」措辭與實際系統世代不符;2023 是 workshop 論文,非期刊同儕審查。

## 可連結脈絡
- 綜合建議 —— [[natural-vs-synthetic-speech]]
- 被重測的原始主張 —— [[luce1983]]、[[duffy1992]]
- 「提高品質不降低 WM 負荷」的反向證據 —— [[francis2009]]
- Klatt 家族合成器 —— [[klatt1980]]
- 自然語音基底的操弄法 —— [[winn2020]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**Pisoni 年代的合成語音負荷結論,現在還成立嗎?** → 本卡:方向仍在,量級縮小,但 KlattGrid 不在「已追近」的那一類。
**哪一條證據暗示「以自然語音為基底的重合成」不承擔負荷代價?** → 本卡的 vocoded speech 結果(我的外推,非原文論證)。
