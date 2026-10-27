---
tags: [literature-note, 軟顎音, 顎化, 協同構音, burst頻譜, 超音波]
citekey: frisch2016
---

# Frisch & Wodzinski (2016) — 軟顎音在 /i/ 前明顯前移,而且 burst 頻譜跟著跑

**DOI / URL** https://doi.org/10.1016/j.wocn.2016.01.001 | PMC4805126 https://pmc.ncbi.nlm.nih.gov/articles/PMC4805126/
**閱讀狀態** **全文已讀**(引句經原始 XML 逐字核對)。⚠️ 其中關於 Keating & Lahiri (1993) 的數字是**本篇的轉述**,該篇原文我未取得。

```bibtex
@article{frisch2016velar,
  author  = {Frisch, Stefan A. and Wodzinski, Sylvia M.},
  title   = {Velar-vowel coarticulation in a virtual target model of stop production},
  journal = {Journal of Phonetics},
  volume  = {56}, pages = {52--65}, year = {2016},
  doi     = {10.1016/j.wocn.2016.01.001}
}
```

## 研究問題
英語的軟顎塞音在前母音前會前移(velar fronting)。這個協同構音的量級有多大?軟顎音是不是根本沒有固有的舌體目標,完全由母音決定?

## 方法與族群
**超音波舌體影像**,十名英語母語者,單音節詞的 /k/ 起始(無尾音或唇音尾)。

## 結果與限制
**前移是真實且大的(原文)**:
> "For all participants, the front vowel context is more forward than the other contexts,
> however, for P1, P2, P5, P6, and P10, there appears to be **a visible discontinuity
> between closure location for the front vowel contexts and the non-front vowel contexts.**"

> "the difference in closure location on the palate between onsets in the words k[ey] and
> c[ough] ... is **large enough to be noticed by naïve speakers despite being allophonic**"

**⚠️ 對 AVWM 最關鍵的一段(本篇轉述 Keating & Lahiri 1993,二手)**:
> "Keating and Lahiri (1993) ... from acoustic data taken from the velar burst conclude
> that **the prominent frequency peak in the burst spectrum is distinct for all five
> contexts and varies systematically with vowel frontness.** ... A closer examination of
> the frequency peaks shows a rather large difference between **front vowel contexts
> (about 3,000 Hz) and back vowel contexts (1,000–1,500 Hz).**"

**→ 軟顎音的 burst 頻譜峰值在前母音與後母音之間差了兩倍以上。**

本篇也轉述 Keating & Lahiri 的理論結論:**舌體前後對軟顎音可能是未指定的(unspecified),由協同構音決定** —— 這正是「固定 burst 的合成器對軟顎音必然失真」的原因。

## 對 AVWM 的意義
**這是排除軟顎音最有力的一條技術理由。**

若用參數合成器(如 KlattGrid)給整條連續體一個固定的 burst 頻譜:
- 對**唇音**:站得住。[[fox2020]] 的已發表實作就是 "The onset noise-burst was 2 ms in duration and **had constant spectral properties across all stimuli**",而且是 /ba/–/pa/。
- 對**軟顎音**:依上述 3000 Hz vs 1000–1500 Hz 的差距,一個固定 burst 不可能同時對前後母音脈絡都正確。

⚠️ **但必須標明:沒有任何文獻直接說「軟顎音難合成」。**這是我從 burst 頻譜資料推出的推論。我特地檢索過 Klatt / Praat / KlattGrid 脈絡下的相關陳述,**查無**。

**知覺層次的延伸(⚠️ 僅讀摘要)** —— Guion, S. G. (1998), *Phonetica* **55**(1–2), 18–52, doi 10.1159/000028423:
> "It is shown that **velars before front vowels are both acoustically and perceptually
> similar to palatoalveolars.**"

對一個需要子音身分毫不含糊的 GRT 設計,軟顎音 + /i/ 在知覺上靠近 /tʃ/ 是實質風險。(此推論為我所加。)

**限制**:
- 十人,單一語言,只做 /k/(未做 /g/)。
- Keating & Lahiri (1993) *Phonetica* **50**, 73–101, doi 10.1159/000261928 —— **書目經 Crossref 核實,全文未讀**,上述數字全部是本篇的轉述。
- 本篇的主題是構音模型(virtual target model),不是刺激設計;把它用於合成可行性的判斷是我的外推。

## 可連結脈絡
- 發音部位的選擇 —— [[consonant-pair-choice]]
- 軟顎音 burst 的另一個結構問題 —— [[kingston1983]]
- 唇音用固定 burst 的已發表實作 —— [[fox2020]]
- burst 頻譜作為 voicing 線索,軟顎音例外 —— [[chodroff2014]]
- /i/ 母音的方法學建議(與本卡構成張力)—— [[winn2020]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**為什麼固定 burst 的合成器不適合軟顎音?** → 本卡:burst 頻譜峰值在前/後母音間差兩倍以上。
**「用 /i/ 避開 F1 混淆」與「避開軟顎音顎化」哪裡衝突?** → 本卡 + [[winn2020]]。⚠️ 沒有人寫過這個衝突;選唇音可完全繞開。
