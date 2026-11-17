@echo off
REM Step 3: one-click diagnostic of the whole calibration chain (imports, short model fit, audio device).
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" debug_adaptivesft_EN.py
pause
