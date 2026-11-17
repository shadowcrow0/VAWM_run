@echo off
REM Step 6: the GRT experiment (GRTv3_ada_EN.py): 72 colour + 72 sound calibration trials (Psi), 15 practice, 576 main.
REM Headphones are required (SNR over speakers is not the configured SNR). Add --audio-device "NAME" to force a device,
REM --pilot for a window instead of fullscreen, --list-audio to only list devices. No PyMC needed for this one.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" GRTv3_ada_EN.py %*
pause
