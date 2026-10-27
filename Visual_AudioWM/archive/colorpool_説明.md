# Colorpool.py 運作說明

## 概述

`colorpool.py` 用於產生實驗所需的 155 組顏色刺激，每組包含：
- 2 個 target 顏色 (color1_target, color2_target)
- 每個 target 各有 1 個 High confusability (H) 和 1 個 Low confusability (L) 顏色

## skimage 的作用

使用 `skimage.color` 模組進行色彩空間轉換：

```python
from skimage import color as skcolor
```

### 為什麼用 CIELAB 色彩空間？

| 色彩空間 | 特性 |
|---------|------|
| RGB | 裝置依賴，歐式距離 ≠ 感知差異 |
| **CIELAB** | 感知均勻，歐式距離 ≈ 人眼感知差異 (Delta E) |

### 主要函數

```python
# LAB → RGB（用於產生 hex 色碼）
rgb = skcolor.lab2rgb(np.array([[[L, a, b]]]))[0][0]
```

## Delta E 計算

Delta E (ΔE) 是 CIELAB 空間中兩色的歐式距離：

```python
def delta_e(c1, c2):
    return float(np.sqrt(np.sum((np.array(c1) - np.array(c2)) ** 2)))
```

$$\Delta E = \sqrt{(L_1 - L_2)^2 + (a_1 - a_2)^2 + (b_1 - b_2)^2}$$

### Delta E 感知參考

| Delta E | 感知程度 |
|---------|---------|
| < 1 | 無法察覺 |
| 1-2 | 仔細觀察可察覺 |
| 2-3.5 | 可察覺 |
| 3.5-5 | 明顯差異 |
| > 5 | 顯著差異 |

## 顏色產生邏輯

### 1. 隨機產生 LAB 顏色

```python
def random_lab():
    L = np.random.uniform(40, 60)      # 亮度：40-60
    C = np.random.uniform(40, 60)      # 彩度：40-60
    H_rad = np.random.uniform(0, 2*π)  # 色相：0-360°
    a = C * cos(H_rad)
    b = C * sin(H_rad)
    return [L, a, b]
```

### 2. 找相近顏色 (H/L)

```python
def find_color(target, de_min, de_max, max_tries=2000):
    # 從 target 出發，隨機方向移動 de_min ~ de_max 距離
    direction = np.random.randn(3)  # 隨機方向
    direction = direction / np.linalg.norm(direction)  # 單位向量
    candidate = target + direction * np.random.uniform(de_min, de_max)
```

### 3. Gamut 檢查

確保顏色在 sRGB 可顯示範圍內：

```python
def is_in_gamut(L, a, b):
    rgb = skcolor.lab2rgb(np.array([[[L, a, b]]]))[0][0]
    return bool(np.all(rgb >= 0) and np.all(rgb <= 1))
```

## 產生條件約束

每組 trial 必須滿足：

| 條件 | Delta E 要求 |
|------|-------------|
| target1 ↔ H1 | 25 ~ 50 |
| target1 ↔ L1 | 20 ~ 30 |
| H1 ↔ L1 | > 15 |
| target2 ↔ H2 | 25 ~ 50 |
| target2 ↔ L2 | 20 ~ 30 |
| H2 ↔ L2 | > 15 |
| target1 ↔ target2 | > 20 |
| 與前一組 targets | > 30 |

## 輸出格式

`stimuli/color_155trials.csv`:

```csv
trial,color1_target,color1_H,color1_L,color1_H_deltaE,color1_L_deltaE,...
1,#009E95,#00FFFF,#32966C,40.41,23.14,...
```

## ⚠️ 已知問題

**只檢查連續 trial 之間的 Delta E：**

```python
# 第 59 行：只比較 prev_targets（上一組）
if prev_targets and any(delta_e(c, pt) < 30 for pt in prev_targets):
    continue

# 第 136 行：只保留上一組
prev_targets = [t1, t2]
```

這導致 Trial 1 和 Trial 100 可能有非常相似的顏色（Delta E < 3），在 shuffle 後可能出現在同一個 block 中。

### 建議修改

改為檢查所有已產生的 targets：

```python
all_targets = []  # 記錄所有 targets

# 檢查與所有已產生的 targets 距離
if any(delta_e(c, pt) < MIN_CROSS_TRIAL_DE for pt in all_targets):
    continue

# 加入新的 targets
all_targets.extend([t1, t2])
```
