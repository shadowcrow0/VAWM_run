---
tags: [literature-note, VOT, burst, trading-relation, 引用查核, 綜合卡]
citekey: burst-vot-tradeoff
---

# 「換 burst ≈ 3 ms VOT」的出處追查(綜合查核卡)

**DOI / URL** Keating 1979 掃描本 https://linguistics.ucla.edu/people/keating/keating.htm | Nittrouer 1999 https://doi.org/10.1044/jslhr.4204.925 | Chodroff & Wilson 2014 https://doi.org/10.1121/1.4896470
**閱讀狀態** **三份原始文獻的相關章節皆已讀**(由 subagent 取得:Keating 1979 為 UCLA 自存掃描本,無 OCR,以視覺閱讀 pp. 72–73、124、131、145;Nittrouer 1999 與 C&W 2014 為已出版 PDF 全文)。

```bibtex
@phdthesis{keating1979polish,
  author = {Keating, Patricia A.},
  title  = {A phonetic study of a voicing contrast in {Polish}},
  school = {Brown University}, address = {Providence, RI}, year = {1979}
}
@article{nittrouer1999temporal,
  author  = {Nittrouer, Susan},
  title   = {Do temporal processing deficits cause phonological processing problems?},
  journal = {Journal of Speech, Language, and Hearing Research},
  volume  = {42}, number = {4}, pages = {925--942}, year = {1999},
  doi     = {10.1044/jslhr.4204.925}
}
```
(Chodroff & Wilson 2014 的 BibTeX 見 [[chodroff2014]]。)

## 研究問題
[[abramson2017]] 卡上記了一條:「換 burst 約值 **3 ms VOT**(Keating 1979)」。這個數字的原始出處到底是什麼?它適用於什麼條件?**這是一次出處追查,不是內容摘要。**

## 方法與族群
追查三層引用鏈:[[winn2020]] → Keating (1979) + Nittrouer (1999),以及把兩者串起來的 [[chodroff2014]]。

## 結果與限制

**第一層 —— Winn (2020) §II.F, p. 857 原文**:
> "**Keating (1979) and Nittrouer (1999) found that substituting a voiceless consonant
> burst at the start of the aspiration in a VOT continuum between /d/ and /t/ was
> perceptually equivalent to adding 3 ms VOT.**"

只引這兩篇。Chodroff & Wilson (2014) 是下一句才出現,用來講複雜化,**不是 3 ms 這個數字的出處**。

**第二層 —— Keating (1979) 是博士論文,不是期刊論文**。3 ms 出現在第三章 §3.4.1, p. 145(原文):
> "With the [d]-burst, listeners needed a greater voice onset time to shift their
> responses to the [t] category: 18 msec VOT with the [d]-burst vs. 15 msec VOT with the
> [t]-burst. **In this sense, whatever cues to voicedness are present in the [d]-burst,
> they are 'worth' about 3 msec of aspirated VOT lag.** That is, there is a trading
> relation that holds here between burst-cues and VOT: one offsets the other."

p. 131 的統計版本:平均邊界 [t]-burst 16.6 ms vs [d]-burst 19.9 ms,差 3.3 ms,t₂₀ = −5.21, p < .001,21 名受試者。

⚠️ **三個 Winn 沒有標明的條件**:
1. **這是波蘭語**(波蘭語受試者、波蘭語詞 tur/dur、tama/dama)。波蘭語是 true-voicing 語言,邊界落在 ~16–20 ms,遠低於英語 /d/–/t/ 的 ~35 ms(Winn 自己 p. 855 的數字)。**把 3 ms 搬到英語刺激上是未經檢驗的外推。**
2. 只做了 **/d/–/t/**(舌尖音),沒有其他發音部位。
3. Keating 取的是 burst 的前 **7 ms**;Nittrouer 取 **10 ms**。

**第三層 —— Nittrouer (1999) 自己從來沒有講過 3 ms**。全文檢索無此陳述。她的方法(p. 933 原文):
> "**Ten milliseconds of burst noise was excised from natural tokens of a male speaker
> saying /dɑ/ and /tɑ/, and added to the front of each vocalic portion.** As would be
> expected given their common place of closure, **the spectra of these noises did not
> differ greatly: the /t/ noise simply had a bit more high-frequency energy than the /d/
> noise.**"

3 ms 這個數字是**從她的 Table 4 推導出來的**:邊界分離量 NPP 組 2.5 ms、PPP 組 3.0 ms。**做這個推導、並把兩篇串起來的是 Chodroff & Wilson (2014) p. 2763**(原文):
> "Nittrouer (1999) obtained similar results by splicing the initial 10 ms of natural /t/
> and /d/ bursts onto the beginning of a nine-step VOT continuum. … **as in Keating
> (1979), the /t/ burst was perceptually equivalent to approximately 3 ms of additional
> VOT.**"

⚠️ **Nittrouer (1999) 全文完全沒有引用 Keating** —— 兩者是獨立發現,不是引用鏈。這一點反而**加強**了 3 ms 這個數字的可信度(兩次獨立測量收斂)。

⚠️ 但 Nittrouer 的條件也需標明:受試者是 **8–10 歲兒童**,母音段是**合成的**(自然 burst 接到合成母音上)。**它不是自然語音的複製。**

## 對 AVWM 的意義
**3 ms 是個小數字,但要看跟什麼比。**

- 若走**合成路線**:burst 是我自己設定的,整條連續體共用同一個 burst,**這個 trading relation 根本不會出現** —— 這是合成路線的真實優勢。
- 若走**自然 cross-splicing 路線**:[[winn2020]] 的 progressive cutback 做法本來就是把無聲 token 的 burst + 送氣接上去,所以 burst 在整條連續體上是**一致的**(都來自無聲端),同樣不產生 3 ms 的漂移。**因此這個顧慮對兩條路線其實都不構成阻礙。**
- **真正有用的是它的量級參考**:3 ms 大約是 [[winn2020]] 所說英語 /b/–/p/ 邊界(~20–25 ms)的 12–15%。一個被忽略的次要線索,量級就有這麼大。這是 AVWM 在寫「單一線索操弄」時該記住的尺度感。

**限制**:Keating 是波蘭語、Nittrouer 是兒童 + 部分合成刺激。**沒有任何一筆是成人英語自然語音的 /b/–/p/ 資料。** 引用 3 ms 時必須標明這一點。

## 可連結脈絡
- 引用這兩篇的方法學教學 —— [[winn2020]]
- 做推導並發現軟顎音例外的那篇 —— [[chodroff2014]]
- 次要線索清單(本卡修正了其中一列的出處)—— [[abramson2017]]
- 發音部位的選擇 —— [[consonant-pair-choice]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**我追查過哪些「大家都在引的數字」的原始出處?** → 本卡(3 ms burst trading relation)。
**哪些常被引的語音數字其實來自非英語資料?** → 本卡(Keating 1979 是波蘭語)。
**哪些數字是二手文獻代為推導、原作者自己沒講過的?** → 本卡(Nittrouer 的 3 ms 由 Chodroff & Wilson 推導)。
