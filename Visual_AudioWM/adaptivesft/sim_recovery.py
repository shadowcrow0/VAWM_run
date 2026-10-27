"""自我驗證:模擬 -> 擬合 -> 參數回復 -> 反解 -> 換成色票。

用法
----
    cd /home/yyc/symmetry/AVWM
    /home/yyc/symmetry/.venv/bin/python -m adaptivesft.sim_recovery

這支腳本對應原 repo 的 simulateLNRM_ogival.R —— 但那支跑不起來,
因為它第 62 行呼叫的 lnrm2a.stan 在 repo 裡不存在。
"""

from __future__ import annotations

import time

import arviz as az
import numpy as np

from .color import build_ladder, make_pair
from .models import fit_lnrm
from .salience import (
    find_salience,
    find_salience_delta,
    salience_for_accuracy,
    summarize,
)
from .simulate import simulate_moc

# 強度單位 = ΔE00。真值挑成:ΔE00=0 時正確率 0.5(機遇),
# ΔE00=12 時約 0.97 —— 涵蓋整條心理測量函數,slope/midpoint 才估得準。
LEVELS = np.linspace(0.0, 12.0, 10)
N_PER_LEVEL = 120
TRUTH = dict(D=0.95, slope=2.0, midpoint=0.37, mu=0.0, sigma=0.30, psi=0.20)
HUE_CENTER = 303.0  # colorWM.md 建議的色相(離藍/紫命名邊界最遠)


def main():
    print("=" * 78)
    print("adaptivesft 自我驗證:ogival LNRM(重建原 repo 缺失的 lnrm2a.stan)")
    print("=" * 78)

    sim = simulate_moc(LEVELS, N_PER_LEVEL, seed=11, **TRUTH)
    print(
        f"\n模擬資料:{len(LEVELS)} 個強度層 × 每層 {N_PER_LEVEL} trial "
        f"= {len(sim['intensity'])} trials,整體正確率 {sim['correct'].mean():.3f}"
    )
    print(f"\n{'ΔE00':>8}{'觀察 acc':>10}{'理論 acc':>10}")
    for r in sim["accuracy_by_level"]:
        print(f"{r['intensity']:>8.2f}{r['observed']:>10.3f}{r['theoretical']:>10.3f}")

    t0 = time.time()
    idata = fit_lnrm(
        sim["intensity"], sim["correct"], sim["rt"], link="ogival", progressbar=False
    )
    elapsed = time.time() - t0

    summ = az.summary(idata, var_names=list(TRUTH), hdi_prob=0.94)
    summ["true"] = [TRUTH[v] for v in summ.index]
    summ["covered"] = (summ["hdi_3%"] <= summ["true"]) & (
        summ["true"] <= summ["hdi_97%"]
    )
    print(f"\n--- 參數回復 ({elapsed:.0f}s) ---")
    print(summ[["mean", "sd", "hdi_3%", "hdi_97%", "true", "covered", "r_hat", "ess_bulk"]])
    n_div = int(idata.sample_stats["diverging"].sum())
    print(f"divergences = {n_div}")
    ok_recover = bool(summ["covered"].all()) and n_div == 0
    print(f"回復通過(全部落在 94% HDI 內且無 divergence):{ok_recover}")

    print("\n--- 反解:目標正確率 -> 所需 ΔE00 ---")
    print(f"{'目標 acc':>9}{'ΔE00 中位數':>14}{'94% CI':>24}{'回代 acc':>11}{'可達':>8}")
    for p in (0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65):
        res = find_salience(idata, acc_high=p, acc_low=0.6001)
        h = res["high"]
        lo, hi = h["ci"]
        print(
            f"{p:>9.2f}{h['intensity']:>14.3f}   [{lo:7.3f}, {hi:7.3f}]"
            f"{h['check_accuracy']:>11.3f}{h['reachable']:>8.1%}"
        )

    print("\n--- 建議的 H / L 設定(acc 0.90 / 0.70)---")
    res = find_salience(idata, acc_high=0.90, acc_low=0.70)
    print(summarize(res))

    print("\n--- 對照:直接套用 Houpt 的 h_targ=8.0 / l_targ=1.3 ---")
    alt = find_salience_delta(idata, h_targ=8.0, l_targ=1.3)
    for name in ("high", "low"):
        a = alt[name]
        print(
            f"  {name:5} delta={a['delta_target']:>4}  可達比例={a['reachable']:>6.1%}"
            f"  隱含正確率={a['implied_accuracy']:.4f}"
        )
    print(
        "  => 那兩個數字是 delta 的目標值不是正確率,綁在他自己模擬的 sigma 上,"
        "換一組資料就不可達。"
    )

    print("\n--- 把 H / L 的 ΔE00 換成實際色票 ---")
    for name, label in (("high", "H"), ("low", "L")):
        d = res[name]["intensity"]
        pair = make_pair(HUE_CENTER, d)
        print(
            f"  {label}  目標acc={res[name]['target_accuracy']:.2f}  ΔE00={d:6.3f}"
            f"  target={pair['target_hex']}  foil={pair['foil_hex']}"
            f"  Δhue={pair['dhue']:.2f}°  (實際 ΔE00={pair['de00']}, ΔE76={pair['de76']})"
        )

    print("\n--- 校準用階梯(build_ladder)前幾筆 ---")
    ladder = build_ladder([0, 2, 4, 6, 9, 12], [HUE_CENTER])
    print(f"  共 {len(ladder)} 個條件")
    for row in ladder[:5]:
        print(
            f"    ΔE00={row['intensity']:>5.1f} dir={row['direction']:+d} "
            f"match={row['is_match']} {row['target_hex']} -> {row['foil_hex']}"
        )

    print("\n" + "=" * 78)
    print(f"驗證結果:{'PASS' if ok_recover else 'FAIL'}")
    print("=" * 78)
    return 0 if ok_recover else 1


if __name__ == "__main__":
    raise SystemExit(main())
