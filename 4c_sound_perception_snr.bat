@echo off
REM Step 4c: the SNR pilot (DECISIONS 24). Same perception test as step 4 on the d' axis, both syllables in
REM speech-shaped noise at one SNR. Run it three times (0, -6, -12 dB), same participant id; each run saves
REM data\<id>_sound_perception_dprime_snr<dB>.csv. Wear the headphones.
call "%~dp0_env.bat" || (pause & exit /b 1)
cd /d "%~dp0Visual_AudioWM"
set "SNR=%~1"
if "%SNR%"=="" set /p SNR=SNR in dB (0, -6 or -12): 
"%PSYCHOPY_PY%" sound_perception_EN.py --axis dprime --snr %SNR% --require-headphones
pause
