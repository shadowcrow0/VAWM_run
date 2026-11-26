# Running both experiments on a Mac from the terminal (GRT + SFT)

For a macOS machine where you work in the terminal (vim, no Builder GUI). Covers the SFT experiment
(`SFT_WM_nochange_EN.py` + `sound_perception_EN.py`) and the GRT experiment (`GRTv3_ada_EN.py`, or the
`modular` branch's `GRTv3_ada_modular.py`).

Updated 2026-11-26. **Not executed on a Mac by the author.** What was checked from a Linux container:

- the install line in §1 resolves on macOS for Apple Silicon and Intel, on Python 3.10, 3.11 and 3.12, and every
  package it needs has a macOS wheel (nothing is compiled);
- the same install, the diagnostics and a simulated session were run on Linux with Python 3.12 and 3.10
  (`RUN_ON_LINUX.md`, first table at the top);
- §0 on Linux, 2026-11-26 (`RUN_ON_LINUX.md`, second table at the top): the route-1 `git clone` and `git pull`, the
  `curl` + `unzip` + `mv` lines, the check command, and `debug_adaptivesft_EN.py` inside the fresh clone were run
  (the clone showed `2026-11-24` and `SND_SNR_DB = None`). Route 2's folder layout was tested on clones of local
  copies of the two repositories, not from GitHub.

Not tested at all: every command of this file on macOS itself, the GitHub login of route 2 (§0), permissions (§2),
CoreAudio device names (§3), the window, the keyboard and timing. Report what breaks, with the exact line.

```
 VAWM_run/                         (from §0: the public bundle, or the two source repositories side by side)
    Visual_AudioWM/     SFT_WM_nochange_EN.py  sound_perception_EN.py  adaptive_vawm_EN.py  sft_noise.py
                        debug_adaptivesft_EN.py  GRTv3_ada_EN.py  AGRT.py  snr_audio.py  snr_runtime.py
                        agrt_colour_lut.json  audio_pick.py  stimuli/  data/
    adaptiveSFT/        the PyMC race-model package the SFT calibration imports
```

## 0. Get the code

Two routes. Both end inside a folder `VAWM_run/` that holds `Visual_AudioWM/` and `adaptiveSFT/` side by side, which
is what every later step assumes (a block that starts with `cd Visual_AudioWM` is written from `VAWM_run/`).

| | route 1: the public run bundle | route 2: the two source repositories |
|---|---|---|
| repository | `shadowcrow0/VAWM_run` | `shadowcrow0/Visual_AudioWM` (private) and `shadowcrow0/adaptiveSFT` |
| GitHub login | none | an account with access to Visual_AudioWM |
| code you get | whatever was last bundled, so it can be behind the source | always current |
| what is in it | the run files only: scripts, `stimuli/`, an empty `data/`, these guides, the Windows `.bat` files | everything, also `tests/`, `DECISIONS.md` and the `modular` branch |
| meant for | an experiment machine | development, or when the bundle is behind |

git: `git --version`. If macOS offers to install the command line developer tools, accept; or `brew install git`.
Route 1 without git needs nothing extra, `curl` and `unzip` ship with macOS.

**Route 1 with git**

```bash
git clone https://github.com/shadowcrow0/VAWM_run.git
cd VAWM_run
```

Later updates: `git pull` in `VAWM_run/`. The bundle's `.gitignore` excludes `Visual_AudioWM/data/*` and
`Visual_AudioWM/audio_device.txt`, so a pull leaves the collected data and the pinned device alone.

**Route 1 without git**

```bash
curl -L -o VAWM_run.zip https://github.com/shadowcrow0/VAWM_run/archive/refs/heads/main.zip
unzip -q VAWM_run.zip
mv VAWM_run-main VAWM_run          # the zip unpacks as VAWM_run-main
cd VAWM_run
```

To update later, unpack a new zip into a fresh folder and copy `Visual_AudioWM/data/` and
`Visual_AudioWM/audio_device.txt` across.

**Route 2** (git and a GitHub login)

```bash
mkdir VAWM_run && cd VAWM_run
git clone https://github.com/shadowcrow0/Visual_AudioWM.git
git clone https://github.com/shadowcrow0/adaptiveSFT.git
```

The same with SSH: `git clone git@github.com:shadowcrow0/Visual_AudioWM.git` and
`git clone git@github.com:shadowcrow0/adaptiveSFT.git`. Over HTTPS git asks for your GitHub user name and a personal
access token (not the account password); over SSH the key must be registered with your account. The inner folder
names must stay as they are: the scripts look for a sibling called exactly `adaptiveSFT`
(`adaptive_vawm_EN.py:61`). The outer folder may have any name. Later updates, from `VAWM_run/`:

```bash
git -C Visual_AudioWM pull         # default branch: main
git -C adaptiveSFT pull            # default branch: master
```

**Check what you got** (from `VAWM_run/`)

```bash
git log -1 --format=%ad --date=short                           # route 1 with git: date of the bundle commit
unzip -z ../VAWM_run.zip | tail -1                             # route 1 from the zip: the commit hash (a zip carries no date)
git -C Visual_AudioWM log -1 --format=%ad --date=short         # route 2: date of the source commit
grep -n "^SND_SNR_DB" Visual_AudioWM/SFT_WM_nochange_EN.py     # every route
```

Expect the last line to print `51:SND_SNR_DB = 3.0` (and the comment that follows it in the file). If it prints
`SND_SNR_DB = None`, the bundle predates 2026-11-26, the day the session SNR was set: the experiment would play
every sound without noise, and the guides inside the bundle are the older ones. Ask for the bundle to be refreshed
(`make_run_bundle.py:4`, run in the source repository) and get it again, or use route 2. On 2026-11-26 a fresh
route-1 clone showed `2026-11-24` and `None`. The value shows up a second time in §4, in group `[8]` of
`debug_adaptivesft_EN.py`.

Participant data in `Visual_AudioWM/data/` never go into the public VAWM_run repository; they go back to the
private Visual_AudioWM repository (commit them in a route-2 checkout, or copy the files off a route-1 machine).

## 1. Install (once per Mac, about 10 min, needs internet)

```bash
brew install uv git            # no Homebrew:  curl -LsSf https://astral.sh/uv/install.sh | sh   (then open a new terminal)
cd VAWM_run                    # the folder from §0; skip this line if you are in it already
uv venv --python 3.12 ~/venv-vawm
source ~/venv-vawm/bin/activate

uv pip install psychopy psychtoolbox pytest             # both experiments
uv pip install "pymc>=5.20" nutpie arviz numba          # SFT calibration only; skip on a GRT-only machine
uv pip install --no-deps -e ./adaptiveSFT               # SFT only

python -c "import sys, psychopy, pymc, nutpie, adaptivesft; print('OK python', sys.version.split()[0], 'psychopy', psychopy.__version__, 'pymc', pymc.__version__, 'nutpie', nutpie.__version__)"
```

Expected last line: `OK python 3.12.x psychopy 2026.2.5 pymc 6.4.0 nutpie 0.16.11` (or newer). Every new terminal
needs `source ~/venv-vawm/bin/activate` again.

- **Python version.** PsychoPy 2026.2 declares support for 3.10, 3.11 and 3.12 only. Always pass `--python 3.12`:
  uv does not stop you from using 3.13 or newer (it ignores the upper bound), and that combination is unsupported.
- **wxPython is no longer needed**; PsychoPy now uses PyQt6, installed by the line above.
- Which Python gives which fitting stack:

  | Python | PyMC | nutpie | ArviZ |
  |---|---|---|---|
  | 3.12 | 6.4.0 | 0.16.11 | 1.3.0 |
  | 3.11 | 5.28.5 | 0.16.8 | 0.23.4 |
  | 3.10 | 5.25.1 | 0.15.2 | 0.23.4 |

  Write the versions from the `OK` line into the lab log.
- If `import sounddevice` reports `PortAudio library not found`: `brew install portaudio`.
- If `psychtoolbox` cannot be imported, the scripts still run: PsychoPy falls back from the `ptb` audio backend to
  `sounddevice` with a warning, at the cost of roughly 5–10 ms audio-onset jitter. Note it in the lab log.

## 2. macOS permissions (once per Mac)

| what | where | why |
|---|---|---|
| Input Monitoring for Terminal / iTerm | System Settings → Privacy & Security → Input Monitoring | PsychoPy's PTB keyboard reads raw key events; without it the response keys and `space` are never seen and every trial times out |
| Accessibility for Terminal / iTerm | same pane → Accessibility | fullscreen window focus; otherwise the window may open behind the terminal |
| Do Not Disturb / Focus on | Control Centre | notifications steal the fullscreen window |
| Display sleep off, "Automatically adjust brightness" off, True Tone and Night Shift off | System Settings → Displays | long sessions; colour calibration assumes a constant display |
| Sound: output = headphones, volume fixed | Control Centre → Sound | pick it once, write the number down, do not touch it afterwards (the noise mixing assumes a fixed playback level) |

Grant the permissions **before** the first run; macOS asks only the first time and a denied prompt is hard to find
again.

## 3. Audio device (every new Mac, every new headphone)

```bash
cd Visual_AudioWM
python audio_pick.py                               # table of CoreAudio outputs, and the one that would be chosen
python audio_pick.py --probe --beep                # also open each device, then play a 1 s tone on the chosen one
python audio_pick.py --set "External Headphones"   # pin by (part of) the name -> audio_device.txt
```

Typical CoreAudio names: `MacBook Pro Speakers`, `External Headphones` (3.5 mm jack), `USB Audio Device`, the
headset's brand, AirPods.

- The automatic choice looks for a name containing `headphone`, `headset`, `earphone`, `earbud`, `airpods` or `buds`
  (`audio_pick.py:42`). `External Headphones` matches; `USB Audio Device` and a brand-only name do **not**.
- A device you name yourself is trusted as it is (`audio_pick.py:203`): pin it with `--set`, or pass
  `--audio-device "NAME"`. `--require-headphones` and the GRT script's built-in headphone requirement then pass.
- Do not use Bluetooth (AirPods included): latency is unstable and the codec changes the noise spectrum.

The device name goes into every data row (`audio_device`).

## 4. Check the chain (every new Mac)

```bash
cd Visual_AudioWM
python debug_adaptivesft_EN.py      # SFT: nine groups [0]-[8]; packages, adaptiveSFT found, simulated calibration, a short PyMC fit, audio device, noise mixer
python snr_runtime.py               # GRT: mixes a few stimuli at exact SNRs and verifies the realised SNR (~1 s)
python -m pytest -q tests           # 36 tests, about half a minute; route 2 only, the bundle has no tests/
```

Every line of the first one should start with `✔`; a `✘` line prints the fix. It ends with
`DEBUG finished: 0 problem(s).` Group `[8]` must show `SND_SNR_DB = 3.0 (every sound mixed at that SNR)`. That line
gets a `✔` whatever the value is (`debug_adaptivesft_EN.py:364`), so read it: `SND_SNR_DB = None (clean tokens)`
means an old bundle (§0).

## 5. SFT experiment (per participant)

```bash
cd Visual_AudioWM
python SFT_WM_nochange_EN.py --robot --quick           # self-test with a simulated participant, no window, under a minute
python sound_perception_EN.py --require-headphones     # ~7 min: fixed 80-pair table + 40 same, no memory load, clean speech
python sound_perception_EN.py --axis dprime --snr 3 --require-headphones   # the same test on the experiment's axis, in +3 dB noise
python SFT_WM_nochange_EN.py --require-headphones      # colour calibration -> sound calibration -> practice -> 6 blocks
```

`--robot --quick` overwrites `data/robot_simple_*`; those files are tracked in the source repository, so in a
route-2 checkout run `git checkout -- data/` afterwards (the bundle ignores `data/`; nothing to restore there).

**Noise.** Since 2026-11-26 the SFT experiment mixes every speech sound into speech-shaped noise at +3 dB
(`SND_SNR_DB = 3.0`, `SFT_WM_nochange_EN.py:51`; reasons and what has not been measured: `DECISIONS.md` 27 in the
source repository).

Output in `data/`:

```
 <id>_sound_perception.csv / .json                     default run (clean speech, fixed pairs)
 <id>_sound_perception_dprime_snr3.csv / .json         with --axis dprime --snr 3
 <id>_simple_calib_trials.csv                          every calibration trial (snd_snr_db, snd_seed_* columns)
 <id>_simple_calib.json                                fitted L / H for colour (dE) and sound (d'), intervals, warnings
 <id>_simple_main.csv                                  main-task probes
 <id>_SFT_WM_<date>.csv / .psydat / .log               PsychoPy's standard files (all phases)
 <id>_snr/                                             the mixed wavs; delete after copying the csv files
```

## 6. GRT experiment (per participant)

```bash
cd Visual_AudioWM
python GRTv3_ada_EN.py                          # ~75–90 min: 72 colour + 72 sound Psi trials → 15 practice → 576 main
python GRTv3_ada_EN.py --pilot                  # windowed 1024×768, id 'pilot'
python GRTv3_ada_EN.py --audio-device "External Headphones"

# modular version (route 2 only: git checkout modular): same flags, plus
python GRTv3_ada_modular.py --no-headphone-check
```

No PyMC needed. Output `data/<id>_GRTv3_ada_<date>.csv/.psydat/.log`, `data/<id>_GRTv3_ada_<date>_snr/` (every wav
played, ~130 MB — delete after copying the csv; each is rebuildable from the logged seed + dB), `…_posterior*.npy`.

## 7. Editing parameters in vim — where the knobs are

```
 SFT_WM_nochange_EN.py      lines 36–55   N_PER_LEVEL, P_MATCH, N_WARMUP, N_FILLER, FIT_KW (tune/draws/chains/nutpie),
                                          N_BLOCKS, SETS_PER_BLOCK, PROBES_PER_SET, N_PRACTICE_SETS, RESP_WINDOW,
                                          OTHER_TARGETS_CHANGE, PROV_*, SND_SNR_DB (session SNR; None = clean)
 adaptive_vawm_EN.py        lines 109–115 LEVELS_COLOUR, LEVELS_AUDIO, CALIB_LINK / CALIB_BIAS / CALIB_PLATEAU
                                          (L = the 50 % point, H = 90 % of the plateau; DECISIONS 25)
 GRTv3_ada_EN.py            439–470       N_VALID_PER_CELL, N_INVALID_PER_CELL, BLOCK_SIZE, N_ADAPT_COL/SND, N_PRACTICE
                            864–893       OVERALL_ACC, LAPSE, SND_TOKEN, SNR_LIM, ADAPT_FIX_ARC / ADAPT_FIX_SNR, MASK_*
 grtv3/config.py (modular)  one file      all of the above for GRT, plus CALIB_JOINT (0 = two blocks, 1 = Glavan joint)
```

Line numbers were checked on 2026-11-26; if they have drifted, `grep -n NAME file`. Before and after touching a
number: `python -m pytest tests/test_adaptive_vawm.py` (SFT), `python -m pytest tests/test_grtv3.py` (GRT, modular
branch). Why each number has its value: `DECISIONS.md`. The tests and `DECISIONS.md` are in the source repository
only (route 2 in §0).

## 8. Mac-specific notes

- Retina: PsychoPy reports the logical resolution; `testMonitor` must be defined once (width cm, distance cm, pixels)
  in Monitor Center — `python -c "from psychopy import monitors; m=monitors.Monitor('testMonitor'); m.setWidth(30.0); m.setDistance(57.0); m.setSizePix([1440, 900]); m.save()"` does it from the terminal. The 4° squares depend on it.
- Fullscreen on a laptop with an external display: screen 0 is the one macOS calls main; the scripts open there.
- `Esc` ends a session and saves what was collected (both experiments).
- Keep `data/` on the local disk, not iCloud Drive or OneDrive: both experiments write a wav for every sound played.
- Participant data go back to the private Visual_AudioWM repository, never into the public VAWM_run repository
  (§0).

## 9. If something fails

| symptom | cause | fix |
|---|---|---|
| the `OK` line in §1 shows Python 3.13 or newer | the venv was made without `--python 3.12` | delete `~/venv-vawm`, redo §1 |
| `ModuleNotFoundError: No module named 'psychopy'` | the venv is not active in this terminal | `source ~/venv-vawm/bin/activate` |
| every trial times out, keys do nothing | Input Monitoring not granted | §2, then quit and reopen the terminal |
| the window opens behind the terminal | Accessibility not granted | §2 |
| `[audio] no output device ... matches` | the pinned name is not there (headphones unplugged, different Mac) | `python audio_pick.py`, then `--set` again |
| `SND_SNR_DB = None` in the §0 check or in group `[8]` of §4 | the bundle predates 2026-11-26 | §0: get a refreshed bundle, or use route 2 |
| `ERROR: file or directory not found: tests` | a route-1 bundle, which has no `tests/` | nothing to fix; the tests are in the source repository (route 2) |
| `Repository not found` or `Authentication failed` while cloning Visual_AudioWM | the account has no access to the private repository, or the login was not accepted | use route 1, or ask for access |
