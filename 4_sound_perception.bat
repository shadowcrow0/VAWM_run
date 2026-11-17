@echo off
REM Step 4: pure perception test of the consonant pairs (no memory load, ~6 minutes). Wear the headphones.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" sound_perception_EN.py --require-headphones %*
pause
