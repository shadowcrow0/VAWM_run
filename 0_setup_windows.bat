@echo off
setlocal EnableDelayedExpansion
REM ============================================================================
REM  0_setup_windows.bat  —  one-click setup of a new Windows PC for both experiments.
REM
REM  Does, in order:   1. find PsychoPy's python          2. install PyMC + nutpie + adaptiveSFT (SFT calibration)
REM                    3. list / probe the audio devices,  4. run the SFT diagnostic (debug_adaptivesft_EN.py)
REM                       play a 1 s tone on the chosen one 5. run the GRT sound self-check (snr_runtime.py)
REM  Output: setup_log.txt (everything), setup_sft_check.txt (step 4), audio_devices.json (step 3), next to this file. Re-run as often as you like; each step is idempotent.
REM
REM  Usage:   0_setup_windows.bat                       (auto-detect PsychoPy)
REM           0_setup_windows.bat "D:\PsychoPy"         (PsychoPy installed elsewhere)
REM           0_setup_windows.bat "" "Headphones"       (also pin the headphone device by part of its name)
REM           set SKIP_INSTALL=1 before running to skip step 2 (no internet / already done)
REM ============================================================================
set "ROOT=%~dp0"
set "LOG=%ROOT%setup_log.txt"
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
set "FAILED="
echo ==== VAWM setup %DATE% %TIME% ==== > "%LOG%"

REM ---- 1. PsychoPy python ------------------------------------------------------
set "PY="
if not "%~1"=="" if exist "%~1\python.exe" set "PY=%~1\python.exe"
if not defined PY if exist "C:\Program Files\PsychoPy\python.exe" set "PY=C:\Program Files\PsychoPy\python.exe"
if not defined PY if exist "%LOCALAPPDATA%\Programs\PsychoPy\python.exe" set "PY=%LOCALAPPDATA%\Programs\PsychoPy\python.exe"
if not defined PY for /d %%D in ("C:\Program Files\PsychoPy*") do if exist "%%D\python.exe" set "PY=%%D\python.exe"
if not defined PY (
  echo [1] FAIL  PsychoPy not found. Install standalone PsychoPy ^(Python 3.10^) or pass its folder: 0_setup_windows.bat "D:\PsychoPy"
  echo [1] FAIL  PsychoPy not found >> "%LOG%"
  goto :end
)
echo [1] OK    PsychoPy python: %PY%
echo [1] OK    %PY% >> "%LOG%"
"%PY%" -c "import sys; print('    python', sys.version.split()[0])" 2>>"%LOG%"

REM ---- 2. PyMC + nutpie + adaptiveSFT (SFT only; GRT does not need it) ----------
if "%SKIP_INSTALL%"=="1" (
  echo [2] SKIP  install ^(SKIP_INSTALL=1^)
) else (
  echo [2] ...   installing PyMC, numba, arviz, nutpie and adaptiveSFT into %PYTHONUSERBASE%  ^(5-10 min, needs internet^)
  "%PY%" -m pip install --user pymc numba arviz nutpie >> "%LOG%" 2>&1 || set "FAILED=!FAILED! install"
  "%PY%" -m pip install --user --no-deps -e "%ROOT%adaptiveSFT" >> "%LOG%" 2>&1 || set "FAILED=!FAILED! adaptiveSFT"
  "%PY%" -c "import pymc, nutpie, adaptivesft; print('[2] OK    pymc', pymc.__version__, 'nutpie', nutpie.__version__)" 2>>"%LOG%" || (
    echo [2] FAIL  PyMC / nutpie / adaptiveSFT import failed - see setup_log.txt & set "FAILED=!FAILED! import")
)

REM ---- 3. audio: list, probe, tone (and pin if a name was given) -----------------
cd /d "%ROOT%Visual_AudioWM"
if not "%~2"=="" (
  echo [3] ...   pinning audio device "%~2"
  "%PY%" audio_pick.py --set "%~2" --beep
  echo [3] pinned "%~2" >> "%LOG%"
)
echo [3] ...   audio devices ^(wear the headphones; you should hear a 1 s tone on the chosen device^)
"%PY%" audio_pick.py --probe --beep --json "%ROOT%audio_devices.json"
if errorlevel 1 (
  echo [3] WARN  no usable audio device, or the chosen one failed to open ^(table saved to audio_devices.json^)
  echo [3] WARN  audio >> "%LOG%"
  set "FAILED=!FAILED! audio"
) else (
  echo [3] OK    audio device opened and tone played ^(if you did not hear it, pin the right one: 1b_set_audio.bat "name"^)
  echo [3] OK    audio >> "%LOG%"
)

REM ---- 4. SFT diagnostic ------------------------------------------------------------
echo [4] ...   SFT diagnostic ^(imports, d' table, simulated calibration, one short fit, audio^)
"%PY%" debug_adaptivesft_EN.py > "%ROOT%setup_sft_check.txt" 2>&1
if errorlevel 1 (
  echo [4] FAIL  the SFT diagnostic found problems - open setup_sft_check.txt, the lines marked with a cross say what to do
  type "%ROOT%setup_sft_check.txt" | findstr /c:"DEBUG finished"
  set "FAILED=!FAILED! sft-check"
) else (echo [4] OK    SFT chain ^(details: setup_sft_check.txt^))
type "%ROOT%setup_sft_check.txt" >> "%LOG%"

REM ---- 5. GRT sound self-check ------------------------------------------------------
echo [5] ...   GRT sound mixing self-check
"%PY%" snr_runtime.py >> "%LOG%" 2>&1
if errorlevel 1 (echo [5] FAIL  snr_runtime.py failed - see setup_log.txt & set "FAILED=!FAILED! grt-audio") else (echo [5] OK    GRT sound mixing)

:end
echo.
if defined FAILED (
  echo ==== NOT READY: problems in: %FAILED%   ^(details: %LOG%^)
  echo ==== NOT READY: %FAILED% >> "%LOG%"
) else (
  echo ==== READY. Next: 4_sound_perception.bat / 5_run_experiment.bat ^(SFT^), 6_run_grt.bat ^(GRT^).
  echo ==== READY >> "%LOG%"
)
echo Log: %LOG%
pause
endlocal
