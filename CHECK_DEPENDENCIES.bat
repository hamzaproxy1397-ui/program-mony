@echo off
title Dependency Checker - Arabic Accounting Software

echo ========================================
echo    Dependency and Files Checker
echo    Arabic Accounting Software
echo ========================================
echo.

cd /d "%~dp0"

echo Searching for Python...

REM Try different Python commands
python --version > nul 2>&1
if not errorlevel 1 (
    echo Python found! Running dependency checker...
    python comprehensive_dependency_checker.py
    goto :end
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo Python found via py launcher! Running dependency checker...
    py comprehensive_dependency_checker.py
    goto :end
)

REM Search in common paths
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo Python found at: %%i
        "%%i\python.exe" comprehensive_dependency_checker.py
        goto :end
    )
)

for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo Python found at: %%i
        "%%i\python.exe" comprehensive_dependency_checker.py
        goto :end
    )
)

echo Python not found! Manual file check:
echo.

REM Manual file check without Python
echo Checking critical files manually...

if exist "ui\main_window.py" (
    echo [OK] ui\main_window.py
) else (
    echo [MISSING] ui\main_window.py
)

if exist "ui\login_window.py" (
    echo [OK] ui\login_window.py
) else (
    echo [MISSING] ui\login_window.py
)

if exist "database\hybrid_database_manager.py" (
    echo [OK] database\hybrid_database_manager.py
) else (
    echo [MISSING] database\hybrid_database_manager.py
)

if exist "themes\modern_theme.py" (
    echo [OK] themes\modern_theme.py
) else (
    echo [MISSING] themes\modern_theme.py
)

if exist "config\settings.py" (
    echo [OK] config\settings.py
) else (
    echo [MISSING] config\settings.py
)

if exist "assets\logo\222555.png" (
    echo [OK] assets\logo\222555.png
) else (
    echo [MISSING] assets\logo\222555.png
)

echo.
echo To install Python and run full check:
echo 1. Install Python from: https://www.python.org/downloads/
echo 2. Run: python comprehensive_dependency_checker.py

:end
echo.
pause
