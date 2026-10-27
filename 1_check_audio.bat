@echo off
REM Step 1: list every audio output device, try to open each one, then play a 1 s tone on the chosen device.
REM Wear the headphones. If you hear the tone, the chosen device is right.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" audio_pick.py --probe --beep %*
pause
