@echo off
chcp 65001 >nul
title 🚀 تشغيل النافذة الرئيسية - برنامج ست الكل للمحاسبة
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 تشغيل النافذة الرئيسية                   ║
echo ║              📊 برنامج ست الكل للمحاسبة                   ║
echo ║                                                              ║
echo ║                    ⚡ تشغيل مباشر وسريع                    ║
echo ║                   🎯 بدون نافذة تسجيل دخول                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 فحص Python...

REM فحص Python
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر
    goto :run_main_window
)

py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر عبر py launcher
    set PYTHON_CMD=py
    goto :run_main_window
)

echo ❌ Python غير مثبت!
echo.
echo 📥 يرجى تثبيت Python أولاً من: https://www.python.org/downloads/
goto :end

:run_main_window
echo.
echo 🚀 تشغيل النافذة الرئيسية مباشرة...
echo.
echo 📋 معلومات التشغيل:
echo    🎯 تشغيل مباشر بدون تسجيل دخول
echo    👤 المستخدم الافتراضي: admin
echo    🔧 الصلاحيات: مدير النظام
echo    ⚡ تشغيل سريع ومحسن
echo.

timeout /t 2 >nul

if defined PYTHON_CMD (
    %PYTHON_CMD% تشغيل_النافذة_الرئيسية.py
) else (
    python تشغيل_النافذة_الرئيسية.py
)

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في تشغيل النافذة الرئيسية
    echo.
    echo 💡 جاري المحاولة مع البرنامج الكامل...
    echo.
    
    if defined PYTHON_CMD (
        %PYTHON_CMD% main.py
    ) else (
        python main.py
    )
)

echo.
echo ✅ تم إغلاق النافذة الرئيسية

:end
echo.
echo اضغط أي مفتاح للخروج...
pause >nul
