# Running the experiments on Windows from the command line

For someone comfortable with a terminal. Same scripts as the `.bat` files; this makes every step explicit so
nothing depends on a hard-coded path. PowerShell throughout.

Updated 2026-11-26. **Not executed on a Windows machine by the author** (the development container is Linux).
What was checked from there:

- the packages in step 3 resolve on Windows for Python 3.10, 3.11 and 3.12, all as wheels (nothing is compiled);
- the same install, the diagnostics and a simulated session were run on Linux with Python 3.12 and with Python 3.10,
  the two stacks in the table of step 3 (`RUN_ON_LINUX.md`, first table at the top);
- step 1 on Linux, 2026-11-26 (`RUN_ON_LINUX.md`, second table at the top): the `git clone` and `git pull` of 1a
  were run; the zip address of 1b was downloaded with `curl` and does unpack as `VAWM_run-main`; the two `git log`
  lines of 1d were run and the file was searched with `grep` (the fresh clone showed `2026-11-24` and
  `SND_SNR_DB = None`); `debug_adaptivesft_EN.py` was run inside that clone. The layout of 1c was tested on clones of
  local copies of the two repositories, not from GitHub.

Not run at all: every PowerShell line of this file (`Invoke-WebRequest`, `Expand-Archive`, `Select-String`
included), and the GitHub login of 1c.

Python route A below (step 2) is what `setup_pymc_coder.bat` does and what the lab machine uses. Python route B is
new and untested on Windows. Report what breaks, with the exact line.

```
 VAWM_run\
    Visual_AudioWM\     SFT_WM_nochange_EN.py, sound_perception_EN.py, adaptive_vawm_EN.py, sft_noise.py,
                        audio_pick.py, debug_adaptivesft_EN.py, GRTv3_ada_EN.py, stimuli\, data\ (output)
    adaptiveSFT\        the model-fitting package (PyMC race model) the SFT calibration imports
```

## 0. What has to be on the machine

| | why | check |
|---|---|---|
| a Python with PsychoPy (route A or B in step 2) | everything is run with that one `python.exe`, stored in `$py` | step 2 |
| git (optional for the public bundle, required for the source repositories) | to get and update this folder; without it, download the zip (step 1b) | `git --version` |
| headphones | over speakers the delivered SNR is not the configured SNR, and since 2026-11-26 every SFT sound is in noise | plugged in before step 4 |

## 1. Get the code

Two routes, numbered so they are not confused with the lettered Python routes of step 2. Both end inside a folder
`VAWM_run\` that holds `Visual_AudioWM\` and `adaptiveSFT\` side by side, which is what every later step assumes.

| | route 1 (1a or 1b): the public run bundle | route 2 (1c): the two source repositories |
|---|---|---|
| repository | `shadowcrow0/VAWM_run` | `shadowcrow0/Visual_AudioWM` (private) and `shadowcrow0/adaptiveSFT` |
| GitHub login | none | an account with access to Visual_AudioWM |
| code you get | whatever was last bundled, so it can be behind the source | always current |
| what is in it | the run files only: scripts, `stimuli\`, an empty `data\`, these guides, the numbered `.bat` files | everything, also `tests\`, `DECISIONS.md` and the `modular` branch; no numbered `.bat` files |
| meant for | an experiment machine | development, or when the bundle is behind |

**1a. Route 1 with git**

```powershell
git clone https://github.com/shadowcrow0/VAWM_run.git
cd VAWM_run
```

Later updates: `git pull` in the same folder. The bundle's `.gitignore` excludes `Visual_AudioWM/data/*`,
`Visual_AudioWM/audio_device.txt` and `psychopy_path.txt`, so a pull leaves the collected data and the machine's
settings alone.

**1b. Route 1 without git** (nothing to install; PowerShell downloads and unpacks the current snapshot)

```powershell
cd $HOME\Documents
Invoke-WebRequest -Uri https://github.com/shadowcrow0/VAWM_run/archive/refs/heads/main.zip -OutFile VAWM_run.zip
Expand-Archive -Path VAWM_run.zip -DestinationPath . -Force
Rename-Item VAWM_run-main VAWM_run        # the zip unpacks as VAWM_run-main
cd VAWM_run
```

To update later, repeat 1b into a fresh folder and copy your `Visual_AudioWM\data\`, `psychopy_path.txt` and
`Visual_AudioWM\audio_device.txt` across (or just download again and redo steps 2 to 4; they take a few minutes).

If you would rather have git: `winget install --id Git.Git -e` in an administrator PowerShell, then open a new
window and use 1a.

**1c. Route 2** (git and a GitHub login)

```powershell
mkdir VAWM_run
cd VAWM_run
git clone https://github.com/shadowcrow0/Visual_AudioWM.git
git clone https://github.com/shadowcrow0/adaptiveSFT.git
```

The same with SSH: `git clone git@github.com:shadowcrow0/Visual_AudioWM.git` and
`git clone git@github.com:shadowcrow0/adaptiveSFT.git`. Over HTTPS, Git for Windows opens a GitHub sign-in window
(or asks for your user name and a personal access token, not the account password); over SSH the key must be
registered with your account. The inner folder names must stay as they are: the scripts look for a sibling called
exactly `adaptiveSFT` (`adaptive_vawm_EN.py:61`). The outer folder may have any name. Later updates, from
`VAWM_run\`:

```powershell
git -C Visual_AudioWM pull         # default branch: main
git -C adaptiveSFT pull            # default branch: master
```

**1d. Check what you got** (from `VAWM_run\`)

```powershell
git log -1 --format=%ad --date=short                                               # 1a: date of the bundle commit
git -C Visual_AudioWM log -1 --format=%ad --date=short                             # 1c: date of the source commit
Select-String -Path Visual_AudioWM\SFT_WM_nochange_EN.py -Pattern '^SND_SNR_DB'    # every route (1b has no date to show)
```

Expect the last line to show line 51 of the file as `SND_SNR_DB = 3.0` (and the comment that follows it). If it
shows `SND_SNR_DB = None`, the bundle predates 2026-11-26, the day the session SNR was set: the experiment would play
every sound without noise, and the guides inside the bundle are the older ones. Ask for the bundle to be refreshed
(`make_run_bundle.py:4`, run in the source repository) and get it again, or use 1c. On 2026-11-26 a fresh clone
(1a) showed `2026-11-24` and `None`; the bundle was refreshed later the same day (commit `67a437f`) and has
shown `3.0` since. The value shows up a second time in step 5, in group `[8]` of
`debug_adaptivesft_EN.py`.

Participant data in `Visual_AudioWM\data\` never go into the public VAWM_run repository; they go back to the
private Visual_AudioWM repository (commit them in a 1c checkout, or copy the files off a route-1 machine).

## 2. Choose the Python: `$py`

Do **one** of the two. Both end with `$py` pointing at a `python.exe`; every later step is the same.

### Route A — Standalone PsychoPy (the lab machine's setup)

Install Standalone PsychoPy 2024.2 or newer from psychopy.org. Its own `python.exe` already has PsychoPy, numpy,
scipy, pandas and psychtoolbox; step 3 adds PyMC, nutpie and `adaptivesft` next to it.

Newer builds do not all put `python.exe` in the same place. Let PowerShell look:

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

PsychoPy adds `<its preferences folder>\packages` to `sys.path`. Installing with `--user` while `PYTHONUSERBASE`
points there puts the packages where both the command line and Coder / Builder see them:

```powershell
& $py -c "from psychopy.preferences import prefs; print(prefs.paths['userPrefsDir'])"
# usually C:\Users\<you>\AppData\Roaming\psychopy3
$env:PYTHONUSERBASE = "$env:APPDATA\psychopy3\packages"     # use <the printed folder>\packages if it differs
$pipargs = @("-m", "pip", "install", "--user")
```

### Route B — a separate Python 3.12 environment (no Standalone PsychoPy, no Coder / Builder)

Use this on a machine that has no PsychoPy yet and will only run the scripts from the terminal. It is the same
environment as the Linux and Mac guides build.

```powershell
winget install --id astral-sh.uv -e          # then open a new PowerShell window
uv venv --seed --python 3.12 $HOME\venv-vawm      # --seed puts pip into the venv; step 3 uses it
$py = "$HOME\venv-vawm\Scripts\python.exe"
uv pip install --python $py psychopy psychtoolbox
$pipargs = @("-m", "pip", "install")
```

Always pass `--python 3.12`: PsychoPy 2026.2 declares support for 3.10 to 3.12 only, and uv does not stop you from
using a newer one.

### Both routes: confirm and remember

```powershell
& $py --version                                              # 3.10, 3.11 or 3.12
& $py -c "import psychopy; print(psychopy.__version__)"
Set-Content -Path psychopy_path.txt -Value $py               # the .bat files read this, so both ways stay in sync
```

`$py`, `$pipargs` and `$env:` settings last for the current PowerShell window only. In a new window, set `$py`
again (`$py = Get-Content psychopy_path.txt`) and, on route A, `$env:PYTHONUSERBASE` as above.

## 3. Install the fitting stack (SFT only; the GRT experiment does not need it)

```powershell
& $py @pipargs --upgrade pip
& $py @pipargs "pymc>=5.20" nutpie arviz numba pytest
& $py @pipargs --no-deps -e .\adaptiveSFT
& $py -c "import sys, pymc, nutpie, arviz, numba, adaptivesft; print('OK python', sys.version.split()[0], 'pymc', pymc.__version__, 'nutpie', nutpie.__version__)"
```

Takes 3–10 minutes the first time. pip picks the newest versions that support the Python it runs under, so what the
`OK` line shows depends on `& $py --version` (resolved on 2026-11-26):

| Python | PyMC | nutpie | ArviZ |
|---|---|---|---|
| 3.12 | 6.4.0 | 0.16.11 | 1.3.0 |
| 3.11 | 5.28.5 | 0.16.8 | 0.23.4 |
| 3.10 | 5.25.1 | 0.15.2 | 0.23.4 |

All three rows work with the scripts (the 3.12 and 3.10 stacks were run on Linux). Write the versions from the `OK`
line into the lab log. If the last line fails on `nutpie`, send the output of `& $py --version`; the fallback is
`FIT_KW = dict(..., nuts_sampler="pymc")` in `SFT_WM_nochange_EN.py` (slower fits, same model).

## 4. Audio: find and pin the headphones

```powershell
cd Visual_AudioWM
& $py audio_pick.py                       # table of output devices, and the one that would be chosen
& $py audio_pick.py --probe --beep        # also open each device, then play a 1 s tone on the chosen one
& $py audio_pick.py --set "Headphones"    # pin by (part of) the device name -> audio_device.txt
```

- The automatic choice looks for a name containing `headphone`, `headset`, `earphone`, `earbud`, `airpods` or `buds`
  (`audio_pick.py:42`). `Speakers (USB Audio Device)` or a brand-only name does **not** match.
- A device you name yourself is trusted as it is (`audio_pick.py:203`): pin it with `--set`, or pass
  `--audio-device "NAME"`. `--require-headphones` and the GRT script's built-in headphone requirement then pass,
  so there is no reason to drop the flag.

The device name is written into every data row (`audio_device`). Set the system volume once with the tone and do
not touch it afterwards. Turn off Windows audio enhancements and spatial sound for that device (Sound settings →
device properties); they change the noise.

## 5. Check the whole chain

```powershell
& $py debug_adaptivesft_EN.py
$LASTEXITCODE                              # 0 = everything passed
& $py -m pytest -q tests                   # 36 tests, about half a minute; route 2 (1c) only, the bundle has no tests\
```

Nine numbered groups `[0]`–`[8]`: environment and packages, `adaptiveSFT` found, imports, which calibration methods
are available, a simulated calibration without a window, a short real PyMC fit, a window test, the audio device and
calibration settings, and the noise mixer. Every line should start with `✔`; a `✘` line prints the fix. Group `[8]`
must show `SND_SNR_DB = 3.0 (every sound mixed at that SNR)`. That line gets a `✔` whatever the value is
(`debug_adaptivesft_EN.py:364`), so read it: `SND_SNR_DB = None (clean tokens)` means an old bundle (step 1d).

## 6. Run

```powershell
# self-test with a simulated participant, no window, under a minute
& $py SFT_WM_nochange_EN.py --robot --quick

# pure perception, no memory load
& $py sound_perception_EN.py --require-headphones                          # ~7 min, fixed 80 pairs + 40 same, clean speech
& $py sound_perception_EN.py --axis dprime --snr 3 --require-headphones    # the experiment's axis, in +3 dB noise

# SFT experiment: colour calibration -> sound calibration -> practice -> 6 blocks
& $py SFT_WM_nochange_EN.py --require-headphones

# GRT experiment
& $py snr_runtime.py                                 # noise-mixer self-check
& $py GRTv3_ada_EN.py
```

`--robot --quick` overwrites `data\robot_simple_*`, which are tracked in the source repository; in a route-2 (1c)
checkout run `git checkout -- data/` afterwards (the bundle ignores `data\`; nothing to restore there).

**Noise.** Since 2026-11-26 the SFT experiment mixes every speech sound into speech-shaped noise at +3 dB
(`SND_SNR_DB = 3.0`, `SFT_WM_nochange_EN.py:51`; reasons and what has not been measured: `DECISIONS.md` 27 in the
source repository). `sound_perception_EN.py` is clean unless `--snr` is given.

Output lands in `Visual_AudioWM\data\`:

```
 <id>_sound_perception.csv / .json                     default run (clean speech, fixed pairs)
 <id>_sound_perception_dprime_snr3.csv / .json         with --axis dprime --snr 3
 <id>_simple_calib_trials.csv                          every calibration trial (snd_snr_db, snd_seed_* columns)
 <id>_simple_calib.json                                fitted L / H per dimension, 50 % point and plateau with intervals, warnings
 <id>_simple_main.csv                                  main-task probes
 <id>_SFT_WM_<date>.csv / .psydat / .log               PsychoPy's standard files
 <id>_snr\                                             the mixed wavs; delete after copying the csv files
                                                       (each is rebuildable from the SNR and seed logged in its row)
```

Participant data go back to the private Visual_AudioWM repository, never into the public VAWM_run repository
(step 1d).

## 7. The knobs, and where they live

| what | file | line / name |
|---|---|---|
| colour levels, calibration model (ogival + b0), plateau fraction | `adaptive_vawm_EN.py` | `LEVELS_COLOUR`, `CALIB_LINK`, `CALIB_BIAS`, `CALIB_PLATEAU` (lines 109–115) |
| sound levels | `adaptive_vawm_EN.py` | `LEVELS_AUDIO` (line 110) |
| session SNR for the SFT sounds (3.0 dB; None = clean) | `SFT_WM_nochange_EN.py` | `SND_SNR_DB` (line 51) |
| trial counts, response window, fit settings | `SFT_WM_nochange_EN.py` | header, lines 36–55 |

The reasons behind every value are in `DECISIONS.md` of the source repository; the single-source table is
`ARCHITECTURE.md` §3 there. Change a value in one place only.

## 8. If something fails

| symptom | cause | fix |
|---|---|---|
| `pip` SSL / proxy errors | institutional network | add `--proxy http://...` to the pip line, or install from a hotspot once |
| `ModuleNotFoundError: pymc` when run from Coder but not from the terminal (route A) | `PYTHONUSERBASE` differs | step 2 route A: use the folder Coder prints, redo step 3 |
| `No module named pip` (route B) | the venv was made without `--seed` | `& $py -m ensurepip --upgrade` |
| every `& $py ...` line fails at the `&` | new PowerShell window, `$py` is empty | `$py = Get-Content psychopy_path.txt` |
| `audio_pick.py` lists only `Microsoft Sound Mapper` / `Primary Sound Driver` | no PortAudio device named after the headphones | select the headphones in Windows sound settings, pin that generic device with `--set`, confirm with `--beep` |
| window opens then closes at once | an exception before the first frame | run again from the terminal; the traceback is in the window you ran it from |
| `PsychoPy python not found` from a `.bat` | step 2 not done | `psychopy_path.txt` with the path, or run the `.bat` and paste it when asked |
| `SND_SNR_DB = None` in step 1d or in group `[8]` of step 5 | the bundle predates 2026-11-26 | step 1d: get a refreshed bundle, or use route 2 (1c) |
| `ERROR: file or directory not found: tests` | a route-1 bundle, which has no `tests\` | nothing to fix; the tests are in the source repository (1c) |
| `Repository not found` or `Authentication failed` while cloning Visual_AudioWM | the account has no access to the private repository, or the login was not accepted | use route 1, or ask for access |
