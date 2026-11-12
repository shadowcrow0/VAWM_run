# Running GRTv3_ada on Linux

Companion to `RUN_ON_LINUX.md` (the SFT scripts). Two entry points do the same experiment:

```
 GRTv3_ada_EN.py          PsychoPy-Builder output, hand-edited (branch main)
 GRTv3_ada_modular.py     the same experiment as a package, grtv3/ (branch modular); no Builder
```

Written 2026-11-12. **Not executed on a Linux desktop by the author** — the development container has no
display or sound card, and Arc (the HPC) has neither, so Arc can run the tests in §4 but never the experiment.

## 0. What is different from the SFT scripts

| | SFT (`SFT_WM_nochange_EN.py`) | GRTv3_ada |
|---|---|---|
| model fitting | PyMC + nutpie (LNRM race), 30–70 s per fit | none at run time: two Psi staircases (`AGRT.py`, numpy + scipy only) |
| extra Python packages | `pymc nutpie arviz numba`, `adaptiveSFT` | none beyond PsychoPy + numpy + scipy |
| sound stimuli | 192 wav tokens in `stimuli/` | one natural [bi] token mixed into speech-shaped noise **on demand** (`snr_audio`, `snr_runtime`); writes a wav per trial into `data/<id>_<date>_snr/` (~130 MB per session, gitignored, rebuildable from the logged seed + dB) |
| colour | CIELAB ΔE from `adaptive_vawm_EN` | arc length on a perceptually uniform hue arc, table `agrt_colour_lut.json` (generated offline; needs no `colour-science` at run time) |
| headphones | optional flag `--require-headphones` | **required**: SNR over speakers is not the configured SNR; `GRTv3_ada_EN.py` stops without a headphone-like device, `GRTv3_ada_modular.py` too unless `--no-headphone-check` |
| Esc | ends and saves | same (modular: `ExperimentAbort` → save in `finally`) |

Session: 72 colour-calibration + 72 sound-calibration trials (each a full ~8–10 s WM trial), 15 practice with
feedback, 576 main trials in 4 blocks. About 75–90 min.

## 1. System packages and Python environment

Follow `RUN_ON_LINUX.md` §1–§2 **up to and including** `pip install psychopy psychtoolbox`. Skip the PyMC line and
the `adaptiveSFT` line; they are not used. Then:

```bash
pip install numpy scipy            # already pulled in by psychopy; scipy ≥ 1.12 is fine (AGRT.py patches the removed mvnun)
python -c "import psychopy, numpy, scipy; print('OK', psychopy.__version__, scipy.__version__)"
```

## 2. Check the pieces that do not need a screen

```bash
cd Visual_AudioWM
python snr_runtime.py                    # mixes a few stimuli, checks the realised SNR, ~1 s; prints a summary
python -c "from grtv3.colour import ColourLUT; l=ColourLUT(); print(l.arc_min, l.arc_max, l.hex_for(0.0))"   # modular branch
python audio_pick.py                     # output devices; plays a 1 s tone on the chosen one
python audio_pick.py --set "USB Audio"   # pin the headphones by (part of) the name → audio_device.txt
```

`snr_runtime.py` must find `stimuli/kutlu_mcmurray_2024/cv/beachpeach1_cv.wav` (tracked in the repo; the token key is
`'bi'` — since commit 8e0c640 the scripts and `snr_runtime` agree on that; older checkouts said `'be'` and crashed
at start-up).

The headphone check looks at the device *name*. On PipeWire/PulseAudio desktops where PortAudio only exposes
`pulse` / `default`, pick the headphones in the desktop sound settings, pin `pulse`, and run the modular entry with
`--no-headphone-check` (the Builder entry has no such switch; edit `require_headphones=True` on its line 42 if you
must). The device name is saved in every data row (`audio_device`).

## 3. Run

```bash
cd Visual_AudioWM

# Builder version (branch main)
python GRTv3_ada_EN.py                          # dialog: participant, session; needs a headphone-like device
python GRTv3_ada_EN.py --audio-device "USB Audio"
python GRTv3_ada_EN.py --pilot                  # windowed 1024×768, participant id 'pilot'
python GRTv3_ada_EN.py --list-audio             # only list devices and exit

# Modular version (branch modular)
git checkout modular
python GRTv3_ada_modular.py                     # same dialog and flags
python GRTv3_ada_modular.py --pilot
python GRTv3_ada_modular.py --no-headphone-check --audio-device pulse
```

Calibration mode of the modular version is a constant, `grtv3/config.py: CALIB_JOINT` — `0` = colour block then
sound block (the Builder design, default), `1` = Glavan's joint calibration (both dimensions proposed on every
trial, `AGRTHandler.next/addResponse`, `N_ADAPT_JOINT` trials).

Output in `Visual_AudioWM/data/`:

```
 <id>_GRTv3_ada_<date>.csv / .psydat / .log    one row per trial: phase, adapt_x, colour_arc_lo/hi, snr_hi/lo, quad_content,
                                               cue_*, opt_perm, pressed_key, chosen_item, outcome, is_correct, rt,
                                               snd_item0..3 / snd_probe / snd_mask (dB + noise seed per stimulus),
                                               psi_*_alpha/beta and final_* on the last calibration row
 <id>_GRTv3_ada_<date>_snr/                     every wav actually played (rebuild any of them: SNRStimulus.rebuild(seed, db))
 <id>_GRTv3_ada_<date>_posterior*.npy           the two Psi posteriors at the end of calibration
```

The modular version writes the same column names (plus `adapt_s`, `adapt_resp_s`, `calib_joint` in joint mode).

## 4. Tests that run anywhere (also on Arc)

```bash
pytest tests/test_grtv3.py        # modular branch: plan, layout, scoring, Psi response rules, LUT, mask noise, calibration wrapper (14 tests)
python snr_runtime.py             # both branches
```

Nothing in `GRTv3_ada_EN.py` is testable without PsychoPy; the modular branch exists for exactly that reason.

## 5. Linux-specific notes

- Wayland: run under XWayland (`GDK_BACKEND=x11 SDL_VIDEODRIVER=x11`).
- Keys `i o k l` and `space` are read with PsychoPy's PTB keyboard; if presses are not registered, add the user to the
  `input` group or set `prefs.hardware['keyboard'] = 'event'` at the top of the script.
- The per-trial wavs are written to disk during the experiment; keep `data/` on a local drive, not a network mount.
- Monitor: the scripts use `monitor='testMonitor'` with degrees of visual angle. Define `testMonitor` (width, distance,
  resolution) in PsychoPy's Monitor Center once per machine, or the 4° squares will be whatever size the default
  calibration implies; the first lines printed at start-up (`monitor: … width_cm … dist_cm …`) show what was used.
