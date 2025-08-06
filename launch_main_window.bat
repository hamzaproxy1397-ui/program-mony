@echo off
title Accounting Software - Main Window

echo ========================================
echo    Accounting Software - Main Window
echo ========================================
echo.

cd /d "%~dp0"

echo Searching for Python...

python --version > nul 2>&1
if not errorlevel 1 (
    echo Python found!
    echo Starting main window...
    echo.
    python run_main_window.py
    goto :end
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo Python found via py launcher!
    echo Starting main window...
    echo.
    py run_main_window.py
    goto :end
)

python3 --version > nul 2>&1
if not errorlevel 1 (
    echo Python3 found!
    echo Starting main window...
    echo.
    python3 run_main_window.py
    goto :end
)

echo Python not found!
echo.
echo Please install Python from: https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation
echo.
echo After installing Python, install requirements:
echo pip install customtkinter pillow numpy
echo.

:end
echo.
pause
