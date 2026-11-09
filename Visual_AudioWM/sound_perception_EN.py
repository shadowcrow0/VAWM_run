"""
sound_perception_EN.py: a pure perception test of the consonant stimuli, no memory load.

    Each trial: syllable 1 (0.6 s)  ->  0.5 s silence  ->  syllable 2 (0.6 s)  ->  "same consonant?"  y / n
    Same talker on both syllables; "same" plays the identical file. Feedback after every trial.
    "Different" pairs are chosen exactly as in the experiment (foil_for on the Miller-Nicely confusion counts)
    at the six levels of LEVELS_AUDIO, N_PER_LEVEL each, plus 1/3 "same" trials.

Why: in the 2026-11-03 pilot the sound dimension sat at chance inside the working-memory task even for the most
dissimilar pairs. This test asks whether the pairs are discriminable at all when nothing has to be remembered:
if the most dissimilar level reaches ~90 % here, the problem is the memory load; if it does not, it is the stimuli.

    python sound_perception_EN.py                 ~6 minutes (108 trials), confusion-count axis (as in the experiment)
    python sound_perception_EN.py --axis features  Miller-Nicely feature distance 1..5 as the axis (5 levels x 14 + 35 same)
    python sound_perception_EN.py --robot         simulated listener, no window (tests the flow)
    python sound_perception_EN.py --audio-device "Headphones"      (or audio_pick.py --set, see README_RUN.md)

Output: data/<id>_sound_perception.csv (one row per trial) and data/<id>_sound_perception.json (accuracy and
median RT per level, false-alarm rate, d' per level), also printed at the end.
"""
import csv
import json
import math
import os
import sys

import numpy as np

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ROBOT = "--robot" in sys.argv

from adaptive_vawm_EN import (LEVELS_AUDIO, TALKERS, audio_x, feature_distance, foil_for,  # noqa: E402
                              foils_at_distance, load_confusion, sound_file)

AXIS = "features" if "--axis" in sys.argv and sys.argv[sys.argv.index("--axis") + 1] == "features" else "counts"

N_PER_LEVEL = 12 if AXIS == "counts" else 14      # counts: 6 levels x 12 = 72; features: 5 levels x 14 = 70
P_SAME = 1 / 3            # plus 1/3 "same" trials -> 108 / 105 in all
LEVELS = LEVELS_AUDIO if AXIS == "counts" else [1, 2, 3, 4, 5]     # feature distance: 1 = e.g. p-b, 5 = s-m
ISI = 0.5                 # silence between the two syllables
RESP_WINDOW = 3.0         # seconds to answer after the second syllable ends
FEEDBACK = 0.6

CONFUSION = load_confusion()
CONSONANTS = sorted(CONFUSION)
rng = np.random.default_rng()


def make_plan():
    plan = [(x, False) for x in LEVELS for _ in range(N_PER_LEVEL)]
    plan += [(None, True)] * int(round(len(plan) * P_SAME / (1 - P_SAME)))
    rng.shuffle(plan)
    trials = []
    for x, same in plan:
        cons = CONSONANTS[int(rng.integers(len(CONSONANTS)))]
        talker = TALKERS[int(rng.integers(len(TALKERS)))]
        if same:
            foil, count, x_actual = cons, None, None
        elif AXIS == "counts":
            foil, count = foil_for(CONFUSION, cons, x)
            x_actual = audio_x(count)
        else:
            cands = foils_at_distance(cons, x)
            while not cands:                                   # not every consonant has a partner at every distance
                cons = CONSONANTS[int(rng.integers(len(CONSONANTS)))]
                cands = foils_at_distance(cons, x)
            foil, count, x_actual = cands[int(rng.integers(len(cands)))], None, x
        trials.append(dict(axis=AXIS, is_same=int(same), x_planned=x, x=x_actual, consonant=cons, foil=foil, count=count,
                           feature_distance=None if same else feature_distance(cons, foil),
                           talker=talker, snd1=sound_file(talker, cons), snd2=sound_file(talker, foil)))
    return trials


if not ROBOT:
    from psychopy import core, event, gui, sound, visual
    from psychopy.hardware import keyboard
    from audio_pick import setup_from_argv
    AUDIO = setup_from_argv(sys.argv)

    exp = {"participant": ""}
    if not gui.DlgFromDict(exp, title="Sound perception test").OK:
        core.quit()
    SUBJ = exp["participant"]
    win = visual.Window(fullscr=True, color="black", units="pix")
    fix = visual.TextStim(win, text="+", height=40, color="white")
    msg = visual.TextStim(win, text="", height=28, color="white", wrapWidth=1000, alignText="left", anchorHoriz="center")
    snd = sound.Sound("A", secs=1, stereo=True, hamming=True)
    clock = core.Clock()
    kb = keyboard.Keyboard(clock=clock)

    def show(text):
        msg.text = text
        msg.draw()
        win.flip()
        if "escape" in event.waitKeys(keyList=["space", "escape"]):
            core.quit()

    def play(path, secs):
        snd.setSound(path, secs=1, hamming=True)
        snd.play()
        t0 = core.getTime()
        while core.getTime() - t0 < secs:
            fix.draw()
            win.flip()
            if kb.getKeys(["escape"]):
                core.quit()
        snd.stop()

    def resp_keys():
        keys = kb.getKeys(["y", "n"], waitRelease=False) + kb.getKeys(["y", "n"], waitRelease=True)
        return sorted(keys, key=lambda k: k.rt)

    def one_trial(t):
        play(t["snd1"], 0.7)
        t0 = core.getTime()
        while core.getTime() - t0 < ISI:
            fix.draw()
            win.flip()
        kb.clearEvents()
        clock.reset()                      # RT from the onset of syllable 2
        play(t["snd2"], 0.7)
        keys = resp_keys()
        while not keys and clock.getTime() < RESP_WINDOW:
            fix.draw()
            win.flip()
            keys = resp_keys()
            if kb.getKeys(["escape"]):
                core.quit()
        if not keys:
            return None, None
        return keys[0].name, keys[0].rt

    def feedback(text):
        msg.text = text
        t0 = core.getTime()
        while core.getTime() - t0 < FEEDBACK:
            msg.draw()
            win.flip()
else:
    SUBJ = "robot"

    def show(text):
        print("[screen]", text.split("\n")[0])

    def one_trial(t):
        # simulated listener: P(say "different") rises with dissimilarity; 10 % false alarms on same trials
        if t["is_same"]:
            return ("n" if rng.uniform() < 0.10 else "y"), 0.6 + rng.exponential(0.2)
        p_diff = 1 / (1 + math.exp(-3.0 * (t["x"] + 1.4))) if AXIS == "counts" else 1 / (1 + math.exp(-1.5 * (t["x"] - 2.5)))
        return ("n" if rng.uniform() < p_diff else "y"), 0.6 + rng.exponential(0.3)

    def feedback(text):
        pass


trials = make_plan()
show(f"Sound test ({len(trials)} trials, about 6 minutes)\n\n"
     "You will hear two syllables, one after the other.\n\n"
     "Is the CONSONANT the same in both?\n"
     "   Y = same      N = different\n\n"
     "Answer after the second syllable, as quickly as you can, on every trial. "
     "You will see whether you were right.\n\nPress the space bar to begin.")

rows = []
for i, t in enumerate(trials, 1):
    key, rt = one_trial(t)
    correct = None if key is None else int(key == ("y" if t["is_same"] else "n"))
    feedback("No response" if key is None else ("Correct" if correct else "Wrong"))
    rows.append(dict(participant=SUBJ, trial=i, **t, key=key, rt=rt, correct=correct))

os.makedirs("data", exist_ok=True)
path = f"data/{SUBJ}_sound_perception{'' if AXIS == 'counts' else '_features'}.csv"
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

# summary: hit rate per level, false alarms on same trials, d' per level (Macmillan & Creelman, with 1/(2N) correction)
def z(p, n):
    p = min(max(p, 0.5 / n), 1 - 0.5 / n)
    return math.sqrt(2) * _erfinv(2 * p - 1)


def _erfinv(y):
    from scipy.special import erfinv
    return float(erfinv(y))


same = [r for r in rows if r["is_same"] and r["key"] is not None]
fa = sum(1 for r in same if r["key"] == "n") / max(len(same), 1)
summary = dict(participant=SUBJ, axis=AXIS, n_trials=len(rows), n_no_response=sum(1 for r in rows if r["key"] is None),
               same_trials=len(same), false_alarm=fa, levels={})
print(f"\n{SUBJ}: {len(rows)} trials, no response {summary['n_no_response']}, false alarm (same trials) {fa:.2f}")
print(f"  axis = {AXIS} ({'confusion counts, -log10(count+1)' if AXIS == 'counts' else 'number of differing Miller-Nicely features'})")
print(f"  {'level x':>8} {'n':>3} {'hit':>5} {'d-prime':>8} {'median RT':>10}")
for x in LEVELS:
    sub = [r for r in rows if not r["is_same"] and r["x_planned"] == x and r["key"] is not None]
    if not sub:
        continue
    hit = sum(r["correct"] for r in sub) / len(sub)
    dprime = z(hit, len(sub)) - z(fa, max(len(same), 1))
    rts = sorted(r["rt"] for r in sub)
    med = rts[len(rts) // 2]
    summary["levels"][str(x)] = dict(n=len(sub), hit=hit, dprime=dprime, median_rt=med)
    print(f"  {x:>8} {len(sub):>3} {hit:>5.2f} {dprime:>8.2f} {med:>10.2f}")
with open(path.replace(".csv", ".json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
print("done:", path)
if not ROBOT:
    show("Done. Thank you!\n\nPress the space bar to exit.")
    win.close()
    core.quit()
