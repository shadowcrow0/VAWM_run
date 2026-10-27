@echo off
REM Step 3: one-click diagnostic of the whole calibration chain (imports, short model fit, dry run).
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" debug_adaptivesft_EN.py
pause
