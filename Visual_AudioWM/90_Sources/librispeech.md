---
tags: [literature-note, 語音語料庫, 刺激來源, 強制對齊, AVWM]
citekey: librispeech
---

# LibriSpeech(+ 第三方 forced alignment)— 量最大、授權最乾淨、但錄音通道最雜

**DOI / URL**
- 官方下載頁 https://www.openslr.org/12/
- 論文 doi:10.1109/ICASSP.2015.7178964 | dblp https://dblp.org/rec/conf/icassp/PanayotovCPK15.html
- **第三方 phone 對齊(Zenodo)** https://zenodo.org/records/2619474 — doi:10.5281/zenodo.2619474
- 第三方對齊(GitHub 鏡像,詞層為主) https://github.com/CorentinJ/librispeech-alignments
- 第三方對齊(HuggingFace 整理版) https://huggingface.co/datasets/gilkeyio/librispeech-alignments
- 衍生的 TTS 版 LibriTTS https://www.openslr.org/60/

**查證狀態** 2026-08-12 **實際打開** openslr.org/12、zenodo.org/records/2619474、
CorentinJ 的 README、gilkeyio 的 HF dataset card、openslr.org/60。**沒有下載任何語料**
(最小的 dev-clean 也有 337 MB;對齊檔 623 MB)。因此**檔案內部結構沒有親自驗證**,
下面關於對齊檔內容的敘述來自各資源頁的自述。標「⚠️ 我的推論」處是我的判斷。

```bibtex
@inproceedings{panayotov2015librispeech,
  author    = {Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and
               Khudanpur, Sanjeev},
  title     = {Librispeech: An {ASR} corpus based on public domain audio books},
  booktitle = {2015 IEEE International Conference on Acoustics, Speech and
               Signal Processing (ICASSP)},
  pages     = {5206--5210},
  year      = {2015},
  doi       = {10.1109/ICASSP.2015.7178964}
}
```
(openslr.org/12 頁面明文指定此篇為引用對象。)

## 研究問題
建一個夠大、**授權完全自由**的英語 ASR 訓練語料。來源是 LibriVox 的公眾領域有聲書錄音,
文本對到 Project Gutenberg。

## 方法與族群
- **授權:CC BY 4.0**(openslr.org/12 頁面明文)。這是所有候選裡**限制最少**的之一。
- **取樣率 16 kHz**,FLAC。
- 約 **1000 小時**朗讀英語;子集:dev-clean / dev-other / test-clean / test-other /
  train-clean-100 (6.3 G) / train-clean-360 (23 G) / train-other-500 (30 G)。
- 語音類型:**朗讀有聲書**(不是自發、也不是孤立音節)。
- **官方沒有 phone 層標註**。官網只說文本「has been carefully segmented and aligned」,
  那是**詞/句層**的對齊,不是音素層。

### 第三方 forced alignment(這是它能用的關鍵)
Zenodo record 2619474,作者 Loren Lugosch (Mila),2019-03-31,**CC BY 4.0**,
單檔 `librispeech_alignments.zip` 623 MB。描述逐字:
> "This contains phoneme alignments and word alignments (= labels for each timestep) for
> all 980 hours of LibriSpeech."

產生方式:**Montreal Forced Aligner + 官方預訓練的 LibriSpeech acoustic model**。
輸出為 TextGrid,詞層與 phone 層分開。

⚠️ **注意一個不一致**:CorentinJ 的 GitHub 鏡像 README **只描述詞層對齊**
(`.alignment.txt`,每個詞的結束時間),我在該 README 裡**沒有看到任何 phone 層的說明**。
gilkeyio 的 HF 版本標為 CC-BY-4.0、涵蓋七個子集共 292k 筆,但 dataset card 我讀到的段落
**沒有寫明 phone 標籤集**(ARPAbet?有沒有 stress digit?)。
→ **要用之前必須先抓 Zenodo 那份 zip 驗證 phone tier 真的存在且標籤集為何。這一步我沒做。**

## 結果與限制

### ⚠️ 我的推論:能不能切出乾淨的 /bi/、/pi/?
**量沒問題,通道有問題。**

**(1) 量**:1000 小時朗讀語音大約 9–10 M 詞。用 CMUdict 查,英語裡開頭是
`B IY1` 的詞有 287 個、`P IY1` 的有 244 個(我 2026-08-12 用 cmudict.dict 實際跑出來的數字)。
在 CMU ARCTIC 的 10,039 詞樣本裡,重音 /bi/ 佔 0.40%、重音 /pi/ 佔 0.08%
(見 [[cmu-arctic]])。**⚠️ 用這個比例外推**到 LibriSpeech train-clean-100(約 100 小時、
接近 1 M 詞),預期約 **4,000 個 /bi/、800 個 /pi/** token。就算九成不可用,剩下的也遠超
GRT 需要的數量。**這是所有候選裡唯一「量絕對夠」的。**

**(2) 但通道是致命傷**:LibriVox 是**志願者在自己家裡錄的**。麥克風、房間殘響、底噪、
壓縮歷史、錄音電平全部不同,而且**同一個語者內也可能不同**(不同時期錄不同章節)。
對 AVWM 這是嚴重問題,因為:
- 你的聽覺維度**就是 SNR**。刺激本身自帶的、不受控的通道噪音會直接汙染你要操弄的維度。
- 就算只用單一語者(LibriSpeech 有 2,484 位語者,單一語者可有數小時),你也還是拿到
  一個未知且不均勻的錄音鏈。
→ **⚠️ 我的判斷:如果聽覺維度是 SNR,LibriSpeech 的通道異質性是 disqualifying 的,
不是「可以事後 normalize 掉」的等級。**

**(3) 位置問題**(這條對所有連續語音語料庫都成立):
- 詞首單音節詞("be", "bee", "beat", "pea", "peak", "peace", "piece")是唯一可能乾淨的來源。
- 但 **"be" 幾乎永遠是弱讀功能詞**,而 "peace"/"people" 是實詞、帶重音 → 兩邊的
  音長、F0、強度系統性不同。
- 從詞中切(例如 "people" 的第一個音節)會帶到右側 coarticulation(/pi/ 之後接 /p/)。
- **朗讀語音的優點是語速比自發語音穩定**,這是 LibriSpeech 比 Buckeye 好的地方。

**工作量估計(我的推估)**:
下載 train-clean-100 (6.3 G) + 對齊檔 (623 MB) → 寫 script 用 TextGrid 篩 `B IY1` /
`P IY1` 序列(半天)→ 依語者 ID 分組、挑錄音品質一致的單一語者(1–2 天,需人耳)→
切檔 + 逐一聽 + 挑掉弱讀/被打斷/背景噪音的(**這是主要成本,以千計的 token 要人工過濾**)→
音量正規化。**合計約 1–2 週,而且結局很可能是「找不到通道夠乾淨的語者」。**

### 順帶:LibriTTS(https://www.openslr.org/60/)
同源、**CC BY 4.0**、**24 kHz**(比 LibriSpeech 高)、約 585 小時、在句界切分、
附原始文本與正規化文本。**但一樣沒有官方 phone 對齊**,而且通道異質性的問題完全相同。
⚠️ **我的判斷:若真要走 LibriVox 路線,LibriTTS 因為 24 kHz 與較乾淨的切分而優於
LibriSpeech;但這不改變上面的通道結論。**

## 可連結脈絡
- 跨語料庫對照與最終建議 —— [[natural-speech-sources]]
- 為什麼通道噪音會汙染 SNR 維度 —— [[snr_audio]]、[[silbert2012]]
- 錄音品質最好的替代 —— [[vctk]]
- phone 標註最完整的替代 —— [[buckeye-corpus]]
- 用大語料庫做 VOT 統計的前例 —— [[chodroff2017]]、[[chodroff2019]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**LibriSpeech 有官方音素標註嗎?** → **沒有**。要靠第三方:Lugosch 的 Zenodo 2619474
(MFA 對齊,CC BY 4.0,自述含 phoneme + word alignment,涵蓋全部 980 小時)。
**LibriSpeech 的授權?** → CC BY 4.0,16 kHz。是候選裡授權最寬鬆的一批。
**LibriSpeech 為什麼不適合當 SNR 實驗的刺激?** → 來源是志願者在家錄的 LibriVox 有聲書,
錄音通道異質。**你要操弄的維度就是 SNR,刺激自帶的未知噪音會直接汙染它。**
**英語裡開頭是 /bi/、/pi/ 的詞各有幾個?** → CMUdict 查:`B IY1` 開頭 287 個、
`P IY1` 開頭 244 個(含大量人名/地名)。真正常用的單音節詞:be, bee, beach, bead, beak,
beam, bean, beat, beef, beep, beet / pea, peace, peach, peak, peal, peas, peat, peek,
peel, peep, Pete, piece, pique。
