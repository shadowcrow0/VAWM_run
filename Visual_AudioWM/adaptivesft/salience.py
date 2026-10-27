"""從 LNRM 後驗反解出 H / L 兩個 salience 水準的刺激強度。

核心關係(參數化見 models.py):

    P(correct | x) = Phi( delta(x) / (sigma * sqrt(2)) )

反過來,給定目標正確率 p:

    delta*  = sqrt(2) * sigma * Phi^-1(p)          <- 依賴 sigma!
    x*      = link 的反函數(delta*)

第二步依 link 而異:

    ogival     x* = midpoint + logit(delta*/D) / slope
    quadratic  x* = (-alpha + sqrt(alpha^2 + 2*alpha2*delta*)) / (2*alpha2)
    linear     x* = delta* / (2*alpha)

反解是**逐個 posterior draw** 做的,所以輸出自帶不確定性;不是先取後驗
平均再反解(那會低估不確定性,而且在非線性反函數下有偏誤)。

與原始 adaptiveSFT 的差異
------------------------
Houpt 的 find_salience_ogival() 收的 h_targ / l_targ 是 **delta 的目標值**
(simulateLNRM_ogival.R 裡是 l_targ=1.3、h_targ=8.0,搭配寫死的 L=10),
不是正確率。那兩個數字對應到什麼正確率完全取決於擬合出來的 sigma,
換一組資料就失效 —— 實測在 D≈0.95 的資料上,delta=1.3 有 99.7% 的
posterior draw 落在模型可達範圍外。

所以本檔的主要介面是 find_salience(...)(吃正確率);
find_salience_delta(...) 保留 Houpt 的原介面,只為對照用。
"""

from __future__ import annotations

import numpy as np
from scipy.special import logit as _logit
from scipy.stats import norm

__all__ = [
    "accuracy_to_delta",
    "delta_to_accuracy",
    "predict_accuracy",
    "salience_for_accuracy",
    "find_salience",
    "find_salience_delta",
    "psychometric_curve",
    "summarize",
]

_SQRT2 = np.sqrt(2.0)


def _flat(idata, name):
    """把 (chain, draw) 攤平成 1 維。"""
    return np.asarray(idata.posterior[name].values).ravel()


def _scaling(idata):
    return float(idata.attrs["x_center"]), float(idata.attrs["x_scale"])


def accuracy_to_delta(p, sigma):
    """目標正確率 -> 目標 delta。p 必須 > 0.5(0.5 是二選一的機遇水準)。"""
    p = np.asarray(p, dtype=float)
    if np.any(p <= 0.5) or np.any(p >= 1.0):
        raise ValueError("目標正確率必須落在 (0.5, 1.0) 開區間")
    return _SQRT2 * np.asarray(sigma, dtype=float) * norm.ppf(p)


def delta_to_accuracy(delta, sigma):
    """delta -> 正確率。"""
    return norm.cdf(np.asarray(delta, float) / (np.asarray(sigma, float) * _SQRT2))


def _delta_at_std(idata, xs):
    """在標準化強度 xs 上,算出每個 posterior draw 的 delta。"""
    link = idata.attrs["link"]
    xs = np.asarray(xs, dtype=float)
    if link == "ogival":
        D, slope, mp = (_flat(idata, k) for k in ("D", "slope", "midpoint"))
        return D * (1.0 / (1.0 + np.exp(-slope * (xs - mp))))
    if link == "quadratic":
        a, a2 = _flat(idata, "alpha"), _flat(idata, "alpha2")
        return 2.0 * (a * xs + a2 * xs**2)
    if link == "linear":
        return 2.0 * _flat(idata, "alpha") * xs
    raise ValueError(f"未知的 link: {link!r}")


def _invert_delta_std(idata, delta_star):
    """delta 目標 -> 標準化強度。不可達的 draw 回傳 NaN。"""
    link = idata.attrs["link"]
    d = np.asarray(delta_star, dtype=float)
    out = np.full(d.shape, np.nan)

    if link == "ogival":
        D, slope, mp = (_flat(idata, k) for k in ("D", "slope", "midpoint"))
        frac = d / D
        ok = (frac > 0.0) & (frac < 1.0) & (slope > 0)
        out[ok] = mp[ok] + _logit(frac[ok]) / slope[ok]
        return out

    if link == "quadratic":
        a, a2 = _flat(idata, "alpha"), _flat(idata, "alpha2")
        disc = a**2 + 2.0 * a2 * d
        near_linear = np.abs(a2) < 1e-8
        ok = (disc >= 0) & ~near_linear
        out[ok] = (-a[ok] + np.sqrt(disc[ok])) / (2.0 * a2[ok])
        lin = near_linear & (np.abs(a) > 1e-12)
        out[lin] = d[lin] / (2.0 * a[lin])
        return out

    if link == "linear":
        a = _flat(idata, "alpha")
        ok = np.abs(a) > 1e-12
        out[ok] = d[ok] / (2.0 * a[ok])
        return out

    raise ValueError(f"未知的 link: {link!r}")


def predict_accuracy(idata, x):
    """給定物理強度 x(純量),回傳每個 posterior draw 預測的正確率。"""
    center, scale = _scaling(idata)
    xs = (float(x) - center) / scale
    return delta_to_accuracy(_delta_at_std(idata, xs), _flat(idata, "sigma"))


def salience_for_accuracy(idata, p):
    """給定目標正確率 p,回傳每個 posterior draw 所需的**物理**強度。

    回傳 (x_draws, reachable_fraction)。不可達的 draw 是 NaN。
    """
    center, scale = _scaling(idata)
    sigma = _flat(idata, "sigma")
    delta_star = accuracy_to_delta(p, sigma)
    xs = _invert_delta_std(idata, delta_star)
    reachable = float(np.mean(np.isfinite(xs)))
    return center + scale * xs, reachable


def _nanmedian(v):
    """全是 NaN 時安靜地回傳 NaN,不噴 RuntimeWarning。"""
    v = np.asarray(v, dtype=float)
    return float(np.median(v[np.isfinite(v)])) if np.any(np.isfinite(v)) else float("nan")


def _interval(v, hdi_prob):
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return float("nan"), float("nan")
    lo_q = 100.0 * (1.0 - hdi_prob) / 2.0
    lo, hi = np.percentile(v, [lo_q, 100.0 - lo_q])
    return float(lo), float(hi)


def find_salience(idata, acc_high=0.90, acc_low=0.70, hdi_prob=0.94):
    """主介面:給兩個目標正確率,回傳 H / L 的刺激強度。

    參數
    ----
    acc_high, acc_low : float
        H(高 salience,正確率高)與 L(低 salience,正確率低)的目標正確率。
    hdi_prob : float
        區間覆蓋率。

    回傳
    ----
    dict,含 high / low 兩個 key,各自有:
        target_accuracy  設定的目標
        intensity        後驗中位數(物理單位)—— 拿這個去做刺激
        ci               (下界, 上界)
        reachable        後驗中有多少比例的 draw 能達到這個正確率
        check_accuracy   把 intensity 回代得到的正確率中位數
    另有 warnings 清單。
    """
    if acc_high <= acc_low:
        raise ValueError("acc_high 必須大於 acc_low")

    result = {"hdi_prob": hdi_prob, "link": idata.attrs["link"], "warnings": []}
    for name, p in (("high", acc_high), ("low", acc_low)):
        x_draws, reachable = salience_for_accuracy(idata, p)
        med = _nanmedian(x_draws)
        lo, hi = _interval(x_draws, hdi_prob)
        result[name] = {
            "target_accuracy": float(p),
            "intensity": med,
            "ci": (lo, hi),
            "reachable": reachable,
            "check_accuracy": (
                float(np.median(predict_accuracy(idata, med)))
                if np.isfinite(med)
                else float("nan")
            ),
        }
        if reachable < 0.95:
            result["warnings"].append(
                f"{name}: 只有 {reachable:.1%} 的 posterior draw 能達到 "
                f"正確率 {p:.2f} —— 校準資料可能沒有涵蓋到這個水準,"
                f"建議擴大強度範圍重跑。"
            )

    levels = idata.attrs.get("intensity_levels")
    if levels:
        lo_lv, hi_lv = float(min(levels)), float(max(levels))
        for name in ("high", "low"):
            xi = result[name]["intensity"]
            if not (lo_lv <= xi <= hi_lv):
                result["warnings"].append(
                    f"{name}: 反解出的強度 {xi:.3f} 落在校準範圍 "
                    f"[{lo_lv:.3f}, {hi_lv:.3f}] 之外(外插),請謹慎採用。"
                )
    return result


def find_salience_delta(idata, h_targ=8.0, l_targ=1.3):
    """Houpt 原介面:h_targ / l_targ 是 **delta 的目標值**,不是正確率。

    只為了跟 adaptiveSFT_functions.R 的 find_salience_ogival() 對照。
    正式校準請改用 find_salience()。
    """
    out = {}
    sigma = _flat(idata, "sigma")
    center, scale = _scaling(idata)
    for name, targ in (("high", h_targ), ("low", l_targ)):
        xs = _invert_delta_std(idata, np.full(sigma.shape, float(targ)))
        x = center + scale * xs
        out[name] = {
            "delta_target": float(targ),
            "intensity": _nanmedian(x),
            "reachable": float(np.mean(np.isfinite(xs))),
            "implied_accuracy": float(np.median(delta_to_accuracy(targ, sigma))),
        }
    return out


def psychometric_curve(idata, x_grid, hdi_prob=0.94):
    """回傳 (中位數, 下界, 上界) 三條曲線,用來畫圖或檢查。"""
    x_grid = np.asarray(x_grid, dtype=float)
    med = np.empty_like(x_grid)
    lo = np.empty_like(x_grid)
    hi = np.empty_like(x_grid)
    for i, x in enumerate(x_grid):
        acc = predict_accuracy(idata, x)
        med[i] = np.median(acc)
        lo[i], hi[i] = _interval(acc, hdi_prob)
    return med, lo, hi


def summarize(res, unit="ΔE00"):
    """把 find_salience() 的結果印成表。"""
    lines = [
        f"link = {res['link']}   區間 = {res['hdi_prob']:.0%}",
        f"{'':6}{'目標acc':>9}{'強度(' + unit + ')':>16}{'區間':>26}{'回代acc':>10}{'可達':>8}",
    ]
    for name, label in (("high", "H"), ("low", "L")):
        r = res[name]
        lo, hi = r["ci"]
        lines.append(
            f"{label:6}{r['target_accuracy']:>9.2f}{r['intensity']:>16.3f}"
            f"   [{lo:8.3f}, {hi:8.3f}]{r['check_accuracy']:>10.3f}"
            f"{r['reachable']:>8.1%}"
        )
    for w in res["warnings"]:
        lines.append(f"  ⚠ {w}")
    return "\n".join(lines)
