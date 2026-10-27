"""吃真實校準資料 -> 擬合 LNRM -> 輸出 H / L 的 ΔE00。

用法
----
    cd /home/yyc/symmetry/AVWM
    /home/yyc/symmetry/.venv/bin/python -m adaptivesft.fit_calibration \
        data/calib_S01.csv --acc-high 0.90 --acc-low 0.70 \
        --out data/salience_S01.json --plot figure/psychometric_S01.png

輸入 CSV 至少要有三欄(欄名可用 --col-* 覆寫):
    intensity  刺激強度,物理單位(顏色用 ΔE00,聽覺用 SNR dB)
    correct    0/1
    rt         反應時間(秒)

輸出 JSON 可直接被刺激產生器讀取,取代 colorpool.py 裡寫死的
H=(25,50) / L=(20,30)。
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from .models import fit_lnrm
from .salience import find_salience, psychometric_curve, summarize


def load_csv(path, col_intensity, col_correct, col_rt):
    x, c, t = [], [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = {col_intensity, col_correct, col_rt} - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(
                f"CSV 缺少欄位 {sorted(missing)};現有欄位:{reader.fieldnames}"
            )
        for row in reader:
            try:
                xi = float(row[col_intensity])
                ci = float(row[col_correct])
                ti = float(row[col_rt])
            except (TypeError, ValueError):
                continue  # 空白或非數值(練習 trial、逾時未反應)一律跳過
            if not np.isfinite([xi, ci, ti]).all():
                continue
            x.append(xi)
            c.append(ci)
            t.append(ti)
    return np.array(x), np.array(c), np.array(t)


def trim_rt(x, c, t, rt_min, rt_max):
    keep = (t >= rt_min) & (t <= rt_max)
    return x[keep], c[keep], t[keep], int((~keep).sum())


def main(argv=None):
    ap = argparse.ArgumentParser(description="LNRM salience 校準")
    ap.add_argument("csv", help="校準資料 CSV")
    ap.add_argument("--col-intensity", default="intensity")
    ap.add_argument("--col-correct", default="correct")
    ap.add_argument("--col-rt", default="rt")
    ap.add_argument("--acc-high", type=float, default=0.90, help="H 的目標正確率")
    ap.add_argument("--acc-low", type=float, default=0.70, help="L 的目標正確率")
    ap.add_argument("--link", default="ogival", choices=("ogival", "quadratic", "linear"))
    ap.add_argument("--rt-min", type=float, default=0.15, help="低於此值視為搶按")
    ap.add_argument("--rt-max", type=float, default=5.0, help="高於此值視為分心")
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--tune", type=int, default=1000)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--unit", default="ΔE00", help="強度的單位名稱,只影響列印")
    ap.add_argument("--out", help="把結果寫成 JSON")
    ap.add_argument("--plot", help="把心理測量函數畫出來存成 PNG")
    args = ap.parse_args(argv)

    x, c, t = load_csv(args.csv, args.col_intensity, args.col_correct, args.col_rt)
    x, c, t, n_trimmed = trim_rt(x, c, t, args.rt_min, args.rt_max)
    if len(x) == 0:
        raise SystemExit("讀不到任何有效 trial")

    levels = np.unique(x)
    print(f"檔案:{args.csv}")
    print(f"有效 trial:{len(x)}(RT 修剪掉 {n_trimmed} 筆)")
    print(f"強度層級:{len(levels)} 個,範圍 {levels.min():.3f} – {levels.max():.3f} {args.unit}")

    # 強度是連續變項時(每個 trial 的 ΔE 都不同),分箱只是為了顯示與診斷;
    # 擬合一律用原始的連續值。
    if len(levels) <= 12:
        bins = [(lv, lv, x == lv) for lv in levels]
        header = f"{args.unit:>18}"
    else:
        edges = np.quantile(x, np.linspace(0, 1, 9))
        edges[-1] += 1e-9
        bins = [
            (edges[i], edges[i + 1], (x >= edges[i]) & (x < edges[i + 1]))
            for i in range(len(edges) - 1)
        ]
        header = f"{args.unit + ' 分箱':>18}"
        print("(強度為連續值,以下依八分位數分箱顯示;擬合仍用原始連續值)")

    print(f"\n{header}{'n':>6}{'正確率':>9}{'中位RT':>9}")
    obs = []
    for lo_e, hi_e, m in bins:
        if not m.any():
            continue
        obs.append(float(c[m].mean()))
        label = f"{lo_e:.2f}" if lo_e == hi_e else f"{lo_e:7.2f}–{hi_e:7.2f}"
        print(f"{label:>18}{m.sum():>6}{c[m].mean():>9.3f}{np.median(t[m]):>9.3f}")
    if max(obs) - min(obs) < 0.20:
        print(
            "\n⚠ 各強度層的正確率差異不到 0.20 —— 心理測量函數幾乎是平的,"
            "slope 會估不準。校準的強度範圍可能太窄,或作業對受試者太難/太簡單。"
        )
    if min(obs) > 0.85:
        print("\n⚠ 最低強度層的正確率仍 > 0.85,校準沒有涵蓋到函數的下半段。")
    if max(obs) < 0.85:
        print("\n⚠ 最高強度層的正確率仍 < 0.85,校準沒有涵蓋到函數的上半段。")

    idata = fit_lnrm(
        x, c, t,
        link=args.link, draws=args.draws, tune=args.tune,
        chains=args.chains, random_seed=args.seed, progressbar=False,
    )
    n_div = int(idata.sample_stats["diverging"].sum())
    if n_div:
        print(f"\n⚠ 有 {n_div} 個 divergence,後驗可能有偏誤。可試著提高 --tune。")

    res = find_salience(idata, acc_high=args.acc_high, acc_low=args.acc_low)
    print("\n--- 校準結果 ---")
    print(summarize(res, unit=args.unit))

    if args.out:
        payload = {
            "source_csv": str(Path(args.csv).resolve()),
            "n_trials": int(len(x)),
            "link": args.link,
            "unit": args.unit,
            "divergences": n_div,
            "high": res["high"],
            "low": res["low"],
            "warnings": res["warnings"],
        }
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\n結果寫入 {args.out}")

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        grid = np.linspace(float(levels.min()), float(levels.max()), 120)
        med, lo, hi = psychometric_curve(idata, grid)
        fig, ax = plt.subplots(figsize=(6.5, 4.2))
        ax.fill_between(grid, lo, hi, alpha=0.25, label="94% CI")
        ax.plot(grid, med, lw=2, label="LNRM 擬合")
        ax.scatter(levels, obs, zorder=5, color="k", label="觀察值")
        for name, color in (("high", "tab:green"), ("low", "tab:orange")):
            r = res[name]
            if np.isfinite(r["intensity"]):
                ax.axvline(r["intensity"], ls="--", color=color,
                           label=f"{name} (acc={r['target_accuracy']:.2f})")
        ax.axhline(0.5, color="grey", lw=0.8, ls=":")
        ax.set_xlabel(args.unit)
        ax.set_ylabel("P(correct)")
        ax.set_ylim(0.4, 1.02)
        ax.legend(fontsize=8)
        fig.tight_layout()
        Path(args.plot).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.plot, dpi=150)
        print(f"圖存到 {args.plot}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
