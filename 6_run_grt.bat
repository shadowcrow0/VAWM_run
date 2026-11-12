@echo off
REM Step 6: the GRT experiment (GRTv3_ada_EN.py): 72 colour + 72 sound calibration trials (Psi), 15 practice, 576 main.
REM Headphones are required (SNR over speakers is not the configured SNR). Add --audio-device "NAME" to force a device,
REM --pilot for a window instead of fullscreen, --list-audio to only list devices. No PyMC needed for this one.
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
cd /d "%~dp0Visual_AudioWM"
"C:\Program Files\PsychoPy\python.exe" GRTv3_ada_EN.py %*
pause
