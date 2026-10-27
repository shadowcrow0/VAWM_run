---
tags: [literature-note, 遮蔽噪音, 工作記憶, 聆聽費力度, 複製研究, 效果量]
citekey: guang2021
---

# Guang, Lefkowitz, Dillman-Hasso, Brown & Strand (2021) — Rabbitt 效應複製成功,但 **d = 0.19**

**DOI / URL** https://doi.org/10.1080/25742442.2021.1896908 | OSF https://osf.io/qjbxw/
**閱讀狀態** ✅ **全文 PDF 已讀**(2026-08-12 下載並逐段閱讀,含方法、全部統計、討論、
作者自承的限制)。

```bibtex
@article{guang2021recall,
  author  = {Guang, Claire and Lefkowitz, Emmett and Dillman-Hasso, Naseem and
             Brown, Violet and Strand, Julia},
  title   = {Recall of speech is impaired by subsequent masking noise:
             A replication of {Rabbitt} (1968) {Experiment} 2},
  journal = {Auditory Perception \& Cognition}, year = {2021},
  doi     = {10.1080/25742442.2021.1896908}
}
```

## 研究問題
[[rabbitt1968]] 實驗 2 被引用近 500 次、是整個 listening effort 領域的理論基礎,
**但從未被直接複製過**。它站得住嗎?效果有多大?

作者原文:
> "despite being cited nearly 500 times and providing the foundation for a wealth of
> subsequent research on the topic, the original study has never been directly replicated."

## 方法與族群
- **200 名受試者**(預註冊樣本;共跑 290 人,依預註冊條件排除),Prolific 線上招募,
  25–69 歲,英語母語、自陳聽力正常。含 Huggins pitch 耳機檢測(六題全對才能繼續)。
- 刺激:數字 1–9(**去掉 seven 使其全為單音節**),女聲錄音,RMS 等化,415–630 ms。
- 噪音:**Praat 生成的 speech-shaped noise**(匹配刺激的長時平均頻譜),再依每個語音檔
  的振幅**調變**,以維持固定 SNR。
- **SNR = −3 dB**,選定方式(原文):
  > "we conducted a brief pilot study to determine the most difficult noise level that
  > would result in 99% speech intelligibility, which was equivalent to intelligibility
  > in the clear: −3 dB."

  ⚠️ **這一點對 AVWM 極其重要:−3 dB 在這裡是「不損害清晰度」的水準。**
  [[silbert2012]] 也用 −3 dB,但他的刺激是 [pa/ba/fa/va] 的混淆集,難度完全不同。
  **SNR 數值不可跨刺激集比較。**
- 設計:八個數字的清單,前半/後半各自 clear 或 noise → 四種組合 × 14 清單 = 56 試次。
  呈現後才提示回憶前半或後半(1 digit/s,中間 2 s 停頓)。
- 分析:重複量數 ANOVA(嚴格計分 + 部分計分)**與** 廣義線性混合效果模型(lme4)。

## 結果與限制

**主要結果 —— 複製成功(原文)**:
> "We replicated the key finding that listening to speech in noise impairs recall for
> items that came earlier in the list."

- ANOVA(嚴格計分):後半噪音損害前半回憶,**F(1, 199) = 22.4, p < 0.001**
- ANOVA(部分計分):**F(1, 199) = 15.41, p < 0.001**
- GLMM:**χ²(1) = 6.34, p = .01**;B = −.32, SE = .12, z = −2.64, p = .008

**效果量(這是本卡最該記住的數字)**:
> "the magnitude of the effect of noise in the second half of the list on recall of the
> first half of the list in our study was **identical to that in Rabbitt's original
> experiment (Cohen's d = 0.19 for both)**"

部分計分下更小:**d = 0.14**。

**平均值(Table 1,前半清單正確回憶數,滿分 7)**:

| C/C | C/N | N/C | N/N |
|---|---|---|---|
| 5.11 (1.84) | 4.75 (2.04) | 4.96 (1.98) | 4.59 (1.82) |

→ **噪音造成的絕對差距約 0.36 個清單(7 個中的 5%)。**

**新增分析:交互作用不存在。** 前半噪音 × 後半噪音的交互在三種分析下全部不顯著
(絕對計分 F(1,199) = 0.001, p = 0.97;部分計分 F(1,199) = 2.14, p = 0.15;
GLMM χ²(1) = 1.28, p = .26)。→ **噪音的記憶代價是加法性的,不隨已有負荷放大。**

**作者對小效果量的解釋(原文)**:
> "participants could complete the task relatively easily even in the most difficult
> condition—indeed, recall accuracy was 92.4% across all conditions. Therefore, even when
> both half-lists were presented in noise, participants may not have been near the limits
> of their cognitive capacity ... **Presenting the digits in more difficult levels of
> background noise or asking participants to recall more than four digits would likely
> increase the magnitude of the effect**"

### ⚠️ 這句自承對 AVWM 是一把雙面刃

- **好消息**:在**清晰度未受損**的 SNR 下,噪音的記憶代價只有 d ≈ 0.19。
- **壞消息**:AVWM 的適應式 SNR 會刻意把辨識率壓到**遠低於 99%**(才有 GRT 的訊息量,
  見 [[silbert2012]]),而且 AVWM 要記 **4 個跨通道複合項目**,比記 4 個數字重得多。
  **依作者自己的推理,AVWM 的條件正是他們預期效應會放大的那一組條件。**
  (這是我依作者原文所做的推論。)

**限制**:
- **作者自承**:機制未定 ——「the mechanisms underlying the effect remain unclear」;
  可能是複誦受阻,也可能是「subsequent noise interferes with sensory memory rather
  than rehearsal」。
- **作者自承**:線上施測、個別受試(原研究是實驗室團測)。但效果量與原研究完全相同。
- 作業為數字序列回憶,**不是**跨通道綁定作業。

## 可連結脈絡
- 被複製的原研究 —— [[rabbitt1968]]
- 同機制的聽損版本 —— [[mccoy2005]]
- 合成語音被類比為噪音 —— [[luce1983]]
- AVWM 用 −3 dB speech-shaped noise 的前例(但刺激集不同) —— [[silbert2012]]
- 噪音改變線索權重 —— [[winn2013]]
- 綜合回顧 —— [[synthetic-speech-cognitive-load]]

---
標籤note:[[literature-note]] [[speech-perception]] [[working-memory]] [[AVWM]]

## 回查線索
**「聆聽費力度會吃掉記憶資源」這個主張的效果量到底多大?** → 本篇:**d = 0.19**。
每次想引用 listening effort 文獻時都該先想起這個數字。
**我在哪些研究看過「SNR 數值不可跨刺激集比較」的具體證據?** → 本篇(−3 dB = 99% 清晰度,
數字閉集)vs [[silbert2012]](−3 dB,[pa/ba/fa/va] 混淆集)。
**哪些預註冊複製研究得到與原研究完全相同的效果量?** → 本篇。
