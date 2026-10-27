---
tags: [literature-note, 子音混淆, transmitted-information, SINFA, 安靜環境, voicing, AVWM]
citekey: wang-bilger1973
---

# Wang & Bilger (1973) — 唯一同時測「安靜」與「噪音」的子音混淆矩陣研究:voicing 的優勢在安靜下會縮小

**這是核實「安靜環境下 voicing 混淆有多小」這個問題最直接的來源** —— Miller & Nicely (1955) 從未測安靜,本篇的 control experiment 補上了這一塊,而且用同一套刺激直接對照噪音與安靜兩種情境。

**DOI / URL** https://doi.org/10.1121/1.1914417 | 免費 PDF(作者存放版,含全部表格) https://jontalle.web.engr.illinois.edu/Public/WangBilger73_NH_CVconfusions.pdf

**閱讀狀態** **全文已讀**(PDF 直接由 Read 工具讀出,19 頁全部內容,含 Tables I–XXI)。**Table VI 的 b–p/d–t/g–k 拆解與比率為我自己的算術**,已標明。

```bibtex
@article{wang1973consonant,
  author  = {Wang, Marilyn D. and Bilger, Robert C.},
  title   = {Consonant confusions in noise: A study of perceptual features},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {54}, number = {5}, pages = {1248--1266}, year = {1973},
  doi     = {10.1121/1.1914417}
}
```

## 研究問題
如果把「特徵在噪音/安靜下互相獨立冗餘」的效果考慮進去(用 sequential information analysis, SINFA,逐步 partial 掉已識別特徵的貢獻),**還有沒有一組「自然的知覺特徵」會穩定地、跨情境地解釋子音辨識表現?voicing 的優勢是不是這樣一個穩定特徵?**

## 方法與族群
- **單一成年男性說話者**,每個音節錄 5 次取最自然/最大聲/時長最典型的一次,存到 Cognitronics Speechmaker 語音鼓上重播(⚠️ **單一說話者、每音節單一 token** —— 與 [[clark1973]] 的固定效果謬誤、[[token-variability-vs-perceptual-variance]] 的疑慮直接相關)。
- **四組 16 音節集**(CV-1、VC-1、CV-2、VC-2),每組 = 16 個子音 × /i, ɑ, u/ = 48 音節。**CV-1 與 Miller & Nicely 幾乎相同**(16 子音組合,只是把 /m n/ 換成 /tʃ dʒ/)。
- **噪音實驗**:6 個 S/N(−10 至 +15 dB,等距),4 個絕對噪音位準(50/65/80/95 dB SPL),三次重複。
- **控制實驗(= 安靜條件)**:同一批刺激,不加噪音,只變化訊號強度(20–45 dB SPL 每 5 dB 一階、55–115 dB SPL 每 10 dB 一階,共 13 個位準),兩組各 6 位受試者。**這是本文對 AVWM 最重要的部分。**
- 受試者:16 位付費志願者(6 男 10 女,17–24 歲),多數無聆聽實驗經驗。

## 結果與限制

### ⭐⭐ 核心發現:voicing/nasality 的優勢是「噪音特有」的,安靜下會相對縮小
> "Two general points can be made about these results. First, **the relative importance of the features changes as a function of the listening conditions, i.e., noise versus quiet. Voicing and nasality are well perceived in the presence of masking noise, but their intelligibility drops relative to that of other features in quiet.**"

**這句話必須小心解讀 —— 「drops relative to」是相對排名下降,不是絕對表現變差。** 實際數字(Table XII,CV-1 集,percent information transmitted):

| 條件 | Voice | High-anterior | Sibilant | 備註 |
|---|---|---|---|---|
| −10 dB | 8.7% | 2.6% | 3.0% | 噪音下 voice 遠贏 |
| +15 dB | 78.1% | 79.5% | 77.9% | 噪音趨緩後三者接近 |
| **Quiet** | **57.1%** | **63.4%** | **60.1%** | **安靜下 voice 變成第三,不是第一** |

**→ Voice 在安靜下絕對值仍高(57.1%),但被 high-anterior(63.4%)、sibilant(60.1%)超過。這不是「voicing 變差」,是「其他特徵在安靜下追上甚至超過它」。**

### SINFA(partial 掉冗餘後)的結果:voice 在安靜下仍是穩定核心特徵之一
Table XVII 的 SINFA 摘要顯示,CV-1 集在**所有**聆聽條件下(含安靜)都會識別出同一組核心特徵:
> "SINFA for the CV-1 syllable set reveals that four features consistently contribute to discrimination performance under all listening conditions: **voice, sibilant, high-anterior, and frication.** ... voice losing its primacy only at +15 dB S/N **and in quiet**."

**→ Voice 在安靜與 +15 dB 這兩個「非常容易」的條件下不再是排名第一的特徵,但仍然是穩定被識別出的四個核心特徵之一 —— 不是被排除,是被追平。**

### 全域結論(Discussion,原文逐字):只有三個特徵跨情境穩定重要
> "The first category contains the features nasal, voice, and round. Nasal and voice are features which have appeared in all feature systems suggested in the literature, and there are no alternative formulations of the distinctions carried by these two features. Because of this, and because **both features are well perceived both in noise and in quiet**, they are identified as perceptually important in every syllable set where they are distinctive."

> "Voice, nasal, and possibly round, appear to be the only exceptions to this rule [that no natural perceptual features exist]."

**→ 這是本篇最重要的一句話對 AVWM 的意義:在「有沒有自然知覺特徵」這個大哉問上,作者整體結論是懷疑的(大多數特徵的重要性隨情境變動),但 voicing 是極少數幾個「不管什麼情境都重要」的特徵之一。這比 Miller & Nicely 單看噪音下的 18 dB 差距更有力,因為它是跨噪音與安靜兩種情境驗證過的。**

### ⭐⭐ 直接可比較 AVWM 的資料:安靜下 b–p / d–t / g–k 的混淆率(我的算術)
Table VI 是 CV-1 集在**全部訊號強度合併**(即安靜控制實驗,20–115 dB SPL 合併)下的混淆矩陣。從中取出 p t k b d g 六個子音的子矩陣:

| | p | t | k | b | d | g | 列總數 |
|---|---|---|---|---|---|---|---|
| p | 773 | 38 | 35 | 9 | 14 | 6 | 930 |
| t | 33 | 783 | 27 | 7 | 19 | 6 | 930 |
| k | 71 | 89 | 585 | 11 | 14 | 18 | 933 |
| b | 21 | 11 | 8 | 587 | 28 | 17 | 933 |
| d | 9 | 10 | 4 | 32 | 771 | 24 | 930 |
| g | 4 | 4 | 8 | 27 | 41 | 764 | 927 |

**跨 voicing 混淆率(我算的)**:

| 配對 | 跨 voicing 錯誤數 | 分母 | 錯誤率 |
|---|---|---|---|
| p ↔ b | 9 + 21 = 30 | 930 + 933 = 1863 | **1.61%** |
| t ↔ d | 19 + 10 = 29 | 930 + 930 = 1860 | **1.56%** |
| g ↔ k | 8 + 18 = 26 | 927 + 933 = 1860 | **1.40%** |
| **三對合併** | 85 | 5583 | **1.52%** |

**→ 在安靜下,三對的跨 voicing 混淆率幾乎相同(1.4–1.6%),差距(0.2 個百分點)遠小於任一組的抽樣誤差(以 n≈1860、p≈0.015 估計,標準誤約 0.28 個百分點)。這與 [[miller-nicely1955]] Table XVIII 在 −12 dB 噪音下量到的「b–p 明顯較高(4.25%)」不同 —— 安靜下這個差異消失了。**

**這三對各自的整體正確率(同一張表)**:p 83.1%、t 84.2%、k 62.7%、b 62.9%、d 82.9%、g 82.4%。**k 與 b 的正確率明顯較低,但低的原因不是 g–k 或 b–p 的 voicing 混淆(那部分只佔 1.4–1.6%)** —— k 主要與塞擦音 /tʃ/(37 次)、/dʒ/(47 次)混淆(這組 CV-1 刺激特有的替代設計),b 的錯誤則分散在多個非 voicing 配對之間。**這與 [[singh-allen2012]] 用完全不同的語料庫、完全不同的方法得到的結論高度一致:b 的高錯誤率主要來自與擦音/塞擦音的混淆,不是與 p 的 voicing 混淆。**

### 母音效果:/i/ 比 /ɑ/ 更難識別子音(不分噪音或安靜)
> "In CV syllable sets, consonants followed by /i/ were the most difficult to identify" (控制實驗); 噪音實驗中 "/ɑ/ 最難、/u/ 最易" 但 CV 語境下 "/i/" 同樣偏難。

⚠️ **對 AVWM 是一個提醒**:AVWM 選 /i/ 母音是為了避開 [[winn2020]] 講的 F1-cutback 混淆,但本篇獨立發現 **/i/ 脈絡本身在 CV 語境下比 /ɑ/、/u/ 更難識別子音**(機制未知,推測與共振峰軌跡或音節結構有關)。這不是否定 /i/ 的選擇,而是提醒:換成 /i/ 換掉了一種混淆(F1 共變),但可能換來另一種(整體辨識率下降)。

## 限制
- **單一說話者、每音節單一 token** —— 這正是 [[clark1973]] 的 language-as-fixed-effect 謬誤要小心的情境,「固定混淆」的疑慮見 [[決策脈絡_聽覺維度]] §七。
- 受試者年輕(17–24 歲)、多數無聆聽實驗經驗,與 Miller & Nicely 訓練有素的聽力小組不同。
- SINFA 的 iteration 選擇有寬鬆的判準(貢獻 ≥1% 總傳輸資訊即列入),作者自陳更嚴格的判準(如 5%)會得到較少特徵。
- **本篇 Table VI 的 b–p/d–t/g–k 拆解是我在查證過程中自己做的計算**,不是原作者分析重點;原文的 SINFA 分析在「特徵」層次(voicing vs. place 等),沒有下探到「哪一對部位配對」的層次。
- CV-1 集用 /tʃ dʒ/ 取代 M&N 原本的 /m n/,因此不能直接說是 M&N 資料的重複,只是「非常接近」。

## 可連結脈絡
- 正典來源與噪音下的 18 dB 差距 —— [[miller-nicely1955]]
- 現代語料庫、utterance 層級的安靜資料 —— [[phatak-allen2007]]、[[singh-allen2012]]
- 母語者 manner ≈ voicing > place 的現代驗證 —— [[cutler2004]]
- 單一說話者/單一 token 的方法學疑慮 —— [[clark1973]]、[[token-variability-vs-perceptual-variance]]
- 子音對選擇的既有回顧(本卡新補的安靜條件證據)—— [[consonant-pair-choice]]
- 本卡是 [[子音混淆最小化]] 的核心證據來源

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**安靜環境下 voicing 的優勢還在嗎?** → **還在,但不再是唯一最強的。** 絕對傳輸率仍有 57%,但被 high-anterior(63%)、sibilant(60%)超過;SINFA 分析裡 voice 在安靜下「失去領先地位,但仍是核心四特徵之一」。

**安靜下 b–p、d–t、g–k 誰的混淆最小?** → **幾乎沒有差別**(1.40–1.61%,合併 1.52%),差距在抽樣誤差範圍內。這與 [[miller-nicely1955]] 在 −12 dB 噪音下量到的「b–p 較高」不同,支持「那個差異是雜訊」的判斷。

**有沒有研究同時測過同一批刺激的安靜與噪音兩種條件?** → 有,就是本篇 —— 這是唯一一篇這樣做的经典子音混淆文獻。
