---
tags: [literature-note, 語音語料庫, 刺激來源, 強制對齊, AVWM]
citekey: cmu-arctic
---

# CMU ARCTIC — 授權最自由、附現成 phone label,但 /pi/ 每人只有 8 個

**DOI / URL**
- 官方頁 http://festvox.org/cmu_arctic/(⚠️ **只有 http,沒有 https**)
- 各語者頁 http://festvox.org/cmu_arctic/dbs_bdl.html(slt / clb / rms / jmk / awb / ksp 同理)
- 打包檔目錄 http://festvox.org/cmu_arctic/packed/
- 單一語者目錄結構 http://festvox.org/cmu_arctic/cmu_arctic/cmu_us_bdl_arctic/
- 授權檔 http://festvox.org/cmu_arctic/cmu_arctic/cmu_us_bdl_arctic/COPYING
- 提示句表 http://festvox.org/cmu_arctic/cmuarctic.data
- 技術報告 CMU-LTI-03-177 http://festvox.org/cmu_arctic/cmu_arctic_report.pdf
- 論文 https://www.isca-archive.org/ssw_2004/kominek04b_ssw.html

**查證狀態** 2026-08-12 **實際打開**上列全部頁面(用 curl,因為 festvox.org 不支援 https,
WebFetch 會被 https 升級擋掉)。**COPYING 全文、AREADME 全文、一個 `.lab` 檔
(`lab/arctic_a0001.lab`)、以及完整的 1,132 句提示表 `cmuarctic.data` 都實際抓下來讀過**。
下方的 /bi/、/pi/ 統計是**我自己用 CMUdict(cmusphinx/cmudict master)跑出來的數字**,
不是文獻陳述,但是**在真實提示表上算的,不是估計**。**沒有下載音檔本體**。

```bibtex
@inproceedings{kominek2004arctic,
  author    = {Kominek, John and Black, Alan W},
  title     = {The {CMU} {Arctic} speech databases},
  booktitle = {Fifth ISCA Workshop on Speech Synthesis (SSW5)},
  pages     = {223--224},
  year      = {2004}
}
```
⚠️ **官網本身沒有指定引用格式**,只連到技術報告 CMU-LTI-03-177。上面這筆是社群通用的
標準引用(我在 ISCA Archive 確認過該篇存在)。若要嚴謹,兩個都引。

## 研究問題
不是研究問題,是資源建置:為 unit-selection 語音合成建一組**音境平衡(phonetically
balanced)、單語者、錄音室品質**的英語資料庫。

## 方法與族群
官網原文:
> "The databases consist of around 1150 utterances carefully selected from out-of-copyright
> texts from Project Gutenberg. ... The distributions include **16KHz waveform and
> simultaneous EGG signals**. Full phoentically labelling was perfromed by the CMU Sphinx
> using the FestVox based labelling scripts."
(原文有兩個拼字錯誤,照抄。)

- **1,132 句提示**(我抓下 `cmuarctic.data` 實際數過:1,132 行)
- **語者數:7 個主要 + 11 個追加 = 18 個**
  - 主要:bdl(US 男)、slt(US 女)、clb(US 女)、rms(US 男)、jmk(加拿大男)、
    awb(蘇格蘭男)、ksp(印度男)
  - 追加(packed/ 目錄):aew, ahw(德), aup(印), axb(印,女), eey(女), fem(德),
    gka(印), ljm(女), lnh(女), rxr(以色列), slp(印)
- **錄音條件**(dbs_bdl.html 原文):
  > "This was recorded at **16bit 32KHz**, in a **sound proof room**, in **stereo**,
  > one channel was the waveform, the other **EGG**."
  → 發布的 packed 版是 **16 kHz**;32 kHz + EGG 的原始版另外放在 `orig/`。
  **有 EGG(電子聲門圖)是很少見的加分項** —— 可以直接看聲帶起振時刻。

### **有現成的 phone label(`lab/`),但完全沒有人工校正**
dbs_bdl.html 原文:
> "The database was automatically labelled using CMU Sphinx using the FestVox labelling
> scripts. **No hand correction has been made.**"

AREADME 對 `lab/` 的說明:「autolabelled phone labels」。
我實際抓的 `lab/arctic_a0001.lab` 內容(ESPS/Festival label 格式,時間單位為秒):
```
#
0.040000 125 pau
0.200000 125 ao
0.300000 125 th
0.410000 125 er
...
2.310000 125 iy
```
→ **ARPAbet 小寫、無 stress digit、每行一個 phone 的結束時間**。母音 /i/ 標為 `iy`。

### 授權:**最自由的一個**
COPYING 全文開頭逐字:
> "**This voice is free for use for any purpose (commercial or otherwise)** subject to the
> pretty light restrictions detailed below."

限制只有三條(Carnegie Mellon University, Copyright (c) 2003):
> "1. The code must retain the above copyright notice, this list of conditions and the
> following disclaimer. 2. Any modifications must be clearly marked as such.
> 3. Original authors' names are not deleted."

→ 等同 BSD/MIT 級。**不用註冊、不用簽約、不用填表、直接 wget。**
在所有候選裡,只有 CMU ARCTIC 允許商業用途且無任何再散布限制。

## 結果與限制

### ⚠️ 這是我實際跑出來的數字,不是推估:提示表裡的 /bi/ 與 /pi/
我用 CMUdict 對 `cmuarctic.data` 的 10,039 個詞 token 逐一查音,取**開頭為 `B IY` /
`P IY`** 的:

| 類別 | 總 token 數 | 明細 |
|---|---|---|
| `B IY1`(重音 /bi/) | **40** | be 29、beach 3、being 3、beating 2、beatrice 1、beady 1、b 1 |
| `P IY1`(重音 /pi/) | **8** | people 4、peace 2、peterborough 1、peeled 1 |
| `P IY0`(弱讀) | 14 | pierre 10、pierre's 2、piano 2 |

**每一位語者都唸同一組 1,132 句 → 上表就是「每位語者能拿到的上限」。**

**⚠️ 我的判斷:這個數字直接判了 CMU ARCTIC 死刑。**
- **/pi/ 只有 8 個**,其中 `people`×4 是雙音節詞的第一音節(右側緊接 /p/,coarticulation
  無法避免);`peace`×2;`Peterborough`、`peeled` 各 1。**單一語者實際可用的乾淨 /pi/ 大概 2–6 個。**
- **/bi/ 的 40 個裡有 29 個是 "be"** —— 朗讀語音裡 "be" 仍是功能詞,通常弱讀、短。
  真正重音的實詞只有 beach×3、being×3、beating×2 等,**約 10 個**。
- GRT 需要每個刺激類別有**可比的、數量對稱的** token。
  **這裡 /bi/ 與 /pi/ 的可用量差了一個數量級,而且兩邊的重音狀態不對等。**
- 就算把 18 個語者全用上,也只是拿到 18 組相同的、同樣稀少的詞 —— **跨語者不能混用**,
  因為那會把語者身分帶進 GRT 的知覺空間。

**句首位置更慘**:我另外算過,1,132 句裡**句首**是 /bi/ 候選詞的有 **0 句**、
/pi/ 候選詞的有 **1 句**。→ 想拿「前面沒有任何音、最乾淨」的 token,基本上沒有。

**工作量估計(我的推估)**:下載單一語者 packed 檔(數百 MB)→ 用現成 `lab/` grep
`b iy` / `p iy` 序列(**半小時,因為對齊已經現成**)→ 切檔 → 人耳挑。
**技術上是所有候選裡最快的(半天),但產出量根本不夠。**

### 順帶:L2-ARCTIC(同一套提示表,非母語者版)
https://psi.engr.tamu.edu/l2-arctic-corpus/ —— 24 位非母語者(印地語、韓語、華語、
西班牙語、阿拉伯語、越南語各 4 人),**forced-aligned 的詞與音素邊界 + 每人約 150 句
人工校正的 TextGrid**(標了 substitution/deletion/addition 三類發音錯誤)。
授權 **CC BY-NC 4.0**,要填下載表(姓名/單位/email)。引用 Zhao et al. (2018) Interspeech 2783–2787。
⚠️ **我的判斷:對 AVWM 無用** —— 用的是同一份 ARCTIC 提示表,所以 /bi/、/pi/ 一樣稀少;
而且非母語者的 VOT 分布本來就偏離英語常模,對「英語 /b/–/p/ 知覺」的實驗是雜訊不是資產。
(⚠️ 但如果專案哪天要做**跨語言 VOT**,這份就變得很有價值。)

## 可連結脈絡
- 跨語料庫對照與最終建議 —— [[natural-speech-sources]]
- 需要多少 token 才夠 GRT —— [[silbert2012]](每類 4 個 token、每刺激 200 trial)
- EGG 可以直接看聲帶起振 → 與 VOT 測量 —— [[abramson2017]]、[[burst-vot-tradeoff]]
- 詞首 vs 詞中、重音對等問題 —— [[consonant-pair-choice]]
- 錄音品質更好但沒對齊的替代 —— [[vctk]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**哪個語音語料庫附現成的 phone label 檔?** → CMU ARCTIC 的 `lab/` 目錄,ESPS/Festival 格式
(時間 + 125 + ARPAbet 小寫)。**但是 EHMM/Sphinx 自動標的,官網明說 "No hand correction
has been made."**
**哪個語音語料庫授權最寬鬆?** → CMU ARCTIC:「free for use for any purpose (commercial or
otherwise)」,BSD 級三條件,免註冊。
**CMU ARCTIC 的 1,132 句裡有幾個 /pi/?** → **重音 /pi/ 只有 8 個**(people 4、peace 2、
Peterborough 1、peeled 1);重音 /bi/ 40 個但其中 29 個是弱讀的 "be"。
**→ 這是「授權最好 ≠ 內容可用」的教科書案例。**
**哪個語料庫有 EGG?** → CMU ARCTIC(原始 32 kHz stereo,一軌波形一軌 EGG)。
**同一套 ARCTIC 提示表的非母語者版?** → L2-ARCTIC,24 人 6 種 L1,CC BY-NC 4.0,
有人工校正的發音錯誤標註。
