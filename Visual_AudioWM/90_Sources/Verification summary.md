---
tags: [literature-note, 查證總結, 刺激當隨機效果, 單一刺激, 方法學]
citekey: verification-summary-clark-lineage
---

# 查證總結：刺激當隨機效果的文獻譜系
# Verification Summary: The Stimuli-as-Random-Effect Lineage

**閱讀狀態**　7 篇全部取得全文並閱讀，書目全部對照 Crossref 核實。
**Read status**　All 7 requested papers: full text obtained and read. All bibliographic
records verified against Crossref.

有一項對原始提問的更正，以及一個決定性的否定發現。
One correction to the prompt, and one decisive negative finding.

---

## ⚠️ 兩則前置警告　Two caveats up front

**引用更正。** Clark 的副標題是 "...a critique of language statistics in **psychological**
research"，**不是** "psycholinguistic research"。已用 PDF 首頁與 Crossref 雙重核實。

**Citation error.** Clark's title is "...a critique of language statistics in
**psychological** research", not "psycholinguistic research". Verified from the PDF's own
title page and Crossref.

**OCR 註記。** Clark (1973) 讀的是 Clark 自己 Stanford 頁面上的**掃描 PDF**。以下引句由
OCR 轉出，明顯的掃描雜訊已修正（例如 "presented 'any" 裡多出來的引號）。頁碼對照印刷版
的頁眉核實過。

**OCR note.** Clark 1973 was read from a scanned PDF. Quotes below are transcribed from
that OCR; obvious scanner artifacts were silently normalised. Page numbers are verified
against the printed running heads.

---

## 1. Clark (1973)

```bibtex
@article{clark1973language,
  author  = {Clark, Herbert H.},
  title   = {The language-as-fixed-effect fallacy: A critique of language
             statistics in psychological research},
  journal = {Journal of Verbal Learning and Verbal Behavior},
  volume  = {12}, number = {4}, pages = {335--359}, year = {1973},
  doi     = {10.1016/S0022-5371(73)80014-3}
}
```
全文來源 / full text: `web.stanford.edu/~clark/1970s/`

### 這個謬誤是什麼　What the fallacy IS （p. 336）

> "In drawing their conclusions, therefore, Baker and Reader have committed a statistical
> error, one I will call the language-as-fixed-effect fallacy. In statistical jargon, they
> have treated Words as a fixed instead of a random effect, **implicitly accepting the
> assumption that the 20 words they chose constitute the complete population of words they
> wish to generalize to.** They have not presented any statistical evidence to show that
> their findings generalize beyond the 20 words they chose, yet they have drawn conclusions
> which presume that they have."

把「詞」當成固定效果而非隨機效果，等於**默默假設你挑的那 20 個詞就是你想推論到的整個母體**。
他們沒有提出任何統計證據顯示結論能推到那 20 個詞之外，卻下了預設能推的結論。

### ⭐⭐ 單一刺激什麼時候合法　When ONE stimulus is legitimate （pp. 352–354）

**這一節直接回答 AVWM 的問題，而且 Clark 的答案不是「單一刺激一律不行」——他給了一個
精確的判準。**

**This section directly answers the question, and it does not say one stimulus is always
illegitimate. It gives a precise criterion.**

> "When used in testing or supporting hypotheses, **the method of single cases has one
> quite severe requirement: The hypotheses of interest must be applicable to single
> cases**, and these are often rather strong hypotheses." (p. 353)

單一個案法有一個相當嚴格的要求：**你關心的假設必須是對單一個案成立的假設**。

> "Since it is impossible to find single homograph/nonhomograph pairs identical in all
> other possible factors—frequency, meaning, word length, spelling difficulty, and other
> undetermined factors—it is only possible to test the hypothesis by looking at the central
> tendencies … **There is no single case imaginable that suffices to disconfirm the
> homograph hypothesis. So the method of single cases is simply not applicable to such
> 'central-tendency' hypotheses.**" (p. 353)

因為不可能找到在所有其他因素上都相同的單一配對，只能看**集中趨勢**來檢驗假設。
沒有任何單一個案足以否證這類假設，**所以單一個案法根本不適用於「集中趨勢假設」**。

> "**It is the lumping together of data, obliterating the single cases, that requires the
> strong assumption.** For this to be done, the overall means must be shown to be
> representative of each instance." (p. 354)

**需要那個強假設的，正是「把資料合併起來、抹去個案」這個動作。** 要這樣做，必須先證明
整體平均能代表每一個個案。

> "The main purpose of the method of single cases is to shed light on individual words.
> Thus, it is crucial for investigators using this method to report both (1) the instances
> used and (2) **the data for each instance separately.**" (p. 354)

用單一個案法的人必須同時報告 (1) 用了哪些個案，以及 (2) **每個個案各自的資料**。

**→ 對 AVWM 的直接後果（這一步是推論，Clark 沒有討論語音刺激）：**

「voicing 的語音表徵與顏色有關聯」是**類別層次的集中趨勢假設** → 依 Clark 的判準，
**用單一 /b/ token 與單一 /p/ token 測不了它**。

但「在 VOT = X ms、F1/F0 固定為 Y 的**這個刺激**上，聽覺判斷與顏色判斷是否交互作用」
**是對單一個案成立的假設** → 依同一個判準，**它可以測**。

**這正好解釋了為什麼合成刺激能救單一刺激設計、而單一自然錄音不能**：合成讓那個「點假設」
可以被**寫下來**；單一自然錄音的點是「這段錄音剛好長這樣」，寫不下來，於是退回集中趨勢假設。

### 小樣本刺激特別危險　Small stimulus samples are worst （p. 355）

> "Many of these experiments, relying on only **small samples of words**, have produced
> effects that have been rather small … It is under just these circumstances … that the
> language-as-fixed-effect fallacy can have its **most serious repercussions**."

只靠少量刺激、效果又小的實驗，正是這個謬誤後果最嚴重的情況。

### 設計原則　Design principle （p. 349）—— 比 Westfall 早 41 年

> "**An experimental design is only as sensitive as the less sensitive of the two
> subdesigns it contains**—the Treatments by Subjects subdesign and the Treatments by Words
> subdesign."

一個實驗設計的敏感度，等於它內含的兩個子設計中**較不敏感的那一個**。

> "To increase his possibility of generalizing to both the language and the subject
> populations simultaneously, the investigator must add in more subjects and more words in
> **comparable amounts**."

要同時推論到語言母體與受試者母體，兩邊都要**等量地**增加。

### ⚠️ 一個常見誤傳，查證後不成立　A common misattribution, refuted

**Clark 從未主張這個偏誤「無法量化」。** 他做的正好相反 —— 用 max F′ / min F′ 給出上下界。
重算結果（p. 342）：

**Clark makes no claim that the inflation is unquantifiable. He does the opposite.**

> "While all 13 values of F₁ were significant at the .005 level, **only five values of
> max F′ are significant, two at only the .025 level.**"

13 個 F₁ 全部在 .005 顯著，但**只有 5 個 max F′ 顯著，其中 2 個只到 .025**。

唯一提到 Type I error 的是腳註 3（p. 340），而且針對的是一個很窄的情形。
（真正的量化是後來 Forster & Dickinson 1976, doi 10.1016/0022-5371(76)90014-1 用蒙地卡羅做的。）

---

## 2. Judd, Westfall & Kenny (2012)

```bibtex
@article{judd2012treating,
  author  = {Judd, Charles M. and Westfall, Jacob and Kenny, David A.},
  title   = {Treating stimuli as a random factor in social psychology: A new and
             comprehensive solution to a pervasive but largely ignored problem},
  journal = {Journal of Personality and Social Psychology},
  volume  = {103}, number = {1}, pages = {54--69}, year = {2012},
  doi     = {10.1037/a0028347}
}
```
⚠️ 取得的是**線上先行版**（頁碼為 000–000），因此以節次而非頁碼引用。
Crossref 確認正式頁碼為 54–69。

### Type I error 的實際量級　Magnitude （模擬結果）

依受試者的 ANOVA 錯誤率 "ranged from **.086 in the best case to .616 in the worst case**,
with an average error rate of **.317, over six times the nominal alpha level**."

最好的情況 .086、最壞 .616，平均 **.317 —— 是名目 alpha 的六倍以上**。

更值得注意的是："**increasing the number of participants led to greater positive bias in
the error rate**." —— **增加受試者人數反而讓偏誤更大。**

### ⭐ 固定混淆的核心陳述　The fixed-confound point（Discussion）

> "And when experimenters attempt to replicate effects **using the same experimental
> stimuli** as in previous work but analyze these data using traditional procedures that
> ignore random stimulus variation, **it can never be clear whether a successful
> replication indicates a truly reliable treatment effect or merely a consistent bias in
> the set of experimental stimuli used.**"

當研究者用**同一批刺激**去複製效果、又用忽略刺激變異的傳統分析時，
**永遠無法分辨成功的複製代表「真正穩固的效果」還是「那批刺激裡一致存在的偏誤」。**

### ⭐ 同質 vs 變異的取捨，他們明講了　The trade-off, stated explicitly

> "Should one ensure considerable stimulus variability or should one attempt to have
> stimuli that resemble each other as closely as possible? … **sampling less variable
> stimuli may lead to power benefits, but more narrowly defined samples of stimuli also
> mean that one is unable to identify significant further moderators** … and that the
> conclusions make reference only to a narrower range of stimuli."

刺激變異小 → **統計檢力有好處**，但代價是找不出其他調節變項，而且結論只適用於較窄的範圍。

效果量方面他們承認沒有乾淨的解：
"there is **no way to easily specify a single standardized effect estimate**."

---

## 3. Westfall, Kenny & Judd (2014)

```bibtex
@article{westfall2014statistical,
  author  = {Westfall, Jacob and Kenny, David A. and Judd, Charles M.},
  title   = {Statistical power and optimal design in experiments in which samples
             of participants respond to samples of stimuli},
  journal = {Journal of Experimental Psychology: General},
  volume  = {143}, number = {5}, pages = {2020--2045}, year = {2014},
  doi     = {10.1037/xge0000014}
}
```

### ⭐ 檢力有天花板，加受試者補不回來　Power has a ceiling

摘要（PMID 25111580 逐字）：
> "…in crossed designs, **statistical power typically does not approach unity as the number
> of participants goes to infinity** but instead approaches a **maximum attainable power
> value** that is possibly small, depending on the stimulus sample."

交叉設計下，**受試者人數趨近無限大，檢力也不會趨近 1**，而是趨近一個由刺激樣本決定的
**可達上限**，那個上限可能很低。

### ⭐ 需要幾個刺激　How many stimuli （p. 2026）

> "maximum achievable power with a medium effect size when using **eight stimuli** … is
> only approximately **.50, even with an infinite number of participants**. … if one
> anticipates a medium effect size and one would like power to roughly equal .80, then the
> **minimum number of stimuli … is about 16.**"

中等效果量、8 個刺激 → 就算受試者無限多，**檢力上限也只有約 .50**。
要達到 .80，**刺激數至少要 16 個**。

### 刺激少的後果　With few stimuli （p. 2032）

> "…where the true effect size is **large at d = 0.8**, and where there are a total of
> **eight stimuli (four per condition)** … the maximum attainable power is only about
> **.41**. However, if we just double the sample size of stimuli to a still relatively
> modest 16 … the maximum power … goes up to about **.78**."

即使真實效果量很大（d = 0.8），8 個刺激的檢力上限只有 **.41**；
把刺激加倍到 16 個，上限就升到 **.78**。

> "Experimenters may believe that they can compensate for a suboptimal sample of stimuli by
> simply recruiting a larger number of participants, but in fact **the degree to which this
> sort of compensation can take place is quite limited.**"

以為多找受試者就能補償刺激樣本不足 —— **能補償的程度其實非常有限。**

> "…a **direct replication with high statistical power is often theoretically impossible**
> when the original study employed a relatively small number of stimuli."

原研究若用的刺激數少，**高檢力的直接複製在理論上往往不可能。**

### 兩條經驗法則　Two rules of thumb

1. （p. 2033）"it is generally better to **increase the sample size of whichever random
   factor is contributing more random variation** to the data"
   —— 優先增加**貢獻較多隨機變異**的那個因子。
2. （p. 2034）"if one of the two sample sizes is considerably smaller than the other, there
   is generally a **greater power benefit in increasing the smaller** sample size"
   —— 兩者差距大時，**增加較小的那個**收益較大。

---

## 4. Baayen et al. (2008) 與 Barr et al. (2013)

```bibtex
@article{baayen2008mixed,
  author  = {Baayen, R. H. and Davidson, D. J. and Bates, D. M.},
  title   = {Mixed-effects modeling with crossed random effects for subjects and items},
  journal = {Journal of Memory and Language},
  volume  = {59}, number = {4}, pages = {390--412}, year = {2008},
  doi     = {10.1016/j.jml.2007.12.005}
}
@article{barr2013random,
  author  = {Barr, Dale J. and Levy, Roger and Scheepers, Christoph and Tily, Harry J.},
  title   = {Random effects structure for confirmatory hypothesis testing: Keep it maximal},
  journal = {Journal of Memory and Language},
  volume  = {68}, number = {3}, pages = {255--278}, year = {2013},
  doi     = {10.1016/j.jml.2012.11.001}
}
```

Baayen (p. 390)：
> "Just as we model human participants as random variables, **we have to model factors
> characterizing their speech as random variables as well.**"

就像我們把受試者當隨機變數，**描述他們語音的那些因子也必須當隨機變數**。

Barr (PMC3881361)：
> "For designs including within-subjects (or within-items) manipulations,
> **random-intercepts-only LMEMs can have catastrophically high Type I error rates**,
> regardless of how p-values are computed from them."

含受試者內操弄的設計，**只放隨機截距的混合模型會有災難性的 Type I error**，
不論 p 值怎麼算都一樣。

**⚠️ 兩篇都沒有建議最少要幾個項目。**　Neither paper recommends a minimum item count.

---

## 5. ⭐ Raaijmakers, Schrijnemakers & Gremmen (1999)

```bibtex
@article{raaijmakers1999how,
  author  = {Raaijmakers, Jeroen G. W. and Schrijnemakers, Joseph M. C. and Gremmen, Frans},
  title   = {How to deal with ``The language-as-fixed-effect fallacy'':
             Common misconceptions and alternative solutions},
  journal = {Journal of Memory and Language},
  volume  = {41}, number = {3}, pages = {416--426}, year = {1999},
  doi     = {10.1006/jmla.1999.2650}
}
```

**這是最支持「不必做 item 分析」的一篇，而且它的條件寫得很明確。**

摘要（逐字）：
> "…contrary to current practice, **in many cases there is no need to perform separate
> subject and item analyses since the traditional F₁ is the correct test statistic. In
> particular this is the case when item variability is experimentally controlled by
> matching or by counterbalancing.**"

與現行做法相反，**很多情況下不需要分開做受試者與項目分析，傳統的 F₁ 就是正確的檢定量 ——
特別是當項目變異已經用配對或對抗平衡加以實驗控制時。**

結論（pp. 425–426）：
> "…when the materials have been **matched on a number of variables** or when the **lists
> are counterbalanced** over different groups of subjects, **there is no need to compute
> (min)F′** and the simple subject analysis (averaging over items) will be correct."

材料若已在數個變項上配對、或清單在不同組間對抗平衡，**就不需要計算 (min)F′**。

### ⚠️ 但配對只是「減少」偏誤，不是消除　Matching reduces, does not eliminate （p. 422）

> "Hence the bias in F₁ is now a function of σ²_AB … and this will **usually be smaller
> than** σ²_W(A) … that is responsible for the bias in the case where items are sampled
> randomly."

配對之後 F₁ 的偏誤變成另一個變異成分的函數，那**通常比**隨機取樣時的偏誤小 —— 是**比較小**，
不是零。

而且他們分析的是理想情況（p. 421）：
> "the **ideal case** in which this type of blocking or matching captures **all** of the
> systematic variability between items … The various blocks are still assumed to be
> **sampled randomly from a larger population of blocks**."

配對捕捉到**全部**系統變異的理想情況，而且**各個區塊仍假設是從更大的區塊母體隨機抽出的**。

**→ 推論（他們沒有明說）：他們的論證需要「一個由配對區塊構成的母體」並從中隨機抽樣。
若只有一組配對（q = 1），σ²_AB 無法估計，也沒有區塊母體可供推論。
他們的結果支持「對一批配對樣本用 F₁」，但不因此支持「單一一組配對」。他們從未討論 q = 1。**

---

## 6. ⭐⭐ 心理物理／SDT／GRT 有沒有處理過 Clark？——量化的答案
## Has psychophysics / SDT / GRT engaged with Clark? — quantified

用 OpenAlex 跑引文網路，不用猜。Clark (1973) 有 **2,278 篇**引用文獻。期刊分布：

| 期刊 Venue | 引用數 |
|---|---|
| Memory & Cognition | 128 |
| Journal of Memory and Language | 97 |
| Journal of Verbal Learning and Verbal Behavior | 93 |
| JEP: Learning, Memory & Cognition | 60 |
| Journal of Psycholinguistic Research | 52 |
| Perception & Psychophysics + AP&P | 32 |
| Journal of Phonetics | 14 |
| Language and Speech | 14 |
| J. Speech, Language & Hearing Research | 10 |
| **Journal of the Acoustical Society of America** | **9** |
| Journal of Mathematical Psychology | 3 |
| Ear and Hearing | 1 |

**發現一：心理聲學／聽力科學傳統幾乎完全沒有接觸這個議題。**
JASA —— 語音與聽覺心理物理的旗艦期刊、發表過數千篇語音知覺論文 —— 只占
2,278 篇裡的 **9 篇（0.4%）**。

**發現二：GRT 從來沒有處理過。這是一個乾淨的否定發現。**

- 同時引用 Ashby & Townsend (1986，GRT 奠基論文，706 篇引用) 與 Clark (1973) 的文獻：
  **恰好 1 篇**，而且是心理語言學論文（JML 2007，關於名稱提取），不是 GRT 方法論文。
- **Noah Silbert** —— 最接近本設計的 GRT 作者 —— 有 16 篇引用 Ashby & Townsend，
  **0 篇**引用 Clark 1973。
- Clark 的 2,278 篇引用者中，標題含 GRT 詞彙（"general recognition"、
  "perceptual separability/independence"、"decisional separability"）的：**零篇**。

**本地證據從內部佐證了這一點。** `90_Sources/silbert2012.md` 記載 Silbert (2012)
每類用 4 個 token，但**明確地對它們合併**——"Response counts were tallied by stimulus
category, not by individual stimuli"——並把 "all marginal variances … at unity" 固定住，
**所以 token 變異在模型裡沒有地方可去**。那 4 個 token 的用途是
"to ensure that the subjects did not simply attend to some irrelevant acoustic feature"，
也就是**防假影的裝置，不是刺激取樣**。

### 但訊號偵測論有處理過　SDT HAS engaged

這是你的論證真正有先例的地方：

- **Rouder & Lu (2005)**, *Psychon. Bull. Rev.* 12(4), 573–604, doi 10.3758/bf03196750 —— 引用 Clark
- **Rouder et al. (2007)**, *Psychometrika* —— 引用 Clark（見第 7 節）
- **DeCarlo, L. T. (2011).** "Signal detection theory with item effects."
  *J. Math. Psychol.* 55(3), 229–239, doi 10.1016/j.jmp.2011.01.002 —— 引用 Clark。
  **這是最接近 GRT 的一次接觸，而且就發表在 GRT 的大本營期刊。**
- **O'Toole, Bartlett & Abdi (2000).** *Visual Cognition* 7(4), 437–463,
  doi 10.1080/135062800394603 —— 引用 Clark

GRT 那一側最接近的類比（但沒有引用 Clark）：
Silbert & Motlagh Zadeh (2018), *JASA* 143(5), 2780–2791, doi 10.1121/1.5037091。

**結論：你想做的這個論證，在訊號偵測論裡有人做過（Rouder、DeCarlo），
但在 General Recognition Theory 裡從來沒有，在心理聲學裡也幾乎沒有。
這個缺口是真實的，可以放心主張。**

---

## 7. Rouder et al. (2007)

```bibtex
@article{rouder2007signal,
  author  = {Rouder, Jeffrey N. and Lu, Jun and Sun, Dongchu and Speckman, Paul
             and Morey, Richard and Naveh-Benjamin, Moshe},
  title   = {Signal detection models with random participant and item effects},
  journal = {Psychometrika},
  volume  = {72}, number = {4}, pages = {621--642}, year = {2007},
  doi     = {10.1007/s11336-005-1350-6}
}
```
⚠️ 取得的是線上先行版，無印刷頁碼，以節次引用。

摘要（逐字）：
> "In practice, researchers aggregate data across items or participants or both. **The
> signal detection model is nonlinear; consequently, analysis with aggregated data is not
> consistent. In fact, mnemonic ability is underestimated, even in the large-sample
> limit.**"

**訊號偵測模型是非線性的，所以用合併過的資料分析並不一致 —— 即使在大樣本極限下，
能力仍然被低估。**

### ⭐ 偏誤的方向與「不可修復性」　Direction and non-fixability

> "Aggregation **implicitly treats items as fixed effects (Clark, 1973)**. Because the
> signal detection model is nonlinear, this misspecification leads to inconsistent
> estimation—**estimates of mnemonic ability are asymptotically downward biased.**"

合併資料**等於默默把項目當固定效果**。因為模型非線性，這個誤設導致估計不一致 ——
**能力估計是漸近向下偏誤的。**

> "This violation has a deleterious effect—sensitivity estimates are too low.
> **Most troubling, this bias is asymptotic.**"

敏感度估計偏低，**而且最麻煩的是：這個偏誤是漸近的**（增加樣本數不會消失）。

對照組（同篇 Simulation 節）：
> "Fortunately, **over-shrinkage bias is not asymptotic; it reduces with increasing sample
> size.**"

**這正是你要的對比**：有些偏誤加資料就會變小，合併偏誤不屬於那一類。

**⚠️ 單一項目的情況：完全沒有討論。** 我在全文搜尋過 "single item"、"one item"、
"few items"、"number of items" —— 零命中。他們只處理多項目的情況。

---

## 8. 固定混淆 vs 隨機變異　Fixed confound vs random variability

**Clark 的 Baker & Reader 思想實驗（pp. 335–336）就是固定混淆危險性的正典示範，
而且它比變異數論證更強：** 在真實效果為零的情況下，兩位研究者各用不同的固定刺激樣本，
得到**完全相反**的結論，**兩邊都 p < .001**。

> "And this is why it was possible for Baker and Reader to come to **exactly contrary
> conclusions, complete with 'statistical' evidence.**"

JWK (2012) 提供了取捨的兩半（引文見第 2 節）：固定刺激那一側是
"merely a consistent bias in the set of experimental stimuli used"；
多刺激那一側是 "sampling less variable stimuli may lead to power benefits, but more
narrowly defined samples … make reference only to a narrower range of stimuli"。

**Brunswik (1955)** —— 書目已核實，**內容未核實**：
```bibtex
@article{brunswik1955representative,
  author  = {Brunswik, Egon},
  title   = {Representative design and probabilistic theory in a functional psychology},
  journal = {Psychological Review},
  volume  = {62}, number = {3}, pages = {193--217}, year = {1955},
  doi     = {10.1037/h0047470}
}
```
未取得全文，因此**不引用其任何文字**。JWK (2012) 開篇引用了他。

**尚未讀到、可能是這個議題最好的補充來源：**
```bibtex
@article{wells1999stimulus,
  author  = {Wells, Gary L. and Windschitl, Paul D.},
  title   = {Stimulus sampling and social psychological experimentation},
  journal = {Personality and Social Psychology Bulletin},
  volume  = {25}, number = {9}, pages = {1115--1125}, year = {1999},
  doi     = {10.1177/01461672992512005}
}
```
書目已核實，摘要與全文皆未取得。

---

## 9. 明確查不到的　COULD NOT VERIFY

- **Brunswik 的核心主張** —— 1955 年論文與 1956 年專書都未取得全文。1955 的書目經
  Crossref 核實；1956 專書完全未核實。他是否處理過固定 vs 隨機混淆的取捨：**未知**。
- **Wells & Windschitl (1999)** —— 書目已核實，摘要與全文皆未取得。
- **「Clark 說 Type I error 膨脹無法量化」** —— 徹底搜尋過，**沒有這種陳述**。他反而量化了。
- **Rouder et al. (2007) 對單一項目的討論** —— 論文中不存在。
- **Westfall, Nichols & Yarkoni 的 fMRI 論文** —— 最終發表期刊未核實
  （只查到預印本 doi 10.1101/077131）。
- **頁碼**：JWK 2012（線上先行版）、Rouder 2007（線上先行版）、Barr 2013（PMC HTML）
  皆無印刷頁碼，改以節次引用。

⚠️ **期刊／共被引的計數來自 OpenAlex**，反映的是 OpenAlex 的收錄範圍 —— 涵蓋良好但非窮盡。
「零篇 GRT 論文引用 Clark」應視為**很強的證據，不是邏輯上的證明**。

---

## 可連結脈絡　Related
- 本查證支撐的推論文章 —— [[自然音vs合成音_理論推論]]
- 單一 token 的判準 —— [[clark1973]]
- token 變異與知覺變異 —— [[token-variability-vs-perceptual-variance]]
- Silbert 對 token 的處理方式 —— [[silbert2012]]、[[silbert2018]]
- 概念說明（給非統計背景讀者）—— [[exemplar與類別的推論範圍]]

---
標籤note：[[literature-note]] [[方法學]] [[GRT]] [[AVWM]]

## 回查線索　Look-up cues
**單一刺激什麼時候合法？** → 當**假設本身對單一個案成立**時（Clark 1973, pp. 352–354）。
集中趨勢假設不行。

**幾個刺激才夠？** → 中等效果量要 .80 檢力，**至少 16 個**（Westfall et al. 2014, p. 2026）。
8 個刺激的檢力上限只有 .50。

**配對能不能免掉 item 分析？** → 可以，但配對只是**減少**偏誤不是消除，
而且需要「配對區塊的母體」（Raaijmakers et al. 1999）。

**哪個領域處理過、哪個沒有？** → SDT 有（Rouder、DeCarlo）；
**GRT 完全沒有**（2,278 篇引用中零篇 GRT 論文）。
