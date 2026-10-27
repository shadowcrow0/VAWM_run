---
tags: [literature-note, 語音語料庫, 刺激來源, AVWM]
citekey: oscaar-speechbox
---

# SpeechBox / OSCAAR (Northwestern) — CC BY 4.0、免費、約 9 萬檔;但**沒有無意義 CV 音節**

**DOI / URL**
- 主站 https://speechbox.linguistics.northwestern.edu/
- Scripted 分支 https://speechbox.linguistics.northwestern.edu/scripted2/
- 舊名 OSCAAR(v3) https://oscaar3.ling.northwestern.edu/
- 授權 http://creativecommons.org/licenses/by/4.0/

**查證狀態**(全部於 **2026-08-12** 實際開啟)
- 主站是 **Vue SPA**,直接抓 HTML 只會拿到 `<div id="app"></div>`(937 bytes),
  WebFetch 也因此讀不到內容。**我改抓其 JS bundle
  `/assets/index-B66jQwL-.js` 與各 view chunk,從中還原頁面文案。**
  → 本卡的引句是**從 JS bundle 內嵌的模板字串抽出**的,不是從渲染後的頁面複製。
  文字內容應與網站一致,但**格式可能有落差**。
- **我未實際送出下載申請、未取得任何音檔。** 下載流程走的是一個嵌入式表單
  (`DownloadRequestForm` chunk,含欄位 "Let us know how you plan to use this data"),
  **實際審核多久、是否人工審、會不會被拒,我沒有驗證。**
- 各語料庫的**取樣率、語者數、是否有音素層標註,網站頁面上沒有明文**,
  我**查無**。以下只寫我確實看到的。
- https://oscaar.ci.northwestern.edu/ 抓取回傳空內容,**未能確認該網址現況**。

```bibtex
@misc{bradlow_speechbox,
  author       = {Bradlow, Ann R.},
  title        = {{SpeechBox}},
  howpublished = {\url{https://speechbox.linguistics.northwestern.edu}},
  note         = {Speech Communication Research Group, Department of Linguistics,
                  Northwestern University. Accessed 2026-08-12},
  year         = {n.d.}
}
```
> 官方指定的 citation 逐字為:
> "Bradlow, A. R. (n.d.) SpeechBox. Retrieved from https://speechbox.linguistics.northwestern.edu"
> BibTeX 包裝是**我自組**的。

## 研究問題
不是單一研究的產物,是**一個機構級的語音語料庫託管平台**。站上自述逐字:

> "SpeechBox (formerly known as OSCAAR) is a web-based system for managing and providing access
> to a large set of digital speech corpora."

> "SpeechBox houses approximately 90,000 audio speech files from many different talkers, in many
> different languages, and from many different speech elicitation materials within dozens of
> different digital speech corpora."

沿革(逐字):
> "OSCAAR was originally developed (in 2009) by Tyler Kendall. In many ways, the original vision
> of OSCAAR was influenced by the Sociolinguistic Archive and Analysis Project (SLAAP) at North
> Carolina State University. The current version of SpeechBox was developed by Chun Liang Chan."

經費來源(逐字):
> "National Institute of Health, National Institute of Deafness and Other Communication
> Disorders, Grants R01DC005794 and R56DC005794"

## 方法與族群

我從 SPA 的 router 設定抽出**站上實際存在的語料庫分支**(共 10 個路由):

`allsstar`、`diapix-adaptation`、`hoosier`、`iu-sentence`、`iu-word`、
`kid-lucid`、`lucid`、`scripted`、`wildcat-diapix`、`wildcat-scripted`

我讀了其中幾個 view chunk 的描述文案(逐字):

- **ALLSSTAR** — "Archive of L1 and L2 Scripted and Spontaneous Transcripts and Recordings",
  含各語言的 North Wind and the Sun 段落朗讀。**句子/段落層級。**
- **Scripted 分支** — "Approximately 20,000 audio recordings of read speech from various speech
  and language research projects. The majority of the recordings in this branch are L1 English
  with a smaller number of corpora containing L2 English as well as L1 Dutch, Croatian and
  Korean." / "Audio recordings segmented at **sentence or word level**."
- **Hoosier** — "Hoosier Database of Native and Nonnative Speech for Children (Tessa Bent, PI)
  at Indiana University. 28 speakers including four speakers each (2 females) from the following
  language backgrounds: English, Spanish, German, French, Mandarin, Japanese, and Korean."
  / "Audio recordings are **sentence or word level** segmented."
- **IU Word** — "Scripted speech corpora from the Speech Research Laboratory (David B Pisoni, PI)
  at Indiana University. Consists of 75 monosyllabic words recorded by 10 native speakers of
  American English at 3 speaking rates (slow, medium, fast)."

**最小切分單位一律是「詞」,不是音節。** 沒有任何一個分支提到 nonsense syllable 或 CV syllable。
我另外對整個 JS bundle 做了關鍵字掃描,**"nonsense"、"syllable" 皆 0 命中**。

## 結果與限制

### 授權(逐字)—— 這是 SpeechBox 最大的優點
> "SpeechBox and all hosted recordings are licensed under a **Creative Commons Attribution 4.0
> International License**."

> "An exception to this is the **Indiana University Corpora and UCL Corpora** which can only be
> used for **research and clinical purposes**."

**CC BY 4.0 意味著:可以重散布。** 這與 LDC 的 "shall not... redistribute"(見
[[articulation-index-corpus]]、[[timit]])形成**決定性差異** ——
CC BY 4.0 下,AVWM **可以把處理後的刺激音檔連同論文一起公開**,只要標註出處。
可重製性上這是巨大的優勢。⚠️ 但 IU / UCL 那兩組例外**不適用**此優勢(僅限研究與臨床用途)。

### 價格
**免費。** 站上沒有任何費用資訊,下載走的是一個表單申請
(欄位包含 "Let us know how you plan to use this data")。
**我未實際送出申請,審核時程與通過率查無。**

### 取得方式
1. 到對應語料庫頁面點下載
2. 填寫嵌入式 DownloadRequestForm(需說明用途)
3. 站上有註記:"If you do not see the form, please turn off incognito mode and reload this page."

另據網路資料,OSCAAR v3 已不需使用者帳號 —— **此點我未在官方頁面上找到明文,標為未證實。**

### 對 AVWM 能不能用 —— **不能,作為 /bi/–/pi/ 刺激來源**
| AVWM 規格 | SpeechBox | 判定 |
|---|---|---|
| 英語 | 有大量 L1 English | ✅ |
| **單一 CV 音節** | **最小單位是詞**,無孤立 CV 音節 | ❌ **關鍵不合** |
| /b/ 與 /p/ | 詞內有,無孤立音節 | ❌ |
| 母音優先 /i/ | 未知 | ❓ |
| 能乾淨切出音節 | 需從詞裡切,同 [[timit]] 的問題 | ❌ |
| 取樣率 ≥ 22.05 kHz | **網站未載明,查無** | ❓ |
| 多語者 | 多(各庫不一) | ✅ |

最接近的是 **IU Word**(75 個單音節詞 × 10 位美語母語者 × 3 種語速)。
即使如此,那是**單音節詞**(CVC 為主),不是 CV;要拿到 /bi/ 得從 "bee"/"pea" 這種詞切,
而且該庫屬於 Indiana University Corpora,**受「僅限研究與臨床用途」的例外條款約束,
不享有 CC BY 4.0 的可重散布優勢**。

**還有一個結構性限制**(站上明文,逐字):
> "Please note that SpeechBox in not available as a repository for speech corpora that are
> developed beyond Northwestern University... The scope and scale of expanding SpeechBox to
> serve as an upload site as well as a download site are unfortunately beyond our current
> capacity."

→ SpeechBox 只收 Northwestern 相關計畫的資料,**不會有人把 CV 音節語料放上來**。
這個方向未來也不會變好。

### 保留價值
雖然不能當刺激來源,**如果 AVWM 之後需要「可公開重散布的自然語音」**(例如做 demo、
線上補充材料、或給審稿人聽的範例),SpeechBox 的 CC BY 4.0 是全篇查證中**唯一**允許重散布的來源。
值得留著這張卡。

### 限制
- 站上**不公布取樣率、位元深度、標註層級**;要知道只能先申請下載再看。
- 我從 JS bundle 還原文案,**可能漏掉只有登入後或子頁面才顯示的內容**。
- 各語料庫的詳細 metadata 我**沒有逐一開啟每個 view 頁面**,只讀了 Home、Hoosier、
  IU Word、Scripted 四個。

## 可連結脈絡
- **真正該用的語料庫** —— [[articulation-index-corpus]](孤立 CV、非會員 $0、20 位語者)
- 授權可否重散布的對照 —— [[timit]](LDC 不可重散布)
- 為什麼不能從詞/句子裡切音節 —— [[silbert2012]]、[[timit]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]、[[natural-vs-synthetic-speech]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**有沒有免費、而且允許我把刺激音檔跟論文一起公開的英語語音語料庫?** →
SpeechBox(Northwestern)是 **CC BY 4.0**,允許重散布;但 Indiana University 與 UCL 那兩組
例外只限研究與臨床用途。**代價是它沒有孤立 CV 音節。**

**SpeechBox / OSCAAR 有無意義音節嗎?** → **沒有。** 10 個分支全部是句子或詞層級,
JS bundle 全文掃描 "nonsense"、"syllable" 皆 0 命中。最接近的是 IU Word(75 個單音節**詞**)。

**為什麼 SpeechBox 抓不到內容?** → 它是 Vue SPA,HTML 只有 937 bytes。
要讀內容得抓 `/assets/index-*.js` 與各 view chunk,從模板字串還原。
