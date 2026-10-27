#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
debug_adaptivesft.py: one-click diagnosis of the whole adaptiveSFT calibration chain from inside PsychoPy Coder (open this file in Coder and Run; no arguments, every switch is in the settings section below): 0 environment, 1 find the adaptiveSFT fork, 2 import adaptive_vawm, 3 METHOD capability check, 4 windowless Psi simulation, 5 shortened LNRM fit (PyMC only), 6 a few real trials in a small window (RUN_WINDOW_TRIALS > 0 only); every failure prints why and how to fix it.
"""
import os
import sys
import time
import traceback

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

N_SIM = 48
SIM_SEED = 7
RUN_WINDOW_TRIALS = 0
WINDOW_DIM = "colour"
TRY_LNRM = True
LNRM_FIT_KW = dict(tune=200, draws=200, chains=1, nuts_sampler="nutpie")
KNOWN_FORK_PATHS = [
    r"C:\Users\spt904\OneDrive - University of Texas at San Antonio\Desktop\adaptiveSFT",
    "/mnt/c/Users/spt904/OneDrive - University of Texas at San Antonio/Desktop/adaptiveSFT",
]
# ────────────────────────────────────────────────────────────────

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
W = 72


def hdr(n, title):
    print("\n" + "=" * W)
    print(f"[{n}] {title}")
    print("=" * W)


def ok(msg):
    print("  ✔ " + msg)


def bad(msg):
    print("  ✘ " + msg)


def fix(msg):
    print("    → fix: " + msg)


hdr(0, "environment")
print(f"  Python   {sys.version.split()[0]}  ({sys.executable})")
print(f"  cwd      {os.getcwd()}")
import site as _site
print(f"  user-site {_site.getusersitepackages()}  in sys.path: {_site.getusersitepackages() in sys.path}"
      f"  (started with python -s: {bool(sys.flags.no_user_site)})")
try:
    import numpy as np
    import scipy
    ok(f"numpy {np.__version__}  scipy {scipy.__version__}")
except Exception as e:
    bad(f"numpy/scipy failed to load: {e}")
    raise SystemExit
try:
    import psychopy
    ok(f"psychopy {psychopy.__version__}")
    HAVE_PSYCHOPY = True
except Exception as e:
    bad(f"psychopy is not in this Python ({type(e).__name__}) — step 6 will be skipped")
    HAVE_PSYCHOPY = False
try:
    import pymc
    ok(f"pymc {pymc.__version__} (lnrm fit available)")
    HAVE_PYMC = True
except Exception as e:
    bad(f"pymc missing ({type(e).__name__}) → METHOD='lnrm' will crash after the 72 trials, at the 'Calculating' screen")
    fix("in this PsychoPy Coder environment only METHOD='psi' works; for lnrm set up the conda environment as described in adaptive_vawm.md")
    HAVE_PYMC = False
for f in ("adaptive_vawm.py", "generate_trials.py", "stimuli/T01_b3.wav", "stimuli/T12_p3.wav"):
    (ok if os.path.exists(f) else bad)(f"{f}")

hdr(1, "find the adaptiveSFT fork (must contain adaptivesft/psi.py)")
cands = []
if os.environ.get("ADAPTIVESFT_PATH"):
    cands.append(("env var ADAPTIVESFT_PATH", os.environ["ADAPTIVESFT_PATH"]))
cands.append(("sibling ../adaptiveSFT", os.path.join(os.path.dirname(HERE), "adaptiveSFT")))
cands += [("known location", p) for p in KNOWN_FORK_PATHS]
found = None
for label, p in cands:
    has_psi = os.path.isfile(os.path.join(p, "adaptivesft", "psi.py"))
    exists = os.path.isdir(p)
    if has_psi:
        ok(f"{label}: {p}")
        if found is None:
            found = p
    elif exists:
        hint = ""
        if os.path.isfile(os.path.join(p, "adaptiveSFT_functions.R")) and not os.path.isdir(os.path.join(p, "adaptivesft")):
            hint = "  ← this is Houpt's original (R/Stan), not the shadowcrow0 fork"
        bad(f"{label}: {p} exists but has no adaptivesft/psi.py{hint}")
    else:
        print(f"  · {label}: {p} (does not exist)")
if found is None:
    bad("no location has adaptivesft/psi.py")
    fix("git clone https://github.com/shadowcrow0/adaptiveSFT.git next to this repo, "
        "or add its path to KNOWN_FORK_PATHS in this file, or set the env var ADAPTIVESFT_PATH")
    raise SystemExit
if not os.environ.get("ADAPTIVESFT_PATH"):
    os.environ["ADAPTIVESFT_PATH"] = found
    print(f"  (ADAPTIVESFT_PATH = {found} set automatically for this run)")
try:
    import subprocess
    sha = subprocess.run(["git", "-C", found, "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip()
    print(f"  fork version: {sha or '(not a git repo)'}")
except Exception:
    pass

# ───────────────────────────── 2. import adaptive_vawm ─────────────────────────────
hdr(2, "import adaptive_vawm")
try:
    import adaptive_vawm_EN as A
    _psi_src = getattr(getattr(A, "psi_module", None), "__file__", "(old version: no psi_module attribute)")
    ok(f"import OK; psi.py comes from {_psi_src}")
except Exception:
    bad("import adaptive_vawm failed:")
    traceback.print_exc()
    raise SystemExit
if not hasattr(A, "PsiCalibrator"):
    bad("this adaptive_vawm.py is the old API (has ColourCalibrator/AudioCalibrator, no PsiCalibrator/LNRMCalibrator)")
    print(f"    file: {A.__file__}")
    fix("this folder is not the latest GitHub main (a ZIP from before 2026-10-02). "
        "re-clone / download main into a new folder and run again; save a copy of any hand-edited VAWM_calibrate.py in the old folder first")
    raise SystemExit
for name in ("next_intensity", "update_at", "nearest_index", "estimate"):
    (ok if hasattr(A.Psi, name) or name == "next_intensity" else bad)(f"Psi.{name}")
try:
    conf = A.load_confusion()
    ok(f"confusion table: {len(conf)} consonants (from generate_trials.py)")
except Exception as e:
    bad(f"load_confusion failed: {e}")
    raise SystemExit

hdr(3, "METHOD capability check")
ok("psi: needs only psi.py + numpy + scipy → available")
LNRM_OK = False
try:
    A.load_full_package()
    from adaptivesft.models_v2 import fit_lnrm_v2      # noqa: F401
    from adaptivesft.salience import find_salience  # noqa: F401
    ok("lnrm: full adaptivesft package + PyMC present → available")
    LNRM_OK = True
except Exception as e:
    bad(f"lnrm: {type(e).__name__}: {str(e)[:90]}")
    fix("change METHOD = \"lnrm\" to \"psi\" on line 73 of VAWM_calibrate.py, or run in an environment that has PyMC")

hdr(4, f"windowless simulation: PsiCalibrator, {N_SIM} trials per dimension")
from scipy.stats import norm


def psi_observer(alpha, beta, fa, lapse=0.02):
    """Simulated participant: P(answer 'different' | x) = fa + (1 − fa − lapse)·Φ((x − α)/β)."""
    def respond(trial, rng):
        p = fa if trial["is_match"] else fa + (1 - fa - lapse) * norm.cdf(trial["x"], alpha, beta)
        return "n" if rng.uniform() < p else "y"
    return respond


TRUE = {"colour": dict(alpha=12.0, beta=8.0, fa=0.15),
        "audio": dict(alpha=-1.5, beta=0.6, fa=0.15)}
missing_wavs = set()
sim_results = {}
for dim in ("colour", "audio"):
    print(f"\n  ── {dim}  true α={TRUE[dim]['alpha']} β={TRUE[dim]['beta']} FA={TRUE[dim]['fa']} ──")
    rng = np.random.default_rng(SIM_SEED)
    respond = psi_observer(**TRUE[dim])
    try:
        cal = A.PsiCalibrator(dim, p_high=0.90, p_low=0.75, p_match=1 / 3, seed=SIM_SEED)
    except Exception:
        bad("PsiCalibrator could not be created:")
        traceback.print_exc()
        continue
    print(f"  {'#':>3} {'x_psi':>7} {'x':>7} {'AA':>3} {'key':>3} {'r':>2} {'ok':>2} {'α̂':>7} {'β̂':>6}  probe_sound")
    t0 = time.time()
    for _ in range(N_SIM):
        t = cal.next_trial()
        for k in ("audio1_target_file", "audio2_target_file", "probe_sound"):
            if not os.path.exists(t[k]):
                missing_wavs.add(t[k])
        key = respond(t, rng)
        r, c = cal.record(key, 0.6)
        a_hat, b_hat = cal.psi.estimate()
        print(f"  {t['trial_no']:>3} {t['x_psi']:>7.2f} {t['x']:>7.2f} {'AA' if t['is_match'] else '  ':>3} "
              f"{key:>3} {str(r):>2} {str(c):>2} {a_hat:>7.2f} {b_hat:>6.2f}  {t['probe_sound']}")
    try:
        res = cal.finish()
        sim_results[dim] = res
        print(f"  finish(): α̂={res['alpha']:.2f} β̂={res['beta']:.2f} FA={res['false_alarm']:.2f}  "
              f"H={res['high']:.2f} L={res['low']:.2f}  in_range={res['in_range']}  "
              f"warnings={res['warnings']}  ({time.time()-t0:.1f}s)")
        (ok if res["low"] < res["high"] else bad)("H > L")
        (ok if res["in_range"] else bad)("H/L in range")
        if dim == "colour":
            (ok if abs(res["alpha"] - 12) < 6 else bad)(f"α̂ close to the true value 12 (off by {abs(res['alpha']-12):.1f})")
    except Exception:
        bad("finish() failed:")
        traceback.print_exc()
if missing_wavs:
    bad(f"{len(missing_wavs)} referenced stimulus files do not exist, e.g. {sorted(missing_wavs)[:3]}")
    fix("check that stimuli/ is complete (T01–T12 × 16 consonants × *3.wav)")
else:
    ok("every stimulus wav referenced in the two simulated dimensions exists")

hdr(5, "LNRMCalibrator shortened fit")
if not (TRY_LNRM and LNRM_OK):
    print("  skipped (TRY_LNRM=False or lnrm unavailable)")
else:
    try:
        from adaptivesft.race import lnrm_random
        dim = "colour"
        rng = np.random.default_rng(SIM_SEED)
        cal = A.LNRMCalibrator(dim, n_per_level=6, seed=SIM_SEED, **LNRM_FIT_KW)
        print(f"  planned {cal.n_trials} trials (6 levels × 6 + AA)")

        def respond(trial):
            if trial["is_match"]:
                return ("n" if rng.uniform() < 0.1 else "y"), 0.8
            u = A.to_model_units(dim, trial["x"])
            rt, correct = lnrm_random([1.0 * u - 0.12 * u * u], 1.0, 0.5, 0.2, rng)
            return ("n" if correct[0] == 1 else "y"), float(rt[0])

        for _ in range(cal.n_trials):
            t = cal.next_trial()
            cal.record(*respond(t))
        t0 = time.time()
        print("  fitting (shortened, about 10–60 s)…")
        res = cal.finish()
        print(f"  α̂={res['alpha']:.2f} α̂₂={res['beta']:.2f} H={res['high']:.2f} L={res['low']:.2f} "
              f"in_range={res['in_range']} divergences={res['extra']['divergences']} ({time.time()-t0:.0f}s)")
        ok("lnrm pipeline ran through")
    except Exception:
        bad("lnrm failed:")
        traceback.print_exc()

hdr(6, f"real run in a window, {RUN_WINDOW_TRIALS} trials ({WINDOW_DIM})")
if RUN_WINDOW_TRIALS <= 0 or not HAVE_PSYCHOPY:
    print("  skipped (RUN_WINDOW_TRIALS = 0 or no psychopy). To try it, set RUN_WINDOW_TRIALS to 3.")
else:
    from psychopy import core, event, sound, visual
    from psychopy.hardware import keyboard
    win = visual.Window(size=(1000, 700), fullscr=False, color="black", units="pix")
    fixs = visual.TextStim(win, text="+", height=40, color="white")
    msg = visual.TextStim(win, text="", height=24, color="white", wrapWidth=900)
    patch_l = visual.Rect(win, width=100, height=100, pos=(-200, 0), colorSpace="hex", lineColor="#808080")
    patch_r = visual.Rect(win, width=100, height=100, pos=(200, 0), colorSpace="hex", lineColor="#808080")
    probe = visual.Rect(win, width=100, height=100, pos=(0, 0), colorSpace="hex", lineColor="#808080")
    try:
        snd = sound.Sound("A", secs=1, stereo=True, hamming=True)
        ok("sound.Sound opens")
    except Exception as e:
        bad(f"sound.Sound failed: {type(e).__name__}: {e}")
        fix("run python audio_pick.py to list the output devices, then python audio_pick.py --set \"NAME\" to pick the headphones")
        snd = None
    kb = keyboard.Keyboard()
    clock = core.Clock()

    def present(draw, secs, play=None):
        if play and snd is not None:
            snd.setSound(play, secs=1, hamming=True)
            snd.play()
        t0 = core.getTime()
        while core.getTime() - t0 < secs:
            if draw:
                draw()
            win.flip()
            if kb.getKeys(["escape"]):
                win.close()
                core.quit()
        if play and snd is not None:
            snd.stop()

    def run_trial(trial):
        present(fixs.draw, 0.3)
        patch_l.fillColor = trial["color1_target"]
        present(patch_l.draw, 1.0)
        patch_r.fillColor = trial["color2_target"]
        present(patch_r.draw, 1.0)
        present(None, 1.0, play=trial["audio1_target_file"])
        present(None, 1.0, play=trial["audio2_target_file"])
        present(fixs.draw, 0.3)
        probe.fillColor = trial["probe_colour"]
        kb.clearEvents()
        clock.reset()
        present(probe.draw, 1.0, play=trial["probe_sound"])
        keys = kb.getKeys(["y", "n"], waitRelease=False)
        while not keys and clock.getTime() < 3.0:
            win.flip()
            keys = kb.getKeys(["y", "n"], waitRelease=False)
            if kb.getKeys(["escape"]):
                win.close()
                core.quit()
        return (keys[0].name, keys[0].rt) if keys else (None, None)

    msg.text = f"DEBUG: {WINDOW_DIM} {RUN_WINDOW_TRIALS} trials\nsame: press y, different: press n\nPress the space bar to begin (esc to quit)"
    msg.draw(); win.flip()
    if "escape" in event.waitKeys(keyList=["space", "escape"]):
        win.close(); core.quit()
    cal = A.PsiCalibrator(WINDOW_DIM, seed=SIM_SEED)
    for i in range(RUN_WINDOW_TRIALS):
        t = cal.next_trial()
        print(f"  trial {t['trial_no']}: x_psi={t['x_psi']:.2f} x={t['x']:.2f} AA={t['is_match']} "
              f"probe={t['probe_colour']} {t['probe_sound']}")
        key, rt = run_trial(t)
        r, c = cal.record(key, rt)
        print(f"           key={key} rt={rt} r={r} correct={c}  α̂,β̂={cal.psi.estimate()}")
        msg.text = "No response" if key is None else ("Correct" if c else "Wrong")
        present(msg.draw, 0.8)
    win.close()
    ok("window flow completed (no finish(); too few trials)")

hdr(7, "VAWM_calibrate.py head dry-run (import, pick the audio device, build the calibrator; stops before the dialog)")
if not HAVE_PSYCHOPY:
    print("  skipped (no psychopy)")
else:
    try:
        _src = open("VAWM_calibrate.py", encoding="utf-8").read().split("expInfo = {")[0]
        _ns = {"__name__": "_vawm_head", "__file__": os.path.abspath("VAWM_calibrate.py")}
        exec(compile(_src, "VAWM_calibrate.py(head)", "exec"), _ns)
        ok(f"METHOD={_ns['METHOD']!r}  FIT_KW={_ns.get('FIT_KW')}")
        if _ns["METHOD"] == "lnrm" and not LNRM_OK:
            bad("METHOD is lnrm but this environment cannot fit it (see step 3)")
        _cal = (A.LNRMCalibrator("colour", n_per_level=_ns["N_PER_LEVEL"], p_match=_ns["P_MATCH"], seed=1,
                                 **_ns.get("FIT_KW", {})) if _ns["METHOD"] == "lnrm"
                else A.PsiCalibrator("colour", seed=1))
        _t = _cal.next_trial()
        ok(f"first trial can be built: probe {_t['probe_colour']} + {_t['probe_sound']}"
           f" ({'file exists' if os.path.exists(_t['probe_sound']) else 'file missing ✘'})")
        print("  ↑ the [audio] line above is the speaker/headphone the experiment will use; if it is wrong, change audioDevice in the PsychoPy preferences")
    except SystemExit:
        bad("the head of VAWM_calibrate.py called core.quit() (most likely an audio-device or window problem; see the messages above)")
    except Exception:
        bad("the head of VAWM_calibrate.py failed:")
        traceback.print_exc()

print("\n" + "=" * W)
print("DEBUG finished. If no ✘ appeared, the calibration chain works in this environment.")
print("=" * W)
