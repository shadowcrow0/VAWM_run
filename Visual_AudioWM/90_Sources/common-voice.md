---
tags: [literature-note, 語音語料庫, 刺激來源, AVWM]
citekey: common-voice
---

# Mozilla Common Voice — CC0 最自由,但眾包 mp3 錄音,對聲學實驗基本不能用

**DOI / URL**
- 舊入口 https://commonvoice.mozilla.org/en/datasets(現已導向 Mozilla Data Collective)
- **現行入口(2025-10 起唯一)** https://mozilladatacollective.com/
  (原網域 https://datacollective.mozillafoundation.org/ 301 導向此處)
- 實際查看的資料集頁 https://mozilladatacollective.com/datasets/cmrt6zbgx000vmm07hfuefigk
  (Common Voice Scripted Speech 26.0 — American English (Male))
- 舊的 HuggingFace 鏡像 https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0
  (**已清空**)
- 論文 https://aclanthology.org/2020.lrec-1.520/

**查證狀態** 2026-08-12 **實際打開** mozilladatacollective.com 的資料集列表與上述單一資料集頁、
HF 的 common_voice_17_0 頁、ACL Anthology 的論文頁。**沒有下載任何資料**(需登入帳號)。
**取樣率我查不到官方明文 —— 下面標「查無」。** 標「⚠️ 我的推論」處是我的判斷。

```bibtex
@inproceedings{ardila2020common,
  author    = {Ardila, Rosana and Branson, Megan and Davis, Kelly and
               Kohler, Michael and Meyer, Josh and Henretty, Michael and
               Morais, Reuben and Saunders, Lindsay and Tyers, Francis and
               Weber, Gregor},
  title     = {Common Voice: A Massively-Multilingual Speech Corpus},
  booktitle = {Proceedings of the Twelfth Language Resources and Evaluation
               Conference (LREC 2020)},
  pages     = {4218--4222},
  address   = {Marseille, France},
  publisher = {European Language Resources Association},
  year      = {2020}
}
```

## 研究問題
用群眾外包建一個**免費、免授權**的多語語音語料,讓 ASR/TTS 不再被商業語料庫綁住。
語言覆蓋是它的核心目標,聲學控制**從來不是**。

## 方法與族群
- **授權:CC0-1.0**(我在資料集頁上看到的 license 欄位就是字串 `CC0-1.0`)。
  → **公眾領域,無任何限制**,是所有候選裡授權最徹底自由的(比 CMU ARCTIC 還自由,
  因為連姓名標示都不要求)。
- **格式:MP3 + TSV**(資料集頁的 "File Formats" 欄位逐字寫 "TSV, MP3")。
- **取樣率:查無官方明文。** 資料集頁與我讀過的所有官方頁面都沒有寫。
  ⚠️ **不要在論文裡憑印象寫 32 kHz 或 48 kHz,用之前實際開一個檔看。**
- 規模範例(Scripted Speech 26.0 - American English (Male)):
  9.68 GB / **390.03 小時** / **295,743 個已驗證片段** / **5,705 位語者**
  (train 5,405 / dev 156 / test 144),發布日 2026-07-20。
- **品質控制 = 社群投票**:每個片段由其他貢獻者聽,**2 個 up-vote 通過、2 個 down-vote 淘汰**。
  ⚠️ **注意這個驗證的判準是「唸的內容跟文字一致嗎」,不是「錄音品質好嗎」。**
- **沒有任何音素標註,也沒有時間對齊。** 只有句層文字。
- 隨附 metadata:年齡、性別、口音(自填,大量缺值)。

### ⚠️ 2025-10 的重大變動:資料搬家了
HuggingFace 上的 `mozilla-foundation/common_voice_*` **已經清空**,頁面明文:
> "Effective October 2025, Mozilla Common Voice datasets are now exclusively available
> through Mozilla Data Collective."

→ 現在**必須註冊 Mozilla Data Collective 帳號才能下載**。
⚠️ **這是一個實務上的坑**:任何 2025 年以前寫的 pipeline(`datasets.load_dataset(
"mozilla-foundation/common_voice_11_0")`)現在都會拿到空資料集。
授權仍是 CC0,但**取得方式從「匿名下載」變成「登入下載」**。

## 結果與限制

### ⚠️ 我的推論:能不能切出乾淨的 /bi/、/pi/?—— **不行,而且理由是硬的**

**(1) MP3 有損壓縮直接殺死你要測的線索。**
AVWM 的聽覺維度是 SNR、對比的是 /b/–/p/,而 /b/–/p/ 的核心線索是
**burst 的頻譜形狀** 與 **VOT 期間的送氣噪音**。這兩者都是**寬頻、低能量、瞬態**的,
正好是 MP3 心理聲學編碼最會丟的東西(它假設這些成分被遮蔽了,所以可以省 bit)。
→ **你在有損編碼過的音檔上疊噪音、再問受試者聽到 /b/ 還是 /p/,等於在測「編碼器留下了
什麼」而不是「聽覺系統如何整合線索」。**
(⚠️ 這一段是我的推論,不是我在文獻上讀到的。但這是 [[burst-vot-tradeoff]] 的直接推論。)

**(2) 錄音通道完全不受控。** 5,705 位語者用自己的筆電/手機/耳麥在任意環境錄音。
底噪、殘響、自動增益、麥克風頻響全部不同,而且**沒有任何 metadata 記錄這些**。
對一個以 SNR 為自變項的實驗,這是 disqualifying 的。

**(3) 沒有對齊,而且不值得去對。** 就算你跑 MFA,前兩點也沒有解決。

**(4) 唯一的優點是授權(CC0)與量。** 但 AVWM 的瓶頸從來不是量或授權,
是 **token 的聲學乾淨度**。

**工作量估計**:註冊帳號 + 下載(~10 GB)+ 自己跑 MFA + 篩 + 人耳挑,**約 1 週**,
**但我的判斷是這一週的產出無法用於 SNR 實驗**,所以工作量不是重點,可行性才是。

### ⚠️ 什麼情況下 Common Voice 會變得有用
如果 AVWM 之後需要**大量、多語者的自然語音當 masker(語音噪音)**而不是當目標刺激,
CC0 + 量大 + 通道雜這三件事就從缺點變成優點。
(對照 [[silbert2012]] 用的是 speech-shaped noise,不是真人語音 masker。)

## 可連結脈絡
- 跨語料庫對照與最終建議 —— [[natural-speech-sources]]
- 為什麼 burst/送氣噪音經不起有損壓縮 —— [[burst-vot-tradeoff]]、[[abramson2017]]
- SNR 作為聽覺維度的設計 —— [[snr_audio]]、[[silbert2012]]、[[winn2013]]
- 授權同樣自由但內容乾淨的替代 —— [[cmu-arctic]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**Common Voice 的授權?** → **CC0-1.0**,公眾領域,連姓名標示都不要求。最自由。
**Common Voice 現在去哪裡下載?** → **2025 年 10 月起只在 Mozilla Data Collective
(mozilladatacollective.com),要註冊帳號。HuggingFace 上的舊 repo 已經清空。**
**Common Voice 的取樣率是多少?** → **查無官方明文**(2026-08-12)。格式是 MP3 + TSV。
用之前自己開檔確認。
**為什麼 MP3 語料不能拿來做 /b/–/p/ 的噪音實驗?** → burst 頻譜與送氣噪音是寬頻、低能量、
瞬態成分,正是心理聲學編碼假設被遮蔽而丟棄的部分。**⚠️ 這是我的推論,不是文獻陳述。**
**Common Voice 的「已驗證」是什麼意思?** → 社群 2 個 up-vote / 2 個 down-vote,
**判準是唸的內容對不對,不是錄音品質好不好。**
