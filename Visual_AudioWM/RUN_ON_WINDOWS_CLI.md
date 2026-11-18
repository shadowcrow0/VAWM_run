# Running the experiments on Windows from the command line

For someone comfortable with a terminal. Same scripts as the `.bat` files; this just makes every step explicit so
nothing depends on a hard-coded path. PowerShell throughout. Not executed on a Windows machine by the author
(the development container is Linux); report what breaks, with the exact line.

```
 VAWM_run\
    Visual_AudioWM\     SFT_WM_nochange_EN.py, sound_perception_EN.py, adaptive_vawm_EN.py, sft_noise.py,
                        audio_pick.py, debug_adaptivesft_EN.py, GRTv3_ada_EN.py, stimuli\, data\ (output)
    adaptiveSFT\        the model-fitting package (PyMC race model) the SFT calibration imports
```

## 0. What has to be on the machine

| | why | check |
|---|---|---|
| Standalone PsychoPy, 2024.2 or newer | the experiment, the audio backend, and the Python we run everything with | installed from psychopy.org |
| git | to get and update this folder | `git --version` |
| headphones | `--require-headphones` refuses speakers; over speakers the delivered SNR is not the configured SNR | plugged in before step 4 |

Everything is run with **PsychoPy's own python.exe**, never with another Python on the machine. PsychoPy's
Python already has numpy, scipy, pandas, psychtoolbox; we add PyMC, nutpie and `adaptivesft` next to it.

## 1. Get the code

```powershell
git clone https://github.com/shadowcrow0/VAWM_run.git
cd VAWM_run
```

Later updates: `git pull` in the same folder. Participant data in `Visual_AudioWM\data\` are ignored by git and
never pushed from here.

## 2. Find PsychoPy's python.exe

Newer PsychoPy builds do not all put `python.exe` in the same place. Let PowerShell look:

```powershell
$py = (Get-ChildItem "C:\Program Files\PsychoPy*", "$env:LOCALAPPDATA\Programs\PsychoPy*", "${env:ProgramFiles(x86)}\PsychoPy*" `
        -Recurse -Filter python.exe -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
$py
```

If that prints nothing: open PsychoPy Coder, click the **Shell** tab at the bottom, run
`import sys; print(sys.executable)`, and copy the path:

```powershell
$py = "C:\...\python.exe"      # the path Coder printed
```

Then confirm and remember it (the `.bat` files read `psychopy_path.txt`, so both routes stay in sync):

```powershell
& $py --version                 # expect Python 3.10 or 3.11
Set-Content -Path psychopy_path.txt -Value $py
```

## 3. Where PsychoPy loads extra packages from

PsychoPy adds `<its preferences folder>\packages` to `sys.path`. Installing with `--user` while `PYTHONUSERBASE`
points there puts the packages where both the command line and Coder/Builder see them:

```powershell
& $py -c "from psychopy.preferences import prefs; print(prefs.paths['userPrefsDir'])"
# usually C:\Users\<you>\AppData\Roaming\psychopy3
$env:PYTHONUSERBASE = "$env:APPDATA\psychopy3\packages"     # use <the printed folder>\packages if it differs
```

`$env:` settings last for the current PowerShell window only; set it again in a new window (or put the line in
your PowerShell profile).

## 4. Install the fitting stack (SFT only; the GRT experiment does not need it)

```powershell
& $py -m pip install --user --upgrade pip
& $py -m pip install --user "pymc>=5.20" nutpie arviz numba
& $py -m pip install --user --no-deps -e .\adaptiveSFT
& $py -c "import pymc, nutpie, arviz, numba, adaptivesft; print('OK pymc', pymc.__version__, 'nutpie', nutpie.__version__)"
```

Takes 3–10 minutes the first time. If `nutpie` has no wheel for PsychoPy's Python version, the last line fails on
`nutpie`: tell me the output of `& $py --version`; the fallback is `FIT_KW = dict(..., nuts_sampler="pymc")`
in `SFT_WM_nochange_EN.py` (slower fits, same results).

## 5. Audio: find and pin the headphones

```powershell
cd Visual_AudioWM
& $py audio_pick.py                       # table of output devices; opens each and plays a 1 s tone on the chosen one
& $py audio_pick.py --set "Headphones"    # pin by (part of) the device name -> audio_device.txt
```

The device name is written into every data row (`audio_device`). Set the system volume once with the tone and do
not touch it afterwards.

## 6. Check the whole chain

```powershell
& $py debug_adaptivesft_EN.py
$LASTEXITCODE                              # 0 = everything passed
```

Eight numbered checks: Python and packages, the d′ table, a headless simulated calibration, a short real PyMC
fit, the audio device, the calibration settings, and the noise mixer. Every line should be a check mark; a ✘ line
prints the fix.

## 7. Run

```powershell
# SNR pilot (pure perception, ~7 min each, same participant id for the three runs)
& $py sound_perception_EN.py --axis dprime --snr 0  --require-headphones
& $py sound_perception_EN.py --axis dprime --snr 6  --require-headphones
& $py sound_perception_EN.py --axis dprime --snr 12 --require-headphones

# SFT experiment: colour calibration -> sound calibration -> practice -> 6 blocks
& $py SFT_WM_nochange_EN.py --require-headphones
& $py SFT_WM_nochange_EN.py --robot --quick          # self-test with a simulated participant, no window

# GRT experiment
& $py snr_runtime.py                                 # noise-mixer self-check
& $py GRTv3_ada_EN.py
```

Output lands in `Visual_AudioWM\data\`:

```
 <id>_sound_perception_dprime_snr<dB>.csv / .json
 <id>_simple_calib_trials.csv            every calibration trial (with snd_snr_db, snd_seed_* columns)
 <id>_simple_calib.json                  fitted L / H per dimension, 50 % point and plateau with intervals, warnings
 <id>_simple_main.csv                    main-task probes
 <id>_SFT_WM_<date>.csv / .psydat / .log PsychoPy's standard files
 <id>_snr\                               the mixed wavs (only when SND_SNR_DB is set; rebuildable from the seeds)
```

Send the `data\` files to the private repository (Visual_AudioWM `data/`), never to VAWM_run.

## 8. The knobs, and where they live

| what | file | line / name |
|---|---|---|
| colour levels, calibration model (ogival + b0), plateau fraction | `adaptive_vawm_EN.py` | `LEVELS_COLOUR`, `CALIB_LINK`, `CALIB_BIAS`, `CALIB_PLATEAU` |
| sound levels | `adaptive_vawm_EN.py` | `LEVELS_AUDIO` |
| session SNR for the SFT sounds (None = clean) | `SFT_WM_nochange_EN.py` | `SND_SNR_DB` |
| trial counts, response window, fit settings | `SFT_WM_nochange_EN.py` | header, lines 36–60 |

The reasons behind every value are in `DECISIONS.md` of the source repository; the single-source table is
`ARCHITECTURE.md` §3 there. Change a value in one place only.

## 9. If something fails

| symptom | cause | fix |
|---|---|---|
| `pip` SSL / proxy errors | institutional network | `& $py -m pip install --user --proxy http://... ` or install from a hotspot once |
| `ModuleNotFoundError: pymc` when run from Coder but not from the terminal | `PYTHONUSERBASE` differs | step 3: use the folder Coder prints, reinstall |
| `audio_pick.py` lists only `Microsoft Sound Mapper` / `Primary Sound Driver` | no PortAudio device named after the headphones | select the headphones in Windows sound settings, pin that generic device, drop `--require-headphones` |
| window opens then closes at once | an exception before the first frame | run again from the terminal; the traceback is in the window you ran it from |
| `PsychoPy python not found` from a `.bat` | step 2 not done | `psychopy_path.txt` with the path, or run the `.bat` and paste it when asked |
