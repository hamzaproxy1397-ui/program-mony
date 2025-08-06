@echo off
chcp 65001 > nul
title النافذة الرئيسية - برنامج ست الكل للمحاسبة

echo ========================================
echo    🏢 برنامج ست الكل للمحاسبة
echo    📊 النافذة الرئيسية مباشرة
echo ========================================
echo.

cd /d "%~dp0"

echo 🚀 تشغيل النافذة الرئيسية مباشرة...

REM محاولة تشغيل البرنامج بطرق مختلفة
python تشغيل_النافذة_الرئيسية_مباشرة.py
if not errorlevel 1 goto :success

py تشغيل_النافذة_الرئيسية_مباشرة.py
if not errorlevel 1 goto :success

REM البحث في مسارات Python الشائعة
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        "%%i\python.exe" تشغيل_النافذة_الرئيسية_مباشرة.py
        if not errorlevel 1 goto :success
    )
)

for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        "%%i\python.exe" تشغيل_النافذة_الرئيسية_مباشرة.py
        if not errorlevel 1 goto :success
    )
)

echo ❌ فشل في تشغيل البرنامج
echo 💡 جرب تشغيل: python main.py
goto :end

:success
echo ✅ تم تشغيل النافذة الرئيسية بنجاح!

:end
echo.
pause
