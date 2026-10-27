---
tags: [literature-note, VOT, 發音部位, 辨識函數斜率, 唇音vs軟顎音, 適應式程序]
citekey: goldenberg2022
---

# Goldenberg et al. (2022) — 唯一一筆唇音 vs 軟顎音的組內斜率比較

**DOI / URL** https://doi.org/10.3389/fnhum.2022.879981 | PMC9334670
**閱讀狀態** **全文已讀**(由 subagent 取回並核對引句)。⚠️ 本卡引用的是該研究的**附帶觀察**,不是它的主要結論。

```bibtex
@article{goldenberg2022congruent,
  author  = {Goldenberg, Dolly and Tiede, Mark K. and Bennett, Ryan T. and
             Whalen, D. H.},
  title   = {Congruent aero-tactile stimuli bias perception of voicing continua},
  journal = {Frontiers in Human Neuroscience},
  volume  = {16}, pages = {879981}, year = {2022},
  doi     = {10.3389/fnhum.2022.879981}
}
```

## 研究問題
本篇的主題是**氣流觸覺**:對皮膚吹氣會不會讓聽者更傾向報告無聲塞音?(先前研究只做端點,本篇沿整條連續體做。)

**但對 AVWM 而言,本卡的價值完全在於它順帶做了一件別人沒做的事:在同一批受試者、同一個實驗裡,同時建了唇音與軟顎音兩條 VOT 連續體,並分別報告了辨識函數的參數。**

## 方法與族群
三條連續體:雙唇("pa/ba")、軟顎("ka/ga")、以及一條母音連續體("head/hid")當控制組。

**刺激製作(原文)** —— 這也是自然 cross-splicing 的一個可用先例:
> "Two eight-step VOT continua were then created, one for the bilabial and one for the
> velar place of articulation. The continua were created by **removing the initial burst
> from one of the voiceless exemplars (/pa/ or /ka/) and then systematically shortening
> the aspiration in log-scaled steps**, with the final step matching the mean aspiration
> duration of the voiced token."

受試者數我未確認。

### ★ 刺激取得(2026-08-12 新增查證)—— **作者確實釋出了那 24 個音檔**

先看**正式的** Data availability,它其實是**沒有公開資料**的那種寫法(逐字):
> "The raw data supporting the conclusions of this article will be made available by the
> authors, without undue reservation."

**但真正有用的資訊藏在 Materials and Methods 的「Acoustic stimuli」小節末尾的註腳 1**(逐字):
> "The 24 sound files used as acoustic stimuli are available as Supplementary Material
> from https://tinyurl.com/2p8tjfnh"

**⚠️ 2026-08-13 更正:檔案已被刪除,這條路不通。**

短網址仍解析到:
```
https://www.dropbox.com/scl/fi/w2gocofutqe1oftrbcjw7/Puffs_Continua.zip
    ?rlkey=48m3e1gijk2ece2767pb2jcgw&dl=0
```
但用 `dl=1` 抓回來的是 190 KB 的 HTML,其 `<title>` 為 **"Dropbox - File Deleted"**。
**HTTP 200 是誤導** —— Dropbox 對已刪除的檔案一樣回 200,只是內容換成提示頁。
先前記錄的「連結是活的」是根據狀態碼判斷,**不成立**。

另外兩條路也查過,都沒有:
- **PMC9334670** 沒有 supplementary 檔案區
- **Frontiers 官網**的 supplementary 段落只是指回同一個 Dropbox 連結

→ **要拿到這 24 個檔只能寫信給作者。**

**刺激的原始規格**(論文 Methods,我讀到的):
- 語者:**一位單語美式英語男性母語者**
- 錄了 /pa/、/ba/、/ka/、/ga/ **各 6 個 token**
- 做成**兩條 8 步 VOT 連續體**(雙唇 + 軟顎)
- 共 24 個音檔
- ⚠️ **取樣率論文未載明,查無。**

**這是本次刺激搜尋中,唯一一個「真正的孤立自然 /ba/–/pa/ CV 音節」來源。**
母音是 /ɑ/(AVWM 的第二順位母音),8 步,單一語者。
對照:[[osf-kutlu-mcmurray-continua]] 母音是 /i/ 但那是 CVC 單詞;
[[osf-kapnoula-vot-f0-stimuli]] 是孤立 CV 且有二維格點但母音是 /ʌ/。

## 結果與限制
**本卡要用的那一段(原文)**:
> "The bilabial category boundary is approximately centered between its endpoints, that
> is, its bias (4.2) is close to its midpoint (4.5). The bias was calculated as the 50%
> crossover point of the psychometric function for the continuum, computed across all
> listeners. **Acuity (a measure of boundary slope) was computed as the difference between
> the 25 and 75% probabilities for the discrimination function.** The velar category
> boundary is not as centralized and is **skewed toward voicelessness (bias = 3.6)**; that
> is, longer VOTs were necessary for /ka/ responses. **The velar acuity (2.0) is shallower
> than that of the bilabial (1.1)**, possibly due to this skew."

**⚠️ 注意 acuity 的定義方向**:它是 25–75% 的**寬度**,所以**數值越大 = 函數越淺**。軟顎音 2.0 vs 唇音 1.1 → **軟顎音的辨識函數寬度約為唇音的兩倍。**

**對 AVWM 的三個後果(我的推論)**:
1. **適應式程序估斜率:函數越淺,同樣試次數換到的 β 精度越差。**軟顎音要付更多試次。
2. **邊界偏斜(bias 3.6 vs 中點 4.5)代表對稱性假設不成立。**AGRT 的雙極結構預期邊界大致落在中點;唇音(4.2)貼近,軟顎音明顯偏離。
3. 淺而偏斜的維度,知覺分布更難與 GRT 的高斯假設相容。

**限制**:
- 這是**單一研究的附帶觀察**,不是為比較部位而設計的實驗;作者自己用 "**possibly** due to this skew" 的試探語氣。
- 兩個數字都是**跨全體聽者**計算的,沒有報告個體變異。
- 本篇的主要操弄(氣流觸覺)與 AVWM 無關,不應引用本卡去支持任何觸覺相關主張。
- 受試者數未確認。

**另外報告的產出數值**(轉引自 Byrd 1993,⚠️ 二手):無聲 / 有聲(ms)—— 唇音 44/18、舌尖音 49/24、軟顎音 52/27。

## 可連結脈絡
- 發音部位的選擇(本卡是該回顧的關鍵證據)—— [[consonant-pair-choice]]
- 子音混淆矩陣正典來源與現代複製(voicing 的知覺穩健度)—— [[子音混淆最小化]]、[[miller-nicely1955]]、[[wang-bilger1973]]
- 軟顎音的其他結構性問題 —— [[kingston1983]]、[[frisch2016]]
- 產出 VOT 的現代大語料庫版本 —— [[chodroff2017]]
- cross-splicing 的方法學正解 —— [[winn2020]]
- 辨識函數斜率不宜當「類別性」指標 —— [[mcmurray2022]]
- **作為刺激來源的橫向比較** —— [[osf-kapnoula-vot-f0-stimuli]]、[[osf-kutlu-mcmurray-continua]]、[[natural-speech-sources]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**有沒有人在同一個實驗裡比較過不同發音部位的辨識函數斜率?** → 本篇,而且是我找到的唯一一筆。
**哪個部位的類別邊界不置中?** → 軟顎音(bias 3.6 vs 中點 4.5)。這對假設對稱的適應程序是問題。

**Goldenberg 有沒有把刺激公開?** → **曾經有,現在沒了。**
正式的 Data availability 寫的是「向作者索取」;真正的連結藏在 **Methods 的註腳 1**:
https://tinyurl.com/2p8tjfnh → Dropbox 的 `Puffs_Continua.zip`(24 個音檔)。
**⚠️ 2026-08-13 實測:檔案已刪除。** Dropbox 對已刪除檔案照樣回 HTTP 200,
抓回來的是 190 KB 的 HTML,`<title>` = "Dropbox - File Deleted"。
**用狀態碼判斷連結死活會被騙,要看內容。** PMC 與 Frontiers 都沒有備份。
→ **只能寫信給作者。** 取樣率查無。

**哪裡有「真正的孤立自然 /ba/–/pa/ CV 音節」?** → **理論上就是這篇的那 24 個檔**
(單一美式英語男性、母音 /ɑ/、8 步),這是本次全部查證中唯一同時符合
「孤立 + 自然 + /b/–/p/」三條件的來源 —— **但檔案已經拿不到了。**
實際可取得的次佳選項見 [[natural-speech-sources]]。
