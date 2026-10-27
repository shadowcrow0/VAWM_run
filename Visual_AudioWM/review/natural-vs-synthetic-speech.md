# 語音知覺實驗該用自然刺激還是合成刺激

**綜合回顧 · 2026-08-12**
針對 AVWM 的 2×2 GRT(顏色 × 聽覺)實驗,聽覺維度該走 KlattGrid 合成 VOT 連續體,還是自然 be/pe token + SNR 遮蔽。

單篇文獻卡在 `90_Sources/`,本文用 `[[ ]]` 連過去。**每一條主張後面標注證據強度與我的閱讀狀態;凡是我的推論而非原文陳述,都明確標出。**

---

## 0. 先把問題問對

「自然還是合成」聽起來像一個問題,實際上是三個彼此獨立的問題疊在一起。文獻上的混亂,大半來自沒把它們拆開。Burton & Blumstein 自己花了六年才把前兩個拆乾淨([[burton-blumstein-naturalness]]):

| 軸 | 文獻用語 | 在 AVWM 裡的具體內容 |
|---|---|---|
| **A. 自然度** | stimulus naturalness | 次要線索(F1、F0、送氣振幅、burst 頻譜)有沒有跟 VOT 一起共變 |
| **B. 品質** | stimulus quality | 訊號被噪音劣化的程度 |
| **C. 合成器身分** | — | 訊號是參數式生成的,還是自然錄音經編輯的 |

AVWM 的兩條路線**不是在同一個軸上對立**:

- **合成路線** = 低自然度(F1 釘死)+ 高品質(無噪音)+ 參數式生成。難度旋鈕轉在 **ΔVOT**。
- **SNR 路線** = 高自然度(全部線索保留)+ **可變品質** + 自然錄音。難度旋鈕轉在 **噪音**。

這個拆解一開始就有一個後果:**兩條路線的難度旋鈕,踩在不同的軸上,而這兩個軸在文獻裡的風險紀錄不一樣。**後面第 5 節會回到這一點。

---

## 1. 有直接比較嗎?有,而且結論比預期樂觀

### 1.1 可辨識度:在 CV 音節首,最好的合成器與自然語音無異

[[logan1989]] 是這個問題的標準答案,而且數字非常具體(Modified Rhyme Test,錯誤率 %):

| 系統 | **音節首** | 音節尾 | 整體 |
|---|---|---|---|
| 自然語音 | **0.50** | 0.56 | 0.53 |
| DECtalk 1.8 Paul | **1.56** | 4.94 | 3.25 |
| MITalk-79 | 4.61 | 9.39 | 7.00 |

作者的檢定結論(原文):
> "Comparisons of the error rates for consonants in initial position indicated **no significant differences between natural speech and DECtalk 1.8 Paul**"

**注意音節首 / 音節尾的不對稱:** DECtalk-Paul 在音節尾差了將近十倍,在音節首只差 1.06 個百分點且不顯著。**一個 CV 音節整個落在有利的那一區。**這是本回顧中對合成路線最強的一條支持證據,證據強度高(全文已讀,表格直接取自 PMC)。

⚠️ 兩個限定。第一,DECtalk 是多年調校的成熟系統;「Klatt 家族做得到」不等於「我手刻的 KlattGrid 參數做得到」。這是**能力上限**的證據,不是我的實作的證據。第二,作者自己在摘要裡就先擋了一句:

> "Substantial differences in performance can be anticipated ... when synthetic speech, even very high-quality synthetic speech, is presented **in noise, under conditions of high cognitive load**"

**AVWM 兩個條件都佔** —— 它是工作記憶作業,而 SNR 路線還要主動加噪音。這句話幾乎是專門寫給本專案的。

### 1.2 實驗效果能不能複製:能,但這個問題有一段不光彩的歷史

最直接的一筆是 [[mcmurray2008]]。同一個實驗室先用合成連續體發現了類別內 VOT 的漸進效果(McMurray, Tanenhaus & Aslin, 2002),再用 cross-splicing 做的**自然**連續體重做一次:

> "Experiment 1 demonstrated gradient effects along VOT continua made from natural speech, **replicating results with synthetic speech**"

**效果跨刺激來源存活。**但要注意這是**跨研究**的準複製(不同年份、不同受試者),不是同一批人身上的對照實驗;證據強度中等。

而作者為什麼要做這個檢查,才是重點。他們在導論裡寫:

> "some of the effects documented with single-cue variation, as studied in the laboratory with synthetic speech, **may not generalize to natural speech stimuli**, which have a richer set of correlated cues."

這個顧慮有真實案例撐著,而且**是失敗案例**:

- **[[burton-blumstein-naturalness]] (1989)**:Ganong 式的詞彙效果,在把連續體做得更接近自然語音參數值之後 —— **"the lexical effect disappeared."**
- **[[shinn1985]]**:Miller & Liberman (1979) 用合成刺激建立的音節時長脈絡效果,換成較不骨架化的刺激後 **消失**。
- **[[hamilton2020]]** 指出視覺科學有同樣的歷史:"many effects assumed to be universal were actually highly dependent on the tightly controlled stimuli, and were diminished or absent in experiments that used natural visual stimuli."

**這是跨領域重複出現的失敗模式,不是語音學的偶發事件。**

但故事有兩次轉折,兩次都讓合成路線好過一些:

1. **Miller & Wayland (1993)**:那個「消失」的脈絡效果,把同樣的自然刺激**放進多人交談噪音**後**又回來了**([[shinn1985]])。
2. **Burton & Blumstein (1995)**:把自然度與品質分開操弄後,發現真正起作用的是 **品質**,**不是** 自然度 —— "the emergence of a lexical effect was influenced by **stimulus quality but not by stimulus naturalness**."

⚠️ 但 1995 那篇的「自然」條件只讓 **burst 與送氣振幅** 共變,**沒有共變 F1** —— 而 F1 才是 [[abramson2017]] / [[winn2020]] 認定最強的次要線索。所以它的「自然」其實仍相當貧乏,「自然度不重要」這個結論的適用範圍因此受限。**不能拿它當合成路線的通行證。**

---

## 2. 合成語音的處理負荷:印象正確,但常見的簡化說法比原文強

> **⚠️ 本節只做摘要。這個題目已另有專門的敘事回顧:[[synthetic-speech-cognitive-load]]。**
> **而且那份回顧得到一個對本文結論很重要的發現:噪音退化的語音與合成語音在工作記憶上是同一個機制,證據還更強。**
> **也就是說,SNR 路線並沒有繞開工作記憶的顧慮 —— 只是換掉了造成退化的來源。**
> **這一點已反映在下面 §6.2 與 §6.3。**

研究者的印象是「Pisoni 有一系列研究說合成語音吃工作記憶資源」。**查證結果:文獻確實存在,方向也對,但三個地方需要修正。**

### 2.1 文獻是真的

[[luce1983]](Human Factors 25(1), 17–32)是旗艦。三個實驗,詞清單回憶。結論句:

> "synthetic speech ... affects the allocation of limited processing resources in short-term working memory."

[[duffy1992]] 是理論整合,[[ralston1991]] 是線上測量(詞監控、逐句聆聽時間)的證據,[[govender2023]] 是 2018/2023 用瞳孔測量做的現代重測。四十年、多種方法、方向一致。**大方向的證據強度:高。**

### 2.2 但簡化說法有三處失真

**(a) 最常被引的「數字預載」結果其實不顯著。** [[luce1983]] 實驗 2 用了 Baddeley & Hitch 的預載典範,結果:

> "**No interaction between voice type and preload was observed for word recall**, F (2, 238) = 1."
> "the data reveal a **trend** ... **although the effect is not statistically significant.**"

作者自評那個支持性指標「at best a crude measure」。

**(b) 「合成語音傷害清單前段」只出現在實驗 3。**實驗 1、2 的序列位置曲線沒有這個解離 —— 需要**依序回憶**這種高負荷作業才做得出來。

**(c) 機制是「時間」,不是「儲存容量」。** [[duffy1992]] 的整合是:

> "because the listener does not normally have control over the rate of presentation of spoken language, **the critical resource during spoken language comprehension is time.**"

辨識變慢 → 在固定的話語時長裡,留給高層理解的時間變少。**這是一個篇章層次的瓶頸。**

### 2.3 對 AVWM 而言,關鍵是這個機制不適用於單一 CV 音節

這是本節的結論,而且是**我的推論**(文獻沒有直接做這個論證):

[[duffy1992]] 所指認的資源耗損機制,定義在**序列**之上 —— 序列順序的編碼、話語時間預算、隨詞數縮放的資源使用。**一個孤立的 CV 音節沒有序列順序要編碼,沒有後續詞在排隊,沒有語意整合會被排擠。**機制在設計上就不咬合。

而且有正面證據:[[logan1989]] 顯示音節首子音上合成與自然**統計上無異** —— 這正是 /ba/–/pa/ 的情形。[[duffy1992]] 也承認,用正確率測量時「with minimal practice, comprehension performance for synthetic and natural speech appear to be roughly equivalent」,而 **AVWM 的依變項正是正確率**(GRT 的混淆矩陣),不是 RT。

### 2.4 兩個仍然會咬人的地方

**(a) 不能用「我的合成品質高」來辯護。** [[francis2009]] 直接否定了這條捷徑:換更好的合成器提升了正確率,**卻沒有**讓 WM 容量被用得更有效率。降低負荷的是**訓練**,不是清晰度。⚠️(此卡僅讀摘要,證據強度中等偏低,但方向明確。)

**(b) 噪音中的 CV 音節,是唯一找到的反例。** [[duffy1992]] 轉述 Clark, Dermody & Palethorpe (1985):自然與合成 CV 音節在噪音中,重複播放能改善自然音的辨識,**卻改善不了合成音**,理由是「the additional redundant cues were not present in the acoustic signal」。

⚠️ **這筆是二手,原始文獻未取得,必須查證。**但它的形狀很值得注意:它不是工作記憶效果,而是**線索冗餘度**效果 —— 而冗餘線索正是合成路線刻意移除的東西。**若 AVWM 走「合成刺激 + 噪音」的組合,這是最該擔心的一條。**

**另外 [[schwab1985]] 提示了一個少被討論的成本**:合成語音的赤字可以被訓練掉(25% → 70%,可遷移、六個月仍保留)。這對合成路線是好消息,但對**適應式程序**是壞消息 —— 底層敏感度會隨練習漂移,適應程序會追著移動中的目標跑。自然刺激因為本來就熟悉,漂移較小。(此為我的推論。)

---

## 3. 範疇知覺 / VOT 文獻:合成刺激會讓知覺看起來**比較不範疇**

這是本回顧中最出乎意料、也對 AVWM 最有實質後果的一節。

直接證據是 [[vanhessen1999]](Phonetica 56, 56–72),而且它問的正是本專案的問題:

> "test the hypothesis that categorical perception of speech stimuli is a function of synthesis quality - specifically, that **the greater complexity of more natural speech stimuli makes it difficult for listeners to focus on particular stimulus parameters as psychoacoustic cues.** The results show that there is **an increase in categorical perception as synthesis quality improves**"

**方向:合成品質越接近自然 → 越範疇化。**反過來說,**貧乏的單線索合成連續體會讓辨識函數變淺。**

**這對適應式程序的後果(我的推論)**:若「範疇化程度」在辨識函數上表現為斜率,那麼合成路線估到的 **β 會系統性地大於**自然聆聽下的真值。這不是「刺激比較難」而已 —— 是**心理計量函數的形狀被刺激製作方式改變了**。對一個要拿 β 當參數的適應程序,這是實質問題。

⚠️ **但這一節的證據強度必須誠實下修為「低到中等」**,原因寫在 [[vanhessen1999]] 卡上:我**只讀到摘要**;摘要把 "sinewave generation" 排在品質最高端並稱之為 "a much more complex type",這與一般理解的 sinewave speech(極不自然)相反。我推測指的是**正弦模型分析合成**,但這是推測。**在讀到全文之前,本節不能當決策依據引用。**

支持性的間接證據有兩條:
- [[schouten1992]]:用**自然**刺激測,結論是塞音知覺「highly categorical」。⚠️ 但 [[mcmurray2008]] 引它來支持「自然比合成更範疇」是一個**跨研究對照的推論**,該篇本身並未在單一研究內比較兩者。這條引用鏈我已在 [[schouten1992]] 卡上查核並更正。
- [[mcmurray2008]] 本身報告:**自然連續體的類別邊界變異(受試者間與 item 間)大於合成連續體。**這對適應程序是直接的實務資訊 —— 自然刺激需要更多試次才收斂,起始猜測要更寬。

至於邊界**位置**會不會變:我找不到任何研究在同一批受試者身上用自然與合成連續體比較過邊界位置。**這是一個明確的文獻空白**,不是我沒找到。

---

## 4. 文獻主張的取捨:沒有人正面論證過哪一邊該優先

我特地找了「有沒有人明確說該優先哪一邊」,**答案是沒有**,而且最該說這話的人反而沉默:

- **[[winn2020]]** 是 VOT 操弄的標準方法學教學,整套建立在自然語音上。但經全文查證:**他從頭到尾沒有提過 Klatt 合成器、共振峰合成或任何合成器作為刺激生成的選項**,也**沒有做過任何自然 vs 合成的正面論證**。他的「自然度」論證是針對**彼此競爭的編輯方法**(哪一種剪接法產生的連續體比較像真的語音),不是針對「錄音 vs 合成器」。他甚至明確中立地寫道 progressive cutback "has been used in a variety of studies using **natural speech** (Repp, 1979; ...) **and synthetic speech** (Ganong, 1980; ...)"。
- **[[hamilton2020]]** 是自然刺激派最強硬的宣言,但作者自己讓出了關鍵一步:"**isolated sentences may be sufficiently natural to study phoneme representations without any penalty.**" —— 連他們都認為音素層次的表徵不需要自然主義刺激。⚠️ 但要小心:他們說的是不需要**更長的脈絡**,不是不在乎**聲學自然度**。拿這段替合成路線背書是誤讀。

所以文獻的真實狀態是:**兩邊都有人用,沒有共識,也沒有人寫過裁決性的論證。**這意味著 AVWM 的選擇必須靠專案內部的理由,而不是靠訴諸文獻權威。

---

## 5. GRT 專屬的論證:正面處理 Silbert 的立場

這是本回顧最關鍵的一節,因為 AVWM 是 GRT 實驗,而 GRT 有它自己的、與生態效度無關的理由。

### 5.1 論證是什麼

[[silbert2012]] 是目前找得到最貼近 AVWM 的已發表前例(2×2 GRT、語音、voicing × manner)。他選自然錄音,理由寫得很明白:

> "**In order to avoid strong assumptions about the relevant acoustic-phonetic dimensions**, naturally produced nonsense syllables were used as stimuli."

而且他用**噪音**調難度,理由同樣是模型內生的:

> "Naturally produced [i.e., not (re)synthesized] tokens can be very acoustically distinct, however, and **identification data with very high accuracy is not particularly informative with respect to perceptual interactions.**"

展開來說:GRT 要估的是知覺分布的形狀與相關。若刺激只沿實驗者選定的單一參數變動,估出來的知覺維度就被那個選擇預先決定了 —— 模型會忠實地報告「VOT 這條軸」,因為那是你唯一給它的軸。

### 5.2 這個論證有多強?—— 前提是領域標準,推論是他個人的

**前提端:非常穩固。** GRT 教學文獻自己就把這件事寫成建模慣例。[[silbert-hawkins2016]](J. Math. Psych. 73, 94–109)原文:

> "The dimensions along which the perceptual distributions and decision bounds are defined are **modeled perceptual dimensions corresponding to the physical dimensions of the stimuli.**"

也就是說,GRT 的輸出永遠是**相對於實驗者所選物理維度**而言的。這不是 Silbert 的怪癖,這是模型結構。

**而且有獨立的第二個聲音。** [[roark2019]](Attention, Perception, & Psychophysics 81, 912–926)來自不同實驗室、不同典範(類別學習)、不同刺激(非語音):

> "These results demonstrate **the need to reconsider the assumption that the orthogonal input dimensions used in designing an experiment are indeed orthogonal in perceptual space**"

**→ 「物理正交 ≠ 知覺正交」不是 Silbert 個人立場,是至少兩個獨立來源提出的顧慮。**

**推論端:是他個人的做法,不是領域共識。** 我對兩份 GRT 教學論文做了全文關鍵詞檢索:

- [[silbert-hawkins2016]]:`synthetic` / `natural speech` / `naturally produced` / `manipulat` —— **全部 0 次命中**。全篇沒有任何一節在談刺激製作方式的選擇。
- [[soto2017]]:談難度操弄時列出三種手段 —— "decreasing image contrast, decreasing presentation times, and **increasing stimulus similarity through morphing**"。前兩者是「劣化訊號」(SNR 路線的類比),**第三者卻是「縮小物理差異」(合成路線縮小 ΔVOT 的類比)**。

**→ GRT 教學文獻對「自然 vs 合成」完全沉默,而且它列出的合法難度操弄手段裡,兩條路線各佔位置。「所以應該用自然刺激」這一步,是 Silbert 在自己實證論文裡的做法,不是教學文獻推導出來的規範。**

### 5.3 有沒有人反駁過?

**沒有找到正面反駁。**但有一個很能說明問題的間接證據:

[[kingston2008]](J. Phonetics 36, 28–54)用**參數控制的刺激 + 非語音類比音**做了一整套 [voice] 的偵測理論分析 —— 這是與 Silbert 相反的方法學選擇,而且是這個文獻裡份量很重的一篇。Silbert 等人 (2009, *J. Phonetics* 37, 339–343) 寫了一篇 addendum 批評它。

**關鍵在於批評的內容:那篇 addendum 針對的是「多變量高斯知覺密度的共變異結構未被探討」,不是刺激的自然度。**⚠️(此為我從摘要做的判讀,addendum 全文未讀。)換句話說,**當 Silbert 真的要批評一個用參數合成刺激的研究時,他用的是共變異結構的論證,而不是他自己的自然度論證。**這暗示他本人也不把自然度當成一個能單獨擊倒對手的理由。

### 5.4 一個反轉:合成路線的賣點,在 GRT 裡並不成立

[[roark2019]] 值得多看一眼,因為它的證據結構有個對 AVWM 很重要的反轉:

**他們用的是完全合成、參數正交的刺激** —— 也就是「合成路線」最理想的版本。結果他們發現這種刺激的維度**仍然不是知覺正交的**。

**→ 合成路線的主要賣點(乾淨的正交線索控制)買到的是物理正交;GRT 要問的可分離性是知覺層次的問題。物理正交不蘊含知覺正交。合成路線並沒有真的買到它看起來買到的那個東西。**

這**削弱**了「為了 GRT 的正交性所以該用合成」這條論證,但**不等於**支持自然刺激 —— 自然刺激的維度同樣可能不知覺正交。正確的結論比較樸素:**知覺可分離性是要被 GRT 估出來的結果,不是靠刺激設計能保證的前提。**[[silbert2014]] 用自然刺激、在教科書等級的 place × voicing 結構上,照樣發現「systematic perceptual deviations」,是同一個訊息。

### 5.5 一個 GRT 內部、支持 SNR 路線的新論證(我的推論)

前面都在談文獻。這裡提一個文獻沒講、但從 GRT 的假設直接推得的論點:

**GRT 的高斯假設,對兩條路線並不對稱。**

- **SNR 路線**:兩個聽覺層次固定是清楚的 /be/ 與 /pe/ 範疇範例,難度來自加性噪音。加性噪音讓知覺分布**對稱地變寬**,這正是 GRT 的等變異高斯圖像。
- **合成路線**:難度來自把兩個 VOT 值往類別邊界靠。但邊界附近正是敏感度**非均勻**的區域 —— [[mcmurray2022]] 雖然駁倒了強版範疇知覺,但仍認定「邊界附近相對敏感度較高」是真實且可重複的。把刺激放在敏感度梯度最陡的地方,知覺分布會被拉扯得偏離高斯。

**⚠️ 這是我的推論,沒有任何文獻做過這個論證,也沒有人量化過偏離的大小。**但它的方向清楚,而且與 [[silbert2012]]([[silbert2014]]、Silbert & Motlagh Zadeh 2018)三次都選噪音而非參數靠近的做法一致。

### 5.6 ⚠️ 但專案內部的 AGRT 假設分析,指向相反的方向

[[決策脈絡_聽覺維度]] 已經用 A1–A5 檢查過兩條路線,結論與 §5.5 **不一致**,必須並陳:

| | 刺激沿維度移動 | 二元反應與維度位置單調相關 | 有習得的界線 α |
|---|---|---|---|
| **VOT / F1 起始** | ✅ | ✅ 報 b/p ↔ 維度位置 | ✅ 類別邊界 |
| **SNR** | ❌ 端點固定 | ❌ b/p 與 SNR 無關 | ❌ |

該文件的結論是 **「VOT 比 SNR 更符合 AGRT 結構」**,而且有實務後果:SNR 是**難度旋鈕,不是 GRT 意義下的維度** —— 受試者報告的是 be/pe 這個類別,不是「吵還是乾淨」。因此聽覺維度必須另開一維 `QuestHandler`,**不能直接餵 `AGRTHandler`**(後者回傳對稱的兩個值)。

**這是 SNR 路線一個實實在在的架構成本,而且是文獻回顧看不到的 —— 它來自專案自己的模型實作。**

**兩邊怎麼調和?(我的看法)** 兩個分析問的其實不是同一件事:
- §5.5 問的是 **GRT 辨識作業本身**的知覺分布形狀。在那個作業裡,聽覺維度只需要**兩個層次**(be / pe),SNR 路線讓這兩個層次維持在清楚的範疇範例上,噪音對稱地把分布撐開。
- §5.6 問的是**適應程序**要沿什麼軸搜尋。AGRT 的雙極結構預設有一條刺激可以移動的物理軸,SNR 不是那條軸。

**所以這不是矛盾,是兩個不同層次的成本落在不同路線上:合成路線的適應程序比較順,SNR 路線的知覺分布假設比較乾淨。**⚠️ 這兩者孰輕孰重,文獻回答不了,必須由專案自行權衡 —— 但至少現在兩邊都攤開了。

---

## 6. 對 AVWM 的建議

### 6.1 建議:走 SNR 路線(自然 token + 噪音),但這是**權衡**而非**壓倒**

**證據強度:中等。**(初稿寫「中等偏強」,在納入 §5.6 的 AGRT 結構成本與 §6.2 的工作記憶對稱風險後下修。)

**先講清楚結論的性質:文獻並沒有判定合成路線不可行,也沒有判定 SNR 路線更安全。**真正的情況是兩條路線的成本落在不同地方,而**只有一個軸上文獻給了明確的方向 —— GRT 的維度解釋**。建議走 SNR,是因為那個軸對本專案的核心主張(知覺可分離性)最要命,不是因為 SNR 路線整體佔優。

四條理由,依強度排序:

**(1) 最貼近的已發表前例做了同樣的選擇,而且理由是模型內生的。**
[[silbert2012]] / [[silbert2014]] / Silbert & Motlagh Zadeh (2018) 三次 GRT 語音研究都用自然錄音 + 噪音遮蔽。⚠️ 但這是同一個人的偏好,三筆不算三個獨立判斷。**證據強度:中等。**

**(2) 合成路線的主要賣點在 GRT 框架下不成立。**
「正交線索控制」買到物理正交,不是知覺正交([[roark2019]]);而 GRT 的可分離性問的是後者。**證據強度:中等**(單篇、僅讀摘要、非語音)。

**(3) 貧乏的單線索合成連續體可能改變心理計量函數的形狀,不只是難度。**
[[vanhessen1999]] 的方向明確,但**我只讀到摘要且摘要有一處費解**。**證據強度:低到中等 —— 讀到全文前不得引用。**

**(4) GRT 的高斯假設偏好「加噪音」而非「往邊界靠」。**
**證據強度:低(純推論,無文獻支持)。**

### 6.2 但必須誠實承認:合成路線並沒有被駁倒

**最強的反方證據是 [[logan1989]]** —— 音節首子音上,好的 Klatt 家族合成器與自然語音**統計上無異**。AVWM 的刺激正是單一 CV 音節的音節首塞音,落在差距最小的位置。**這條證據強度高(全文已讀,數字直接取自表格)。**

**而合成路線有一個 SNR 路線沒有的真實優勢:難度旋鈕的乾淨度。**
[[winn2013]] 已經證明遮蔽噪音會改變 VOT 與 F0 的**相對權重**,不只是均勻降低敏感度;[[shinn1985]] 的故事(效果在自然刺激上消失、加噪音後回來)指向同一件事 —— 噪音會系統性地改變聽者依賴哪些線索。**也就是說,SNR 路線的難度旋鈕,正好轉在 [[burton-blumstein-naturalness]] (1995) 指認為「真正會改變結果」的那一軸上。**

這是本回顧最不舒服的一個發現:**SNR 路線在自然度軸上贏,卻把難度旋鈕放在品質軸上,而文獻說重要的是品質軸。**

**而且還有第二個、更直接的版本。**[[synthetic-speech-cognitive-load]] 那份回顧查出:[[luce1983]] 的作者自己就把合成語音的記憶代價**類比成噪音**——

> "The synthetic words were, in a sense, acting as if they were **'noisy' or degraded items** by placing increased capacity demands on encoding and/or rehearsal processes because they were initially more difficult to encode and identify."

**→ 若合成語音的工作記憶代價機制就是「訊號退化 → 編碼負荷上升」,那麼主動加噪音的 SNR 路線走的是同一條路,而不是繞道。**AVWM 是工作記憶作業,這個顧慮不會因為改用自然 token 就消失。

**這對本文的建議有實質影響:§6.1 那四條理由裡,沒有一條是「SNR 路線在認知負荷上比較安全」—— 而且不應該有。**選 SNR 路線的理由必須全部落在 **GRT 的維度解釋**上(§5),不能訴諸認知成本。認知成本這一軸上,兩條路線大致打平,甚至 SNR 路線可能更差(因為它刻意把訊噪比壓到閾值附近)。

⚠️ 所幸 AVWM 的主 block 只用**單一**適應出來的 SNR,線索權重在該 block 內固定 —— 這個問題主要影響適應階段的解釋,不影響主要分析。(此點已記在 [[winn2013]] 卡上。)

### 6.3 兩條路線的成本對照

| | 合成(KlattGrid + ΔVOT) | SNR(自然 token + 噪音) |
|---|---|---|
| CV 音節可辨識度 | 與自然無異 ✅([[logan1989]],強) | 天然無問題 ✅ |
| WM 負荷 | 機制不適用於單一音節 ✅(推論);但不能用「品質好」辯護([[francis2009]]) | ⚠️ **並未免疫** —— 訊號退化本身就是同一個機制([[luce1983]] 作者自陳;見 [[synthetic-speech-cognitive-load]]) |
| 心理計量函數形狀 | 可能變淺、β 被高估 ⚠️([[vanhessen1999]],弱) | 未見報告 |
| GRT 維度解釋 | 維度被實驗者預先決定 ⚠️([[silbert-hawkins2016]] 建模慣例) | 較不受此限 ✅([[silbert2012]]) |
| 高斯假設 | 邊界附近敏感度非均勻 ⚠️(純推論) | 加性噪音較對稱 ✅(純推論) |
| 難度旋鈕的乾淨度 | **乾淨,不動線索權重** ✅ | **會改變線索權重** ⚠️([[winn2013]],中等) |
| **符合 AGRT 雙極結構** | ✅ 可直接餵 `AGRTHandler`([[決策脈絡_聽覺維度]]) | ⚠️ **不符合** —— SNR 是難度旋鈕非維度,需另開 `QuestHandler` |
| 邊界變異 / 收斂速度 | 較小 ✅([[mcmurray2008]]) | **較大,需更多試次** ⚠️ |
| 練習漂移 | 較大 ⚠️([[schwab1985]],推論) | 較小 ✅ |
| 噪音中的線索冗餘 | **合成 + 噪音是最該擔心的組合** ⚠️(Clark et al. 1985,二手未查證) | 冗餘線索完整 ✅ |

### 6.4 實務建議

1. **主線走 SNR 路線。**理由集中在 §6.1(1)(2),不要靠 §6.1(3)(4) 那兩條弱證據撐場面。
2. **絕對不要主張 SNR 路線在認知負荷上比較安全。**它不是。訊號退化本身就會抬高編碼負荷([[luce1983]]、[[synthetic-speech-cognitive-load]])。這個主張如果寫進論文,審稿人查一下 Luce 等人的 General Discussion 就會抓到。
3. **論文裡替 SNR 路線辯護時,用 [[silbert2012]] 的方法論論證,不要用生態效度論證。**兩者性質不同([[hamilton2020]] 是生態效度式的,[[silbert2012]] 是模型假設式的),後者對 GRT 審稿人有力得多。
4. **不要主張「合成不可行」。**[[logan1989]] 擋得住這個主張。正確的寫法是「兩條路線都可行,我們基於 GRT 的維度解釋選了自然刺激」。
5. **預期自然刺激的邊界變異較大**([[mcmurray2008]]):適應程序的先驗要放寬,試次預算要留餘裕。
6. **limitation 段必寫**:遮蔽噪音會改變線索權重([[winn2013]]),因此適應階段估到的閾值不能解讀為「純粹的 VOT 敏感度」。
7. **四件必須補做的查證**(見 §7)。

---

## 7. 明確的缺口與待查證項目

**文獻空白(不是我沒找到,是真的沒有):**
- 沒有任何研究在同一批受試者身上用自然與合成 VOT 連續體比較**類別邊界位置**。
- 沒有任何研究測過**單一孤立 CV 音節**層次的合成語音工作記憶成本。
- 沒有人正面論證過控制 vs 生態效度該優先哪一邊。

**必須補的查證(依重要性排序):**
1. **[[vanhessen1999]] 全文** —— 「範疇化程度」用什麼指標量化?"sinewave generation" 到底指什麼?§3 整節的效力取決於此。
2. **Clark, Dermody & Palethorpe (1985)** —— 原始文獻未取得,只有 [[duffy1992]] 的二手轉述。這是唯一一筆 CV 音節 + 噪音的自然/合成差異,對 AVWM 高度相關。
3. **[[francis2009]] 全文** —— 目前僅讀摘要,卻承擔了一個否定性論證(§2.4a)。
4. **[[silbert2012]] / [[silbert2014]] 的 SNR 決定方式** —— 他怎麼選 −3 dB?固定值還是預試估的?這對 AVWM 的適應程序設計有直接參考價值。

---

**相關卡片**:[[silbert2012]] · [[silbert2014]] · [[silbert-hawkins2016]] · [[soto2017]] · [[roark2019]] · [[kingston2008]] · [[logan1989]] · [[luce1983]] · [[duffy1992]] · [[francis2009]] · [[schwab1985]] · [[govender2023]] · [[mcmurray2008]] · [[vanhessen1999]] · [[schouten1992]] · [[burton-blumstein-naturalness]] · [[shinn1985]] · [[hamilton2020]] · [[winn2020]] · [[winn2013]] · [[mcmurray2022]] · [[abramson2017]] · [[klatt1980]]

**其他回顧**:[[consonant-pair-choice]](子音配對選擇) · [[synthetic-speech-cognitive-load]](認知負荷)
**專案決策脈絡**:[[決策脈絡_聽覺維度]] · [[決策脈絡_AGRT模型假設]]

---
標籤note:[[literature-note]] [[speech-perception]] [[GRT]] [[AVWM]]
