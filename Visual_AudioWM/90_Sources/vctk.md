---
tags: [literature-note, 語音語料庫, 刺激來源, 錄音品質, AVWM]
citekey: vctk
---

# CSTR VCTK Corpus — 錄音品質最好(半消音室 / 48 kHz),但完全沒有時間對齊

**DOI / URL**
- **0.92(現行版)** https://datashare.ed.ac.uk/handle/10283/3443 — doi:10.7488/ds/2645
- 0.92 README(逐字讀過) https://datashare.ed.ac.uk/bitstream/handle/10283/3443/README.txt
- **0.80(已被取代)** https://datashare.ed.ac.uk/handle/10283/2651
- HuggingFace 鏡像 https://huggingface.co/datasets/CSTR-Edinburgh/vctk
- 文本選取法論文 doi:10.1109/ICSDA.2013.6709856

**查證狀態** 2026-08-12 **實際打開** DataShare 3443 與 2651 兩個 item 頁、HF dataset card,
並**用 curl 抓下 0.92 的 README.txt 全文逐字讀過**(5,236 bytes)。
0.92 的授權敘述是 README 原文。**0.80 的授權我沒有讀到全文**,只在 2651 頁面的
「Licences」區塊看到掛的檔名是 `LICENCE_ODC_BY.txt`(見下)。**沒有下載語料本體**(10.94 GB)。
標「⚠️ 我的推論」處是我的判斷。

```bibtex
@misc{yamagishi2019vctk,
  author       = {Yamagishi, Junichi and Veaux, Christophe and MacDonald, Kirsten},
  title        = {{CSTR VCTK} Corpus: English Multi-speaker Corpus for {CSTR}
                  Voice Cloning Toolkit (version 0.92)},
  year         = {2019},
  publisher    = {University of Edinburgh. The Centre for Speech Technology
                  Research (CSTR)},
  doi          = {10.7488/ds/2645},
  howpublished = {[sound]}
}
```
(此為 DataShare item 頁上的官方 citation 欄位。README 另給一個較短的
「Veaux, Yamagishi, MacDonald」版本 —— **兩者作者順序不同**,論文引用時建議用 DataShare 版。)

## 研究問題
建一個多語者、多口音、錄音條件完全一致的英語語料,原本目標是 HMM/DNN-based TTS 與
speaker adaptation。**「所有語者用同一套錄音設定」是它的設計核心**,這正好是 AVWM 需要的。

## 方法與族群
README 原文:
> "This CSTR VCTK Corpus includes speech data uttered by **110 English speakers** with
> various accents. Each speaker reads out about **400 sentences**, which were selected from
> a newspaper, the rainbow passage and an elicitation paragraph used for the speech accent
> archive."

> "All speech data was recorded using an **identical recording setup**: an omni-directional
> microphone (**DPA 4035**) and a small diaphragm condenser microphone with very wide
> bandwidth (**Sennheiser MKH 800**), **96kHz sampling frequency at 24 bits** and in a
> **hemi-anechoic chamber** of the University of Edinburgh. (However, two speakers, p280 and
> p315 had technical issues of the audio recordings using MKH 800). All recordings were
> converted into 16 bits, were **downsampled to 48 kHz**, and were **manually end-pointed**."

**→ 這是所有候選裡唯一在半消音室、用專業麥克風、統一設定錄的。**

**文本組成**(這一段對 AVWM 很重要):
1. **Herald Glasgow 報紙句** —— 每個語者拿到**不同**的一組(greedy 演算法選的,為了音境覆蓋)
2. **Rainbow Passage** —— **所有語者相同**
3. **Speech Accent Archive 的 elicitation paragraph** —— **所有語者相同**

### 授權:0.80 與 0.92 **確實不同**
- **0.92 = CC BY 4.0**。README 的 COPYING 段逐字:
  > "This corpus is licensed under the Creative Commons License: Attribution 4.0
  > International http://creativecommons.org/licenses/by/4.0/legalcode"
- **0.80 = ODC-By(Open Data Commons Attribution License)**。DataShare 2651 頁的
  「Licences」區塊掛的檔案是 **`LICENCE_ODC_BY.txt`**(連結標籤寫 "Depositor Agreement")。
  ⚠️ **我沒有讀到該檔全文**,只確認了檔名。**若要在論文寫 0.80 的授權,請先開那個檔。**
- 0.80 有 **109** 位語者、0.92 有 **110** 位;0.80 頁面明文
  「This item has been replaced by the one which can be found at
  https://doi.org/10.7488/ds/2645」。
- ⚠️ **我的建議**:直接用 0.92。CC BY 4.0 比 ODC-By 在「音檔」這種非資料庫的客體上
  法律關係更清楚,而且是現行版。

### **沒有音素標註,也沒有詞層對齊**
0.92 的下載內容只有 `wav48_silence_trimmed/`(音檔)與 `txt/`(整句文字)。
HF dataset card 列出的欄位是 speaker_id / audio / file / text / text_id / age / gender /
accent / region / comment —— **沒有任何時間對齊資訊,沒有 .lab、沒有 TextGrid**。
→ **要用就必須自己跑 forced aligner(MFA)。**

## 結果與限制

### ⚠️ 我的推論:能不能切出乾淨的 /bi/、/pi/?—— **錄音品質最佳,但 /bi/ 是個大洞**

**(1) 兩段共同文本裡的 /pi/ 是一個現成的、跨 110 語者的受控樣本。**
我 2026-08-12 查到兩段共同文本的全文:
- Rainbow Passage:「...There is, according to legend, a boiling pot of gold at one end.
  **People** look, but no one ever finds it.」以及「Throughout the centuries **people** have
  explained the rainbow in various ways.」→ **2 個重音 /pi/**
- Elicitation paragraph:「Six spoons of fresh snow **peas**, five thick slabs of blue
  cheese...」→ **1 個重音 /pi/**("peas" = `P IY1 Z`)

→ **每位語者至少 3 個重音 /pi/,而且句法位置與前後音境對 110 個語者完全相同。**
這在跨語者比較上是極罕見的控制條件。

**(2) 但共同文本裡幾乎沒有可用的 /bi/。**
"beautiful"(rainbow passage)是 `B Y UW1`(/bju/),**不是 /bi/**;
elicitation paragraph 裡的 "Bob"、"bring"、"blue"、"bags" 全部不是 /bi/。
→ ⚠️ **這是致命的不對稱:VCTK 的共同文本給你 /pi/ 卻不給你 /bi/。**
要湊 /bi/ 就得回去翻**每個語者不同的**報紙句 —— 一旦這麼做,受控的共同文本優勢就沒了,
而且必須先跑對齊才知道哪些句子有。

**(3) 工作量估計(我的推估)**:
下載 10.94 GB → 安裝 MFA(⚠️ **注意:絕不要裝進系統或使用者 site-packages,用 conda env
或 venv**)→ 對 110 語者跑 forced alignment(GPU 不需要,CPU 數小時)→ 從 TextGrid 篩
`B IY1` / `P IY1` → 切檔 + 人耳挑選。
**合計約 3–5 天。** 比 LibriSpeech 省(語料乾淨、不用挑語者),比 CMU ARCTIC 貴(要自己對齊)。
**但最後你會發現 /pi/ 很好拿、/bi/ 得靠運氣。**

**(4) 一個 VCTK 特別適合的替代用法**:
⚠️ **我的推論** —— 如果 AVWM 最後決定**自己錄**(這在 GRT 語音實驗裡是常態,見
[[silbert2012]]:作者自己發音),VCTK 的價值不是當刺激來源,而是當**錄音規格的參照**:
半消音室、DPA 4035 全指向 + Sennheiser MKH 800、96 kHz/24-bit 錄、降到 48 kHz/16-bit、
手動 end-point。這是一份可以直接照抄的方法段。

## 可連結脈絡
- 跨語料庫對照與最終建議 —— [[natural-speech-sources]]
- 自己錄 vs 找現成的 —— [[silbert2012]](作者自錄)、[[natural-vs-synthetic-speech]]
- 需要自己跑對齊時的工具 —— [[librispeech]](Lugosch 的 MFA 對齊可當 pipeline 範例)
- 錄音通道對 SNR 操弄的影響 —— [[snr_audio]]
- 有 phone 對齊但錄音較差的替代 —— [[cmu-arctic]]、[[buckeye-corpus]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**VCTK 0.80 跟 0.92 的授權真的不同嗎?** → **是**。0.92 的 README 明寫 CC BY 4.0;
0.80 在 DataShare 掛的授權檔是 `LICENCE_ODC_BY.txt`(ODC-By)。⚠️ 0.80 全文我沒讀。
**哪個公開語料庫的錄音條件最接近實驗室標準?** → VCTK:半消音室、DPA 4035 + MKH 800、
96 kHz/24-bit 原始、48 kHz/16-bit 發布、手動 end-point、**110 位語者用完全相同的設定**。
**VCTK 有音素標註嗎?** → **完全沒有**。只有整句文字。必須自己跑 MFA。
**有沒有哪一句話是所有 110 位 VCTK 語者都唸過的?** → 有兩段:Rainbow Passage 與
Speech Accent Archive 的 "Please call Stella" 段。裡面共有 **3 個重音 /pi/**
(people×2, peas×1),**但 0 個可用的 /bi/**。
**我要自己錄語音刺激時,錄音規格照誰?** → VCTK 的方法段可以直接抄。
