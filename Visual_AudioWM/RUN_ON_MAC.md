# Running both experiments on a Mac from the terminal (GRT + SFT)

For a macOS machine where you work in the terminal (vim, no Builder GUI). Covers the SFT experiment
(`SFT_WM_nochange_EN.py` + `sound_perception_EN.py`) and the GRT experiment (`GRTv3_ada_EN.py`, or the
`modular` branch's `GRTv3_ada_modular.py`). Written 2026-11-12 from the package requirements; **not executed on a
Mac by the author** — the development container has no display or sound card. Report what breaks.

```
 VAWM_run/                         (the public bundle; or a checkout of Visual_AudioWM + adaptiveSFT side by side)
    Visual_AudioWM/     SFT_WM_nochange_EN.py  sound_perception_EN.py  adaptive_vawm_EN.py  debug_adaptivesft_EN.py
                        GRTv3_ada_EN.py  AGRT.py  snr_audio.py  snr_runtime.py  agrt_colour_lut.json
                        audio_pick.py  stimuli/  data/
    adaptiveSFT/        the PyMC race-model package the SFT calibration imports
```

## 1. Install (once per Mac, ~15 min, needs internet)

```bash
# Python 3.11 (Apple Silicon or Intel both fine)
brew install python@3.11 portaudio
cd VAWM_run
python3.11 -m venv ~/venv-vawm
source ~/venv-vawm/bin/activate
python -m pip install --upgrade pip wheel

pip install psychopy psychtoolbox              # wxPython has macOS wheels, so this just works (5–10 min)
pip install "pymc>=5.20" nutpie arviz numba     # SFT calibration only; skip for GRT-only machines
pip install --no-deps -e ./adaptiveSFT          # SFT only

python -c "import psychopy, pymc, nutpie, adaptivesft; print('OK', psychopy.__version__, pymc.__version__, nutpie.__version__)"
```

If `pip install psychtoolbox` fails on Apple Silicon (no wheel for your Python), the scripts still run: PsychoPy falls
back from the `ptb` audio backend to `sounddevice` with a warning, at the cost of ~5–10 ms audio-onset jitter. Note
it in the lab log; the calibrations do not depend on audio-onset precision, the RT measures do only weakly.

## 2. macOS permissions (once per Mac)

| what | where | why |
|---|---|---|
| Input Monitoring for Terminal / iTerm | System Settings → Privacy & Security → Input Monitoring | PsychoPy's PTB keyboard reads raw key events; without it `i o k l`, `y n`, `space` are never seen and every trial times out |
| Accessibility for Terminal / iTerm | same pane → Accessibility | fullscreen window focus; otherwise the window may open behind the terminal |
| Do Not Disturb / Focus on | Control Centre | notifications steal the fullscreen window |
| Display sleep off, "Automatically adjust brightness" off | System Settings → Displays | 90-minute sessions; colour calibration assumes constant brightness |
| Sound: output = headphones, volume fixed | Control Centre → Sound | pick it once, write the number down, do not touch it afterwards (the SNR mixing assumes a fixed playback level) |

Grant the permissions **before** the first run; macOS asks only the first time and a denied prompt is hard to find
again.

## 3. Audio device (every new Mac, every new headphone)

```bash
cd Visual_AudioWM
python audio_pick.py                          # table of CoreAudio outputs; opens each; 1 s tone on the chosen one
python audio_pick.py --set "External Headphones"     # pin by (part of) the name → audio_device.txt
```

Typical CoreAudio names: `MacBook Pro Speakers`, `External Headphones` (3.5 mm jack), `USB Audio Device`, the
headset's brand, AirPods (do not use Bluetooth: variable latency and the codec resamples the noise). The headphone
check in both experiments looks at the name: `External Headphones` and anything with "headphone/headset/USB Audio"
passes; a brand-only name may not — pin it with `--set` and pass `--audio-device "name"` to be explicit. The device
name goes into every data row (`audio_device`).

## 4. Check the chain (every new Mac)

```bash
cd Visual_AudioWM
python debug_adaptivesft_EN.py      # SFT: Python, adaptiveSFT found, imports, d′ table, simulated calibration, one short PyMC fit, audio device
python snr_runtime.py               # GRT: mixes a few stimuli at exact SNRs and verifies the realised SNR (~1 s)
```

Every line `OK`. A `FAIL` line prints the fix.

## 5. SFT experiment (per participant)

```bash
cd Visual_AudioWM
python sound_perception_EN.py --require-headphones     # ~8 min: fixed 80-pair table + 40 same, no memory load
python SFT_WM_nochange_EN.py --require-headphones      # ~60–75 min: colour calibration → sound calibration → practice → 6 blocks
python SFT_WM_nochange_EN.py --robot --quick           # self-test with a simulated participant, no window
```

Output `data/<id>_sound_perception.csv/.json`, `data/<id>_simple_calib.json` (H/L for colour in ΔE and sound in
d′, `in_range`, false-alarm rate), `data/<id>_simple_calib_trials.csv`, `data/<id>_SFT_WM_<date>.csv/.psydat/.log`.

## 6. GRT experiment (per participant)

```bash
cd Visual_AudioWM
python GRTv3_ada_EN.py                          # ~75–90 min: 72 colour + 72 sound Psi trials → 15 practice → 576 main
python GRTv3_ada_EN.py --pilot                  # windowed 1024×768, id 'pilot'
python GRTv3_ada_EN.py --audio-device "External Headphones"

# modular version (git checkout modular): same flags, plus
python GRTv3_ada_modular.py --no-headphone-check
```

No PyMC needed. Output `data/<id>_GRTv3_ada_<date>.csv/.psydat/.log`, `data/<id>_GRTv3_ada_<date>_snr/` (every wav
played, ~130 MB — delete after copying the csv; each is rebuildable from the logged seed + dB), `…_posterior*.npy`.

## 7. Editing parameters in vim — where the knobs are

```
 SFT_WM_nochange_EN.py      lines 36–58   LEVELS_COLOUR / LEVELS_AUDIO, N_PER_LEVEL, P_MATCH, N_WARMUP, N_FILLER,
                                          FIT_KW (tune/draws/chains/nutpie), N_BLOCKS, SETS_PER_BLOCK, PROBES_PER_SET,
                                          N_PRACTICE_SETS, RESP_WINDOW, OTHER_TARGETS_CHANGE
 adaptive_vawm_EN.py        ~line 110     LEVELS_*, H_TARG_DEFAULT / L_TARG_DEFAULT (drift-separation targets 8.0 / 1.3)
 GRTv3_ada_EN.py            434–479       N_VALID_PER_CELL, N_INVALID_PER_CELL, BLOCK_SIZE, N_ADAPT_COL/SND, N_PRACTICE
                            866–889       OVERALL_ACC, LAPSE, SND_TOKEN, SNR_LIM, ADAPT_FIX_ARC / ADAPT_FIX_SNR, MASK_*
 grtv3/config.py (modular)  one file      all of the above for GRT, plus CALIB_JOINT (0 = two blocks, 1 = Glavan joint)
```

Before and after touching a number: `pytest tests/test_adaptive_vawm.py` (SFT), `pytest tests/test_grtv3.py` (GRT,
modular branch). Why each number has its value: `DECISIONS.md`.

## 8. Mac-specific notes

- Retina: PsychoPy reports the logical resolution; `testMonitor` must be defined once (width cm, distance cm, pixels)
  in Monitor Center — `python -c "from psychopy import monitors; m=monitors.Monitor('testMonitor'); m.setWidth(30.0); m.setDistance(57.0); m.setSizePix([1440, 900]); m.save()"` does it from the terminal. The 4° squares depend on it.
- Fullscreen on a laptop with an external display: screen 0 is the one macOS calls main; the scripts open there.
- Bluetooth headphones: do not. Latency is unstable and the codec changes the noise spectrum.
- `Esc` ends a session and saves what was collected (both experiments).
- Keep `data/` on the local disk, not iCloud Drive or OneDrive: the GRT script writes a wav every trial.
- Participant data never go into the public VAWM_run repository; copy `data/` back to the private Visual_AudioWM
  repository.
