@echo off
REM Step 4: pure perception test of the consonant pairs (no memory load, ~6 minutes). Wear the headphones.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" sound_perception_EN.py --require-headphones %*
pause
