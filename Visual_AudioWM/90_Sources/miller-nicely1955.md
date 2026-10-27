---
tags: [literature-note, 子音混淆, transmitted-information, voicing, place, 正典來源, AVWM]
citekey: miller-nicely1955
---

# Miller & Nicely (1955) — voicing 比 place 穩健 18 dB 的正典來源(⚠️ 但從未測過「安靜」)

**這是「voicing/nasality 是高度可區辨的聽覺資訊」這個說法的正典出處。**核實結果:說法成立,但有兩個常被省略的但書——(1)全篇沒有一個「安靜、無噪音」的條件,最好的條件是 +12 dB S/N;(2)母音固定是 /ɑ/(father),不是 AVWM 的 /i/。

**DOI / URL** https://doi.org/10.1121/1.1907526 | 免費 PDF(課程網站重製全文,含全部表格)
https://jontallen.ece.illinois.edu/uploads/537.F18/Papers/MillerNicely55.pdf
勘誤 *JASA* 27(3), 617 (1955)(⚠️ 內容未取得,僅由 AIP 頁面標題確認存在)

**閱讀狀態** **全文已讀**(PDF 直接由 Read 工具讀出,含 Tables I–XXI、Figs. 1–6 全部內容,逐字核對)。本卡的 Table XVIII 計算與各 SNR 相對傳輸率計算為**我自己的算術**,已標明。

```bibtex
@article{miller1955analysis,
  author  = {Miller, George A. and Nicely, Patricia E.},
  title   = {An Analysis of Perceptual Confusions Among Some English Consonants},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {27}, number = {2}, pages = {338--352}, year = {1955},
  doi     = {10.1121/1.1907526}
}
```

## 研究問題
語音在噪音/濾波下的錯誤不是隨機的。如果把 16 個英語子音拆成 5 個構音特徵(voicing、nasality、affrication、duration、place),**每個特徵各自在噪音/濾波下的穩健程度是多少?這些特徵是不是彼此獨立的知覺「通道」?**

## 方法與族群
- **5 位女性受試者**兼任說話者與聽者(除一位加拿大人外皆為美國公民),互相輪流說/聽,沒有言語或聽力缺陷。
- **16 個子音**:/p t k f θ s ʃ b d g v ð z ʒ m n/。
- **母音固定為 /ɑ/**(原文逐字):"The 16 consonants were spoken initially before the vowel |a| (father)."(p. 339)—**已核實不是 /i/**。
- 200 個無意義音節的清單,每個音節出現機率 1/16,順序隨機;受試者被強迫每個音節都要猜。
- **17 個測試條件**:Tables I–VI 是 S/N = −18, −12, −6, 0, +6, +12 dB(頻寬 200–6500 Hz);Tables VII–XII 是 +12 dB 但低通濾波(300–5000 Hz 六種截止頻率);Tables XIII–XVII 是 +12 dB 但高通濾波(1000–4500 Hz 五種截止頻率)。
- 每個矩陣 4000 筆觀察(5 位說話者 × 4 位聽者 × 200 音節),每個音節平均被判斷 250 次。

### ⚠️ 沒有「安靜」條件
**全部 17 個條件都含噪音或濾波,最寬鬆的條件是 +12 dB S/N(200–6500 Hz,Table VI/condition 6)或 +12 dB + 200–5000 Hz 帶通(condition 12)。原文從未報告一個無噪音的基準。** 這點在 AVWM 的情境(安靜播放)下必須另外用 [[wang-bilger1973]] 或 [[singh-allen2012]] 的真正 quiet 資料補。

## 結果與限制

### ⭐ 核心主張(原文逐字,p. 348–349)
> "The glaringly obvious statement that must be made about Figs. 1 and 2 is that voicing and nasality are much less affected by a random masking noise than are the other features. Affrication and duration, which are so similar that a single function could represent them both, are somewhat superior to place but far inferior to voicing and nasality. **Voicing and nasality are discriminable at signal-to-noise ratios as poor as −12 db whereas the place of articulation is hard to distinguish at ratios less than 6 db, a difference of some 18 db in efficiency.**"

Fig. 1 圖說(p. 348):
> "Voicing information is transmitted at signal-to-noise levels 18 db below those needed for place information."

**這就是「18 dB」這個數字的出處** —— 是 voicing 與 place 兩條相對傳輸率曲線在圖上的水平位移,不是單一統計檢定的效果量。

### Voicing 與 nasality 的關係:原文的兩種說法不完全一致
- 噪音遮蔽下(Fig. 2 圖說,p. 349):**"Nasality and voicing are equally discriminable."**
- 低通濾波下(Fig. 4 圖說,p. 350):**"Nasality is somewhat more discriminable than voicing."**

⚠️ **我自己用 Table XXI 除以各特徵的 Maximum possible(見下)重算了每個 SNR 下 voicing 與 nasal 的相對傳輸率,發現 voicing 在噪音遮蔽的六個 SNR 中都略高於 nasal**(差距約 2–7 個百分點,見下表)。這與原文「equally discriminable」的定性描述大致相容(差距不大),但嚴格說**不是完全相等** —— 這是我的算術,原文沒有明說這個細節。

### 具體數字:各 SNR 下 voicing 與 place 的相對傳輸率
原始資料是 Table XXI(bits/stimulus,已傳輸資訊量)加上該表最底列的 Maximum possible(voicing 上限 0.989 bits、place 上限 1.546 bits)。**相對傳輸率(即 Fig. 1 所畫的百分比)是我依原文定義的公式重算的**(原文定義見下):

> "The relative measure is computed from Table XXI by dividing each entry in that table by the maximum value given at the bottom of each column." (p. 349)

| S/N (dB) | Voicing 相對傳輸率 | Place 相對傳輸率 |
|---|---|---|
| −18 | 2.1% | 0.06% |
| −12 | 52.2% | 3.8% |
| −6 | 80.6% | 16.1% |
| 0 | 95.4% | 37.4% |
| +6 | 96.2% | 55.4% |
| +12 | 96.7% | 70.5% |

**→ Voicing 在 −12 dB 已達五成以上的傳輸率,place 要到 +6 dB 才追上這個水準。**

### ⭐⭐ 直接可比較 AVWM 的資料:Table XVIII 六子音矩陣(S/N = −12 dB)
本文在示範「一般化的 articulation score」時,剛好用了一個**只含 6 個塞音**(p t k b d g)的獨立矩陣(p. 346,2000 筆觀察),這是全文唯一一處把 voicing 對比拆到「配對」層次的地方:

> TABLE XVIII. Confusion matrix at S/N = −12 db with a 200–6500-cps channel.

| | p | t | k | b | d | g | Sum |
|---|---|---|---|---|---|---|---|
| p | 117 | 58 | 115 | 14 | 10 | 2 | 316 |
| t | 74 | 101 | 103 | 8 | 4 | 6 | 296 |
| k | 105 | 109 | 153 | 5 | 8 | 4 | 384 |
| b | 13 | 9 | 10 | 217 | 45 | 26 | 320 |
| d | 3 | 4 | 5 | 47 | 200 | 117 | 376 |
| g | 3 | 11 | 8 | 45 | 147 | 94 | 308 |

**由此表算出的 b–p / d–t / g–k 跨 voicing 混淆率(我的算術,原文沒有算這個)**:

| 配對 | 跨 voicing 錯誤數 | 分母(兩列總數) | 錯誤率 |
|---|---|---|---|
| p ↔ b | 14 + 13 = 27 | 316 + 320 = 636 | **4.25%** |
| t ↔ d | 8 + 4 = 12 | 296 + 376 = 672 | **1.79%** |
| k ↔ g | 4 + 8 = 12 | 384 + 308 = 692 | **1.73%** |

**→ 在這一個 −12 dB 的樣本裡,b–p 的跨 voicing 混淆率是三對裡最高的**(約 d–t、g–k 的兩倍多)。⚠️ **但這是單一 SNR、單一樣本(n 僅 636–692),且與同一部位內的 place 混淆相比小得多**(同一張表裡,voiceless 組內 p/t/k 互相混淆的比例高達 56.6%,voiced 組內 b/d/g 互混高達 42.5% —— 見 [[子音混淆最小化]] 正文計算)。**這個 4.25% vs 1.7–1.8% 的差異在 [[wang-bilger1973]] 的安靜資料中沒有重現**(見該卡),應視為雜訊而非穩定效應。

### 五個特徵的定義(Table XIX,原文完整分類)
voicing:/ptkfθsʃ/ 無聲 vs /bdgvðzʒmn/ 有聲。nasality:僅 /m n/。affrication:/fθsʃvðzʒ/ vs 其餘。duration:/sʃzʒ/(長)vs 其餘 12 個。place:front /pbfvm/、middle /tdθsʃzʒn/、back /kgʒ/(原文注明 place 是五個特徵裡「最表面、最不令人滿意」的一個)。

### 高通 vs 低通濾波的不同性質(方法論觀察,p. 350)
> "low-pass filters affect the several linguistic features differentially, leaving the phonemes audible but similar in predictable ways, whereas high-pass filters remove most of the acoustic power in the consonants, leaving them inaudible and, consequently, producing quite random confusions."

→ 噪音遮蔽的效果與低通濾波非常相似(兩者都留下規律的、可預測的混淆型態);高通濾波則是另一種性質完全不同的破壞(製造出接近隨機的錯誤)。**這代表噪音遮蔽下量到的 18 dB voicing 優勢,是「規律混淆」意義下的優勢,不是任何形式退化都會重現的。**

## 限制
- **沒有安靜(quiet)條件** —— 這是本卡對 AVWM 最重要的限制,見上。
- **母音固定 /ɑ/**,不是 AVWM 的 /i/;§4(Winn 2020 的論證)已在 [[consonant-pair-choice]] 中討論過 /ɑ/ 脈絡對 voicing-vs-place 判斷可能帶來的額外混淆,但 M&N 本身沒有測試母音效果。
- 5 位女性說話者(單一性別),受試者也全部是女性,無意義音節、非自然對話語速。
- Table XVIII 的 b–p/d–t/g–k 拆解是**我在查證過程中自己做的計算**,不是原作者的分析重點;原文從未在部位配對層次比較 voicing 穩健度。
- 這是**16 選 16 的開放式辨識**,不是 AVWM 可能採用的 2 選 2(b vs p)強迫選擇;16 選 16 下的許多「錯誤」其實是與 p/b 完全無關的其他 14 個子音,不能直接套用到二選一的情境(見 [[子音混淆最小化]] §5 的討論)。

## 可連結脈絡
- 後續複製與修正 —— [[wang-bilger1973]](安靜 vs 噪音)、[[phatak-allen2007]]、[[singh-allen2012]](現代語料庫、utterance 層級)、[[cutler2004]](manner ≈ voicing > place)
- 子音對選擇的既有回顧 —— [[consonant-pair-choice]]、[[軟顎音證據補充]]
- 母音脈絡與 VOT 操弄方法學 —— [[winn2020]]
- 本卡是 [[子音混淆最小化]] 的核心證據來源

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**「voicing 比 place 穩健 18 dB」這句話的出處是什麼,精確地說是什麼意思?** → 本篇 Fig. 1 圖說(p. 348):voicing 在比 place 低 18 dB 的 S/N 下就能達到同等的相對傳輸率。這是圖上兩條曲線的水平位移,不是單一效果量。

**Miller & Nicely 有沒有測過「安靜」?** → **沒有。** 全部 17 個條件都是噪音或濾波,最寬鬆的是 +12 dB S/N。查安靜的量化證據要用 [[wang-bilger1973]]。

**b–p、d–t、g–k 這三對在 M&N 的資料裡誰的 voicing 混淆最小?** → 在其 Table XVIII(−12 dB)裡,**b–p 反而最高**(4.25% vs d–t 1.79%、g–k 1.73%),但這是我自己拆解單一 SNR 資料算出來的,樣本小、未在其他研究重現,不宜當定論。
