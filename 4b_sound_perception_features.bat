@echo off
REM Step 4b: the same perception test with the Miller-Nicely feature-distance axis (1..5 differing features). ~6 minutes.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
"%PSYCHOPY_PY%" sound_perception_EN.py --axis features --require-headphones %*
pause
