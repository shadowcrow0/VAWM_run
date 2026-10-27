---
tags: [literature-note, 刺激來源, 聽力學, AVWM]
citekey: itcp-iowa-consonant
---

# Iowa Test of Consonant Perception (ITCP) —— **完全免費開放、44.1 kHz、4 語者**,但材料是 CVC 詞不是 CV 音節

**DOI / URL**
- **OSF 材料庫** https://osf.io/hycdu/
- OSF API(節點確認)https://api.osf.io/v2/nodes/hycdu/?format=json
- 驗證論文全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC8637717/
- 英國版 https://pmc.ncbi.nlm.nih.gov/articles/PMC12928676/
- 人工電子耳族群驗證 https://pmc.ncbi.nlm.nih.gov/articles/PMC11833676/

**查證狀態(2026-08-12)**
- **語者、取樣率、詞結構、選詞流程、音韻覆蓋:已直接查證**,出自我實際打開的 PMC8637717 全文。
- **OSF 節點為公開狀態:已直接查證**(OSF API 回傳 public = true,建立於 2020-01-22)。
- **授權:未能確認,而且這是個實質問題。** OSF API 的 license 欄**沒有指定授權**。
  論文只說 "All the materials to use the ITCP or to construct your own version of the ITCP are
  freely available"。**「freely available」不是一個授權條款** ——
  它沒告訴你能不能改作、能不能再散布。
- **/bi/ /pi/ 是否在 120 詞之中:未能確認。** 論文**沒有列出完整詞表**,PMC8637717 明確沒有給窮舉清單。
  我沒有下載 OSF 的檔案來核對詞表。

```bibtex
@article{geller2021validation,
  author  = {Geller, Jason and Holmes, Ann and Schwalje, Adam and Berger, Joel I. and
             Gander, Phillip E. and Choi, Inyong and McMurray, Bob},
  title   = {Validation of the {Iowa} Test of Consonant Perception},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {150}, number = {3}, pages = {2131--2153}, year = {2021},
  doi     = {10.1121/10.0006246},
  note    = {全文見 PMC8637717。作者列表與卷期頁碼取自搜尋引擎彙整的 JASA/PubMed 書目
             (PubMed 34598595;JASA article/150/3/2131),**我未直接打開 JASA 頁面覆核**}
}

@misc{itcp-osf,
  author       = {{Iowa Test of Consonant Perception authors}},
  title        = {{ITCP} Iowa Test of Consonant Perception (OSF repository)},
  year         = {2020},
  note         = {公開 OSF 專案,含全部音檔、實驗程式與分析碼。**OSF 未指定授權。**},
  howpublished = {\url{https://osf.io/hycdu/}}
}
```

## 研究問題
有沒有一份**完全免費、授權相對乾淨、取樣率合格、多語者**的現代子音辨識材料,
可以當作 AVWM 的保底方案?

## 方法與族群
ITCP 是為了取代老舊的 NU-6 / CNC 而設計的**現代子音辨識測驗**,並且刻意做成**開放材料**。
論文明文:

> "All the materials to use the ITCP or to construct your own version of the ITCP are freely available"

> "All raw and summary data, analysis code, and materials related to the ITCP are available on our OSF website."

## 結果與限制

### 規格(PMC8637717 明文)

| 項目 | 內容 |
|---|---|
| **語者** | **4 位** —— **2 男 2 女**,Midland American English,18–25 歲 |
| **取樣率** | **44.1 kHz / 16-bit** ✅ 合格 |
| 詞數 | 120 個單音節詞 |
| 結構 | **CVC**(少數 CVCC) |
| 音韻覆蓋 | **19 個字首子音 × 8 個母音**,母音分四個象限(高前、高後、低前、低後),
每個子音-母音象限組合約 2 個詞 |
| 選詞來源 | Clearpond、MRC、IPHOD;SUBTLEX-US 頻率 > 0.5 per 10⁶;鄰域密度至少 3 |
| 詞性 | **全部是真詞** |

### 對 AVWM 的意義

**好處:**
1. **取樣率合格(44.1 kHz)** —— 這是 [[articulation-index-corpus]] 拿不到的那一分,
   也是 ITCP 存在的唯一理由(LDC 那份在其他每一項上都更強)。
2. **免費、立即可下載,且不需簽授權** —— OSF 直接抓。
   (註:[[articulation-index-corpus]] 對非會員也是 $0,但仍須走 LDC 的授權簽署流程。)
3. **4 位語者、男女均衡** —— 雖不如 LDC 的 20 位,但足以做語者變異。
4. 設計上**「19 子音 × 4 母音象限,每格約 2 詞」** →
   **/b/ 與 /p/ 配高前母音的詞,依設計必然存在**(這是我從設計規則做的推論,不是明文清單)。

**硬傷:**
1. **它是 CVC 詞,不是 CV 音節。** 要拿到 CV 必須把尾音切掉,而這有兩個已知問題
   (與 [[va-ncrar-speech-materials]] 的詞表分析同一組理由,**我的推論**):
   - **尾音協同構音**:CVC 的母音帶著尾音的構音痕跡,切掉尾音不會讓它變回開音節的母音;
   - **pre-fortis clipping**:清尾音前的母音顯著較短。若 /b/ 那邊配到濁尾音、/p/ 那邊配到清尾音,
     切出來的兩個「CV」在**時長上系統性不等**,而這會與 VOT / 時長線索混淆 ——
     對 GRT 這種要求維度可分離的設計,**這是會直接污染結論的偏誤**。
   - 除非能找到**尾音相同**的一對詞(理想是 beat/peat 這類),否則不建議。
     **beat 在詞表中是否存在、peat 是否存在 —— 未確認。**
2. **每詞應只有各語者一個 token**(論文未明說每詞錄幾次;**我的推論**)。
3. **授權未指定。** 「freely available」+ OSF 公開,但沒有掛 CC 授權。
   要在論文中再散布切割後的刺激,**嚴格說法律狀態不明**,應寫信問作者(作者群仍在職,回信機率遠高於已退休的 Shannon)。

### 判定
**這是「保底方案」,不是首選。** 它的價值在於:
**如果 Shannon 索取失敗、LDC 的 16 kHz 又不能接受,ITCP 是唯一還能立刻動手的 44.1 kHz 多語者來源。**
但用它就必須接受「切 CVC」的方法學代價,而那個代價對 GRT 設計不小。

## 可連結脈絡
- 自然語音來源總覽 —— [[natural-speech-sources]]
- 首選 —— [[shannon1999-consonant-recordings]]
- 最務實的現成方案(非會員 $0,但 16 kHz) —— [[articulation-index-corpus]]
- 同樣是「詞而非音節」的困境 —— [[va-ncrar-speech-materials]]、[[nonsense-syllable-tests]]
- 維度可分離性為何怕系統性時長差 —— [[silbert2012]]、[[silbert-hawkins2016]]
- 取樣率與頻寬 —— [[winn2020]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**有沒有免費、44.1 kHz、多語者的子音材料?** → **有,ITCP**(OSF hycdu),4 語者(2 男 2 女),120 個 CVC 詞。
**為什麼它不是首選?** → 它是 **CVC 詞**,切成 CV 會帶進尾音協同構音與 pre-fortis clipping,造成 /b/ 與 /p/ 兩側系統性時長差。
**ITCP 的授權是什麼?** → **未指定**。OSF 節點公開、論文說 "freely available",但沒有掛 CC 授權。要再散布須問作者。
**ITCP 裡有 /bi/ /pi/ 嗎?** → 依「19 子音 × 4 母音象限、每格約 2 詞」的設計規則**應該有**,但**論文沒有列詞表,未確認**。
