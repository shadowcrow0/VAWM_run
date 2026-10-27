---
tags: [literature-note, VOT, 語料庫, 語者變異, Mixer6, 產出數值]
citekey: chodroff2015
---

# Chodroff et al. (2015) — Mixer 6 語料庫的 VOT 母體數值(129 位語者、68,456 token)

**URL** https://www.internationalphoneticassociation.org/icphs-proceedings/ICPhS2015/Papers/ICPHS0632.pdf
**無 DOI**(ICPhS 會議論文集)。
**閱讀狀態** **Table 1 與 Fig. 1 的軸刻度已由 subagent 親自核對**;全文未通讀。

```bibtex
@inproceedings{chodroff2015structured,
  author    = {Chodroff, Eleanor and Godfrey, John and Khudanpur, Sanjeev and
               Wilson, Colin},
  title     = {Structured variability in acoustic realization: A corpus study of
               voice onset time in {American English} stops},
  booktitle = {Proceedings of the 18th International Congress of Phonetic Sciences},
  address   = {Glasgow}, year = {2015}
}
```

## 研究問題
大規模電話語音語料庫(Mixer 6)裡,英語塞音 VOT 的實現有沒有跨語者的結構?

## 方法與族群
**129 位語者、68,456 個 token。**連續(電話)語音。

## 結果與限制

**Table 1(母體平均 / SD,ms;⚠️ 這是**語者內 + 語者間合併**的 SD,不是分解過的)**:

| | P | T | K | B | D | G |
|---|---|---|---|---|---|---|
| 平均 | 50.8 | 60.5 | 54.4 | 8.7 | 13.8 | 17.2 |
| SD | 21.1 | 21.8 | 20.2 | 5.0 | 8.7 | 10.6 |

**平均與 SD 的相關(原文)**:
> "/p/: r = 0.55; /t/: r = 0.48; /k/: r = 0.47; /b/: r = 0.74; /d/: r = 0.63;
> /g/: r = 0.42; **all categories collapsed: r = 0.93.**"

**Fig. 1** 畫的是 talker 平均 VOT(x)對 **talker 的 VOT sd**(y)。
subagent 核對的 y 軸刻度:P/T/K 為 **15/20/25**;B/D/G 為 **2.5/5.0/7.5/10.0/12.5**。
**→ 這張圖就是 [[kleinschmidt2019]] 目視估出「/p/ 的平均語者內 SD 約 20 ms」的來源。**

### 對 AVWM 的用途

1. **這是「/p/ 的語者內 VOT SD ≈ 20 ms」這個數字的原始出處**(經由 Fig. 1)。
2. ⚠️ **Table 1 的 SD 不能當語者內 SD 用** —— 它是母體 SD(合併兩種變異)。
   要語者內的數字請用 [[chodroff2017]] 的 "Range of Talker SDs" 欄
   或 [[chodroff-bradshaw-livesay2023]] 的 mean talker SD。

**限制**:
- **電話語音、連續語音**,不是孤立 CV 音節。AVWM 是後者。
- 會議論文,篇幅短,方法細節有限。
- 我未通讀;只有 Table 1 與 Fig. 1 軸刻度經核對。

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- 讀本篇 Fig. 1 得出「語者內約為語者間兩倍」的論文 —— [[kleinschmidt2019]]
- 同作者的孤立語 + 連續語數值(有語者內欄)—— [[chodroff2017]]
- 唯一報告平均語者內 SD 的來源 —— [[chodroff-bradshaw-livesay2023]]
- 聽者內在雜訊的對照基準 —— [[clayards2008]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**「/p/ 語者內 SD ≈ 20 ms」出自哪裡?** → 本篇 Fig. 1,經 [[kleinschmidt2019]] 目視估讀。
**Table 1 的 SD 是語者內還是語者間?** → **都不是,是合併的母體 SD。** 不要誤用。
