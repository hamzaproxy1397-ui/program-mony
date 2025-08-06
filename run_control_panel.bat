@echo off
chcp 65001 > nul
title لوحة التحكم المركزية المطورة

echo ========================================
echo 🎛️ لوحة التحكم المركزية المطورة
echo ========================================
echo.

echo 🔍 فحص Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    echo 💡 يرجى تثبيت Python من: https://python.org
    pause
    exit /b 1
)

echo ✅ Python متوفر
echo.

echo 🔍 فحص customtkinter...
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ customtkinter غير مثبت
    echo 📦 تثبيت customtkinter...
    pip install customtkinter
    if %errorlevel% neq 0 (
        echo ❌ فشل في تثبيت customtkinter
        pause
        exit /b 1
    )
)

echo ✅ customtkinter متوفر
echo.

echo 🚀 تشغيل لوحة التحكم المطورة...
echo ========================================
echo.

python test_advanced_control_panel.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ حدث خطأ في تشغيل البرنامج
    echo 🔍 تحقق من الأخطاء أعلاه
    pause
) else (
    echo.
    echo ✅ تم إغلاق البرنامج بنجاح
)

pause
