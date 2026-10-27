---
tags: [literature-note, 語音語料庫, 刺激來源, AVWM]
citekey: buckeye-corpus
---

# Buckeye Corpus of Conversational Speech — 標註最好、但語音最不適合切 CV 的那一個

**DOI / URL**
- 官網 https://buckeyecorpus.osu.edu/
- 語料說明 https://buckeyecorpus.osu.edu/php/corpusInfo.php
- 註冊頁 https://buckeyecorpus.osu.edu/php/registration.php
- FAQ https://buckeyecorpus.osu.edu/php/faq.php
- **授權全文 PDF** https://buckeyecorpus.osu.edu/License.pdf
- **標註手冊 PDF** https://buckeyecorpus.osu.edu/BuckeyeCorpusmanual.pdf
- Interspeech 2007 更新報告 https://www.isca-archive.org/interspeech_2007/foslerlussier07_interspeech.pdf

**查證狀態** 2026-08-12 **實際打開上列全部七個頁面/檔案**;License.pdf(5 頁)與
BuckeyeCorpusmanual.pdf(26 頁)與 Interspeech 2007 論文(4 頁)是**下載後逐字抽取文字**,
下方所有引號內文字皆為原文。**沒有實際下載語料本體**(需簽授權書)。
標「**⚠️ 我的推論**」的段落是我的判斷,不是文獻陳述。

```bibtex
@misc{pitt2007buckeye,
  author    = {Pitt, Mark A. and Dilley, Laura and Johnson, Keith and
               Kiesling, Scott and Raymond, William and Hume, Elizabeth and
               Fosler-Lussier, Eric},
  title     = {Buckeye Corpus of Conversational Speech (2nd release)},
  year      = {2007},
  address   = {Columbus, OH},
  publisher = {Department of Psychology, Ohio State University (Distributor)},
  url       = {https://buckeyecorpus.osu.edu/}
}
```
(此格式**逐字取自官網 FAQ 頁**,是官方指定引用法。)

## 研究問題
不是一篇論文,是一個資源。它的建置問題是:自發對話語音的發音變異有多大?機器與人要辨識
口語詞,必須解決哪些問題?—— 因此它刻意收**自發訪談**而非朗讀。

## 方法與族群
- **語者 40 人**,分層取樣:「20 old, 20 young, 20 male, 20 female」;全部是
  「Caucasian, long-time local residents of Columbus, Ohio」,中至上層勞工階級。
- **語音類型:自發訪談獨白**,不是朗讀。原文:
  > "The speech is in interview format; talkers give monologues about various topics
  > (the school system, politics, family life, etc.) in response to prompts from an interviewer."
- 規模(Phase 1+2,Interspeech 2007 Table 1):**40 語者 / 38.1 小時 / 296,663 詞 /
  870,224 個 phone**。
- 錄音:「a quiet room with a close-talking head-mounted microphone」,未壓縮 WAV。
- **取樣率 16 kHz / mono / 16-bit** —— 手冊裡的操作步驟原文:
  > "In the box select 16000 for sample rate, mono, and 16-bit, then OK."

**有 phone 層標註,而且是人工校正過的**(這是它最大的賣點):
> "In the first stage, phonetic content was automatically aligned using the Xwaves Aligner
> program. In the second stage, trained phonetic analysts hand-corrected the
> automatically-generated phoneme alignments on the basis of spectrogram and waveform
> displays, as well as auditory perceptual information. The protocol for phonetic labeling
> was adapted from the TIMIT labeling guidelines."

標註者間一致性(三次測試平均):整體 80.8%,**塞音 84.3%**,擦音 84.9%,母音 77.8%。
標註檔為 Xwaves 格式(`.words` / `.phones`),Praat、Wavesurfer 可讀。

**⚠️ 對本專案最關鍵的一條標註慣例**(標註手冊 5.4.3 原文):
> "Stops are marked with a single label spanning both a closure (silence) and any release
> (including any aspiration). ... If there is no evidence of when an initial stop begins or
> a final stop ends, assume a 70ms closure interval."

**也就是說 phone 層不切開 closure / burst / aspiration。**
→ 你拿到的是「塞音起點 → 母音起點」這一段的邊界,**VOT 本身沒有被標出來**,要自己量。
對 AVWM 而言這其實不算壞消息(從 stop label 起點切到 vowel label 終點,剛好就是完整的
closure+burst+送氣+母音),但**不能直接把標註當 VOT 用**。

## 結果與限制

### 授權:**不是開放授權,要簽紙本合約**
License.pdf 是 The Ohio State University Research Foundation 的正式 content licensing
agreement。關鍵條款逐字:

> §2(a) "Licensor grants to Licensee ... a non-exclusive, non-assignable, and
> non-transferable license to use the Content for **educational and research purposes only**,
> provided that the Licensor and authors of the Content are acknowledged in any publications
> reporting its use"

> §2(c) "Licensee shall **not copy or otherwise distribute the Content**, provided, however,
> that the Content may be copied purely for archival, backup or disaster recovery purposes only"

> §2(e) "Licensee shall not modify, **create derivative works**, translate, reverse engineer
> or assemble, decompile or disassemble the Content. Furthermore, Licensee shall not
> manipulate the Content in any manner that **compromises the Content as a historical record**."

> §2(f) "Licensee agrees that Content shall not be used as the basis for a commercial
> software or hardware product or service"

> §6 Confidentiality: "Licensee agrees and warrants that Licensee and Licensee's employees,
> representatives and agents will never, either directly or indirectly, use or disclose any
> Confidential Information"

**但是有一條對刺激製作很重要的例外**:
> §2(b) "Licensee may augment the Content with supplemental annotations. Such annotations
> shall not constitute a derivative work or Improvement of the Content. Furthermore, **these
> supplemental annotations may be distributed by the Licensee**"

→ **你自己做的標註可以散布,但切出來的音檔本身不行。**

**取得流程**:先在 registration.php 填表(email、姓名、地址、辦公室電話、職業、
兩句話說明用途),再簽授權書。授權書最後一頁的指示逐字:
> "Complete the opening section and section 16.7. Sign, date and **fax to (614) 292–8907**
> Attention 'Director'"

→ **需要實體簽名 + 傳真**。FAQ 說 PI 簽一份全實驗室可用:
> "If the head of a laboratory (e.g., director, PI, faculty member) completes the license
> agreement, then all members of that lab can use the corpus."
且不得放在任何超出實驗室/課程範圍的伺服器上:
> "Under no circumstances must it be accessible by a larger group of individuals, such as
> all members of a department, institution, or the general public."

**費用**:官網首頁寫「The corpus is FREE for noncommercial uses」。授權書定義了 "Fee"
但**沒有填入金額**。⚠️ **我的推論**:實際上是零費用,但這一點官網與合約沒有互相對上,
若要寫進論文方法段應直接寫信確認。

### ⚠️ 我的推論:能不能切出乾淨的 /bi/、/pi/?—— **最不推薦**
1. **自發對話 = 系統性弱化**。這正是這個語料庫存在的理由(它就是為了記錄 reduction 而建的)。
   詞首 /b/ 在連續語音中常被前面的母音連濁、甚至完全 lenite;/p/ 在非重音音節常常
   unreleased 或 glottalized。**AVWM 需要的恰好是 canonical、送氣清楚的 token**,而這個
   語料庫刻意收集的是它的反面。
2. **/bi/ 的主要來源 "be" 是功能詞**,在自發語音裡幾乎必然是弱讀、縮短、常縮成 "'s/'re"。
   拿弱讀的 "be" 跟重讀的 "peace" 對,voicing 差異會跟音長、強度、韻律位置全部共變 ——
   對 GRT 而言這是**額外的、不受控的知覺維度**,直接破壞 2×2 設計。
3. **語速與韻律變異極大**,而 GRT 的高斯知覺分布假設在刺激本身就有大變異時很難解釋。
4. 唯一的優點(人工校正的 phone 邊界)在這裡救不了場:**邊界準不代表 token 乾淨。**

**結論(我的判斷)**:Buckeye 的標註品質是所有候選裡最好的,但語音類型與 AVWM 的需求
**方向相反**。若真要用,唯一合理路線是「用它當 /b/–/p/ 自然變異的**參考分布**(例如查
VOT 在自發語音中的實際範圍),而不是當**刺激來源**」。工作量估計:簽約 1–2 週往返 +
下載 + 用 phone tier 篩 `b iy` / `p iy` 序列(script 半天),但**篩出來之後還要逐一人耳
挑選可用 token,這才是真正的工作量,而且良率會很低**。

## 可連結脈絡
- 跨語料庫對照與最終建議 —— [[natural-speech-sources]]
- 為什麼要用自然 token 而不是合成 —— [[silbert2012]]、[[natural-vs-synthetic-speech]]
- 自發語音的 VOT 實際分布 —— [[chodroff2017]]、[[chodroff2019]](這兩篇正是用大語料庫做 VOT 統計)
- 詞首 vs 詞中位置對 /b/–/p/ 的影響 —— [[consonant-pair-choice]]
- closure/burst/aspiration 的切法 —— [[burst-vot-tradeoff]]、[[abramson2017]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**哪個英語語料庫有人工校正的 phone 邊界?** → Buckeye(Xwaves Aligner 自動對齊 + 訓練過的
phonetician 逐一手校,標註者間一致性:塞音 84.3%)。
**Buckeye 的塞音標註有沒有把 VOT 標出來?** → **沒有**。一個 label 同時涵蓋 closure、
burst 與 aspiration,VOT 要自己量。
**Buckeye 要怎麼拿?** → 註冊表 + 簽紙本授權書傳真到 OSU Office for Technology Licensing,
非商業免費(官網說法),不可散布語料本體,但**自製的補充標註可以散布**。
**為什麼標註最好的語料庫反而最不適合當刺激?** → 它是**自發對話**語料庫,存在目的就是記錄
弱化與變異;AVWM 要的是 canonical token。這是「標註品質」與「token 品質」的分離。
