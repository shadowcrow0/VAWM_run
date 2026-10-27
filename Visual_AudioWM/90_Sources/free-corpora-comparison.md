---
tags: [literature-note, 語音語料庫, 刺激來源, 綜合判斷, AVWM]
citekey: free-corpora-comparison
---

# 免費語音語料庫 × /bi/–/pi/ 刺激 — 六個候選的橫向對照與我的結論

> ⚠️ **本卡原名 `natural-speech-sources.md`,與綜合回顧 `review/natural-speech-sources.md`
> 檔名相撞,已更名為 `free-corpora-comparison`。**
> **本卡只涵蓋「免費連續語音語料庫」這一條途徑**;完整的來源排序(含 LDC 的孤立 CV 語料庫、
> 臨床材料、OSF 刺激集、自錄)請見 [[natural-speech-sources]]。

**DOI / URL** 這是一張**綜合卡**,不是單一文獻。各語料庫的逐字查證與 URL 見個別卡片:
[[buckeye-corpus]]、[[librispeech]]、[[vctk]]、[[cmu-arctic]]、[[common-voice]]。
本卡另外查證的次要候選:
- LibriTTS https://www.openslr.org/60/
- L2-ARCTIC https://psi.engr.tamu.edu/l2-arctic-corpus/
- VoxForge https://www.voxforge.org/home
- Speech Commands https://arxiv.org/abs/1804.03209 |
  https://www.tensorflow.org/datasets/catalog/speech_commands

**查證狀態** 2026-08-12 上列全部頁面**實際打開過**。個別語料庫的授權原文、規格數字見各卡。
**本卡的「切 /bi/–/pi/ 的工作量」與「排序建議」整段都是 ⚠️ 我的推論,不是文獻陳述。**
唯一的例外是 CMU ARCTIC 的 token 統計 —— 那是我用 CMUdict 在真實提示表上跑出來的數字。

```bibtex
@misc{avwm2026corpussurvey,
  author = {{AVWM project}},
  title  = {Survey of freely licensed English speech corpora as a source of
            natural /bi/--/pi/ CV stimuli},
  year   = {2026},
  note   = {Internal synthesis note; no external publication.
            Primary sources cited in the linked literature cards.}
}
```
(⚠️ 這不是一篇可引用的文獻,bibtex 僅為卡片格式一致性而存在。)

## 研究問題
AVWM 需要**自然錄音**的 /bi/ 與 /pi/ CV 音節當聽覺維度的刺激(理由見 [[silbert2012]]:
用自然 token 是為了避免對「哪些聲學線索相關」下強假設)。
**免費/開放授權的語音語料庫裡,有沒有一個能真的切出這兩個音節?**

## 方法與族群

### 對照表

| 語料庫 | 授權 | 語者數 | 取樣率 | 音素標註 | 語音類型 | 切 /bi/–/pi/ 的工作量 |
|---|---|---|---|---|---|---|
| **Buckeye** | OSU 專屬合約,**要簽名傳真**;非商業免費;不可散布語料本體 | 40 | **16 kHz** 16-bit mono | ✅ **自動對齊 + 人工校正**(塞音一致性 84.3%);⚠️ 塞音一個 label 涵蓋 closure+burst+送氣 | **自發訪談獨白** | 簽約 1–2 週 + 篩選半天 + **人耳挑選是主要成本,良率極低** |
| **LibriSpeech** | **CC BY 4.0** | 2,484 | **16 kHz** FLAC | ❌ 官方無;✅ 第三方 MFA 對齊(Zenodo 2619474,CC BY 4.0,自述含 phone tier) | 朗讀有聲書(LibriVox 志願者家錄) | 下載 6.3 G + 篩選半天 + **挑語者與人耳過濾 1–2 週** |
| **VCTK 0.92** | **CC BY 4.0**(0.80 是 **ODC-By**) | **110** | **48 kHz** 16-bit(原始 96k/24-bit) | ❌ **完全沒有**,連詞層都沒有 | 朗讀句(報紙 + Rainbow Passage + Stella 段) | 自己跑 MFA,**3–5 天** |
| **CMU ARCTIC** | **BSD 級,「free for any purpose (commercial or otherwise)」,免註冊** | 7 + 11 = **18** | **16 kHz**(原始 32 kHz + **EGG**) | ✅ **附現成 `.lab`**,但 EHMM/Sphinx 全自動,**明說無人工校正** | 朗讀單句(1,132 句,音境平衡) | **技術上半天**(對齊現成),**但產出量不夠** |
| **Common Voice** | **CC0-1.0**(最自由) | 5,705(單一 EN 子集) | **查無官方明文**;格式 **MP3** | ❌ 無 | 眾包朗讀,任意裝置/環境 | 約 1 週,**但我判斷產出不可用於 SNR 實驗** |
| **LibriTTS** | **CC BY 4.0** | (LibriSpeech 同源) | **24 kHz** | ❌ 無 | 同 LibriSpeech,句界切分較乾淨 | 同 LibriSpeech |

### 次要候選(查證後排除)
- **LibriTTS**(openslr.org/60,CC BY 4.0,24 kHz,約 585 小時,附原始+正規化文本):
  比 LibriSpeech 好(取樣率高、切分乾淨),但**通道異質性的問題完全相同**,而且一樣沒有
  官方 phone 對齊。→ **若走 LibriVox 路線就用它,但別走。**
- **L2-ARCTIC**(CC BY-NC 4.0,24 位非母語者,6 種 L1,**有人工校正的 TextGrid**,
  Zhao et al. 2018 Interspeech 2783–2787,要填下載表):
  用**同一份 ARCTIC 提示表** → /bi/、/pi/ 一樣稀少;非母語者 VOT 偏離英語常模。
  → **對本專案無用;但若日後做跨語言 VOT 就很有價值。**
- **VoxForge**(voxforge.org,**GPL** 授權的語音):
  ⚠️ 我只確認了「submitted audio files under the GPL license」與網站仍在(© 2006-2026),
  **規模、取樣率、有無音素標註我都查無明文**。
  → **GPL 用在音檔上法律關係詭異(衍生作品的定義不清),加上眾包錄音、資訊不足,排除。**
- **Speech Commands**(CC BY 4.0,**16 kHz,1 秒孤立詞**,4,000+ 語者,約 105,000 個樣本,
  Warden 2018 arXiv:1804.03209):
  **這是唯一「孤立單詞」的候選,格式最接近 CV 音節。**
  但完整詞表是:
  > "yes no up down left right on off stop go zero one two three four five six seven eight
  > nine bed bird cat dog happy house marvin sheila tree wow"(+ backward/forward/follow/
  > learn/visual)
  → **裡面一個 /bi/ 或 /pi/ 開頭的詞都沒有。**("bed" 是 /bɛd/,"bird" 是 /bɝd/。)
  → **完全排除。這是一個乾淨的否定結果,不用再回頭查了。**

## 結果與限制

### ⚠️ 我的推論:從連續語音切 CV 音節的三個結構性問題
(這一整節是判斷,不是文獻陳述。)

**(1) 重音不對等 —— 這是最嚴重的一個。**
英語裡 /bi/ 最高頻的載體是 **"be"**,而它是**功能詞**,在朗讀與自發語音中幾乎必然弱讀:
音長短、F0 平、強度低。/pi/ 最高頻的載體是 **"people" / "peace" / "peas"**,全是**實詞**,
帶主重音。
→ 如果你直接拿 "be" 的 /bi/ 對上 "peace" 的 /pi/,**voicing 差異會與音長、強度、F0
全面共變**。對 GRT 而言這不是小瑕疵:**它等於偷偷加了第三個維度進 2×2 設計**,
而 GRT 的整個推論架構建立在「兩個維度」上。這會讓 perceptual separability 的估計無法解釋。
→ **解法只有一個:兩邊都只用帶主重音的實詞**(beach/bead/beak/beam/bean/beat vs
peace/peak/peel/peat/piece)。而一旦加上這個限制,所有語料庫的產出量都會暴跌。

**(2) coarticulation 與右側語境。**
CV 音節不會單獨出現。從 "beach" 切出 /bi/,你切到哪裡?
- 切在母音穩定段中間 → 拿到的是被截斷的母音,聽起來不自然。
- 切到 /tʃ/ 之前 → 母音後段已經帶 /tʃ/ 的 F2 轉折。
- "people" 的第一音節後面緊接 /p/ → 母音後段被第二個 /p/ 的閉合影響。
→ **要湊出右側語境對等的 /bi/–/pi/ 配對,實務上等於要求「兩個詞的第二個子音相同」。**
CMUdict 裡真正配得起來的最小對立組只有幾組:**beach/peach、beak/peak、beat/peat、
bead/(無)、bean/(無)、bee/pea、beep/peep、beam/(無)**。
→ **`bee`–`pea` 與 `beach`–`peach`、`beak`–`peak`、`beat`–`peat` 是唯一乾淨的路。**

**(3) 語速。**
自發語音(Buckeye)語速變異最大;朗讀單句(ARCTIC、VCTK)最穩;有聲書(LibriSpeech)
居中但受朗讀者風格影響。**VOT 隨語速縮放**,所以語速變異會直接變成 VOT 變異
(見 [[chodroff2017]]、[[chodroff2019]])。對一個要精準操弄 voicing 的實驗,這是額外雜訊。

### ⚠️ 我的排序建議

**如果一定要從現成語料庫切:**
1. **VCTK 0.92** —— 錄音品質壓倒性最好(半消音室 / 48 kHz / 110 人統一設定),
   授權乾淨(CC BY 4.0)。代價是**要自己跑 MFA**(3–5 天),而且共同文本只給 /pi/
   (people×2、peas×1)不給 /bi/,/bi/ 得去翻各語者不同的報紙句。
2. **LibriSpeech / LibriTTS** —— 唯一「量絕對夠」的,第三方 MFA 對齊現成。
   但 LibriVox 是志願者家錄,**通道異質性對 SNR 實驗是致命的**。
3. **CMU ARCTIC** —— 授權最好、對齊現成、有 EGG、技術上半天搞定;
   **但每位語者只有 8 個重音 /pi/,量根本不夠。**
4. **Buckeye** —— 標註最好,但**自發對話語音的弱化正好是 AVWM 要避開的東西**。
5. **Common Voice** —— MP3 + 不受控通道,對 SNR 實驗不可用。
6. **Speech Commands / VoxForge / L2-ARCTIC** —— 已排除(理由見上)。

**⚠️ 但我真正的建議是第七個選項:自己錄。**
理由不是懶,是上面的分析指向同一個結論:
- **沒有任何一個語料庫同時滿足「錄音乾淨 + 有對齊 + /bi/ 與 /pi/ 數量對稱且重音對等」。**
  最好的三個各缺一項,而缺的那一項都不是靠工程可以補的。
- AVWM 需要的 token 數其實**很少**。[[silbert2012]] 的 2×2 GRT 實驗每類只用了
  **4 個 token**(而且是作者本人錄的)。你需要的是 8–16 個乾淨 token,不是 4,000 個髒 token。
- 錄 `bee / pea` 或 `beach / peach` 各 4–8 次,一個母語者、一小時、一支好麥克風就結束。
  **VCTK 的方法段可以直接當錄音規格照抄**(見 [[vctk]] 回查線索)。
- 這也正好符合 GRT 語音實驗的既有慣例([[silbert2012]] 作者自錄、
  [[silbert-hawkins2016]] 同一路線)。

→ **語料庫調查的價值不在於找到來源,而在於證明「自己錄」是有根據的選擇,
以及提供錄音規格的參照(VCTK)與 VOT 常模的參照(Buckeye / [[chodroff2019]])。**

### 本卡的限制
- 我**沒有下載任何語料本體**,所以上面所有關於「切出來會怎樣」的敘述都是從規格與
  文本推的,**沒有聽過任何一個實際 token**。
- **只有 CMU ARCTIC 的 /bi/、/pi/ 數量是實測**(我抓了完整提示表用 CMUdict 跑)。
  LibriSpeech 的數量是**用 ARCTIC 的比例外推**,VCTK 的是**只算了兩段共同文本**,
  Buckeye 完全沒算(拿不到文本)。
- Zenodo 那份 LibriSpeech 對齊檔**是否真的含 phone tier,我沒有開檔驗證**
  (Zenodo 描述說有,但 CorentinJ 的鏡像 README 只講詞層)。**這是 pipeline 的第一個
  待驗證點。**

## 可連結脈絡
- **全部途徑的排序與建議(本卡的上層)** —— [[natural-speech-sources]]
- ⭐ **本卡結論的重要例外**:LDC 有**專門錄孤立 CV 音節**的語料庫,不必從連續語音切
  —— [[articulation-index-corpus]]、[[shannon1999-consonant-recordings]]
- 各語料庫詳卡 —— [[buckeye-corpus]]、[[librispeech]]、[[vctk]]、[[cmu-arctic]]、[[common-voice]]
- 為什麼要自然而非合成 —— [[silbert2012]]、[[natural-vs-synthetic-speech]]、[[mbrola-cannot-do-vot]]
- 自己錄的前例與 token 數基準 —— [[silbert2012]]、[[silbert-hawkins2016]]
- 子音對的選擇 —— [[consonant-pair-choice]]、[[burst-vot-tradeoff]]、[[abramson2017]]
- VOT 的自然分布與語速縮放 —— [[chodroff2017]]、[[chodroff2019]]、[[chodroff2014]]
- SNR 當聽覺維度 —— [[snr_audio]]、[[snr_vs_grt_dimension]]、[[winn2013]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**免費語料庫裡哪一個最適合切 /bi/–/pi/?** → **沒有一個真的適合。**最好的三個各缺一項:
VCTK 缺對齊與 /bi/、LibriSpeech 缺通道一致性、CMU ARCTIC 缺數量。
**→ 我的結論是自己錄,錄音規格照 VCTK,token 數照 [[silbert2012]](每類 4 個)。**
**Speech Commands 有 /bi/ 或 /pi/ 的詞嗎?** → **一個都沒有。**35 個詞裡最接近的
"bed"(/bɛd/)、"bird"(/bɝd/)都不是。**這個否定結果不用再查第二次。**
**從連續語音切 CV,最大的陷阱是什麼?** → **重音不對等**。/bi/ 最常見的載體 "be" 是弱讀
功能詞,/pi/ 最常見的載體 "people/peace" 是重讀實詞 → voicing 會與音長/強度/F0 共變,
**等於在 2×2 GRT 裡偷偷加了第三個維度**。
**哪些 /bi/–/pi/ 詞對在右側語境上是對等的?** → bee–pea、beach–peach、beak–peak、
beat–peat、beep–peep。(用 CMUdict 查 `B IY1 X` 與 `P IY1 X` 同尾的組合。)
**哪個語料庫可以當錄音規格的參照?** → VCTK:半消音室、DPA 4035 + Sennheiser MKH 800、
96 kHz/24-bit 錄、降到 48 kHz/16-bit、手動 end-point。
