@echo off
title Arabic Accounting Software - Error Handler

echo ========================================
echo    Arabic Accounting Software
echo    With Error Detection and Fixing
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Python installation...

REM Try to find Python
python --version > nul 2>&1
if not errorlevel 1 (
    echo Python found! Version:
    python --version
    goto :check_requirements
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo Python found via py launcher! Version:
    py --version
    set PYTHON_CMD=py
    goto :check_requirements
)

REM Search in common paths
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo Python found at: %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :check_requirements
    )
)

for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo Python found at: %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :check_requirements
    )
)

echo ERROR: Python not found!
echo Please install Python from: https://www.python.org/downloads/
goto :end

:check_requirements
echo.
echo Step 2: Checking required packages...

if not defined PYTHON_CMD set PYTHON_CMD=python

%PYTHON_CMD% -c "import customtkinter" > nul 2>&1
if errorlevel 1 (
    echo Installing customtkinter...
    %PYTHON_CMD% -m pip install customtkinter
)

%PYTHON_CMD% -c "import PIL" > nul 2>&1
if errorlevel 1 (
    echo Installing Pillow...
    %PYTHON_CMD% -m pip install Pillow
)

%PYTHON_CMD% -c "import numpy" > nul 2>&1
if errorlevel 1 (
    echo Installing numpy...
    %PYTHON_CMD% -m pip install numpy
)

echo.
echo Step 3: Checking file integrity...

if not exist "main.py" (
    echo ERROR: main.py not found!
    goto :end
)

if not exist "ui\main_window.py" (
    echo ERROR: ui\main_window.py not found!
    goto :end
)

echo.
echo Step 4: Running syntax check...
%PYTHON_CMD% -m py_compile main.py > nul 2>&1
if errorlevel 1 (
    echo ERROR: Syntax error in main.py
    echo Running error fixer...
    %PYTHON_CMD% -c "
import ast
import sys
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
    print('main.py syntax is OK')
except SyntaxError as e:
    print(f'Syntax error in main.py: {e}')
    print(f'Line {e.lineno}: {e.text}')
except Exception as e:
    print(f'Error checking main.py: {e}')
"
)

echo.
echo Step 5: Starting application...
echo.
echo Login credentials:
echo Username: admin
echo Password: admin
echo.

%PYTHON_CMD% main.py

if errorlevel 1 (
    echo.
    echo Application exited with error. Checking logs...
    if exist "logs\app.log" (
        echo Last 10 lines of log:
        powershell "Get-Content logs\app.log -Tail 10"
    )
    goto :end
)

echo.
echo Application closed successfully!
goto :end

:end
echo.
echo Press any key to exit...
pause > nul
