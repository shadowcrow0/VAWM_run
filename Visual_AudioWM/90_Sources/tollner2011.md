---
tags: [literature-note, 視覺搜尋, 顯著性, PCN-N2pc, ERP, 顏色維度, AVWM]
citekey: tollner2011
---

# Töllner, Zehetleitner, Gramann, & Müller (2011) — 顯著性越高、前注意處理越快:RT 與 PCN 潛時/振幅的平行證據

**「彩度/顯著性對知覺處理並非中性」這條設計理由的電生理證據來源。**
特別值得注意:他們的顏色操弄**正是在等亮度下只動色度**——與 AVWM
固定 L\* 只動色相的設計邏輯同款。

**DOI / URL** https://doi.org/10.1371/journal.pone.0016276 | PLoS ONE 開放取用
**閱讀狀態** **全文已讀**(2026-08-13 由 subagent 自 journals.plos.org 取回完整
HTML,含方法、結果、討論;書目經 Crossref API 逐欄核對,**與引用完全相符**)。

```bibtex
@article{tollner2011saliency,
  author  = {T{\"o}llner, Thomas and Zehetleitner, Michael and
             Gramann, Klaus and M{\"u}ller, Hermann J.},
  title   = {Stimulus saliency modulates pre-attentive processing speed
             in human visual cortex},
  journal = {PLoS ONE},
  volume  = {6}, number = {1}, pages = {e16276}, year = {2011},
  doi     = {10.1371/journal.pone.0016276}
}
```

## 研究問題
顯著性地圖/dimension-weighting 架構的一個具體預測:pop-out 目標與干擾項的
特徵對比越大(越顯著),**前注意的感覺編碼越快、焦點注意越早投入**。
用 PCN(= N2pc,作者改稱 Posterior Contralateral Negativity)的潛時當
前注意處理速度的時間標記,能不能看到 RT 效果的神經對應?

## 方法與族群
- 受試者 13 人(4 女,20–30 歲)。⚠️ 內文寫 13 人,但所有 ANOVA 自由度是
  F(2,22)(即 n=12),排除未說明——論文自身的內部不一致,引用樣本數時留意。
- 刺激:黑背景、34 根彩色橫桿排成三個同心圓;干擾項黃色。
  **顏色目標在等亮度(全部 23 cd/m²)下只動 CIE xy 色度**,三個顯著性等級
  (高 .595/.332、中 .555/.367、低 .540/.388);方向目標傾斜 33.5°/58°/67°。
- 作業:pop-out 視覺搜尋的**左右定位**二選一(顯示 200 ms,1728 試次);
  控制實驗確認三個對比等級的搜尋斜率都 <5 ms/item(皆為 efficient search)。
- 測量:64 導 EEG;PCN = PO7/PO8 對側減同側;峰潛時 + jackknife 起始潛時;
  2(維度)×3(顯著性)重複量數 ANOVA。

## 結果與限制
- **RT**:高/中/低顯著性 = 340/354/372 ms,F(2,22)=104,p<.0001,
  三等級兩兩皆顯著;錯誤率 2.5%/5.4%/7.0% 同向(非速度—準確度交換)。
- **PCN 潛時**:起始 187/203/215 ms、峰 223/240/250 ms(F(2,22)=70.6,
  p<.001,η²=.865),三等級兩兩皆顯著;Saliency×Dimension 交互作用不顯著
  → 效果跨顏色與方向兩維度概化。
- **PCN 振幅**:−2.64/−2.37/−2.08 µV(F(2,22)=7.14,p<.004);⚠️ 事後比較
  **只有高 vs. 低顯著**(p<.002),涉及中間等級的比較不顯著(p>.148)。
  引用時「潛時與振幅皆反映顯著性」成立,但振幅的解析度只到高低兩端。
- 原文(摘要):"For two feature-dimensions (color and orientation), we
  observed decreasing RTs with increasing target saliency. Importantly, this
  pattern was systematically mirrored by the timing, as well as amplitude,
  of the PCN."
- 限制(作者自述):振幅方向與 Hopf et al. 相反,歸因於作業需求不同;
  PCN 的觸發與時程可被 top-down(task/dimensional set)調節,非純 bottom-up。

**對 AVWM 的含意**:探針類型之間若有系統性的顯著性差異(如彩度差),
差的不只是「難度」,連前注意階段的處理速度都被動到——RT 型依變項會被
直接污染。這是 [[實驗設計脈絡_平面跟等彩度的問題]] §3「在設計層面固定
彩度」的主要依據之一。

## 可連結脈絡
- 固定彩度的設計論證 — [[實驗設計脈絡_平面跟等彩度的問題]] §3
- 「等亮度下只動色度」與 AVWM 固定 L\*/C\* 只動色相同構 — [[決策脈絡_顏色維度]]
- 飽和度/明度與 VWM 的行為證據(結論比本篇更有條件)— [[qian2018]]
- 顯著性之外,記憶內的顏色相似度效應 — [[johnson2022]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**「顯著性影響前注意處理速度」的電生理證據哪裡來?** → 本篇:PCN 起始/峰潛時隨目標顯著性單調縮短,跨顏色與方向兩維度。
**有沒有「等亮度下只操弄色度」的已發表前例?** → 本篇方法段:四種顏色全部 23 cd/m²,只動 CIE xy。
