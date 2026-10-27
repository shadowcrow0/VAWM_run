@echo off
REM Step 2 (once per machine): install PyMC + nutpie + the adaptiveSFT package into PsychoPy's own package folder.
REM Needs internet. Takes 5-10 minutes.
call "%~dp0Visual_AudioWM\setup_pymc_coder.bat" "%~dp0adaptiveSFT"
