# VAWM_run — everything needed to run the experiment, in one folder

Copy this whole folder to the experiment PC (USB stick, OneDrive, anything). Nothing in it
depends on where it sits, except that **PsychoPy must be installed** at
`C:\Program Files\PsychoPy` (standalone PsychoPy, Python 3.10). Edit the path at the top of
the `.bat` files if PsychoPy lives somewhere else.

```
VAWM_run\
   1_check_audio.bat          list the sound devices, open each one, play a 1 s tone   (every new PC)
   1b_set_audio.bat           remember the headphone device by name                     (every new PC)
   2_install_pymc.bat         install PyMC + nutpie into PsychoPy                        (once per PC, needs internet)
   3_check_everything.bat     one-click diagnostic of the whole chain                    (every new PC)
   4_run_experiment.bat       the real experiment                                        (per participant)
   4_run_experiment_robot.bat the same script with a simulated participant, no window    (optional self-test)
   Visual_AudioWM\            experiment scripts, stimuli, calibration code, data\ output
   adaptiveSFT\               the model-fitting package the calibration uses
```

The scripts find `adaptiveSFT` because it sits next to `Visual_AudioWM`. Keep the two folders
side by side.

## Step 1 — find the headphones (every new PC)

Plug in the headphones, put them on, double-click **`1_check_audio.bat`**. You get a table like

```
 host: LAB-PC-03   (Windows 10)
 saved PsychoPy preference: none
 4 output device(s):
   idx  ch    rate  host API        name
     4   2   48000  WASAPI          Speakers (Realtek(R) Audio)
     7   2   48000  WASAPI          Headphones (Realtek(R) Audio)  <- headphones?
     9   2   48000  WASAPI          DELL U2722D (NVIDIA High Definition Audio)
 opening each device:
   OK   Speakers (Realtek(R) Audio)  (opened)
   OK   Headphones (Realtek(R) Audio)  (opened)
   FAIL DELL U2722D ...  (PortAudio error: Unanticipated host error)
 [audio] LAB-PC-03: using 'Headphones (Realtek(R) Audio)' (auto)
 [audio] playing a 1.0 s tone on 'Headphones (Realtek(R) Audio)' ...
```

- You hear the tone in the headphones and the chosen line says a headphone-like name → done.
- You hear nothing, or the chosen device is the speakers → find the headphone's name in the
  table and run **`1b_set_audio.bat "part of its name"`**, for example
  `1b_set_audio.bat "USB Audio"`. It plays the tone again on that device and remembers the
  choice in `Visual_AudioWM\audio_device.txt`, so every experiment script will use it.
- No device at all → the sound driver or the headphone jack; nothing in this folder can fix that.

The experiment scripts refuse to run on speakers (`--require-headphones` in the bat): the
sound stimuli are speech in noise and speaker playback makes the data unusable.

## Step 2 — install PyMC (once per PC, needs internet)

Double-click **`2_install_pymc.bat`**. It installs PyMC, numba, arviz, nutpie and the
`adaptiveSFT` package into PsychoPy's own package folder
(`%APPDATA%\psychopy3\packages`), which is the only place PsychoPy Coder looks. 5–10 minutes.
The last line should read `OK pymc 5.x nutpie 0.x`.

The calibration fits a race model at the end of each calibration block (about 70 s with
nutpie on a lab PC). Without this step the experiment stops at the first fit.

## Step 3 — check everything (every new PC)

Double-click **`3_check_everything.bat`**. It checks, in order: the Python environment, that
`adaptiveSFT` is found, the imports (`fit_lnrm_v2`, `find_salience`), a headless simulated
calibration, a short real model fit, and a dry run of the experiment up to the participant
dialog. Every line should say OK. A FAIL line prints what to do next.

## Step 4 — run a participant

Double-click **`4_run_experiment.bat`**. Enter the participant id in the dialog. The session is:

```
 colour calibration   72 trials   (sound fixed, colour difference varies)      → fit → colour H / L
 sound calibration    72 trials   (colour fixed, sound difference varies)      → fit → sound H / L
 practice             15 trials   with feedback
 main task            6 blocks × 24 study sets × 9 probes
```

Output, all in `Visual_AudioWM\data\`:

| file | what |
|---|---|
| `<id>_simple_calib_trials.csv` | every calibration trial (level, response, RT) |
| `<id>_simple_calib.json` | the fitted H / L values for both dimensions |
| `<id>_simple_main.csv` | one row per probe in the main task (this is what the analysis reads) |
| `<id>_SFT_WM_<date>.csv / .psydat / .log` | PsychoPy's standard output, all phases |

Every row also records `audio_device`, the output device that was actually used.

Copy the whole `data\` folder back after each session.

Command-line options (append to the bat or run the script yourself):

| option | effect |
|---|---|
| `--audio-device "NAME"` | force this output device (must exist, else the script stops and lists the devices) |
| `--require-headphones` | stop instead of falling back to speakers (already on in `4_run_experiment.bat`) |
| `--list-audio` | only print the device table and exit |
| `--robot --quick` | no window, simulated participant, short fits (self-test) |

`4_run_experiment.bat` runs `SFT_WM_nochange_EN.py` (targets on the non-calibrated dimension
fixed during calibration). For the other variant run `SFT_WM_change_EN.py` the same way.

## If something fails

| symptom | cause / fix |
|---|---|
| `[audio] no device ... looks like headphones` | the headphones have an unusual name → Step 1, `1b_set_audio.bat "name"` |
| `[audio] no output device on ... matches 'X'` | the remembered device is not on this PC → `1b_set_audio.bat` again |
| `ModuleNotFoundError: pymc` at the end of a calibration block | Step 2 not done on this PC |
| `ImportError: ... adaptiveSFT` | the `adaptiveSFT` folder is not next to `Visual_AudioWM` |
| the fit takes > 10 min | nutpie missing (falls back to pure Python) → Step 2 |
| no feedback / wrong keys | keys are `y` = same, `n` = different |

## Updating this folder

This repository is a flat snapshot of two upstream repositories (commits in `SOURCES.txt`):
`Visual_AudioWM` → github.com/shadowcrow0/Visual_AudioWM, `adaptiveSFT` → github.com/shadowcrow0/adaptiveSFT.
To refresh it, clone both upstream repos, copy their contents over the two folders here (without their `.git`
directories), update `SOURCES.txt`, commit and push. The `.bat` files and this README do not change.

Decisions behind the numbers: `Visual_AudioWM\DECISIONS.md`. Hand-off notes:
`Visual_AudioWM\review\進度交接_2026-10-27.md`.
