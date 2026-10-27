"""從 LNRM 產生模擬資料,用於參數回復驗證與所需樣本數評估。

原始 adaptiveSFT 用 DDM (diffIRT::simdiffT) 生資料再用 LNRM 擬合,
刻意製造模型不匹配來測試 salience 反解的穩健性。本檔先做**自回復**
(LNRM 生、LNRM 擬合)—— 這是最基本的正確性檢查,自回復都過不了的話
談模型不匹配沒有意義。
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

__all__ = ["delta_ogival", "simulate_moc", "accuracy_at"]


def delta_ogival(x_std, D, slope, midpoint):
    return D / (1.0 + np.exp(-slope * (np.asarray(x_std, float) - midpoint)))


def accuracy_at(delta, sigma):
    return norm.cdf(np.asarray(delta, float) / (sigma * np.sqrt(2.0)))


def simulate_moc(
    levels,
    n_per_level,
    D=1.0,
    slope=4.0,
    midpoint=0.30,
    mu=0.0,
    sigma=0.30,
    psi=0.20,
    x_center=None,
    x_scale=None,
    seed=11,
):
    """產生 method-of-constant-stimuli 資料。

    levels 給的是**物理**強度(例如 ΔE00)。ogive 的參數 (slope, midpoint)
    定義在標準化強度上,所以會先用 x_center / x_scale 標準化;不給的話
    就用 levels 自己的平均與標準差(與 models.standardize 一致)。

    回傳 dict:intensity / correct / rt(皆為長度 len(levels)*n_per_level
    的陣列),以及 truth(真值)與 accuracy_by_level。
    """
    rng = np.random.default_rng(seed)
    levels = np.asarray(levels, dtype=float)
    x = np.repeat(levels, n_per_level)

    if x_center is None:
        x_center = float(x.mean())
    if x_scale is None:
        x_scale = float(x.std()) or 1.0
    xs = (x - x_center) / x_scale

    delta = delta_ogival(xs, D, slope, midpoint)
    t_correct = psi + rng.lognormal(mu - delta / 2.0, sigma)
    t_error = psi + rng.lognormal(mu + delta / 2.0, sigma)
    correct = (t_correct < t_error).astype(float)
    rt = np.minimum(t_correct, t_error)

    by_level = []
    for lv in levels:
        m = x == lv
        d = delta_ogival((lv - x_center) / x_scale, D, slope, midpoint)
        by_level.append(
            {
                "intensity": float(lv),
                "observed": float(correct[m].mean()),
                "theoretical": float(accuracy_at(d, sigma)),
                "n": int(m.sum()),
            }
        )

    return {
        "intensity": x,
        "correct": correct,
        "rt": rt,
        "truth": dict(
            D=D, slope=slope, midpoint=midpoint, mu=mu, sigma=sigma, psi=psi
        ),
        "x_center": x_center,
        "x_scale": x_scale,
        "accuracy_by_level": by_level,
    }
