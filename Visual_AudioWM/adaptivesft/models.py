"""Lognormal Race Model (LNRM) 的 PyMC 實作。

取代 jhoupt/adaptiveSFT 的 Stan 模型:

    Stan 檔          本檔對應                    repo 內是否存在
    lnrm2.stan   ->  fit_lnrm(link="quadratic")  有
    lnrm1.stan   ->  fit_lnrm(link="linear")     沒有(被引用但不存在)
    lnrm2a.stan  ->  fit_lnrm(link="ogival")     沒有(被引用但不存在,本檔重建)

參數化(全套件一致,salience.py 反解時會用到):

    delta(x)  = 兩條賽道漂移率的「差」,恆正、隨強度單調遞增
    z_correct = mu - delta/2
    z_error   = mu + delta/2
    (rt - psi) ~ LogNormal(z, sigma)      兩條賽道獨立競爭,先到者勝

兩條 lognormal 賽道共用 sigma 時,正確率有封閉解:

    P(correct | x) = Phi( delta(x) / (sigma * sqrt(2)) )

這條式子是整套校準的核心 —— 它讓「目標正確率」可以反解成「目標強度」。

link 的三種形式:

    ogival     delta = D * inv_logit(slope * (xs - midpoint))   <- 建議用這個
    quadratic  delta = 2 * (alpha * xs + alpha2 * xs^2)
    linear     delta = 2 * alpha * xs

xs 是**標準化後**的強度(見 standardize),所以 slope/midpoint/alpha 的先驗
不必隨物理單位(ΔE00、dB、cd/m^2 ...)重調。標準化參數存在
idata.attrs 裡,salience.py 會自動換算回物理單位。

注意
----
Stan 的 lognormal(z, s) 第二個參數是**對數尺度的標準差 sigma**,不是變異數。
原碼把它命名為 varZ 又配 inv_gamma 先驗,容易誤導;本檔一律叫 sigma。
"""

from __future__ import annotations

import numpy as np
import pymc as pm
import pytensor.tensor as pt

__all__ = ["fit_lnrm", "standardize", "LINKS"]

LINKS = ("ogival", "quadratic", "linear")


def _normal_lcdf(x):
    """標準常態的 log CDF。

    寫成 log(erfc(...)) 的形式,pytensor 的 local_log_erfc 改寫會在
    |x| > 26.64 時自動切換到漸近展開,所以不會 underflow
    (已對照 scipy.stats.norm.logcdf 驗證到 x = -300)。
    """
    return pt.log(0.5) + pt.log(pt.erfc(-x / pt.sqrt(2.0)))


def standardize(x):
    """把物理強度轉成 z 分數,回傳 (xs, center, scale)。"""
    x = np.asarray(x, dtype=float)
    center = float(np.mean(x))
    scale = float(np.std(x))
    if not np.isfinite(scale) or scale <= 0:
        scale = 1.0
    return (x - center) / scale, center, scale


def _delta_expr(link, xs, params):
    """依 link 組出 delta(xs)。回傳 pytensor 運算式。"""
    if link == "ogival":
        return params["D"] * pm.math.invlogit(
            params["slope"] * (xs - params["midpoint"])
        )
    if link == "quadratic":
        return 2.0 * (params["alpha"] * xs + params["alpha2"] * xs**2)
    if link == "linear":
        return 2.0 * params["alpha"] * xs
    raise ValueError(f"未知的 link: {link!r},可用 {LINKS}")


def fit_lnrm(
    intensity,
    correct,
    rt,
    link="ogival",
    draws=1000,
    tune=1000,
    chains=4,
    target_accept=0.9,
    random_seed=11,
    psi_max_frac=0.99,
    progressbar=False,
    **sample_kwargs,
):
    """對 method-of-constant-stimuli 資料擬合 LNRM。

    參數
    ----
    intensity : array
        每個 trial 的刺激強度,**物理單位**(例如 ΔE00、SNR dB)。
    correct : array
        0/1,該 trial 是否正確。
    rt : array
        反應時間(秒)。必須全為正,且 > psi。
    link : {"ogival", "quadratic", "linear"}
        delta(x) 的形式。ogival 是有上下漸近線的標準心理測量函數,
        外插最穩,建議用它。
    psi_max_frac : float
        psi 的上界 = psi_max_frac * min(rt)。設成 1.0 時 psi 可以貼到
        minRT,log(rt - psi) 會發散;留一點邊界比較穩。

    回傳
    ----
    arviz.InferenceData
        idata.attrs 內含 link、x_center、x_scale,供 salience.py 反解用。
    """
    if link not in LINKS:
        raise ValueError(f"未知的 link: {link!r},可用 {LINKS}")

    x = np.asarray(intensity, dtype=float)
    c = np.asarray(correct, dtype=float)
    y = np.asarray(rt, dtype=float)
    if not (len(x) == len(c) == len(y)):
        raise ValueError("intensity / correct / rt 長度必須一致")
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(y)):
        raise ValueError("intensity 或 rt 含有 NaN/Inf")
    if np.any(y <= 0):
        raise ValueError("rt 必須全為正數")
    if len(np.unique(x)) < 3:
        raise ValueError("強度層級少於 3 個,心理測量函數無法識別")

    xs, x_center, x_scale = standardize(x)
    psi_upper = psi_max_frac * float(y.min())

    with pm.Model() as model:
        params = {
            "mu": pm.Normal("mu", 0.0, 1.0),
            "sigma": pm.InverseGamma("sigma", alpha=1.0, beta=0.1),
            "psi": pm.Uniform("psi", 0.0, psi_upper),
        }
        if link == "ogival":
            params["slope"] = pm.HalfNormal("slope", 5.0)
            params["midpoint"] = pm.Normal("midpoint", 0.0, 1.0)
            # D = delta 的上漸近線。不像原碼寫死 10;寫死會讓可用區段被
            # 擠到 ogive 的極端尾巴,slope/midpoint 反而估不準。
            params["D"] = pm.HalfNormal("D", 2.0)
        elif link == "quadratic":
            params["alpha"] = pm.Normal("alpha", 0.0, 2.0)
            params["alpha2"] = pm.Normal("alpha2", 0.0, 1.0)
        else:
            params["alpha"] = pm.Normal("alpha", 0.0, 2.0)

        delta = _delta_expr(link, xs, params)
        pm.Deterministic("delta", delta)

        z_correct = params["mu"] - delta / 2.0
        z_error = params["mu"] + delta / 2.0
        z_win = pt.where(c > 0.5, z_correct, z_error)
        z_lose = pt.where(c > 0.5, z_error, z_correct)

        t = y - params["psi"]
        logt = pt.log(t)
        sigma = params["sigma"]

        # 勝者的 log 密度 + 敗者的 log 存活函數
        log_pdf = (
            -logt
            - pt.log(sigma)
            - 0.5 * np.log(2.0 * np.pi)
            - 0.5 * ((logt - z_win) / sigma) ** 2
        )
        log_sf = _normal_lcdf((z_lose - logt) / sigma)
        pm.Potential("lik", pt.sum(log_pdf + log_sf))

        idata = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=progressbar,
            **sample_kwargs,
        )

    idata.attrs["link"] = link
    idata.attrs["x_center"] = x_center
    idata.attrs["x_scale"] = x_scale
    idata.attrs["n_trials"] = int(len(x))
    idata.attrs["intensity_levels"] = sorted(float(v) for v in np.unique(x))
    return idata
