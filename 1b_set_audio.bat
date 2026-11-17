@echo off
REM Remember the headphone device for all experiment scripts. Usage:  1b_set_audio.bat "Headphones"
if "%~1"=="" (echo Usage: 1b_set_audio.bat "part of the device name"   e.g. 1b_set_audio.bat "Headphones" & pause & exit /b 1)
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" audio_pick.py --set %1 --beep
pause
