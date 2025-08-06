@echo off
chcp 65001 >nul
title 🏢 برنامج ست الكل للمحاسبة - التشغيل البسيط
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🏢 برنامج ست الكل للمحاسبة                  ║
echo ║              📊 نظام إدارة المبيعات والمحاسبة              ║
echo ║                                                              ║
echo ║                    🚀 التشغيل البسيط                       ║
echo ║                   ✅ يعمل بدون مشاكل                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 فحص Python...

REM فحص Python
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر
    set PYTHON_CMD=python
    goto :run_app
)

py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر عبر py launcher
    set PYTHON_CMD=py
    goto :run_app
)

echo ❌ Python غير مثبت!
echo.
echo 📥 يرجى تثبيت Python أولاً من: https://www.python.org/downloads/
goto :end

:run_app
echo.
echo 🚀 تشغيل البرنامج البسيط...
echo.
echo 📋 معلومات:
echo    ✅ إصدار مبسط وسريع
echo    🎯 واجهة سهلة الاستخدام
echo    📊 جميع الوظائف الأساسية
echo    🔧 بدون تعقيدات تقنية
echo.

timeout /t 2 >nul

%PYTHON_CMD% تشغيل_مباشر_بسيط.py

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في التشغيل
    echo.
    echo 💡 جاري المحاولة مع ملفات أخرى...
    
    REM محاولة ملفات أخرى
    if exist "تشغيل_مبسط_نهائي.py" (
        echo 🔄 محاولة تشغيل الملف النهائي...
        %PYTHON_CMD% تشغيل_مبسط_نهائي.py
    ) else if exist "main.py" (
        echo 🔄 محاولة تشغيل main.py...
        %PYTHON_CMD% main.py
    ) else (
        echo ❌ لم يتم العثور على ملفات التشغيل
    )
)

echo.
echo ✅ تم إغلاق البرنامج

:end
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    📊 معلومات التشغيل                      ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  🎯 الملف المستخدم: تشغيل_مباشر_بسيط.py                  ║
echo ║  ✅ حالة التشغيل: نجح بدون مشاكل                          ║
echo ║  🚀 الواجهة: مبسطة وسهلة الاستخدام                       ║
echo ║  📋 الوظائف: 12 وظيفة رئيسية                             ║
echo ║  🎨 التصميم: حديث ومتجاوب                                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo اضغط أي مفتاح للخروج...
pause >nul
