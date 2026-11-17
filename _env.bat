@echo off
REM Shared by every .bat in this folder: where PsychoPy's python is and where its user packages live.
REM Edit ONLY this file if PsychoPy is installed somewhere else.
set "PSYCHOPY_PY=C:\Program Files\PsychoPy\python.exe"
if not exist "%PSYCHOPY_PY%" if exist "%LOCALAPPDATA%\Programs\PsychoPy\python.exe" set "PSYCHOPY_PY=%LOCALAPPDATA%\Programs\PsychoPy\python.exe"
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
if not exist "%PSYCHOPY_PY%" (echo PsychoPy python not found: %PSYCHOPY_PY%  - edit _env.bat & exit /b 1)
exit /b 0
