@echo off
REM Quick self-test: no window, simulated participant, short fits. Should finish in a few minutes.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" SFT_WM_nochange_EN.py --robot --quick
pause
