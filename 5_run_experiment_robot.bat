@echo off
REM Quick self-test: no window, simulated participant, short fits. Should finish in a few minutes.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" SFT_WM_nochange_EN.py --robot --quick
pause
