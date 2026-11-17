@echo off
REM Step 6b: self-check of the GRT sound pipeline (mix a few stimuli at exact SNRs, verify the realised SNR). ~1 s, no window.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" snr_runtime.py
pause
