# 刺激 token 的變異,會不會污染 GRT 估到的知覺變異?

**敘事型回顧 · 2026-08-12**

研究者提出一個 [[silbert2012]] 的論證沒有處理的反面:GRT 估的是知覺分布的變異與相關
(β、ρ)。若刺激本身在 token 之間就有聲學變異,那個變異會**加進**估到的知覺變異裡 ——
β 就不再是純知覺雜訊。若研究目標是量出「最底層的知覺現況」,這個考量的方向與
Silbert 相反。

**本文的結論是:研究者的直覺方向正確,但問題的形式要改寫兩次;改寫之後,
答案不是「單一自然 token」,而是更前面的一步。**

**引用紀律**:每一條主張後面標注證據強度與閱讀狀態;凡是我的推論而非原文陳述,
都明確標出;凡是本地實測而非文獻,標為「本地實測」。

**姊妹文章**:[[自然音vs合成音_理論推論]] —— 在「實驗室操控優先、生態效度非優先」
的前提下,從理論推出一個明確的選擇。本文負責證據,那篇負責推論。

---

## 0. TL;DR

1. **「β 是不是純知覺雜訊」這個問法在 GRT 裡本來就不成立。** GRT 明文表態
   **不模型化**知覺變異的來源([[silbert-hawkins2016]] §1.1.1 原文),而 Ashby 自己
   把 "stimulus and perceptual noise" 並列為同一個分布的來源([[ashby2000]] 原文)。
   框架甚至已經承認知覺雜訊與決策雜訊**不可分離、只有和可估**
   ([[ashby-wenger-handbook]] 原文)。**刺激變異是同一個和裡的第三項。**
   → 正確的問法是:**那個和裡面「非知覺」的成分有多大、受不受控、對兩個類別對不對稱。**

2. **形式後果的方向是確定的,而且已發表** —— 但在 SDT 不在 GRT。
   [[rouder2007]]:把 item 併掉之後,SDT 的敏感度估計**不一致**,而且**低估**,
   **"even in the large-sample limit"** —— **加試次救不了。**
   GRT 從來沒有引進這個結果(五份 GRT 主要來源的 `stimulus variability` 關鍵詞命中全部為 0)。

3. **實證上,「1 個 token → 4 個 token」是最傷的那一步。**
   [[uchanski1998]]:辨別力 **"substantially reduced by an increase in the number of tokens
   from 1 to 4, but ... little further reduction when the number of tokens increases to 16."**
   ⚠️ Silbert (2012) 用的正是**每類 4 個**。

4. **但 token 變異與 [[決策脈絡_統計方法]] §3 的 intrusion 是完全不同型的污染。**
   本地模擬(§4.2):intrusion **製造**假的 ρ;token 變異**只衰減** ρ,
   而且衰減量精確等於 ρ/√(1+s²) —— **它不會製造假陽性,但它會直接壓縮 d′ 與 β。**

5. **⚠️ 一個推翻性的本地實測:專案現在根本沒有自然 token。**
   `be.wav` / `pe.wav` **與 espeak-ng 的輸出逐取樣點完全相同**(§5.1)。
   整份 [[natural-vs-synthetic-speech]] 與 [[決策脈絡_聽覺維度]] 稱之為
   「自然 token + 噪音」的路線,**在實作上是「規則式共振峰合成 + 噪音」**。
   **這使得「多 token vs 單 token」的排序問題,暫時不是最緊急的問題。**

6. **三個選項的排序:合成 > 多個自然 token > 單一自然 token。**
   ⚠️ **這修正了本文初稿**(初稿把單一自然 token 排第二)。
   決定性的不是變異大小,而是 [[clark1973]] 的判準:
   **單一刺激設計只有在「假設本身對單一個案成立」時才合法。**
   合成能把假設寫成點假設(VOT = X、F1/F0 = Y);
   **單一自然錄音的「點」是「這段錄音剛好長什麼樣」—— 寫不下來,
   所以它兩種假設都撐不起來**,而它唯一的優點(β 乾淨)換來的是
   一個不可移除、不可量化的固定偏誤(§7.1、§7.2)。
   而本文 §4.2 的模擬正好支持這個排序:**多 token 的污染只衰減、不製造假陽性**,
   固定偏誤沒有這個保護。
   ⚠️ 這個排序**與 [[natural-vs-synthetic-speech]] §6.1 的建議衝突**(§8),
   而且第一名**與 Clark 一系文獻本身的主流結論相反**(§7.1)。**兩處都明講。**

7. ⭐⭐ **框架本身可能是錯的:還有第四個選項** —— **多對配對的合成刺激**(§10.1)。
   它同時滿足配對條件、刺激數要求、防漏洞理由,**而且不需要退守成點假設**。
   「多 token vs 單 token vs 合成」把「合成」與「多刺激」當成互斥,那是框架的錯。

---

## 1. 先把問題改寫兩次

研究者的原問題:**「token 變異會不會加進 GRT 估到的知覺變異?」**

### 1.1 第一次改寫:GRT 的知覺分布**在定義上**就吃下刺激變異

[[ashby2000]] 原文(Ashby 本人):
> "Over trials, however, **stimulus and perceptual noise** are assumed to induce variability
> in the percept associated with every specific stimulus"

> "**Because of stimulus and neural noise**, x*ᵢ* is assumed to be a random vector that
> varies across trials."

[[silbert2012]] §II.A 原文(Silbert 的版本,清單不同):
> "it is assumed that the presentation of a stimulus produces a random perceptual effect due
> to **internal noise, external noise added to the stimulus, or both.**"

[[silbert-hawkins2016]] §1.1.1 p.95 原文(教學論文的表態):
> "Although there are multiple possible sources for random perceptual variability (e.g.,
> environmental and/or neural noise; Ashby & Lee, 1993), **the specific sources of perceptual
> variability are not (typically) modeled in GRT.**"

**三份來源的清單彼此不一致**(Ashby 寫 stimulus noise;Silbert 寫 external noise added to
the stimulus;教學論文寫 environmental/neural)。但三份的**結構相同**:知覺分布是一個
容器,裝進去的東西不再分開。

**→ 答案:會。而且不是「不小心」會 —— 是模型的設計如此。**

### 1.2 第二次改寫:框架已經放棄分離變異來源了

[[ashby-wenger-handbook]] 原文:
> "**perceptual and criterial noise are not separately identifiable** (Ashby & Maddox, 1993).
> Instead, **only the sum of the perceptual and criterial noise variances is estimable.**
> For this reason, it makes no difference whether we assume that the noise is perceptual or
> decisional (or some combination of the two)."

**GRT 連「知覺 vs 決策」這兩項都不打算分,而且明說「反正分不開,假設是哪一種都無所謂」。**

**→ 所以「換哪種刺激才能讓 β 變成純知覺雜訊」這個目標,在 GRT 裡達不到。**
(這一步是**我的推論**;原文只講知覺 vs 決策,沒有講刺激。)

### 1.3 改寫後的問題

> **不是**:哪種刺激讓 β 變純?
> **而是**:哪種刺激讓 β 這個「和」裡面的**非知覺項最小、最受控、對兩個類別最對稱**?

這個改寫看起來像退讓,其實是**把問題變得可回答了** —— 因為「小」「受控」「對稱」
三件事都可以逐項比較,而「純」不能。**本文其餘各節都在這三個軸上比。**

---

## 2. 形式後果:方向確定,而且加試次救不了

### 2.1 已發表的結果(在 SDT,不在 GRT)

[[rouder2007]] 摘要原文:
> "In practice, researchers aggregate data across items or participants or both. **The signal
> detection model is nonlinear; consequently, analysis with aggregated data is not
> consistent. In fact, mnemonic ability is underestimated, even in the large-sample limit.**
> We present two hierarchical Bayesian models that **simultaneously account for participant
> and item variability.**"

**逐項拆開它對 AVWM 說了什麼**:

| 摘要的話 | 對 AVWM 的意思 |
|---|---|
| "not consistent" | 併掉 token 的估計量**不收斂到真值** |
| "even in the large-sample limit" | **加試次救不了。**專案目前每刺激 96 次、Silbert 用 200 次 —— 這個討論在這裡沒有意義 |
| "**underestimated**" | 敏感度低估 ⇔ **有效知覺變異高估** ⇔ **β 被膨脹**。方向正是研究者擔心的那個 |
| 解方 = item 隨機效果 | **GRT 沒有任何模型這樣做**(§2.2) |

⚠️ **限定**:我**只讀到摘要**,沒讀推導;而且這是**再認記憶**的 SDT,不是 2×2 GRT。
**把它搬到 GRT 是我的外推。** 但摘要那三句話本身沒有歧義。

### 2.2 GRT 文獻確實沒有做過這件事 —— 這是查證出來的,不是猜的

subagent 對五份 GRT 主要來源做了全文關鍵詞檢索:
GRT-wIND([[soto2015]])、grtools 教學([[soto2017]], arXiv 1610.03207)、
GRT-wIND 可辨識性論文(arXiv 1606.05598)、GRT 教學([[silbert-hawkins2016]])、
[[ashby-wenger-handbook]]。

| 關鍵詞 | 命中 |
|---|---|
| `stimulus variability` | **五份全部 0** |
| `token` | **五份全部 0** |
| `exemplar` | 教學論文正文 0 |

**→ 「多 token 會膨脹估到的 perceptual variance」這個警告,GRT 文獻裡不存在。
直接回答研究者的問題 B6:沒有。**

而且**沒有任何 GRT 模型把 token 當隨機效果**:
- [[silbert2012]] 是唯一有真隨機效果的階層高斯 GRT,但那一層是**受試者**;
  token **明文併掉**(§IV.B.2:"Response counts were tallied by stimulus category,
  not by individual stimuli."),而且**所有邊際變異數固定為 1**。
- [[soto2015]] GRT-wIND 唯一能縮放變異數的參數是**注意力** κ_k、λ_k。
  ⚠️ 這對 AVWM 特別危險:**AVWM 的核心操弄就是注意力**
  ([[決策脈絡_統計方法]] 的 valid/invalid),刺激變異會倒進同一個參數。(我的推論。)

### 2.3 ⭐ Silbert 的模型結構讓污染「無處可見」

[[silbert2012]] §II.B 原文:
> "the mean of one perceptual distribution is fixed at (0, 0), and **all marginal variances
> are fixed at unity.**"

**→ 在他的模型裡,token 變異不可能表現為「某個變異數估大了」,因為變異數被釘死。
它只能表現為**平均數之間的距離被壓縮** —— 也就是 d′ 變小。**
(這一步是我的推論;Silbert 沒有做這個論證。)

**這與 [[rouder2007]] 的「敏感度被低估」是同一件事,只是換了個座標系。**

⚠️ **AVWM 與 Silbert 在這一點上不同**:AVWM 的適應程序估的 β 就是斜率
(≈ 1/σ_total),而且若正式分析要比較 valid/invalid 兩組的變異數比
([[決策脈絡_統計方法]] §5),那些變異數就**不是**固定的。
**所以 AVWM 比 Silbert 更暴露在這個問題下,不是更少。**

---

## 3. 自然語音的 token 變異有多大,以及它被測過的效果

### 3.0 ⭐ 量級:/p/ 的 token 變異**大於**聽者自己的知覺雜訊

這是研究者的問題 A1–A3,而且答案比預期嚴重。

**⚠️ 先講一個決定性的限定**:**沒有任何已發表研究報告「同一位語者重複唸同一個 CV 音節」
的 VOT SD。** [[theodore2009]] 是唯一用純重複設計(/pi/、/ti/、/ki/)的研究,
但**只報迴歸斜率與截距,不報 SD**(全文已確認)。
所有可得的語者內 SD 都涵蓋多個母音或詞脈絡,**因此都是上界,不是純 token 重複雜訊。**

**語者內 VOT SD**([[chodroff2017]] Table 1 / Table 6 的 "Range of Talker SDs" 欄,ms):

| | pʰ | b | 說明 |
|---|---|---|---|
| **孤立語**(24 位語者) | **12–27** | **2–8** | 涵蓋 10 個母音脈絡 × 5 block |
| **連續語**(Mixer 6,180 位語者) | **11–35** | **2–8** | |

**平均值**(唯一一筆已發表的):[[chodroff-bradshaw-livesay2023]] 用同一批孤立語資料重算,
**[tʰ]、[kʰ] 的 mean talker SD 都是 16 ms**;正文:
> "adult stop-specific standard deviations are typically **between 10 and 30 ms** for
> word-initial aspirated stops in isolated speech"

**跨語者對照**:[[theodore2009]] 同音節、語速配對的語者間 SD(**subagent 由印出值計算**)
/pi/ **18.3 ms**、/ki/ 13.7、/ti/ 9.9;[[chodroff2017]] 孤立語 talker 平均的 SD
/pʰ/ 27、/b/ 5(⚠️ 該欄有資料品質疑慮,見該卡)。

**[[kleinschmidt2019]] 對連續語音的判讀(原文)**:
> "cross-talker variation in voiceless word-initial stop VOT is **roughly half of
> within-category variation**: … **the mean standard deviation of /p/ is around 20 ms, while
> the standard deviation of the mean VOT of /p/ is less than 10 ms**"

**→ 在連續語音裡,同一位語者自己的 token 抖動比換一位語者還大。**
⚠️ 但在**孤立語**(AVWM 的層次)方向相反(語者間 27 > 語者內 ~19.5)。
**比值隨說話風格反轉,引用時務必標明。**

#### ⭐⭐ 與知覺尺度的對照 —— 這是回答問題 A3 的關鍵

**基準**:[[clayards2008]] —— 聽者在 VOT 軸上的**內在雜訊 σ ≈ 10.7 ms**
(subagent 用作者的式 (3) 獨立重建,與作者印出值吻合到 2% 以內);
**/b/–/p/ 辨識函數的 25–75% 過渡寬度 = 7.7 ms(窄輸入)到 13.6 ms(寬輸入)**;
**[[winn2020]] p. 855 的邊界位置 20–25 ms。**

**把語者內 SD 除以 10.7 ms(以下是我的算術)**:

| | 語者內 SD | s = SD/10.7 | 變異膨脹 √(1+s²) | **β 降至** | **ρ 衰減至** |
|---|---|---|---|---|---|
| **/b/**(2–8,取中點 5) | 5 ms | 0.47 | 1.10× | **91%** | 91% |
| **/pʰ/**(12–27,取中點 19.5) | 19.5 ms | **1.82** | **2.08×** | **48%** | **48%** |

**→ 三個結論:**

1. **問題 A3 的答案:不可忽略,而且是同一個數量級或更大。**
   /pʰ/ 的語者內 SD(12–27 ms)**大於**聽者的內在雜訊(10.7 ms),
   也**大於**整個 25–75% 過渡寬度(7.7–13.6 ms),
   甚至**與整個邊界位置(20–25 ms)相當**。
2. **用多個自然 /p/ token,聽覺維度的有效變異會超過兩倍,β 掉到不到一半。**
3. ⭐ **而且嚴重不對稱:/pʰ/ 的 token SD 是 /b/ 的 3–4 倍。**
   這正是 §4.3 模擬的那個危險情形。

⚠️ **這個換算有三層假設**:(a) 10.7 ms 適用於 AVWM 的受試者與 SNR 條件;
(b) 語者內 SD 是上界不是純重複雜訊;(c) token 位移與知覺雜訊獨立可加。
**所以上表是量級推估,不是定量預測。但即使把 /pʰ/ 的 SD 砍半到 10 ms,
s 仍有 0.93,β 仍降到 73%。結論的方向不會因為這些假設而反轉。**

#### 其他聲學維度的 token 變異(相對不重要)

| 維度 | 語者內 SD | 量測雜訊底線 | 判斷 |
|---|---|---|---|
| **F1** | ≈ 24.6 Hz([[heald-nusbaum2015]] 中位數) | 11.7 Hz([[hillenbrand1995]]) | **約一半是分析雜訊**;粗估 ≈ 0.44 ms 的 VOT 等值 → **小項** |
| **F2** | ≈ 57.8 Hz | 25.2 Hz | 同上 |
| **F0** | ≈ 5.6 Hz | 1.7 Hz | 小項 |
| **時長** | CV ≈ 0.09–0.10,成人 ≈ 21 ms(Munson 2004,⚠️ 二手未建卡) | 6.9 ms | ⚠️ 值得注意 —— 與邊界寬度同量級 |
| **振幅 / 強度** | ⛔ **查無任何來源** | — | 文獻空白 |

**→ VOT 本身的 token 抖動是主要問題;共振峰是小項。**
⚠️ 但 [[sommers1994]] 的原則提醒:重要的不是物理變異量,是**該維度對 /b/–/p/ 判斷相不相關**
—— 而 F1 起始**是**相關的次要線索([[winn2020]])。**小,但不是零。**

### 3.1 單一 token vs 多 token 真的被測過嗎?

這是研究者的問題 A4。**答案是:有,但極少,而且直到 2023 年作者們仍認為這是開放問題。**

### 3.2 文獻缺口有多大 —— 用一篇 2023 年的回顧當證據

[[luthra2023]] 全文原文,在列舉 within-talker token 變異研究時:
> "within-talker token variability (**Drown & Theodore, 2020; Kapadia et al., 2023;
> Uchanski & Braida, 1998**)"

**總共三筆,其中一筆(Drown & Theodore 2020, JASA 148, 2504)是會議摘要,不是完整論文。**

[[kapadia2023]] 自己的說法:
> "In this literature, '**high variability**' is almost always implemented using stimuli
> produced by multiple different talkers, as opposed to any other kind of variability, such
> as **multiple tokens from a single talker** ..."

> "within-talker phonetic variation is a less well-understood source of variability in
> speech, and **it is unknown how processing costs from within-talker variation compare to
> those from between-talker variation.**"

### 3.3 ⭐ [[uchanski1998]] —— 唯一把 token 數當自變項的研究

摘要原文:
> "**Experimental results indicate that this ability is substantially reduced by an increase
> in the number of tokens from 1 to 4, but that there is little further reduction when the
> number of tokens increases to 16.**"

**兩個對 AVWM 直接有用的事實**:
1. **1 → 4 是最傷的那一步。**⚠️ Silbert (2012) 用的正是**每類 4 個**。
2. **4 → 16 幾乎不再降。**「多用幾個沒差」與「用很多比 4 個更糟」**兩種直覺都錯**。

⚠️ **同一份摘要的最後一句往反方向拉,必須並陳**:
> "**The effectiveness of the cues used in the latter case is limited more by internal noise
> than by the variability of the cues themselves.**"

**這是對「token 變異膨脹 β」最直接的反證** —— 作者認為多 token 情境下的限制主要仍是
內在雜訊。⚠️ **但這是一句摘要結論,我讀不到支持它的資料;而且它可能只是一個**量級**
主張(在他們測到的變異量下內在雜訊仍佔多數),不是**性質**主張。全文未取得前不可當定論。**

**還有一句被低估的話**:單 token 情境下聽者用 "a multiplicity of cues",
多 token 情境下用 "a smaller set"。
**→ token 數不只改變雜訊量,還改變受試者用哪些線索。**
對 GRT 這是嚴重的:GRT 的知覺維度是相對於實際被使用的線索定義的
([[silbert-hawkins2016]] 的建模慣例)。**換 token 數 = 換掉被估的維度。**
(這一步推論是我做的。)

### 3.4 [[kapadia2023]] —— 正確率沒事,RT 有事

2×2×2 因子設計,within-talker token 變異是明確因子(1 個 exemplar vs 8 個)。

| 情境 | ΔRT | 統計 |
|---|---|---|
| **單一語者、單一對比**(最乾淨那格) | **39.7 ms** | t = 3.128, p < 0.005 * |
| 跨語者對照 | 48.3 ms | t = 3.816, p < 0.001 * |

**⭐ 但正確率**:within-talker β = 0.021, z = 0.300, **p = 0.764(n.s.)**;
跨語者**有**效果(z = 2.007, p = 0.045 *)。摘要原文:
> "**Between-talker variability affected both word-identification accuracy and response time,
> but within-talker variability affected only response time.**"

**→ 這對 AVWM 是好消息:GRT 的依變項是混淆矩陣,不是 RT。**

⚠️ **三個必須並陳的但書**:
1. **「沒抓到」不等於「沒有」。** 24 人、無噪音、天花板附近的詞辨識,檢力有限;
   AVWM 刻意把難度壓到 ~80%,那正是正確率對變異最敏感的區段。(我的推論。)
2. **那 8 個 exemplar 不是天真重複** —— 是刻意誘發的 3 音高 × 2 時長 + 2 語調輪廓。
   **這是自然抖動的上限,不是下限。**
3. 詞辨識,不是 CV 音節;不是 GRT。

### 3.5 ⭐ 只有「語音上相關」的維度變異才收費

[[sommers1994]](within-talker 操弄):

| 變異來源 | 結果 |
|---|---|
| **語速**(改變時間結構 → 與 VOT 相關) | F(1,88) = 28.83, p < 0.005 **有害** |
| **整體振幅**(不改變任何音段線索) | F(1,58) = 0.036, p > 0.1 **無效果** |

原文:
> "**Trial-to-trial variations in overall amplitude did not produce significant decrements in
> identification performance.**"

**→ 這給了一個可操作的篩選原則(我的推論,原文沒這樣說):
token 之間若只在「與 /b/–/p/ 判斷無關」的維度上不同,代價可能接近零;
若在 VOT、F1 起始、burst 頻譜上不同,代價就直接進到聽覺維度的知覺變異裡。**

⚠️ **一個對本專案的直接後果**:`snr_audio.py` 的 `TARGET_RMS` 音量對齊,
處理的正好是那個**零代價**的維度。它是必要的(避免音量變成線索),
但**它不能被當成「已經控制了 token 差異」的證據**。

### 3.6 ⚠️ 一個會反轉全部推論的混淆

[[magnuson2007]] 摘要原文:
> "Listeners **expecting to hear 2 different talkers** differing only slightly in average
> pitch **showed performance costs typical of adjusting to talker variability**, whereas
> listeners hearing **the same materials** but expecting a single talker or given no special
> instructions **did not show these performance costs.**"

**同樣的聲學,換指導語,代價有無之別。**

**→ 若「變異代價」有一大部分是期待 / 注意力 / 監控負荷,它落腳的地方
不是知覺分布的變異數,而是決策與注意力參數。**

**這對 GRT 比「β 被膨脹」更糟**(我的推論):GRT 的標準做法是**假設
decisional separability**([[silbert2012]] §II.A.3 明文),
**一個被污染的決策參數會違反模型的核心假設,而不只是讓某個估計值偏大。**
這與 [[決策脈絡_統計方法]] §3 的 intrusion 論證是同一類問題(模型誤設)。

---

## 4. 本地模擬:token 變異在 2×2 GRT 裡到底做了什麼

**⚠️ 以下全部是本地模擬,不是文獻。**腳本與可重現參數見本節末。

**模型**:x = 顏色知覺維度,y = 聽覺知覺維度。四個刺激,真實知覺分布為二元常態。
每個聽覺層次的知覺效果 = 知覺雜訊 + **token 位移**(4 個等權 token,在 y 軸上以
常態分位數配置,SD = s,單位是知覺 SD)。
**擬合模型採用與 [[silbert2012]] §II.B 相同的可辨識性約束**:
所有邊際變異數固定為 1、一個平均數固定在 (0,0)、假設 decisional separability。
12 個自由參數 = 12 個資料自由度,恰好可辨識。

### 4.1 token 變異精確地衰減 ρ,而且衰減量有封閉形式

真實 ρ = 0.5,兩個維度真實分離度各 2.0 知覺 SD:

| token SD s | 變異中 token 佔比 f = s²/(1+s²) | **ρ̂(擬合)** | 解析預測 0.5/√(1+s²) | 邊際 d′(聽覺) |
|---|---|---|---|---|
| 0.00 | 0.000 | 0.5000 | 0.5000 | 2.0000 |
| 0.20 | 0.038 | 0.4903 | 0.4903 | 1.9608 |
| 0.30 | 0.083 | 0.4791 | 0.4789 | 1.9141 |
| 0.40 | 0.138 | 0.4646 | 0.4642 | 1.8526 |
| 0.50 | 0.200 | 0.4478 | 0.4472 | 1.7794 |
| 0.70 | 0.329 | 0.4097 | 0.4096 | 1.6111 |

**擬合值與解析預測吻合到小數第三、四位。**

**解析推導(精確,不需模擬)**:令知覺效果 = P + T,T 是與 P 獨立的 token 位移,
且只作用在聽覺維度。則
$$\Sigma_{\text{obs}} = \Sigma_P + \Sigma_T,\qquad
\hat\rho = \frac{\text{Cov}(x,y)}{\sigma_x\sqrt{\sigma_y^2+\sigma_T^2}}
= \frac{\rho_{\text{true}}}{\sqrt{1+s^2}}$$
因為 T 只進到 y 的變異數,**不進到共變數**。

**三個後果**:
1. **β(= 1/σ_total)被壓縮的倍數是 1/√(1+s²)** —— 這正是研究者說的「β 不再純」,
   而且量化了。
2. **ρ 被**衰減**,不是被扭曲。**
3. **d′ 同比例縮小** —— 但**適應程序會補償**它(把 SNR 調高),所以**正確率看不出來**。
   **污染是隱形的。**(我的推論。)

### 4.2 ⭐ 與 intrusion 的關鍵差異:token 變異**不製造**假的 ρ

真實 ρ = 0,只加 token 變異:

| token SD s | **max\|ρ̂\|** | 邊際 d′(聽覺) | 邊際 d′(顏色) |
|---|---|---|---|
| 0.00 | **0.00000** | 2.0000 / 2.0000 | 2.0000 / 2.0000 |
| 0.30 | **0.00000** | 1.9141 / 1.9141 | 2.0000 / 2.0000 |
| 0.50 | **0.00000** | 1.7794 / 1.7794 | 2.0000 / 2.0000 |
| 1.00 | **0.00000** | 1.3463 / 1.3463 | 2.0000 / 2.0000 |
| 1.50 | **0.00000** | 0.9862 / 0.9862 | 2.0000 / 2.0000 |

**即使 token SD 大到 1.5 個知覺 SD(聽覺 d′ 從 2.0 掉到 0.99),ρ̂ 仍然精確為 0。**
而且**顏色維度的 d′ 完全不受影響**,兩個顏色層次的聽覺 d′ 也**完全相等** ——
**不會製造出假的知覺可分離性違反。**

**解析論證(不需模擬即成立)**:若 token 位移只作用在聽覺維度、且與顏色層次無關
(隨機配對),則它**不改變共變數**,因此在真實 ρ = 0 時 Cov 仍為 0,
**不可能製造出非零的 ρ**。模擬只是確認 4 點離散混合也不會經由非高斯性洩漏出來。

**對照 [[決策脈絡_統計方法]] §3**:
```
intrusion 10%,真實 rho=0  →  Delta_SI = +0.01722  ← 憑空製造出等同 rho=0.5 的訊號
token 變異,真實 rho=0     →  rho_hat 保持 0        ← 只衰減,不製造
```

**→ 兩種污染是不同型的:**

| | intrusion | token 變異 |
|---|---|---|
| 機制 | **模型誤設**(模型裡沒有「報告了別的 item」這個參數) | **變異可加**(模型裡有變異數這個容器) |
| 對 ρ | **製造假的**,方向不可預測 | **只衰減**,方向確定、量有封閉形式 |
| 對 β / d′ | —— | **直接膨脹 β / 壓縮 d′** |
| 假陽性風險 | **高** | **無**(偏向虛無) |
| 可否事後還原 | 可(靠平衡的 relation 估 π) | **可,但需要知道 s** —— 而 s 需要逐 token 聲學量測 |

**這個對照是本文最重要的單一結論**:研究者擔心的污染是**真的**,但它**不會製造假陽性**,
它**降低檢力並直接偏誤 β**。若研究目標是「量出 β 與 ρ 的值」(而不是「檢定 ρ≠0」),
**這正是最糟的那一種**,因為偏誤直接落在要報告的量上。

### 4.3 ⭐ 不對稱的 token 變異:偏誤落在**決策界線**上

**這個情形不是假設 —— §3.0 已經確認它是真的**:語者內 VOT SD
**/pʰ/ 12–27 ms vs /b/ 2–8 ms,相差 3–4 倍**([[chodroff2017]])。

模擬(真實 ρ = 0,真實決策界線在兩個平均數的正中間 cy = 1.0):

| SD(b) | SD(p) | 邊際 d′(聽覺) | 邊際 d′(顏色) | max\|ρ̂\| | 擬合的聽覺平均數 | **擬合 cy** | **cy − 中點** |
|---|---|---|---|---|---|---|---|
| 0.00 | 0.00 | 2.000 / 2.000 | 2.000 / 2.000 | 0.0000 | 0 → 2.000 | 1.000 | **0.000** |
| 0.20 | 0.60 | 1.829 / 1.829 | 2.000 / 2.000 | 0.0000 | 0 → 1.829 | 0.980 | **+0.066** |
| 0.20 | 1.00 | 1.654 / 1.654 | 2.000 / 2.000 | 0.0000 | 0 → 1.654 | 0.980 | **+0.153** |
| 0.30 | 1.20 | 1.550 / 1.550 | 2.000 / 2.000 | 0.0000 | 0 → 1.550 | 0.957 | **+0.182** |

**三個發現**:

1. **ρ̂ 仍然精確為 0,顏色維度仍然完全乾淨。** 不對稱**也不會**製造假的知覺獨立性違反。
2. **兩個顏色層次的聽覺 d′ 完全相等** → **也不會製造假的知覺可分離性違反。**
3. ⭐ **但決策界線被推移了。** 真實界線在中點,擬合出來的 cy 卻高於中點 **0.07–0.18 個
   知覺 SD**,而且**位移量隨不對稱程度單調增加**,方向**朝向變異較大的那個類別**。

**→ 這是本次模擬最有價值的發現:不對稱的 token 變異偽裝成**反應偏差**(response bias),
不是偽裝成知覺結構。**

**為什麼這特別麻煩(我的推論)**:
- GRT 的標準做法是**假設 decisional separability** 並把界線位置當成**決策**參數解讀
  ([[silbert2012]] §II.A.3:"decision-making is at least partially under the control of the
  listener, whereas perception is not")。
- **一個由刺激製作造成的界線位移,會被解讀成受試者的反應策略。**
- 而 AVWM 的核心比較是 valid vs invalid([[決策脈絡_統計方法]])——
  **注意力操弄本來就預期會移動決策界線。刺激造成的位移會與它混在一起。**

⚠️ 位移量(0.07–0.18 SD)在等變異模型下不算大,而且**這個模擬把變異數釘死在 1**;
若讓變異數自由,吸收方式會不同(可能改為變異數不等,界線不移)。**沒有測過。**

### 4.4 模擬的限制

- 假設 token 位移只在**一個**維度(聽覺)上,且各 token 等機率、與顏色層次獨立配對。
  真實情況下 token 也會在其他聲學維度上動,可能映射到多個知覺維度。
- 假設擬合模型的變異數固定為 1(Silbert 的約束)。若讓變異數自由,吸收方式會不同。
- 未模擬**有限試次**的取樣變異。⚠️ 真實實驗中 token 與顏色的配對只是**近似**平衡,
  這會造成**過度離散**(overdispersion),使假設多項式抽樣的適配度檢定 Type I error 上升。
  **這一項我沒有模擬,但方向明確。**(我的推論。)
- 腳本:`token_var_sim2.py`(scratchpad,未進版控)。隨機種子 20260812。

---

## 5. 專案現況:兩個本地實測

### 5.1 ⛔ `be.wav` / `pe.wav` **不是自然錄音,是 espeak-ng 合成音**

**這是本次回顧最重要的單一發現,而且它推翻的是專案文件的一個基本前提。**

**證據(完全可重現)**:
```
espeak-ng -v en "[[b'i:]]" -w rb.wav  →  與 be.wav 逐取樣點比對:max abs diff = 0.0,完全相同
espeak-ng -v en "[[p'i:]]" -w rp.wav  →  與 pe.wav 逐取樣點比對:max abs diff = 0.0,完全相同
espeak-ng -v en `` [[b3:]] ``             →  13142 frames,等於 b3.wav 的長度
```
- 兩檔皆 22050 Hz 單聲道 —— espeak-ng 的預設輸出格式
- `snr_audio.py:35-38` 的 `SPEECH_FILES` **每類只有一個檔案** → **token 變異已經是 0**
- `stimuli/T01–T12_*.wav` 是舊 VAWM 的 **MBROLA** 合成(`GetAudioStim.py` 的
  `make_pho` / `synthesize`);`talker_info.csv` 的 12 位「語者」是 us1/us2/us3
  三個 diphone 庫 × pitch ratio,**不是 12 位真人**

**→ 三個後果**:

1. **[[natural-vs-synthetic-speech]] 與 [[決策脈絡_聽覺維度]] 通篇稱 SNR 路線為
   「自然 token + 噪音」,在實作層次上不成立。**
2. **[[silbert2012]] 的模型假設論證目前完全沒有被實作滿足。** espeak-ng 是**規則式**
   共振峰合成 —— 它的「相關聲學維度」由合成器作者預先決定,正是 Silbert 說要避開的
   那種「強假設」。**而且比 KlattGrid 更糟:KlattGrid 至少是研究者自己控制參數。**
3. **本題(多 token vs 單 token)在專案現況下暫時不是最緊急的問題** ——
   現況已經是「單一 token」,只是那個 token 的來源錯了。

### 5.2 本地量測:兩個 token 之間有多條線索同時在動

**本地實測(2026-08-12,自寫的自相關 F0 追蹤器,20 ms 窗 / 5 ms hop / 週期性門檻 0.45)**:

| | F0 起始 | F0 結束 | 降幅 | 全距 | SD | 有聲段長 |
|---|---|---|---|---|---|---|
| `be.wav` | 99.8 Hz | 77.6 Hz | 22.1 Hz | 24.4 | 7.8 | 244.4 ms |
| `pe.wav` | 102.6 Hz | 76.3 Hz | 26.3 Hz | 26.3 | 7.8 | 194.6 ms |

兩 token 之間:起始 F0 差 **−2.8 Hz**、對齊有聲起點後**逐幀最大 F0 差 9.5 Hz**、
**有聲段長度差 49.9 ms**。

⚠️ **F0 追蹤器的參數會影響數字**:另一次用不同窗長的量測得到起始 F0 差 −5.0 Hz、
逐幀最大差 9.6 Hz、有聲段長度差 60 ms。**量級一致,個位數不可引用。**

先前已量到並記錄的:**聲學起始差 35.9 ms**、有聲段位準差 **1.6 dB**
(見 [[consonant-pair-choice]] §7.2、§8.4)。

**⚠️ 這些不全是「瑕疵」,論證的正確形式不是「自然音品質差」:**
- 母音起始 F0 較高**本來就是**無聲塞音的次要線索 —— `pe` 確實較高(+2.8 Hz),
  **方向正確**
- 有聲段長度差**部分是** VOT 差異的必然結果

**正確的論證形式是:多條線索同時在動,無法把效果歸因到 voicing 這一個維度。**
這正是 [[silbert-hawkins2016]] 那句建模慣例的另一面 ——
模型會報告「聽覺維度」,但那條維度上實際承載了 VOT、F0 輪廓、時長、位準的**混合**。

**而且這還是 espeak 輸出。田野錄音的未受控共變只會更多。**

---

## 6. running noise:它**不是**免費的,但它有一個自然 token 沒有的優勢

這是研究者的問題 C10。**初稿的答案(「running noise 比 token 變異好處理」)在查證後
必須大幅下修 —— 但下修之後剩下的那一條優勢,反而是最關鍵的一條。**

`snr_audio.py` 的 `speech_shaped_noise()` 每次呼叫產生新樣本,
原始碼註解的理由是「否則受試者會學會噪音圖樣」。

### 6.1 它在 GRT 模型裡是**明文合法**的變異來源

[[silbert2012]] §II.A 的來源清單裡,第二項就是它:
> "internal noise, **external noise added to the stimulus**, or both"

**→ 外加噪音是 GRT 明文承認會進到知覺分布的東西;token 變異不在那份清單上。**
這是文獻事實,不是推論。

而且它有正式的可加分解 —— **聽覺領域**的版本是 [[buss2006]] Eq. (1):
> "**The value of σ can be decomposed into internal noise (σi) and external noise (σe),
> resulting in the equation d′ = Δ/√(σe² + σi²).**"

視覺領域的等價式見 [[ludosher1999]] Eq. (2)(3):**N² = N²ext + N²add**。

### 6.2 ⛔ 但三個查證結果推翻了「外加噪音是小而乾淨的擾動」

**(a) 外部噪音的變異與內部雜訊**量級相當**,不是小項。**

[[siegel-colburn1989]] 摘要原文:
> "**response probabilities and sensitivities vary significantly across noise waveforms**,
> indicating a **considerable external noise component** in subject response variability. …
> **For both NoSo and NoSπ, internal and external noise variance are of similar magnitude.**"

跨研究收斂:內部 ≈ 0.75–3 倍外部([[neri2010]] 的大樣本估計是 **1.3 倍**;
Burgess & Colborne 1988 視覺是 0.75)。
**→ 換算成佔比,外部噪音佔總變異約 37–64%。**
**在 SNR 路線下,估到的「知覺變異」裡有三到六成根本不是知覺的。**
(這個換算是我做的。它同時給了 [[決策脈絡_統計方法]] §4 稀釋分析裡的 f 一個實測錨點。)

**(b) ⭐⭐ 噪音樣本本身就有 token 效應,而且是在**音素辨識**作業上量到的。**

[[osses-varnet2024]] —— 這是本次查證中最直接反駁「running noise 乾淨」的一篇,
而且它做的正是 AVWM 的作業。導論原文:
> "**token-specific effects are usually considered negligible by researchers in the case of
> stationary maskers**, probably because two tokens of a steady noise generated by the same
> statistical process are often considered as perceptually indistinguishable. **However,
> there is evidence that this is not generally true.**"

摘要原文:
> "**The effect of the noise fluctuations explained on average 8.1% of the participants
> responses in white noise, a proportion that increased up to 13.3% for noises with a larger
> amount of fluctuations.** … We argue that this **token-specific effect of noise is a form of
> informational masking.**"

**→ 「哪一段噪音被抽到」解釋了 8–13% 的音素反應。這不是捨入誤差。**

⚠️ 而且被歸類為 **informational masking** —— 其大小取決於噪音與目標的相似性。
**/b/ 與 /p/ 的頻譜—時間結構不同,所以它未必對兩個類別對稱。**(我的推論。)

**(c) frozen 噪音**顯著比較好偵測**,而且原因是記憶不是不確定性。**

[[pfafflin1968]] 摘要原文:
> "**Signal detectability was found to be significantly better when a single noise was present
> in a block of trials.** Introducing variability in the stimulus by **altering the number of
> different signal levels presented during a block of trials did not affect detection.** The
> results support the importance of **memory for the noise from trial to trial** in the
> detection process."

**→ running noise 確實增加了有效變異(代價是真的);但控制條件排除了「泛泛的刺激
不確定性」解釋 —— 效果特定於噪音波形的記憶。**

**而這反過來說明了為什麼 running noise 仍然是對的選擇**(我的推論):
frozen 的優勢**來自學習**。在一個跑數百試次的適應程序裡,受試者會持續學習那一段噪音,
**閾值會隨時間漂移** —— 對適應程序而言,可學習的優勢是有害的,因為它讓目標移動。

⚠️ 語音領域的量級補充:frozen vs fresh 的效果**集中在 informational masker(babble)**;
對穩態 SSN 而言閾值差 **< 0.5 dB** 且斜率相當(subagent 由摘要取得,⚠️ 未建卡)。
**AVWM 用 SSN,所以這一項的實際代價可能很小。**

### 6.3 剩下的那一條優勢,才是關鍵:**它可以被完整記錄**

回到 §1.3 的三個判準,誠實重評:

| 判準 | running noise | 自然 token 變異 |
|---|---|---|
| **量的大小** | ⛔ **不小** —— 佔總變異 37–64%([[siegel-colburn1989]]、[[neri2010]]);噪音樣本解釋 8–13% 的音素反應([[osses-varnet2024]]) | ⛔ 也不小 —— /pʰ/ 的 s ≈ 1.8,變異膨脹 2.08×(§3.0) |
| **是否受控 / 可描述** | ✅ **決定性優勢** —— [[ludosher1999]] 的推導明文用 "**experimenter-controlled**";而且**波形或 RNG 種子可以逐試次存下來**([[osses-varnet2024]] 存了 4000 段) | ⛔ 未量測、未報告;事後無法還原 |
| **對兩類別是否對稱** | ⚠️ **依構造對稱**(同一個噪音程序),但 informational masking 的成分**未必**對稱(我的推論) | ⛔ **依構造不對稱** —— /pʰ/ 的 token SD 是 /b/ 的 3–4 倍(§3.0) |
| **與訊號是否獨立** | ✅ 加性、獨立取樣 | ⛔ 不獨立 —— token 變異**就是**類別內結構 |

**→ 修正後的結論:running noise **不是**比 token 變異「小」或「乾淨」。
它的優勢只有一個,但那一個很重要 —— **它的分布是實驗者指定的,而且它可以被逐試次記錄。**
自然 token 的變異兩者皆非。**

**這與 §1.3 的改寫完全一致**:目標不是消滅非知覺變異(做不到),
而是讓它**受控且可描述**。

### 6.4 ⚠️ 一個實作項:**存 RNG 種子**,成本為零

double-pass(重播同一序列,用反應一致性分離內部/外部雜訊)**要求兩個 pass 之間
噪音完全相同**([[green1964]] 的原始方法),而 pass 之內要 running。

**→ 「running noise 用過即丟」永久放棄了估計內部雜訊、以及做反向相關(ACI)的可能。**
[[osses-varnet2024]] 把 4000 段噪音全存下來,正是為了這個。

**`snr_audio.py` 目前是 `rng = np.random.default_rng()`(無種子)。
改成逐試次指定並記錄種子,成本是零,價值是保留一整條分析路線。**(我的建議。)

### 6.5 一個更深的代價:噪音可能改變**處理策略**,不只是加難度

[[allard2014]] 原文:
> "**To avoid different processing strategies operating in absence of noise and in high noise,
> external noise should match, as much as possible, the characteristics of internal noise**"

> "**a contrast detection task in 0D noise is processed as a contrast discrimination task.**"

**→ 外部噪音典範的核心假設(noise-invariance)可能失效 —— 加噪音會改變被測量的東西。**

這與 [[winn2013]] 在語音領域的發現方向一致(噪音改變 VOT 與 F0 的**相對權重**),
只是 Allard 等人把它上升成一般命題。

**→ 所以「用噪音調難度」不是中性旋鈕。它與「把 VOT 往邊界靠」一樣會改變被測量的東西,
只是改變方式不同。**(這個並列是我的推論;沒有文獻做過這個比較。)

[[natural-vs-synthetic-speech]] §6.2 已處理過語音版本,本文不重複。


## 7. 三個選項的取捨表

**⚠️ 判準是「β 的純度」優先** —— 這是研究者指定的前提(實驗室操控優先、
生態效度非優先)。**若換掉這個前提,排序會變,見 §8。**

| | (a) 多個自然 token | (b) 單一自然 token | (c) 合成刺激 |
|---|---|---|---|
| **β 的純度** | ⛔ **最差**。token 變異直接加進 σ²,β 膨脹 1/√(1+s²) 倍(§4.1);[[rouder2007]] 說偏誤**不一致**、加試次救不了 | ✅ **within-category 變異 = 0**;但兩個 token 之間的未受控差異是**固定且與類別完全共線**的偏差(§7.1) | ✅ **within 為 0,而且 between 的差異正好就是你指定的那些**(§7.1) |
| **類化範圍** | ✅ 最廣(類別層次) | ⛔ 綁死在那兩個錄音上 | ⛔ 綁死在那組合成參數上,而且是**單線索**的 voicing(§7.2) |
| **Silbert 的模型假設論證** | ✅ 完整滿足 —— [[silbert2012]] §I.C.2 原文明說機制就是 "naturally produced, **and so naturally variable**" | ⚠️ **只滿足一半** —— 保住「單一 token 之內線索共變」,丟掉「跨 token 的變異」。⚠️ Silbert 的原句把兩者綁在一起,拆開的是我 | ⛔ 正是他要避開的「predetermined acoustic-phonetic dimensions」 |
| **實作成本** | ⛔ 要錄音、要逐 token 聲學量測(否則 s 未知、無法還原)、要平衡配對 | ✅ **最低** —— 錄一組、量一次、對齊起始與位準 | ⚠️ 中等 —— KlattGrid 可行且已驗證([[決策脈絡_聽覺維度]] 反轉 6:取樣點解析度),但參數要自己選、自己辯護 |
| **對 AGRT 雙極結構** | ⚠️ 若走 SNR 調難度則不符,需另開 QuestHandler | ⚠️ 同左 | ✅ 若走 ΔVOT 則直接可餵 AGRTHandler([[決策脈絡_聽覺維度]]) |
| **文獻直接證據** | [[uchanski1998]]:1→4 token 辨別力 "substantially reduced" | [[uchanski1998]] 的基準條件;[[kapadia2023]] 的 low-variability 條件 | [[logan1989]]:音節首子音上與自然**統計上無異** |
| **⭐ [[clark1973]] 的單一個案判準** | ✅ **不需要**退守點假設,可做類別層次主張(但需混合模型) | ⛔ **兩種假設都撐不起來** —— 集中趨勢假設 Clark 明說不行;點假設又寫不下來(§7.2) | ⚠️ **只能做點假設**,而且**寫得下來**(VOT = X、F1/F0 = Y) |
| **偏誤 vs 變異** | ⚠️ **變異**(§4.2 模擬:只衰減,**不製造假陽性**,顏色維度完全乾淨) | ⛔ **偏誤**(固定、與類別共線、不可量化) | ✅ 兩者皆無(within = 0,between 已知) |
| **統計檢力** | ⚠️ 若當隨機因子,4 個/條件 + 大效果 → 上限 **.41**([[westfall2014]]) | — (n=1,不適用) | ✅ 點假設下刺激非隨機因子,天花板不適用 |
| **綜合排序** | **第 2** | ⛔ **第 3(最差)** | ✅ **第 1** |

**⚠️ 這張表遺漏了一個選項。** 「合成/自然」與「單一/多個」被當成同一個軸,
但它們是**兩個獨立的軸**。**多對配對的合成刺激**(§10.1 第 6 條)在
「β 純度」「Clark 判準」「檢力」上**同時**優於上表三者。

### 7.1 ⭐ 選項 (b) 有一個容易被漏掉的問題:它**凍結**了 between-category 的混淆

**⚠️ 這一節修正了本文初稿的排序:單一自然 token 從第二名降到第三名(最差)。**

**修正的理由有三條,而且兩條來自本文自己的其他部分:**
1. §4.2 的模擬證明:多 token 的污染**只衰減、不製造假陽性**,而且顏色維度完全乾淨。
   **固定偏誤沒有這個保護** —— 它直接偏移平均數,而 d′ 就是平均數距離。
2. §7.2 的 [[clark1973]] 判準:單一**自然**錄音兩種假設都撐不起來。
3. **獨立佐證**:[[決策脈絡_聽覺維度]] 的分析(另一個 agent,不同路徑)得到**同樣的排序**。
   ⚠️ 兩份分析共用了本地實測資料,不算完全獨立;但推論路徑不同。

三個選項在**兩種**變異上的表現並不一樣:

| | within-category 變異 | **between-category 的未受控差異** |
|---|---|---|
| (a) 多 token | 有,膨脹 β | **會平均掉** —— 每個類別抽多個樣本,idiosyncrasy 趨於相消 |
| (b) 單一 token | **無**(β 乾淨) | ⛔ **固定且永久**,而且**與類別完全共線** —— 每個試次都帶著同一個偏差 |
| (c) 合成 | **無** | ✅ **between 的差異正好就是實驗者指定的那些** |

**具體到本專案(§5.2 的實測)**:`be.wav` 與 `pe.wav` 之間的 F0 輪廓差、有聲段長度差
49.9 ms、起始差 35.9 ms、位準差 1.6 dB —— **這些在單一 token 設計下不會被平均掉,
它們每一個試次都在,而且 100% 與「這是 b 還是 p」共線。**

**→ 選項 (b) 把一個**隨機**污染換成一個**系統性**污染。**
在統計上這是更糟的交換:隨機污染衰減效果、降低檢力(§4.2 已證明它不製造假陽性);
**系統性污染直接偏移平均數,而 GRT 的 d′ 就是平均數之間的距離。**

⚠️ **對齊可以移除已知的那幾項**(起始、位準,`snr_audio.py` 已做或待做,
見 [[consonant-pair-choice]] §8.4),**但只能移除你想到要量的那些**。
F0 輪廓、嗓音品質、共振峰軌跡、頻譜傾斜……清單沒有盡頭。
**「我對齊了 A 和 B」不蘊含「C 和 D 沒有差異」。**

**這個論證在文獻上有對應,而且比預期早得多。**

**[[brunswik1955]] p. 194** —— 他 1955 年就這樣稱呼單一刺激設計:
> "This constitutes **artificially induced perfect confounding**, and may be labeled
> '**tied-variables' design** or, in short, **tied design**."

而且他明說多加受試者沒用(p. 204):
> "**individual sample situations, no matter how lifelike, cannot answer the funtional [sic]
> problem** … **Only representative design can answer this problem.**"

**[[judd2012]] 討論段** —— 現代版:
> "when experimenters attempt to replicate effects **using the same experimental stimuli** …
> **it can never be clear whether a successful replication indicates a truly reliable
> treatment effect or merely a consistent bias in the set of experimental stimuli used.**"

**[[judd2012]] 的量級**:只對受試者做分析時 Type I error **平均 .317**、最壞 .616,
**而且加受試者會讓偏誤更大**。

### ⭐ [[clark1973]] 的判準比「固定 vs 隨機」細緻,而且它才是決定性的

Clark 的「單一個案法」一節(pp. 352–354)**沒有**說單一刺激一律不合法:
> "**The hypotheses of interest must be applicable to single cases.**"
> "**There is no single case imaginable that suffices to disconfirm the homograph hypothesis.
> So the method of single cases is simply not applicable to such 'central-tendency'
> hypotheses.**"

**→ 這個判準把 (b) 與 (c) 分開(以下是我的推論)**:
- **合成**的點假設 =「在 VOT = X、F1/F0 = Y 這個刺激上」→ **寫得下來,判準滿足**
- **單一自然錄音**的點 =「這段錄音剛好長什麼樣」→ **寫不下來**,只能退回集中趨勢假設

推導細節見 [[自然音vs合成音_理論推論]] §5.3。

### ⚠️⚠️ 但這支文獻的主流結論**與本文的排序相反**

| 反面 | 來源 |
|---|---|
| **合成路線正是 Brunswik 點名批判的做法** —— "the holding constant of a third variable" 造出 "pseudo-univariate design" | [[brunswik1955]] pp. 195–196 |
| **刺激少 → 檢力有天花板**:4 個/條件 + **大**效果 d = 0.8 → 上限僅 **.41**;要 .80 需 **≥16 個** | [[westfall2014]] p. 2032 |
| **主流建議是「多刺激 + 混合效果模型」**,即支持選項 (a) | [[baayen2008]]、[[barr2013]] |
| **配對設計的例外到不了 n = 1** —— [[raaijmakers1999]] 的推導需要「配對區塊的**母體**」 | [[raaijmakers1999]] p. 421 |

**→ 本文借用的只是這支文獻的**前半**(單一刺激 = 固定混淆),不是它的**結論**。
這是選擇性引用,必須明白標示。** 調和方式見 [[自然音vs合成音_理論推論]] §8。

### ⭐ 而且這支文獻從未進入 GRT —— 用引文網路量化過

| 事實 | 數字 |
|---|---|
| [[clark1973]] 被引總數 | **2,278** |
| 其中 *JASA* | **9(0.4%)** |
| **同時**引用 Clark 與 Ashby & Townsend (1986) 的著作 | **恰好 1 篇,且非 GRT 方法論文** |
| Silbert 引用 Ashby & Townsend / 引用 Clark | **16 / 0** |
| 全部引用者的引用脈絡掃描 `psychophysic\|signal detection\|d-prime\|threshold` | **0 命中** |

**唯一的橋是階層貝氏 SDT**([[rouder2007]]、[[decarlo2011]])——
⚠️ **[[decarlo2011]] 就發表在 GRT 的主場期刊 JMP**,但停在再認記憶。
**論證就在隔壁,沒有跨過那一步。**

⚠️ **方法但書**:以上依賴 OpenAlex/Crossref 索引;SDT 教科書的參考文獻不被索引。
**這是很強的證據,不是邏輯證明。**

⚠️ **[[silbert2018]]** 確實建了有語者/聽者隨機變異的多層 GRT,
但其 54 筆參考文獻中**沒有 Clark、Coleman 或 Judd/Westfall** ——
**做法從語音學獨立長出來了,論證沒有。**(該篇未讀,不可主張它處理了 token。)

### 7.2 選項 (c) 的誠實代價:它測到的是**單線索**的 voicing 知覺

若用 KlattGrid 把 F0 與 F1 完全固定、只動 VOT,**VOT 就成為唯一的 voicing 線索**。
自然聆聽時聽者是整合多線索的,而且 [[winn2013]] 顯示噪音還會改變 VOT / F0 的相對權重。

**→ 合成刺激測到的是「一個通道」的 voicing 知覺,不是完整的 voicing 知覺。**

在「操控優先、要最底層機制」的前提下,**這可能正是想要的**(隔離出一個通道),
但**必須明說這個限縮**:研究問題是「子音語音表徵與色彩的關聯」,
**單線索刺激探測到的表徵,比多線索的窄。**
論文的主張範圍要跟著縮:不是「voicing 表徵與顏色的關聯」,
而是「**沿 VOT 定義的 voicing 維度**與顏色的關聯」。

---

## 8. 這推翻 `natural-vs-synthetic-speech.md` 的建議嗎?**部分推翻,而且原因是前提不同**

**是的,有衝突,而且我明講。**

| | [[natural-vs-synthetic-speech]] §6.1 | 本文 §7 |
|---|---|---|
| **建議** | 走 SNR 路線(自然 token + 噪音) | **合成 > 多自然 token > 單一自然 token** |
| **隱含前提** | 未列出「生態效度非優先」;把 [[silbert2012]] 的模型假設論證當作最強的一條 | **明文以「實驗室操控優先、生態效度非優先」為前提** |
| **對 token 變異** | 只在 [[silbert2012]] 卡的限制欄提過一句「會影響 GRT 分布的解釋」,未展開 | **當成核心判準**,並量化(§4.1) |

**造成分歧的**單一**前提差異是:類化(generalization)的權重。**

- [[natural-vs-synthetic-speech]] 的論證鏈裡,「GRT 的維度解釋」之所以最要命,
  是因為它擔心**估到的維度不是聽者真正用的維度** —— 這個擔心**同時**服務於
  「參數要正確」與「結論要能類化」。
- 加上「生態效度非優先」之後,**兩者分家**:
  - 「參數要正確」→ 仍然成立,但它現在**偏好受控刺激**(§1.3 的三個判準)
  - 「結論要能類化」→ **降權**

**→ 同一條論證在兩個前提下指向相反方向。這不是誰算錯了,是判準換了。**

### 8.1 ⚠️ 但有一條**不因前提改變而失效**的論證,必須誠實保留

[[silbert-hawkins2016]] 的建模慣例:
> "The dimensions along which the perceptual distributions and decision bounds are defined
> are **modeled perceptual dimensions corresponding to the physical dimensions of the
> stimuli.**"

**這是模型結構,不是生態效度訴求。** 它說:你只給模型 VOT 一條軸,模型就只會報告
VOT 這條軸,**在結構上沒有辦法**告訴你受試者其實靠別的東西在判斷。

**這條論證在新前提下仍然成立**,而且 [[roark2019]] 用完全合成、參數正交的刺激
仍發現維度**不是知覺正交**,是獨立的第二個聲音。

**→ 所以本文的結論不是「合成沒有代價」,而是「在 β 純度這個判準上合成佔優,
而它的代價(§7.2 的單線索限縮)必須寫進論文的主張範圍」。**
詳細的推導見 [[自然音vs合成音_理論推論]]。

### 8.2 一個**兩份文件都同意**、而且更緊急的結論

**無論排序如何,`be.wav` / `pe.wav` 是 espeak-ng 輸出這件事(§5.1)在兩個前提下都是問題:**
- 生態效度前提下:它不自然
- 操控優先前提下:它的參數**不是實驗者控制的**

**→ 這是本次回顧唯一一條不依賴前提的行動項。**

---

## 9. 直接回答研究者的 13 個問題

| # | 問題 | 答案 |
|---|---|---|
| 1 | within-talker VOT SD 多少 ms? | **/pʰ/ 12–27、/b/ 2–8 ms**(孤立語,[[chodroff2017]] 的 "Range of Talker SDs" 欄);平均 16 ms([[chodroff-bradshaw-livesay2023]])。⚠️ **但沒有任何研究測過「重複唸同一音節」的 SD**,這些是上界([[theodore2009]]) |
| 2 | 跨語者變異多大? | [[chodroff2017]] 表列;辨識代價 6.7–21 個百分點([[mullennix1989]]) |
| 3 | 相對於 20–25 ms 邊界寬度是什麼量級? | ⛔ **不可忽略,同量級或更大**。/pʰ/ 的 12–27 ms **大於**聽者內在雜訊 10.7 ms([[clayards2008]])、**大於**整個 25–75% 過渡寬度 7.7–13.6 ms。/b/ 的 2–8 ms 則是小項。**兩者差 3–4 倍** |
| 4 | 有無單 token vs 多 token 的直接證據? | ✅ **有,但只有兩筆完整論文**:[[uchanski1998]](1→4 辨別力顯著下降)、[[kapadia2023]](RT 有、**正確率沒有**) |
| 5 | GRT 把刺激變異當模型內還是模型外? | **模型內,而且明文不分解來源**([[silbert-hawkins2016]]、[[ashby2000]]、[[ashby-wenger-handbook]]) |
| 6 | 有無「多 token 膨脹 perceptual variance」的警告? | ⛔ **GRT 文獻中沒有**(五份來源 `stimulus variability` 命中全 0)。**SDT 有**([[rouder2007]]) |
| 7 | 有無主張**應該**用多 token 的? | ✅ 有,[[silbert2012]] §IV.A:防止受試者鑽單一 token 的漏洞;§I.C.2:變異就是避開強假設的機制 |
| 8 | Silbert 有無討論 4 token 對估計的影響? | ⛔ **完全沒有**。全文通讀 + 關鍵詞計數確認([[silbert2012]] 卡的專節)。他的 limitation 是**類化**不是估計 |
| 9 | 單一自然 token 可行嗎?有人做過嗎? | [[uchanski1998]] 與 [[kapadia2023]] 的**基準條件**就是。⚠️ 但 §7.1:它**凍結**了 between-category 混淆 |
| 10 | running noise 的變異怎麼算?比 token 變異好處理嗎? | GRT **明文承認**外加噪音進到知覺分布([[silbert2012]] §II.A),形式上是 σe²([[buss2006]])。**但它不小也不乾淨** —— 佔總變異 37–64%([[siegel-colburn1989]]、[[neri2010]]),噪音樣本本身解釋 8–13% 的音素反應([[osses-varnet2024]])。**唯一的真優勢是它可被指定與記錄**(§6.3) |
| 11 | 有沒有第三條路? | 見 §10.1 |
| 12 | 三個選項怎麼排? | **合成 > 多自然 token > 單一自然 token**(⚠️ 已修正初稿);推導見 [[自然音vs合成音_理論推論]] §8。**但框架本身漏了第四個選項**(§10.1 第 6 條) |
| 13 | 與現有建議衝突嗎? | ✅ **衝突,§8 明講**。分歧來自**類化的權重**這一個前提 |

---

## 10. 缺口、待查、與第三條路

### 10.1 第三條路(問題 11)

1. **⭐ 把 token 當隨機效果放進階層 GRT。** [[rouder2007]] 的解方。
   **GRT 文獻裡沒有人做過** —— 這是可以宣稱的空白。
   代價:模型參數變多,而 2×2 GRT 在個體層次本來就飽和([[silbert2012]] 自陳)。
2. **多 token + 逐 token 聲學量測當共變量。** 保住類化,又能把 s 估出來、事後校正
   (結構同 [[決策脈絡_統計方法]] §3 用平衡的 relation 還原 intrusion)。
3. **自然錄音 → 選一個 token → 用它當合成的目標**(analysis-by-synthesis)。
   保住「這個 token 的線索共變」,同時取得參數控制。
4. **多 token 但只沿「語音上不相關」的維度變異**(整體音量、絕對 F0 水平) ——
   [[sommers1994]] 說這些是零代價的。**可以擋掉「受試者記住單一 token」的批評,
   而不付 β 的代價。**⚠️ 這是我從 [[sommers1994]] 推得的設計,沒有人做過。
5. **雙 pass 設計**:同一個 token + 同一個噪音樣本重複呈現,用反應一致性分離
   內部/外部雜訊([[green1964]] 的原始方法)。
   **要求:必須逐試次記錄噪音波形或 RNG 種子**([[osses-varnet2024]] 存了 4000 段)。
   `snr_audio.py` 目前無種子、用過即丟 —— **改成記錄種子,成本為零。**
6. ⭐⭐ **多對配對的合成刺激**(本次查證浮現的第四條路,三選項的框架看不到它)。
   若干組(8–16)配對合成刺激,**組內只有 VOT 不同**,**組間只在語音上不相關的維度**
   變動(整體 F0、時長、音量)。
   它同時滿足:[[raaijmakers1999]] 的配對條件(而且 q > 1,有區塊母體)、
   [[westfall2014]] 的刺激數要求、[[silbert2012]] §IV.A 的防漏洞理由、
   [[sommers1994]] 的不相關維度原則,**而且不需要退守成點假設**。
   ⚠️ 沒有人做過;GRT 模型層次沒有現成解。詳見 [[自然音vs合成音_理論推論]] §9.2。

**⚠️ 選項 4 值得特別注意** —— 它同時滿足 Silbert 的防漏洞理由([[silbert2012]] §IV.A
明說那才是他用 4 個 token 的目的)與 β 的純度要求。**這可能是最好的折衷。**

### 10.2 明確的文獻空白(不是我沒找到)

- **GRT 從未討論刺激變異對參數估計的影響。** 五份主要來源關鍵詞命中全 0。
- **[[rouder2007]] 的 item 聚合偏誤結果從未被引進 GRT。**
- **within-talker token 變異的完整論文只有兩筆**([[luthra2023]] 點名三筆,一筆是會議摘要)。
- **沒有人在 GRT 或心理物理裡比較過「單一 token 的固定混淆」與「多 token 的隨機變異」。**
  該論證在**方法學統計**裡存在且成熟([[brunswik1955]]、[[clark1973]]、[[judd2012]]、
  [[westfall2014]]),在 **SDT** 裡有橋([[rouder2007]]、[[decarlo2011]]),
  **但從未跨進 GRT**(引文網路已量化,見 §7.1)。

### 10.3 待補查證(依重要性)

1. ~~within-talker VOT / 共振峰 / 時長的 SD 數字~~ —— **已完成**(§3.0)。**剩下的真空白**:同一音節重複產出的 VOT SD 從未被報告([[theodore2009]]);**振幅/強度的語者內 SD 查無任何來源**
2. ~~刺激當固定 vs 隨機效果的方法學文獻~~ —— **已完成**(§7.1)。
   **剩下未取得**:Brunswik (1956) 專書(Archive.org 借閱受限);
   Wells & Windschitl (1999) *PSPB* 25(9), 1115–1125, doi 10.1177/01461672992512005
   (書目已核實,全文未取得,是這個 crux 最後一條未讀線索);
   [[decarlo2011]] 全文(取不到可引用的句子)
3. ~~frozen vs running noise、內外雜訊分解~~ —— **已完成**,結果推翻了初稿的 §6(見 §6.2)
4. **[[silbert2018]]** —— 標題就是 "talker-based sources of variability",
   本題最可能被正面處理的一篇,**未讀**
5. **Ashby & Lee (1993)** "Perceptual Variability as a Fundamental Axiom of Perceptual
   Science", doi 10.1016/S0166-4115(08)62778-8 —— GRT 談變異來源的正典,
   ScienceDirect 有 captcha,**未取得**。若有 Elsevier 權限,這是最該補的一筆
6. **[[uchanski1998]] 全文** —— 摘要最後一句(「限制主要來自內在雜訊」)是本文最強的反證,
   但我讀不到支持它的資料
7. **Ashby & Townsend (1986)** "Varieties of perceptual independence",
   *Psychological Review* **93(2), 154–179**, doi 10.1037/0033-295X.93.2.154 ——
   **全文未取得**(Semantic Scholar 標 CLOSED;ResearchGate 403;ScienceDirect captcha;
   ⚠️ PubMed 該筆**沒有摘要**)。**書目更正:是 93(2),不是 93(3)。**

---

**相關卡片**:[[silbert2012]] · [[silbert2014]] · [[silbert2018]] · [[silbert-hawkins2016]] ·
[[soto2015]] · [[soto2017]] · [[ashby2000]] · [[ashby-wenger-handbook]] · [[rouder2007]] ·
[[decarlo2011]] · [[brunswik1955]] · [[clark1973]] · [[judd2012]] · [[westfall2014]] ·
[[raaijmakers1999]] · [[baayen2008]] · [[barr2013]] · [[buss2006]] · [[ludosher1999]] ·
[[siegel-colburn1989]] · [[neri2010]] · [[green1964]] · [[pfafflin1968]] ·
[[osses-varnet2024]] · [[allard2014]] · [[clayards2008]] · [[kleinschmidt2019]] ·
[[chodroff2015]] · [[chodroff-bradshaw-livesay2023]] · [[theodore2009]] ·
[[heald-nusbaum2015]] · [[hillenbrand1995]] ·
[[uchanski1998]] · [[kapadia2023]] · [[luthra2023]] · [[mullennix1989]] · [[sommers1994]] ·
[[magnuson2007]] · [[chodroff2017]] · [[mcmurray2008]] · [[roark2019]] · [[winn2013]] ·
[[winn2020]] · [[logan1989]] · [[goldenberg2022]]

**其他回顧**:[[自然音vs合成音_理論推論]] · [[natural-vs-synthetic-speech]] ·
[[consonant-pair-choice]] · [[synthetic-speech-cognitive-load]]
**專案決策脈絡**:[[決策脈絡_統計方法]] · [[決策脈絡_聽覺維度]] · [[決策脈絡_AGRT模型假設]]

---
標籤note:[[literature-note]] [[GRT]] [[speech-perception]] [[AVWM]]
