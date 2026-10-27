---
tags: [literature-note, 刺激來源, 語音知覺, AVWM]
citekey: osf-kapnoula-vot-f0-stimuli
---

# OSF `qxmyk`「English VAS stimuli」— **7(VOT) × 5(F0) 自然 "buh"–"puh" 正交格點,44.1 kHz,已下載驗證**

**DOI / URL**
- OSF 專案 https://osf.io/qxmyk/ (DOI `10.17605/OSF.IO/QXMYK`)
- 論文 https://www.nature.com/articles/s41598-026-47943-3
- 檔案直鏈 https://osf.io/download/ew7yh/ (`English VAS stimuli.zip`)

**查證狀態**(2026-08-12)
- **我實際下載了 `English VAS stimuli.zip`(1,096,815 bytes)並解開。** 以下 35 個檔名與
  音訊規格是我用 Python `wave` 模組**逐檔讀 header 得到的**,不是轉述。
- OSF metadata 走 `https://api.osf.io/v2/nodes/qxmyk/` 取得(`public: true`,
  `date_created: 2026-01-23`)。網頁版 https://osf.io/qxmyk/ 是 SPA,WebFetch 讀不到內容,
  **所以我改用 OSF API**。
- 論文本文由 WebFetch 讀取(需經 `idp.nature.com` 兩段轉址才能拿到全文)。
  刺激製作的數字是**論文 Methods 的引句**。
- ⚠️ **`node_license` 回傳 `None` —— 這個 OSF 專案沒有設定任何授權。**
  不是 CC0,也不是 CC BY。要用必須自己判斷或去信詢問。
- ⚠️ **語者性別、人數、錄音環境:論文未載明,我查無。** 從單一連續體推斷應為單一語者,
  但這是**我的推論**。
- ⚠️ 論文寫英語刺激「取自先前研究」以維持可比性。我**沒有展開該引用編號**;
  依關鍵字比對推測是 Kapnoula, Winn, Kong, Edwards & McMurray (2017) JEP:HPP
  (PubMed 28406683),**此血緣為推論,未證實**。

```bibtex
@article{wong2026consistency,
  author  = {Wong, Brian W. L. and Samuel, Arthur G. and Kapnoula, Efthymia C.},
  title   = {Speech perception consistency facilitates initial lexical activation,
             but not speech perception flexibility},
  journal = {Scientific Reports},
  year    = {2026},
  url     = {https://www.nature.com/articles/s41598-026-47943-3}
}

@misc{wong2026osf,
  author       = {Wong, Brian W. L. and Samuel, Arthur G. and Kapnoula, Efthymia C.},
  title        = {{Speech Perception Consistency Facilitates Initial Lexical Activation,
                  but Not Speech Perception Flexibility}},
  howpublished = {OSF},
  year         = {2026},
  doi          = {10.17605/OSF.IO/QXMYK}
}
```
> ⚠️ 兩則 BibTeX 皆為**我自組**。論文的 Data availability 逐字只給了一句話
> (見下),官方沒有指定刺激的引用格式。

## 研究問題
論文本身問的是「知覺一致性(consistency)會不會促進初期詞彙活化」,**與 AVWM 無關**。
本卡的價值**完全在於它的刺激檔**。

論文 Data availability 逐字:
> "The datasets generated during and/or analyzed during the current study are available
> in the OSF repository, https://doi.org/10.17605/OSF.IO/QXMYK"

## 方法與族群

### OSF `Stimuli` 資料夾的四個檔(我用 API 列出)
| 檔名 | 大小 (bytes) | 直鏈 |
|---|---|---|
| `English VAS stimuli.zip` | 1,096,815 | https://osf.io/download/ew7yh/ |
| `English VWP recording.zip` | 9,581,271 | https://osf.io/download/h53w2/ |
| `Spanish VAS stimuli.zip` | 722,965 | — |
| `Spanish VWP recording.zip` | 10,979,456 | — |

**我只下載了 `English VAS stimuli.zip`**,另外三個未下載(避免大檔),內容未確認。

### `English VAS stimuli.zip` 的實測內容
**35 個 wav,命名為 `B_NP_F0_{1..5}_VOT_{1..7}.wav`** —— 即一個
**5 (F0) × 7 (VOT) 的完整正交格點**。

**全部 35 檔規格完全一致**(我逐檔驗過,`unique specs` 只有一組):

| 項目 | 實測值 |
|---|---|
| 聲道 | mono |
| 取樣率 | **44,100 Hz** |
| 位元深度 | 16-bit |
| 時長 | **0.520 s**(每一檔都一模一樣) |

(zip 內另有 `__MACOSX/._*` 的 macOS resource fork 垃圾檔,可忽略。
**無 README、無 txt/pdf 說明文件** —— 我掃過整份檔案清單,確認沒有。)

### 論文 Methods 對這批刺激的描述(引句)
> 刺激 "drawn from a natural-speech 'buh'–'puh' continuum in English"

> "seven VOT steps (1 to 45 ms; step size ≈7–8 ms) and five F0 steps
> (90–125 Hz in 8.75 Hz increments)"

英語刺激用 **cross-splicing**;F0 的變化用 **PSOLA**(pitch-synchronous overlap-add)產生。

→ 檔名裡的 `VOT_1..7` 對應 1–45 ms,`F0_1..5` 對應 90–125 Hz,**方向與對應關係我未驗證**
(沒有 README,也沒實際量測聲學),要用前應自己在 Praat 裡量一次。

## 結果與限制

### 為什麼這是本次搜尋的**最佳命中**
**它已經是一個二維正交格點,而不是一條一維連續體。**
VOT × F0 這兩個維度正是 GRT 文獻裡用來測 perceptual separability / integrality 的經典配對
(見 [[silbert2012]]、[[kingston2008]]),而別人已經把 7×5 = 35 個格點做好、
用自然語音、對齊到同一時長了。這省掉的不只是錄音,是整套 cross-splicing + PSOLA 的製作工。

| AVWM 規格 | 本刺激集 | 判定 |
|---|---|---|
| 英語單一 CV 音節 | "buh"/"puh",**是孤立 CV** | ✅ |
| 子音 /b/ 與 /p/ | ✅ | ✅ |
| 母音優先 /i/,其次 /ɑ/ | **/ʌ/** | ❌ **不合** |
| 取樣率 ≥ 22.05 kHz | **44,100 Hz** | ✅ 超標 |
| 能乾淨切出 | 已切好,0.520 s 等長 | ✅ |
| 多語者加分 | **推測單一語者** | ❌ |
| 授權 | **未設定** | ⚠️ |

### 限制 / 風險
1. **母音是 /ʌ/,不是 /i/。** 這是與目標規格唯一的硬衝突。
   若母音維度在 AVWM 裡不承載操弄,/ʌ/ 是否可接受是一個**設計決策**,不是技術問題。
2. **沒有授權。** OSF `node_license` 為空。可以下載使用,但**不能假設可重散布**;
   若 AVWM 要把刺激連同論文公開,必須先取得作者同意。對照 [[oscaar-speechbox]] 的 CC BY 4.0。
3. **沒有 README。** 刺激的物理參數(每一步實際的 VOT/F0 值、burst 對齊方式)
   全部得自己回頭量。論文只給了範圍與步階大小。
4. **單一語者。** 若 AVWM 要多語者變異,這批不夠。
5. **`VOT_1` 到底是 1 ms 還是 45 ms 端我沒驗證。** 命名方向要自己確認。

## 可連結脈絡
- VOT × F0 作為 GRT 維度配對的理論依據 —— [[silbert2012]]、[[kingston2008]]、[[silbert-hawkins2016]]
- 同一血緣的另一批 McMurray 系刺激(CC0、母音 /i/) —— [[osf-kutlu-mcmurray-continua]]
- 製作這類刺激的工具與方法學 —— [[winn2020]]、[[listenlab]]
- 自然 vs 合成的取捨 —— [[abramson2017]]、[[haskins-legacy-vot]]
- 其他自然語音取得管道 —— [[natural-speech-sources]]、[[oscaar-speechbox]]
- 子音配對的選擇 —— [[consonant-pair-choice]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**有沒有現成、可下載、自然語音的 VOT × F0 二維格點?** → **有,而且是本次搜尋唯一一個。**
OSF `qxmyk` 的 `English VAS stimuli.zip`,7 VOT × 5 F0 = 35 檔,mono/44.1 kHz/16-bit/0.520 s,
全部等長。直鏈 https://osf.io/download/ew7yh/

**它的母音是什麼?** → **/ʌ/("buh"–"puh")**,不是 /i/。這是與 AVWM 規格唯一的硬衝突。

**可以拿去公開重散布嗎?** → **不確定,OSF 沒設授權**(`node_license: None`)。
自用沒問題,要公開得先問作者。

**為什麼 WebFetch 抓 osf.io 抓不到東西?** → OSF 網頁是 SPA。
改打 `https://api.osf.io/v2/nodes/<id>/` 與 `.../files/osfstorage/<folder_id>/`,
分頁參數要用 `-G --data-urlencode "page[size]=200"`(方括號直接放進 URL 會被吃掉)。
