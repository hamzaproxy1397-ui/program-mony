@echo off
chcp 65001 >nul
title 🎨 النافذة الرئيسية الأصلية - برنامج ست الكل للمحاسبة
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🎨 النافذة الرئيسية الأصلية                 ║
echo ║              📊 برنامج ست الكل للمحاسبة                   ║
echo ║                                                              ║
echo ║                   ✨ التصميم الأصلي الكامل                 ║
echo ║                   🎯 جميع المكونات الأصلية                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 فحص Python...

REM فحص Python
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر
    set PYTHON_CMD=python
    goto :run_original
)

py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر عبر py launcher
    set PYTHON_CMD=py
    goto :run_original
)

echo ❌ Python غير مثبت!
echo.
echo 📥 يرجى تثبيت Python أولاً من: https://www.python.org/downloads/
goto :end

:run_original
echo.
echo 🎨 تشغيل النافذة الأصلية الكاملة...
echo.
echo 📋 مكونات النافذة الأصلية:
echo    🔝 الشريط العلوي مع القائمة والبحث
echo    🟢 الشريط الأخضر مع 6 أيقونات سريعة
echo    🎯 منطقة الأيقونات الرئيسية (18 وظيفة)
echo    👤 معلومات المستخدم في الأسفل
echo    📊 الشريط السفلي مع شريط المهام
echo.
echo 🎉 التصميم الأصلي المتقدم والكامل
echo.

timeout /t 3 >nul

%PYTHON_CMD% تشغيل_النافذة_الأصلية.py

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في تشغيل النافذة الأصلية
    echo.
    echo 💡 جاري المحاولة مع ملفات بديلة...
    
    if exist "main.py" (
        echo 🔄 محاولة تشغيل main.py...
        %PYTHON_CMD% main.py
    ) else (
        echo ❌ لم يتم العثور على ملفات بديلة
    )
)

echo.
echo ✅ تم إغلاق النافذة الأصلية

:end
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  🎨 النافذة الأصلية المكتملة               ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  ✅ الشريط العلوي: قائمة تنقل + شريط بحث                  ║
echo ║  🟢 الشريط الأخضر: 6 أيقونات سريعة ملونة                 ║
echo ║  🎯 الأيقونات الرئيسية: 18 وظيفة في 3 صفوف              ║
echo ║  👤 معلومات المستخدم: صورة شخصية + بيانات                ║
echo ║  📊 الشريط السفلي: شريط مهام مع أيقونات                   ║
echo ║  🎨 التصميم: أصلي ومتقدم وكامل                           ║
echo ║  ⚡ الأداء: محسن ومستقر                                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo اضغط أي مفتاح للخروج...
pause >nul
