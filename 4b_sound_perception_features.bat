@echo off
REM Step 4b: the same perception test with the Miller-Nicely feature-distance axis (1..5 differing features). ~6 minutes.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" sound_perception_EN.py --axis features --require-headphones %*
pause
