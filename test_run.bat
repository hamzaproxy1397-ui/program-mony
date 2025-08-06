@echo off
chcp 65001 > nul
title اختبار تشغيل برنامج ست الكل للمحاسبة

echo ========================================
echo    اختبار تشغيل برنامج ست الكل للمحاسبة
echo ========================================
echo.

echo جاري البحث عن Python...

REM محاولة العثور على Python بطرق مختلفة
python --version > nul 2>&1
if not errorlevel 1 (
    echo ✅ تم العثور على Python
    echo جاري تشغيل الاختبار...
    python test_main_window.py
    goto :end
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo ✅ تم العثور على Python عبر py launcher
    echo جاري تشغيل الاختبار...
    py test_main_window.py
    goto :end
)

python3 --version > nul 2>&1
if not errorlevel 1 (
    echo ✅ تم العثور على Python3
    echo جاري تشغيل الاختبار...
    python3 test_main_window.py
    goto :end
)

REM البحث في مسارات شائعة
if exist "C:\Python*\python.exe" (
    echo ✅ تم العثور على Python في C:\Python
    for /d %%i in ("C:\Python*") do (
        "%%i\python.exe" test_main_window.py
        goto :end
    )
)

if exist "%LOCALAPPDATA%\Programs\Python\Python*\python.exe" (
    echo ✅ تم العثور على Python في AppData
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        "%%i\python.exe" test_main_window.py
        goto :end
    )
)

echo ❌ لم يتم العثور على Python
echo.
echo يرجى تثبيت Python من:
echo https://www.python.org/downloads/
echo.
echo أو تشغيل الملف مباشرة إذا كان Python مثبت:
echo python test_main_window.py

:end
echo.
echo اضغط أي مفتاح للخروج...
pause > nul
