---
tags: [literature-note, 統計檢力, 刺激當隨機效果, 交叉隨機因子, 實驗設計]
citekey: westfall2014
---

# Westfall, Kenny & Judd (2014) — 刺激太少時,**檢力有天花板**,加受試者也上不去

**DOI / URL** https://doi.org/10.1037/xge0000014 | PMID 25111580
**閱讀狀態** **全文 PDF 已由 subagent 取得並閱讀**(經 Wayback Machine 取回作者自存版);
頁碼引自該 PDF。⚠️ 我本人未通讀。

```bibtex
@article{westfall2014statistical,
  author  = {Westfall, Jacob and Kenny, David A. and Judd, Charles M.},
  title   = {Statistical power and optimal design in experiments in which samples of
             participants respond to samples of stimuli},
  journal = {Journal of Experimental Psychology: General},
  volume  = {143}, number = {5}, pages = {2020--2045}, year = {2014},
  doi     = {10.1037/xge0000014}
}
```

## 研究問題
當受試者與刺激**都是**隨機因子時,檢力怎麼算?最佳的設計是什麼?

## 結果與限制

### ⭐⭐ 核心結果:檢力有天花板(摘要原文)
> "**statistical power typically does not approach unity as the number of participants goes to
> infinity but instead approaches a maximum attainable power value that is possibly small,
> depending on the stimulus sample.**"

### 具體數字(p. 2026,完全交叉設計)
> "maximum achievable power with a **medium effect size** when using **eight stimuli**—a fairly
> typical value of q in many experimental studies—**is only approximately .50, even with an
> infinite number of participants.** … if one anticipates a medium effect size and one would
> like power to roughly equal .80, then **the minimum number of stimuli that can be used, even
> with a very large number of participants, is about 16.**"

### 更嚴重的情形(p. 2032,stimuli-within-condition 設計)
> "where the true effect size is **large at d = 0.8**, and where there are a total of **eight
> stimuli (four stimuli per condition)** … **the maximum attainable power is only about .41.**
> However, if we just double the sample size of stimuli to a still relatively modest 16 (eight
> per condition), then the maximum power to detect a large effect goes up to about .78."

> "Experimenters may believe that they can compensate for a suboptimal sample of stimuli by
> simply recruiting a larger number of participants, but in fact **the degree to which this
> sort of compensation can take place is quite limited.**"

> "**a direct replication with high statistical power is often theoretically impossible when
> the original study employed a relatively small number of stimuli.**"

### ⚠️⚠️ 這對 AVWM 是最尖銳的一條反面證據

**「每個類別 4 個 token」正是他們算出「大效果檢力只有 .41」的那個設定。**
⚠️ Silbert (2012) 用的正是每類 4 個([[silbert2012]]);
AVWM 若走多 token 路線,大概也會落在這個量級。

**但它同時也是對「單一 token」最尖銳的反面** —— q = 1 比 q = 4 更極端。

**→ 這篇的訊息不是「用少一點刺激」,而是「**若把刺激當隨機因子**,少刺激的設計檢力極差」。
它與 [[judd2012]] 一起構成一個明確的主張:**應該用很多刺激(≥16)並用混合模型。****

**⚠️ 這與 [[自然音vs合成音_理論推論]] 的結論方向相反,必須並陳。**
調和的關鍵在於**推論目標**:他們算的是「對**刺激母體**做推論」的檢力。
若研究問題被明確限縮成「在這個指定的刺激上」([[clark1973]] 的
"method of single cases" 判準),**刺激就不是隨機因子,這個檢力天花板不適用。**
**但那個限縮必須寫進論文的主張,不能只在心裡想。**(這個調和是我的推論。)

### 設計原則
- p. 2033:"it is generally better to **increase the sample size of whichever random factor is
  contributing more random variation to the data**"
- p. 2034:"if one of the two sample sizes is considerably smaller than the other, there is
  generally a greater power benefit in increasing the smaller sample size"

**限制**:
- 假設的變異成分(VPC)是「標準情形」,不是從語音資料估的。
- 我未通讀。
- 它算的是**對刺激母體推論**的檢力,見上。

## 可連結脈絡
- 本卡所屬的推論文章 —— [[自然音vs合成音_理論推論]] §5、§8
- 證據回顧 —— [[token-variability-vs-perceptual-variance]] §7.1
- 同一群作者的前作 —— [[judd2012]]
- 原始論證 —— [[clark1973]](他 p. 349 已預告了「設計的敏感度取決於較弱的那一半」)
- 更早的心理物理版 —— [[brunswik1955]]
- **反方**:配對設計不需要 item 分析 —— [[raaijmakers1999]]
- 用每類 4 個 token 的 GRT 前例 —— [[silbert2012]]

---
標籤note:[[literature-note]] [[GRT]] [[AVWM]]

## 回查線索
**刺激太少會怎樣?** → **檢力有天花板,加受試者無效**(本篇)。
8 個刺激 + 中效果 → 上限 .50;4 個/條件 + 大效果 → 上限 .41。
**要幾個刺激?** → 中效果要 .80 檢力需 **≥16 個**。
**這個天花板什麼時候不適用?** → 當刺激**不是**隨機因子時,亦即研究主張被限縮到
指定的刺激上([[clark1973]] 的單一個案判準)。
