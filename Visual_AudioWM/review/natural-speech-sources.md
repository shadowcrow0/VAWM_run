# 自然語音 /b/–/p/ CV 音節刺激:哪些途徑真的走得通

**綜合回顧 · 2026-08-12**
專案已定案走「自然 token + speech-shaped noise 調難度」([[natural-vs-synthetic-speech]] §6)、
子音配對定案 /b/–/p/ + /i/([[consonant-pair-choice]] §8.1)。**本文不重複那兩份的論證**,
只回答一個純操作性的問題:**這樣的刺激,從哪裡拿得到?**

單篇卡在 `90_Sources/`,用 `[[ ]]` 連過去。**每一條都標注查證狀態;我的推論與查到的事實嚴格分開。**

---

## 0. 結論先講

**第一順位:去 LDC 申請 `LDC2015S12` Articulation Index LSCP。它對非會員 $0.00,
裡面有 `<語者>_s_bi.wav` 與 `<語者>_s_pi.wav` —— 20 位美式英語母語者、孤立朗讀的
/biː/ 與 /piː/、音節邊界人工校正過。**

**第二順位(同時進行,因為只是一封信):寫信索取 Shannon et al. (1999) 的子音錄音庫。**
規格更好(44.1 kHz、已對母音穩態段正規化),但管道是「向作者索取」而作者已退休。

**這兩條都是「別人已經替你錄好孤立 CV 音節」的路。自己錄(路線 C)退居第三,
作為前兩條都失敗時的保底。**

**⚠️ 這個排序不是全體一致的結論,而是我在三個彼此矛盾的建議之間做的判斷。**
本次調查分五條線平行進行,三條線各自給出了**不同的**第一順位:

| 調查線 | 它的第一順位 | 它的理由 | 為什麼我沒採用它 |
|---|---|---|---|
| 免費語料庫線 | **自己錄** | 沒有任何免費語料庫同時滿足「乾淨 + 有對齊 + /bi/ 與 /pi/ 對稱」 | 它**沒有查 LDC 的孤立 CV 語料庫** —— 它的結論在「連續語音語料庫」這個範圍內完全正確,但範圍不是全部 |
| 臨床材料線 | **Shannon 1999** | 規格七項全中 | 規格確實最好,但**管道未確認**(作者已退休);LDC 那條是**確定**拿得到 |
| LDC 線 | **LDC2015S12** | 免費、孤立 CV、20 語者、檔名已核對 | ← **採用** |

**我採用 LDC2015S12 的理由是「確定性」:**它的每一個關鍵事實我都**獨立複查過**
—— readme 的檔名編碼、20 位語者 ID、四份排除清單、以及用 `curl` 直接讀目錄頁的價格表
(並用 [[timit]] 的 $250 當對照組排除「未登入一律顯示 $0」)。
**Shannon 1999 的規格更好但要賭一封信;LDC 這條只賭行政流程。**

**→ 所以正確的做法不是二選一,而是 §8.1 的四條平行推進。**

**一個必須先講的更正:問題比原本以為的大。** 你發現 `be.wav`/`pe.wav` 是 espeak-ng 合成的。
**`stimuli/` 底下那 209 個檔也全是合成的**,而且更糟 —— 見 §1。

---

## 1. 先修正事實:專案現有的聽覺刺激**全部**是合成的

`stimuli/` 看起來像一套 12 語者的自然語料。**它不是。**讀 `GetAudioStim.py`(第 1–56 行)
與 `stimuli/talker_info.csv` 即可確認:

| 表面 | 實際 |
|---|---|
| `T01`–`T12` 十二位語者 | **3 個 MBROLA diphone 語者**(`us1`/`us2`/`us3`)× VTL/F0 參數組合 |
| 音節 `b3` / `p3` | 母音是 **/ɜ˞/**(SAMPA `r=`,rhotic 央元音)—— **既不是 /i/ 也不是 /ɑ/** |
| — | 取樣率 **15000–17000 Hz**(`voice_freq` 被當語者參數在掃),低於 22.05 kHz |
| — | MBROLA **改不動 VOT**(已證,見 [[mbrola-cannot-do-vot]]) |

**→ 目前的處境不是「一套合成刺激」,是兩套合成刺激,而且沒有一套符合已定案的
/b/–/p/ + /i/ 規格。**`stimuli/` 那套連子音配對之外的母音都不對。

⚠️ 這一節是我讀原始碼與 wav header 得到的,不是文獻。可用 `python3 -c` 與
`grep VOICES GetAudioStim.py` 重現。

---

## 2. 判準:七項規格,以及哪一項其實可以讓

| # | 規格 | 出處 |
|---|---|---|
| 1 | 英語、**單一 CV 音節**、單獨呈現 | 專案設計 |
| 2 | 子音 /b/ 與 /p/ | [[consonant-pair-choice]] §8.1 |
| 3 | 母音 **/i/** | [[winn2020]] §II.D(避免 F1 與 VOT 共變) |
| 4 | 能乾淨切出(或本來就是獨立錄音) | 專案設計 |
| 5 | 取樣率 ≥ 22.05 kHz | ⚠️ **見下** |
| 6 | 多語者加分 | [[silbert2012]] 每類 4 token |
| 7 | 授權允許研究使用 | — |

**⚠️ 第 5 項應該放寬,而且理由要寫清楚。**
「≥ 22.05 kHz」這個數字的來源是**現有檔案剛好是 22050 Hz**,不是任何原理推導。
對 /bi/–/pi/ 而言,關鍵線索是 VOT(時間量,16 kHz 給 0.0625 ms 解析度,綽綽有餘)、
F1 起始(< 1000 Hz)、與唇音的 burst 頻譜 —— 而 [[chodroff2014]] 認定唇音正是 burst
頻譜 voicing 線索**最強**的部位,唇音 burst 又是低頻主導。**8 kHz 的 Nyquist 對這組對比
應該足夠。**

⚠️ **但這是我的推論,沒有文獻直接檢驗過「16 kHz 是否足以保存 /b/–/p/ 的全部線索」。**
兩個實務後果必須處理:(a) speech-shaped noise 也要一併帶限到 8 kHz,否則噪音有能量而
訊號沒有,實際 SNR 會被高估;(b) 論文方法段必須交代取樣率與噪音頻寬。

**第 6 項也需要一個反向的但書。**「多語者加分」在 [[silbert2012]] 的脈絡裡指的是
**同一位語者的多個 token**(每類 4 個,理由是防止受試者鑽單一 token 的漏洞,見該卡專章)。
**「20 位不同語者」是完全不同的東西** —— 它引入的是**語者變異**,而 [[silbert2018]]
正是專門為了建模語者變異才寫了一篇論文。

**→ 我的建議:即使拿到 20 位語者的語料,也不要全用。挑 1–4 位,對齊 [[silbert2012]] 的設計。**
(此為我的推論。)

---

## 3. 途徑 A:現成語料庫

### 3.1 ⭐ 為孤立 CV 音節而建的語料庫 —— 只有兩個,而且兩個都命中

這是本次調查最重要的發現:**確實存在「專門把所有 CV 組合逐一錄下來」的語料庫**,
而且它們不是新東西,是聽力學/語音知覺傳統裡的老資產。

#### (a) Articulation Index LSCP(LDC2015S12)—— **$0.00,而且我核對到檔名了**

詳見 [[articulation-index-corpus]]。核心事實(**我獨立複查過,不只是轉述**):

- **20 位美式英語語者(12 男 8 女)**,readme 逐字列出 `f101`…`m120` 全部 20 個 ID
- readme 逐字:
  > "All possible Consonant-Vowel (CV) and Vowel-Consonant (VC) combinations were recorded
  > for each speaker twice: **once in isolation** and once within a carrier-sentence"
- 檔名規則:`<語者>_<s|p>_<音節>.wav`,**`s` = isolated syllable**
- ASCII↔IPA 對照表逐字:`b → b (bee)`、`p → p (pea)`、`i → iː (beet)`
  **→ 目標檔就是 `f101_s_bi.wav`、`f101_s_pi.wav` …… 共 20 + 20 個**
- 邊界:> "The time-alignments for the beginning and end of the syllables ... were **manually
  adjusted**";孤立音節檔**已切除頭尾靜音**
- **我逐一檢查了 readme 的四份排除清單**(設計上不錄的組合、146 個遺失錄音、6 個音節錯誤、
  52 個 weird)—— **`_s_bi` 與 `_s_pi` 一個都沒出現。**
- 價格:我用 `curl` 直接讀目錄頁的 `data-price-table`:
  `LDC2015S12` → Non-Member **$0.00**、Reduced-License $0.00、Member $0.00。
  **對照組排除誤讀**:同一抓法下 `LDC93S1` → Non-Member **$250.00** / Reduced $125.00。
- 授權:**LDC User Agreement for Non-Members**,限非商業研究、**不得再散布**

**⚠️ 唯一硬傷:16 kHz、16-bit**(readme 逐字 "mono 16KHz 16-bit PCM encoding")。
LSCP 版把原始 AIC 的 8 kHz 窄頻版拿掉了,只留 16 kHz 寬頻版。見 §2 對第 5 項規格的討論。

**成本結構**:技術上半天(下載 → 抓 40 個檔 → 試聽 → 正規化)。
**真正的成本是行政** —— LDC 授權書落款欄是 "For the organization",需要機構簽署與 LDC 審核。

**⚠️ 一條沒證實但很重要的線索**:[[silbert2018]](Silbert & Motlagh Zadeh, *JASA* 143(5), 2780)
摘要逐字寫的是
> "ten tokens of each of four consonant categories—[t], [d], [s], [z]—produced by
> **20 talkers in CV syllables**"

**「20 位語者 + CV 音節」與本語料庫的 20 位語者高度吻合。**若屬實,那就是
「AVWM 最貼近的前例作者本人用的正是這套語料」。**我沒能證實** —— 全文付費牆擋住,
不要在論文裡當成事實寫。

#### (b) Shannon et al. (1999) 子音錄音庫 —— 規格更好,管道更險

詳見 [[shannon1999-consonant-recordings]]。**摘要全文我從 OpenAlex 的
`abstract_inverted_index` 還原取得**(JASA 403、PubMed 因是 Letter 而無摘要欄、
Semantic Scholar 被出版社 elide —— 三條路都不通,OpenAlex 是唯一通的)。逐字:

> "**Five male and five female talkers** were recorded producing the twenty-five consonants
> ... in medial (v/C/v) and **initial (C/v) positions** using vowels /a/ ("hod"), **/i/
> ("heed")**, and /u/ ("who'd"). The **sampling rate for these recordings was 44.1 kHz**.
> **Representative tokens of each consonant were amplitude normalized to the steady-state
> portion of the vowel.** ... **The full set of recordings is available for research use.**"

**七項規格全中**,而且多送兩樣:

1. **44.1 kHz** —— 沒有 §2 的取樣率妥協
2. **「已對母音穩態段振幅正規化」** —— 這正好是 [[consonant-pair-choice]] §8.4 第 2 點
   要求的修正(現有實作對整檔含靜音正規化,殘留 0.30 dB)。**這一步別人做掉了。**

**風險全在管道**:唯一有記載的取得方式是向作者索取(第三方論文 PMC6194309 明文
"in the dataset obtained from the author"),而 Shannon 已退休、House Ear Institute 已改組。
**但摘要最後那句 "available for research use" 是作者在論文裡的公開承諾,索取時可以直接引用。**

**⭐ 實務建議**:不要只寫給 Shannon。**同時寫給近年還在用這套語料的實驗室**(如
PMC6194309 的通訊作者)—— 他們手上就有檔案,回信率比退休教授高。

### 3.2 連續語音語料庫 —— 全部是死路,而且死因是同一個

TIMIT、Buckeye、LibriSpeech、VCTK、CMU ARCTIC、Common Voice、SpeechBox/OSCAAR
—— 這些的問題**不是取得困難,也不是品質**,而是**刺激類型根本不對**。

| 語料庫 | 錄的是什麼 | 有音素對齊? | 取樣率 | 授權 | 為什麼還是不行 |
|---|---|---|---|---|---|
| [[timit]] | 朗讀**句子**,630 語者 | ✅ 人工校驗,**連閉鎖段與釋放段都分開標**(`pcl`/`p`) | 16 kHz | LDC,$250 | 標註品質全場最好,**但錄的是句子** |
| [[buckeye-corpus]] | 自發**對話** | ✅ | — | 需簽同意書 | 標註最好、**語音最不適合切 CV** |
| [[librispeech]] | 有聲書朗讀 | ⚠️ 靠第三方 forced alignment | 16 kHz | CC BY 4.0 | 量最大、授權最乾淨,**但錄音通道最雜** |
| [[vctk]] | 朗讀句子,110 語者 | ❌ **完全沒有時間對齊** | 48 kHz | CC BY 4.0 | 錄音品質最好(半消音室),**但要自己對齊** |
| [[cmu-arctic]] | 朗讀句子 | ✅ **附現成 phone label** | — | 最自由 | **/pi/ 每位語者只有 8 個**,且都在詞中 |
| [[common-voice]] | 眾包朗讀 | ❌ | mp3 有損 | CC0 | **眾包 mp3,對聲學實驗基本不能用** |
| [[oscaar-speechbox]] | 句子與詞 | 只到 "sentence or word level" | 未載明 | **CC BY 4.0** ⭐ | 全場唯一允許**再散布**,但沒有 CV |

**共同死因(我的推論,但與 [[silbert2012]] 的方法論一致)**:從連續語音或詞中切出的音節,
帶著**不受控的共構、重音、語速與前後脈絡**。AVWM 要的是「除了 voicing 之外什麼都不動」
的兩個類別範例。**把這些變異源塞進 GRT 的知覺分布裡,正是 [[silbert2012]] 選自然孤立音節
時要避開的東西 —— 從連續語音切,等於用更大的工作量換到更差的刺激。**

#### ⭐ 而且有一個**結構性**的死因,不是工作量問題 —— 英語的 /bi/ 與 /pi/ 重音不對等

這是本次調查最有價值的一個否定結果(詳見 [[free-corpora-comparison]],
數字是 agent 用 CMUdict 在真實提示表上跑出來的,不是估計):

| 語料庫 | 重音 `P IY1` | 重音 `B IY1` | 問題 |
|---|---|---|---|
| [[cmu-arctic]](1,132 句提示表) | **8 個**(people×4、peace×2、Peterborough、peeled) | 40 個,**但其中 29 個是弱讀的 "be"** | 數量與重音都不對等 |
| [[vctk]](110 語者共同文本) | **每人 3 個**(people×2、snow peas),句法位置完全相同 | **0 個可用**("beautiful" 是 /bju/) | **一邊有、一邊沒有** |

**為什麼這是結構性問題而不是取樣問題**:
**/bi/ 在英語裡最常見的載體 `be` 是弱讀功能詞;/pi/ 最常見的載體 `people`/`peace` 是
重讀實詞。**於是 voicing 會與**音長、強度、F0** 系統性共變 ——
**等於在 2×2 GRT 裡偷偷加了第三個維度。**

⚠️ 這正是 [[silbert-hawkins2016]] 所說「知覺維度對應到實驗者選定的物理維度」那個問題的
最壞版本:你以為在操弄 voicing,實際上同時操弄了重音。**而 GRT 會忠實地把它報告成
「維度不可分離」。**

**→ 從連續語音切 CV,對 AVWM 不只是「工作量大」,是「會污染主要結論」。這條路應該關掉。**
(可對等的詞對只有 bee–pea、beach–peach、beak–peak、beat–peat、beep–peep ——
**而這幾對正好都不在上述語料庫的共同文本裡。**)

⚠️ **一個相反方向的用途**:[[vctk]] 的**方法段可以直接抄來當錄音規格**
(半消音室、DPA 4035 + Sennheiser MKH 800、96 kHz/24-bit 錄後降到 48 kHz/16-bit、
手動 end-point)。**語料庫調查的真正價值在這裡,以及在證明「自己錄有根據」。**

⚠️ 唯一的例外情境:若哪天需要**可公開再散布**的 demo 音檔,[[oscaar-speechbox]] 的
CC BY 4.0 是本回顧中唯一做得到的。

### 3.3 語音學教學檔案庫 —— 名氣大,但沒有孤立 CV

- [[ucla-phonetics-archive]]:628 種語言、44.1 kHz(⚠️ 官方沒寫,是 agent 用 HTTP Range
  讀 WAV 的 `fmt ` chunk 自己量出來的),**但一個 WAV 檔 = 一整份最多 106 詞的連續朗讀**
  —— 連「一詞一檔」都沒有,比 [[timit]] 更糟(TIMIT 至少有音素層標註)。
  授權是散文式的 NC + SA 描述,**沒有 CC 版本號**,而 NC 具傳染性。
- [[iowa-sounds-of-speech]]:有 `p-sound`/`b-sound`,**但例音是單詞、音訊包在 mp4 的有損
  AAC 音軌裡、取樣率查無、授權完全查無**。⚠️ 連「是不是真人錄音」都未能確認
  (環境無 ffprobe,未解碼)—— 但前三個否決理由任一個都已足夠。
- [[listenlab]](Winn):**工具齊全,但公開的 demo 音檔只有 /d/–/t/ 與 /g/–/k/,
  沒有任何 /b/–/p/**(三個 repo + 兩個網頁全掃過,0 命中)。
  ⭐ **但它的 `Make_VOT_Continuum_v33` 是 GPL-3.0**,支援 VOT 與 F0 獨立或共變操弄、
  支援 prevoicing,repo 內直接附了 [[winn2020]] 的 PDF。**這是走路線 C 時的工具,不是來源。**
  ⚠️ `listenlab.umn.edu` **網域已不存在**(DNS 查無);`mattwinn.com` 443 埠拒連。
- [[haskins-legacy-vot]]:/ba/–/pa/ **一鍵可下載**,但是 **1960 年代的共振峰合成** ——
  列為對照,不是候選。

---

## 4. 途徑 B:Python 套件 —— **沒有任何一個能給你孤立 CV 音節**

這條是實測掉的,不是猜的。詳見 [[torchaudio-datasets]]、[[huggingface-speech-datasets]]、
[[speech-python-toolkits]]、[[montreal-forced-aligner]]。

- `torchaudio.datasets` 實測 **22 個類別**(官方文件頁少列一個),全是連續語音或孤立**詞**
  (SPEECHCOMMANDS 是 yes/no/up/down)。TEDLIUM-3 的硬編碼 URL **已 404**。
- HuggingFace Hub 搜 `voice onset time` → **零筆**。
- `librosa` 範例只有不到一分鐘的人聲片段。
- `speechbrain` / `nemo` / `espnet` / `pyroomacoustics` **零音檔**,只是同一批語料庫的下載器。

**⚠️ 授權地雷**:HF Hub 上有 30+ 個 TIMIT 副本,下載量遠高於官方 repo。
**那些是 LDC93S1 的未授權重製。**要用就走 LDC 正規途徑。

**MFA 是陷阱**:`pip install montreal-forced-aligner` 會**安裝成功然後沉默失敗**
(`ModuleNotFoundError: No module named '_kalpy'`,因為 PyPI 的 `requires_dist` 沒列
`kalpy`,實質是 conda-only)。而且**就算裝好也不該用** —— GMM-HMM 對齊誤差在**數十毫秒**
量級,與 /b/–/p/ 的邊界區(20–25 ms)同一個數量級。

**⭐ 唯一的正面發現:`praat-parselmouth`。**實測可從 Python 呼叫 Praat 原生指令,
`To PointProcess (periodic, cc)` 抓聲門脈衝 —— **那正是定位 voicing onset、也就是量 VOT
的核心機具**。這是拿到刺激**之後**要用的工具,不是刺激來源。

> 環境紀律:上述安裝全在隔離 venv(`<scratchpad>/testenv`)進行,**事後已刪除並複驗**
> 系統 Python 的 numpy 1.26.4 / scipy 1.11.4 未變動。總下載約 500 MB,未碰 GB 級語料。

---

## 5. 途徑 C:自己錄 —— 可行,而且風險比直覺小

[[silbert2012]] 就是作者本人錄的("a mid-30s midwestern, male phonetician")。
規範與檢查清單見 [[recording-protocol]]。這裡只講**專案特有的三個判斷**。

### 5.1 非母語者錄英語 /bi/–/pi/:風險已量化,而且**不對稱**

[[chen2007]](36 位成大的台灣華語者,PDF 全文已讀):

| | 台灣華語者說英語 | 英語母語者參考值 |
|---|---|---|
| /pʰ/ | **68.7 ms**(SD 21.8) | 58 / 47 / 42 |
| /kʰ/ | **93.4**(SD 20.5) | 80 / 70 / 62 |

原文:"Chinese speakers produce **much longer** VOT values than native English speakers."

**⚠️ 三個判讀(我的推論,作者未討論刺激製作):**

1. **/p/ 端偏長對 AVWM 不致命,甚至無害。** AVWM 不建連續體 —— 難度旋鈕在 SNR 不在 ΔVOT。
   VOT 偏長只會讓兩個類別**更分開**。「口音會毀掉刺激」這個直覺在連續體研究上成立,
   **在本專案的設計上不成立**。
2. **/b/ 端是真正的未知數,而且是文獻空白。**[[chen2007]] **刻意不測英語濁塞音**
   (原文:"due to the debatable implementation of English voiced stops")。
   但台灣華語的不送氣 /p/ 是 **13.9 ms(SD 6.6)**,而英語 /b/ 的參考值是 11 / 15 ——
   **落在同一區**。風險比直覺小,**但錄完必須用 Praat 實測驗證**。
3. **/kʰ/ 93.4 ms 遠超母語者** —— 又一條排除軟顎音的理由,可回寫進 [[consonant-pair-choice]]。

**⚠️ 一個本回顧回答不了的問題**:AVWM 的受試者若也是台灣人,用台灣語者的 token 是「口音
匹配」還是「雙重偏移」?我查不到直接證據。**這是自錄路線最大的未解風險。**

### 5.2 設備與擺位:有一項是 /p/ 專屬的

完整清單見 [[recording-protocol]]。**最要緊的一條**:麥克風放在**嘴角側邊 2–3 cm,
離軸,不要正對嘴前** —— 因為 **/p/ 的爆破會直接吹到麥克風產生 pop,而 pop 的低頻能量
會污染 burst 與送氣段,也就是污染 VOT 量測所依賴的那兩個地標。**

台灣在地的設備先例([[chen2007]] §3.4):隔音室 + AKG C1000S + MicroTrack 24/96。

### 5.3 幾個 token

| 來源 | 每類 token | 語者 |
|---|---|---|
| [[silbert2012]] | **4** | 1(作者本人) |
| [[silbert2018]] | 10 | 20 |

⚠️ **[[silbert2012]] 用 4 個的理由是防止受試者鑽單一 token 的漏洞,不是取樣類別**
(原文明說變異被刻意壓小:"a small degree of within-category variability")。
**所以 4 不是「取樣充分性」的標準。**建議錄 ≥ 10 次再篩選。

---

## 6. 途徑 D:臨床材料與已發表刺激集

### 6.1 聽力學詞表 —— 這條路可以正式關掉

CNC / NU-6 / CID W-22 是**詞**不是 CV 音節。而且有一個決定性的實測結果
([[va-ncrar-speech-materials]]):把說明書印出的詞表窮舉後,
**`BEE` 存在(真正的開音節 /bi/),但 `PEA` 根本不存在** —— /p/+/i/ 只有 `PEAK`。
**這些詞表湊不出 /bi/–/pi/ 這一對。**

- **[[va-ncrar-speech-materials]]**:Disc 4.0 全是詞;**Disc 2.0 Track 9 才是 CV 音節**
  (BA DA GA PA TA KA),但母音是 **/ɑ/**、推論為單一語者,且 token 已被 "edited and
  aligned"(對齊與電平處理可能動到 VOT 起始瞬態,對 AVWM 是實質風險)。
  以捐款索取,官方原文「Typically, we receive donations of **$100/disc**」。
- **[[auditec]]**:**死路,而且是授權死路。**條款頁逐字(我獨立複查過):
  > "Sharing and distribution are prohibited." / "Each purchased recording gives license for
  > up to two audiometers at one location."
  完全沒提研究用途。切割後隨論文公開刺激明確違規。
- **[[nonsense-syllable-tests]]**:CUNY-NST 等概念上全對(含 /i/),**但錄音幾乎全都拿不到**。

### 6.2 ⭐ 已發表研究釋出的刺激 —— 三筆真的拿得到

#### (a) Goldenberg et al. (2022) —— **唯一「孤立 + 自然 + /ba/–/pa/」三條件全中的**

[[goldenberg2022]] 這張卡專案裡本來就有(它是 [[consonant-pair-choice]] §2 的核心證據)。
**新查到的是:那 24 個音檔作者其實釋出了,而且連結還活著。**

- ⚠️ **正式的 Data availability 是「沒公開資料」的那種寫法**
  ("will be made available by the authors, without undue reservation")。
  **真正的連結藏在 Materials and Methods「Acoustic stimuli」小節的註腳 1**:
  > "The 24 sound files used as acoustic stimuli are available as Supplementary Material
  > from https://tinyurl.com/2p8tjfnh"
- 解析到 Dropbox 的 `Puffs_Continua.zip`,**2026-08-12 實測 HTTP 200,連結活著**
- ⚠️ **但 `dl=1` 抓回來是 Dropbox 的 HTML 介面頁,必須用瀏覽器手動下載。**
  zip 內的實際檔名、大小、**取樣率全部未確認**(論文也沒載明取樣率)
- 規格:**一位單語美式英語男性**、/pa/ /ba/ /ka/ /ga/ **各 6 個 token**、
  做成兩條 8 步 VOT 連續體、共 24 檔、母音 **/ɑ/**

**這條的吸引力**:單語者 + 每類 6 token,**正好貼近 [[silbert2012]] 的 4-token 單語者設計**,
比 20 位語者的語料庫更接近已發表的 GRT 前例。**而且今天就能拿到。**

**⚠️ 母音是 /ɑ/ —— 但這個扣分可能沒有看起來重。**
[[winn2020]] §II.D 反對 /ɑ/ 的理由,是**在用 cutback 做連續體時**,F1 會與 VOT 共變而成為
額外線索。**AVWM 不建連續體** —— 它要的是兩個清楚的類別範例 + 噪音調難度。
在那個設計裡,/b/ 與 /p/ 之間本來就存在的自然 F1 起始差異,**正是 SNR 路線刻意要保留的
「自然共變線索」**([[natural-vs-synthetic-speech]] §0 的 A 軸)。
**⚠️⚠️ 這是我的推論,而且它與 [[consonant-pair-choice]] §8.1 已定案的 /i/ 選擇有張力。
我不建議據此改變定案,但它意味著:若 /i/ 的來源全部落空,退到 /ɑ/ 的代價比原本估計的小。**
⚠️ 另外要記得 [[goldenberg2022]] 自己就是在 /ɑ/ 脈絡下測出「軟顎音辨識函數較淺」的那篇,
其 /ɑ/ 與部位的交互作用無法分離(見 [[consonant-pair-choice]] §7.5)。

#### (b) OSF 上的兩筆 —— 授權兩極

- **[[osf-kutlu-mcmurray-continua]]**(Kutlu & McMurray 2024, *Sci. Rep.* 14:28825):
  **CC0 1.0 授權**(agent 實查 OSF API 的 license metadata,不是推論)、8 條 9 步自然
  cross-spliced 連續體,**含 `beach`–`peach`(母音 /i/)**、44.1 kHz、已下載驗證單檔。
  **這是本回顧中授權最乾淨的一筆** —— CC0 代表可以隨論文再散布。
  ⚠️ 但它是**詞**(CVC)不是 CV 音節、單一語者、而且是**連續體**;
  若要用,取兩端(step 1 / step 9)當類別範例,不用中間各步。
  ⚠️ 而且 `beach`/`peach` 的尾塞音會引入 **pre-fortis clipping**(母音在清塞音前變短),
  造成兩側系統性時長差 —— 對 GRT 是額外的維度污染。(此為我的推論。)
- **[[osf-kapnoula-vot-f0-stimuli]]**:7(VOT) × 5(F0) 自然 "buh"–"puh" 正交格點、
  44.1 kHz、已下載驗證 35 個檔。⚠️ **但母音是 /ʌ/**,而且 OSF 的 `node_license` 回傳
  `None` —— **這個專案沒有設定任何授權**。

---

## 7. 一張表看完

規格欄:✅ 符合 / ⚠️ 有條件 / ❌ 不符。**排序依「可行性 × 工作量 × 授權」**。

| 順位 | 來源 | 孤立CV | /i/ | /b//p/ | 語者 | 取樣率 | 授權 | 費用 | 工作量 | 主要風險 |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | [[articulation-index-corpus]] **LDC2015S12** | ✅ | ✅ | ✅ | 20 | ⚠️ 16 kHz | LDC 非會員約定(不得再散布) | **$0.00** | **半天**(+行政 3 天–3 週) | 機構簽署流程;16 kHz |
| **2** | [[shannon1999-consonant-recordings]] | ✅ | ✅ | ✅ | 10 | ✅ 44.1 kHz | 未確認 | 免費(索取) | 半天(+等信) | **管道**:作者已退休 |
| **3** | 自己錄([[recording-protocol]]) | ✅ | ✅ | ✅ | 1+ | ✅ 任選 | 自有 ✅ | 設備 | **數天–數週** | /b/ 端無文獻保證([[chen2007]]);單語者 |
| **4** | [[goldenberg2022]] 的 24 檔 | ✅ **孤立自然 CV** | ❌ /ɑ/ | ✅ | 1 | **未確認** | 未確認 | 免費 | **1 小時**(需手動下載) | 母音 /ɑ/;取樣率查無;授權未確認 |
| 5 | [[osf-kutlu-mcmurray-continua]] | ❌ 詞 | ✅ | ✅ | 1 | ✅ 44.1 | **CC0** ⭐ | 免費 | 1 小時 | pre-fortis clipping;是連續體 |
| 6 | [[osf-kapnoula-vot-f0-stimuli]] | ✅ 孤立 CV | ❌ /ʌ/ | ✅ | 1? | ✅ 44.1 | **無授權** | 免費 | 1 小時 | 母音不對;OSF 未設授權 |
| 7 | [[va-ncrar-speech-materials]] Disc 2.0 | ✅ | ❌ /ɑ/ | ✅ | 1? | 未確認 | 未確認 | ~$100 捐款 | 1–2 天 | 母音不對;token 已被編輯 |
| 8 | [[itcp-iowa-consonant]] | ❌ CVC 詞 | ? | ? | 4 | ✅ 44.1 | 未指定 | 免費 | 2–3 天 | 詞表未列出;授權未指定 |
| 9 | [[timit]] | ❌ 句 | — | — | 630 | 16 kHz | LDC | $250 | 數天–一週 | **刺激類型錯** |
| 10 | [[vctk]] / [[librispeech]] / [[cmu-arctic]] / [[buckeye-corpus]] / [[oscaar-speechbox]] | ❌ | — | — | 多 | 不一 | 多為 CC BY | 免費 | 最大 | ⭐ **重音不對等會污染結論**(§3.2) |
| — | [[auditec]] | ⚠️ | ? | ✅ | ? | ? | **禁止散布** ❌ | $74.75+ | — | **授權死路** |
| — | Python 套件(§4) | ❌ **全部沒有** | — | — | — | — | — | — | — | — |

---

## 8. 建議與具體下一步

### 8.1 四條**平行**推進,不要串列

**因為 1 與 2 的成本都是「等待」,不是「工作」。**

**動作 1(今天就能做,10 分鐘)—— 申請 LDC2015S12**
- 到 https://catalog.ldc.upenn.edu/LDC2015S12 註冊帳號、覆核 Non-Member Fee 是否真為 $0.00
- 走機構簽署流程(授權書落款欄是 "For the organization",需要單位用印)
- **同時**先抓 `LDC2017S16`(LDC Spoken Language Sampler,頁面明寫 "available as a free
  download",內含本語料庫樣本)**試聽音質**,不必等審核

**動作 2(今天就能做,20 分鐘)—— 寫兩封信索取 Shannon 1999**
- 收件人 A:Robert V. Shannon(USC,已退休;USC HCN 個人頁 fid=77)
- 收件人 B:**近年仍在用此語料的實驗室**(PMC6194309 的通訊作者)—— 回信率更高
- 信裡直接引用摘要最後一句:"The full set of recordings is available for research use."
- 明確說明你要的是:**initial C/v 位置、/i/ 母音、/b/ 與 /p/**

**動作 3(今天,5 分鐘)—— 用瀏覽器抓 [[goldenberg2022]] 的 24 個檔當「立即可用的先導素材」**
- https://tinyurl.com/2p8tjfnh → Dropbox `Puffs_Continua.zip`(2026-08-12 實測連結活著)
- 母音是 /ɑ/ 不是 /i/,**不建議當正式刺激**,但它讓你**今天**就能拿真人錄的 /ba/ /pa/
  去跑 `snr_audio.py` 的管線、驗證 SNR 適應程序,不必等任何審核或回信
- ⚠️ 下載後第一件事:**確認取樣率**(論文未載明)

**動作 4(不等前三者)—— 準備自錄**
- 依 [[recording-protocol]] 的檢查清單備妥環境與麥克風擺位(**側邊 2–3 cm,離軸**)
- 這是保底方案;即使前兩條成功,自錄的 token 也可當作 talker 變異的對照

### 8.2 拿到檔案之後,三件必做的事

1. **挑 1–4 位語者,不要用全部 20 位。**理由見 §2:20 位語者引入的是**語者變異**,
   那是 [[silbert2018]] 需要另寫一篇論文來建模的東西。
   對齊 [[silbert2012]] 的 4-token 設計比較安全。(我的推論。)
2. **用 Praat / `praat-parselmouth` 實測每個 token 的 VOT**,確認 /bi/ 落在 short lag、
   /pi/ 落在 long lag,並記錄數值進論文方法段。
3. **套用 [[consonant-pair-choice]] §8.4 的兩個修正**:裁齊前導靜音、以**有聲段**RMS 正規化。
   ⚠️ 若走 Shannon 1999,第二項已由原作者做掉("amplitude normalized to the steady-state
   portion of the vowel")。

### 8.3 論文寫作注意

1. **取樣率要交代。**若用 LDC2015S12 的 16 kHz,必須寫明,並說明 speech-shaped noise
   **同樣帶限到 8 kHz**。不要迴避這一點。
2. **不要寫「文獻建議用現成語料庫」。**沒有這回事。正確寫法是「我們使用 X 語料庫,
   因為它提供孤立朗讀的 CV 音節,避免從連續語音切分帶入的共構與韻律變異」。
3. **授權要交代。**LDC 的約定**不允許再散布刺激** —— 若期刊要求公開刺激,這會衝突。
   ⚠️ **這一點請在投稿前確認目標期刊的資料政策。**
   (唯一能公開再散布的是 [[osf-kutlu-mcmurray-continua]] 的 CC0 與
   [[oscaar-speechbox]] 的 CC BY 4.0。)
4. **`stimuli/` 那套 MBROLA 刺激不能出現在論文裡**,連「先導實驗」都不宜 —— 母音是 /ɜ˞/,
   與定案的設計不符(§1)。

---

## 9. 明確的缺口與待查證

**真實的空白 / 已確定的否定結果(不用再查第二次):**
- **沒有任何 Python 套件提供孤立 CV 音節**(實測,§4)。
- **CNC / NU-6 / W-22 詞表湊不出 /bi/–/pi/** —— `PEA` 不在任何詞表裡(§6.1)。
- **Speech Commands 的 35 個詞裡一個 /bi/ 或 /pi/ 開頭的都沒有**("bed"、"bird" 都不是)。
- **[[vctk]] 的 110 語者共同文本有 3 個重音 /pi/,但 0 個可用的 /bi/。**
- **[[listenlab]] 的公開 demo 音檔只有 /d/–/t/ 與 /g/–/k/,沒有 /b/–/p/**(三 repo 全掃)。
- **沒有文獻檢驗過「16 kHz 是否足以保存 /b/–/p/ 的全部知覺線索」。**
- **沒有文獻處理「用 L1-華語語者的 token 給華語聽者聽」是匹配還是雙重偏移**(§5.1)。
- ⚠️ **`listenlab.umn.edu` 網域已不存在;Common Voice 2025-10 起已從 HuggingFace 下架**
  (只在 Mozilla Data Collective 且需登入)。

**必須補的查證(依重要性):**
1. **LDC2015S12 的 $0.00 需登入覆核** —— 我與 subagent 都只讀到未登入頁面的
   `data-price-table`,沒有實際走完結帳。(已做對照組排除「未登入一律顯示 $0」。)
2. **下載後清點 `_s_bi` / `_s_pi` 實際檔數** —— 「各 20 個」是我從 readme 的排除清單
   **推導**的,不是清點檔案的結果。
3. **Silbert & Motlagh Zadeh (2018) 到底用哪套語料** —— 若證實是 LDC2015S12,
   §3.1 的論證強度會大幅提升。全文付費牆擋住。
4. **Shannon 1999 全文** —— 目前只有摘要(OpenAlex 還原)。錄音室細節、每子音的 token 數、
   語者背景都未知。
5. **[[itcp-iowa-consonant]] 的 120 詞完整詞表** —— 論文未列出,`/bi/`、`/pi/` 是否在內未確認。
6. **[[goldenberg2022]] 那 24 個檔的取樣率與實際內容** —— 必須用瀏覽器下載後親自確認;
   論文未載明取樣率,授權也未確認。
7. **⚠️ 沒有任何一個候選的音檔被實際聽過。** 本回顧的所有規格都來自文件與 header,
   **音質、語者間音量差異、口音一致性全部未驗證。**拿到檔案後第一件事是**試聽**。

---

**刺激來源卡**:[[articulation-index-corpus]] · [[shannon1999-consonant-recordings]] ·
[[goldenberg2022]] · [[osf-kutlu-mcmurray-continua]] · [[osf-kapnoula-vot-f0-stimuli]] ·
[[itcp-iowa-consonant]] · [[va-ncrar-speech-materials]] · [[auditec]] ·
[[nonsense-syllable-tests]] · [[haskins-legacy-vot]]
**語料庫卡**:[[free-corpora-comparison]](免費語料庫橫向對照)· [[timit]] ·
[[buckeye-corpus]] · [[librispeech]] · [[vctk]] · [[cmu-arctic]] · [[common-voice]] ·
[[oscaar-speechbox]] · [[ucla-phonetics-archive]] · [[iowa-sounds-of-speech]] · [[listenlab]]
**工具卡**:[[torchaudio-datasets]] · [[huggingface-speech-datasets]] ·
[[speech-python-toolkits]] · [[montreal-forced-aligner]] · [[recording-protocol]] ·
[[mbrola-cannot-do-vot]]
**證據卡**:[[chen2007]] · [[silbert2018]] · [[silbert2012]] · [[winn2020]] · [[chodroff2014]] ·
[[silbert-hawkins2016]]

**其他回顧**:[[natural-vs-synthetic-speech]](為什麼走自然)·
[[consonant-pair-choice]](為什麼是 /b/–/p/ + /i/)· [[synthetic-speech-cognitive-load]]
**專案決策脈絡**:[[決策脈絡_聽覺維度]]

---
標籤note:[[literature-note]] [[speech-perception]] [[刺激來源]] [[AVWM]]
