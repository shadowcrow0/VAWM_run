---
tags: [literature-note, 統計方法, 刺激當隨機效果, 單一刺激, 類化, 方法學]
citekey: clark1973
---

# Clark (1973) — ⭐⭐ 「單一刺激」什麼時候合法:他給了一個精確的判準

**這是回答「單一自然 token 是不是可以」的正典來源,而且他的答案比「可以/不可以」細緻得多。**

**DOI / URL** https://doi.org/10.1016/S0022-5371(73)80014-3 |
作者自存 PDF https://web.stanford.edu/~clark/1970s/
**閱讀狀態** **全文已由 subagent 取得並閱讀**(作者自存的**掃描 PDF**;
引句由 OCR 轉出,subagent 已修正明顯的掃描雜訊,頁碼對照印刷版的頁眉核實)。
⚠️ 我本人未通讀。

```bibtex
@article{clark1973language,
  author  = {Clark, Herbert H.},
  title   = {The language-as-fixed-effect fallacy: A critique of language statistics
             in psychological research},
  journal = {Journal of Verbal Learning and Verbal Behavior},
  volume  = {12}, number = {4}, pages = {335--359}, year = {1973},
  doi     = {10.1016/S0022-5371(73)80014-3}
}
```
⚠️ **書目更正**:副標題是 "...in **psychological** research",**不是** "psycholinguistic
research"(經 PDF 首頁與 Crossref 雙重核實)。這個誤植在二手引用裡很常見。

## 研究問題
心理學實驗把**刺激**(詞、句子)當成固定效果,只對受試者做統計推論。
這樣做錯在哪裡?後果多嚴重?該怎麼辦?

## 方法與族群
方法學論文。以 Baker & Reader 的同音異義詞研究為引子,重新分析 13 組已發表資料。

## 結果與限制

### 謬誤是什麼(p. 336 原文)
> "they have treated Words as a fixed instead of a random effect, **implicitly accepting the
> assumption that the 20 words they chose constitute the complete population of words they
> wish to generalize to.** They have not presented any statistical evidence to show that
> their findings generalize beyond the 20 words they chose, yet they have drawn conclusions
> which presume that they have."

### ⭐ 固定混淆的危險:兩位研究者、同一個虛無、相反的結論
Clark 的引子論證比變異數論證更強:在真實效果為零的情況下,
兩位研究者各用不同的固定刺激樣本,得到**完全相反**的結論,而且**兩邊都 p < .001**。
> "And this is why it was possible for Baker and Reader to come to **exactly contrary
> conclusions, complete with 'statistical' evidence.**"

### ⭐⭐ 「單一個案法」——這一節直接回答 AVWM 的問題(pp. 352–354)

**Clark 沒有說單一刺激一律不合法。他給了一個精確的判準:**

> "When used in testing or supporting hypotheses, **the method of single cases has one quite
> severe requirement: The hypotheses of interest must be applicable to single cases**, and
> these are often rather strong hypotheses." (p. 353)

> "Since it is impossible to find single homograph/nonhomograph pairs identical in all other
> possible factors—frequency, meaning, word length, spelling difficulty, **and other
> undetermined factors**—it is only possible to test the hypothesis by looking at the central
> tendencies … **There is no single case imaginable that suffices to disconfirm the homograph
> hypothesis. So the method of single cases is simply not applicable to such
> 'central-tendency' hypotheses.**" (p. 353)

> "**It is the lumping together of data, obliterating the single cases, that requires the
> strong assumption. For this to be done, the overall means must be shown to be
> representative of each instance.**" (p. 354)

**→ ⭐ 判準:單一個案法適用於「對單一個案成立的假設」,不適用於「集中趨勢假設」。**

**對 AVWM 的直接後果(我的推論):**
「voicing 的語音表徵與顏色有關聯」是一個**類別層次的集中趨勢假設** ——
依 Clark 的判準,**用單一 /b/ token 與單一 /p/ token 測不了它**。

**但**「在 VOT = X ms、F1/F0 固定為 Y 的這個刺激上,聽覺判斷與顏色判斷是否交互作用」
**是一個對單一個案成立的假設** —— 依同一個判準,**它可以測**。

**→ 這正好解釋了為什麼合成刺激能救單一刺激設計而自然錄音不能:
合成刺激讓那個「點假設」可以被**寫下來**;
單一自然錄音的點是「這段錄音剛好長什麼樣」,寫不下來,也就退回集中趨勢假設。**
(這一步是我的推論,Clark 沒有討論合成刺激。)

### 小樣本刺激特別危險(p. 355)
> "Many of these experiments, relying on only **small samples of words**, have produced effects
> that have been rather small … It is under just these circumstances … that the
> language-as-fixed-effect fallacy can have its **most serious repercussions**."

### 設計原則(p. 349)
> "**An experimental design is only as sensitive as the less sensitive of the two subdesigns
> it contains**—the Treatments by Subjects subdesign and the Treatments by Words subdesign."

### ⚠️ 一個常見的誤傳,查證後不成立
**Clark 從未主張這個偏誤「無法量化」。** 他做的正好相反 —— 用 max F′ / min F′ 給出上下界,
並重算:13 個 F₁ 全部 p < .005,但 **只有 5 個 max F′ 顯著,其中 2 個只到 .025**。
唯一提到 Type I error 的是腳註 3(p. 340),而且是針對一個很窄的情形。

**限制**:
- 1973 年;現代做法是混合效果模型([[barr2013]] 一系),不是 min F′。
- 掃描 PDF + OCR。
- **他討論的是詞與句子,不是語音刺激。**外推到語音學是我做的。

## 可連結脈絡
- 本卡所屬的推論文章 —— [[自然音vs合成音_理論推論]] §5
- 證據回顧 —— [[token-variability-vs-perceptual-variance]] §7.1
- 現代版與 Type I error 的量化 —— [[judd2012]]、[[westfall2014]]、[[barr2013]]
- **反方**:配對/平衡之後不需要 item 分析 —— [[raaijmakers1999]]
- 這個論證進到 SDT 的版本 —— [[rouder2007]]、[[decarlo2011]]
- ⚠️ GRT 從未引用本篇(見 [[judd2012]] 卡的引文網路統計)

---
標籤note:[[literature-note]] [[GRT]] [[AVWM]]

## 回查線索
**單一刺激什麼時候合法?** → 當**假設本身對單一個案成立**時(本篇 pp. 352–354)。
集中趨勢假設不行。
**固定刺激樣本有多危險?** → 兩位研究者可以用同一個虛無得出相反結論,兩邊都 p < .001。
**「Clark 說偏誤無法量化」對嗎?** → **不對**,他用 min F′/max F′ 量化了。
