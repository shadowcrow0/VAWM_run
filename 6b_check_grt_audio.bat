@echo off
REM Step 6b: self-check of the GRT sound pipeline (mix a few stimuli at exact SNRs, verify the realised SNR). ~1 s, no window.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" snr_runtime.py
pause
