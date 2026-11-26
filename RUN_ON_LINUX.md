# Running the SFT experiment on Linux

Same scripts and folder layout as on Windows; only the installation and the audio layer differ.
For the GRT experiment on Linux see `RUN_GRTv3_ON_LINUX.md` (it reuses §1–§3 of this file, §1b included).

Updated 2026-11-26. **What was actually executed** (Ubuntu 24.04 container, no sound card, virtual display):

| step | Python 3.12 | Python 3.10 |
|---|---|---|
| §2 install, exactly as written | ran, 24 s | ran |
| versions it produced | PsychoPy 2026.2.5, PyMC 6.4.0, nutpie 0.16.11 | PsychoPy 2026.2.5, PyMC 5.25.1, nutpie 0.15.2 |
| `from psychopy import visual, sound, core, data, gui` | ok | not run |
| a PsychoPy window opened and drew on a virtual display (Xvfb) | ok | not run |
| §4 `debug_adaptivesft_EN.py` | all checks pass except the audio device (the container has none) | same |
| §5 `SFT_WM_nochange_EN.py --robot --quick` | whole session, 18 s | whole session, 31 s |

Getting the code (§1b), same container, 2026-11-26:

| command | result |
|---|---|
| route 1, `git clone https://github.com/shadowcrow0/VAWM_run.git` (run with `--depth 1`), then `git pull` | ran; commit `adc1023`, dated 2026-11-24 |
| route 1 without git: the `curl`, `unzip`, `mv` lines | ran; same files as the clone |
| the check at the end of §1b, in that clone | ran: `2026-11-24` and `51:SND_SNR_DB = None`, so on that day the bundle was behind the source |
| §2's `uv pip install --no-deps -e ./adaptiveSFT` (into a new, otherwise empty venv) and §4's `debug_adaptivesft_EN.py`, in that clone | ran; the sibling `adaptiveSFT` is found, all checks pass except the audio device, group `[8]` prints `SND_SNR_DB = None (clean tokens)` |
| route 2, the folder layout and the `git -C ... pull` lines | ran on clones of **local copies** of the two repositories, not from GitHub; sibling found, group `[8]` prints `SND_SNR_DB = 3.0`, 36 tests pass |
| route 2, cloning the private repository with a personal login (HTTPS token or SSH key) | not tested |

**Not tested anywhere by the author:** a real monitor, real sound output, the keyboard, timing, the GitHub login of
route 2, and the Arch and Fedora package names in §1. Report what breaks, with the exact line.

```
 VAWM_run/
    Visual_AudioWM/     SFT_WM_nochange_EN.py, sound_perception_EN.py, adaptive_vawm_EN.py, sft_noise.py,
                        audio_pick.py, debug_adaptivesft_EN.py, stimuli/ (wav + csv), data/ (output)
    adaptiveSFT/        the model-fitting package (PyMC race model) the calibration imports
```

Keep the two folders side by side: the scripts find `adaptiveSFT` relative to `Visual_AudioWM`. Where the folder
comes from: §1b.

## 0. What has to be on the machine

| | why | how to check |
|---|---|---|
| Python 3.10, 3.11 or 3.12 | PsychoPy 2026.2 declares support for these only (`requires-python >=3.10,<3.13`). **Use 3.12**; `uv` fetches it for you, so the distro's own Python does not matter | `python --version` inside the venv |
| the system libraries in §1 | OpenGL, PortAudio and the X11 pieces Qt needs; none of them come from pip | §1 |
| git, or `curl` and `unzip` | to get the code (§1b); git is required only for route 2 there | `git --version` |
| headphones, seen as an ALSA / PulseAudio / PipeWire output | over speakers the delivered SNR is not the configured SNR, and since 2026-11-26 every SFT sound is in noise | `python audio_pick.py` |
| a desktop session (X11, or Wayland with XWayland) | PsychoPy opens a pyglet window; a bare TTY or an SSH session will not do | `echo $DISPLAY` |

wxPython is **no longer needed**: PsychoPy now depends on PyQt6, which pip installs as a wheel. The earlier version
of this file spent a section on building wxPython; ignore it if you still have a copy.

## 1. System packages

Debian / Ubuntu (run on Ubuntu 24.04; each library was reported missing by a failing import before it was added):

```bash
sudo apt update
sudo apt install -y curl git build-essential \
    libglu1-mesa libgl1 libegl1 libportaudio2 libusb-1.0-0 pulseaudio-utils \
    libxcb-cursor0 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-render-util0 libxcb-xkb1 libxcb-util1 libxcb-xinerama0 libxcb-shape0
curl -LsSf https://astral.sh/uv/install.sh | sh        # uv: installs Python 3.12 and the packages; open a new terminal afterwards
```

Arch (package names not checked on an Arch machine):

```bash
sudo pacman -S --needed git base-devel uv glu libglvnd portaudio libusb alsa-lib libpulse \
    xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil libxkbcommon-x11
```

Fedora (not checked either): `sudo dnf install git gcc-c++ uv mesa-libGLU libglvnd-glx portaudio libusb1 alsa-lib
pulseaudio-utils xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil libxkbcommon-x11`.

What each one is for, so a missing one can be recognised from its error:

| library | error without it |
|---|---|
| GLU (`libglu1-mesa`, `glu`) | `ImportError: Library "GLU" not found.` on `from psychopy import visual` |
| PortAudio (`libportaudio2`, `portaudio`) | `OSError: PortAudio library not found` |
| `libxcb-cursor0` and the other xcb / xkbcommon packages | Qt: `Could not load the Qt platform plugin "xcb"` when the participant dialog should appear |
| `pactl` (`pulseaudio-utils`, `libpulse`) | `sh: 1: pactl: not found` while listing audio devices (harmless, but the list may be incomplete) |
| a C++ compiler | only matters on Python 3.10 / 3.11, where the older PyMC compiles C; without it fits are slow and print a warning |

Optional, PsychoPy's own recommendation: let the user raise process priority, which tightens timing. Without it
the experiment runs and prints a warning.

```bash
sudo groupadd --force psychopy
sudo usermod -a -G psychopy "$USER"
echo "@psychopy  -  nice      -20
@psychopy  -  rtprio    50
@psychopy  -  memlock   unlimited" | sudo tee /etc/security/limits.d/99-psychopylimits.conf
# log out and in again
```

## 1b. Get the code

Two routes. Both end inside a folder `VAWM_run/` that holds `Visual_AudioWM/` and `adaptiveSFT/` side by side, which
is what every later step assumes (a block that starts with `cd Visual_AudioWM` is written from `VAWM_run/`).

| | route 1: the public run bundle | route 2: the two source repositories |
|---|---|---|
| repository | `shadowcrow0/VAWM_run` | `shadowcrow0/Visual_AudioWM` (private) and `shadowcrow0/adaptiveSFT` |
| GitHub login | none | an account with access to Visual_AudioWM |
| code you get | whatever was last bundled, so it can be behind the source | always current |
| what is in it | the run files only: scripts, `stimuli/`, an empty `data/`, these guides, the Windows `.bat` files | everything, also `tests/`, `DECISIONS.md` and the `modular` branch |
| meant for | an experiment machine | development, or when the bundle is behind |

**Route 1 with git**

```bash
git clone https://github.com/shadowcrow0/VAWM_run.git
cd VAWM_run
```

Later updates: `git pull` in `VAWM_run/`. The bundle's `.gitignore` excludes `Visual_AudioWM/data/*` and
`Visual_AudioWM/audio_device.txt`, so a pull leaves the collected data and the pinned device alone.

**Route 1 without git** (`curl` and `unzip`; `sudo apt install -y unzip` if that command is missing)

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
route-1 clone showed `2026-11-24` and `None`; the bundle was refreshed later the same day
(commit `67a437f`) and has shown `3.0` since. The value shows up a second time in §4, in group `[8]` of
`debug_adaptivesft_EN.py`.

Participant data in `Visual_AudioWM/data/` never go into the public VAWM_run repository; they go back to the
private Visual_AudioWM repository (commit them in a route-2 checkout, or copy the files off a route-1 machine).

## 2. Python environment

```bash
cd VAWM_run                           # the folder from §1b; skip this line if you are in it already
uv venv --python 3.12 ~/venv-vawm
source ~/venv-vawm/bin/activate
uv pip install psychopy psychtoolbox "pymc>=5.20" nutpie arviz numba pytest
uv pip install --no-deps -e ./adaptiveSFT

python -c "import sys, psychopy, pymc, nutpie, adaptivesft; print('OK python', sys.version.split()[0], 'psychopy', psychopy.__version__, 'pymc', pymc.__version__, 'nutpie', nutpie.__version__)"
```

Expected last line: `OK python 3.12.x psychopy 2026.2.5 pymc 6.4.0 nutpie 0.16.11` (or newer). Every new terminal
needs `source ~/venv-vawm/bin/activate` again.

Without uv, the same thing with the distro's Python, **only if** `python3 --version` says 3.10, 3.11 or 3.12:

```bash
python3 -m venv ~/venv-vawm && source ~/venv-vawm/bin/activate
python -m pip install --upgrade pip
pip install psychopy psychtoolbox "pymc>=5.20" nutpie arviz numba pytest
pip install --no-deps -e ./adaptiveSFT
```

Which Python gives which fitting stack (pip picks the newest versions that support that Python; resolved on
2026-11-26):

| Python | PyMC | nutpie | ArviZ | executed here |
|---|---|---|---|---|
| 3.12 | 6.4.0 | 0.16.11 | 1.3.0 | yes |
| 3.11 | 5.28.5 | 0.16.8 | 0.23.4 | resolved only |
| 3.10 | 5.25.1 | 0.15.2 | 0.23.4 | yes |
| 3.13 and later | not supported by PsychoPy, but **uv installs it anyway** (it ignores the upper bound; resolved here, not run). What pip does was not checked. Always pass `--python 3.12` | | | no |

Write the versions from the `OK` line into the lab log: a calibration fitted with PyMC 5 and one fitted with PyMC 6
are the same model, but the record should say which.

## 3. Audio: find and pin the headphones

```bash
cd Visual_AudioWM
python audio_pick.py                        # table of output devices, and the one that would be chosen
python audio_pick.py --probe --beep         # also open each device, then play a 1 s tone on the chosen one
python audio_pick.py --set "pulse"          # pin a device by (part of) its name -> audio_device.txt
```

Device names come from PortAudio. With PipeWire or PulseAudio you usually see one device called `pulse` or `default`
plus the raw ALSA cards (`hw:0,0 ...`).

- The automatic choice looks for a name containing `headphone`, `headset`, `earphone`, `earbud`, `airpods` or `buds`
  (`audio_pick.py:42`). A device called `USB Audio` or `pulse` does **not** match.
- A device you name yourself is trusted as it is (`audio_pick.py:203`): pin it with `--set`, or pass
  `--audio-device "NAME"`, or set `VAWM_AUDIO_DEVICE`. `--require-headphones` then still works, because the flag only
  restricts the automatic choice. The earlier advice to drop the flag when only `pulse` is listed was wrong.
- So on a PipeWire / PulseAudio desktop: select the headphones in the desktop sound settings, run
  `python audio_pick.py --set "pulse"`, and confirm with `--beep` that the tone comes out of the headphones.

The device name is written into every data row (`audio_device`), so the choice is auditable.

Set the system volume once with the tone and do not touch it afterwards; the noise mixing assumes a fixed playback
level.

## 4. Check the whole chain

```bash
cd Visual_AudioWM
python debug_adaptivesft_EN.py        # 10-20 s
python -m pytest -q tests             # 36 tests, about half a minute; route 2 only, the bundle has no tests/
```

`debug_adaptivesft_EN.py` runs nine numbered groups `[0]`–`[8]`: environment and packages, `adaptiveSFT` found, imports,
which calibration methods are available, a simulated calibration without a window, a short real PyMC fit, a window
test, the audio device and calibration settings, and the noise mixer. Every line should start with `✔`; a `✘` line
prints the fix. The last line reads `DEBUG finished: 0 problem(s).` Group `[8]` must show
`SND_SNR_DB = 3.0 (every sound mixed at that SNR)`. That line gets a `✔` whatever the value is
(`debug_adaptivesft_EN.py:364`), so read it: `SND_SNR_DB = None (clean tokens)` means an old bundle (§1b).

## 5. Run

```bash
cd Visual_AudioWM
python SFT_WM_nochange_EN.py --robot --quick               # self-test with a simulated participant, no window, under a minute
python sound_perception_EN.py --require-headphones         # ~7 min, pure perception, fixed 80-pair table + 40 same, clean speech
python sound_perception_EN.py --axis dprime --snr 3 --require-headphones   # the same test on the experiment's axis, in +3 dB noise
python SFT_WM_nochange_EN.py --require-headphones          # the experiment: colour calibration -> sound calibration -> practice -> 6 blocks
```

`--robot --quick` overwrites `data/robot_simple_*`; those three files are tracked in the source repository, so in
a route-2 checkout run `git checkout -- data/` afterwards (the bundle ignores `data/`; nothing to restore there).

Optional flags (all scripts): `--audio-device "NAME"`, `--list-audio`. The environment variable
`VAWM_AUDIO_DEVICE` does the same as `--audio-device`.

**Noise.** Since 2026-11-26 the SFT experiment mixes every speech sound into speech-shaped noise at +3 dB
(`SND_SNR_DB = 3.0`, `SFT_WM_nochange_EN.py:51`; reasons and what has not been measured: `DECISIONS.md` 27 in the
source repository). `sound_perception_EN.py` is clean unless `--snr` is given.

Output lands in `Visual_AudioWM/data/`:

```
 <id>_sound_perception.csv / .json                     default run (clean speech, fixed pairs)
 <id>_sound_perception_dprime_snr3.csv / .json         with --axis dprime --snr 3
 <id>_simple_calib_trials.csv                          every calibration trial (snd_snr_db, snd_seed_* columns)
 <id>_simple_calib.json                                fitted L / H for colour (dE) and sound (d'), intervals, warnings
 <id>_simple_main.csv                                  main-task probes
 <id>_SFT_WM_<date>.csv / .psydat / .log               PsychoPy's standard files (all phases)
 <id>_snr/                                             the mixed wavs; delete after copying the csv files
                                                       (each is rebuildable from the SNR and seed logged in its row)
```

Participant data go back to the private Visual_AudioWM repository, never into the public VAWM_run repository
(§1b).

## 6. Known differences from Windows

- The `.bat` files are Windows-only; the commands above are their equivalents.
- `PYTHONUSERBASE=%APPDATA%\psychopy3\packages` (the standalone-PsychoPy trick) is not needed in a venv.
- Fullscreen on a multi-monitor X11 setup opens on screen 0 (`visual.Window(fullscr=True, ...)`,
  `SFT_WM_nochange_EN.py:92`); add `screen=1` there if the participant's monitor is the second one.
- Wayland: pyglet does not do native Wayland. Run under XWayland (`xorg-xwayland` on Arch); if the window does not
  appear, start the script with `QT_QPA_PLATFORM=xcb SDL_VIDEODRIVER=x11 python ...`.
- The PsychToolbox audio backend prints a licence / priority notice on first use; it is informational.
- Keyboard: `psychopy.hardware.keyboard.Keyboard` uses the PTB backend, which on Linux may need the user in the
  `input` group to read raw key events (`sudo usermod -a -G input "$USER"`, then log out and in). If keys are still
  not registered, add `prefs.hardware['keyboard'] = 'event'` at the top of the script as a fallback (timing precision
  drops to the event loop, about one frame).

## 7. If something fails

| symptom | cause | fix |
|---|---|---|
| the `OK` line in §2 shows Python 3.13 or newer, or a PsychoPy older than 2026 | the venv was made with a Python PsychoPy does not support | delete `~/venv-vawm`, redo §2 with `--python 3.12` |
| `ImportError: Library "GLU" not found.` | system library missing | §1 |
| `OSError: PortAudio library not found` | system library missing | §1 |
| `Could not load the Qt platform plugin "xcb"` | xcb / xkbcommon libraries missing | §1; `QT_DEBUG_PLUGINS=1 python ...` names the missing file |
| `NoSuchDisplayException: Cannot connect to "None"` | no desktop session (SSH, TTY) | run on the machine's own desktop |
| `[audio] no audio output device found` | PortAudio sees no card | check `pactl list short sinks`; plug the headphones in before starting |
| `ModuleNotFoundError: No module named 'psychopy'` | the venv is not active in this terminal | `source ~/venv-vawm/bin/activate` |
| `SND_SNR_DB = None` in the §1b check or in group `[8]` of §4 | the bundle predates 2026-11-26 | §1b: get a refreshed bundle, or use route 2 |
| `ERROR: file or directory not found: tests` | a route-1 bundle, which has no `tests/` | nothing to fix; the tests are in the source repository (route 2) |
| `Repository not found` or `Authentication failed` while cloning Visual_AudioWM | the account has no access to the private repository, or the login was not accepted | use route 1, or ask for access |
