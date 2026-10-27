# adaptivesft

用 Lognormal Race Model (LNRM) 校準 SFT / DFP 的 salience 水準:
**給定目標正確率(H 高、L 低),反解出該用多大的刺激差異。**

純 Python(PyMC),不需要 R 或 Stan。

## 為什麼不直接用 jhoupt/adaptiveSFT

原 repo(已 clone 到 `/home/yyc/symmetry/adaptiveSFT`,最後 commit 2019-03)有三個問題:

| 問題 | 說明 |
|---|---|
| **缺檔** | 程式碼引用 `lnrm0/lnrm1/lnrm2/lnrm2a.stan` 四支,repo 裡只存在 `lnrm2.stan`。ogival 版 `lnrm2a.stan` 不存在,所以 `find_salience_ogival()` 與 `simulateLNRM_ogival.R` **都跑不起來** |
| **`adaptive_sft2.py` 是壞的** | `posterior_samples['intensity']^2` 把 `^` 當次方(Python 裡是 XOR)、`allchannels` 從未定義、`lognorm.logpdf` 同時給 `loc` 與 `scale` 參數化錯誤 |
| **介面誤導** | `find_salience_ogival(dat, h_targ, l_targ)` 的 `h_targ`/`l_targ` 是 **drift 差的目標值,不是正確率**。`simulateLNRM_ogival.R` 用的 `l_targ=1.3`/`h_targ=8.0` 綁在他自己 DDM 模擬的 σ 上,換一組資料就不可達 |

本套件重建 ogival 模型,並把介面改成**直接吃目標正確率**。

## 模型

```
delta(x)  = D · inv_logit(slope · (x_std − midpoint))     兩條賽道的漂移「差」
z_correct = mu − delta/2
z_error   = mu + delta/2
(rt − psi) ~ LogNormal(z, sigma)                          獨立競爭,先到者勝
```

兩條賽道共用 `sigma` 時正確率有封閉解:

```
P(correct | x) = Φ( delta(x) / (sigma·√2) )
```

反解(逐個 posterior draw 做,所以輸出自帶不確定性):

```
delta* = √2 · sigma · Φ⁻¹(p)
x*     = midpoint + logit(delta*/D) / slope
```

強度在模型內部**標準化**,所以先驗不必隨物理單位(ΔE00 / dB / cd·m⁻²)重調;
`idata.attrs` 存了 `x_center`/`x_scale`,反解會自動換回物理單位。

## 用法

```python
from adaptivesft import fit_lnrm, find_salience, summarize

idata = fit_lnrm(intensity=dE00, correct=acc, rt=rt, link="ogival")
res = find_salience(idata, acc_high=0.90, acc_low=0.70)
print(summarize(res))
```

把 ΔE00 換成實際色票(固定 L\*/C\*、只變色相、CIEDE2000):

```python
from adaptivesft import make_pair, build_ladder

make_pair(h_target=303.0, target_de00=res["high"]["intensity"])
build_ladder([0, 2, 4, 6, 9, 12], hue_centers=[303.0])   # MOC 校準用階梯
```

## 命令列

```bash
PY=/home/yyc/symmetry/.venv/bin/python
cd /home/yyc/symmetry/AVWM

# 自我驗證(模擬 -> 擬合 -> 回復 -> 反解 -> 色票)
$PY -m adaptivesft.sim_recovery

# 跑真實校準資料
$PY -m adaptivesft.fit_calibration data/calib_S01.csv \
    --acc-high 0.90 --acc-low 0.70 \
    --out data/salience_S01.json --plot figure/psychometric_S01.png
```

輸入 CSV 需要 `intensity` / `correct` / `rt` 三欄(欄名可用 `--col-*` 覆寫)。

## 驗證狀態

`sim_recovery` 用 10 個強度層 × 每層 120 trial 的模擬資料:

- 6 個參數全部落在 94% HDI 內,`r_hat` = 1.00,**0 divergences**,抽樣約 13 秒
- 反解 0.65–0.95 的目標正確率,回代誤差 < 0.001

## 已知限制

- `D`(delta 的上漸近線)在資料沒觸及天花板時識別度差。`find_salience` 會回報
  `reachable`(有多少比例的 posterior draw 能達到目標正確率),低於 95% 就代表
  **校準範圍不夠寬,不要直接採用結果**。
- `psi` 是識別度最弱的參數,區間偏寬。這不影響 salience 反解(反解只用
  `sigma`/`slope`/`midpoint`/`D`)。
- 模型假設二選一作業、機遇水準 0.5、無 lapse rate。若實際作業的機遇水準不是 0.5
  (例如 yes/no 且目標出現率遠低於 50%),`accuracy` 會跟反應偏誤糾纏在一起,
  擬合出來的東西不是純粹的知覺敏感度。
