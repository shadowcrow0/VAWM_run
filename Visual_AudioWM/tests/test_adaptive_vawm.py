"""adaptive_vawm.py 的測試：模擬受試者跑完校準 → H/L 合理；block csv 欄位與 practice.csv 相同；VAWM 輸出 → SIC 分析。"""
import csv
import os
import sys

import numpy as np
import pytest
from scipy.stats import norm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from adaptive_vawm import (CSV_COLUMNS, LNRMCalibrator, PsiCalibrator, audio_x, count_from_x, delta_e,  # noqa: E402
                           find_colour_at, is_in_gamut, lab_to_hex, load_confusion, load_full_package,
                           random_target, read_calibration, save_calibration, to_model_units, write_blocks)


def test_colour_helpers():
    rng = np.random.default_rng(0)
    t = random_target(rng)
    assert is_in_gamut(t) and lab_to_hex(t).startswith("#") and len(lab_to_hex(t)) == 7
    f = find_colour_at(t, 25.0, rng)
    assert f is not None and abs(delta_e(t, f) - 25.0) <= 0.5
    assert lab_to_hex([50, 0, 0]) in ("#767676", "#777777")                     # 中性灰（int() 截尾同 colorpool）


def test_confusion_table_and_axis():
    conf = load_confusion()
    assert len(conf) == 16 and ("k", 207) in conf["p"]                          # generate_trials.py 的第一列
    assert audio_x(1) > audio_x(451) and abs(count_from_x(audio_x(91)) - 91) < 1e-9


# ---------------------------------------------------------------- Psi 版：模擬一個「答不同」機率服從累積常態的受試者

def psi_observer(alpha, beta, fa, lapse=0.02):
    def respond(trial, rng):
        if trial["is_match"]:
            p_say_different = fa
        else:
            p_say_different = fa + (1 - fa - lapse) * norm.cdf(trial["x"], alpha, beta)
        return "n" if rng.uniform() < p_say_different else "y"
    return respond


def test_psi_colour_recovers_observer():
    rng = np.random.default_rng(1)
    respond = psi_observer(alpha=12.0, beta=8.0, fa=0.15)
    cal = PsiCalibrator("colour", p_high=0.90, p_low=0.75, p_match=1 / 3, seed=1)
    for _ in range(120):
        t = cal.next_trial()
        assert {"color1_target", "color2_target", "audio1_target_file", "probe_colour", "probe_sound"} <= set(t)
        cal.record(respond(t, rng), 0.6)
    res = cal.finish()
    assert res["dim"] == "colour" and res["n_match"] > 20 and res["extra"]["method"] == "psi"
    assert abs(res["false_alarm"] - 0.15) < 0.12
    assert abs(res["alpha"] - 12) < 5 and abs(res["beta"] - 8) < 5
    assert res["low"] < res["high"] and res["in_range"]
    x_high_true = 12 + 8 * norm.ppf((0.90 - 0.15) / 0.83)
    assert abs(res["high"] - x_high_true) < 8


def test_psi_audio_snaps_to_available_foils():
    rng = np.random.default_rng(2)
    respond = psi_observer(alpha=-1.0, beta=0.6, fa=0.1)
    cal = PsiCalibrator("audio", p_high=0.90, p_low=0.75, p_match=1 / 3, seed=2)
    conf = load_confusion()
    for _ in range(120):
        t = cal.next_trial()
        if not t["is_match"]:
            target_file = t["audio1_target_file"] if t["probe_of"] == 1 else t["audio2_target_file"]
            target_cons = os.path.basename(target_file).split("_")[1][:-5]
            assert (t["foil"], t["count"]) in conf[target_cons]                # foil 一定是該子音表裡的
            assert abs(t["x"] - audio_x(t["count"])) < 1e-12
        cal.record(respond(t, rng), 0.7)
    res = cal.finish()
    assert res["dim"] == "audio" and abs(res["alpha"] + 1.0) < 0.6
    assert res["extra"]["count_high"] < res["extra"]["count_low"]              # H = 不易混淆 = 次數少


def test_record_validation_and_no_response():
    cal = PsiCalibrator("colour", seed=3)
    with pytest.raises(RuntimeError):
        cal.record("y", 0.5)
    cal.next_trial()
    with pytest.raises(ValueError):
        cal.record("x", 0.5)
    r, c = cal.record(None, None)
    assert r is None and c is None and cal.log[-1]["key"] is None


# ---------------------------------------------------------------- lnrm 版：模擬一個 LNRM 賽跑受試者（要 PyMC）

def lnrm_observer(d_of_u, dim, fa=0.1, mu=1.0, varZ=0.5, psi=0.2):
    """d_of_u：模型單位的 u → 難度 d。不同試用 adaptivesft.race.lnrm_random 抽 (rt, correct)。"""
    load_full_package()
    from adaptivesft.race import lnrm_random

    def respond(trial, rng):
        if trial["is_match"]:
            key = "n" if rng.uniform() < fa else "y"
            return key, 0.8
        u = to_model_units(dim, trial["x"])
        rt, correct = lnrm_random([d_of_u(u)], mu, varZ, psi, rng)
        key = "n" if correct[0] == 1 else "y"
        return key, float(rt[0])
    return respond


@pytest.mark.parametrize("dim", ["colour", "audio"])
def test_lnrm_quadratic_recovers_and_matches_r_inversion(dim):
    """定值刺激法 + lnrm2 + 反解漂移差：回復 α/α₂，H/L 與 R 公式在後驗平均上的反解一致，H > L，在範圍內。"""
    pytest.importorskip("pymc")
    rng = np.random.default_rng(11)
    alpha, alpha2 = 1.0, -0.12
    cal = LNRMCalibrator(dim, n_per_level=12, seed=11, tune=400, draws=400, chains=2)
    respond = lnrm_observer(lambda u: alpha * u + alpha2 * u * u, dim)
    assert cal.n_trials == 6 * 12 + 36
    for _ in range(cal.n_trials):
        t = cal.next_trial()
        assert {"probe_colour", "probe_sound", "is_match"} <= set(t)
        cal.record(*respond(t, rng))
    with pytest.raises(StopIteration):
        cal.next_trial()
    res = cal.finish()
    assert res["dim"] == dim and res["extra"]["method"] == "lnrm_quadratic" and res["n_match"] == 36
    assert abs(res["alpha"] - alpha) < 0.5 and abs(res["beta"] - alpha2) < 0.15
    assert res["extra"]["divergences"] < 20
    # 2·d(u) = targ 的較小根（adaptiveSFT_functions.R:229-232）
    a, a2 = res["alpha"], res["beta"]
    u_high = (-a / a2 - np.sqrt((a / a2) ** 2 + 2 / a2 * cal.h_targ)) / 2
    assert abs(to_model_units(dim, res["high"]) - u_high) < 0.15
    assert res["low"] < res["high"] and res["in_range"]
    if dim == "audio":
        assert res["extra"]["count_high"] < res["extra"]["count_low"]


def test_lnrm_ogival_link_decision_b():
    """link="ogival"（決定 B：½L·inv_logit、L = 10 固定）配 Houpt 的 8.0 / 1.3：回復 slope / midpoint，H/L 對上閉式反解。"""
    pytest.importorskip("pymc")
    rng = np.random.default_rng(6)
    slope, mid, L = 2.0, 1.5, 10.0
    cal = LNRMCalibrator("colour", n_per_level=12, seed=6, link="ogival", h_targ=8.0, l_targ=1.3,
                         tune=400, draws=400, chains=2)
    respond = lnrm_observer(lambda u: 0.5 * L / (1 + np.exp(-slope * (u - mid))), "colour")
    for _ in range(cal.n_trials):
        cal.record(*respond(cal.next_trial(), rng))
    res = cal.finish()
    p = res["extra"]["params"]
    assert res["extra"]["method"] == "lnrm_ogival" and abs(p["slope"] - slope) < 0.6 and abs(p["midpoint"] - mid) < 0.3

    def invert(targ):                                                           # adaptiveSFT_functions.R:180-199
        return (np.log((targ / L) / (1 - targ / L)) / slope + mid) * 10
    assert abs(res["high"] - invert(8.0)) < 3 and abs(res["low"] - invert(1.3)) < 3 and res["in_range"]


# ---------------------------------------------------------------- block csv 與分析

def test_write_blocks_matches_practice_csv_layout(tmp_path):
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(here, "stimuli", "practice.csv"), newline="", encoding="utf-8-sig") as f:
        practice_cols = next(csv.reader(f))
    assert practice_cols == CSV_COLUMNS
    # 假的校準結果：ΔE_H 30、ΔE_L 20；count_H 1、count_L 90
    colour = dict(dim="colour", high=30.0, low=20.0, extra=dict(method="psi"))
    audio = dict(dim="audio", high=-0.3, low=-1.96, extra=dict(method="psi", count_high=1.0, count_low=90.0))
    path = tmp_path / "S_calib.json"
    save_calibration(path, colour, audio, info={"participant": "S"})
    cal = read_calibration(path)
    paths = write_blocks(cal, tmp_path / "stimuli", n_blocks=2, trials_per_block=5, seed=7)
    assert [os.path.basename(p) for p in paths] == ["block1.csv", "block2.csv"]
    with open(paths[0], newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0].keys()) == CSV_COLUMNS and len(rows) == 5
    for r in rows:
        assert abs(float(r["color1_H_deltaE"]) - 30) <= 0.5 and abs(float(r["color1_L_deltaE"]) - 20) <= 0.5
        assert int(r["audio1_H_count"]) <= int(r["audio1_L_count"])
        assert r["audio1_H_file"].startswith("stimuli/T") and r["audio1_H_file"].endswith("3.wav")
        assert r["audio1_target_talker"] == r["audio1_H_talker"] == r["audio1_L_talker"]


def test_vawm_csv_to_dfp_analysis(tmp_path):
    """假造一份 VAWM_nobox.py 格式的輸出（每個探測一列），PAR-OR 的 DDM 填 RT → 判 ParallelOR。要 PyMC。"""
    pytest.importorskip("pymc")
    from adaptive_vawm import analyze_vawm, vawm_to_dfp_rows
    load_full_package()
    from adaptivesft.ddm import dfp_ddm
    rng = np.random.default_rng(9)
    drift = {2: 3.0, 1: 1.0}
    cell = {8: (2, 2), 9: (2, 2), 14: (2, 1), 15: (2, 1), 10: (1, 2), 11: (1, 2), 16: (1, 1), 17: (1, 1)}
    recs = []
    for cond in list(range(18)) * 40:
        if cond in cell:
            c1, c2 = cell[cond]
            rt, correct = dfp_ddm(1, drift[c1], drift[c2], 3.0, 0.1, 0.2, "PAR", "OR", rng=rng)
            key = "n" if correct[0] == 1 else "y"
            rt = float(rt[0])
        else:
            key = "y" if cond in (0, 1) else "n"
            rt = 0.8
        recs.append({"participant": "S9", "condition": cond, "ResponseBox.keys": key, "ResponseBox.rt": rt, "block1.thisN": 0})
    path = tmp_path / "S9_VAWM.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
        w.writeheader()
        w.writerows(recs)
    rows, others = vawm_to_dfp_rows(path)
    assert len(rows) == 8 * 40 and len(others) == 10 * 40 and rows[0]["subject"] == "S9"
    out = analyze_vawm(path)
    assert out["n_dfp"] == 320 and out["accuracy_other"][0] == 1.0
    assert out["result"]["DFP"]["classification"]["Predicted_by"] == "ParallelOR"
    assert "ParallelOR" in out["report"]
