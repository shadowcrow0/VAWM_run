@echo off
REM Step 4: run the experiment (English version, fixed targets during calibration).
REM Add --audio-device "NAME" to force a device, --require-headphones to refuse speakers.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" SFT_WM_nochange_EN.py --require-headphones %*
pause
