---
tags: [literature-note, 刺激來源, 聽力學, AVWM]
citekey: auditec
---

# Auditec of St. Louis —— 臨床語音材料的商業總代理;**授權條款明文禁止散布,是這條路的致命傷**

**DOI / URL**
- 官網 https://auditec.com/
- **條款** https://auditec.com/terms-conditions/
- **價目表 PDF(2022c)** https://auditec.com/wp-content/uploads/2022/05/2022c-price-list.pdf
- Nonsense Syllable Test 產品頁 https://auditec.com/2015/09/23/nonsense-syllable-test/
- Dichotic Consonant-Vowel 產品頁 https://auditec.com/2015/08/04/dichotic-consonant-vowel-dcv/
- 產品總表 https://auditec.com/price/

**查證狀態(2026-08-12)**
價目表 PDF 我下載後用 `pypdf` 抽出全文,下列品項與價格是 **PDF 明文逐行**,非轉述。
條款頁與兩個產品頁我實際打開讀過,引句為官方明文。
**「不能用於研究」是我的推論,不是 Auditec 的明文** —— 條款根本沒提到研究,詳見下方。
所有價格**查證日期 2026-08-12**,幣別 USD,未含運費(部分品項標示美國本土免運)。

```bibtex
@misc{auditec2022pricelist,
  author       = {{Auditec, Inc.}},
  title        = {Auditec, Inc. Price List (2022c)},
  year         = {2022},
  note         = {商業語音測驗錄音發行商,St.\ Louis, MO。非論文,故以 @misc 建卡。
                  價格查證日 2026-08-12},
  howpublished = {\url{https://auditec.com/wp-content/uploads/2022/05/2022c-price-list.pdf}}
}
```

## 研究問題
NU-6、CNC、W-22 的商業錄音由誰發行、多少錢、能不能用於研究並在論文中描述?
更重要的是 —— **Auditec 有沒有賣孤立的 CV 音節 / 無意義音節產品?**

## 方法與族群
不是研究,是商業發行商。自述銷售 "over 200 recordings",客群是
"audiologists, psychologists, speech-language pathologists, hearing professionals,
and other trained medical professionals"。
VA/DoD 的 CAPD 工作小組清單(NCRAR 官網 PDF,2024-01-08 版)把 Auditec 列為
**編號 1 的來源**,絕大多數聽處理測驗都指向它 —— 它實質上是這個領域的總代理。

## 結果與限制

### 與 /b/–/p/ CV 相關的品項(價目表明文,含編號與價格)

| 品項 | 編號 | 價格(USD) | 與 AVWM 的相關性 |
|---|---|---|---|
| **Dichotic Consonant-Vowel©** | 175 | **$74.75** | **最相關** —— 就是 CV 音節對 |
| Nonsense Syllable Test©(= Edgerton-Danhauer) | 190 | $80.50 | 相關但結構不符 |
| California Consonant Test© | 119 | $102.75 | **是詞不是音節** |
| Dichotic Digits, Standard© | 197 | $94.75 | 無關(數字) |
| Dichotic Sentence Identification© | 176 | $110.25 | 無關(句子) |

USB 版本另計(如 USB190 = $86.50、USB175 = $80.75)。

**Dichotic Consonant-Vowel (DCV)** 產品頁明文:
"pairs of consonant-vowel (CV) syllables",有同時起始版本與**一耳領先 90 ms** 的錯開版本;
可觀察 right ear advantage、lag effect、auditory capacity effect;附 PDF 指導語與計分表,含 5 歲以上常模。

> **產品頁沒有寫語者人數、也沒有寫是哪些音節、哪個母音、也沒有引用 Berlin et al.**
> 我實際讀了頁面,這些資訊**不在上面**。
> **我的推論**:這極可能與 [[va-ncrar-speech-materials]] 的 Disc 2.0 Track 9/10 是同一批
> Berlin et al. (1973) 材料 —— 因為兩者的「90 ms 錯開」設計與六音節典範完全吻合。
> **但這是推論,Auditec 沒有明說,我沒有證據。** 若要走這條路必須寫信問。

### Nonsense Syllable Test 的結構問題

產品頁明文:"consists of two 25-element lists in six randomizations",另名
Edgerton-Danhauer Nonsense Syllable Test,適用兒童與成人。

> **產品頁沒有寫音節結構(CV / VC / CVC)、沒有寫子音母音清單、沒有寫語者人數或性別。**
> 我讀了頁面,這些**都不在上面**。**未能確認它是否含孤立 CV。**
> (文獻上 Edgerton-Danhauer NST 一般被描述為 CVC 無意義音節,但我這次**沒有查證到**,故不寫入。)

### 授權 —— **這是本卡最重要的發現**

條款頁明文:

> "Customers may create **one** backup of Auditec recordings for their own personal use."

> "Each purchased recording gives license for **up to two audiometers at one location**."

> "**Sharing and distribution are prohibited.**"

產品頁上的著作權聲明另外禁止 "sharing, uploading to servers, publishing to the internet,
and all other forms of distribution",並禁止上傳到伺服器或雲端供多人共用。

**條款全文完全沒有提到「研究用途」** —— 既沒允許也沒禁止。以下是**我的推論**:

1. 買一份、在**單一地點的實驗室內**播放給受試者聽,**大致落在授權範圍內**
   (「two audiometers at one location」的精神);但實驗用的是電腦不是 audiometer,
   嚴格說已在條款文字之外。
2. **把 token 切出來、重新合成、隨論文公開刺激檔 —— 明確違反 "Sharing and distribution are prohibited"。**
3. 因此對 AVWM 這種**需要切割、操弄、且理想上要開放刺激以利重現**的研究,
   Auditec 路線**在授權上是死路**,除非另行取得書面授權。
4. "all sales are final" —— 買了不能退。買下去之前無法試聽確認音質與音節內容,**風險全在買方**。

**行動建議**:如果真的要走 Auditec,**先寫信問清楚三件事再付錢**:
(a) DCV 的音節清單、母音、語者人數;(b) 取樣率與原始母帶來源;
(c) 是否可為研究目的切割並在論文中公開刺激。得到書面答覆前不要下單。

## 可連結脈絡
- 同一批 Berlin CV 材料的非商業管道(且說明書公開、資訊透明得多) —— [[va-ncrar-speech-materials]]
- 各種無意義音節測驗的比較 —— [[nonsense-syllable-tests]]
- 授權乾淨的替代方案 —— [[itcp-iowa-consonant]]、[[articulation-index-corpus]]
- 規格最佳解 —— [[shannon1999-consonant-recordings]]
- 自然語音來源總覽 —— [[natural-speech-sources]]
- 聽力學詞表傳統 —— [[humes1993]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**Auditec 有賣 CV 音節嗎?** → 有,Dichotic Consonant-Vowel(編號 175,$74.75),但產品頁不寫音節清單、母音與語者人數。
**Auditec 的材料能用於研究並公開刺激嗎?** → **不能公開**。條款明文 "Sharing and distribution are prohibited",且「每份授權限一地點兩台聽力計」。條款完全沒提研究用途。
**Auditec 的 NST 是 CV 還是 CVC?** → **未能確認**,產品頁沒寫。
**為什麼說 Auditec 是「總代理」?** → VA/DoD CAPD 工作小組 2024 清單裡,絕大多數測驗的來源編號都指向 Auditec。
