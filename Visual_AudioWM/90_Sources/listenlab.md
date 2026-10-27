---
tags: [literature-note, 刺激來源, 語音知覺, AVWM]
citekey: listenlab
---

# Winn 的 ListenLab(GitHub + mattwinn.com)— **工具齊全,但公開的 demo 音檔只有 /d/–/t/ 與 /g/–/k/,沒有 /b/–/p/**

**DOI / URL**(全部於 2026-08-12 實際開啟)
- GitHub 組織 https://github.com/ListenLab
- VOT 腳本 repo https://github.com/ListenLab/VOT
- VOT demo 音檔 repo https://github.com/ListenLab/VOT_demo_steps
- 個人站 Praat 頁 http://www.mattwinn.com/praat.html
- 練習音檔頁 http://www.mattwinn.com/practice_sounds.html
- 教學論文 https://doi.org/10.1121/10.0000692(JASA 147(2):852–866)

**查證狀態**(2026-08-12)
- GitHub 組織頁、`VOT`、`VOT_demo_steps` 三頁**皆實際開啟**,repo 清單為逐項抄錄。
- **`LICENSE` 我用 raw 直抓確認**:https://raw.githubusercontent.com/ListenLab/VOT/master/LICENSE
  開頭為 "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007" → **GPL-3.0**。
- **音檔規格是我下載後用 Python `wave` 讀 header 得到的**(`DT_Deer.wav`、
  `DT_VOT_1.wav`、`aud/ga.wav` 三檔),不是轉述。
- ⚠️ **`http://www.listenlab.umn.edu/` DNS 查無**(`getaddrinfo ENOTFOUND`)。
  這個網址**不存在**。搜尋顯示實驗室現址為
  `https://sites.google.com/umn.edu/listen-lab`,但**我沒有實際開啟該頁**,標為未證實。
- ⚠️ `mattwinn.com` **443 埠拒絕連線**(`ECONNREFUSED`),只能走 **HTTP**。
  WebFetch 會自動把 http 升級成 https,所以**必須用 curl 才抓得到**。
- ⚠️ `VOT_demo_steps` **沒有 README、沒有 LICENSE**(GitHub 檔案列表確認),
  所以那 7 個檔的授權狀態**不明**,不能直接套 `VOT` repo 的 GPL-3.0。
- ⚠️ `DT_Deer.wav` / `DT_Tier.wav` 的**錄音者、錄音環境、是否允許再散布,README 未載明,查無**。

```bibtex
@misc{winn_listenlab_vot,
  author       = {Winn, Matthew B.},
  title        = {{ListenLab/VOT}: Praat script to manipulate {VOT} in natural speech},
  howpublished = {\url{https://github.com/ListenLab/VOT}},
  note         = {GPL-3.0. Accessed 2026-08-12},
  year         = {n.d.}
}
```
> **自組**。repo 沒有 `CITATION.cff`,README 指向的正式引用是
> [[winn2020]] 那篇 JASA 教學論文。

## 研究問題
不是研究,是**工具集**。核心命題(README 逐字):

> "Praat script to manipulate VOT in natural speech"

> 透過一連串步驟處理 "pre-existing sounds (e.g. 'deer' and 'tier')" 來
> "generate a continuum varying by VOT and other related properties"

→ **這句話本身就界定了它的定位:它假設你已經有自然錄音,它幫你做成連續體。
它不提供 /b/–/p/ 的錄音。**

## 方法與族群

### GitHub 組織的 10 個 repo(逐項抄錄)
| repo | 描述 | 對 AVWM |
|---|---|---|
| **`VOT`** | "VOT manipulation" | ★ 核心 |
| **`VOT_demo_steps`** | "demo sound output from the VOT continuum script" | ★ 有音檔 |
| `Praat` | "A collection of Praat scripts and Praat-R tools" | 一般 |
| `Fricatives` | "praat script to generate fricative continuum for perception experiments" | 若改做擦音 |
| `Vocoder` | "praat script for vocoding speech" | — |
| `Spectral_ripple` | 電子耳模擬的頻譜漣漪刺激 | — |
| `make_vowel_space` | Praat + R 畫母音空間 | — |
| `R_tools` / `R_custom_spectrogram_from_image` / `small_projects` | 雜項 | — |

### `ListenLab/VOT` 的檔案內容
- 音檔:**`DT_Deer.wav`、`DT_Tier.wav`、`VOT_continuum.wav`**
- 標註:`VOT_continuum.TextGrid`
- 腳本:`Make_VOT_Continuum` v30 – **v33**(README 說最新版會在檔名上標明)
- 文件:`README.md`、**`Winn_2020_VOT_manipulation_tutorial.pdf`**(教學論文 PDF 直接內附)
- `LICENSE` = **GPL-3.0**

README 提到腳本提供三種 VOT 操弄策略,可讓 VOT **獨立變化或與 F0 共變**,
並支援正 VOT 與 **prevoicing(負 VOT)**。
對 `DT_Deer` / `DT_Tier` 這兩個示範音,"The current version of the script will
automatically select the correct landmarks for these sounds."

### 音檔實測規格(我下載讀 header)
| 檔案 | 來源 | 聲道 | 取樣率 | 位元 | 時長 |
|---|---|---|---|---|---|
| `DT_Deer.wav` | `ListenLab/VOT` | mono | **44,100 Hz** | 16 | 0.524 s |
| `DT_VOT_1.wav` | `ListenLab/VOT_demo_steps` | mono | **44,100 Hz** | 16 | 0.526 s |
| `aud/ga.wav` | mattwinn.com 練習頁 | mono | **44,100 Hz** | 16 | 0.690 s |

`VOT_demo_steps` 共 **7 個檔**:`DT_VOT_1.wav` ~ `DT_VOT_7.wav`
→ 即 `deer`–`tier` 的 **7 步 VOT 連續體成品**。

### mattwinn.com 上還有什麼
- **`praat.html`** 掛了約 25 個 Praat 腳本(純 .txt),含
  `Make_VOT_Continuum_v33.txt`、`Make_Formant_Continuum_v46.txt`、
  `Make_Fricative_Continuum13.txt`、`Make_Duration_Continuum.txt`、
  `F0_contour_manipulation_v3.txt`、`praat_vocoder_v59.txt` 等。
  頁內 `#votContinuum` 段落直接連到 https://github.com/ListenLab/VOT。
- **`practice_sounds.html`** 的音檔(逐項抄錄):
  `aud/Heat.wav`、`aud/Hit.wav`、`aud/HeatHit_Continuum_5.wav`、`aud/HeatHit_Continuum_12.wav`、
  **`aud/ga.wav`、`aud/ka.wav`**、`aud/MW_HE.wav`、`aud/MW_WHO.wav`、
  `aud/ieee013.wav`、`aud/ieee410.wav`、`aud/uu_M.wav`、`aud/M4*.wav`(音樂)
- `tools.html` 只有 R / Excel 的分析工具,**無音檔**。

## 結果與限制

### 對 AVWM 的判定:**工具要用,刺激拿不到**
| AVWM 規格 | ListenLab | 判定 |
|---|---|---|
| 英語單一 CV 音節 | `ga`/`ka` 是 CV;`deer`/`tier` 是詞 | ⚠️ 部分 |
| **子音 /b/ 與 /p/** | **完全沒有** | ❌ **關鍵不合** |
| 母音 /i/ 或 /ɑ/ | `ga`/`ka` 是 /ɑ/;`deer`/`tier` 是 /ɪr/ | ⚠️ |
| 取樣率 ≥ 22.05 kHz | **44,100 Hz** | ✅ |
| 能乾淨切出 | 已是獨立檔 | ✅ |
| 多語者 | **單一(推測是 Winn 本人,未證實)** | ❌ |

**所有公開的示範音都是 /d/–/t/(deer/tier)與 /g/–/k/(ga/ka),沒有任何 /b/–/p/。**
我掃過三個 repo 與兩個網頁,確認為 0 命中。

### 但它仍然是本次查證中最重要的**方法學資產**
1. **`Make_VOT_Continuum_v33` 是把「自己錄的 /bi/、/pi/」變成刺激的現成路徑。**
   若 AVWM 最後決定自行錄音(多語者是加分項,這條路本來就有吸引力),
   這個腳本 + [[winn2020]] 的教學論文可以直接省掉方法學摸索。
2. **腳本支援 VOT 與 F0 共變或獨立變化** —— 這正是 GRT 二維設計要的
   「兩個維度可正交操弄」。這是 [[osf-kapnoula-vot-f0-stimuli]] 那批 7×5 格點的製作工具
   (Winn 是該刺激原始論文的共同作者),血緣是通的。
3. GPL-3.0 允許自由使用與修改(注意:GPL 的傳染性只及於**腳本**,不及於腳本產生的音檔)。

### 限制
- `VOT_demo_steps` 無授權宣告,那 7 個檔不可假設可散布。
- `DT_Deer.wav` / `DT_Tier.wav` 的錄音來源不明,同上。
- 實驗室網站 `listenlab.umn.edu` **不存在**;正確網址我未證實。

## 可連結脈絡
- 這些腳本的方法學正文 —— [[winn2020]]
- 用這套工具做出來的成品刺激 —— [[osf-kapnoula-vot-f0-stimuli]](Winn 為共同作者)
- 另一個自然 cross-splicing 的先例 —— [[goldenberg2022]]、[[osf-kutlu-mcmurray-continua]]
- 自然 vs 合成的取捨 —— [[abramson2017]]、[[haskins-legacy-vot]]、[[mbrola-cannot-do-vot]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**Winn 有沒有公開 /b/–/p/ 的刺激音檔?** → **沒有。** 三個 repo + 兩個網頁全掃過,
公開的示範音只有 `deer`/`tier`(/d/–/t/)與 `ga`/`ka`(/g/–/k/)。

**那 Winn 有什麼可以用?** → **工具**:`Make_VOT_Continuum_v33`(GPL-3.0),
可讓 VOT 與 F0 獨立或共變,支援 prevoicing。repo 內還直接附了
`Winn_2020_VOT_manipulation_tutorial.pdf`。

**`VOT_demo_steps` 那 7 個檔是什麼?** → `deer`–`tier` 的 7 步 VOT 連續體成品,
mono/44.1 kHz/16-bit/約 0.526 s。**但 repo 無 README 無 LICENSE,授權不明。**

**為什麼抓 mattwinn.com 一直失敗?** → 該站 **443 埠拒絕連線**,只有 HTTP。
WebFetch 會強制升級成 HTTPS,所以只能用 `curl http://www.mattwinn.com/...`。

**`listenlab.umn.edu` 打不開?** → 那個網域**根本不存在**(DNS 查無)。
