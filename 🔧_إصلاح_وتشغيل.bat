@echo off
chcp 65001 > nul
title إصلاح وتشغيل البرنامج المحاسبي

echo ========================================
echo    🔧 إصلاح وتشغيل البرنامج المحاسبي
echo    🏢 برنامج ست الكل للمحاسبة
echo ========================================
echo.

cd /d "%~dp0"

echo 🔍 بدء عملية الإصلاح والتشغيل...

REM محاولة تشغيل أداة الإصلاح
python fix_and_run.py
if not errorlevel 1 goto :success

REM محاولة بـ py launcher
py fix_and_run.py
if not errorlevel 1 goto :success

REM البحث عن Python في المسارات الشائعة
echo 🔍 البحث عن Python...

for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ وُجد Python في: %%i
        "%%i\python.exe" fix_and_run.py
        if not errorlevel 1 goto :success
    )
)

for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ وُجد Python في: %%i
        "%%i\python.exe" fix_and_run.py
        if not errorlevel 1 goto :success
    )
)

REM إذا فشل كل شيء
echo ❌ فشل في العثور على Python أو تشغيل البرنامج
echo.
echo 💡 الحلول المقترحة:
echo    1. ثبت Python من: https://www.python.org/downloads/
echo    2. تأكد من تحديد "Add Python to PATH" أثناء التثبيت
echo    3. أعد تشغيل الكمبيوتر بعد التثبيت
echo    4. جرب تشغيل هذا الملف مرة أخرى
echo.
goto :end

:success
echo ✅ تم تشغيل البرنامج بنجاح!

:end
echo.
pause
