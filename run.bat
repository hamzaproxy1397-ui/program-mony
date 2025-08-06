@echo off
chcp 65001 > nul
title برنامج ست الكل للمحاسبة
echo ============================================================
echo 🏢 برنامج ست الكل للمحاسبة
echo ============================================================
echo.
echo 🔍 فحص Python...
REM التحقق من وجود Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ تم العثور على Python
    echo.
    echo 🚀 جاري تشغيل البرنامج...

    REM تفعيل البيئة الافتراضية إذا كانت موجودة
    if exist "venv" (
        call venv\Scripts\activate.bat
)

    REM تثبيت المتطلبات إذا لم تكن موجودة
    pip install -r requirements.txt >nul 2>&1

    REM تشغيل البرنامج
    python main.py

) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        echo ✅ تم العثور على Python Launcher
echo.
        echo 🚀 جاري تشغيل البرنامج...
        py main.py
    ) else (
        echo ❌ لم يتم العثور على Python
echo.
        echo 📋 الرجاء التأكد من:
        echo    1. تثبيت Python من الموقع الرسمي python.org
        echo    2. تفعيل خيار "Add Python to PATH" أثناء التثبيت
        echo    3. إعادة تشغيل الحاسوب بعد التثبيت
        echo.
        echo 🔑 بيانات تسجيل الدخول:
        echo    اسم المستخدم: 123
        echo    كلمة المرور: 123
        echo.
        pause
        exit /b 1
    )
)
if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في تشغيل البرنامج
    echo 🔍 تحقق من وجود الملفات المطلوبة
    echo.
    pause
) else (
echo.
    echo ✅ تم إغلاق البرنامج بنجاح
)
pause