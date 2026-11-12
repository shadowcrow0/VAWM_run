# Running the SFT experiment on Linux

Companion to `README.md` (Windows). Same scripts, same folder layout; only the installation and the audio layer
differ. Written 2026-11-12 from the package requirements; **not executed on a Linux desktop by the author** — the
development container has no display or sound card. Report what breaks.

```
 VAWM_run/
    Visual_AudioWM/     SFT_WM_nochange_EN.py, sound_perception_EN.py, adaptive_vawm_EN.py, audio_pick.py,
                        debug_adaptivesft_EN.py, stimuli/ (wav + csv), data/ (output)
    adaptiveSFT/        the model-fitting package (PyMC race model) the calibration imports
```

Keep the two folders side by side: the scripts find `adaptiveSFT` relative to `Visual_AudioWM`.

## 0. What has to be on the machine

| | why | how to check |
|---|---|---|
| Python 3.10 or 3.11 | PsychoPy 2024–2026 and nutpie both ship wheels for these | `python3 --version` |
| PsychoPy ≥ 2024.2 | the experiment and the audio backend | `python -c "import psychopy; print(psychopy.__version__)"` |
| PortAudio / PsychToolbox audio | `sound.Sound.backend = 'ptb'` is what the scripts set | see §2 |
| PyMC ≥ 5.20, nutpie, arviz, numba | the calibration fits an LNRM race model after each calibration block | `python -c "import pymc, nutpie"` |
| headphones, seen as an ALSA/Pulse/PipeWire output device | `SFT_WM_nochange_EN.py` runs with `--require-headphones` and refuses speakers | `python audio_pick.py` |
| a desktop session (X11 or XWayland) | PsychoPy opens a pyglet window; a bare TTY or SSH session will not do | `echo $DISPLAY` |

## 1. System packages (Debian / Ubuntu names)

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev build-essential \
    portaudio19-dev libasound2-dev libpulse-dev libusb-1.0-0-dev \
    libsdl2-2.0-0 libgtk-3-0 libwebkit2gtk-4.1-0 libnotify4 libsm6 libxxf86vm1 \
    libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 freeglut3-dev
```

The GTK/WebKit lines are only needed by wxPython, which PsychoPy pulls in as a dependency; the experiment itself
never opens a wx window. On Fedora the equivalents are `portaudio-devel alsa-lib-devel pulseaudio-libs-devel
libusb1-devel SDL2 gtk3 webkit2gtk4.1`.

PsychoPy's PsychToolbox backend wants permission to raise its priority. Either give the user that right
(PsychoPy's own recommendation) or ignore the warning; timing is then slightly worse but the experiment runs:

```bash
sudo groupadd --force psychopy
sudo usermod -a -G psychopy "$USER"
echo "@psychopy  -  nice      -20
@psychopy  -  rtprio    50
@psychopy  -  memlock   unlimited" | sudo tee /etc/security/limits.d/99-psychopylimits.conf
# log out and in again
```

## 2. Python environment

```bash
cd VAWM_run
python3.11 -m venv ~/venv-vawm
source ~/venv-vawm/bin/activate
python -m pip install --upgrade pip wheel

# wxPython first, from the prebuilt wheels for your distro (building it from source takes ~1 h and often fails)
pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04 wxPython   # pick your distro

pip install psychopy psychtoolbox
pip install "pymc>=5.20" nutpie arviz numba
pip install --no-deps -e ./adaptiveSFT

python -c "import psychopy, pymc, nutpie, adaptivesft; print('OK psychopy', psychopy.__version__, 'pymc', pymc.__version__, 'nutpie', nutpie.__version__)"
```

If `pip install psychopy` fails on wxPython and you do not care about Builder/Coder, install without the GUI stack:

```bash
pip install --no-deps psychopy
pip install numpy scipy matplotlib pandas pillow pyglet==1.5.27 psychtoolbox soundfile python-bidi arabic-reshaper \
            json_tricks packaging requests freetype-py msgpack msgpack-numpy pyyaml tables xmltodict javascripthon \
            questplus psutil gevent future imageio imageio-ffmpeg moviepy opencv-python-headless pyzmq
```

and try `python -c "from psychopy import visual, sound, core, data, gui"`; add whatever module it still complains
about. The scripts use `gui.DlgFromDict`, which needs either wx or PyQt5/6 — `pip install PyQt6` is the lighter
option.

## 3. Audio: find and pin the headphones

```bash
cd Visual_AudioWM
python audio_pick.py              # table of output devices, opens each, plays a 1 s tone on the chosen one
python audio_pick.py --set "USB Audio"      # pin a device by (part of) its name → audio_device.txt
```

On Linux the device names come from PortAudio: with PipeWire/PulseAudio you usually see one device called
`pulse` or `default` plus the raw ALSA cards (`hw:0,0 …`). The headphone check (`--require-headphones`) only looks
at the device *name*, so:

- if a card is listed under a headphone-like name (`… Headphones`, `USB Audio`, the headset's brand), pin it with
  `--set` and keep `--require-headphones` when you run;
- if only `pulse` / `default` shows up, select the headphones in the desktop sound settings, pin `pulse`, and run
  the scripts **without** `--require-headphones` (the flag is an option, not a default; the Windows `.bat` files add
  it). Confirm the tone from `python audio_pick.py` comes out of the headphones.

Whatever you choose, the device name is written into every data row (`audio_device`), so the choice is auditable.

Set the system volume once with a reference tone and do not touch it afterwards; the SNR mixing in `snr_audio`
assumes a fixed playback level.

## 4. Check the whole chain

```bash
cd Visual_AudioWM
python debug_adaptivesft_EN.py
```

Every line should read `OK`: Python version, `adaptiveSFT` found, imports, the d′ table
(`stimuli/consonant_dprime.csv`), a headless simulated calibration, a short real PyMC fit (nutpie), and the audio
device. A `FAIL` line prints the fix.

## 5. Run

```bash
cd Visual_AudioWM
python sound_perception_EN.py --require-headphones        # ~8 min, pure perception, fixed 80-pair table
python SFT_WM_nochange_EN.py --require-headphones          # the experiment: 2 calibrations → practice → 6 blocks
                                                           # drop --require-headphones if the device is only 'pulse' (see §3)
python SFT_WM_nochange_EN.py --robot --quick               # self-test with a simulated participant, no window
```

Optional flags (all scripts): `--audio-device "NAME"`, `--list-audio`. Environment variable `VAWM_AUDIO_DEVICE`
does the same as `--audio-device`.

Output lands in `Visual_AudioWM/data/`:

```
 <id>_sound_perception.csv / .json
 <id>_simple_calib_trials.csv            every calibration trial
 <id>_simple_calib.json                  the fitted H / L for colour (ΔE) and sound (d′), in_range flags, FA
 <id>_SFT_WM_<date>.csv / .psydat / .log PsychoPy's standard files (all phases)
 <id>_simple_main.csv                    main-task probes
```

Copy `data/` back to the private `Visual_AudioWM` repository, never into this public bundle.

## 6. Known differences from Windows

- The `.bat` files are Windows-only; the commands above are their one-to-one equivalents.
- `PYTHONUSERBASE=%APPDATA%\psychopy3\packages` (the standalone PsychoPy trick) is not needed in a venv.
- Fullscreen on a multi-monitor X11 setup opens on screen 0; set `screen=` in the script if the headphones PC uses
  another monitor.
- Wayland: run under XWayland (`GDK_BACKEND=x11`, `SDL_VIDEODRIVER=x11`) — pyglet does not do native Wayland.
- The PsychToolbox audio backend prints a licence/priority notice on first use; it is informational.
- Keyboard: `psychopy.hardware.keyboard.Keyboard` uses the PTB backend, which on Linux may need the user in the
  `input` group to read raw key events; if keys are not registered, add `prefs.hardware['keyboard'] = 'event'`
  at the top of the script as a fallback (timing precision drops to the event loop, ~ 1 frame).
