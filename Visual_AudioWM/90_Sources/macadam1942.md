---
tags: [literature-note, 辨色橢圓, 色差, 知覺非均勻性, 正典來源, AVWM]
citekey: macadam1942
---

# MacAdam (1942) — 辨色橢圓的正典來源(⚠️ 未讀原文;嚴格說他量的是配色標準差,不是 JND)

**「色彩空間不均勻」這件事的起點。**核實結果:書目正確(原附註「依領域
慣例填寫」的卷期頁碼 32(5), 247–274 每一欄都查到來源背書,可解除標記);
但常見的「JND 橢圓」說法是後世簡稱——**MacAdam 實際測的是重複配色的
標準差**(matching variability),他正是因為 JND 型判準不夠可重現才改用
SD;後世慣以約 3 倍 SD 當 JND。引用處已於 2026-08-13 照此修正
([[實驗設計脈絡_平面跟等彩度的問題]] §5.2)。

**DOI / URL** https://doi.org/10.1364/JOSA.32.000247 |
作者自述:MacAdam (1982) Citation Classic,
https://garfield.library.upenn.edu/classics1982/A1982PP53900001.pdf
**閱讀狀態** ⚠️ **未讀原文**(Optica 付費牆;唯一公開掃描被擋)。依據:
(1) Crossref 權威書目;(2) **MacAdam 本人 1982 年 Citation Classic 全文**
(已讀,一頁,關於此文最權威的作者自述);(3) [[krauskopf-gegenfurtner1992]]
原文(已讀)對其方法的描述。方法細節均轉引自這些來源,**非 1942 原文逐字**。
頁碼 247–274 的末頁由三個獨立來源確認(K&G 1992 印刷版參考文獻、
MacAdam 1982 自引、Optica 期刊頁首)。

```bibtex
@article{macadam1942visual,
  author  = {MacAdam, David L.},
  title   = {Visual sensitivities to color differences in daylight},
  journal = {Journal of the Optical Society of America},
  volume  = {32}, number = {5}, pages = {247--274}, year = {1942},
  doi     = {10.1364/JOSA.32.000247}
}
```

## 研究問題
CIE 1931 色度圖上的幾何距離不代表知覺色差——同距離在不同位置、不同方向
的可辨性差距可達 20:1(作者自述)。要量化:色度圖各處、各方向上,人眼對
色差的靈敏度是多少(Kodak 解讀分光光度量測的工程需求)。

## 方法與族群(轉引)
- **單一正常觀察者**(即著名的 PGN),**>25,000 次配色**、**25 個色度中心**
  (MacAdam 1982 自述:"Over 25,000 color matches by a single normal
  observer were recorded and analyzed.")。
- 自製色彩混合器:2° 雙分視野,一半固定、一半可調,**等亮度**(約
  48 cd/m²);42° 環境場(近 illuminant C,亮度約一半;此細節取自 K&G
  1992 p. 2165 的轉述)。
- 判準:試過多種(含 JND 類),**最後採「重複配色的標準差」**——最可
  重現;沿多條方向線測 SD,以之為半徑擬合每個中心的橢圓。

## 結果與限制
- 25 個中心各得一個等辨別性橢圓(原文 figures 23–48);**大小與長軸方向
  隨位置劇烈變化**,差距可達 20:1;成為其後 30 餘年色差解讀的標準工具、
  CIE 色差公式與 SDCM 規格的源頭。
- 限制(多為後人指出):單一觀察者;2° 中央窩、單一亮度平面(3D 推廣是
  Brown & MacAdam 1949);Wyszecki & Fielder (1971) 重測顯示同一觀察者的
  橢圓重測變異很大;[[krauskopf-gegenfurtner1992]] 指出其適應控制不嚴
  (觀察者實際上適應了配色刺激本身)——他們的重做正是為此。

**對 AVWM 的含意**:這是「不能拿 CIELAB/CIE76 的等距當知覺等距」的
歷史根據;AVWM 用 ΔE00 弧長當座標、又要跨圈檢驗 ΔE00 的修正是否足夠
([[決策脈絡_跨色相圈類推]]),整條線的起點在這裡。

## 可連結脈絡
- 適應控制嚴格版的重做(閾值在適應點最小)— [[krauskopf-gegenfurtner1992]]
- 非均勻性的現代官方修正 — [[luo2001]](CIEDE2000);顯示色驗證 — [[cui2001]]
- 引用處 — [[實驗設計脈絡_平面跟等彩度的問題]] §5.2
- AVWM 座標系決策 — [[決策脈絡_顏色維度]]

---
標籤note:[[literature-note]] [[AVWM]]

## 回查線索
**「MacAdam 橢圓」引用時最容易犯的錯?** → 寫成「JND 橢圓」。他量的是配色 SD,JND 是後世約 3 倍 SD 的慣例;引用時要嘛寫「配色標準差」,要嘛加註。
**「同樣距離的可辨性差 20 倍」出處?** → 本篇(經 MacAdam 1982 自述確認的數字)。
