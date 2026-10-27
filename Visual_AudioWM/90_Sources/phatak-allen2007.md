---
tags: [literature-note, 子音混淆, 語料庫, LDC, 安靜環境, AVWM]
citekey: phatak-allen2007
---

# Phatak & Allen (2007) — 現代語料庫版子音混淆矩陣(⚠️ 全文未取得,僅摘要 + 二手轉引)

**⚠️ 誠實聲明:本卡的內容主要來自兩個間接來源,不是我直接讀到的全文。** 這篇論文在四個不同網域(`jontalle.web.engr.illinois.edu`、`jontallen.ece.illinois.edu`、鏡像站)都對 WebFetch/curl 回傳 403,**全文 PDF 未能取得**。以下內容分別標明來源:
1. **PubMed 摘要**(NCBI eutils API 直接取得的官方摘要逐字稿,非 AI 摘要,可信度高但只有摘要層級的資訊)。
2. **[[singh-allen2012]] 對本篇方法與部分數字的逐字轉引**(該篇是本篇資料的重新分析,全文已讀,轉引部分已與該卡交叉核對)。

**凡是本卡沒有明確標成「摘要逐字」或「轉引自 Singh & Allen」的內容,一律不要當成查證過的事實。**

**DOI / URL** https://doi.org/10.1121/1.2642397 | PMID 17471744

**閱讀狀態** **⚠️ 未取得全文**。摘要由 NCBI eutils 直接取得(逐字)。

```bibtex
@article{phatak2007consonant,
  author  = {Phatak, Sandeep A. and Allen, Jont B.},
  title   = {Consonant and vowel confusions in speech-weighted noise},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {121}, number = {4}, pages = {2312--2326}, year = {2007},
  doi     = {10.1121/1.2642397}
}
```

## 研究問題
用一個**現代、大規模、多語者**的語料庫重做 Miller & Nicely 式的子音混淆矩陣分析:16 個子音 × 4 個母音,在言語頻譜噪音(speech-weighted noise)下的多個 SNR **以及安靜**條件下,哪些子音會互相混淆成群?

## 方法與族群(摘要逐字 + [[singh-allen2012]] 轉引)

摘要逐字(NCBI eutils,已核實):
> "This paper presents the results of a closed-set recognition task for 64 consonant-vowel sounds (16 C X 4 V, **spoken by 18 talkers**) in speech-weighted noise (−22,−20,−16,−10,−2 [dB]) **and in quiet**. The confusion matrices were generated using responses of **a homogeneous set of ten listeners** and the confusions were analyzed using a graphical method."

**⚠️ 語者人數有矛盾,未解決**:摘要明寫 **18 位語者**;但 [[singh-allen2012]] 描述「同一批語料庫」時方法段寫的是 **14 位語者**("the LDC2005S22 corpus...14 talkers speaking CVs")。**我沒有找到任何地方解釋這個落差**(可能是原始錄了 18 位、後續分析篩選剩 14 位,但這是我的猜測,原文未證實)。引用語者人數時應註明「依來源不同,18 或 14」。

**語料庫身份(轉引自 [[singh-allen2012]] 方法段)**:使用的是 **LDC2005S22 Articulation Index Corpus** —— **這正是 AVWM 專案 [[articulation-index-corpus]] 卡片已經查證過、且該卡判定為「這輪查到最好的選項」的同一個語料庫。**

**母音**(轉引自 [[singh-allen2012]]):/ɑ ɛ ɪ æ/(不含 AVWM 首選的 /i/)。

**受試者篩選**(摘要 + [[singh-allen2012]] 交叉核對):PA07 原文從 25 位受試者中,依安靜下的表現排除 4 位低表現者,留下 10 位「高表現」聽者做正式的混淆矩陣分析([[singh-allen2012]] p. 2315,轉引)。[[singh-allen2012]] 的重分析用了完成全部試驗的 14 位(4 位低表現 + 10 位高表現),範圍比 PA07 原始分析更廣。

## 結果與限制(摘要逐字為主)

### 三組子音,依噪音下表現分群(摘要逐字)
> "In speech-weighted noise the consonants separate into three sets: a low-scoring set C1 (/f/, /θ/, /v/, /ð/, /b/, /m/), a high-scoring set C2 (/t/, /s/, /z/, /ʃ/, /ʒ/) and set C3 (/n/, /p/, /g/, /k/, /d/) with intermediate scores."

**⚠️ 注意:/b/ 被分在低分組 C1,與 /f/ /θ/ /v/ /ð/ /m/ 同組 —— 全部是擦音或鼻音,唯獨 /b/ 是塞音。/p/ 則落在中間分數的 C3 組,與 /n/ /g/ /k/ 同組。這代表 /b/ 的低表現不是一個「b 對 p」的 voicing 問題,而是 b 這個特定塞音混進了擦音的困難群組。**

### 知覺混淆群組(摘要逐字)
> "The perceptual consonant groups are C1: {/f/-/θ/, /b/-/v/-/ð/, /θ/-/ð/}, C2: {/s/-/z/, /ʃ/-/ʒ/}, and C3: {/m/-/n/}"

**→ 摘要層級就已經指出 /b/ 的混淆對象是 /v/、/ð/(擦音),不是 /p/。這與 [[singh-allen2012]] 對同一筆資料的細部重分析結論完全一致(見該卡:「/b/ forms a confusion group with the fricatives /v-f/」)。兩篇論文(原始版與重分析版)在這一點上互相印證。**

### AI 模型與噪音類型比較(摘要逐字)
> "The exponential articulation index (AI) model for consonant score works for 12 of the 16 consonants... a comparison with past work shows that white noise masks the consonants more uniformly than speech-weighted noise, and shows that the AI... is a better measure than the wideband signal-to-noise ratio."

### 安靜條件的量化結果 —— 全部轉引自 [[singh-allen2012]],不是我直接讀到 PA07 原文
[[singh-allen2012]] 對本篇資料重新做 utterance 層級分析,得到「−2 dB SNR 與安靜」合併(因兩者對 >80% 的音節而言表現無實質差異)後,六個塞音的平均錯誤率(該篇原文逐字):
> "The average errors for /p/,/t/,/k/,/b/,/d/,/g/ at −2 [dB] SNR are 1.8%, 2.3%, 0.8%, 11%, 2.2%, and 0.7%, respectively."

**這句話出自 [[singh-allen2012]],不是 PA07 原文** —— 但因為兩篇用的是同一組原始資料,我把它視為 PA07 資料集在安靜/低噪音下的最佳量化估計,並在 [[子音混淆最小化]] 正文中優先引用 [[singh-allen2012]] 而非本卡去呈現這些數字,以維持引用鏈的準確性。

## 限制
- **全文未取得,是本次查證中資訊最不完整的一張卡。** 任何需要精確方法細節(如受試者篩選的統計判準、確切的混淆矩陣數值)的引用,都必須改引 [[singh-allen2012]] 或明確註記「轉引自」。
- 語者人數 18 vs 14 的矛盾未解決。
- 母音是 /ɑ ɛ ɪ æ/,不含 AVWM 的 /i/。
- 摘要層級的「三組」分類是噪音下的整體正確率分群,不是 voicing 特定的混淆分析。

## 可連結脈絡
- 對本篇資料的 utterance 層級重分析(全文已讀,資訊量遠大於本卡)—— [[singh-allen2012]]
- 使用的語料庫,AVWM 已獨立查證過 —— [[articulation-index-corpus]]
- 正典來源與噪音下的比較 —— [[miller-nicely1955]]、[[wang-bilger1973]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**這篇論文的全文有沒有讀到?** → **沒有,四個網域都 403。** 只有摘要(NCBI eutils 逐字)與 [[singh-allen2012]] 的轉引。引用前必須先看是不是能改引 [[singh-allen2012]]。

**/b/ 在這篇的噪音下分組結果是什麼?** → 低分組 C1,與 /f/ /θ/ /v/ /ð/ /m/(擦音+鼻音)同組;知覺混淆對象是 /v/、/ð/,不是 /p/。/p/ 則在中間分數的 C3 組。

**這篇用的語料庫,AVWM 專案自己有沒有查過?** → **有**,見 [[articulation-index-corpus]],是本次全部查證中「規格最合適」的候選語料庫之一。
