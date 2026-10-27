# 決策脈絡 — AGRT 對刺激座標的隱含假設

## 結論

`AGRT.py` 的整個測量模型只有一行(加入 mvnun 相容層後在**第 133 行**,
上游原始檔是第 99 行):

```python
stats.norm.cdf(self._alpha, loc=self._x, scale=self._beta)
```

即 `P(r=0 | x) = δ/2 + (1-δ)·Φ((α - x)/β)`。受試者每次試驗抽一個內在知覺樣本
`ψ ~ N(x, β²)`,`ψ < α` 回答「低」,否則「高」,另有 δ 機率亂猜。

由此推出五條對刺激座標的要求:

| # | 要求 | 程式碼依據 | 違反的後果 |
|---|---|---|---|
| A1 | 感知轉換函數必須**線性**(仿射會被 α、β 吸收) | `loc=self._x`,無 transducer 參數 | 非線性成分無參數可吸收,被錯攤到 β |
| A2 | β 是**整個範圍共用一個常數** | `_beta` 形狀 `(1,1,β網格,1)`,無 x 軸 | Weber 式雜訊(音長)必須先取 log |
| A3 | α 落在 `dimrange` 內,且**接近中點** | α 網格 = `dim1range`;β 上限用 `mean(range)-range[0]` | 界線在範圍外 → 後驗堆在邊界 |
| A4 | 三個網格都**等距** | `stepType='lin'` 寫死 | 座標若彎曲,取樣密度分配錯誤 |
| A5 | 每維只有**兩個反應層級**且**單調** | `self.r = np.array(range(2))`;Φ 對 x 嚴格遞減 | 環狀維度(色相)繞回就崩潰 |

**由 A3 推出的範圍公式**(lapse=0.08):

```
beta 上限 = 半範圍 / 2.3107
```

分子 `np.average(dim1range) - dim1range[0]` 是**半範圍**,不是全範圍。

## 被推翻的假設

### ❌「這些假設寫在 AGRT 的文件裡」

**沒有。** 全檔搜尋 `monoton|continu|psychometric|assum|linear|gaussian|normal`
只命中三處,都與此無關(第 206、212 行的 docstring 講 2AFC 的 expectedMin,
第 543 行講 lapse)。

**這五條是我從第 133 行推導的**,不是文件記載。分層來看:
- **程式碼字面寫的**:公式本身,自由參數只有 α、β
- **數學必然推論**:Φ 對 x 嚴格遞減 → 單調性;`estimateThreshold` 回傳
  `α ± β√2·erfinv(·)` 是**任意實數** → 座標必須能實際做出該值
- **我的判斷**:「所以座標要先拉直」是建議,不是程式碼直接說的

一開始沒講清楚這個分層是我的疏漏。

### ❌「`overallAccuracy` 填多少就得到多少」

**不是。** `estimateGRTintensities` 傳 `np.sqrt(overallAccuracy)` 給
`estimateThreshold`,後者內部**又取一次** `np.sqrt(thresh)`,最終目標是
`overallAcc^(1/4)`:

```
overallAccuracy=0.75    → 單維 0.9306, 聯合 0.8660
overallAccuracy=0.5625  → 單維 0.8660, 聯合 0.7500
overallAccuracy=0.6400  → 單維 0.8944, 聯合 0.8000   ← 目前採用
```

而 `AGRT Quick Accuracy Check.R` 印的是「Overall Accuracy (targeting 75%)」、
算的正是**聯合**正確率(`mycorrect` 要整個 (r1,r2) 都對才算 1)。
同時 `RunAdaptiveBlock` 的邊界檢查用 `sqrt(overallAcc)` 當單維目標,
與內部那層 sqrt 不一致。**看起來是多套了一次開根號。**

引用前應核對 Glavan 等人論文正文報告的 achieved accuracy 是哪個數字。

## 相關
- 顏色軸如何滿足 A1/A2 — [[決策脈絡_顏色維度]]
- 聽覺軸為何一直卡在 A1/A2/A5 — [[決策脈絡_聽覺維度]]
- 目標正確率的選擇 — [[決策脈絡_統計方法]]
