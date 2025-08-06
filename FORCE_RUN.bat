@echo off
title Arabic Accounting Software - Force Run

echo ========================================
echo    Arabic Accounting Software
echo    Force Run - Searching All Paths
echo ========================================
echo.

cd /d "%~dp0"

echo Searching for Python in common locations...

REM Try standard commands first
python --version > nul 2>&1
if not errorlevel 1 (
    echo Found Python! Starting application...
    python main.py
    goto :success
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo Found Python via py launcher! Starting application...
    py main.py
    goto :success
)

python3 --version > nul 2>&1
if not errorlevel 1 (
    echo Found Python3! Starting application...
    python3 main.py
    goto :success
)

REM Search in common Python installation paths
echo Searching in Program Files...
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo Found Python at: %%i
        "%%i\python.exe" main.py
        goto :success
    )
)

echo Searching in Program Files (x86)...
for /d %%i in ("C:\Program Files (x86)\Python*") do (
    if exist "%%i\python.exe" (
        echo Found Python at: %%i
        "%%i\python.exe" main.py
        goto :success
    )
)

echo Searching in AppData Local...
for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo Found Python at: %%i
        "%%i\python.exe" main.py
        goto :success
    )
)

echo Searching in AppData Roaming...
for /d %%i in ("%APPDATA%\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo Found Python at: %%i
        "%%i\python.exe" main.py
        goto :success
    )
)

REM Try Microsoft Store Python
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    echo Found Microsoft Store Python!
    "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" main.py
    goto :success
)

REM Try Anaconda/Miniconda
if exist "%USERPROFILE%\Anaconda3\python.exe" (
    echo Found Anaconda Python!
    "%USERPROFILE%\Anaconda3\python.exe" main.py
    goto :success
)

if exist "%USERPROFILE%\Miniconda3\python.exe" (
    echo Found Miniconda Python!
    "%USERPROFILE%\Miniconda3\python.exe" main.py
    goto :success
)

REM Last resort - try to run the .py file directly
echo Trying to run Python file directly...
START_HERE.py
if not errorlevel 1 goto :success

main.py
if not errorlevel 1 goto :success

REM If all fails
echo.
echo ========================================
echo    PYTHON NOT FOUND ANYWHERE!
echo ========================================
echo.
echo Please install Python from one of these sources:
echo.
echo 1. Official Python: https://www.python.org/downloads/
echo 2. Microsoft Store: Search for "Python" in Microsoft Store
echo 3. Anaconda: https://www.anaconda.com/products/distribution
echo.
echo IMPORTANT: During installation, make sure to:
echo - Check "Add Python to PATH"
echo - Install for all users (if possible)
echo.
echo After installation, run this command:
echo pip install customtkinter pillow numpy matplotlib
echo.
goto :end

:success
echo.
echo Application finished successfully!
goto :end

:end
echo.
echo Press any key to exit...
pause > nul
