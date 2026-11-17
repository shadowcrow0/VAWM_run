@echo off
REM Step 5: run the experiment (nochange variant: the non-calibrated dimension is fixed during calibration).
REM Add --audio-device "NAME" to force a device, --require-headphones to refuse speakers.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" SFT_WM_nochange_EN.py --require-headphones %*
pause
