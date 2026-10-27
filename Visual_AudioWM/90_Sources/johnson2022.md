---
tags: [literature-note, 視覺工作記憶, 相似度, repulsion, 連續回報, DNF模型, CIELAB, AVWM]
citekey: johnson2022
---

# Johnson, van Lamsweerde, Dineva, & Spencer (2022) — WM 裡度量上相似的顏色在維持期互相推開,且解析度較低

**「探針與目標的度量相似度會改變記憶表徵本身」的直接證據**:相似的顏色
不是被動地難分,而是在主動維持期間**互相排斥**(記成比實際更不同),
同一陣列內的相似色解析度也**低於**同時保持的獨特色。對 AVWM:CL/CH 的
相似度操弄操弄到的不只是決策難度,連記憶表徵的幾何都會動。

**DOI / URL** https://doi.org/10.1038/s41598-022-22328-4 | PMC9588047(CC-BY)
**閱讀狀態** **全文已讀**(2026-08-13 由 subagent 自 nature.com 與 Europe PMC
取回全文與 JATS XML;書目經 Crossref 核對,**完全相符**,文號 17756)。
⚠️ 誠實聲明:Exp 1 各條件 μ 的逐條點估計只在圖 2 與補充材料,主文文字
未列;本卡只用主文可核實的數字。

```bibtex
@article{johnson2022neural,
  author  = {Johnson, Jeffrey S. and van Lamsweerde, Amanda E. and
             Dineva, Evelina and Spencer, John P.},
  title   = {Neural interactions in working memory explain decreased recall
             precision and similarity-based feature repulsion},
  journal = {Scientific Reports},
  volume  = {12}, number = {1}, pages = {17756}, year = {2022},
  doi     = {10.1038/s41598-022-22328-4}
}
```

## 研究問題
WM 中的項目是各自獨立儲存,還是在主動維持期間互相作用?檢驗動態神經場
(DNF)模型的預測:側抑制使度量上相近的表徵在延遲期互相「推開」
(repulsion),並拉低各自的解析度與儲存機率。

## 方法與族群
- Exp 1:12 名大學生;控制實驗:另 12 名。作者自承樣本量依當時實驗室
  慣例決定。
- 刺激:**180 色等距分布於 CIELAB**(中心 L=70, a=28, b=12)——與 AVWM
  同一色彩空間傳統(定圓心、繞圓取色)。
- 相似度操弄(SS3):1 個 Unique 色 + 2 個相似色(彼此相距 20°,一 CW
  一 CCW;距 Unique 170°);SS1 = 單一色。
- 作業:連續回報 recall——樣本 800 ms → **延遲 1000 ms** → 在 180 色環上
  點選;800 試次/人;誤差用 Zhang & Luck 混合模型拆 μ(偏誤)、s.d.
  (解析度)、Pm(儲存機率)。控制實驗把色環提前到樣本期出現(延遲≈0)。

## 結果與限制
- **排斥偏誤**:CW 偏正、CCW 偏負(皆 p<.01);**CW−CCW 排斥量:有延遲
  12.23°,無延遲 1.55°**——差近一個數量級,證明排斥發生在**主動維持期**,
  不是知覺編碼。原文:"metrically similar colors were remembered as being
  more distinct than they really were."
- **解析度**:同一陣列內,相似色 s.d.(CW 21.63°/CCW 20.44°)>
  Unique(18.66°),t(11)=2.47,p=.031,d=0.71;控制實驗中消失。
  作者稱此為新發現:set size 固定下,解析度隨度量相似性變化——違反
  固定解析度的 slot 模型。
- Pm:SS1 > SS3;Unique 的 Pm 反而有低於相似色的(不顯著)趨勢。
- 模型:含序列固化的 DNF 模型 2 較能捕捉全貌(AIC 打平,RMSE 大幅較佳)。
- 限制(作者自述):相似色 s.d. 差(約 2–3°)可能受 swap 誤差污染
  (補充分析認為不足以解釋,但保留 "if real" 措辭);混合模型參數的機制
  對應仍有爭議;每實驗僅 12 人。

**對 AVWM 的含意**:(1) CL(近探針)落在會與目標互斥的相似度範圍內時,
「目標的記憶位置」本身被推移——比較的基準不是靜止的;(2) 延遲長度是
互動量的調節變因,AVWM 的延遲設定要記進方法段;(3) 其 20°/170° 的操弄
印證「相似度要以知覺度量(此處 CIELAB 角距)定義」的做法。

## 可連結脈絡
- 引用處 — [[實驗設計脈絡_平面跟等彩度的問題]] §3
- 記憶中顏色的另一種系統性漂移(更飽和)— [[bloj2016]]
- 顯著性層面的混淆(處理速度)— [[tollner2011]]、[[qian2018]]
- AVWM 的顏色座標同樣是「CIELAB 圓上取角距」— [[決策脈絡_顏色維度]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**「WM 裡相似的顏色會互相排斥」出處?** → 本篇:CW−CCW 排斥 12.23°,移除延遲後縮到 1.55°——效應在維持期。
**「相似度會動到解析度」的證據?** → 本篇:同陣列內相似色 s.d. 比獨特色高 2–3°(d=0.71),set size 固定。
