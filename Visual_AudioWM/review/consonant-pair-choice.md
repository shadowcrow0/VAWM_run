# 子音配對該選哪一組:/b/–/p/、/d/–/t/、還是 /g/–/k/

**綜合回顧 · 2026-08-12**
AVWM 的聽覺維度需要一組塞音 voicing 對比。三個發音部位怎麼選?

單篇文獻卡在 `90_Sources/`。**每一條主張標注證據強度與閱讀狀態;我的推論與原文陳述嚴格分開。**
姊妹回顧:[[natural-vs-synthetic-speech]](自然 vs 合成)· [[synthetic-speech-cognitive-load]](認知負荷)

---

## 0. 結論先講

**選 /b/–/p/(唇音),配 /i/ 母音 —— 也就是維持現有的 be/pe。證據強度:中等偏強。**

結論比預期乾淨:**軟顎音在多條獨立的證據上都比較差,而唇音沒有任何一條「作為配對」的專屬缺點。**這不是「勉強挑一個」,是三組裡有一組被明確排除、另一組(舌尖音)只是次佳。

⚠️ **但唇音不是沒有問題 —— 只是問題不在配對層次。**§7.2 實測發現現有的 `be.wav` / `pe.wav` 有兩個殘留混淆(語音起始差 **36 ms**、有聲段位準差 **0.30 dB**),兩者都是**施工問題**,換成 /d/–/t/ 也會重新出現,但都必須修。

**關鍵發現是一筆直接的組內比較**([[goldenberg2022]]):同一批受試者、同一個實驗,**軟顎音的辨識函數寬度是唇音的近兩倍**(acuity 2.0 vs 1.1),而且邊界偏斜。⚠️ **但後續查證發現它用的母音是 /ɑ/,不是 AVWM 的 /i/** —— 部位與母音的效果在該研究裡無法分離,因此這條的權重已下修(§2、§7.5)。

⚠️ **刺激層次的但書(2026-08-12 追加)**:AVWM 的刺激是**單一 CV 音節、單獨呈現**(實測 `be.wav` 566.7 ms、`pe.wav` 585.8 ms)。本回顧倚重的證據**不全是這個層次** —— 產出數值來自詞與連續語音、多重 burst 統計來自語料庫。**§7 專門處理配對與層次問題,並下修了幾條原本被高估的證據。**結論(/b/–/p/ + /i/)在加上這個條件後**仍然成立**,但支撐它的主要不再是 §2,而是 §7.1(Winn 的 /i/ 論證對唇音成立且點名唇音)與 §7.3(詞彙地位平衡)。

**兩塊補充證據**(獨立查證,寫成 [[軟顎音證據補充]]):軟顎音在 /i/ 前的前移確實存在但
「顎化」一詞過重(Keating & Lahiri 1993:是 gradient,弱於音位顎化);母語者 **67.28%**
的軟顎音有多重 burst(唇音 33.92%),造成 VOT 起點約 **14 ms** 的地標歧義。
⚠️ 但後者主要是**自然語音**的問題 —— 合成的 burst 是自己放的單一脈衝,不會有這個歧義,
而 Klatt Table III 本來就標明只適用前母音,所以「軟顎音難合成」在固定母音的設計裡站不住。
**因此軟顎音的缺點在自然路線上成立且嚴重,在合成路線上大幅減弱。**

⚠️ **但仍要標明:沒有任何一篇文獻正面論證過三個部位在 VOT 實驗中的優劣。**[[winn2020]] 是這領域的標準方法學教學,經全文查證,**他對發音部位不做任何推薦**。本回顧是把散落的部位特定證據拼起來的**推論**。

---

## 1. 基本參數:VOT 範圍與知覺邊界

### 1.1 知覺邊界 —— 研究者的印象獲得證實

[[winn2020]] §II.A(全文已讀)原文:

> "In simple single-syllable recognition situations for English, one could expect the perceptual boundary between **/b/ and /p/ to fall somewhere around 20–25 ms**, the boundary between **/d/ and /t/ to fall near 35 ms**, and the boundary between **/g/ and /k/ to fall near 40 ms.**"

⚠️ Winn 給這些數字時**沒有引用特定來源**,是以「一般預期」的語氣寫的。

**獨立的唇音實證值**([[fox2020]],全文已讀):
> "A psychophysical category boundary between 20 ms and 30 ms divided the continuum into stimuli most often perceived as voiced (/b/: 0 ms, 10 ms, 20 ms VOTs) or as voiceless (/p/: 30 ms, 40 ms, 50 ms VOTs)."

**Winn Table I 的端點建議**:/b p/ 3→60 ms;/d t/ 10→70 ms;/g k/ 15→70 ms。

### 1.2 產出數值:軟顎音的兩端**最擠**

[[chodroff2017]](*J. Phonetics* 61, 30–47,全文已讀)是現代大語料庫版本,Table 1(孤立語)與 Table 6(連續語)的平均 VOT(ms):

| | pʰ | tʰ | kʰ | b | d | g |
|---|---|---|---|---|---|---|
| 孤立語 平均 | 89 | 98 | 99 | 13 | 21 | **28** |
| 連續語 平均 | 51 | 61 | 56 | 8 | 14 | **17** |
| 孤立語 talker 平均的 SD | 27 | 28 | 24 | 5 | 7 | **10** |

**由這些已發表平均值算出的有聲–無聲間距(這是我的算術,不是原作者的主張)**:

| | 唇音 | 舌尖音 | 軟顎音 |
|---|---|---|---|
| 孤立語 | 76 | 77 | **71** |
| 連續語 | 43 | 47 | **39** |

**→ 軟顎音的可用區間最窄**,因為 /g/ 的 short-lag VOT 最長(28 / 17 ms),把有聲端往上頂。而且**有聲端的說話者間變異隨部位後移而變大**(b 5 → d 7 → g 10)。

**對 AVWM 的意義(我的推論)**:適應式程序需要一段乾淨、夠寬的搜尋範圍。唇音的有聲錨點最低(8–13 ms)、間距最寬,**給適應程序最大的操作空間**。

### 1.3 經典的部位序列其實不穩

[[chodroff2017]] 原文直接修正了教科書說法:
> "The present study observed a strong tendency for the ranking of [pʰ]<[kʰ] ... and **little difference between the means of [tʰ] and [kʰ]** within or across talkers in both studies. Among the voiced stops, the overwhelming majority of speakers had increasing VOT with more posterior places of articulation ([b]<[d]<[g])."

[[chodroff2019]] 的 100+ 語言調查也讓 [[winn2020]] 加了但書:
> "**a more recent cross-linguistic study by Chodroff et al. (2019) challenges the long-held notion of this ordering** of VOT based on place of articulation"

**→ 無聲端的三分序列不可靠;有聲端的 b<d<g 才穩。**這正好強化 §1.2 的重點:唇音的優勢在**有聲端**,而有聲端的序列是可靠的那一半。

### 1.4 為什麼 VOT 隨部位後移而增加

[[abramson2017]](全文已讀,原始 XML 逐字核對)§3:
> "Using VOT data from 18 languages, **Cho and Ladefoged (1999)** ... focusing their attention on the increasing values of voicing lag as the place of stop articulation moves from the lips to the back of the mouth ... Cho and Ladefoged discuss such possible causative factors as **cavity size behind the occlusion and in front of it, the size of the area of contact, and the aerodynamics in the region of the larynx.**"

直接的空氣動力學證據 —— Eshghi, Alemi & Zajac (2016), *Folia Phoniatr. Logop.* 68(5), 239–246, doi 10.1159/000478523(⚠️ **僅讀摘要**):
> "Aerodynamically, Po was greatest for the velar stop, intermediate for the alveolar stop, and smallest for the bilabial stop."

⚠️ 注意這支持的是**「唇音 vs 其餘」的二分**,而不是乾淨的三分序列。

⚠️ **Cho & Ladefoged (1999) 全文未取得**(確認為封閉取用),機制細節僅透過 [[abramson2017]] 的轉述。

---

## 2. 軟顎音的辨識函數又淺又偏 —— 但那是在 /ɑ/ 脈絡下測的

**這是本回顧唯一一筆「同一批受試者、同一個實驗、直接比較兩個部位」的資料。**初稿把它當成最有決策價值的一條;**加上刺激層次的條件後,它的權重已下修 —— 原因見本節末與 §7.5。**

[[goldenberg2022]](*Front. Hum. Neurosci.* 16:879981,全文已讀)原文:

> "The bilabial category boundary is approximately centered between its endpoints, that is, its bias (4.2) is close to its midpoint (4.5). ... **Acuity (a measure of boundary slope) was computed as the difference between the 25 and 75% probabilities** for the discrimination function. **The velar category boundary is not as centralized and is skewed toward voicelessness (bias = 3.6)**; that is, longer VOTs were necessary for /ka/ responses. **The velar acuity (2.0) is shallower than that of the bilabial (1.1)**, possibly due to this skew."

**因為 acuity 定義為 25–75% 的寬度,數值越大代表越淺:軟顎音的辨識函數寬度約為唇音的兩倍。**

**對 AVWM 的直接後果(我的推論)**:
1. **適應式程序估斜率會更慢、更不準。**函數越淺,同樣的試次數換到的 β 精度越差。
2. **邊界偏斜代表對稱性假設不成立。**AGRT 的雙極結構預期邊界大致落在中點;軟顎音的 bias(3.6)明顯偏離中點(4.5),唇音(4.2)則貼近。
3. GRT 要估的知覺分布,在一個偏斜、淺平的維度上更難與高斯假設相容。

⚠️ **限制**:這是**單一研究**的附帶觀察,不是專門為比較部位而設計的實驗;作者自己用 "possibly due to this skew" 這種試探語氣。

⚠️⚠️ **一個更嚴重的限制,見 §7.5:這兩條連續體用的母音是 /ɑ/,正是 [[winn2020]] 明確不推薦的那一個。**在 /ɑ/ 脈絡下,F1 起始會隨 VOT 共變成為額外線索,而這個共變的量級**本來就隨部位不同**。因此「軟顎音較淺」有多少來自部位本身、有多少來自 /ɑ/ 與部位的交互作用,**該研究無法分離**。**AVWM 用的是 /i/,不是 /ɑ/。**

**→ 證據強度下修為:中等偏弱**(直接組內比較是強項;單一來源、附帶觀察、且母音脈絡與 AVWM 不符是弱項)。**本節標題的「決定性」在加上單一 CV 音節 + /i/ 的條件後不再成立。**

---

## 3. 軟顎音的三個結構性問題

### 3.1 雙重 burst,而且在無聲端更嚴重

[[kingston1983]](*JASA* 74(S1), S51–S52,⚠️ **僅讀摘要,且該摘要本身是會議摘要**)原文:

> "**Multiple intensity peaks, 'double bursts,' are common in the release of velar stops.** ... If a high rate of air flow causes this second, brief closure, then **double bursts should occur more often after /k/ than /g/**, since intraoral air pressure during closure is higher for the voiceless stop than the voiced one."

> "Intensity measurements ... show **vowel quality determines burst intensity for velars—least intense before [u], most before [i]** ... more than the voiced/voiceless or aspirated/unaspirated contrasts do. **Alveolar releases vary much less across vowels.**"

**三件事一次到位:**
1. 雙重 burst 在軟顎音「common」;
2. 預期**在 /k/ 比 /g/ 更常見** —— 正好落在要建的連續體的無聲端;
3. 軟顎音的 burst 強度**由母音決定的程度超過由 voicing 決定的程度**,而舌尖音「varies much less across vowels」。

**為什麼這對 AVWM 要緊**:VOT 是**從 burst onset 起算**的。burst 結構不單純,burst onset 的定位就不單純。[[abramson2017]] 已記錄 burst/送氣界線難劃是主要量測誤差來源。

⚠️ **重要的負面結果**:[[abramson2017]] 是現代 VOT **量測**問題的標準回顧,而它**全文從未出現 "velar" 一詞**,也沒有討論多重 burst。**所以「軟顎音比較難量」是從 Kingston (1983) 推出的合理推論,不是量測文獻的既有陳述。**

**✅ 發生率統計已補上**(見 [[軟顎音證據補充]] §三,來源 Barrera-Pardo 2023, *Loquens* 10(1-2), e100,全文已讀):

| 發音部位 | 有多重 burst 的比例 | 平均 burst 數 |
|---|---|---|
| 唇音 | 33.92% | 2.21 |
| 舌尖音 | 15.78% | 2.28 |
| **軟顎音** | **67.28%** | **2.86** |

χ²(2) = 37.72, p < .001, η² = 0.15(大效果量)。**軟顎音近七成有多重 burst,是唇音的兩倍。**

**而且它造成可量化的地標歧義**:同一資料「從第一個 burst 量」vs「從最後一個 burst 量」的 VOT 差 —— /p/ 7.73 ms(n.s.)、/t/ 11.50 ms(n.s.)、**/k/ 14.18 ms(p < .001, d = 0.82)**。

⚠️ **但這主要是自然語音的問題**:合成路線的 burst 是自己放的單一脈衝,不會有這個歧義。詳見 [[軟顎音證據補充]] §三與下方 §8.2。

⚠️ **仍然查無**:各部位 **burst 時長(ms)** 的數值。「軟顎音 burst 較長」這個說法**沒有任何取得到的來源支持**,不應寫進論文。

### 3.2 軟顎音的 burst 頻譜隨母音劇烈變動 —— 但這對**固定母音**的設計不致命

[[frisch2016]](*J. Phonetics* 56, 52–65,PMC4805126,全文已讀)用超音波確認了英語軟顎音在前母音前的前移:
> "the difference in closure location on the palate between onsets in the words k[ey] and c[ough] ... is large enough to be noticed by naïve speakers despite being allophonic"

而該文轉述 Keating & Lahiri (1993)(⚠️ **二手**,原文未讀)給出了關鍵數字:
> "Keating and Lahiri (1993) ... conclude that **the prominent frequency peak in the burst spectrum is distinct for all five contexts and varies systematically with vowel frontness.** ... A closer examination of the frequency peaks shows a rather large difference between **front vowel contexts (about 3,000 Hz) and back vowel contexts (1,000–1,500 Hz).**"

**→ 軟顎音的 burst 頻譜峰值在前母音與後母音間差了兩倍以上。**Keating & Lahiri 的結論是舌體前後對軟顎音**沒有內在目標**,完全由協同構音決定 —— 這正是固定 burst 的合成器會失敗的原因。

**對照組**:[[fox2020]] 用 Klatt 合成 **/ba/–/pa/**,方法段原文:
> "**The onset noise-burst was 2 ms in duration and had constant spectral properties across all stimuli.**"

**一個 2 ms、頻譜固定的 burst,對唇音是站得住的設計。**(這個對照是我的推論,Fox 等人沒有討論部位選擇。)

⚠️ **初稿在此推論「所以對軟顎音必然失真」—— 這一步經查證後站不住,必須修正。**
[[軟顎音證據補充]] §二查到 [[klatt1980]] Table III 的標題原文就寫著 "Parameter values for the synthesis of selected components of English consonants **before front vowels**",內文並重申「Values presented in the table are appropriate only for consonants before front vowels」。

**→ 用 KlattGrid 做「軟顎音 + /i/」時,Table III 的值本來就是正確的參數組。真正的錯誤是拿同一組 burst 跨前後母音使用 —— 而 AVWM 的母音是固定的。**

**因此「軟顎音難合成」在固定母音的設計裡站不太住。**這是本回顧在查證過程中被推翻的一個推論,保留在此以免重蹈。§8.2 已據此改寫。

### 3.3 軟顎音 + 前母音在知覺上靠近 /tʃ/ ——「前移」正確,「顎化」誇大

Guion, S. G. (1998). *Phonetica* 55(1–2), 18–52, doi 10.1159/000028423(⚠️ **僅讀摘要**):
> "Voiceless velar stops may become palatoalveolar affricates before front vowels. ... It is shown that **velars before front vowels are both acoustically and perceptually similar to palatoalveolars.**"

**對一個需要子音身分毫不含糊的 GRT 設計,這是實質風險。**(此推論為我所加。)

⚠️ **但用詞必須節制。**[[軟顎音證據補充]] §一查到 Keating & Lahiri (1993) 的結論原文:
> "**Contextual fronting of velars is a gradient effect, less extreme than phonemic palatalization of velars**"

**→ 說軟顎音在 /i/ 前「前移」正確;說它「顎化」則誇大。**三者(脈絡前移、音位顎化、真正的硬顎音)彼此可分。論文用詞應寫「前移 / fronting」,不要寫「顎化 / palatalization」。

不過無論用哪個詞,對 AVWM 的實質意義不變:**這是一個隨母音變動的額外變異來源**,而 AVWM 需要的是「除了 VOT 之外什麼都不動」。

---

## 4. 母音脈絡:/i/ 是對的 —— 而且它與軟顎音衝突

[[winn2020]] §II.D(全文已讀)原文:

> "**the /ɑ/ vowel context could be a particularly unfortunate choice** for experimenters hoping to isolate auditory processing of a purely temporal nature. **Conversely, the /i/ context would be far less affected by VOT cutback**, since (1) its formants are more stable across time in general and (2) the F1 of /i/ is already low ... **F1 for /i/ simply remains at a low frequency regardless of the amount of vowel cutback, thus offering no covarying cue for VOT.**"

他要避開的混淆有多大:
> "The difference of 300 Hz in F1 ... occupies roughly 3 mm of cochlear space, which is roughly **10% of the tonotopic range** of the basilar membrane in an adult human"

**這個建議是通用的、不限部位**,而且他明確點名兩種脈絡:"e.g., for **/bɑ/-/pɑ/** sounds or **/dɑ/-/tɑ/** sounds"。

**F1 混淆的量化參考**(⚠️ **二手**,轉引自 Benkí 2005):Kluender (1991) *JASA* 90, 83–96 報告 F1 起始差 400 Hz 約值 **7 ms 的 VOT 邊界位移**(跨三個部位平均)。

### 4.1 ⚠️ 這個衝突沒有人寫過 —— 但它只咬軟顎音

**明確的負面結果**:[[winn2020]] 全文檢索,**"palatal" 出現 0 次**;"velar" 只出現 3 次(兩次在 VOT 範圍段、一次在 burst 頻譜段)。**他推薦 /i/,卻從未提及軟顎音前移、顎化、或他的母音建議與子音選擇之間的任何交互作用。兩個建議並存於同一篇論文而從未被調和。**

targeted 檢索(Europe PMC、Crossref、四輪網路搜尋)也找不到任何討論此權衡的論文。**這是真實的文獻空白。**

**但實務上這個衝突會自己消失 —— 只要選唇音。** /bi/–/pi/ 完整享有 Winn 的 F1 好處,而且完全沒有顎化問題。**被雙重詛咒的只有 /gi/–/ki/。**

⚠️ **一個與部位無關的 /i/ 注意事項**([[chodroff2017]] 原文):
> "Longer VOTs are observed before high and tense vowels, particularly [i], for voiceless stops (Klatt, 1975; ...)"

**→ /i/ 脈絡的連續體端點應比 Winn Table I 的(非母音特定的)數值稍微往長的方向調。**

---

## 5. 文獻先例:唇音是合成 VOT 連續體的主場

| 研究 | 連續體 | 部位 | 方法 | 閱讀狀態 |
|---|---|---|---|---|
| Abramson & Lisker(Haskins legacy set) | /ba/–/pa/ | **唇音** | Haskins 共振峰合成器 | 官網頁面已讀 |
| [[fox2020]] *eLife* 9:e53051 | /ba/–/pa/ | **唇音** | Klatt KLSYN88a | 方法段已讀 |
| [[zuk2013]] *PLoS ONE* 8:e80546 | /ga/–/ka/ | **軟顎音** | Klatt-based | 方法段已讀 |
| [[goldenberg2022]] | pa/ba **與** ka/ga | **兩者** | 自然,漸進縮短送氣 | 全文已讀 |
| *Sci. Rep.* 14:28825 (2024), PMC11582665 | **beach/peach** + dime/time | **唇音(+/i/!)** | Praat 自然漸進 cross-splicing | 全文已讀 |
| Benkí 2005, ISB4 240–248 | bossy/posse | **唇音** | Klatt & Klatt (1990) cascade | PDF 已讀 |
| [[silbert2012]] / [[silbert2014]] | — | **唇音 / 唇音+舌尖音** | 自然錄音 + 噪音 | 見各卡 |
| [[mcmurray2008]] Exp 1 | /b/–/p/ 系列詞 | **唇音** | 自然 cross-splicing | 見卡 |

**兩個觀察:**

1. **領域史上最常被重用的合成 VOT 連續體(Haskins 的 Abramson/Lisker 組)就是唇音。**
2. ⭐ **`beach/peach` —— 唇音 + /i/ + 自然漸進 cross-splicing —— 已經有已發表的使用先例**(*Sci. Rep.* 2024, PMC11582665)。**AVWM 想做的那個設計不是自創的。**

**粗略的分佈指標**(⚠️ Europe PMC 的**詞彙共現**計數,**不是**經整理的研究計數,含偽陽性,**不可當作調查數據引用**):「ba+pa+VOT continuum」51、「da+ta」39、「ga+ka」13。方向與上表一致。

**Winn 自己的例子刻意保持部位中立**(§IV.A):"like **deer/tier, big/pig, goat/coat**, etc." —— 三個部位各給一個。

⚠️ **明確的負面結果**:**沒有任何論文說某個部位比較好合成或比較難合成,也沒有任何方法段以合成品質為理由解釋部位選擇。**

---

## 6. 沒有查到的東西

1. **各部位 burst 時長(ms)的數值** —— 完全查無。本回顧最弱的一項。**不要寫「軟顎音 burst 較長」。**
2. ~~軟顎音多重 burst 的發生率統計~~ —— **✅ 已補上**,見 §3.1 與 [[軟顎音證據補充]](Barrera-Pardo 2023:軟顎音 67.28%、唇音 33.92%、舌尖音 15.78%)。
3. **Lisker & Abramson (1964) 原文** —— 出版社 403。英語平均值僅有二手來源(Chen, Chao & Peng 2007 的 Table 1 重製:/b/ 1, /d/ 5, /g/ 21;/p/ 58, /t/ 70, /k/ 80 ms)。**引用須標明轉引。**
4. **Lisker & Abramson (1970)** 的知覺邊界值 —— 會議論文集,遍尋不獲。
5. **Benkí (2001)** *J. Phonetics* 29(1), 1–22, doi 10.1006/jpho.2000.0128,「Place of articulation and first formant transition pattern both affect perception of voicing in English」—— **這是唯一一篇正面交叉「部位 × F1」的論文,付費牆擋住。強烈建議透過館藏取得。**光是標題就說明部位對 F1 混淆不是中性的。
6. **Volaitis & Miller (1992)** *JASA* 92, 723–735 —— 經典的唇音 vs 軟顎音類別內部結構比較,出版社 403。
7. **Cho & Ladefoged (1999)** 全文 —— 封閉取用。
8. **Keating & Lahiri (1993)** 全文 —— 僅二手。
9. **任何正面比較三部位在 VOT 實驗中優劣的研究** —— **查無,真實空白。**

---

## 7. 子音-母音**配對**:兩個決定其實不獨立

前面六節把「選哪個子音」與「選哪個母音」當成兩個決定。本節處理它們的交互作用,以及 AVWM 特定情境(**單一 CV 音節、單獨呈現、適應式程序**)下的配對問題。

### 7.0 每條證據的刺激層次總表

AVWM 的目標情境是 **單一 CV 音節、單獨呈現**(實測 `be.wav` 566.7 ms / `pe.wav` 585.8 ms,每試次一個)。下表標明本回顧每條證據的原始刺激層次,以及它能不能直接外推過來。

| 證據 | 用在哪一節 | 原始刺激層次 | 可外推? |
|---|---|---|---|
| [[winn2020]] 的知覺邊界值(20–25 / 35 / 40 ms) | §1.1 | **單一音節辨識**(原文 "simple single-syllable recognition situations") | ✅ **正是目標層次** |
| [[winn2020]] 的腳本與工作範例 | §5 | **詞**(deer/tier, big/pig, goat/coat) | ⚠️ 方法可移植,但詞彙效果不適用於非詞音節 |
| [[fox2020]] 的邊界(20–30 ms)與 Klatt 參數 | §1.1, §3.2 | **合成 CV 音節,300 ms,單獨呈現** | ✅ **正是目標層次**(唯一差別是母音 /ɑ/) |
| [[goldenberg2022]] 的 acuity 2.0 vs 1.1 | §2 | CV 音節連續體(pa/ba, ka/ga)+ 一條**詞**連續體(head/hid)作控制 | ⚠️ 層次相符,**但母音是 /ɑ/**(§7.5) |
| [[chodroff2017]] 的產出平均與 SD | §1.2 | **孤立語與連續語語料庫**(詞與連續語音,非 CV 音節) | ⚠️ **層次不符**;數值供參考,不宜當 AVWM 的精確預期 |
| Barrera-Pardo (2023) 多重 burst 比例 | §3.1 | 語料庫(⚠️ **單位未確認**,例子如 "kids" 看起來是**詞**) | ⚠️ **層次可能不符** —— 見下方警告 |
| [[chodroff2014]] burst 頻譜(產出) | §2.1, §3 | **CVC 音節**(18 名大學生 × 六塞音 × 十母音) | ⚠️ CVC 非 CV,但接近 |
| [[chodroff2014]] TIMIT 語料庫部分 | §3 | **朗讀句子(連續語音)** | ❌ 層次不符 |
| [[chodroff2014]] 知覺實驗 | §2.2 | cross-spliced VOT × burst 連續體(唇音+舌尖音) | ✅ 接近目標層次 |
| [[frisch2016]] 軟顎音前移 | §3.2 | **單音節詞**(key, cough…),超音波構音 | ⚠️ 詞層次,且是**產出**不是知覺 |
| [[kingston1983]] 雙重 burst | §3.1 | [kʰ, sk, g, tʰ, st, d] 在 [i, ʌ, u] 前 —— **音節層次** | ✅ 層次相符(但僅會議摘要) |
| [[silbert2012]] / [[silbert2014]] | §5 | **自然產出的無意義 CV 音節,噪音遮蔽,單獨呈現** | ✅ **正是目標層次,且是 GRT** |
| [[mcmurray2008]] | §5 | **詞**(b-/p- 起始的真詞) | ❌ 詞層次,有詞彙效果 |
| [[burst-vot-tradeoff]] 的 3 ms | §8.3 | Keating: 波蘭語**詞**;Nittrouer: **/dɑ/–/tɑ/ 音節**(兒童) | ⚠️ 混合 |
| [[logan1989]] MRT 錯誤率 | (見另一回顧) | **單音節詞** | ⚠️ 詞層次 |

**⚠️ 三個因此需要下修權重的地方:**

1. **[[goldenberg2022]](§2)** —— 層次相符,但母音是 /ɑ/。已在 §2 與 §7.5 下修。
2. **[[chodroff2017]] 的產出數值(§1.2)** —— 來自詞與連續語音的語料庫。**「軟顎音間距最窄」這個由我計算的結論,是在詞/連續語音的層次上成立的,不保證在單獨呈現的 CV 音節上成立。**孤立語與連續語的數值本身就差很多(如 /kʰ/ 99 vs 56 ms),說明層次確實會改變數值。**§8.1 表的第 5 列權重應視為「弱到中等」而非「中等」。**
3. **Barrera-Pardo (2023) 的多重 burst 比例(§3.1)** —— ⚠️ **我未能確認分析單位是詞還是音節。**若是連續語音或詞中的塞音,則釋放的完整程度、語速、與後接脈絡都與「單獨呈現、清楚發音的 CV 音節」不同,**67.28% 這個比例不保證能外推**。單獨、清楚地念一個 CV 音節時,釋放通常更完整、更受控。**引用這個數字時必須標明它的來源層次。**

**一個相反方向的提醒**:AVWM 的刺激是**單獨呈現的非詞/詞音節**,沒有句子脈絡、沒有語速變異、沒有前後協同構音。這意味著**大部分來自連續語音的變異來源在 AVWM 都不存在**。因此層次不符時,通常的方向是**文獻高估了 AVWM 會遇到的變異**,而不是低估 —— 這對整體結論是有利的,但不能拿來當作忽略層次差異的藉口。

### 7.1 Winn 的 /i/ 論證對唇音成立嗎?—— 成立,而且他點名了唇音

這是配對問題的第一個關鍵:**Winn 推薦 /i/ 的論證,是針對某個發音部位提出的嗎?**

**不是。經全文查證,他的機制完全建立在「母音本身的 F1 行為」上**([[winn2020]] §II.D 原文):
> "the F1 of /i/ is already low, meaning that the upward F1 transition common to the other vowels would be minimized. **F1 for /i/ simply remains at a low frequency regardless of the amount of vowel cutback, thus offering no covarying cue for VOT.**"

F1 cutback 的混淆來自**母音的 F1 高度**,不是子音的部位。所有塞音在閉塞期的 F1 都很低,差別在於母音把 F1 拉多高 —— /ɑ/ 拉得高(所以 cutback 造成大的 F1 差),/i/ 本來就低(所以幾乎不變)。

**而且他明確把唇音列為受害者之一**(原文):
> "In some previous studies where the vowel environment /ɑ/ was used (**e.g., for /bɑ/-/pɑ/ sounds** or /dɑ/-/tɑ/ sounds), it is impossible to disentangle the potential confound of formant cues that accompany changes in VOT."

**→ /bɑ/–/pɑ/ 被點名為壞例子,而它的修正版正是 /bi/–/pi/。Winn 的建議對唇音不但成立,唇音還是他舉的第一個例子。**證據強度:**強**(全文已讀,論證機制清楚)。

### 7.2 ⚠️ 但 be/pe 有兩個實測出來的殘留混淆(本節為我的實測,非文獻)

我直接量了專案現有的 `be.wav` / `pe.wav`,並讀了 `snr_audio.py` 的混音邏輯。**發現兩個與 VOT 無關、但與 token 身分完全相關的差異。**

**(a) 語音起始時間差 36 ms**

| | 檔案總長 | 語音起始 | 有聲段長度 |
|---|---|---|---|
| `be.wav` | 566.7 ms | **13.0 ms** | 250.5 ms |
| `pe.wav` | 585.8 ms | **49.0 ms** | 233.1 ms |

(以最大振幅的 0.5%–5% 為門檻掃描,結果穩定:Δ起始 35–36 ms、Δ有聲段 −17 ms。)

`snr_audio.py` 的 `mix_components()` 用 `sp[lead:lead+len(x)] = x`,把噪音固定提前 `NOISE_LEAD_MS = 200` ms **從檔案開頭**算起。因此**從噪音起始到語音起始的間隔**是:be 213 ms、pe **249 ms**。

⚠️ **噪音起始是一個聽得見的時間地標,而語音相對於它的延遲差了 36 ms —— 這比 /b/–/p/ 的整個知覺邊界區(20–25 ms)還大。**原始碼註解已經意識到「噪音的起始點等於告訴受試者語音在哪」而加了 lead;但**兩個 token 的檔內前導靜音不等長**這件事沒有被處理。

**建議**:把兩個 token 的前導靜音裁齊(或以偵測到的語音起始對齊後再補靜音)。這是低成本的修正。

**(b) 有聲段的實際位準差 0.30 dB**

`TARGET_RMS` 的正規化是**對整個檔案**(含靜音)做的,而兩個 token 的靜音佔比不同(be 43.0%、pe 40.1%)。實測結果:

| | 整檔 RMS | **有聲段 RMS** |
|---|---|---|
| `be` | 0.05000 | 0.07623 |
| `pe` | 0.05000 | **0.07895** |

**→ 語音實際發聲的那段,pe 比 be 大 0.30 dB,因此兩個 token 的「實際 SNR」也差 0.30 dB。**

原始碼註解說正規化是為了修正「實際值會差 0.7 dB」的問題 —— 它把差距從 0.7 dB 縮到 0.30 dB,但沒有歸零,因為正規化的分母含靜音。

**建議**:改成對**有聲段**計算 RMS 再正規化。

⚠️ **這兩點都不是選唇音的理由,也不影響 §8.1 的結論** —— 它們是**現有實作的施工問題**,換成 /d/–/t/ 或任何自然 token 都會重新出現。列在這裡是因為它們正是「配對層次」才看得到的東西。

### 7.3 詞彙地位:be/pe 是平衡的,/gi/–/ki/ 不是

這一條在文獻上有明確的機制,但據我所知**沒有人把它當成配對選擇的準則**(以下推論為我所加,機制引自已核實的文獻)。

[[burton-blumstein-naturalness]] 記錄的 Ganong 式**詞彙效果**:當連續體的一端是詞、另一端不是詞時,類別邊界會朝「變成詞」的方向偏移。把三組配對按詞彙地位排:

| 配對 | 有聲端 | 無聲端 | 平衡? |
|---|---|---|---|
| **/bi/–/pi/**(be/pe) | be、bee、字母 B | pea、pee、字母 P | **✅ 兩端都是常用詞 + 字母名** |
| /di/–/ti/ | dee、字母 D | tea、tee、字母 T | ✅ 平衡 |
| /bɑ/–/pɑ/ | (非詞) | (非詞) | ✅ 平衡(兩端都不是詞) |
| **/gi/–/ki/** | ghee(罕用) | **key(高頻)** | ❌ **嚴重不平衡** |

**→ /bi/–/pi/ 在詞彙地位上是平衡的,這是它一個未被提及的優點;/gi/–/ki/ 則是本回顧發現的、軟顎音的第 N 個問題。**

⚠️ **而且這一條對 AVWM 特別要緊**:[[burton-blumstein-naturalness]] (1995) 的結論是詞彙效果的出現**取決於 stimulus quality(訊號是否被噪音劣化)**,而**不是** naturalness。**AVWM 的 SNR 路線正是刻意把訊號劣化到閾值附近 —— 也就是最容易讓詞彙效果冒出來的條件。**配對的詞彙平衡因此比一般實驗更重要。

⚠️ 但要標明:be/pe 兩端**都是**詞,這意味著詞彙效果(若出現)會**雙向**作用,而不是單向偏移。這比一端是詞好,但不等於沒有效果 —— 兩個詞的**頻率**未必相等,我沒有查詞頻。

### 7.4 唇音 + /i/ 有沒有自己的問題?

**(a) F2 transition 的量級**:唇音的 F2 locus 低,而 /i/ 的 F2 很高,因此 /bi/ 的 F2 transition 是一段大幅上升。直覺上這像是個問題(cutback 會削掉一部分 transition)。

**但依 [[winn2020]] 的方法,這不構成問題(我的推論)**:progressive cutback and replacement 是把母音起始**換成同一個發音部位的無聲 token 的送氣段**,共振峰軌跡仍然在,只是被去嗓音化。Winn 的核心主張正是「送氣不是貼在母音前的音段,而是母音起始的去嗓音化」——**F2 transition 被保留為無聲形式,而不是被刪除**。若走合成路線,F2 軌跡是明確設定的參數,更不成問題。

⚠️ 我沒有找到任何文獻直接處理「唇音 + 高前母音的 F2 transition 對 VOT 連續體是否構成問題」。**這一段是推理,不是查證結果。**

**(b) /i/ 前的 VOT 本來就比較長**([[chodroff2017]] 原文):
> "**Longer VOTs are observed before high and tense vowels, particularly [i]**, for voiceless stops (Klatt, 1975; Port & Rotunno, 1979; Weismer, 1979...)"

**→ /i/ 脈絡的連續體端點與邊界預期,都應比非母音特定的通用值(如 [[winn2020]] Table I 的 3→60 ms)往長的方向調。**這是配對層次才看得到的修正。⚠️ 我未取得 Klatt (1975) 原文,不知道位移的確切量級,也不知道它是否隨部位不同。

### 7.5 有沒有研究直接比較過不同 CV 配對?

**目前查無。**我沒有找到任何研究在同一個實驗裡比較 /bi/–/pi/ 與 /bɑ/–/pɑ/(或其他配對)在 VOT 辨識上的邊界位置、斜率或信度。

最接近的是 [[goldenberg2022]] —— 但它比較的是**部位**(pa/ba vs ka/ga),**母音固定為 /ɑ/**,所以它回答不了母音配對的問題。**而且要注意:它用的是 /ɑ/,正是 [[winn2020]] 明確不推薦的那個母音**,因此它測到的斜率差異有多少來自部位、有多少來自 /ɑ/ 的 F1 混淆與部位的交互作用,**無法從該研究分離**。

⚠️ **這一點下修了 §2 那條「決定性證據」的權重:軟顎音在 /ɑ/ 脈絡下辨識函數較淺,不保證在 /i/ 脈絡下也較淺。**§8.1 的表已據此標注。

---

## 8. 建議

### 8.1 選 /b/–/p/ + /i/(維持 be/pe)

依證據強度排序:

| # | 理由 | 來源 | 強度 |
|---|---|---|---|
| 1 | **軟顎音辨識函數寬約兩倍且邊界偏斜**;唇音邊界置中。⚠️ **但測的是 /ɑ/ 脈絡,不是 AVWM 的 /i/**(§7.5) | [[goldenberg2022]] 直接組內比較 | **中等偏弱**(母音脈絡不符) |
| 2 | **軟顎音 burst 頻譜隨母音差兩倍以上**(前母音 ~3000 Hz vs 後母音 1000–1500 Hz);唇音則可用 2 ms 固定 burst 且已有發表實作。⚠️ 但**固定母音的合成設計不受此害**(§3.2) | [[frisch2016]]、Keating & Lahiri(二手)、[[fox2020]] | **中等**(自然路線)/ **弱**(固定母音的合成路線) |
| 3 | **軟顎音 67.28% 有多重 burst**(唇音 33.92%),/k/ 的 VOT 起點有 **14.18 ms** 地標歧義(p<.001, d=0.82) | Barrera-Pardo (2023) 見 [[軟顎音證據補充]];機制見 [[kingston1983]] | **強**(自然路線)/ **弱**(合成路線) |
| 4 | **/i/ 有明確方法學背書**,而 /i/ 正是軟顎音**前移**最明顯的環境(不是「顎化」,§3.3);唇音完全繞開 | [[winn2020]] §II.D + Keating & Lahiri (1993)、Guion 1998 | **強**(Winn)/**中等**(衝突為我的推論) |
| 5 | **唇音有聲錨點最低、間距最寬、有聲端變異最小** → 適應程序空間最大。⚠️ 但語料是**詞與連續語音**,非單獨 CV 音節(§7.0) | [[chodroff2017]](我的算術) | **弱到中等**(層次不符) |
| 6 | **唇音是合成與自然 VOT 連續體的主場**,且 beach/peach 已有先例 | §5 | **弱**(便利樣本) |
| 7 | 實務:be/pe 是現有素材,`snr_audio.py` 已完成 | 專案內部 | — |

**舌尖音 /d/–/t/ 是合格的第二順位。**沒有查到針對它的專屬缺點,而且是 Keating/Nittrouer 那條 VOT 文獻的主場([[burst-vot-tradeoff]])。若 be/pe 錄音有問題,換 /d/–/t/ 不需重新論證。

**軟顎音 /g/–/k/ 應排除。**

### 8.2 ⚠️ 但軟顎音的缺點強度**取決於走哪條路線**

這一節被改寫過兩次,兩次都是被證據推翻的,值得保留過程:

- **初稿推測**:走合成路線時軟顎音反而較誠實(它本來就沒有 burst 頻譜的 voicing 線索,[[chodroff2014]])。→ **推翻**,因為軟顎音的 burst 頻譜隨母音劇烈變動(§3.2)。
- **第二版推論**:所以軟顎音在兩條路線上都差。→ **也推翻**,因為 [[klatt1980]] Table III **本來就是前母音專用的參數組**,固定母音的合成設計不會踩到那個坑(§3.2、[[軟顎音證據補充]] §二)。

**目前的正確版本**([[軟顎音證據補充]] §四):

| 軟顎音的問題 | 自然 token + 噪音路線 | KlattGrid 合成路線 |
|---|---|---|
| /i/ 前前移 | 有影響(額外變異來源) | 有影響(要用對的參數組) |
| burst 頻譜隨母音變 | 有影響 | **固定母音就不成問題** |
| **多重 burst(67.28%,/k/ 有 14 ms 地標歧義)** | **嚴重** | **幾乎不適用**(自己放一個乾淨的 burst) |
| 辨識函數又淺又偏([[goldenberg2022]]) | 有影響 | 有影響 |

**→ 軟顎音的缺點在自然路線上成立且嚴重;在合成路線上大幅減弱,主要只剩前移與辨識函數那兩項。**

**由於專案目前傾向自然路線**([[natural-vs-synthetic-speech]] §6、[[決策脈絡_聽覺維度]]),**§8.1 的 /b/–/p/ 建議維持不變,而且現在證據更完整。**但若日後改走合成路線,軟顎音的排除理由會弱掉一大半,屆時應重新評估。

**唇音在兩條路線上都好:**SNR 路線上它的 burst 頻譜 voicing 線索最強([[chodroff2014]] 預測 /p/–/b/「if anything stronger」),而且多重 burst 比例只有軟顎音的一半;合成路線上它的 burst 可以合理地固定([[fox2020]] 的實作證明)。

### 8.3 論文寫作注意

1. **不要寫「文獻建議用唇音」。**沒有這回事。正確寫法:「唇音在 X、Y、Z 上有優勢,且未發現針對它的特定缺點」。
2. **引用 [[chodroff2014]] 的軟顎音結果時必須寫成產出/聲學層次**,不是知覺虛無結果(詳見該卡的引用查核)。
3. **引用部位 VOT 數值時**:優先用 [[chodroff2017]](現代大語料庫、可直接取得);要用 Lisker & Abramson (1964) 的數字必須標明轉引。
4. **引用 3 ms burst trading relation 時標明它來自波蘭語資料**([[burst-vot-tradeoff]])。
5. **/i/ 脈絡的端點要比 Winn Table I 稍往長調**(§4.1)。
6. **不要寫「軟顎音 burst 較長」** —— 查無來源(§6.1)。可以寫的是「多重 burst 較常見」(有數據)。
7. **用「前移 / fronting」,不要用「顎化 / palatalization」** —— Keating & Lahiri (1993) 明說前者是 gradient 且弱於後者(§3.3)。
8. **軟顎音的排除理由要標明它與路線耦合**(§8.2),不要寫成無條件的結論。

---

**相關卡片**:[[goldenberg2022]] · [[kingston1983]] · [[frisch2016]] · [[chodroff2017]] · [[chodroff2014]] · [[chodroff2019]] · [[fox2020]] · [[burst-vot-tradeoff]] · [[winn2020]] · [[abramson2017]] · [[silbert2012]] · [[silbert2014]] · [[mcmurray2008]] · [[zuk2013]] · [[klatt1980]]
**其他回顧**:[[natural-vs-synthetic-speech]] · [[synthetic-speech-cognitive-load]] · [[軟顎音證據補充]] · [[子音混淆最小化]](本篇處理「哪個部位的 VOT 連續體較好合成/較不易混」;[[子音混淆最小化]] 處理「voicing 這個特徵本身、以及 b–p/d–t/g–k 三對,在混淆矩陣文獻裡誰的知覺混淆最小」——兩者互補,結論一致:都支持 /b/–/p/。)
**專案決策脈絡**:[[決策脈絡_聽覺維度]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

### 8.4 ⚠️ 必須修的兩個實作問題(§7.2 實測)

這兩項與選哪組子音無關,但**在跑正式實驗前必須處理**:

1. **裁齊前導靜音。**`be.wav` 語音起始 13.0 ms、`pe.wav` 49.0 ms;`snr_audio.py` 的 `NOISE_LEAD_MS` 從**檔案開頭**算起,因此「噪音起始 → 語音起始」的間隔是 be 213 ms vs pe **249 ms**。**36 ms 的系統性差異,比 /b/–/p/ 的整個知覺邊界區(20–25 ms)還大**,而噪音起始是聽得見的時間地標。
2. **改用有聲段 RMS 正規化。**目前 `TARGET_RMS` 對整檔(含靜音)正規化,而兩檔靜音佔比不同(43.0% vs 40.1%),導致**有聲段實際位準差 0.30 dB**,亦即兩個 token 的實際 SNR 差 0.30 dB。原始碼註解說正規化是為了修正 0.7 dB 的差距 —— 它修到剩 0.30 dB,沒有歸零。

⚠️ 兩項都是我在本次回顧中實測 + 讀 `snr_audio.py` 得到的,**不是文獻**。數值可用 `python3 -c` 重現。

### 8.5 刺激層次的注意事項(2026-08-12 追加條件)

1. **§7.0 的總表列出每條證據的原始刺激層次。**引用時務必標明,尤其 [[chodroff2017]](詞與連續語音)與 Barrera-Pardo 2023(單位未確認)。
2. **不要把 [[goldenberg2022]] 的 acuity 差異當成「軟顎音在 /i/ 前也比較淺」** —— 它測的是 /ɑ/(§7.5)。
3. **層次不符時的方向通常對 AVWM 有利**(單獨呈現的 CV 音節變異來源比連續語音少),但這不是忽略差異的理由。
4. **仍然查無**:任何直接比較不同 CV **配對**(/bi/–/pi/ vs /bɑ/–/pɑ/ 等)在 VOT 辨識上表現的研究(§7.5)。
