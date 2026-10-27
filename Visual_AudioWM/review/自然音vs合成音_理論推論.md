# 在「操控優先」的前提下,GRT 該用哪一種語音刺激

**理論推論 · 2026-08-12**

---

## 前提(本文的全部推導都建立在這上面)

> **實驗室操控是優先;生態效度不是優先考慮的狀態。想知道的是最底層的理論現況。**

研究問題:**子音的語音表徵與色彩之間的關聯。**

**這個前提不是中性的。**它把兩件本來綁在一起的事拆開:
「參數要正確」與「結論要能類化」。本文的整條論證,就是追蹤這一刀切下去之後,
既有的論證各自還剩多少。

**姊妹文章**:[[token-variability-vs-perceptual-variance]] 負責證據與數字,
本文負責推論。本文引用的每個數字都在那邊有出處。

**結論先講**:**選合成刺激**(參數式,VOT 連續體),而且若資源允許,
用 **§9.2 的第四選項:多對配對的合成刺激**。

排序是 **(c) 合成 > (a) 多個自然 token > (b) 單一自然 token**。

理由不是「合成比較乾淨」這種空話,而是 §5.3b 的判準:
**[[clark1973]] 說單一刺激設計只有在「假設本身對單一個案成立」時才合法 ——
而只有合成刺激能把那個假設寫下來。**

⚠️ **三件必須先說的話**:
1. 這個結論**完全依賴**上面那個前提。**最強的反面**([[brunswik1955]] 點名批判
   「固定第三變項」的做法)不是被駁倒,是被**前提排除**(§8 的反面表)。
2. **論文的主張句必須跟著限縮**,否則整條論證失效(§9.0)。
3. **三選項的框架本身是錯的** —— 「合成/自然」與「單一/多個」是兩個獨立的軸(§9.2)。

反轉條件寫在 §9。

---

## 1. GRT 到底在估什麼

**這一步全部是文獻陳述,沒有我的推論。**

GRT 假設每個刺激在知覺空間裡對應一個機率分布;辨識反應由決策界線切出的區域決定。
估出來的東西有三類:**平均數位置、共變異矩陣(變異數與相關 ρ)、決策界線**。

**關鍵性質一:參數是相對量,不是絕對量。**
模型只在仿射變換下可辨識,所以必須固定尺度。[[silbert2012]] §II.B 的做法是:
> "the mean of one perceptual distribution is fixed at (0, 0), and **all marginal variances
> are fixed at unity.**"

**→ 一切「距離」都以知覺 SD 為單位。實質上被估的是 d′ 這種比值。**

**關鍵性質二:知覺維度是「對應到物理維度」而定義的。**
[[silbert-hawkins2016]]:
> "The dimensions along which the perceptual distributions and decision bounds are defined
> are **modeled perceptual dimensions corresponding to the physical dimensions of the
> stimuli.**"

**關鍵性質三:GRT 明文不模型化變異的來源。**
[[silbert-hawkins2016]] §1.1.1, p. 95:
> "Although there are multiple possible sources for random perceptual variability …
> **the specific sources of perceptual variability are not (typically) modeled in GRT.**"

**關鍵性質四:框架已經承認它估的是一個「和」。**
[[ashby-wenger-handbook]]:
> "**perceptual and criterial noise are not separately identifiable** … Instead, **only the sum
> of the perceptual and criterial noise variances is estimable.**"

---

## 2. 什麼會進到那個「和」裡

分母(知覺 SD)裡有什麼,決定了 β 與 d′ 的意義。文獻給的清單有三份,而且**彼此不一致**:

| 來源 | 它列的變異來源 |
|---|---|
| [[ashby2000]](Ashby 本人) | "**stimulus and perceptual noise**" / "stimulus and neural noise" |
| [[silbert2012]] §II.A | "internal noise, **external noise added to the stimulus**, or both" |
| [[silbert-hawkins2016]] | "environmental and/or neural noise" |

**把三份合起來,再加上 [[ashby-wenger-handbook]] 的決策雜訊,實際上有四項:**

$$\sigma^2_{\text{估到的}} = \underbrace{\sigma^2_{\text{神經}}}_{\text{要的}} + \underbrace{\sigma^2_{\text{決策}}}_{\text{分不開}} + \underbrace{\sigma^2_{\text{外加噪音}}}_{\text{受控}} + \underbrace{\sigma^2_{\text{刺激 token}}}_{\text{⚠️ 未受控}}$$

聽覺領域的正式可加式見 [[buss2006]] Eq. (1):**d′ = Δ/√(σe² + σi²)**;
而且他們明文寫 "**external noise (i.e., stimulus variability)**" ——
**外加噪音與刺激變異在形式上是同一項。**

### 2.1 ⭐ 第一個推論:「純 β」是達不到的目標

**(我的推論,但每一步都有上面的原文支撐。)**

研究者原本的目標是「讓 β 變成純知覺雜訊」。但:
- 第二項(決策)**框架明說分不開**;
- 第三項(外加噪音)在 SNR 路線下**佔總變異 37–64%**
  ([[siegel-colburn1989]] 的「量級相當」、[[neri2010]] 的 1.3 倍,見
  [[token-variability-vs-perceptual-variance]] §6.2);
- 第四項才是 token 變異。

**→ 目標必須改寫成:讓**未受控**的那幾項最小,讓剩下的變成**實驗者指定且可記錄**的。**

**這個改寫是本文其餘部分的判準。**它有三個可比較的面向:
**(i) 未受控變異的大小;(ii) 是否可描述/可記錄;(iii) 對兩個類別是否對稱。**

---

## 3. 三種刺激各讓什麼進到分母

### 3.1 多個自然 token

**未受控變異最大,而且量級已經確認。**

[[chodroff2017]] 的語者內 VOT SD:**/pʰ/ 12–27 ms、/b/ 2–8 ms**(孤立語)。
[[clayards2008]] 的聽者內在雜訊:**σ ≈ 10.7 ms**。

→ /pʰ/ 的 s = SD/σ ≈ **1.8**,變異膨脹 √(1+s²) ≈ **2.08 倍**,**β 掉到 48%**。

**而 [[rouder2007]] 說這種偏誤「not consistent … even in the large-sample limit」——
加試次救不了。**

### 3.2 單一自然 token

**within-category 變異 = 0。**這一項乾淨。

**但 §5 會說明它換來了一個更糟的東西。**

### 3.3 合成刺激

**within-category 變異 = 0,而且 between-category 的差異是實驗者寫下來的。**

---

## 4. 研究者的新論證:歸因問題

> 自然音來自田野,有更多的下降跟揚起(F0 輪廓變化),沒辦法控制,
> **所以無法歸因到子音的影響**。

**這個論證的正確形式不是「自然音品質差」,而是「多條線索共變,無法歸因」。**
本地實測支持它,而且**用的還是專案現有的、已經算乾淨的檔案**。

**本地實測(2026-08-12,自寫的自相關 F0 追蹤器)**:

| | F0 起始 | F0 結束 | 降幅 | 有聲段長 |
|---|---|---|---|---|
| `be.wav` | 99.8 Hz | 77.6 Hz | 22.1 Hz | 244.4 ms |
| `pe.wav` | 102.6 Hz | 76.3 Hz | 26.3 Hz | 194.6 ms |

兩 token 之間:起始 F0 差 **−2.8 Hz**、對齊有聲起點後**逐幀最大 F0 差 9.5 Hz**、
**有聲段長度差 49.9 ms**。
另已記錄:**聲學起始差 35.9 ms**、有聲段位準差 **1.6 dB**
([[consonant-pair-choice]] §7.2)。

⚠️ **F0 追蹤器參數會影響數字**(另一次量測得 −5.0 Hz / 9.6 Hz / 60 ms)。
**量級一致,個位數不可引用。**

### 4.1 ⚠️ 這些不全是瑕疵 —— 這正是論證的重點

- 母音起始 F0 較高**本來就是**無聲塞音的次要線索([[winn2020]]);`pe` 確實較高,**方向正確**。
- 有聲段長度差**部分是** VOT 差異的必然結果。

**所以不能說「自然音有錯」。要說的是:**

> **當 VOT、F0 輪廓、時長、位準同時不同時,GRT 估到的「聽覺維度」承載的是這些的混合。
> [[silbert-hawkins2016]] 的建模慣例保證了模型會報告「一條聽覺維度」,
> 但它在結構上無法告訴你那條維度是哪些線索的線性組合。**

**而研究問題是「子音語音表徵與色彩的關聯」。**
若那條「聽覺維度」其實是「VOT + F0 輪廓 + 時長」的混合,
那麼與顏色相關的到底是子音表徵,還是其中某一條副線索,**在模型層次無法分辨。**

**⚠️ 而且這還是 espeak 輸出。** `be.wav` / `pe.wav` 與 espeak-ng 的
`` [[b'i:]] `` / `` [[p'i:]] `` 輸出**逐取樣點完全相同**(本地實測,max abs diff = 0.0)。
**田野錄音的未受控共變只會更多,不會更少。**

---

## 5. ⭐ 核心論證:單一自然 token **凍結**了 between-category 的混淆

**這一節是本文最重要的一步,而且它把「單一自然 token」從第二名推到最後一名。**

三個選項在**兩種**變異上的表現不一樣,而先前的討論只看了第一種:

| | **within-category 變異** | **between-category 的未受控差異** |
|---|---|---|
| **多 token** | 有,膨脹 β(§3.1) | ✅ **會平均掉** —— 每個類別抽多個樣本,idiosyncrasy 趨於相消 |
| **單一 token** | ✅ 無 | ⛔ **固定、永久,而且與類別完全共線** |
| **合成** | ✅ 無 | ✅ **等於實驗者指定的差異** |

### 5.1 為什麼「固定的混淆」比「隨機的變異」更糟

**這是統計上的一般原則,而且本專案的模擬已經在同一個框架裡驗證過它的兩半:**

**隨機污染(多 token)的行為**——
[[token-variability-vs-perceptual-variance]] §4.2 的模擬:
即使 token SD 大到 1.5 個知覺 SD,**ρ̂ 仍精確為 0**;兩個顏色層次的聽覺 d′ **完全相等**。
**→ 它衰減效果、降低檢力,但不製造假的結構。**

**固定污染(單一 token)的行為**——
`be.wav` 與 `pe.wav` 之間的 F0 輪廓差、時長差 49.9 ms、起始差 35.9 ms、位準差 1.6 dB,
**每一個試次都在,而且 100% 與「這是 b 還是 p」共線。**
它**不是**加在變異數上,而是**直接加在兩個類別的平均數距離上** ——
**而 GRT 的 d′ 就是平均數之間的距離。**

**→ 隨機污染偏向虛無(保守);固定污染直接偏移要報告的那個量,方向無法預測、
且無法從資料中辨識。**

### 5.2 對齊救不了,而且理由是原則性的

`snr_audio.py` 已經對齊了聲學起始與 RMS,[[consonant-pair-choice]] §8.4 還要再修兩項。
**這是必要的,但在原則上不可能完備:**

> **你只能對齊你想到要量的東西。**
> 「我對齊了起始與位準」不蘊含「F0 輪廓、共振峰軌跡、頻譜傾斜、嗓音品質沒有差異」。

而且 [[sommers1994]] 給了一個令人不安的補充:對齊**整體振幅**這件事,
處理的正好是那個**零代價**的維度(F(1,58) = 0.036, p > 0.1),
而**語音上相關**的維度(語速/時間結構)才是有代價的那個(F(1,88) = 28.83, p < 0.005)。
**目前做的對齊,做的是容易做的那些,不是重要的那些。**

### 5.3 文獻上有沒有人做過這個論證?**有,而且比我預期的早 18 年**

#### (a) 「固定混淆」的論證存在,而且非常明確

**[[brunswik1955]] p. 194 原文** —— 他就是這樣稱呼單一刺激設計的:
> "This constitutes **artificially induced perfect confounding**, and may be labeled
> '**tied-variables' design** or, in short, **tied design**."

而且他明說**多加受試者救不了**(p. 204):
> "**As a matter of principle, individual sample situations, no matter how lifelike, cannot
> answer the funtional [sic] problem** … **Only representative design can answer this problem.**"

**[[judd2012]] 討論段原文** —— 現代版,而且說得更貼近本專案:
> "when experimenters attempt to replicate effects **using the same experimental stimuli** …
> **it can never be clear whether a successful replication indicates a truly reliable
> treatment effect or merely a consistent bias in the set of experimental stimuli used.**"

**→ §5.1 的第一原理論證有文獻背書了。而且 [[judd2012]] 的模擬給出量級:
只對受試者做分析時 Type I error 平均 **.317**,最壞 .616;
**而且「加受試者會讓偏誤更大」**,與 Brunswik 1955 的斷言一致。**

#### (b) ⭐⭐ 但 [[clark1973]] 給的判準比「固定 vs 隨機」細緻,而且**它才是真正的關鍵**

Clark 的「單一個案法」一節(pp. 352–354)沒有說單一刺激一律不合法。他給了條件:

> "**The hypotheses of interest must be applicable to single cases**, and these are often
> rather strong hypotheses."

> "**There is no single case imaginable that suffices to disconfirm the homograph hypothesis.
> So the method of single cases is simply not applicable to such 'central-tendency'
> hypotheses.**"

**→ 判準是:假設本身對單一個案成立嗎?**

套到 AVWM(**以下是我的推論**):

| 假設的寫法 | 是不是集中趨勢假設? | 單一刺激對能測嗎? |
|---|---|---|
| 「voicing 的語音表徵與顏色有關聯」 | ✅ 是(類別層次) | ⛔ **不能** |
| 「在 VOT = X ms、F1/F0 固定為 Y 的這個刺激上,聽覺與顏色判斷是否交互作用」 | ❌ 否(點假設) | ✅ **能** |

**⭐ 這正是合成刺激與單一自然錄音的分水嶺:**
- **合成**讓那個點假設可以被**寫下來**(X 與 Y 是你指定的數字)。
- **單一自然錄音**的「點」是「這段錄音剛好長什麼樣」——
  **寫不下來,也就沒辦法退守成點假設,只能退回集中趨勢假設,而那是 Clark 說不行的那種。**

**這是本文最強的一步,而且現在有文獻判準支撐,不再只是第一原理。**

#### (c) ⚠️⚠️ 三條**與本文結論方向相反**的證據,必須並陳

**(c-1) Brunswik 點名批判的正是「固定第三變項」——也就是合成路線的核心手法。**
[[brunswik1955]] pp. 195–196:
> "***Classical psychophysics as pseudo-univariate design.*** … the implicit design policy was
> **artificially to tie the distal and proximal variables** … Note that the tying of the two
> variables is the direct result of **a celebrated device of systematic design, the holding
> constant of a third variable.**"

**把 F1 與 F0 釘死、只動 VOT,正是這句話描述的做法。依 Brunswik,合成路線不是解方,
而是這個錯誤的原型。**

**怎麼回應?** —— Brunswik 的論證**就是**生態效度論證,而且是它最純粹的形式
(他的解方叫 "representative design")。**本文的前提明文把它降權。**
所以這條反面不是被駁倒,是被**前提排除**了。⚠️ **這必須寫進論文的 limitation,
不能假裝它不存在。**

**(c-2) [[westfall2014]]:刺激少的時候檢力有天花板,加受試者上不去。**
> "maximum achievable power with a medium effect size when using **eight stimuli** … is only
> approximately **.50, even with an infinite number of participants**."
> 4 個/條件 + **大**效果 d = 0.8 → 上限僅 **.41**;要 .80 需 **≥16 個刺激**。

**怎麼回應?** —— 那個天花板算的是**「對刺激母體做推論」**的檢力。
若研究主張被限縮成 (b) 表格裡的點假設,**刺激就不是隨機因子,天花板不適用。**
⚠️ **但那個限縮必須真的寫進論文的主張句,不能只在心裡想。**
(這個調和是我的推論,不是 Westfall 等人的。)

**(c-3) 該支文獻的主流結論是「用很多刺激並當隨機效果」,亦即支持選項 (a)。**
[[baayen2008]]:"Just as we model human participants as random variables, we have to model
factors characterizing their speech as random variables as well."
[[barr2013]]:只有隨機截距的模型「can have **catastrophically high Type I error rates**」。

**本文借用的只是它們的**前半**(單一刺激 = 固定混淆),不是它們的**結論**。
這個借用必須誠實標明,否則是斷章取義。**

#### (d) 一個對 AVWM 最有利、但到不了 n = 1 的例外

[[raaijmakers1999]] 摘要:
> "**in many cases there is no need to perform separate subject and item analyses** since the
> traditional F₁ is the correct test statistic. In particular this is the case **when item
> variability is experimentally controlled by matching or by counterbalancing.**"

**AVWM 正是配對設計**(/b/ 與 /p/ 是配對的,不是各自獨立抽樣的)。**這對本專案有利。**

⚠️ **但兩個限定**:
1. 配對只**減少**偏誤:"σ²_AB … will **usually** be smaller"(p. 422)。**不是零。**
   而 σ²_AB 就是「配對沒配好的那部分」= §5.2 的「你只能對齊你想到要量的東西」。
2. **他們的推導需要一個「配對區塊的母體」**(p. 421:"The various blocks are still assumed
   to be **sampled randomly from a larger population of blocks**")。
   **只有一對時 q = 1,σ²_AB 估不出來。他們從未討論 q = 1。**
   (這個推論是 subagent 的,不是作者的。)

**→ 它替的是「**多對**配對刺激」,不是「單一配對」。
⭐ 而那是一個本專案還沒有考慮過的第四個選項 —— 見 §8.1。**

#### (e) ⭐⭐ 這條論證從未進入 GRT —— 而且這次是用引文網路量化的

subagent 跑了引文圖(OpenAlex),不是憑印象:

| 事實 | 數字 |
|---|---|
| [[clark1973]] 的被引總數 | **2,278** |
| 其中 *JASA*(語音與聽覺心理物理的旗艦期刊) | **9(0.4%)** |
| 其中 *J. Mathematical Psychology* | **3** |
| **同時**引用 Clark (1973) 與 Ashby & Townsend (1986) 的著作 | **恰好 1 篇,而且是心理語言學論文,不是 GRT 方法論文** |
| **Noah Silbert** 引用 Ashby & Townsend 的著作 / 引用 Clark 的 | **16 / 0** |
| Clark 的 2,278 篇引用者中,標題含 GRT 詞彙的 | **0** |
| 對全部引用者做 `psychophysic\|signal detection\|d-prime\|psychometric function\|threshold` 的引用脈絡掃描 | **0 命中** |
| *Perception & Psychophysics* 的 26 筆引用,內容檢查 | **全部是詞彙辨識/閱讀/促發** —— 沒有一筆關於閾值、辨別、d′ |

**唯一的橋是階層貝氏 SDT**([[rouder2007]]、[[decarlo2011]]、Rouder & Lu 2005、
Pratte et al. 2010)—— 它們**引用了** Clark,**修好了**問題(item 隨機效果),
但停在**再認記憶**,從未跨進知覺敏感度的估計。
⚠️ **[[decarlo2011]] 就發表在 GRT 的主場期刊 JMP** —— 論證**就在隔壁,但沒有跨過那一步。**

**⚠️ 一個必須誠實的補充**:[[silbert2018]]("Modeling **talker- and listener-based sources of
variability**")**確實**建了有語者與聽者隨機變異的多層 GRT,
但它的 54 筆參考文獻裡**沒有 Clark、沒有 Coleman、沒有 Judd/Westfall**。
**做法從語音學那邊獨立長出來了,論證沒有。**
⚠️ 而且**它是否把 token(而非語者)當隨機因子,subagent 取不到全文,不可主張。**

**方法上的但書**:以上全部依賴 OpenAlex/Crossref/Semantic Scholar 的索引;
專書的參考文獻不被索引(Macmillan & Creelman、Wickens 等 SDT 教科書無從檢查)。
**「GRT 從未engage」是很強的證據,不是邏輯證明。**

---

## 6. 把 Silbert 的論證拆成兩半

[[silbert2012]] §I.C.2 是他最完整的理論陳述:
> "if the goal is to study interactions or independence between phonological dimensions, as
> it is here, **strong assumptions about the relevant set of acoustic-phonetic cues should be
> avoided as much as possible. Many such assumptions can be avoided by using naturally
> produced, and so naturally variable, stimuli.**"

**這句話裡有兩個獨立的主張,他把它們綁成一句:**

| | 主張 | 在新前提下 |
|---|---|---|
| **前半** | 沿單一實驗者選定的參數變動,會讓估到的知覺維度被那個選擇**預先決定** | ✅ **仍然成立** —— 這是模型結構([[silbert-hawkins2016]] 的建模慣例),與生態效度無關 |
| **後半** | **自然的變異性**是達成前半的機制("and so naturally variable") | ⚠️ **這一半才是被降權的** |

### 6.1 前半還剩多少力道?

**⭐ 這是本文的關鍵判斷,而且是我的推論:前半的力道**不依賴 token 之間的變異**。**

前半擔心的是:**你給模型的軸,是不是聽者實際使用的軸。**
解決這件事需要的是**單一 token 之內線索的共變** ——
一個自然錄音的 /pi/ 裡,F1 起始、F0、burst 頻譜、送氣振幅本來就與 VOT 一起變動。
**這在一個 token 上就成立,不需要第二個 token。**

**→ 所以「單一自然 token」能保住前半、丟掉後半,同時把 token 變異歸零。
這正是選項 (b) 看起來像答案的原因。**

### 6.2 ⛔ 但 §5 把它擋掉了

單一自然 token 保住了「線索共變」,**代價是把那些共變的線索永久綁在類別身上**。

**而且這兩件事是同一件事的兩面**:
- 「線索共變」= /pi/ 的 F0、時長、F1 都與 /bi/ 不同,而且方向一致
- 「固定混淆」= 那些差異每個試次都在,且 100% 與類別共線

**→ 選項 (b) 想要的優點與它的缺點,在物理上是同一個東西。無法只留一半。**

**這是本文最強的一步推論**,也是我認為研究者的新論證正確、而先前排序需要修正的理由。

### 6.3 那合成刺激呢?

合成刺激**明白地放棄前半**:它讓實驗者指定哪些線索共變、共變多少。

**在「操控優先」的前提下,這不是缺點,是規格。**
但它有一個真實的代價,§7 處理。

**⚠️ 一個必須誠實的補充**:[[roark2019]] 用**完全合成、參數正交**的刺激,
仍發現維度**不是知覺正交**。
**→ 合成不能保證知覺正交。**正確的說法是:合成讓你知道**你放進去了什麼**,
不保證聽者**取出了什麼**。這是一個關於**已知**的優勢,不是關於**正交性**的優勢。

---

## 7. 合成路線的誠實代價:它測到的是**單線索**的 voicing 知覺

若用 KlattGrid 把 F0 與 F1 完全固定、只動 VOT,**VOT 就成為唯一的 voicing 線索**。

自然聆聽時聽者整合多條線索,而且 [[winn2013]] 顯示**噪音還會改變 VOT 與 F0 的相對權重**。

**→ 合成刺激探測到的是「一條通道」的 voicing 知覺,不是完整的 voicing 表徵。**

**在「要最底層機制」的前提下,這可能正是想要的**(隔離出一個通道),
**但必須明說這個限縮,而且它對研究問題有實質後果:**

| | 可以主張的 | **不可以**主張的 |
|---|---|---|
| 合成路線 | 「**沿 VOT 定義的 voicing 維度**與顏色的關聯」 | 「voicing 的語音表徵與顏色的關聯」 |

**這是一個範圍的縮小,不是一個瑕疵** —— 但論文的標題與結論句必須跟著縮。
若研究者要主張的是「子音**表徵**」這種較抽象的層次,
**單線索刺激探測到的表徵比多線索的窄**,審稿人會問,而且問得有道理。

⚠️ **還有一個實作上的問題不能忘**:[[決策脈絡_聽覺維度]] 反轉 6 的實測顯示
KlattGrid 的時間解析度是**取樣點級**(0.0227 ms),
**不是**先前以為的量化到音高週期。**合成路線在技術上是可行的**,
而且 [[決策脈絡_聽覺維度]] 的 A1–A5 檢查顯示 **VOT 比 SNR 更符合 AGRT 的雙極結構**
(可直接餵 `AGRTHandler`,不需另開 `QuestHandler`)。
**這是合成路線一個獨立的、實作層次的加分。**

---

## 8. 結論

**在「實驗室操控優先、生態效度非優先、要最底層的理論現況」這個前提下:**

### 排序:**(c) 合成 > (a) 多個自然 token > (b) 單一自然 token**

⚠️ **這修正了本文初稿**(初稿把單一自然 token 排第二)。修正的理由在 §5.3b 與 §8.0。
⚠️ **而且這個三選項框架本身是錯的** —— 見 §9.2 的第四選項。

### 8.0 為什麼單一自然 token 是**最差**而不是第二

初稿的直覺是「β 乾淨 → 排第二」。**那個直覺錯在把偏誤與變異當成同一類東西。**

| | 多個自然 token | 單一自然 token |
|---|---|---|
| 污染的型態 | **變異** | **偏誤** |
| 對 ρ 的影響 | **只衰減**,不製造假陽性(模擬:token SD 到 1.5 個知覺 SD,ρ̂ 仍精確為 0) | 直接偏移平均數距離,**方向不可預測** |
| 對顏色維度 | **完全乾淨**(模擬:d′ 恆為 2.000) | 未知 |
| 能不能事後處理 | 可以 —— 混合模型([[barr2013]])或逐 token 聲學量測 | ⛔ **不能** —— n = 1,沒有東西可以估 |
| [[clark1973]] 判準 | ✅ 可做類別層次主張 | ⛔ **兩種假設都撐不起來** |
| 偏誤會不會隨試次縮小 | (變異會) | ⛔ **不會** |

**→ 保守的偏誤方向(衰減)可以被承認並報告;不可量化的固定偏誤不能。
在「要量出最底層的知覺現況」這個目標下,一個會低估效果的方法仍然可用,
一個會把效果推向未知方向的方法不可用。**

⚠️ **獨立佐證**:[[決策脈絡_聽覺維度]] 由另一路分析得到**同樣的排序**
(「單一自然 token 是三者中最差的」)。
⚠️ 兩份分析共用了本地實測資料,不算完全獨立,但推論路徑不同。

---

**理由,依強度排序:**

**1. ⭐ 只有合成能讓研究假設退守成一個**寫得下來的點假設**。**(§5.3b)
這是三個選項裡唯一的結構性差異,其餘都是程度問題。

依 [[clark1973]] 的判準,單一刺激設計合法的**充要條件**是「假設本身對單一個案成立」。
- **合成**:點假設 = 「在 VOT = X、F1/F0 = Y 這個刺激上」→ **寫得下來,判準滿足。**
- **單一自然錄音**:點 = 「這段錄音剛好長什麼樣」→ **寫不下來**,只能退回集中趨勢假設,
  而那正是 Clark 說「no single case imaginable」的那一種。
- 而且單一自然 token 把一個**隨機**污染換成一個**固定且與類別共線**的污染
  ([[brunswik1955]] 的 "artificially induced perfect confounding";
  [[judd2012]] 的 "merely a consistent bias in the set of experimental stimuli used")。

**證據強度:中等偏強**(判準是原文;**套用到語音刺激與合成/自然的分野是我的推論**,
Clark 沒有討論合成刺激)。

**2. 多 token 的量級代價已經確認,而且加試次救不了。**(§3.1)
/pʰ/ 的語者內 SD(12–27 ms)**大於**聽者的內在雜訊(10.7 ms),
β 掉到約 48%;[[rouder2007]] 說這種偏誤不一致。
**證據強度:中等偏強**(數字來自已核實的表格,但**換算過程有三層假設**,見
[[token-variability-vs-perceptual-variance]] §3.0)。

**3. 而且多 token 的代價嚴重不對稱**(/pʰ/ 是 /b/ 的 3–4 倍),
模擬顯示這會偽裝成**決策界線的位移**(見 [[token-variability-vs-perceptual-variance]] §4.3)——
**而 AVWM 的核心操弄正是注意力,決策界線本來就是要看的東西。**
**證據強度:中等**(模擬清楚,但只測了變異數固定的模型)。

**4. Silbert 的論證只有後半失效,前半仍成立** —— 但前半**擋不住**合成路線,
只是要求論文明說範圍的限縮(§6、§7)。
**證據強度:高**(原文引句明確)。

### ⚠️ 這個結論最強的三條反面(不要在論文裡假裝它們不存在)

| 反面 | 來源 | 我的回應 | 回應夠不夠強? |
|---|---|---|---|
| **合成路線正是 Brunswik 點名批判的「pseudo-univariate / tied design」** —— 「固定第三變項」被他當成錯誤的原型 | [[brunswik1955]] pp. 195–196 | Brunswik 的論證**就是**生態效度論證(解方叫 representative design),**被前提排除**,不是被駁倒 | ⚠️ **只在前提內成立。前提一變就翻。必須寫進 limitation** |
| **刺激少 → 檢力有天花板,加受試者無效**(4 個/條件 + 大效果 → 上限 .41) | [[westfall2014]] p. 2032 | 那個天花板算的是**對刺激母體推論**的檢力;點假設下刺激不是隨機因子 | ⚠️ **只有在論文真的把主張限縮成點假設時才成立** |
| **該支文獻的主流結論是「用很多刺激(≥16)+ 混合模型」,即支持選項 (a)** | [[baayen2008]]、[[barr2013]]、[[judd2012]] | 本文只借它的**前半**,不借結論 | ⚠️ **這是選擇性引用,必須明白標示** |

**→ 誠實的總結:本文的結論**完全依賴那個外生給定的前提**。
它不是「合成客觀上比較好」,而是「**在這個前提下**,合成是唯一能讓研究主張站得住的選項」。**

### ⚠️ 一個比排序更緊急的行動項

**`be.wav` / `pe.wav` 是 espeak-ng 的輸出**(本地實測,逐取樣點相同)。
espeak-ng 是**規則式**共振峰合成 —— 它的線索結構由合成器作者決定,**不是研究者控制的**。

**→ 現況既不是自然刺激(沒有真實的線索共變),也不是受控合成(參數不由你指定)。
兩邊的好處都沒拿到。**

**在三選項的排序之前,這一項必須先處理。**它在兩個前提下都是問題:
生態效度前提下它不自然;操控優先前提下它不受控。

---

## 9. 這個結論在什麼條件下會反轉

**列出來是因為前提是外生給定的,而前提可能會變。**

| 條件 | 反轉成什麼 | 為什麼 |
|---|---|---|
| **要投稿到重視生態效度的期刊**(Lab Phon、J. Phonetics、Cognition) | **(a) 多自然 token** | 那些期刊的審稿人會直接引 [[silbert2012]] §I.C.2 與 [[hamilton2020]];而且「單一 token」在那個社群裡近乎不可辯護 |
| **審稿人要求類化證據** | **(a)** | 單一刺激的結果在形式上只能推論到那個刺激。這是 Clark 1973 一系文獻的主場,而本文只借了它的前半(§5.3) |
| **研究問題改成「類別層次的 voicing 表徵」而非「沿 VOT 的 voicing 維度」** | **(a)** | §7 的限縮就從「可接受的範圍聲明」變成「與研究問題不符」 |
| **發現 KlattGrid 做不出可信的 /bi/–/pi/** | **(b)** | 合成路線的前提是合成器做得到。⚠️ [[決策脈絡_聽覺維度]] 已驗證解析度沒問題,但**沒有驗證過知覺可信度** |
| **決定要跑 double-pass / 反向相關分析** | 不反轉,但**必須存 RNG 種子** | [[green1964]]、[[osses-varnet2024]];成本為零 |
| **[[uchanski1998]] 全文顯示 token 變異的影響確實遠小於內在雜訊** | 減弱理由 2,**但不動理由 1** | 該篇摘要最後一句是本文最強的反證,而全文未取得 |
| **[[silbert2018]]("talker- and listener-based sources of variability")顯示 Silbert 已正面處理過刺激變異** | 可能大幅改寫 | **未讀。這是最高優先的待補項** |

### 9.0 ⭐ 論文裡**必須**寫的一句話(否則結論失效)

因為結論倚賴 [[clark1973]] 的點假設判準,**主張句必須跟著限縮**:

> ❌ 不可寫:「voicing 的語音表徵與顏色表徵之間存在知覺互動」
> ✅ 應寫:「**在沿 VOT 定義、其他 voicing 線索受控固定的刺激上**,
> 聽覺類別判斷與顏色判斷之間存在/不存在知覺互動」

**若做不到這個限縮(例如研究者要主張的就是類別層次的結論),
本文的整條論證失效,排序應回到 (a) 多 token + 混合模型。**

### 9.1 ⚠️ 一個折衷方案,可能兩邊都要得到

[[silbert2012]] §IV.A 說明他用 4 個 token 的**真正理由**:
> "**In order to ensure that the subjects did not simply attend to some irrelevant acoustic
> feature of a particular token of a particular category**, a small degree of within-category
> variability was introduced"

**這個理由與「類化」無關 —— 它是防止受試者鑽單一 token 的漏洞。**

而 [[sommers1994]] 證明:**只在「語音上不相關」的維度上變異,代價為零**
(整體振幅 F(1,58) = 0.036, p > 0.1)。

**→ 折衷:用單一合成基底,但讓 token 在語音上不相關的維度上抖動**
(整體音量、絕對 F0 水平、起始相位),**而 VOT 與所有 voicing 相關線索固定。**

- ✅ 滿足 Silbert 的防漏洞理由
- ✅ token 變異不進到聽覺知覺維度(依 [[sommers1994]] 的原則)
- ✅ between-category 差異仍等於實驗者指定的
- ⚠️ **沒有人做過這個設計**,而且 [[sommers1994]] 的原則是從詞辨識推來的
  (**我的外推**)。

**這條路值得在 pilot 裡試,但不能當成有文獻依據的成熟做法。**

### 9.2 ⭐⭐ 一個先前完全沒考慮過的第四選項:**多對配對的合成刺激**

**[[raaijmakers1999]] 的分析指向一個三選項之外的設計,而且它同時滿足最多條件。**

**做法**:不是「一組 /bi/–/pi/」,也不是「4 個 /bi/ + 4 個 /pi/ 各自獨立」,
而是**若干**配對的**合成刺激組**(例如 8–16 組),每一組內部的 /b/ 與 /p/
**只在 VOT 上不同**,而**組與組之間**在語音上不相關的維度上變動
(整體 F0 水平、母音時長、整體音量)。

| 條件 | 滿足嗎? |
|---|---|
| within-pair 的 between-category 差異 = 實驗者指定 | ✅ 每一對內部只有 VOT 不同 |
| [[raaijmakers1999]] 的「配對」條件 | ✅ 而且**這次真的有配對區塊的母體**(q > 1),F₁ 合法 |
| [[westfall2014]] 的刺激數要求(≥16) | ✅ 可達成 |
| [[clark1973]] 的判準 | ✅ **不需要**退守點假設 —— 可以做集中趨勢主張 |
| [[silbert2012]] §IV.A 的防漏洞理由 | ✅ 受試者無法鑽單一 token |
| token 變異進到聽覺知覺維度? | ✅ **不會**,若組間只動語音上不相關的維度([[sommers1994]]) |
| [[brunswik1955]] 的批判 | ⚠️ **仍然中** —— 它仍是 tied design(F1 被固定) |

**→ 這個設計把「合成」與「多刺激」的優點疊起來,而三選項的框架把它們當成互斥,
那是框架的錯,不是事實。**

⚠️ **三個誠實的但書**:
1. **沒有人做過這個設計**;[[sommers1994]] 的「不相關維度零代價」原則是從**詞辨識**
   推來的(**我的外推**)。
2. **GRT 的模型層次沒有現成解** —— 2×2 GRT 在個體層次已飽和([[silbert2012]] 自陳),
   加 token 隨機效果會不可辨識([[barr2013]] 卡)。實務上可能只能**併掉**,
   那就退回 [[rouder2007]] 的偏誤(⚠️ 但因為組間只動不相關維度,σ_token 應該很小)。
3. 實作成本高於單一刺激對。

**這是我建議 pilot 優先試的方向。**

---

## 10. 與 `natural-vs-synthetic-speech.md` 的衝突 —— 明講

**有衝突,而且是結論層次的。**

| | [[natural-vs-synthetic-speech]] §6.1 | 本文 §8 |
|---|---|---|
| 建議 | 走 SNR 路線(自然 token + 噪音) | **合成刺激** |
| 前提 | **未列出**「生態效度非優先」 | **明文以它為前提** |
| Silbert 論證的處理 | 當成最強的一條,整體採用 | **拆成兩半**;前半保留,後半降權(§6) |
| token 變異 | 只在 [[silbert2012]] 卡的限制欄提過一句 | **核心判準**,並量化 |

**分歧來自單一一個前提差異:類化的權重。**

那份回顧的論證鏈裡,「GRT 的維度解釋」之所以最要命,是因為它同時服務於
「參數要正確」與「結論要能類化」。
**加上「生態效度非優先」之後,兩者分家,而它們指向相反的方向。**

**這不是誰算錯,是判準換了。**

**⚠️ 而且必須說清楚**:那份回顧的 §6.2 已經誠實承認
「合成路線並沒有被駁倒」,並引 [[logan1989]](音節首子音上合成與自然統計上無異)
當最強的反方證據。**本文只是在新前提下把那條反方證據推到了主位。**

---

**相關卡片**:[[silbert2012]] · [[silbert-hawkins2016]] · [[silbert2018]] · [[ashby2000]] ·
[[ashby-wenger-handbook]] · [[rouder2007]] · [[buss2006]] · [[siegel-colburn1989]] ·
[[neri2010]] · [[green1964]] · [[osses-varnet2024]] · [[clayards2008]] · [[chodroff2017]] ·
[[chodroff-bradshaw-livesay2023]] · [[theodore2009]] · [[kleinschmidt2019]] ·
[[uchanski1998]] · [[kapadia2023]] · [[sommers1994]] · [[roark2019]] · [[winn2013]] ·
[[winn2020]] · [[logan1989]] · [[hamilton2020]]

**其他回顧**:[[token-variability-vs-perceptual-variance]](證據與數字) ·
[[natural-vs-synthetic-speech]](⚠️ 結論相衝突,見 §10) · [[consonant-pair-choice]]
**專案決策脈絡**:[[決策脈絡_聽覺維度]] · [[決策脈絡_統計方法]] · [[決策脈絡_AGRT模型假設]]

---
標籤note:[[literature-note]] [[GRT]] [[speech-perception]] [[AVWM]]
