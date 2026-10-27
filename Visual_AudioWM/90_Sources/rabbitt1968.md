---
tags: [literature-note, 遮蔽噪音, 工作記憶, 聆聽費力度, 經典文獻]
citekey: rabbitt1968
---

# Rabbitt (1968) — 噪音中的語音會吃掉「頻道容量」,傷害的是**先前**已聽到的項目

**DOI / URL** https://doi.org/10.1080/14640746808400158 | PMID 5683763
**閱讀狀態** ⚠️ **未讀原文,且 PubMed 無摘要**。本卡的全部內容為**二手**,來源有二:
(a) [[guang2021]] 的直接複製研究(該文的方法/導論段我已逐字閱讀),
(b) [[luce1983]] 導論段對本篇的引述(亦已逐字閱讀)。
**引用具體數值前必須取得原文。**

```bibtex
@article{rabbitt1968channel,
  author  = {Rabbitt, Patrick M. A.},
  title   = {Channel-capacity, intelligibility and immediate memory},
  journal = {Quarterly Journal of Experimental Psychology},
  volume  = {20}, number = {3}, pages = {241--248}, year = {1968},
  doi     = {10.1080/14640746808400158}
}
```

## 研究問題
噪音造成的回憶下降,是不是**只是**因為項目聽錯了?還是「在噪音中辨識語音」這個動作
本身就佔用了處理容量,連帶傷害到**已經正確聽到**的其他項目?

⚠️ **這是 AVWM 現在最該問的問題。** 因為專案傾向改走「自然 token + speech-shaped noise」,
而 AVWM 的作業本身就是工作記憶作業。

## 方法與族群
三個實驗(以下依 [[guang2021]] 的描述,非原文):

- **實驗 1**:數字串經 pulse-modulated 白噪音呈現。錯誤數**超過**「辨識錯誤與記憶錯誤
  各自獨立」所預期的量。
- **實驗 2(最有影響力)**:八個數字的清單,**前半與後半各自**在噪音或安靜中呈現,
  呈現後才提示回憶前半或後半。→ 2×2 設計(clear/clear、clear/noise、noise/clear、
  noise/noise)。
- **實驗 3**:散文段落,事後回答事實性問題。

族群、樣本數、SNR **原文均未取得**;[[guang2021]] 明說 Rabbitt 未報告 SNR
(「Rabbitt (1968) did not report the signal-to-noise ratio used」),且他一次測
11–21 人。

## 結果與限制

**關鍵發現(依 [[guang2021]] 的逐字描述)**:

> "The key finding was that recall of digits in the first half was better when items in
> the second half were presented in the clear rather than in noise. That is, subsequent
> noise impaired recall for previously presented items, regardless of whether those items
> were themselves presented in noise."

**為什麼這個發現特別有力([[guang2021]] 的論證,逐字)**:

> "recall for the words in the first half of the list was impaired as a result of a noise
> manipulation that occurred **after** those words were presented ... Thus, the impaired
> recall of first-half items **cannot be attributed to noise obscuring the intelligibility
> of the to-be-remembered items.**"

**實驗 3 的類比結果**:散文前半的回憶正確率,在後半必須在噪音中聽時較差。

**Rabbitt 自己的解釋**:在噪音中聽語音佔用了「channel capacity」,因而抑制了複誦。

**[[luce1983]] 對本篇的引述(逐字)**:
> "Rabbitt concluded that degraded input requires 'spare capacity' in short-term memory"

### 對 AVWM 的意義 —— 這是路線切換後的核心風險

**如果 AVWM 改用「自然 token + 噪音」,它並沒有避開資源消耗的問題,只是換了退化的來源。**
Rabbitt 的效應**不需要**受試者聽錯就會發生 —— 這意味著即使 AVWM 把 SNR 調到讓辨識率
落在目標區間,噪音仍可能在消耗保留期的複誦資源。

**限制**:
- **我完全沒讀原文。** 上述全部是二手。
- Rabbitt 未報告 SNR、族群細節。
- 效應量小(見 [[guang2021]]:Cohen's d = 0.19)。
- Rabbitt 的作業是**數字串序列回憶**,與 AVWM 的「顏色+語音複合項目」跨通道作業不同。
- **機制未定**:[[guang2021]] 明說「the mechanisms underlying the effect remain unclear」,
  可能是複誦被干擾,也可能是感官記憶被干擾。

## 可連結脈絡
- 五十二年後的直接複製 —— [[guang2021]](效果量完全相同,d = 0.19)
- 同一機制的聽損版本 —— [[mccoy2005]](effortfulness hypothesis)
- 合成語音研究把合成音類比為噪音 —— [[luce1983]] General Discussion
- AVWM 為何走噪音路線 —— [[silbert2012]]
- 噪音改變線索權重(另一個噪音的副作用) —— [[winn2013]]
- 綜合回顧 —— [[synthetic-speech-cognitive-load]]

---
標籤note:[[literature-note]] [[speech-perception]] [[working-memory]] [[AVWM]]

## 回查線索
**我在哪些研究看過「操弄發生在項目之後,卻仍傷害該項目的回憶」這種因果分離設計?** → 本篇
實驗 2 與 [[guang2021]]。這是排除「清晰度解釋」的漂亮手法,AVWM 若要自己驗證噪音的
記憶代價,可以直接借用。
**「degraded input 需要 spare capacity」這句話的出處?** → 本篇(經 [[luce1983]] 轉引)。
