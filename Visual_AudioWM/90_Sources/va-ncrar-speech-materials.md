---
tags: [literature-note, 刺激來源, 聽力學, AVWM]
citekey: va-ncrar-speech-materials
---

# VA 語音測驗光碟(Wilson 系列)—— Disc 4.0 **全是詞**;**Disc 2.0 Track 9 才是 CV 音節**,且可用聲道分離切出 /bɑ/ /pɑ/

**DOI / URL**
- 訂購頁 https://chs.asu.edu/shs/audio-cds-speech-audiometry
- **Disc 4.0 說明書 PDF** https://chs.asu.edu/sites/g/files/litvpz611/files/2022-05/booklet-speech_recid_disc_4.0_0.pdf
- **Disc 2.0 說明書 PDF** https://chs.asu.edu/sites/g/files/litvpz611/files/2022-05/booklet-tone-speech_version_2.pdf
- NCRAR 官網 https://www.ncrar.research.va.gov/
- VA/DoD CAPD 測驗清單 https://www.ncrar.research.va.gov/Documents/AuditoryProcessingTests.pdf

**查證狀態(2026-08-12)**
**本卡的核心內容是我逐頁讀過原始說明書 PDF 得到的,不是轉述。**
兩份 PDF 我都下載並用 `pypdf` 完整抽取文字(Disc 4.0 = 24 頁;Disc 2.0 = 25 頁),
包含**逐軌腳本與完整詞表**。下述軌道內容、詞表內容、參考文獻均為 PDF **明文**。
訂購與捐款金額出自 ASU 訂購頁,為官方明文引句。
凡屬我的推論(尤其「聲道分離可切出孤立 CV」)已逐條標明。

```bibtex
@misc{wilson2006speechrecid,
  author       = {Wilson, Richard H.},
  title        = {Speech Recognition and Identification Materials, Disc 4.0},
  year         = {2006},
  note         = {音訊 CD;2011 年再版(黃色片)。VA Rehabilitation Research and
                  Development Service 贊助,James H. Quillen VA Medical Center,
                  Mountain Home, TN 製作。非論文,故以 @misc 建卡},
  howpublished = {\url{https://chs.asu.edu/shs/audio-cds-speech-audiometry}}
}

@misc{wilson1998tonalspeech,
  author       = {Wilson, Richard H.},
  title        = {Tonal and Speech Materials for Auditory Perceptual Assessment, Disc 2.0},
  year         = {1998},
  note         = {音訊 CD;為 1992 年 Disc 1.0 的改版。Track 9--10 為雙耳分聽 CV 音節。
                  非論文,故以 @misc 建卡},
  howpublished = {\url{https://chs.asu.edu/shs/audio-cds-speech-audiometry}}
}

@article{berlin1973dichotic,
  author  = {Berlin, Charles I. and Lowe-Bell, Sandra S. and Cullen, John K. and
             Thompson, Charles L. and Loovis, Charles F.},
  title   = {Dichotic speech perception: An interpretation of right-ear advantage
             and temporal offset effects},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {53}, pages = {699--709}, year = {1973},
  note    = {書目逐字抄自 Disc 2.0 說明書參考文獻列表(第 793--795 行);DOI 未查證,故不填}
}

@article{wilson1996identification,
  author  = {Wilson, Richard H. and Leigh, E. D.},
  title   = {Identification performance by right- and left-handed listeners on the
             dichotic consonant-vowel (CVS) materials recorded on the VA-CD},
  journal = {Journal of the American Academy of Audiology},
  volume  = {7}, pages = {1--6}, year = {1996},
  note    = {書目逐字抄自 Disc 2.0 說明書參考文獻列表(第 880--882 行)}
}
```

## 研究問題
VA/NCRAR 這套「Speech Recognition and Identification Materials」光碟,常被當成臨床語音材料的公定來源。
它到底裝了什麼?**有沒有孤立 CV 音節?** 拿不拿得到?能不能用在研究上?

## 方法與族群
這不是研究,是**材料發行**。由 Richard H. Wilson(VA Senior Research Career Scientist, Audiology)
在 Mountain Home TN 的 VA Auditory Research Laboratory 編製,供 VA 聽力師做補償與撫卹(C&P)鑑定。
現由 **Arizona State University** 的 College of Health Solutions 對外發行。

## 結果與限制

### Disc 4.0 = 全部是詞,**沒有任何 CV 音節**(已用全文檢索確認)

我對抽出的 24 頁全文做 `grep -i "syllab|CV|nonsense|dichotic|consonant"`,
**除了參考文獻裡一個 "Monosyllabic Words" 的論文標題外,零命中**。
軌道內容為:1000 Hz 校正音、CID W-1 揚揚格詞、Maryland CNC 詞表、CID W-22 詞表、
NU No. 6 詞表(含對側競爭句)、Rush Hughes 版 PB-50 詞表、Words-in-Noise (WIN)、
西班牙語圖片辨識、500 Hz MLD。**全是詞或音調,沒有音節。**

**→ 任務清單裡「NCRAR 的 CD 有沒有子音辨識用的 CV 音節?」的答案:Disc 4.0 沒有。**

### CNC / NU-6 / W-22 能不能切出 /bi/ /pi/? —— **不能,而且我有詞表證據**

我對說明書裡**實際印出的詞表**(CNC 1/3/6/7/9、W-22 1A–4A、NU-6 1A–4A、PB-50 8B)
做了 /b/ 與 /p/ 起首詞的窮舉:

- **/b/ 起首**:BACK BAD BAKE BALL BAR BASE BATH **BEAN BEAT BED BEE BEEF** BEG BELL BET BID BIG BILL BIND BIRTH BIT BITE BOAT BOLT BONE BOOK BOOST BORED BOTH BOUGHT BREAD BUD BUG BUN BURN BUSH BY
- **/p/ 起首**:PACE PAD PAGE PAIN PALE PALM PAN PASS PATH **PEAK** PEARL PEG PERCH PEW PHONE PICK PICTURE PIE PIECE PIKE PILE PILL PINE PINT POD POLE POOL POPE POWER PUFF PUN PURGE

**關鍵不對稱(這是我從詞表推論出來的)**:
高前母音 /i/ 的詞裡,/b/ 有 BEE(**而且 BEE 就是真正的開音節 CV /bi/**)、BEAT、BEAN、BEEF;
**/p/ 這邊只有 PEAK 一個**,而 **PEA 完全不存在**。
所以 **/bi/–/pi/ 的最小對比在這些詞表裡湊不出來**。

即使退而求其次去切 CVC 的前半段,也有兩個硬傷(**我的推論**):
1. 切掉尾音會破壞尾音協同構音,而且清尾音前的母音本來就較短(pre-fortis clipping),
   BEAT 與 PEAK 的母音長度本就不可比;
2. 每個詞在一份詞表裡**只出現一次,且只有一位語者** —— 拿不到 token 變異,也拿不到多語者。

**→ 這條路我判定不可行。** 詞表是詞表,不是音節庫。

### Disc 2.0 Track 9–10 = **真的有 CV 音節**,而且我讀到了逐條腳本

說明書明文(Disc 2.0,Track 9):

> "This 155-s stereo track contains the 30 possible pairings of six nonsense (CV) syllables
> (**BA, DA, GA, PA, TA, and KA**) in a dichotic format (Berlin, Lowe-Bell, Cullen, Thompson,
> & Loovis, 1973; Wilson & Leigh, 1996). The syllables were digitized (from the right channel of
> an analog tape produced by **Kresge Hearing Research Laboratory, New Orleans**), edited, and
> aligned at the VA Medical Center, Long Beach."

Track 10 與 Track 9 相同,但**左聲道延遲 90 ms**。

說明書還印出了**每一對的時間碼與左右聲道內容**。例如 Track 9:

```
13. 1:03  BA   DA        14. 1:08  BA   PA
20. 1:39  PA   TA        23. 1:55  PA   BA
27. 2:16  BA   TA        28. 2:21  BA   KA        30. 2:31  BA   GA
```

30 對 = 6 個音節的全部有序配對(6×5),因此 **BA 在左聲道出現 5 次、右聲道 5 次;PA 同理**。
Track 9 單軌就有 **10 個 BA、10 個 PA** 的 token 位置,Track 10 再來一輪。

**可行的取出路徑(這是我的推論,標明)**:Track 9 是**同時起始**的立體聲,
左右聲道各自是一個獨立的單音節錄音。把 CD 的 L / R 聲道分離,
再依說明書的時間碼切段,就能得到**孤立的自然 /bɑ/ 與 /pɑ/**,44.1 kHz(CD 規格)。
數位 CD 的聲道串音可忽略,所以切出來應該是乾淨的。
**但這一步我沒有實際驗證過 —— 我手上沒有這片 CD。**

**這條路的限制(重要)**:
1. **母音是 /ɑ/,不是 /i/** —— 落在次選,不是首選。
2. **應該只有一位語者。** Berlin et al. (1973) 的原始材料是 Kresge 實驗室的單一錄音;
   說明書沒有寫語者人數。**「單語者」是我的推論,未經證實。** → 「多語者加分」這項拿不到。
3. **Token 已被編輯過**:說明書明說經過 "edited, and aligned"。做過切齊與電平調整,
   原始的 VOT 與起始瞬態**可能已被動過**。對 AVWM 這種要精確控制聲學維度的實驗,這是實質風險。
4. 來源是**類比磁帶轉錄**(1973 年的 tape),高頻底噪與帶寬受限於當年設備 ——
   即使容器是 44.1 kHz,**有效帶寬不等於 22 kHz**。(我的推論)

### 取得方式與費用

ASU 訂購頁明文:

> "We do not sell the CDs, but rather we ask for a donation. Typically, we receive donations of **$100/disc**."

> "Requested CDs are sent out the next day by Priority Mail"

- **誰可以要**:訂購頁未設限,任何人聯絡 Richard H. Wilson 指明要哪片即可。
  (Disc 4.0 說明書封面寫明:聯邦政府部門經 VA 的 Auditory and Vestibular Dysfunction REAP 取得;
  **私部門經 Arizona State University Foundation 取得**。)
- **付款**:ASU Foundation 線上捐款頁 / 支票寄 College of Health Solutions / Email 洽詢。
- **價格查證日期 2026-08-12。**

### 授權能不能用於研究?

**未能確認。** 兩份說明書與訂購頁我都讀過,**沒有任何一處寫著授權條款、著作權聲明或使用範圍限制**。
只有 Disc 4.0 說明書提到材料來源是「public domain 或相關個人的慷慨授權」:

> "the availability of the materials either through the public domain or through the generosity of
> the individuals responsible for the materials"

**這句話不等於允許再散布。** 沒有明文授權,不代表可以自由使用,也不代表不可以。
**若要用,必須直接寫信向 Wilson / ASU 確認「切割後的 token 能否用於研究、能否隨論文公開」。**
我不會替它假設一個授權狀態。

## 可連結脈絡
- 自然語音來源總覽 —— [[natural-speech-sources]]
- 規格上更好但取得管道有風險的對照 —— [[shannon1999-consonant-recordings]]
- 同一批 CV 材料的商業版(Auditec DCV) —— [[auditec]]、[[nonsense-syllable-tests]]
- 授權乾淨、但要切 CVC 的替代 —— [[itcp-iowa-consonant]]
- 語者變異與維度分離 —— [[silbert2012]]
- 聽力學的詞表傳統 —— [[humes1993]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**VA 的語音光碟裡有沒有 CV 音節?** → **Disc 4.0 沒有(全文檢索零命中);Disc 2.0 Track 9–10 有**(BA DA GA PA TA KA,雙耳分聽)。
**NU-6 / CNC / W-22 能不能切出 /bi/–/pi/?** → **不能**。詞表裡有 BEE,但 **PEA 根本不存在**,/p/+/i/ 只有 PEAK。已用實際印出的詞表窮舉驗證。
**Disc 2.0 的 CV 母音是什麼?幾位語者?** → /ɑ/;語者人數說明書未載,我推論為單一語者(Kresge 實驗室 1973 錄音)。
**多少錢?怎麼拿?** → 非賣品,以捐款方式索取,慣例 $100/片,聯絡 Richard H. Wilson(ASU)。查證日 2026-08-12。
**為什麼「已 edited and aligned」是個問題?** → 因為切齊與電平正規化可能動到 VOT 與起始瞬態,而那正是 AVWM 要操弄的維度。
