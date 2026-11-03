# VAWM_run — everything needed to run the experiment, in one folder

Copy this whole folder to the experiment PC (USB stick, OneDrive, anything). Nothing in it depends on where it
sits, except that **PsychoPy must be installed** at `C:\Program Files\PsychoPy` (standalone PsychoPy, Python
3.10). Edit the path at the top of the `.bat` files if PsychoPy lives somewhere else.

```
VAWM_run\
   1_check_audio.bat          list the sound devices, open each one, play a 1 s tone   (every new PC)
   1b_set_audio.bat           remember the headphone device by name                     (every new PC)
   2_install_pymc.bat         install PyMC + nutpie into PsychoPy                        (once per PC, needs internet)
   3_check_everything.bat     one-click diagnostic of the whole chain                    (every new PC)
   4_sound_perception.bat     pure perception test of the consonants, ~6 min            (per participant, before the experiment)
   5_run_experiment.bat       the real experiment                                        (per participant)
   5_run_experiment_robot.bat the same script with a simulated participant, no window    (optional self-test)
   Visual_AudioWM\            the scripts, the stimuli (wav), data\ output
   adaptiveSFT\               the model-fitting package the calibration uses
```

The scripts find `adaptiveSFT` because it sits next to `Visual_AudioWM`. Keep the two folders side by side.

## Step 1 — find the headphones (every new PC)

Plug in the headphones, put them on, double-click **`1_check_audio.bat`**. You get a table like

```
 host: LAB-PC-03   (Windows 10)
 4 output device(s):
   idx  ch    rate  host API        name
     4   2   48000  WASAPI          Speakers (Realtek(R) Audio)
     7   2   48000  WASAPI          Headphones (Realtek(R) Audio)  <- headphones?
 opening each device:
   OK   Speakers (Realtek(R) Audio)  (opened)
   OK   Headphones (Realtek(R) Audio)  (opened)
 [audio] LAB-PC-03: using 'Headphones (Realtek(R) Audio)' (auto)
 [audio] playing a 1.0 s tone on 'Headphones (Realtek(R) Audio)' ...
```

- You hear the tone in the headphones and the chosen line names a headphone-like device → done.
- You hear nothing, or the chosen device is the speakers → find the headphone's name in the table and run
  **`1b_set_audio.bat "part of its name"`**, e.g. `1b_set_audio.bat "USB Audio"`. It plays the tone again on
  that device and remembers the choice in `Visual_AudioWM\audio_device.txt`, so every script will use it.
- No device at all → the sound driver or the headphone jack; nothing in this folder can fix that.

`5_run_experiment.bat` refuses to run on speakers (`--require-headphones`).

## Step 2 — install PyMC (once per PC, needs internet)

Double-click **`2_install_pymc.bat`**. It installs PyMC, numba, arviz, nutpie and the `adaptiveSFT` package into
PsychoPy's own package folder (`%APPDATA%\psychopy3\packages`), the only place PsychoPy Coder looks.
5–10 minutes. The last line should read `OK pymc 5.x nutpie 0.x`. The calibration fits a race model at the end of
each calibration block (about 30–70 s with nutpie); without this step the experiment stops at the first fit.

## Step 3 — check everything (every new PC)

Double-click **`3_check_everything.bat`**. It checks the Python environment, that `adaptiveSFT` is found, the
imports, a headless simulated calibration, a short real model fit, and the audio device. Every line should say
OK; a FAIL line prints what to do next.

## Step 4 — sound perception test (per participant, ~6 min)

Double-click **`4_sound_perception.bat`**. Two syllables, same talker, "same consonant? y / n", feedback, 108
trials, no memory load. At the end it prints and saves hit rate, d' and median RT per confusion level
(`data\<id>_sound_perception.csv/.json`). This tells whether the participant can hear the consonant contrasts
at all; the 2026-11-03 pilot found the sound dimension at chance inside the memory task but discriminable here.

## Step 5 — run a participant

Double-click **`5_run_experiment.bat`**. Enter the participant id in the dialog. The session is:

```
 colour calibration   58 trials  (10 warm-up with feedback, 6 dE levels x 5 + 10 "same", 8 filler) → fit → colour H / L
 sound calibration    58 trials  (same structure on the consonant axis)                              → fit → sound H / L
 practice             2 study sets x 16 probes, feedback
 main task            6 blocks x 14 study sets x 16 probes  (AA x4, single-distractor x2 each, double x1 each)
```

About 17 min of calibration plus two fits, then about 80 min of main task. Keys: `y` = same, `n` = different.

Output, all in `Visual_AudioWM\data\`:

| file | what |
|---|---|
| `<id>_simple_calib_trials.csv` | every calibration trial (level, response, RT) |
| `<id>_simple_calib.json` | the fitted H / L for both dimensions, with warnings if they fell outside the presentable range |
| `<id>_simple_main.csv` | one row per probe in the main task (this is what the analysis reads) |
| `<id>_SFT_WM_<date>.csv / .psydat / .log` | PsychoPy's standard output, all phases |
| `<id>_sound_perception.csv / .json` | step 4 |

Every row also records `audio_device`. Copy the whole `data\` folder back after each session (data are not
part of this public repository).

Command-line options (append to the bat or run the script yourself):

| option | effect |
|---|---|
| `--audio-device "NAME"` | force this output device (must exist, else the script stops and lists the devices) |
| `--require-headphones` | stop instead of falling back to speakers (on in `5_run_experiment.bat`) |
| `--list-audio` | only print the device table and exit |
| `--robot --quick` | no window, simulated participant, short fits (self-test) |

## If something fails

| symptom | cause / fix |
|---|---|
| `[audio] no device ... looks like headphones` | unusual headphone name → `1b_set_audio.bat "name"` |
| `[audio] no output device on ... matches 'X'` | the remembered device is not on this PC → `1b_set_audio.bat` again |
| `ModuleNotFoundError: pymc` at the end of a calibration block | Step 2 not done on this PC |
| `ImportError: ... adaptiveSFT` | the `adaptiveSFT` folder is not next to `Visual_AudioWM` |
| the fit takes > 10 min | nutpie missing (falls back to pure Python) → Step 2 |
| "calibration fell outside the tested range and was clipped" | the participant needs a bigger difference than the stimuli can show; note it, the run continues with the clipped value |

## Updating this folder

This repository is a snapshot of the run files of two upstream repositories (commits in `SOURCES.txt`):
`Visual_AudioWM` ← github.com/shadowcrow0/Visual_AudioWM (only the files the experiment needs),
`adaptiveSFT` ← github.com/shadowcrow0/adaptiveSFT (only the package). To refresh it, in a checkout of
Visual_AudioWM run `python make_run_bundle.py --repo <path to this folder>`, update `SOURCES.txt`, commit, push.
The `.bat` files and this README live only here. Design decisions and notes stay in the upstream repositories
(`Visual_AudioWM/DECISIONS.md`, `Visual_AudioWM/review/`).
