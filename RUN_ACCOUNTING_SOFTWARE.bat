@echo off
title Arabic Accounting Software

echo ========================================
echo    Arabic Accounting Software
echo    Set Al-Kol Accounting System
echo ========================================
echo.

cd /d "%~dp0"

echo Checking for Python installation...

REM Try different Python commands
python --version > nul 2>&1
if not errorlevel 1 (
    echo Python found! Starting application...
    echo.
    python main.py
    goto :success
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo Python found via py launcher! Starting application...
    echo.
    py main.py
    goto :success
)

python3 --version > nul 2>&1
if not errorlevel 1 (
    echo Python3 found! Starting application...
    echo.
    python3 main.py
    goto :success
)

REM Python not found
echo.
echo ERROR: Python is not installed or not found in PATH
echo.
echo SOLUTION:
echo 1. Install Python from: https://www.python.org/downloads/
echo 2. During installation, check "Add Python to PATH"
echo 3. After installation, run: pip install customtkinter pillow numpy
echo 4. Then run this file again
echo.
echo Alternative: Double-click on START_HERE.py if Python is installed
echo.
goto :end

:success
echo.
echo Application closed successfully.
goto :end

:end
echo.
echo Press any key to exit...
pause > nul
