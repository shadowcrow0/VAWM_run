---
tags: [literature-note, 訊號偵測論, 階層貝氏, item隨機效果, 聚合偏誤, 統計方法]
citekey: rouder2007
---

# Rouder et al. (2007) — ⭐ 「把 item 併掉會低估敏感度,而且加試次救不了」

**DOI / URL** https://doi.org/10.1007/s11336-005-1350-6
**閱讀狀態** ⚠️ **僅讀摘要**(由 Crossref 取得出版社存放的完整摘要,逐字)。
全文未取得。**本卡的核心主張全部出自摘要,那幾句話本身很明確,但支持它的推導我未讀。**

```bibtex
@article{rouder2007signal,
  author  = {Rouder, Jeffrey N. and Lu, Jun and Sun, Dongchu and Speckman, Paul and
             Morey, Richard and Naveh-Benjamin, Moshe},
  title   = {Signal detection models with random participant and item effects},
  journal = {Psychometrika},
  volume  = {72}, number = {4}, pages = {621--642}, year = {2007},
  doi     = {10.1007/s11336-005-1350-6}
}
```

## 研究問題
訊號偵測模型的參數是在**聚合過的資料**上估的(把 item 併掉、或把受試者併掉、或兩者)。
訊號偵測模型是**非線性**的。這樣做會有什麼後果?

## 方法與族群
理論 + 兩個階層貝氏模型(同時容納受試者與 item 兩個隨機效果)。應用領域是再認記憶。

## 結果與限制

**摘要原文(逐字,Crossref 存放版)**:
> "The theory of signal detection is convenient for measuring mnemonic ability in recognition
> memory paradigms. In these paradigms, randomly selected participants are asked to study
> randomly selected items. **In practice, researchers aggregate data across items or
> participants or both. The signal detection model is nonlinear; consequently, analysis with
> aggregated data is not consistent. In fact, mnemonic ability is underestimated, even in the
> large-sample limit.** We present two hierarchical Bayesian models that **simultaneously
> account for participant and item variability.**"

### ⭐ 這三句話對 AVWM 的意義

**逐項拆開(以下是我對摘要的解讀,不是新主張)**:

1. **"analysis with aggregated data is not consistent"** —— 併掉 item 之後的估計量
   **不一致**(統計學意義:樣本數趨近無窮也不收斂到真值)。
2. **"even in the large-sample limit"** —— **加試次救不了。**
   這一點對 AVWM 特別重要:專案目前每刺激 96 次、Silbert 用 200 次
   ([[silbert2012]]),討論試次預算時很自然會以為「多跑一點就準了」。
   **這種偏誤不是那一類。**
3. **"underestimated"** —— **方向確定:敏感度被低估。**
   在 GRT/SDT 的等價語言裡,敏感度低估 = **有效知覺變異被高估**。
   **這正是研究者提出的那個顧慮,而且是已發表的形式結果。**
4. **解方是把 item 當隨機效果。** —— 而 GRT 文獻裡**沒有任何一個模型**這樣做
   (見 [[silbert2012]]:階層只有受試者那一層,token 明文併掉)。

**⚠️ 但必須誠實標明適用範圍**:
- 這是**再認記憶**的 SDT,不是 GRT,不是 2×2 辨識。
- 我**只讀摘要**,沒讀推導,不知道偏誤大小如何隨 item 變異量縮放。
- **把這個結果搬到 GRT 是我的外推。** subagent 對五份 GRT 來源做過全文關鍵詞檢索
  (GRT-wIND、grtools 教學、GRT-wIND 可辨識性論文、Silbert & Hawkins 教學、
  Ashby & Wenger 手冊章節):`stimulus variability` **五份全部 0 命中**、
  `token` **五份全部 0 命中**。**這個搬運在文獻上沒有人做過。**

**姊妹作**(⚠️ 書目經核實,內容未讀):
Rouder, J. N., & Lu, J. (2005). "An introduction to Bayesian hierarchical models with an
application in the theory of signal detection." *Psychonomic Bulletin & Review*, 12(4),
573–604. doi 10.3758/BF03196750

## 可連結脈絡
- 本卡所屬的敘事回顧 —— [[token-variability-vs-perceptual-variance]]
- 理論推論文章 —— [[自然音vs合成音_理論推論]]
- 把 token 明文併掉、階層只有受試者層的 GRT —— [[silbert2012]]
- GRT 明說不分解知覺變異來源 —— [[silbert-hawkins2016]]
- GRT 已承認兩種雜訊不可分離,只有和可估 —— [[ashby-wenger-handbook]]
- Ashby 自己把 stimulus noise 與 perceptual noise 並列 —— [[ashby2000]]
- token 數的實證效果 —— [[uchanski1998]]、[[kapadia2023]]
- 專案內結構相同的污染論證(intrusion)—— [[決策脈絡_統計方法]] §3

---
標籤note:[[literature-note]] [[GRT]] [[AVWM]]

## 回查線索
**有沒有形式結果說「把 item 併掉會偏誤 SDT 參數」?** → 有,本篇。方向是**低估敏感度**,
而且**不一致**(加樣本救不了)。
**解方是什麼?** → item 隨機效果。**GRT 文獻裡沒有人做過。**
**我在哪看過「加試次救不了的偏誤」?** → 本篇;以及 [[決策脈絡_統計方法]] §3 的 intrusion
(那個是模型誤設,同樣不是取樣誤差)。
