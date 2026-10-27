#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SFT_WM_change.py: the readable single-file version of the SFT experiment (change variant): calibration (original adaptiveSFT, lnrm) -> practice -> main task; during calibration the targets of both dimensions are redrawn on every trial (sister script: SFT_WM_nochange.py).

    Run directly from Coder.                     real session
    python SFT_WM_change.py --robot             robot answers by itself, no window (tests the flow)
    python SFT_WM_change.py --robot --quick     robot + shortened fit + one block (finishes in minutes)

Outputs (all in data/):
    <subj>_simple_calib_trials.csv   every calibration trial (plain csv)
    <subj>_simple_calib.json         the calibrated H / L (make_adaptive_blocks.py can read it too)
    <subj>_simple_main.csv           one row per probe of the main task (adaptive_vawm.analyze_vawm can read it)
    <subj>_SFT_WM_<date>.csv / .psydat / .log   PsychoPy standard format (ExperimentHandler; all calibration + practice + main trials)
"""
import csv
import json
import os
import sys
import time

import numpy as np

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ROBOT = "--robot" in sys.argv
QUICK = "--quick" in sys.argv

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
LEVELS_COLOUR = [2.0, 6.0, 12.0, 20.0, 30.0, 45.0]
LEVELS_AUDIO = [-2.6, -2.1, -1.6, -1.1, -0.7, -0.3]
N_PER_LEVEL = 8
P_MATCH = 1 / 3
N_WARMUP = 8
N_FILLER = 24
H_TARG, L_TARG = 2.0, 0.5
FIT_KW = dict(tune=1000, draws=1000, chains=4, nuts_sampler="nutpie")
RT_MIN, RT_MAX = 0.15, 3.0
N_BLOCKS = 6
SETS_PER_BLOCK = 24
PROBES_PER_SET = 9
N_PRACTICE_SETS = 2
RESP_WINDOW = 3.0
OTHER_TARGETS_CHANGE = True
PROV_DE_H, PROV_DE_L = 30.0, 6.0
PROV_COUNT_H, PROV_COUNT_L = 10, 200
if QUICK:
    FIT_KW = dict(tune=300, draws=300, chains=2, nuts_sampler="nutpie")
    N_BLOCKS, SETS_PER_BLOCK, N_PRACTICE_SETS = 1, 3, 1

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
from adaptive_vawm_EN import (TALKERS, audio_x, count_from_x, delta_e, find_colour_at, foil_for,  # noqa: E402
                           from_model_units, lab_to_hex, load_confusion, load_full_package, random_target,
                           sound_file, to_model_units)
CONFUSION = load_confusion()
CONSONANTS = sorted(CONFUSION)
rng = np.random.default_rng()

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
if not ROBOT:
    from psychopy import core, event, gui, sound, visual
    from psychopy.hardware import keyboard

    # Audio output device: handled by audio_pick.py (list devices, open for real, prefer headphones).
    # On a new machine run `python audio_pick.py` first. Name the device with --audio-device "NAME",
    # the environment variable VAWM_AUDIO_DEVICE, or `python audio_pick.py --set "NAME"`.
    # --require-headphones stops instead of falling back to speakers; --list-audio only prints the devices.
    from audio_pick import setup_from_argv
    AUDIO = setup_from_argv(sys.argv)

    exp = {"participant": "", "session": "001"}
    if not gui.DlgFromDict(exp, title="VAWM simple").OK:
        core.quit()
    SUBJ = exp["participant"]
    exp["audio_device"] = AUDIO["name"]      # saved in every data row
    from psychopy import data as _pdata, logging as _plog
    thisExp = _pdata.ExperimentHandler(name="SFT_WM", extraInfo=dict(exp),
                                       dataFileName=f"data/{SUBJ}_SFT_WM_{_pdata.getDateStr()}",
                                       savePickle=True, saveWideText=True)
    _plog.LogFile(thisExp.dataFileName + ".log", level=_plog.EXP)
    win = visual.Window(fullscr=True, color="black", units="pix")
    fix = visual.TextStim(win, text="+", height=40, color="white")
    msg = visual.TextStim(win, text="", height=28, color="white", wrapWidth=1000,
                          alignText="left", anchorHoriz="center")
    patch_l = visual.Rect(win, width=100, height=100, pos=(-200, 0), colorSpace="hex", lineColor="#808080")
    patch_r = visual.Rect(win, width=100, height=100, pos=(200, 0), colorSpace="hex", lineColor="#808080")
    patch_c = visual.Rect(win, width=100, height=100, pos=(0, 0), colorSpace="hex", lineColor="#808080")
    snd = sound.Sound("A", secs=1, stereo=True, hamming=True)
    clock = core.Clock()
    kb = keyboard.Keyboard(clock=clock)

    def show(text):
        msg.text = text
        msg.draw()
        win.flip()
        if "escape" in event.waitKeys(keyList=["space", "escape"]):
            core.quit()

    def present(draw, secs, play=None):
        if play:
            snd.setSound(play, secs=1, hamming=True)
            snd.play()
        t0 = core.getTime()
        while core.getTime() - t0 < secs:
            if draw:
                draw()
            win.flip()
            if kb.getKeys(["escape"]):
                core.quit()
        if play:
            snd.stop()

    def study(c1, c2, s1, s2):
        """Study phase: fixation .3 → left colour 1 s → right colour 1 s → sound 1 → sound 2 (once per set in the main task, followed by 9 probes)."""
        present(fix.draw, 0.3)
        patch_l.fillColor = c1
        present(patch_l.draw, 1.0)
        patch_r.fillColor = c2
        present(patch_r.draw, 1.0)
        present(None, 1.0, play=s1)
        present(None, 1.0, play=s2)

    def probe_trial(probe_col, probe_snd):
        """Probe: fixation .3 → colour+sound 1 s → wait for y/n; returns (key, reaction time)."""
        present(fix.draw, 0.3)
        patch_c.fillColor = probe_col
        kb.clearEvents()
        clock.reset()
        present(patch_c.draw, 1.0, play=probe_snd)
        keys = kb.getKeys(["y", "n"], waitRelease=False)
        while not keys and clock.getTime() < RESP_WINDOW:
            win.flip()
            keys = kb.getKeys(["y", "n"], waitRelease=False)
            if kb.getKeys(["escape"]):
                core.quit()
        return (keys[0].name, keys[0].rt) if keys else (None, None)

    def one_trial(c1, c2, s1, s2, probe_col, probe_snd):
        """For calibration: one study + one probe (calibration re-studies on every trial)."""
        study(c1, c2, s1, s2)
        return probe_trial(probe_col, probe_snd)

    def feedback(text):
        msg.text = text
        present(msg.draw, 0.8)

    def record(row):
        for k, v in row.items():
            thisExp.addData(k, v)
        thisExp.nextEntry()

else:
    SUBJ = "robot"
    from scipy.stats import norm

    def show(text):
        print("[screen]", text.split("\n")[0])

    def record(row):
        pass

    def study(c1, c2, s1, s2):
        pass

    def probe_trial(probe_col, probe_snd, _info=None):
        return one_trial(None, None, None, None, probe_col, probe_snd, _info=_info)

    def feedback(text):
        pass

    load_full_package()
    from adaptivesft.race import lnrm_random

    def one_trial(c1, c2, s1, s2, probe_col, probe_snd, _info=None):
        dim, x, is_match, other = _info
        if other != "T":
            return ("y" if rng.uniform() < 0.10 else "n"), 0.9
        if is_match:
            return ("n" if rng.uniform() < 0.10 else "y"), 0.8
        u = to_model_units(dim, x)
        rt, correct = lnrm_random([1.0 * u - 0.12 * u * u], 1.0, 0.5, 0.2, rng)
        return ("n" if correct[0] == 1 else "y"), float(rt[0])

os.makedirs("data", exist_ok=True)


def write_csv(path, rows):
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def foil_near(cons, count):
    """Among the foil consonants of the target, the one whose confusion count is closest to count."""
    cands = CONFUSION[cons]
    return cands[int(np.argmin([abs(np.log10(c + 1) - np.log10(count + 1)) for _, c in cands]))][0]


def two_targets():
    """Draw two target colours (>= 20 ΔE apart), two different consonants, and one talker each."""
    t1 = random_target(rng)
    t2 = random_target(rng, avoid=[t1])
    s1, s2 = rng.choice(CONSONANTS, 2, replace=False)
    k1, k2 = rng.choice(TALKERS, 2)
    return t1, t2, str(s1), str(s2), str(k1), str(k2)

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
def run_calib_trial(dim, x, other, fixed, fixed_cols):
    """Run one calibration trial: draw targets, decide is_match / other, find the probe colour+sound, call one_trial; shared by the warm-up and the 72 real trials, returns one data row (without trial number)."""
    t1, t2, s1, s2, k1, k2 = two_targets()
    if not OTHER_TARGETS_CHANGE:
        if dim == "colour":
            s1, s2, k1, k2 = fixed[2], fixed[3], fixed[4], fixed[5]
        else:
            t1, t2 = fixed[0], fixed[1]
    which = int(rng.integers(2))
    target_col = [t1, t2][which]
    target_snd, talker = [s1, s2][which], [k1, k2][which]
    is_match = x is None
    answer_same = is_match and other == "T"
    if dim == "colour":
        if is_match:
            probe_lab = target_col
        else:
            probe_lab = find_colour_at(target_col, x, rng)
            if probe_lab is None:
                probe_lab = target_col
        x_actual = delta_e(target_col, probe_lab)
        probe_col = lab_to_hex(probe_lab)
        if other == "T":
            probe_snd = sound_file(talker, target_snd)
        else:
            probe_snd = sound_file(talker, foil_near(target_snd, PROV_COUNT_H if other == "H" else PROV_COUNT_L))
    else:
        if is_match:
            foil, count = target_snd, 0
        else:
            foil, count = foil_for(CONFUSION, target_snd, x)
        x_actual = audio_x(count)
        probe_snd = sound_file(talker, foil)
        if other == "T":
            probe_col = lab_to_hex(target_col)
        elif (which, other) in fixed_cols:
            probe_col = fixed_cols[(which, other)]
        else:
            lab = find_colour_at(target_col, PROV_DE_H if other == "H" else PROV_DE_L, rng)
            probe_col = lab_to_hex(lab if lab is not None else target_col)
    args = (lab_to_hex(t1), lab_to_hex(t2), sound_file(k1, s1), sound_file(k2, s2), probe_col, probe_snd)
    key, rt = one_trial(*args, _info=(dim, x_actual, answer_same, other)) if ROBOT else one_trial(*args)
    correct = None if key is None else int(key == ("y" if answer_same else "n"))
    return dict(dim=dim, is_match=int(is_match), x_planned=x, x=round(x_actual, 3), other=other,
                probe_col=probe_col, probe_snd=probe_snd, key=key, rt=rt, correct=correct)


def calibrate(dim, log_rows):
    levels = LEVELS_COLOUR if dim == "colour" else LEVELS_AUDIO
    easiest = levels[-1]
    warmup_plan = [(None, "T"), (easiest, "T")] * (N_WARMUP // 2)
    plan = [(x, "T") for x in levels for _ in range(N_PER_LEVEL)]
    plan += [(None, "T")] * int(round(len(plan) * P_MATCH / (1 - P_MATCH)))
    plan += [(rng.choice(levels + [None]), lev) for lev in ["H", "L"] * (N_FILLER // 2)]
    plan = [(None if x is None else float(x), o) for x, o in plan]
    rng.shuffle(plan)

    n_total = len(plan)
    show((f"Part 1 of 3: colour calibration ({n_total} trials)" if dim == "colour"
          else f"Part 2 of 3: sound calibration ({n_total} trials)") +
         "\n\nOn each trial you will first see two coloured squares and hear two speech sounds. "
         "Try to remember them. Then one colour will appear together with one sound.\n\n"
         "Did this colour AND this sound both appear a moment ago?\n"
         "   Y = yes, both of them did.      N = no, at least one of them is different.\n\n"
         f"First, {N_WARMUP} practice trials with feedback. Then {n_total} trials without feedback.\n\n"
         "Press the space bar to begin.")
    fixed = two_targets()
    fixed_cols = {}
    if not OTHER_TARGETS_CHANGE and dim == "audio":
        for wi, tcol in enumerate(fixed[:2]):
            for lev, de in (("H", PROV_DE_H), ("L", PROV_DE_L)):
                lab = find_colour_at(tcol, de, rng)
                fixed_cols[(wi, lev)] = lab_to_hex(lab if lab is not None else tcol)

    for i, (x, other) in enumerate(warmup_plan, 1):
        row = run_calib_trial(dim, x, other, fixed, fixed_cols)
        feedback("No response" if row["key"] is None else ("Correct" if row["correct"] else "Wrong"))
        record(dict(phase=f"warmup_{dim}", trial=i, is_match=row["is_match"], x=row["x"], other=row["other"],
                    key=row["key"], rt=row["rt"], correct=row["correct"]))
    show("Practice done. From now on there is no feedback.\n\nPress the space bar to continue.")

    for i, (x, other) in enumerate(plan, 1):
        row = run_calib_trial(dim, x, other, fixed, fixed_cols)
        log_rows.append(dict(dim=row["dim"], trial=i, is_match=row["is_match"], x_planned=row["x_planned"],
                             x=row["x"], other=row["other"], probe_col=row["probe_col"], probe_snd=row["probe_snd"],
                             key=row["key"], rt=row["rt"], correct=row["correct"]))
        write_csv(f"data/{SUBJ}_simple_calib_trials.csv", log_rows)
        record(dict(phase=f"calib_{dim}", **log_rows[-1]))

    if not ROBOT:
        msg.text = "Calculating... this takes about a minute. Please wait."
        msg.draw(); win.flip()
    else:
        print("  fitting...")
    load_full_package()
    from adaptivesft.models import make_data
    from adaptivesft.models_v2 import fit_lnrm_v2 as fit_lnrm   # PyMC built-in LogNormal logp/logcdf version (DECISIONS 14)
    from adaptivesft.salience import find_salience
    use = [r for r in log_rows if r["dim"] == dim and r["other"] == "T" and not r["is_match"] and r["key"] is not None
           and RT_MIN <= r["rt"] <= RT_MAX]
    data = make_data([to_model_units(dim, r["x"]) for r in use], [r["rt"] for r in use], [r["correct"] for r in use])
    t0 = time.time()
    trace = fit_lnrm(data, link="quadratic", **FIT_KW)
    res = find_salience(trace, h_targ=H_TARG, l_targ=L_TARG, alpha2_rule="filter")
    high = from_model_units(dim, res["high"]["intensity"])
    low = from_model_units(dim, res["low"]["intensity"])
    lo_lim, hi_lim = min(levels), max(levels)
    if not (np.isfinite(high) and np.isfinite(low)):
        print(f"  ⚠ [{dim}] the fit could not solve for H/L ({res['warnings']}); using middle levels for now; this participant's calibration must be redone")
        high, low = levels[-2], levels[1]
    in_range = bool(lo_lim <= low < high <= hi_lim)
    if not in_range:
        print(f"  ⚠ [{dim}] the fitted H={high:.2f} L={low:.2f} is outside the presentable range [{lo_lim}, {hi_lim}]; clipped; "
              "this participant's calibration must be redone or the data checked")
        high = float(np.clip(high, lo_lim, hi_lim))
        low = float(np.clip(low, lo_lim, hi_lim))
        if low >= high:
            low = lo_lim
    aa = [r["key"] == "n" for r in log_rows if r["dim"] == dim and r["other"] == "T" and r["is_match"] and r["key"] is not None]
    out = dict(dim=dim, high=float(high), low=float(low), in_range=in_range,
               false_alarm=float(np.mean(aa)) if aa else None,
               n_used=len(use), fit_seconds=round(time.time() - t0), warnings=list(res["warnings"]),
               extra=dict(method="lnrm_quadratic"))
    if dim == "audio":
        out["extra"]["count_high"] = float(count_from_x(high))
        out["extra"]["count_low"] = float(count_from_x(low))
    print(f"[{dim}] H={out['high']:.2f} L={out['low']:.2f} in_range={in_range} FA={out['false_alarm']} "
          f"fit {out['fit_seconds']}s {out['warnings']}")
    if not ROBOT and not in_range:
        show(f"Note for the experimenter: the {dim} calibration fell outside the tested range "
             "and was clipped. Please write this down.\n\nPress the space bar to continue.")
    return out

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
def make_study_set(calib):
    de_h, de_l = calib["colour"]["high"], calib["colour"]["low"]
    cnt_h, cnt_l = calib["audio"]["extra"]["count_high"], calib["audio"]["extra"]["count_low"]
    for _ in range(200):
        t1, t2, s1, s2, k1, k2 = two_targets()
        cols = [find_colour_at(t, de, rng) for t in (t1, t2) for de in (de_h, de_l)]
        if all(c is not None for c in cols):
            break
    else:
        raise RuntimeError("no in-gamut colours found at ΔE_H / ΔE_L")
    h1, l1, h2, l2 = cols

    return dict(
        color1_target=lab_to_hex(t1), color1_H=lab_to_hex(h1), color1_L=lab_to_hex(l1),
        color2_target=lab_to_hex(t2), color2_H=lab_to_hex(h2), color2_L=lab_to_hex(l2),
        audio1_target_file=sound_file(k1, s1), audio1_H_file=sound_file(k1, foil_near(s1, cnt_h)),
        audio1_L_file=sound_file(k1, foil_near(s1, cnt_l)),
        audio2_target_file=sound_file(k2, s2), audio2_H_file=sound_file(k2, foil_near(s2, cnt_h)),
        audio2_L_file=sound_file(k2, foil_near(s2, cnt_l)),
    )

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
COND = {
    0: ("AA", "color1_target", "audio1_target_file"), 1: ("AA", "color2_target", "audio2_target_file"),
    2: ("HA", "color1_target", "audio1_H_file"),      3: ("HA", "color2_target", "audio2_H_file"),
    4: ("LA", "color1_target", "audio1_L_file"),      5: ("LA", "color2_target", "audio2_L_file"),
    6: ("AH", "color1_H", "audio1_target_file"),      7: ("AH", "color2_H", "audio2_target_file"),
    8: ("HH", "color1_H", "audio1_H_file"),           9: ("HH", "color2_H", "audio2_H_file"),
    10: ("LH", "color1_L", "audio1_H_file"),          11: ("LH", "color2_L", "audio2_H_file"),
    12: ("AL", "color1_L", "audio1_target_file"),     13: ("AL", "color2_L", "audio2_target_file"),
    14: ("HL", "color1_H", "audio1_L_file"),          15: ("HL", "color2_H", "audio2_L_file"),
    16: ("LL", "color1_L", "audio1_L_file"),          17: ("LL", "color2_L", "audio2_L_file"),
}


def nine_probes():
    """The 9 probes of one set: 2 AA, 1 HA, 1 LA, 1 AH, 1 AL, 3 two-channel (HH/LH/HL/LL at random), shuffled."""
    c = [int(rng.choice([0, 1])) for _ in range(2)]
    c += [int(rng.choice([2, 3])), int(rng.choice([4, 5])), int(rng.choice([6, 7])), int(rng.choice([12, 13]))]
    c += [int(rng.choice([8, 9, 10, 11, 14, 15, 16, 17])) for _ in range(3)]
    rng.shuffle(c)
    return c


def run_sets(n_sets, block, calib, rows, with_feedback):
    for s in range(1, n_sets + 1):
        st = make_study_set(calib)
        study(st["color1_target"], st["color2_target"], st["audio1_target_file"], st["audio2_target_file"])
        for p, cond in enumerate(nine_probes(), 1):
            name, col_key, snd_key = COND[cond]
            probe_col, probe_snd = st[col_key], st[snd_key]
            key, rt = (probe_trial(probe_col, probe_snd, _info=("colour", 20.0 if name != "AA" else 0.0, name == "AA", "T"))
                       if ROBOT else probe_trial(probe_col, probe_snd))
            correct = None if key is None else int(key == ("y" if name == "AA" else "n"))
            if with_feedback:
                feedback("No response" if key is None else ("Correct" if correct else "Wrong"))
            row = dict(participant=SUBJ, block=block, set=s, probe=p, condition=cond, cond_name=name,
                       targetCol=probe_col, targetAud=probe_snd, correct=correct)
            row["ResponseBox.keys"] = key
            row["ResponseBox.rt"] = rt
            row.update(st)
            rows.append(row)
            write_csv(f"data/{SUBJ}_simple_main.csv", rows)
            record(dict(phase="practice" if block == 0 else "main", **row))

# ════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════
calib_rows = []
colour = calibrate("colour", calib_rows)
audio = calibrate("audio", calib_rows)
calib = dict(info=dict(participant=SUBJ, method="lnrm", h_targ=H_TARG, l_targ=L_TARG), colour=colour, audio=audio)
with open(f"data/{SUBJ}_simple_calib.json", "w", encoding="utf-8") as f:
    json.dump(calib, f, ensure_ascii=False, indent=2)

main_rows = []
show("Part 3 of 3: the main task. First, a short practice.\n\n"
     "Each round starts the same way: two colours and two sounds to remember. "
     "Then you will answer nine questions in a row, one colour-and-sound pair at a time.\n\n"
     "Both the same as before: press Y.   Anything different: press N.\n\n"
     "Feedback is shown during practice only.\n\nPress the space bar to begin.")
run_sets(N_PRACTICE_SETS, 0, calib, main_rows, with_feedback=True)
for b in range(1, N_BLOCKS + 1):
    show(f"Main task: block {b} of {N_BLOCKS}\n\nSame rules as the practice. There is no feedback from now on.\n\n"
         "Answer as accurately as you can; speed is not important.\n\nPress the space bar to begin.")
    run_sets(SETS_PER_BLOCK, b, calib, main_rows, with_feedback=False)
show("That is the end of the experiment. Thank you very much!\n\nPress the space bar to finish.")
print("done:", f"data/{SUBJ}_simple_calib.json", f"data/{SUBJ}_simple_main.csv")
if not ROBOT:
    thisExp.saveAsWideText(thisExp.dataFileName + ".csv")
    thisExp.saveAsPickle(thisExp.dataFileName)
    _plog.flush()
    win.close()
    core.quit()
