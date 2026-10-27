---
tags: [literature-note, 錄音規範, 方法學, 刺激製作, 自錄語音, AVWM]
citekey: recording-protocol
---

# 自己錄語音刺激的規範(綜合證據卡)

**DOI / URL**
- Švec & Granqvist (2010) https://doi.org/10.1044/1058-0360(2010/09-0091) | PMID 20601621
- NC State Phonetics Lab 錄音手冊 https://phon.wordpress.ncsu.edu/lab-manual/sound-recording/
- 台灣在地設備先例 —— [[chen2007]] §3.4

**查證狀態**(2026-08-12)
- **Švec & Granqvist:⚠️ 只讀到摘要**(ASHA 全文頁 403;摘要經 Europe PMC REST API 取得)。
  下列數值全部出自摘要,**教學正文未讀**,細節與適用條件不明。
- **NC State 手冊:頁面已完整讀過**,引句逐字。⚠️ 這是一份**大學實驗室的內部手冊**,
  不是同儕審查文獻;它的權威來自「被實際使用」,不是被驗證過。
- **[[chen2007]] 的設備段:PDF 全文已讀**,引句逐字。
- ⚠️ **UCL 的 `phon.ucl.ac.uk` 錄音課程頁我嘗試抓取但連線被拒(ECONNREFUSED),
  未能納入。**

```bibtex
@article{svec2010microphones,
  author  = {{\v S}vec, Jan G. and Granqvist, Svante},
  title   = {Guidelines for Selecting Microphones for Human Voice Production Research},
  journal = {American Journal of Speech-Language Pathology},
  volume  = {19}, number = {4}, pages = {356--368}, year = {2010},
  doi     = {10.1044/1058-0360(2010/09-0091)}
}
@misc{ncsuphon_recording,
  author       = {{NC State Phonetics Lab}},
  title        = {Sound recording (Lab Manual)},
  howpublished = {\url{https://phon.wordpress.ncsu.edu/lab-manual/sound-recording/}},
  note         = {查閱於 2026-08-12}
}
```
> ⚠️ NC State 那筆 BibTeX 是**我自組**的;該頁未提供建議引用格式。

## 研究問題
如果 AVWM 走 [[natural-speech-sources]] 的**路線 C(自己錄)**,「錄得夠好」的操作定義是
什麼?哪些參數是有文獻背書的門檻,哪些只是慣例?

**一個 /b/–/p/ 專屬的問題**:**/p/ 的爆破會直接吹到麥克風產生 pop**,而 pop 的低頻能量會
污染 burst 與送氣段 —— 也就是污染 VOT 量測本身所依賴的那兩個地標。這不是一般錄音品質
問題,是**對本專案的依變項有直接後果**的問題。

## 方法與族群
三份來源的性質完全不同,不能等量齊觀:

| 來源 | 性質 | 權威來源 |
|---|---|---|
| Švec & Granqvist (2010) | *AJSLP* 同儕審查 **tutorial** | 期刊、聲學推導 |
| NC State 手冊 | 大學實驗室內部 SOP | 實務慣例 |
| [[chen2007]] §3.4 | 單一研究的方法段 | 在地先例(台灣、36 位語者) |

## 結果與限制

### 1. 麥克風規格(Švec & Granqvist 2010,⚠️ 僅摘要)
摘要中的具體數值:
- 頻率響應在關注頻段內應**平坦,變異 < 2 dB**
- 麥克風**等效噪音位準**應比**最輕發聲**的音壓級**低至少 15 dB**
- 摘要提到 **30 cm 與 5 cm** 兩種距離的數值指引
- 指向性麥克風要注意**近接效應(proximity effect)**

⚠️ 「頻率範圍」的下限應涵蓋**預期最低 F0**,上限涵蓋**關注的最高頻譜成分**;摘要用的是
一般性措辭,**沒有給 /b/–/p/ 這種塞音的具體上限建議**。

### 2. 擺位、取樣、增益(NC State 手冊,頁面已讀)
逐字引句:
> "head-mounted microphone is often the best choice for recording speech"
> "microphone ideally located about **2cm to the side of the corner of the mouth**"
> "head-mounted microphone should be placed so that the microphone is **2-3 centimeters from
> the corner of the mouth, not in front**"

**⭐ "not in front" 這四個字就是 /p/ 爆破音的解方**,而且它與 Švec & Granqvist 的離軸建議
方向一致。(這個「對 /p/ 特別要緊」的連結是**我加的**,兩份來源都沒有針對塞音討論。)

其餘規格:
- 取樣率 **44.1 kHz**;錄製 **32-bit float**,分析前轉 **16-bit**
- **單聲道**優於立體聲
- **隔音室(sound booth),門關上**
- 事後在 Praat 用 `Scale peak`,`New absolute peak is 0.99`
- 軟體:Audacity 或 Praat

⚠️ **該頁不提供**重複次數(repetitions)或載體句(carrier phrase)的建議 —— 這兩項在該手冊
是空白,不是有建議而我沒抄。

### 3. 台灣在地的設備先例([[chen2007]] §3.4,全文已讀)
> "Each subject was scheduled to record the word lists in a **soundproof booth**, using a
> **high-quality microphone (AKG C1000S)** and a **professional 2-channel mobile digital
> recorder (MicroTrack 24/96)**."

**→ 一組在台灣、對 36 位語者實際跑完的組合。**AKG C1000S 是電容式,MicroTrack 24/96 支援
24-bit/96 kHz。⚠️ 兩者都是 2007 年的機型,現已停產;**這是「等級的參考」,不是採購清單。**

### 4. token 數的慣例(來自 GRT 語音文獻,不是錄音文獻)

| 研究 | 每類 token 數 | 語者 |
|---|---|---|
| [[silbert2012]] | **4** | 作者本人 1 位 |
| Silbert & Motlagh Zadeh (2018) *JASA* 143(5), 2780 | 10 | 20 位 |
| [[articulation-index-corpus]] | 1(每語者) | 20 位 |
| Shannon et al. (1999) | 代表性 token | 10 位 |

⚠️ **[[silbert2012]] 用 4 個 token 的理由是「防止受試者鑽某個 token 的漏洞」,不是「取樣
類別」**(見該卡的專章),原文明說變異是被刻意壓小的("a small degree of within-category
variability")。**所以 4 這個數字不能當成「取樣充分性」的標準。**

## 對 AVWM 的最小可行檢查清單(⚠️ 這份清單是**我綜合三份來源編的**,不是任何一份的原文)

**錄音前**
1. 安靜空間(隔音室最佳;退而求其次:小房間、軟裝、關空調與除濕機)
2. 麥克風:電容式,頻率響應平坦度 < 2 dB;等效噪音低於最輕發聲 15 dB 以上
3. **擺位:嘴角側邊 2–3 cm,離軸,不要正對嘴前**(/p/ 的 pop)
4. 44.1 kHz(或 48 kHz)、32-bit float 或 24-bit、**單聲道**
5. **關掉所有自動增益(AGC)與效果**
6. 試錄最大聲的 /pi/,確認峰值不削波(留 −6 dB 以上餘裕)

**錄音中**
7. 每個目標音節錄**遠多於**最終要用的數量(建議 ≥ 10 次),事後篩選
8. 隨機化 /bi/ 與 /pi/ 的順序,避免整批連念產生節律化
9. ⚠️ **載體句 vs 孤立朗讀是一個實質決定**:[[chen2007]] 用雙音節詞會**壓低** VOT;
   [[articulation-index-corpus]] **兩種都錄**。AVWM 的目標是**單獨呈現的單音節**,
   因此應以**孤立朗讀**為主。(此推論為我所加。)

**錄音後(這三項專屬於 AVWM,來自 [[consonant-pair-choice]] §8.4 的實測)**
10. **用 Praat 實測每個 token 的 VOT**,確認 /bi/ 落在 short lag、/pi/ 落在 long lag
    —— 對台灣語者尤其必要,見 [[chen2007]] 的 /b/ 端空白
11. **裁齊前導靜音** —— 現有 `be.wav`/`pe.wav` 差 36 ms,比整個知覺邊界區還大
12. **以有聲段(非整檔)RMS 正規化** —— 現有實作殘留 0.30 dB 差異
    (⚠️ Shannon et al. 1999 的語料據稱已對母音穩態段正規化,可省下這一步)

## 可連結脈絡
- 完整的來源比較與排序 —— [[natural-speech-sources]]
- 自錄的已發表先例(作者本人錄、每類 4 token) —— [[silbert2012]]
- 台灣語者念英語塞音的實測風險 —— [[chen2007]]
- 現成孤立 CV 語料庫(省掉整條錄音路線) —— [[articulation-index-corpus]]
- 必須修的兩個施工問題(前導靜音、RMS) —— [[consonant-pair-choice]] §8.4
- 為什麼要走自然刺激 —— [[natural-vs-synthetic-speech]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**麥克風該放哪裡才不會被 /p/ 的爆破吹爆?** → 嘴角**側邊** 2–3 cm、離軸,不要正對嘴前
(NC State;Švec & Granqvist 的近接效應警告方向一致)。
**「錄得夠好」有沒有可查的數字門檻?** → 有兩個:頻率響應平坦度 < 2 dB、等效噪音低於最輕
發聲 ≥ 15 dB(Švec & Granqvist 2010 摘要)。
**GRT 語音實驗每類用幾個 token?** → 4([[silbert2012]])到 10(Silbert & Motlagh Zadeh 2018);
但 4 那個數字的理由是防漏洞,不是取樣充分性。
