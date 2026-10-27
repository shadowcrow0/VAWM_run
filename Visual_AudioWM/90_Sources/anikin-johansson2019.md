---
tags: [literature-note, crossmodal-correspondence, hue, lightness, IAT, AVWM]
citekey: anikin-johansson2019
---

# Anikin & Johansson (2019) — ⭐⭐⭐ 直接操弄「等明度等彩度只動色相」測跨感官對應:幾乎全部落空

**這是 AVWM 顏色維度設計(固定 L\*/C\*、只動色相角)的直接鏡像實驗——他們就是刻意把 hue 從 luminance、saturation 中獨立出來測。結果:hue 獨立於明度彩度之後,幾乎測不到任何聲學對應,只有一個很小的 pitch–blue 效應,效應量只有明度對應的一半。**

**DOI / URL** https://doi.org/10.3758/s13414-018-01639-7

**閱讀狀態** **未取得全文 PDF**(Springer 與 PMC 的下載請求均被擋下,只取得 HTML/空檔)。內容經 subagent 用 WebFetch 對 PMC6407832 全文頁面**逐段摘要並附精確引句**,含研究問題、方法(如何用 CIE-Lab 色彩空間只讓一個視覺維度變動)、統計量(誤差率 %、95% CI、RT ms)。⚠️ 我本人未通讀原始 PDF,以下引句由 subagent 從全文網頁版轉述,未經我自己逐字核對原文排版與頁碼。

```bibtex
@article{anikin2019implicit,
  author  = {Anikin, Andrey and Johansson, Niklas},
  title   = {Implicit associations between individual properties of color and sound},
  journal = {Attention, Perception, \& Psychophysics},
  volume  = {81}, number = {3}, pages = {764--777}, year = {2019},
  doi     = {10.3758/s13414-018-01639-7}
}
```

## 研究問題
用 Implicit Association Test(IAT)系統性地測試:視覺的 luminance(明度)、hue(紅綠 a\* 軸、黃藍 b\* 軸)、saturation(彩度)三個維度,分別跟聽覺的 loudness、pitch、formant(F1/F2)、spectral centroid、trill 等維度,哪些會產生穩定的內隱聯結?**關鍵設計是讓每一對比較只在單一視覺維度上不同**(其餘維度固定),藉此把 hue 從 luminance/saturation 中乾淨地分離出來。

## 方法與族群
一系列 IAT 實驗。顏色刺激取自 CIE-Lab 感知均勻色彩空間,成對顏色只在**單一維度**(L、a、b 三選一)上不同。聲音刺激用共振峰合成器(formant synthesizer)產生類母音的複合音,可分別操弄 loudness、pitch、F1、F2、spectral centroid、trill 有無。為了排除響度混淆,先用前測校正各刺激組的主觀響度。

## 結果與限制

### ⭐⭐⭐ 核心發現:等明度等彩度下,hue 幾乎測不到任何聲學對應
> "Neither green-red nor yellow-blue hue contrasts were reliably associated with any of the tested acoustic features, with one exception: high pitch was associated with blue (vs. yellow) hue."

唯一的例外效應很小:
> "This effect was relatively small, but its confidence intervals excluded zero for both error rates (1.1% fewer errors, 95% CI [0, 3.5]) and response time (49 ms, 95% CI [10, 96])."

還有一個邊緣顯著的頻譜重心效應(方向一致但未達顯著):
> "A statistically marginal, but logically consistent congruence effect was observed between high spectral centroid and blue (vs. yellow) hue" — errors 1.5%(95% CI [−0.1, 4.5]),RT 25 ms(95% CI [−3, 59])。

**效應量對照(這是最關鍵的一句)**:
> "The effect size for hue contrasts (0–1.5% and 0–50 ms) was thus about half of that for luminance contrasts."

### 明度(luminance)對應穩固:pitch↔lightness
> "Higher pitch was associated with light as opposed to dark gray." Table 4 顯示明度對應的誤差率差距達 3–4%、RT 差距 60–120 ms —— **是 hue 對應效應量的兩倍左右**。而且 pitch–luminance 與 loudness–luminance 是兩個獨立機制(有各自的解離證據)。

### 彩度(saturation)對應:loudness↔saturation
> "High (vs. low) saturation was associated with greater loudness." 誤差率差距 4.1%(95% CI [1.9, 8.5]),RT 差距 84 ms(95% CI [39, 137])。

### formant 與明度/色相皆無關聯
> "We did not observe any association between changes in the frequencies of the first two formants and either luminance or hue of the presented colors."

作者將此歸因於他們用 spectral centroid 控制法把 formant 位移造成的頻譜重心變化去掉了——意味著文獻裡許多「母音↔顏色」的對應,底層驅動的可能其實是頻譜重心(整體頻譜能量的高低頻平衡),不是母音音質本身。

## 限制
- ⚠️ **本卡未經我本人通讀全文**,只有 subagent 的 WebFetch 摘要,雖附精確數字與引句,但無法排除摘要遺漏了原文的但書或方法細節。**這是本卡最大的限制,查證時務必意識到。**
- 本研究用的聲音刺激是合成母音類的複合音,沒有測試過任何子音特徵(voicing、manner、place),所以完全沒有直接處理 AVWM 關心的 voicing×hue 問題——它證明的是「hue 本身作為一個視覺維度」在等明度等彩度條件下幾乎不參與跨感官對應,不是「voicing 這個聲學特徵」不參與。
- 唯一測到的 hue 效應(pitch↔blue)是在**藍黃軸**(b\* 軸)上,AVWM 的色相軸(303° 錨點,藍紫到粉紫)混合了 a\*、b\* 兩個分量,不是乾淨的藍黃對比,套用時需要額外小心。

## 可連結脈絡
- 這是 [[johansson2020]] 引用的姊妹研究,結論被該文用來解釋為何略過 hue 分析
- 與 [[spence2011]] Table 1 的 pitch–hue 陰性結果(Bernstein, Eason, & Schurman 1971)方向一致,是後續更精細的直接驗證
- 本卡是 [[voicing與顏色的跨感官對應]] 回答「AVWM 一致性對比是否歸零」這題的**最直接證據**

---
標籤note:[[literature-note]] [[crossmodal-correspondence]] [[AVWM]]

## 回查線索
**AVWM「固定 L\*/C\*、只動色相」的設計,文獻上直接測過類似操弄嗎?** → **測過,而且結果對 AVWM 不利。** 本研究就是刻意把 hue 從 luminance/saturation 隔離開來測,結果幾乎沒有可靠的聲學對應,唯一的例外(pitch↔blue)效應量只有明度對應的一半。

**明度和色相,哪個承載跨感官對應比較穩固?** → **明度。** pitch–luminance 效應量(3–4% 誤差率、60–120ms)是 hue 對應效應量(0–1.5%、0–50ms)的兩倍左右。

**本卡的證據強度打了什麼折扣?** → 未取得原始 PDF,是 subagent 的網頁摘要,雖有精確數字但未經我本人逐字核對。
