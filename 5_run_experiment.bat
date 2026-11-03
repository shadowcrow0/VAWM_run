@echo off
REM Step 5: run the experiment (nochange variant: the non-calibrated dimension is fixed during calibration).
REM Add --audio-device "NAME" to force a device, --require-headphones to refuse speakers.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" SFT_WM_nochange_EN.py --require-headphones %*
pause
