@echo off
REM Step 1: list every audio output device, try to open each one, then play a 1 s tone on the chosen device.
REM Wear the headphones. If you hear the tone, the chosen device is right.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" audio_pick.py --probe --beep %*
pause
