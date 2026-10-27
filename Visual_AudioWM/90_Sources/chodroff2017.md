---
tags: [literature-note, VOT, 發音部位, 產出數值, 語料庫, 說話者變異]
citekey: chodroff2017
---

# Chodroff & Wilson (2017) — 現代大語料庫的英語 VOT 數值(取代 1964 的轉引)

**DOI / URL** https://doi.org/10.1016/j.wocn.2017.01.001 | 作者自存 PDF https://colincwilson.github.io/papers/ChodroffWilsonCovariationVOT2017.pdf
**閱讀狀態** **全文已讀**(subagent 取得作者自存 PDF;表格數值逐格核對)。

```bibtex
@article{chodroff2017structure,
  author  = {Chodroff, Eleanor and Wilson, Colin},
  title   = {Structure in talker-specific phonetic realization:
             Covariation of stop consonant {VOT} in {American English}},
  journal = {Journal of Phonetics},
  volume  = {61}, pages = {30--47}, year = {2017},
  doi     = {10.1016/j.wocn.2017.01.001}
}
```

## 研究問題
說話者之間的 VOT 差異是隨機的,還是有結構?同一位說話者在不同發音部位上的 VOT 是不是綁在一起變動?

## 方法與族群
兩個語料庫:**孤立語**(isolated speech)與**連續語**(connected speech),多位美式英語者。逐一報告每個塞音的平均、標準差、以及 talker 平均值的全距。

## 結果與限制
**Table 1(孤立語)與 Table 6(連續語)的平均 VOT(ms)**:

| | pʰ | tʰ | kʰ | b | d | g |
|---|---|---|---|---|---|---|
| 孤立語 平均 | 89 | 98 | 99 | 13 | 21 | **28** |
| 孤立語 SD(talker 平均) | 27 | 28 | 24 | 5 | 7 | **10** |
| 連續語 平均 | 51 | 61 | 56 | 8 | 14 | **17** |

**由上述已發表平均值計算的有聲–無聲間距(⚠️ 這是我的算術,不是原作者的主張)**:

| | 唇音 | 舌尖音 | 軟顎音 |
|---|---|---|---|
| 孤立語 | 76 | 77 | **71** |
| 連續語 | 43 | 47 | **39** |

**→ 軟顎音的可用區間最窄**(因為 /g/ 的 short-lag VOT 最長),而且**有聲端的說話者間變異隨部位後移而增大**(b 5 → d 7 → g 10)。

---

## ⭐ 追加(2026-08-12):本卡原本漏掉了**同一位語者之內**的變異數字

**這一欄才是 [[token-variability-vs-perceptual-variance]] 需要的那一欄,原卡只抄了
「talker 平均值的 SD」(語者**之間**),漏了「Range of Talker SDs」(語者**之內**)。**

Table 1(孤立語,24 位語者)與 Table 6(連續語,Mixer 6,180 位語者)的
**"Range of Talker SDs" 欄** —— 亦即**每位語者自己的 VOT 標準差的全距**(ms):

| | pʰ | tʰ | kʰ | b | d | g |
|---|---|---|---|---|---|---|
| **孤立語:語者內 SD 全距** | **12–27** | 10–26 | 11–20 | **2–8** | 3–10 | 4–13 |
| **連續語:語者內 SD 全距** | **11–35** | 9–34 | 11–30 | **2–8** | 4–13 | 6–15 |

表題原文:
> "Descriptive statistics of talker-specific VOT (ms)… Ranges are reported for
> talker-specific means and standard deviations."

**→ ⭐ 唇音的語者內 SD:/pʰ/ 12–27 ms、/b/ 2–8 ms。兩者相差 3–4 倍。**
這個**不對稱**正是 [[token-variability-vs-perceptual-variance]] §4.3 模擬的那個情形。

**⚠️ 一個必須標明的限定**:這個 SD **不是「同一個音節重複唸」的變異** ——
它涵蓋 10 個母音脈絡 × 5 個 block(孤立語)。
**所以它是純 token 重複雜訊的上界,不是它本身。**
subagent 查證的結論:**沒有任何已發表研究報告「同一位語者重複唸同一個 CV 音節」的
VOT SD。** Theodore et al. (2009) 用了純重複(/ti/、/pi/、/ki/),但只報告
每位語者的迴歸斜率與截距,**沒有報 SD**(全文已確認)。

**平均值(唯一一筆已發表的「平均語者內 SD」)** —— Chodroff, Bradshaw & Livesay (2023)
用同一批孤立語原始資料重算:**[tʰ] mean talker SD = 16 ms、[kʰ] = 16 ms**。
> "In contrast, adult stop-specific standard deviations are typically **between 10 and 30 ms**
> for word-initial aspirated stops in isolated speech (Chodroff & Wilson, 2017)."

**平均與標準差高度相關(原文)**:
> "Significant correlations of the talker means and standard deviations were observed for
> **all stops (r = 0.90)**, as well as for voiced stops ([b]: r=0.71, [d]: r=0.76,
> [g]: r=0.75, ps < 0.008)"

⚠️ **但「VOT 的變異係數 CV 是常數」這個常見說法,subagent 遍尋不獲任何來源。**
用上表中點 ÷ 平均算出的 CV(**我的算術**)顯示 CV **不是**跨類別常數:
孤立語 pʰ 0.22、b 0.38(有聲端約為無聲端的兩倍)。**CV 大致只在同一個 voicing 類別內穩定。**

### ⚠️ 一個資料品質警訊(subagent 發現,原文未標示)

**孤立語的 [b] 那一列在數學上不可能**:平均 13、SD 5、talker 平均值全距 11–20。
n = 24 且全部落在 [11, 20] 之內時,樣本 SD 的**最大可能值是 4.60**(subagent 的計算)。

而且 Chodroff, Bradshaw & Livesay (2023) 用**同一批原始資料**重算,得到
**[tʰ] SD = 23、[kʰ] = 18**,而本篇印的是 **28 與 24**;[pʰ] 的 talker 平均全距
他們列 **56–139**,本篇印 **46–139**。

**→ 孤立語的「SD」欄(語者**之間**)引用時要謹慎。
語者**之內**那一欄不受這個問題影響。**

**修正教科書的部位序列(原文)**:
> "Regarding the relative ranking of [tʰ], the findings are inconsistent ... The present
> study observed a strong tendency for the ranking of **[pʰ]<[kʰ]**, consistent with
> previous findings, and **little difference between the means of [tʰ] and [kʰ]** within or
> across talkers in both studies. **Among the voiced stops, the overwhelming majority of
> speakers had increasing VOT with more posterior places of articulation ([b]<[d]<[g]).**"

**→ 無聲端的三分序列不可靠;有聲端的 b<d<g 才穩。**

**一條與母音有關的重要提醒(原文)**:
> "**Longer VOTs are observed before high and tense vowels, particularly [i]**, for
> voiceless stops (Klatt, 1975; Port & Rotunno, 1979; Weismer, 1979...)"

⚠️ **AVWM 用 /i/ 母音,因此連續體端點應比非母音特定的通用建議值(如 [[winn2020]] Table I)稍往長的方向調。**

## 對 AVWM 的意義
1. **這是引用英語 VOT 數值時的首選來源** —— 現代、大語料庫、可直接取得。Lisker & Abramson (1964) 的數字我只有二手轉引(出版社 403),用本篇可避開轉引問題。
2. **唇音的有聲錨點最低(8–13 ms)、間距最寬、有聲端變異最小** → 給適應式程序最大的乾淨操作空間。(此推論為我所加。)
3. 說明部位選擇不是在挑「性質不同的維度」,而是在挑落點與寬度。

**限制**:
- 美式英語;產出資料,非知覺邊界。
- 上表的間距是**我從平均值相減**得到的,不是作者報告的統計量,**沒有信賴區間**。引用時必須標明。
- 受試者數與語料庫細節我未逐一核對。

## 可連結脈絡
- 發音部位的選擇 —— [[consonant-pair-choice]]
- 同作者的跨語言後續 —— [[chodroff2019]]
- 同作者的 burst 頻譜研究 —— [[chodroff2014]]
- 端點建議值 —— [[winn2020]]
- 知覺邊界的斜率比較 —— [[goldenberg2022]]
- VOT 定義與量測 —— [[abramson2017]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**引用英語 VOT 數值時該用哪一篇?** → 本篇(可直接取得),不要轉引 Lisker & Abramson (1964)。
**哪個部位的有聲端最穩定?** → 唇音(SD 5),軟顎音最不穩(SD 10)。
**用 /i/ 母音要注意什麼?** → 無聲塞音在 /i/ 前 VOT 較長,端點要往長調(本篇)。
