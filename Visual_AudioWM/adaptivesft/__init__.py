"""adaptivesft — 用 Lognormal Race Model 校準 SFT/DFP 的 salience 水準。

把 jhoupt/adaptiveSFT (Stan + R + Python 混用) 需要的部分改寫成純 Python
(PyMC),並補上原 repo 引用卻不存在的 ogival 模型 (lnrm2a.stan)。

典型用法
--------
    from adaptivesft import fit_lnrm, find_salience, summarize

    idata = fit_lnrm(intensity=dE00, correct=acc, rt=rt, link="ogival")
    res = find_salience(idata, acc_high=0.90, acc_low=0.70)
    print(summarize(res))

自我驗證
--------
    python -m adaptivesft.sim_recovery

實際校準資料
------------
    python -m adaptivesft.fit_calibration <校準資料.csv>
"""

from .color import build_ladder, foil_hue_for_de00, make_pair
from .models import LINKS, fit_lnrm, standardize
from .salience import (
    accuracy_to_delta,
    delta_to_accuracy,
    find_salience,
    find_salience_delta,
    predict_accuracy,
    psychometric_curve,
    salience_for_accuracy,
    summarize,
)
from .simulate import simulate_moc

__all__ = [
    "fit_lnrm",
    "standardize",
    "LINKS",
    "find_salience",
    "find_salience_delta",
    "salience_for_accuracy",
    "predict_accuracy",
    "psychometric_curve",
    "accuracy_to_delta",
    "delta_to_accuracy",
    "summarize",
    "simulate_moc",
    "make_pair",
    "foil_hue_for_de00",
    "build_ladder",
]

__version__ = "0.1.0"
