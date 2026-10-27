---
tags: [literature-note, 合成語音, 認知負荷, 瞳孔測量, 現代TTS, 結論與數據不符]
citekey: govender2018
---

# Govender & King (2018) — 瞳孔測量現代合成語音:**摘要的結論比它的統計強**

**DOI / URL** https://doi.org/10.21437/Interspeech.2018-1174 | PDF https://www.isca-archive.org/interspeech_2018/govender18_interspeech.pdf
**閱讀狀態** ✅ **全文 PDF 已讀**(2026-08-12 下載並逐段閱讀,含三個實驗的全部 ANOVA 數值)。

```bibtex
@inproceedings{govender2018using,
  author    = {Govender, Avashna and King, Simon},
  title     = {Using pupillometry to measure the cognitive load of synthetic speech},
  booktitle = {Proc. Interspeech 2018},
  pages     = {2838--2842}, year = {2018},
  doi       = {10.21437/Interspeech.2018-1174}
}
```

## 研究問題
1980 年代的合成語音認知負荷研究都用規則式合成器。**現代(unit selection / HMM / hybrid)
的合成語音,還會不會比自然語音耗更多認知資源?** 瞳孔測量能不能當成評估工具?

作者自陳的動機(原文):
> "Cognitive load has been investigated in the past, when rule-based speech synthesizers
> were popular, but there is little or no recent work using state-of-the-art
> text-to-speech."

**這正是 AVWM 第 5 題的正面對應文獻。**

## 方法與族群
- **45 名受試者**,分到三個實驗,**每個實驗 15 人**(19–37 歲英語母語者)。
- 刺激來自 **Blizzard Challenge 2010 / 2011** 的參賽系統:Hybrid、Unit Selection、
  HMM、Low-Quality HMM,加上**同一語者的自然錄音**。
- 眼動儀 SR Eyelink 1000 plus,500 Hz。依變項:**平均瞳孔大小、峰值擴張、峰值潛時**,
  外加**口語複誦正確率**與**主觀評分**(自然度、困難度、動機)。
- 實驗 1、2 用 **semantically unpredictable sentences (SUS)**;實驗 3 用**有意義句**。
- 分析:repeated-measures ANOVA + Bonferroni 校正的成對 t 檢定。

## 結果與限制

### ⚠️ 本卡最重要的一點:摘要/結論與內文統計不一致

**摘要與結論段的宣稱(原文)**:
> "In all cases, synthetic speech imposes a higher cognitive load than natural speech."

**但三個實驗的瞳孔 ANOVA 幾乎全部不顯著(全部逐字自原文):**

| 實驗 | 平均瞳孔 | 峰值擴張 | 峰值潛時 |
|---|---|---|---|
| 1 (SUS, BC2011) | F(4,56)=1.5, **p=0.2** | F(4,56)=2.09, **p=0.09** | F(4,56)=4.21, **p=0.005 ✅** |
| 2 (SUS, BC2010) | F(4,56)=1.8, **p=0.14** | F(4,56)=0.9, **p=0.44** | F(4,56)=1.44, **p=0.23** |
| 3 (有意義句, BC2011) | F(4,56)=1.19, **p=0.32** | F(4,56)=1.67, **p=0.17** | F(4,56)=0.6, **p=0.65** |

**九個檢驗中只有一個顯著**:實驗 1 的峰值潛時,而且是**自然語音 vs Low-Quality HMM**
這一對(自然 3.1 s vs LQ-HMM 2.3 s)—— **不是**自然 vs 高品質合成。實驗 1 原文:

> "The differences in mean and peak pupil dilations between all systems were
> statistically insignificant."

作者自己在討論段也承認系統間差異難以偵測:
> "differences between speech synthesizers were more difficult to detect. We found a
> tendency towards differences, but these were not strong enough to reach significance.
> Alternative statistical tests, such as growth curve analysis, might have given more
> accurate estimates of significance."

**我的判讀(推論,非原文)**:摘要那句 "In all cases, synthetic speech imposes a higher
cognitive load" **不是由本文的推論統計支撐的**,而是由圖形的目視趨勢支撐的。
**引用本篇時不可拿摘要那句當證據。** 本篇實際能支持的是更弱的命題:
「在 n=15、以瞳孔為指標的條件下,高品質合成語音與自然語音的認知負荷差異偵測不到。」

### 其他有用的結果

- **複誦正確率**:實驗 1 全系統 ≥ 95%,實驗 3 全系統 ≥ 94%,實驗 2 平均 91%。
  高品質合成器與自然語音**無差異**。
- **主觀評分**:三個實驗都是自然語音被評為最容易聽 —— **主觀負荷與客觀瞳孔分歧**。
- 實驗 3(有意義句)原文:「it is clear that natural speech barely causes any pupil
  dilation at all ... listening to meaningful natural sentences in quiet conditions is
  effortless」。而實驗 1 的 SUS 材料確實引起自然語音的瞳孔擴張。
  → **語意可預測性主宰了認知負荷,遠超過合成 vs 自然。**

**限制**:
- **每個實驗只有 15 人** —— 對於全部 null 結果,這是嚴重的檢定力問題。
  作者自承統計方法可能不夠敏感。
- 最新的系統是 hybrid / unit selection / HMM,**沒有 DNN / neural vocoder / 端到端
  TTS**(2010–2011 年的 Blizzard)。所以「state-of-the-art」是 2018 年的說法,
  對 2026 年仍是舊的。
- 刺激是**整句**,不是單音節。與 AVWM 的作業結構差距很大。

## 可連結脈絡
- 1980 年代的原始發現 —— [[luce1983]]、[[humes1993]]
- 另一份現代瞳孔測量,結論更複雜 —— [[simantiraki2023]]
- 「品質改善 ≠ 負荷下降」的實驗檢驗 —— [[francis2009]]
- 綜合回顧 —— [[synthetic-speech-cognitive-load]]

---
標籤note:[[literature-note]] [[speech-perception]] [[working-memory]] [[AVWM]]

## 回查線索
**我在哪些論文抓到「摘要的結論強過內文統計」?** → 本篇。
與 [[mbrola-cannot-do-vot]] 的「工具宣稱 vs 實測」是同一類警覺。
**認知負荷的主宰因素是什麼?** → 本篇實驗 1 vs 3 的對比顯示:**語意可預測性 > 語音來源**。
