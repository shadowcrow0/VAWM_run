#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Calibration program for VAWM (run before VAWM_nobox.py): block 1 calibrates the colour distance, block 2 the consonant confusability, with the same task as VAWM_nobox.py and feedback after every trial; METHOD = "lnrm" (original adaptiveSFT, needs PyMC) or "psi" (Psi, numpy + scipy only); writes data/<participant>_calib.json, then:

    python make_adaptive_blocks.py data/<participant>_calib.json     # generates stimuli/block1..6.csv
    python VAWM_nobox.py                                              # main experiment as usual

Needs the adaptivesft package: pip install -e <path to adaptiveSFT>. In a container without PsychoPy this file has only been py_compiled.
Why the parameters have these values: DECISIONS.md.
"""
import csv
import os
import sys

from psychopy import core, data, event, gui, sound, visual
from psychopy.hardware import keyboard

# Audio output device: handled by audio_pick.py (list devices, open for real, prefer headphones).
# On a new machine run `python audio_pick.py` first. Name the device with --audio-device "NAME",
# the environment variable VAWM_AUDIO_DEVICE, or `python audio_pick.py --set "NAME"`.
# --require-headphones stops instead of falling back to speakers; --list-audio only prints the devices.
from audio_pick import setup_from_argv
AUDIO = setup_from_argv(sys.argv)


from adaptive_vawm_EN import LNRMCalibrator, PsiCalibrator, save_calibration

METHOD = "lnrm"
P_MATCH = 1 / 3
# lnrm
N_PER_LEVEL = 8
H_TARG, L_TARG = 2.0, 0.5
LINK = "quadratic"
FIT_KW = dict(tune=1000, draws=1000, chains=4,
              nuts_sampler="nutpie")
# psi
N_COLOUR = 72
N_AUDIO = 72
P_HIGH, P_LOW = 0.90, 0.75
RESP_KEYS = ["y", "n"]
RESP_WINDOW = 3.0
# ─────────────────────────────────

expInfo = {"participant": "", "session": "001"}
if not gui.DlgFromDict(expInfo, title="VAWM calibration").OK:
    core.quit()
subj = expInfo["participant"]
expInfo["audio_device"] = AUDIO["name"]      # saved in every data row
os.makedirs("data", exist_ok=True)
log_path = f"data/{subj}_calib_trials.csv"
from psychopy import logging as _plog
thisExp = data.ExperimentHandler(name="VAWM_calib", extraInfo=dict(expInfo),
                                 dataFileName=f"data/{subj}_VAWM_calib_{data.getDateStr()}",
                                 savePickle=True, saveWideText=True)
_plog.LogFile(thisExp.dataFileName + ".log", level=_plog.EXP)

win = visual.Window(fullscr=True, color="black", units="pix")
fix = visual.TextStim(win, text="+", height=40, color="white")
msg = visual.TextStim(win, text="", height=28, color="white", wrapWidth=1000)
patch_l = visual.Rect(win, width=100, height=100, pos=(-200, 0), colorSpace="hex", lineColor="#808080")
patch_r = visual.Rect(win, width=100, height=100, pos=(200, 0), colorSpace="hex", lineColor="#808080")
probe = visual.Rect(win, width=100, height=100, pos=(0, 0), colorSpace="hex", lineColor="#808080")
snd = sound.Sound("A", secs=1, stereo=True, hamming=True)
clock = core.Clock()
kb = keyboard.Keyboard(clock=clock)
rows = []


def save_trial_log():
    """Written after every trial, so a crash mid-way keeps the data."""
    columns = []
    for r in rows:
        for k in r:
            if k not in columns:
                columns.append(k)
    with open(log_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)


def show(text):
    msg.text = text
    msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=["space", "escape"])
    if "escape" in keys:
        core.quit()


def present(stim_draw, secs, play=None):
    """Draw stim_draw() for secs seconds (if play is a wav path, play it at the same time)."""
    if play:
        snd.setSound(play, secs=1, hamming=True)
        snd.play()
    t0 = core.getTime()
    while core.getTime() - t0 < secs:
        if stim_draw:
            stim_draw()
        win.flip()
        if kb.getKeys(["escape"]):
            core.quit()
    if play:
        snd.stop()


def run_trial(trial):
    present(fix.draw, 0.3)
    patch_l.fillColor = trial["color1_target"]
    present(patch_l.draw, 1.0)
    patch_r.fillColor = trial["color2_target"]
    present(patch_r.draw, 1.0)
    present(None, 1.0, play=trial["audio1_target_file"])
    present(None, 1.0, play=trial["audio2_target_file"])
    present(fix.draw, 0.3)
    probe.fillColor = trial["probe_colour"]
    kb.clearEvents()
    clock.reset()
    present(probe.draw, 1.0, play=trial["probe_sound"])
    keys = kb.getKeys(RESP_KEYS, waitRelease=False)
    while not keys and clock.getTime() < RESP_WINDOW:
        win.flip()
        keys = kb.getKeys(RESP_KEYS, waitRelease=False)
        if kb.getKeys(["escape"]):
            core.quit()
    if keys:
        return keys[0].name, keys[0].rt
    return None, None


def run_block(cal, n, title):
    show(f"{title}\n\nAfter you see a colour and hear a sound:\npress [y] if it is the same as the one you just memorised, [n] if it is different\n\nPress the space bar to begin")
    for i in range(n):
        trial = cal.next_trial()
        key, rt = run_trial(trial)
        r, correct = cal.record(key, rt)
        fb = "No response" if key is None else ("Correct" if correct else "Wrong")
        present(lambda: (setattr(msg, "text", fb), msg.draw()), 0.8)
        row = dict(cal.log[-1])
        row["block"] = cal.dim
        rows.append(row)
        save_trial_log()
        for k, v in row.items():
            thisExp.addData(k, v)
        thisExp.nextEntry()
    if METHOD == "lnrm":
        msg.text = "Calculating, please wait…"
        msg.draw()
        win.flip()
    res = cal.finish()
    print(f"[{cal.dim}] {res['extra']['method']} FA={res['false_alarm']:.2f} alpha={res['alpha']:.2f} "
          f"beta={res['beta']:.2f} H={res['high']:.2f} L={res['low']:.2f} in_range={res['in_range']} {res['warnings']}")
    if not res["in_range"]:
        show(f"Note: the {cal.dim} H/L fell outside the range\n{res['warnings']}\n\nPress the space bar to continue")
    return res


seed = int(subj) if subj.isdigit() else abs(hash(subj)) % 2**32
if METHOD == "lnrm":
    cal_c = LNRMCalibrator("colour", n_per_level=N_PER_LEVEL, p_match=P_MATCH, h_targ=H_TARG, l_targ=L_TARG,
                           link=LINK, seed=seed, **FIT_KW)
    cal_a = LNRMCalibrator("audio", n_per_level=N_PER_LEVEL, p_match=P_MATCH, h_targ=H_TARG, l_targ=L_TARG,
                           link=LINK, seed=seed + 1, **FIT_KW)
    n_c, n_a = cal_c.n_trials, cal_a.n_trials
elif METHOD == "psi":
    cal_c = PsiCalibrator("colour", p_high=P_HIGH, p_low=P_LOW, p_match=P_MATCH, seed=seed)
    cal_a = PsiCalibrator("audio", p_high=P_HIGH, p_low=P_LOW, p_match=P_MATCH, seed=seed + 1)
    n_c, n_a = N_COLOUR, N_AUDIO
else:
    raise ValueError(f"METHOD must be 'lnrm' or 'psi', got {METHOD!r}")
colour = run_block(cal_c, n_c, "Block 1: colour")
audio = run_block(cal_a, n_a, "Block 2: sound")
out = f"data/{subj}_calib.json"
save_calibration(out, colour, audio, info=dict(expInfo, date=data.getDateStr(), method=METHOD, n_colour=n_c, n_audio=n_a))
thisExp.saveAsWideText(thisExp.dataFileName + ".csv")
thisExp.saveAsPickle(thisExp.dataFileName)
_plog.flush()
show(f"Calibration finished.\n\n{out}\nNext run make_adaptive_blocks.py, then VAWM_nobox.py\n\nPress the space bar to finish")
win.close()
core.quit()
