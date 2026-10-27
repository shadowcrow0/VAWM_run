"""
校準結果 → stimuli/block1..6.csv（欄位與 practice.csv 相同），之後 VAWM_nobox.py 照舊。

    python make_adaptive_blocks.py data/<participant>_calib.json
    python make_adaptive_blocks.py data/<participant>_calib.json --out stimuli --blocks 6 --trials 24 --seed 1

會先印出校到的值：顏色 ΔE_H / ΔE_L（Lab 距離）、聲音 count_H / count_L（混淆次數）與假警報率。
H/L 落在範圍外時會警告但仍產生（要不要用由你決定）。
"""
import argparse

from adaptive_vawm import read_calibration, write_blocks


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("calib_json")
    ap.add_argument("--out", default="stimuli")
    ap.add_argument("--blocks", type=int, default=6)
    ap.add_argument("--trials", type=int, default=24, help="每個 block 的 study 組數（每組 9 個探測，同 VAWM_nobox）")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args(argv)

    cal = read_calibration(args.calib_json)
    c, a = cal["colour"], cal["audio"]
    print(f"method: {c['extra']['method']}  targets = {c['p_high']} / {c['p_low']}")
    print(f"colour: FA={c['false_alarm']:.2f}  alpha={c['alpha']:.2f} beta={c['beta']:.2f}  "
          f"dE_H={c['high']:.2f} dE_L={c['low']:.2f}  in_range={c['in_range']} {c['warnings']}")
    print(f"audio : FA={a['false_alarm']:.2f}  alpha={a['alpha']:.2f} beta={a['beta']:.2f}  "
          f"count_H={a['extra']['count_high']:.1f} count_L={a['extra']['count_low']:.1f}  in_range={a['in_range']} {a['warnings']}")
    paths = write_blocks(cal, args.out, n_blocks=args.blocks, trials_per_block=args.trials, seed=args.seed)
    for p in paths:
        print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
