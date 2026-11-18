@echo off
REM Shared by every .bat in this folder: find PsychoPy's python.exe and set PSYCHOPY_PY / PYTHONUSERBASE.
REM Search order (first hit wins):
REM   1. PSYCHOPY_PY already set in the environment
REM   2. psychopy_path.txt next to this file (one line: full path to python.exe; written by step 5 below)
REM   3. the usual install folders, any version suffix, machine-wide or per-user
REM   4. a recursive search of those folders (newer PsychoPy builds keep python.exe in a subfolder)
REM   5. ask: paste the path printed by  import sys; print(sys.executable)  in PsychoPy Coder's Shell;
REM      the answer is saved to psychopy_path.txt so you are asked only once.
if defined PSYCHOPY_PY if exist "%PSYCHOPY_PY%" goto :found

if exist "%~dp0psychopy_path.txt" set /p PSYCHOPY_PY=<"%~dp0psychopy_path.txt"
if defined PSYCHOPY_PY if exist "%PSYCHOPY_PY%" goto :found
set "PSYCHOPY_PY="

for %%P in ("C:\Program Files\PsychoPy\python.exe" "%LOCALAPPDATA%\Programs\PsychoPy\python.exe" "%ProgramFiles(x86)%\PsychoPy\python.exe" "C:\PsychoPy\python.exe") do (
  if not defined PSYCHOPY_PY if exist "%%~P" set "PSYCHOPY_PY=%%~P"
)
if defined PSYCHOPY_PY goto :found

for %%D in ("C:\Program Files\PsychoPy*" "%LOCALAPPDATA%\Programs\PsychoPy*" "%ProgramFiles(x86)%\PsychoPy*" "C:\PsychoPy*") do (
  if not defined PSYCHOPY_PY if exist "%%~D\python.exe" set "PSYCHOPY_PY=%%~D\python.exe"
)
if defined PSYCHOPY_PY goto :found

for %%D in ("C:\Program Files\PsychoPy*" "%LOCALAPPDATA%\Programs\PsychoPy*" "%ProgramFiles(x86)%\PsychoPy*" "C:\PsychoPy*") do (
  if not defined PSYCHOPY_PY if exist "%%~D\" for /f "delims=" %%F in ('dir /s /b "%%~D\python.exe" 2^>nul') do if not defined PSYCHOPY_PY set "PSYCHOPY_PY=%%F"
)
if defined PSYCHOPY_PY goto :found

echo.
echo PsychoPy's python.exe was not found in the usual places.
echo Open PsychoPy Coder, click the "Shell" tab at the bottom, and run:
echo     import sys; print(sys.executable)
echo Then paste the printed path here (it ends with python.exe).
set /p PSYCHOPY_PY=Path: 
if not exist "%PSYCHOPY_PY%" (echo Not found: "%PSYCHOPY_PY%" & exit /b 1)
> "%~dp0psychopy_path.txt" echo %PSYCHOPY_PY%
echo Saved to psychopy_path.txt - you will not be asked again.

:found
set "PYTHONUSERBASE=%APPDATA%\psychopy3\packages"
exit /b 0
