# Voicing 與顏色的跨感官對應 —— 查證報告

**日期** 2026-08-13　**用途** 回答「AGRT 的 voicing×顏色一致性對比,文獻預測零還是非零?」
**範圍** 三個問題:(1) voiced↔暗這個主張站不站得住、原始來源是誰;(2) 對應的方向掛在哪個聲學/視覺參數上;(3) 有沒有人直接測過 voicing×hue 或 voicing×顏色記憶。

## 0. 一句話結論

**「voiced↔暗」這個主張確實有直接行為實驗支持,但支持它的證據測的是「語意類別歸屬」(這個名字比較適合邪惡屬性還是妖精屬性),不是「視覺明度知覺」;而文獻裡真正測過知覺明度的跨感官對應(pitch/timbre↔lightness)全部集中在「明度」這個通道上,**沒有一篇測過 voicing 本身,也沒有一篇繞過明度直接測色相(hue)**。更關鍵的是,唯一直接操弄「等明度等彩度只動色相」這個設計(與 AVWM 完全同構)的心理物理學實驗,結果幾乎是零——效應量只有明度對應的一半,而且從未涉及 voicing。**結論:AVWM 現有的顏色維度設計(固定 L\*/C\*、只動色相)很可能把 voicing 與顏色之間唯一有實證支持的通道(明度)排除在外,(C1B+C2P) vs (C2B+C1P) 這個對比,文獻傾向預測趨近於零,而非有方向的顯著效應。**這是設計本身的推論後果,不是失敗——但必須在論文裡明說。

---

## 1. 「voiced ↔ 較暗」這個對應站不站得住?

### 1.1 原始實證來源:分成兩條完全不同性質的證據鏈

查證過程中發現,這個主張其實有**兩條完全獨立、性質不同的證據鏈**,文獻裡經常被混在一起講,但拆開來看意義差很多:

**證據鏈 A ——日語聲音象徵/寶可夢命名研究(語意類別聯想)**

最直接、統計最乾淨的行為證據是 [[kawahara-kumagai2019]](Kawahara & Kumagai, 2019)。68 位日語母語者被要求判斷一對只在目標子音上不同的無意義詞,哪個比較適合「dark type」(暗屬性/邪惡陣營)寶可夢、哪個比較適合「fairy type」(妖精屬性)寶可夢。結果:

> "We observe that all the comparisons except the [w]-[y] comparison show expected response ratios above the 50 percent level (from left to right: 78.5%, 59.7%, 57.4%, 67.6%, 44.7%, and **87.6%**)." (p. 5)

voiced stops vs. voiceless stops 這一組的效應量(87.6%)是**六組對比裡最大的**,統計檢定 z = 5.87, p < .001。而且效應**不是**單純從遊戲名字背下來的表面聯想——受試者對寶可夢的熟悉度與效應量的相關是負的(r = −0.13, n.s.),排除了這個混淆。

這個模式在 [[kawahara2021]](Kawahara, Godoy & Kumagai, 2021)裡對英語母語者做了跨語言複製,方向一致但效應較弱(強迫二選一格式下 70% vs. 日語的 87.6%),而且只在強迫比較格式下才穩定。

**⚠️ 但這條證據鏈測的是什麼,必須精確講清楚**:受試者判斷的是「哪個名字比較適合『dark type』(遊戲設定裡的暗屬性/邪惡陣營)」,不是「哪個聲音讓你覺得視覺上比較暗」。[[kawahara-kumagai2019]] 自己在 Discussion 把這條聯想追溯到:

> "voiced obstruents are associated with **negative images** (e.g. Hamano 1986; Kawahara et al. 2008; Kubozono 1999; Suzuki 1962; Uemura 1965 among others), often appearing in **villains' and monsters' names**" (p. 6)

「dark type」在寶可夢設定裡本身就等同「邪惡、鬼怪、黑暗陣營」,這是一條**語意/情感類別**的聯想鏈(邪惡、負面、怪物、大、重、粗——見 [[hamano1986]] 的二手轉引內容),不是一條**知覺明度**的聯想鏈。這篇實驗本身**完全沒有色彩刺激或視覺明度測量**。

**證據鏈 B ——聲學機制論證(頻譜頻率↔大小,不是明暗)**

[[ohala1994]](Ohala, 1994)提供了一個獨立的聲學機制,常被拿來當「voiced=暗」的理論基礎,但查證後發現**這篇論文全文 22 頁,"dark"、"light"(顏色義)、"color" 一次都沒出現**。它談的核心是「頻率碼」(frequency code):嗓音基頻(F0)與物理體型大小的對應(F0 低=大、F0 高=小),子音 voicing 只在一個半頁篇幅的小節(22.4.2)裡用**不同的機制**接上:

> "In consonants, **voiceless obstruents have higher frequency than voiced because of the higher velocity of the airflow**... higher frequencies are associated with **smallness**, lower frequencies with **largeness**." (pp. 334–335)

這條論證鏈是「voiced ↔ 低頻 ↔ 大」,不是「voiced ↔ 低頻 ↔ 暗」。**darkness 從未出現在 Ohala 的原始論證裡**——把「大/小」延伸到「明/暗」,是後續文獻(尤其是日語聲音象徵一系)自己做的延伸,不是 Ohala 本人的主張。

### 1.2 ⚠️ 特別警惕的混淆:bouba/kiki 不能當 voicing 的證據

依照查證任務的提醒,逐筆檢查了 bouba/kiki 這一系文獻。[[spence2011]] 與 [[johansson2020]] 都指出這個效應的driving factor 是**整體聲音的圓潤/尖銳感**,由多個線索共同構成:

> "Speech sounds such as the nasal /m/, the voiced bilabial plosive /b/, the liquid /l/, or the back vowels /u/ and /o/ as in 'bouba' and 'maluma' are rather round... labial place of articulations, voicing, and lip rounding have independently been shown to be associated with round shapes." (WebSearch 綜合摘要,轉引自 Sidhu & Pexman 系列文獻,未直接核實原文頁碼)

也就是說 bouba 這個詞同時疊了 voicing(b 是濁音)、唇音(bilabial)、圓唇母音(/u/, /o/)、流音(/l/)四個線索,無法從中單獨拆出 voicing 的貢獻。**bouba/kiki 系列研究不能被引用來支持「voicing 本身」與任何視覺屬性(包括形狀或顏色)的對應**——這正是查證任務事先提醒要警惕的混淆,查證後確認這個警惕是對的。

### 1.3 小結:兩條證據鏈都不能直接回答 AVWM 的問題

| 證據鏈 | 測的是什麼 | 能不能回答「voicing 影響視覺明度知覺」 |
|---|---|---|
| A. 日語/英語寶可夢命名(Kawahara 系列) | 名字適不適合「邪惡/暗屬性」這個**語意類別** | ❌ 不能,沒有色彩刺激,測的是語意聯想不是知覺 |
| B. Ohala 頻率碼 | voicing↔頻譜頻率↔**大小** | ❌ 不能,全文未提明暗/顏色,是延伸推論不是原始主張 |
| bouba/kiki | 整詞(圓唇+唇音+voicing+流音)↔形狀圓尖 | ❌ 不能,voicing 的貢獻無法從其他線索中拆解出來 |

**→ 對問題一的回答:「voiced↔暗」這個語意聯想有清楚的行為證據支持(尤其在日語裡),但它是一條「聲音→語意類別(邪惡/負面)」的連結,不是一條「聲音→知覺明度」的連結。文獻裡沒有任何一篇直接讓受試者對聲音刺激的「視覺明暗程度」打分數並測 voicing 效應。**

---

## 2. 對應的「方向」到底掛在哪個聲學/視覺參數上?

### 2.1 最穩固的對應:pitch(音高)↔ lightness(明度),不是任何形式的 hue

逐一查證 [[spence2011]](Spence, 2011 的教學回顧,全文逐字讀完)、[[ward2006]](Ward et al., 2006)、[[johansson2020]]、[[anikin-johansson2019]] 四篇後,結論非常一致:**文獻裡最穩固、被最多獨立研究重複驗證的跨感官對應是 pitch↔lightness/brightness,方向是「音高越高、視覺越亮」。**

[[spence2011]] Table 1(p. 979)把 speeded classification 任務裡驗證過的所有跨感官對應列成表,「Yes」的包括 pitch–elevation、pitch–brightness、**pitch–lightness**、pitch–shape/angularity、pitch–size、pitch–spatial frequency、loudness–brightness,方向都是「高音/大聲 ↔ 高/亮/小/尖/高空間頻率」。

[[ward2006]] 直接比較聯覺者與一般人在同一套聲音-顏色配對作業上的表現:

> "Both groups show a monotonic increase in lightness with pitch... There was a highly significant effect of pitch [F(9, 162) = 56.32, p < .001], but no difference between synaesthetes and controls" (p. 267–268)

Table I(p. 277)把這條對應總結為「Nature of mapping: **Pitch → lightness**」,聯覺者與一般人共用同一套機制。

### 2.2 送氣噪音(高頻)vs. voice bar(低頻)的機制,理論上會怎麼預測?

依照查證任務的提示,AVWM 的直覺是:voiceless /p/ 的送氣是高頻噪音、voiced /b/ 有低頻 voice bar,若對應掛在「頻譜重心↔明度」,voiceless 應該對應較亮、voiced 對應較暗。這條推論鏈在文獻裡**有一半的支持、一半沒有**:

**支持的一半**——[[ohala1994]] 明確給出「voiceless 頻譜較高」的機制(p. 334–335,見上);[[johansson2020]] 的前測證實 spectral centroid(頻譜重心)確實是「亮度」的良好聲學代理,相關係數 r = .76–.92(Table 1, p. 65)。

**不支持的一半**——但 [[johansson2020]] 在跨語言顏色詞語料裡實測子音頻譜重心與顏色明度的關係,結果是:

> "We found no relation between the spectral centroid of consonants and color luminance (Figure 6B) or saturation (Figure 6D), suggesting that the 'brightness' of consonants in color words **does not depend on the perceptual characteristics of the designated color**." (p. 73)

也就是說:**只有母音**的頻譜重心/響度/F1 與顏色明度有關聯,**子音的頻譜重心跟顏色明度無關**。這對「voiceless /p/ 送氣頻譜較高→較亮」這條直覺推論是一個直接的反例——至少在自然語言的顏色詞語料裡,子音層次的頻譜特性沒有承載這個對應。

### 2.3 ⚠️ 更意外的張力:voicing/sonority 的方向可能跟日語文獻相反

[[johansson2020]] 用 sonority hierarchy(響度層級,voiced stops 排序略高於 voiceless stops,但兩者都在階層最底端)當 voicing 的粗略代理,測跨語言顏色詞:

> "there was some evidence that sonorous consonants were over-represented in words for both luminant and saturated colors. For luminance... 0.43 (95% CI [−0.07, 0.93])... For saturation... 0.51, 95% CI [0.02, 0.84]" (p. 73)

方向是 **voiced/高 sonority ↔ 較亮較飽和**(雖然明度這條邊際顯著、信賴區間含零),跟日語聲音象徵文獻(voiced↔暗/負面,見上)方向**相反**。這不是決定性證據(sonority 不等於嚴格的 voicing 二元對比,效應也弱),但足以說明:**「voiced↔暗」不是一條在所有證據來源裡都指向同一方向的穩固規律**,至少存在一個用不同方法（跨語言語料 vs. 行為判斷實驗）、不同語言樣本得到的反方向訊號。

### 2.4 有沒有任何研究顯示「色相本身」(等明度等彩度下)與聲音特徵有對應?

這是查證任務裡明確提出的關鍵問題。答案分兩層:

**心理物理學的直接證據:幾乎沒有,而且有明確的理論理由**

[[spence2011]] p. 978:

> "no crossmodal correspondence has so far been observed between pitch and hue (blue vs. red; Bernstein, Eason, & Schurman, 1971) or between loudness and lightness (Marks, 1987a)."

p. 979 註 5 給出理論解釋:

> "while pitch is a polar dimension, **hue is a circular dimension** (Marks, 1978), thus perhaps explaining why people do not match these dimensions crossmodally."

[[ward2006]] 這篇實際蒐集了 70 個聲音的顏色配對資料,卻在方法上直接放棄分析 hue:

> "hue is a circularly varying dimension and **cannot be analysed in the same way**." (p. 268, 註 3)

[[anikin-johansson2019]](Anikin & Johansson, 2019)是與 AVWM 設計**幾乎完全同構**的一篇 IAT 心理物理學實驗——顏色刺激取自 CIE-Lab 空間,每對比較只在單一視覺維度(luminance / hue / saturation 三選一)上不同,其餘固定。結果:

> "Neither green-red nor yellow-blue hue contrasts were reliably associated with any of the tested acoustic features, with one exception: high pitch was associated with blue (vs. yellow) hue." 效應量:誤差率 1.1%(95% CI [0, 3.5]),RT 49ms(95% CI [10, 96])。

> "The effect size for hue contrasts (0–1.5% and 0–50 ms) was thus about half of that for luminance contrasts."

[[johansson2020]] 在跨語言語料分析裡也直接放棄分析 hue,理由之一明確引用心理學證據:

> "psychological research on cross-modal associations between color and sound has produced much stronger evidence for cross-modal associations between sound and luminance or saturation than between sound and hue." (p. 70)

**藍紫範圍內的色相對應?沒有查到任何研究測過。** AVWM 的色相軸錨點在 h=303°(薰衣草紫,偏藍紫到偏粉紫),[[anikin-johansson2019]] 唯一測到的微弱 hue 效應是在**藍-黃軸**(pitch↔blue),不是 AVWM 用的紫色系範圍,而且效應本身極小、從未搭配任何語音/子音刺激測試過。**沒有查到任何研究專門測過藍-紫這個色相範圍內的聲音對應。**

---

## 3. 有沒有人直接做過 voicing × hue(或 voicing × 顏色記憶)?

### 3.1 直接的 voicing × 顏色知覺/記憶實驗

**查無此類研究。** 用多種查詢角度搜尋("voicing hue color experiment"、"voiced consonant color perception"、"b p color association test" 等),沒有找到任何一篇直接操弄子音 voicing(如 /b/ vs /p/)並測量對顏色知覺、顏色記憶、或顏色選擇的實驗。最接近的是 [[kawahara-kumagai2019]] 系列的語意類別判斷(見第 1 節),但那不是顏色/明度測量。

### 3.2 有沒有人在工作記憶綁定作業裡放過跨感官對應一致性?

**有,但不是 voicing、也不是顏色。** [[brunetti2017]](Brunetti, Indraccolo, Mastroberardino, Spence & Santangelo, 2017)在雙模態 2-back 作業裡操弄了三種跨感官對應一致性:pitch/形狀(bouba/kiki)、pitch/仰角、聽覺-視覺數量一致性。結果:

> 全一致(PENSc)725ms vs. 全不一致(PENSi)773ms,F(1,65)=31.242, p<.001;正確率 .80 vs. .77(邊際顯著)。

這證明了「跨感官對應一致性可以促進工作記憶表現」這個**方法學層次的先例確實存在**,而且效應發生在**提取/反應選擇階段**(不是編碼階段的知覺融合)。但三種操弄裡沒有一種涉及 voicing 或顏色,pitch/形狀那組用的還是 bouba/kiki(混淆多重線索,見 1.2 節)。

### 3.3 缺口的量化總結

| 查過的管道 | 找到什麼 | voicing×hue 直接證據? |
|---|---|---|
| Crossref / OpenAlex / PubMed / PMC 關鍵字搜尋(voicing+color/hue) | 無相關結果 | ❌ |
| 聲音象徵/寶可夢命名文獻(Kawahara 系列) | voiced↔語意類別「dark type」,無色彩刺激 | ❌(語意不是知覺) |
| 跨感官對應心理物理學文獻(Spence 系列、Anikin & Johansson) | pitch/loudness↔lightness/saturation 穩固,hue 幾乎零;完全不含 voicing | ❌(無 voicing) |
| 跨語言顏色詞語料庫研究(Johansson et al. 2020) | sonority(voicing 相關)↔saturation 弱關聯,方向與日語文獻可能相反;明確排除 hue 分析 | ❌(無 hue、方向存疑) |
| 工作記憶跨感官綁定文獻(Brunetti et al. 2017) | CC 一致性促進 WM,但測 pitch/形狀/仰角/數量,不含 voicing 或顏色 | ❌(無 voicing、無顏色) |

**→ 對問題三的回答:這是一個可主張的真實缺口。** 五個查過的管道裡沒有一個直接測過 voicing×hue 或 voicing×顏色記憶/知覺,連最接近的鄰近領域(voicing×語意類別、pitch×hue、CC 一致性×WM)都各自缺了一角。

---

## ⭐⭐⭐ 4. 核心問題:在等明度等彩度只動色相的設計下,(C1B+C2P) vs (C2B+C1P) 是零還是非零?方向?

把前三節的證據放在一起看:

1. **AVWM 顏色維度的設計是固定 L\*=55、C\*=38,只動色相角**(見 `決策脈絡_顏色維度.md`)。
2. **文獻裡「voiced↔暗」最直接、效應量最大的證據(87.6%,z=5.87)測的是語意類別歸屬(邪惡/暗屬性),不是視覺明度知覺**——它甚至沒有用到色彩刺激,無法直接告訴我們如果真的操弄色彩,效果會不會出現、往哪個方向。
3. **文獻裡真正測過知覺層次跨感官對應的研究(pitch/loudness↔顏色),對應幾乎全部集中在明度(lightness)與彩度(saturation)這兩個通道**,方向是「高音/響亮 ↔ 亮/飽和」。
4. **唯一直接操弄「等明度等彩度只動色相」這個與 AVWM 完全同構的設計的實驗**([[anikin-johansson2019]] 的 IAT),結果幾乎是零——除了一個效應量只有明度對應一半、方向在藍-黃軸(不在 AVWM 用的紫色系範圍)、且從未搭配 voicing 或其他子音特徵測試過的微弱 pitch-blue 效應之外,**hue 獨立於明度彩度之外幾乎不承載任何聲學對應**。
5. **沒有任何研究直接測過 voicing 是否能繞過明度、直接與色相產生對應。**

把這五點串起來,能得出的推論是:

**若 voicing 與顏色之間存在任何跨感官對應,文獻證據壓倒性地指向這個對應是透過「明度」這個通道傳遞的(voiceless 高頻→可能較亮,voiced 低頻→可能較暗;但連這條也只在母音層次得到語料支持,子音層次的語料證據是反例)。AVWM 把明度固定住、只讓色相變動,等於把這條唯一有實證基礎的通道堵死了。而色相本身作為一個獨立通道,在等明度等彩度的條件下,文獻(尤其是與 AVWM 設計幾乎同構的 Anikin & Johansson 2019 IAT 實驗)顯示它幾乎不參與任何聲學跨感官對應——不只是「還沒人測過 voicing 這個特定案例」,而是**連對應最穩固的 pitch/loudness 這兩個聲學維度,碰到「等明度等彩度的純色相」時效應都幾乎消失**。**

**→ 我的推論(不是文獻直接證明,是從上述四篇文獻的證據鏈推導而來):在 AVWM 目前的座標系下,(C1B + C2P) vs (C2B + C1P) 這個一致性對比,文獻預測結果是趨近於零,而非有方向的顯著效應。這是一個「設計本身把訊號歸零」的推論,不是「效應不存在」的推論——如果 AVWM 未來想保留 voicing×顏色一致性這個賣點,需要的設計調整方向會是讓明度也能變動(哪怕只是次要維度),而不是繼續在純色相軸上找方向。**

**這個推論的信心程度**:中高。理由是(a) 四篇獨立來源(Spence 2011 的正典回顧、Ward et al. 2006 的實測放棄分析、Johansson et al. 2020 的方法學排除決定、Anikin & Johansson 2019 的直接同構實驗)在「hue 獨立於明度彩度時幾乎不參與聲學對應」這一點上完全一致,不是單一研究的孤例;(b) 但沒有任何研究真的把 voicing 當自變項、把等明度等彩度的色相當依變項直接測過,所以這仍是跨領域推論而非直接證明,理論上不能完全排除 voicing 是一條「例外規則」的可能性(尤其如果它的作用機制不是聲學-知覺,而是語意-類別聯想,像 [[kawahara-kumagai2019]] 那樣——語意聯想理論上可能不受「色相是循環維度」這個知覺層次限制的約束,但目前沒有實證測過)。

---

## 5. 誠實性檢查:哪些是文獻直接支持,哪些是我的推論

| 陳述 | 狀態 |
|---|---|
| pitch↔lightness 是穩固、被獨立重複驗證的跨感官對應 | **文獻直接支持**([[spence2011]] Table 1、[[ward2006]]、[[anikin-johansson2019]]) |
| hue 獨立於明度彩度時幾乎不參與聲學跨感官對應 | **文獻直接支持**(四篇獨立來源一致) |
| voiced obstruent 在日語裡與「dark type/邪惡」語意類別有強關聯 | **文獻直接支持**([[kawahara-kumagai2019]],z=5.87, p<.001) |
| 這個「dark type」語意聯想等同於「視覺明度知覺」 | **未經證實,是常見的過度延伸**——原論文測的是類別歸屬判斷,不是明度評分 |
| voiceless 送氣頻譜較高、voiced 頻譜較低(機制) | **文獻直接支持**([[ohala1994]] p. 334–335) |
| 子音頻譜重心與顏色明度有關 | **反例存在**([[johansson2020]] 實測子音頻譜重心與顏色明度、彩度皆無關,p. 73) |
| AVWM 的色相軸(303° 錨點)在等明度等彩度下的一致性對比會趨近零 | **我的推論**,基於上述證據鏈的合理外推,不是任何單一研究直接測出的結果 |
| bouba/kiki 可以當 voicing 的獨立證據 | **明確不成立**,查證後確認需排除(多重線索混淆) |

---

## 可連結脈絡

- 顏色維度座標系定案 —— `決策脈絡_顏色維度.md`(固定 L\*=55、C\*=38,只動色相,ΔE00 弧長)
- 聽覺維度定案(Kutlu & McMurray beachpeach 連續體) —— `決策脈絡_聽覺維度.md`、`聽覺維度_嘗試與放棄紀錄.md`
- 子音配對選擇(混淆最小化) —— `子音混淆最小化.md`、`consonant-pair-choice.md`
- Miller & Nicely (1955) voicing 穩健性的正典來源(與本文問題性質不同,是噪音下的辨識穩健度,不是跨感官對應) —— [[miller-nicely1955]]
- 單一刺激/q=1 範圍聲明的判準(本文的三個核心來源全部是跨語言/跨受試者的集中趨勢研究,適用同一套判準) —— [[clark1973]]

## 回查線索

**「voiced=暗」這句話站得住嗎?** → 有直接行為證據支持(日語受試者把濁音配對到「dark type」寶可夢,效應大且穩,z=5.87),**但這是語意類別聯想(邪惡/負面),不是知覺明度判斷**——原論文完全沒有用到色彩刺激。

**這個對應的方向掛在哪個參數上?** → 文獻裡最穩固的是 **pitch(音高)↔lightness(明度)**,不是任何形式的 hue。若要把 voicing 接上這條鏈,理論上的橋接是「voiceless 送氣頻譜較高→可能較亮」(Ohala 1994 的機制),但這條橋接**只在母音層次有語料支持,子音層次是反例**(Johansson et al. 2020 實測子音頻譜重心與顏色明度無關)。

**有沒有人直接測過 voicing×hue?** → **沒有。** 查過聲音象徵、跨感官對應心理物理學、跨語言顏色詞語料、工作記憶跨感官綁定四個管道,沒有一個直接測過這個組合。

**AVWM 現在的色相軸設計,文獻預測一致性對比是零還是非零?** → **傾向零。** 這是推論而非文獻直接證明,但支撐這個推論的證據鏈很一致:hue 獨立於明度彩度時本身就幾乎不承載任何聲學對應(連最穩固的 pitch/loudness 都測不到),而 voicing 目前唯一有實證支持的視覺對應管道正是被 AVWM 固定住的明度。

**⚠️ 查不到 / 被推翻的**
- 查不到 Hamano (1986/1998) 原文全文,"voiced=darkness" 這句話的精確出處與頁碼未經核實,只有二手轉引(見 [[hamano1986]])。
- 查不到任何研究測過藍-紫範圍內(AVWM 色相軸所在區域)的聲音-色相對應。
- 查不到 Spence (2011) 之後是否有更新的跨感官對應回顧文章專門處理 hue 議題(本次查證以 2011–2023 之間的文獻為主,未系統性搜尋 2023 年後的新文獻)。
- bouba/kiki 系列**被明確排除**當 voicing 的證據,查證後確認這個警惕是對的(多重線索混淆,查不到能拆解出純 voicing 貢獻的版本)。
