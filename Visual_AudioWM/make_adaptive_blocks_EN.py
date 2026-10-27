"""
Calibration result → stimuli/block1..6.csv (same columns as practice.csv); afterwards VAWM_nobox.py runs as usual. Prints the calibrated values first (colour ΔE_H / ΔE_L, sound count_H / count_L, false-alarm rate) and warns when H/L fall outside the range but still writes the files.

    python make_adaptive_blocks.py data/<participant>_calib.json
    python make_adaptive_blocks.py data/<participant>_calib.json --out stimuli --blocks 6 --trials 24 --seed 1
"""
import argparse

from adaptive_vawm_EN import read_calibration, write_blocks


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("calib_json")
    ap.add_argument("--out", default="stimuli")
    ap.add_argument("--blocks", type=int, default=6)
    ap.add_argument("--trials", type=int, default=24, help="study sets per block (each set has 9 probes, as in VAWM_nobox)")
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
