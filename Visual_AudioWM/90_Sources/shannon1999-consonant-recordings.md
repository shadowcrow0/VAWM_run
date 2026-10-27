---
tags: [literature-note, 刺激來源, 聽力學, AVWM]
citekey: shannon1999-consonant-recordings
---

# Shannon et al. (1999) 子音錄音庫 — 規格上**最貼近 AVWM 需求**的自然語音 CV 庫,但取得管道已老化

**DOI / URL**
- DOI https://doi.org/10.1121/1.428150
- JASA 頁面 https://pubs.aip.org/asa/jasa/article/106/6/L71/915911/Consonant-recordings-for-speech-testing(**我實際請求時回 HTTP 403**,未讀到全文)
- PubMed https://pubmed.ncbi.nlm.nih.gov/10615713/(**cookie 牆,WebFetch 讀不到**)
- NCBI eutils efetch(PMID 10615713)—— 有書目欄位但 **AB 欄為空**,此文是 Letter,PubMed 未存摘要
- Europe PMC REST https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1121/1.428150%22&resultType=core&format=json —— **書目確認**:Shannon RV, Jensvold A, Padilla M, Robert ME, Wang X; JASA 106(6): L71-4; 1999。摘要欄同樣沒有內容
- 獨立佐證(**我實際打開並讀到內文**)https://pmc.ncbi.nlm.nih.gov/articles/PMC6194309/

**查證狀態(2026-08-12)**
分四級,請務必分辨:

1. **書目資料 = 已直接查證**。Europe PMC REST 回傳的作者、卷期頁碼與年份,與 DOI 一致。

2. **⭐ 語料規格 = 已由 OpenAlex 取得摘要全文,逐字確認(2026-08-12 第二輪補查)。**
   原先此欄記為「未能直接查證」,因 JASA 403 / PubMed cookie 牆 / PubMed AB 欄為空、
   Semantic Scholar 的 abstract 欄被出版社 elide。**改走 OpenAlex API
   (`https://api.openalex.org/works/doi:10.1121/1.428150`)的 `abstract_inverted_index`,
   還原後得到完整摘要。**逐字如下:

   > "Initial and medial consonants were recorded in three vowel contexts for use in speech
   > recognition experiments. **Five male and five female talkers** were recorded producing the
   > **twenty-five consonants /b,d,g,p,t,k,m,n,ŋ,l,r,f,v,θ,ð,s,z,∫,t∫,dȝ,ȝ,j,w,ʍ,h/** in medial
   > (v/C/v) and **initial (C/v) positions** using vowels **/a/ ("hod"), /i/ ("heed"), and /u/
   > ("who'd")**. The **sampling rate for these recordings was 44.1 kHz**. **Representative tokens
   > of each consonant were amplitude normalized to the steady-state portion of the vowel.**
   > Listening tests were conducted with normal-hearing listeners on a subset of twenty consonants
   > in all three vowel contexts and in initial and medial positions. The results showed that the
   > consonants were clearly recognized with only a few minor confusions, primarily between /v/
   > and /ð/. **The full set of recordings is available for research use.**"

   → **原先標為待覆核的每一項規格,現在都是摘要原文。**⚠️ 但這仍是**摘要**,不是全文;
   錄音室細節、每個子音的 token 數、語者背景、以及「available for research use」的具體
   操作方式,摘要都沒說。

   **⭐ 兩個先前沒注意到、對 AVWM 有直接後果的句子:**
   - **"amplitude normalized to the steady-state portion of the vowel"** —— 這正好是
     [[consonant-pair-choice]] §8.4 第 2 點要求的「以有聲段而非整檔 RMS 正規化」。
     **這套語料已經替 AVWM 做掉了那一步。**
   - **"The full set of recordings is available for research use."** —— 這是**作者在論文裡
     的公開承諾**,不只是慣例。索取時可以直接引用這一句。

3. **獨立佐證(第三方論文)**。我實際打開 PMC6194309(Frontiers in Neuroscience 2018)並讀到:
   > "these recordings were made in a double-walled sound-treated booth using a sample rate of 44.1 kHz and were stored in an uncompressed, 16-bit format."

   > "Three male talkers were selected randomly from the full corpus to match the earlier study, which corresponded to talker IDs **M2, M3, and M5** in the dataset **obtained from the author**."

   → 44.1 kHz / 16-bit 確認;「至少有 5 位男聲」由 talker ID `M5` 反推(**這是我的推論**);
   取得方式「向作者索取」為該文明文。

4. **取得管道 = 未能確認可用**(此欄未變)。我查到 Robert V. Shannon 現為 **retired**(USC 個人頁 https://web-app.usc.edu/web/hcn/profile.php?fid=77;維基 https://en.wikipedia.org/wiki/Robert_V._Shannon)。
   我**查無**任何公開下載點(GitHub / OSF / JASA supplementary / House Ear Institute 網站皆查無)。
   House Ear Institute 已改組為 House Institute Foundation。**現行索取窗口未能確認。**

```bibtex
@article{shannon1999consonant,
  author  = {Shannon, Robert V. and Jensvold, Angela and Padilla, Monica and
             Robert, Mark E. and Wang, Xiaosong},
  title   = {Consonant recordings for speech testing},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {106}, number = {6}, pages = {L71--L74}, year = {1999},
  doi     = {10.1121/1.428150}
}
```

## 研究問題
AVWM 需要**真人錄音**的 /b/–/p/ CV 音節,母音優先 /i/,≥22.05 kHz,多語者。
有沒有一份現成的、為語音測驗而系統性錄製的自然子音庫,直接滿足全部條件?

## 方法與族群
這是一篇 JASA 的 Letter to the Editor(故篇幅只有 L71–L74,且 PubMed 未收摘要)。
性質是**資源公告**而非實驗論文 —— 作者錄了一套子音庫,做了常人聽辨驗證,然後公告給社群使用。
驗證聽測以正常聽力者對子音子集進行。

## 結果與限制

**為什麼這是規格上的最佳解**(規格已由摘要原文逐字確認,見查證狀態 §2):

| AVWM 需求 | Shannon et al. (1999) |
|---|---|
| 英語單一 CV 音節 | 有「字首 Cv」條件 —— **就是孤立 CV** |
| /b/ 與 /p/ | 25 子音必含 /b/ /p/ |
| 母音優先 /i/ | **/i/ 是三個母音脈絡之一**(heed) |
| 次選 /ɑ/ | **/ɑ/ 也在**(摘要寫 "hod") |
| ≥22.05 kHz | **44.1 kHz / 16-bit,已獨立佐證** |
| 能乾淨切出 | 本來就是孤立音節,錄音室隔音間錄製 |
| 多語者加分 | **10 位語者(5 男 5 女)** |

**七項全中**。這在本次調查的所有來源中是唯一的。

**限制與風險**

1. **取得風險是主要風險,不是規格風險。** 唯一有記載的取得方式是「向作者索取」,而作者已退休。
   這不是「付錢就有」的商業管道,是人情管道,可能已經斷掉。
2. **母音是 /i/ 還是 /ɪ/ 未確認。** 搜尋摘要寫 "heed",若屬實則是緊母音 /i/,符合需求。但我沒讀到原文。
3. **每 token 重複次數**:PMC6194309 提到刺激「presented 10 times」,但那是**聽測呈現次數**,
   不等於語料庫中每個 token 有 10 個錄音版本。**我不能從那句話推出語料庫的 token 數。**(標明:這是我對證據邊界的判斷)
4. **未確認是否有授權條款。** 若是「作者贈與」,論文中能不能重新散布刺激檔是開放問題,需與作者確認。

**行動建議**:這條值得花一封信去試,但**必須同時備妥 Plan B**,不能等回信。
可試的窗口:USC HCN 頁面、House Institute Foundation、以及近年仍在用此語料的實驗室
(如 PMC6194309 的通訊作者)—— 後者往往比原作者更容易回信,且他們手上就有檔案。

## 可連結脈絡
- 自然語音來源總覽 —— [[natural-speech-sources]]
- 為什麼要自然語音而非合成 —— [[mbrola-cannot-do-vot]]、[[winn2020]]
- 子音對的選擇 —— [[consonant-pair-choice]]、[[abramson2017]]
- 多語者對 GRT 的意義(語者變異 vs 維度分離) —— [[silbert2012]]、[[silbert-hawkins2016]]
- 聽力學脈絡的子音辨識傳統 —— [[humes1993]]、[[nonsense-syllable-tests]]
- 備援管道 —— [[articulation-index-corpus]]、[[va-ncrar-speech-materials]]、[[itcp-iowa-consonant]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**哪一份自然語音庫同時滿足 /i/ 母音 + /b//p/ + 多語者 + 44.1 kHz?** → 本卡(Shannon 1999),但取得管道未確認。
**我親眼讀過 Shannon 1999 的原文嗎?** → **沒有**。JASA 403、PubMed cookie 牆、PubMed 無摘要欄。規格數字是搜尋引擎轉述,待覆核。
**「向作者索取」這個說法出自哪裡?** → PMC6194309 內文 "the dataset obtained from the author",我實際打開讀到的。
**為什麼 PubMed 上沒有摘要?** → 這是 Letter to the Editor,PubMed 的 AB 欄為空。不是我查錯。
