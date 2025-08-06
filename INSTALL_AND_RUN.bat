@echo off
title Arabic Accounting Software - Auto Installer

echo ========================================
echo    Arabic Accounting Software
echo    Automatic Installation and Setup
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Checking for Python...

REM Try to find Python in various ways
python --version > nul 2>&1
if not errorlevel 1 (
    echo Python found! Proceeding to setup...
    goto :setup
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo Python found via py launcher! Proceeding to setup...
    set PYTHON_CMD=py
    goto :setup
)

REM Check Microsoft Store Python
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    echo Microsoft Store Python found!
    set PYTHON_CMD="%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    goto :setup
)

REM Search in common installation paths
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo Python found at: %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :setup
    )
)

for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo Python found at: %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :setup
    )
)

REM Python not found - offer installation options
echo.
echo Python not found on this system!
echo.
echo Choose installation method:
echo 1. Download and install Python manually
echo 2. Install via Microsoft Store (Windows 10/11)
echo 3. Try to run anyway (if Python is installed but not in PATH)
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto :manual_install
if "%choice%"=="2" goto :store_install
if "%choice%"=="3" goto :try_anyway
if "%choice%"=="4" goto :end

:manual_install
echo.
echo Opening Python download page...
start https://www.python.org/downloads/
echo.
echo Instructions:
echo 1. Download the latest Python version
echo 2. During installation, CHECK "Add Python to PATH"
echo 3. Complete the installation
echo 4. Run this script again
echo.
goto :end

:store_install
echo.
echo Opening Microsoft Store...
start ms-windows-store://pdp/?productid=9NRWMJP3717K
echo.
echo Instructions:
echo 1. Install Python from Microsoft Store
echo 2. After installation, run this script again
echo.
goto :end

:try_anyway
echo.
echo Trying to run the application anyway...
START_HERE.py
if not errorlevel 1 (
    echo Application started successfully!
    goto :end
)

main.py
if not errorlevel 1 (
    echo Application started successfully!
    goto :end
)

echo Failed to start application.
echo Please install Python first.
goto :end

:setup
if not defined PYTHON_CMD set PYTHON_CMD=python

echo.
echo Step 2: Installing required packages...

echo Installing customtkinter...
%PYTHON_CMD% -m pip install customtkinter --quiet
if errorlevel 1 (
    echo Failed to install customtkinter
    echo Trying with --user flag...
    %PYTHON_CMD% -m pip install --user customtkinter --quiet
)

echo Installing Pillow...
%PYTHON_CMD% -m pip install Pillow --quiet
if errorlevel 1 (
    echo Failed to install Pillow
    echo Trying with --user flag...
    %PYTHON_CMD% -m pip install --user Pillow --quiet
)

echo Installing numpy...
%PYTHON_CMD% -m pip install numpy --quiet
if errorlevel 1 (
    echo Failed to install numpy
    echo Trying with --user flag...
    %PYTHON_CMD% -m pip install --user numpy --quiet
)

echo.
echo Step 3: Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "database" mkdir database
if not exist "reports" mkdir reports
if not exist "backups" mkdir backups

echo.
echo Step 4: Running diagnostic check...
%PYTHON_CMD% quick_diagnostic.py

echo.
echo Step 5: Starting application...
echo.
echo Default login credentials:
echo Username: admin
echo Password: admin
echo.
echo Starting in 3 seconds...
timeout /t 3 > nul

%PYTHON_CMD% main.py

if errorlevel 1 (
    echo.
    echo Application exited with error.
    echo Running error checker...
    %PYTHON_CMD% error_checker_and_fixer.py
    echo.
    echo Try running the application again.
    goto :end
)

echo.
echo Application closed successfully!
goto :end

:end
echo.
echo Press any key to exit...
pause > nul
