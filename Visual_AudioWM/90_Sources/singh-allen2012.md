---
tags: [literature-note, 子音混淆, 語料庫, LDC, 安靜環境, utterance層級, AVWM]
citekey: singh-allen2012
---

# Singh & Allen (2012) — 把子音混淆拆到「單一錄音」層級:大部分安靜下的塞音幾乎零錯誤,錯誤集中在少數「唸得不好」的 token

**這是本次查證裡對 AVWM 最直接有用的一篇** —— 不是報告「voicing 平均錯幾 %」,而是把 [[phatak-allen2007]] 的同一批資料拆到**每一個錄音檔**的層級,結果顯示安靜/低噪音下,絕大多數塞音錄音是**完全零錯誤**,少數幾個「唸得不清楚」的 token 撐起了幾乎全部的平均錯誤率。**這對 AVWM 用單一 token(beachpeach)的設計是好消息,但也是警訊 —— token 品質本身就是決定性因素。**

**DOI / URL** https://doi.org/10.1121/1.3682054 | PMC3339505 https://pmc.ncbi.nlm.nih.gov/articles/PMC3339505/

**閱讀狀態** **全文 HTML 已由 PMC 取得**(3339505),以關鍵詞全文檢索方式讀過摘要、引言、方法、六個塞音(p t k b d g)各自的結果段、討論與結論;**不是逐行從頭讀到尾,但核心數據段落與所有直接引用的句子均已核對原文 HTML,非二手轉述。**

```bibtex
@article{singh2012influence,
  author  = {Singh, Rahul and Allen, Jont B.},
  title   = {The influence of stop consonants' perceptual features on the Articulation Index model},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {131}, number = {4}, pages = {3051--3068}, year = {2012},
  doi     = {10.1121/1.3682054}
}
```

## 研究問題
Articulation Index (AI) 模型假設錯誤率是 SNR 的平滑指數函數,是對「平均」子音錯誤取的擬合。**但若拆到單一錄音(utterance)層級,錯誤真的是平滑漸增的,還是其實是「聽得到就 100% 對、聽不到就接近亂猜」的二元開關,只是不同錄音的門檻不同?**

## 方法與族群
- 重新分析 [[phatak-allen2007]] 的原始資料:**LDC2005S22 Articulation Index Corpus**(與 AVWM 已查證過的 [[articulation-index-corpus]] 同一語料庫)。
- 6 個塞音 /p t k b d g/ × 4 個母音 /ɑ ɛ ɪ æ/ × **14 位語者** = 336 個獨立錄音(utterance)。⚠️ 語者人數與 [[phatak-allen2007]] 摘要所寫的 18 位有出入,見該卡。
- **25 位正常聽力受試者**;14 位完成全部試驗(即 PA07 篩出的 4 位低表現 + 10 位高表現),本篇重分析納入這 14 位的全部資料(PA07 原始分析只用 10 位高表現者)。
- SNR:−22 至 −2 dB,以及 **Q(安靜)**。**「低噪音環境」定義為 −2 dB S/N 與安靜合併**,理由是逐字:
  > "For 80% of all the utterances, there is no substantial difference between these two conditions [41 /p/ sounds have zero error (Pe = 0), and 11 more have a single error (Pe < 3%)]... hence the data are averaged across −2 dB SNR and quiet"
- 每個 utterance 在低噪音環境的平均呈現次數 N ≈ 38(每位聽者對每個聲音只聽一次)。

## 結果與限制

### ⭐⭐⭐ 六個塞音在「低噪音(≈安靜)」下的平均錯誤率(原文逐字)
> "The average errors for /p/,/t/,/k/,/b/,/d/,/g/ at −2 [dB] SNR are **1.8%, 2.3%, 0.8%, 11%, 2.2%, and 0.7%**, respectively. Thus the errors are around 1%–2% with the notable exception of /b/, which has a much larger error by more than a factor of 5."

**→ 五個塞音(p t d k g)全部落在 0.7%–2.3% 的窄範圍內,唯獨 /b/ 是 11%,高出五倍以上。**

### ⭐ 「穩健零錯誤」(RZE = 零錯誤 + 低錯誤)比例(原文逐字)
> "the percentage of robust zero error (RZE) sounds (i.e., 100 × |ZE + LE| / 56) for /p,t,k,b,d,g/, is **92.8%, 89.3%, 92.9%, 37.5%, 73.2%, and 89.3%**, respectively (average 78.6%, which excluding /b/, approaches 90%)."

**→ 排除 /b/ 之後,其餘五個塞音有近九成的錄音在低噪音下完全穩健、零錯誤。/b/ 只有 37.5% 的錄音達到這個標準。**

### ⭐⭐⭐ /b/ 的高錯誤率不是「與 p 的 voicing 混淆」,是與擦音的 manner 混淆(原文逐字)
> "Consonant /b/ is substantially different from the other five stop consonants used in the study, as it has an 11% error rate as compared to an average of ≈1.5% in quiet for the other consonants. **Specifically, /b/ forms a confusion group with the fricatives /v-f/ because the /b/ acoustic feature is not robust and is easily masked by noise.**"

> "For most HE [high error] sounds, **/b/ is confused with /v/ and /f/.**"

**→ 這是本卡對 AVWM 最重要的一條發現。/b/ 之所以在噪音下表現差,不是因為它常被聽成 /p/(voicing 對比),而是因為它常被聽成擦音 /v/、/f/(manner 混淆)。在 AVWM 的 b-vs-p 二選一(或少數選項)強迫作業裡,v/f 從一開始就不是可能的答案選項 —— 因此這個「/b/ 特別差」的效應,在只有 b/p 兩個選項的作業裡很可能根本不會顯現。** ⚠️ 這是我的推論(該篇沒有討論二選一情境),但直接建立在原文對錯誤去向的逐字報告上。

### 個別子音的錯誤去向(原文逐字,涵蓋六個塞音全部)
- **/k/**:僅 7 個錄音有誤,其中 2 個(f101ka, f101kI)高錯誤,**"these two sounds are confused with /g/"**(k→g,voicing 跨界,但只發生在單一語者的 2 個 misarticulated 錄音上,機制是 burst-to-vowel 時間間隔不符合典型 /k/ 特徵)。
- **/g/**:56 個錄音**沒有任何一個**落入高錯誤組:**"/g/ is a robust (highly salient) sound and no utterance... is misarticulated."**
- **/d/**:4 個高錯誤錄音分別誤聽為 /g/、/g/、/b/、/ð/ —— **沒有一個誤聽為 /t/**。原文逐字:m115dI "confused 7 of 38 times with /b/"; m102de "mainly confused with ð, perhaps because ... not articulated with sufficient 'voicing.'"
- **/t/**:f103te(5 次錯誤)**"mostly confused with /d/"**(t→d,voicing 跨界,單一錄音,因為 burst 到母音間隔過短、類似有聲 /d/ 的特徵)。
- **/p/**:8 個低錯誤錄音的單次誤聽分別是 **"/f,k,k,θ,t,f,t,v/"**——**沒有一個誤聽為 /b/**;另有 3 個誤聽是 /d/、/n/、noise-only,判斷為隨機猜測。一個高錯誤錄音(f113pI)的誤聽組合是 /b,k,n,t,y/(熵值 H=1,判定為接近隨機,不是系統性混淆)。

**→ 綜合來看:六個塞音裡,真正表現出「與 voicing 對應子音系統性混淆」的只有 /k/→/g/(2 個錄音,單一語者誤發音)與 /t/→/d/(1 個錄音)。/b/ 的大量錯誤完全不指向 /p/。/d/、/p/、/g/ 幾乎沒有指向各自 voicing 對應子音的系統性錯誤。這比任何一個「平均混淆率」數字都更直接地回答 AVWM 的問題:在安靜/低噪音下,b–p、d–t、g–k 的 voicing 混淆本身極其罕見,個別塞音的整體錯誤率(尤其是 /b/)主要由其他機制(manner 混淆、語者發音品質)驅動。**

### 核心理論主張:安靜下的正常聽力知覺是二元的
> "We conclude that for normally articulated utterances, normal hearing speech perception is a binary decision process in which errors are essentially zero above their threshold."

> "for salient syllables (RZE)...normal hearing speech perception is a binary decision making process (you either hear the cue or not) in which the errors are essentially zero when the syllable event is above threshold."

**→ 對 AVWM 的推論(我的推論,原文未直接討論 AVWM 的情境)**:若 beachpeach 這類自然 token 屬於「發音清楚」的一類(而不是像本文 /b/ 語者中 13/14 位那樣的「misarticulated」錄音),那麼在安靜下,voicing 判斷本身應該接近零錯誤 —— 這與 [[wang-bilger1973]] 安靜下 1.4–1.6% 的 b-p/d-t/g-k 混淆率量級一致。**但同時也提醒:單一 token 的品質是決定性的**,若 beachpeach 的 /b/ 端剛好是個「不清楚」的錄音,錯誤率可能遠高於平均。

### /b/ 的個體差異極端(補充,原文逐字)
> "13 of 14 talkers of /b/ are high error. Talker f101 has all its utterances in the RZE group. This proves that the listeners can do the task because they make no errors for this talker, who clearly enunciates the consonant /b/."

**→ 14 位語者裡只有 1 位的 /b/ 是完全穩健的,其餘 13 位或多或少有問題。這進一步支持「/b/ 難是發音/錄音品質問題,不是知覺系統性弱點」的判讀 —— 只要挑到清楚的錄音(如 f101 那樣),/b/ 是可以被穩定辨識的。**

## 限制
- 分析對象是**噪音下**的表現(−2 dB SNR 與 quiet 合併),不是純安靜單獨的數字 —— 原文自己說明兩者對 >80% 的音節沒有實質差異,但沒有拆開單獨報告「純 quiet」的平均錯誤率。
- 母音是 /ɑ ɛ ɪ æ/,不含 /i/。
- 「HE(高錯誤)」判準是 ≥12% 的錯誤率,樣本數不大(每個 utterance 平均只呈現 ~38 次),個別數字的信賴區間較寬。
- 本篇的核心論點(二元決策過程)本身仍有爭議空間,是作者自己的理論詮釋,不是無可爭議的既成事實。
- 語者人數(14)與 [[phatak-allen2007]] 摘要(18)的落差未解決。

## 可連結脈絡
- 原始資料來源(⚠️ 全文未取得)—— [[phatak-allen2007]]
- 同一語料庫,AVWM 已獨立查證規格與授權 —— [[articulation-index-corpus]]
- 正典噪音下比較 —— [[miller-nicely1955]]
- 唯一的安靜條件矩陣資料 —— [[wang-bilger1973]]
- **單一 token 品質決定一切,與固定效果謬誤直接相關** —— [[clark1973]]、[[token-variability-vs-perceptual-variance]]
- 本卡是 [[子音混淆最小化]] 的核心證據來源

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**六個塞音在安靜/低噪音下的平均錯誤率各是多少?** → p 1.8%、t 2.3%、k 0.8%、b 11%、d 2.2%、g 0.7%(原文逐字,−2dB 與安靜合併)。

**/b/ 為什麼特別差?是因為跟 /p/ 搞混嗎?** → **不是。** /b/ 主要與擦音 /v/、/f/ 混淆(manner 混淆),原文逐字兩次確認。在只有 b/p 兩個選項的作業裡,這個效應很可能不會出現。

**六個塞音裡,哪些真的表現出「與 voicing 對應子音系統性混淆」?** → 只有 /k/→/g/(2 個語者發音不良的錄音)與 /t/→/d/(1 個錄音)。/b/→/p/、/p/→/b/、/d/→/t/、/g/→/k/ 在本篇報告的錯誤清單裡**完全沒有出現**。

**這篇用的語料庫,AVWM 專案自己有沒有查過?** → **有**,見 [[articulation-index-corpus]]。
