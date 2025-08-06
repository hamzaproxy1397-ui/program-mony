@echo off
chcp 65001 > nul
title 🏢 برنامج ست الكل للمحاسبة - التشغيل النهائي

echo ========================================
echo    🏢 برنامج ست الكل للمحاسبة
echo    📊 نظام إدارة المبيعات والمحاسبة
echo    ✨ الإصدار النهائي المحسن
echo ========================================
echo.

cd /d "%~dp0"

echo 🔍 فحص النظام...

REM فحص Python أولاً
python --version > nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر
    goto :run_checks
)

py --version > nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر عبر py launcher
    set PYTHON_CMD=py
    goto :run_checks
)

REM البحث في المسارات الشائعة
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Python موجود في: %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :run_checks
    )
)

for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Python موجود في: %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :run_checks
    )
)

REM Python غير موجود
echo ❌ Python غير مثبت!
echo.
echo 📥 يرجى تثبيت Python أولاً:
echo    1. اذهب إلى: https://www.python.org/downloads/
echo    2. حمل أحدث إصدار
echo    3. تأكد من تحديد "Add Python to PATH"
echo    4. أعد تشغيل هذا الملف
echo.
goto :end

:run_checks
if not defined PYTHON_CMD set PYTHON_CMD=python

echo 🔧 فحص التبعيات والملفات...
%PYTHON_CMD% -c "
import sys
print('✅ Python version:', sys.version.split()[0])

# فحص المكتبات الأساسية
try:
    import customtkinter
    print('✅ customtkinter متوفر')
except ImportError:
    print('❌ customtkinter مفقود - سيتم تثبيته')

try:
    from PIL import Image
    print('✅ PIL/Pillow متوفر')
except ImportError:
    print('❌ PIL/Pillow مفقود - سيتم تثبيته')

try:
    import numpy
    print('✅ numpy متوفر')
except ImportError:
    print('❌ numpy مفقود - سيتم تثبيته')

# فحص الملفات الأساسية
import os
files_to_check = [
    'ui/main_window.py',
    'ui/login_window.py', 
    'database/hybrid_database_manager.py',
    'themes/modern_theme.py',
    'config/settings.py'
]

missing_files = []
for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f'✅ {file_path}')
    else:
        print(f'❌ {file_path}')
        missing_files.append(file_path)

if missing_files:
    print(f'❌ ملفات مفقودة: {len(missing_files)}')
    sys.exit(1)
else:
    print('✅ جميع الملفات الأساسية موجودة')
    sys.exit(0)
"

if errorlevel 1 (
    echo.
    echo ⚠️ هناك ملفات أو مكتبات مفقودة
    echo 🔧 تشغيل الإصلاح التلقائي...
    %PYTHON_CMD% comprehensive_dependency_checker.py
    echo.
)

echo 📦 تثبيت/تحديث المكتبات المطلوبة...
%PYTHON_CMD% -m pip install --upgrade customtkinter pillow numpy matplotlib --quiet

echo.
echo 🚀 تشغيل البرنامج المحاسبي...
echo.
echo 🔐 بيانات تسجيل الدخول الافتراضية:
echo    👤 اسم المستخدم: admin
echo    🔑 كلمة المرور: admin
echo.
echo 📝 ملاحظات:
echo    - لإغلاق البرنامج: أغلق النافذة أو اضغط Alt+F4
echo    - في حالة عدم ظهور النافذة: تحقق من شريط المهام
echo    - للمساعدة: راجع ملف "اقرأني_أولاً.txt"
echo.

timeout /t 3 > nul

REM تشغيل البرنامج
%PYTHON_CMD% main.py

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في تشغيل البرنامج
    echo 🔧 تشغيل التشخيص...
    %PYTHON_CMD% quick_diagnostic.py
    echo.
    echo 💡 للمساعدة:
    echo    - راجع ملف logs/app.log
    echo    - شغل error_checker_and_fixer.py
    echo    - راجع FINAL_DEPENDENCY_AUDIT_REPORT.md
    goto :end
)

echo.
echo ✅ تم إغلاق البرنامج بنجاح!
goto :end

:end
echo.
echo اضغط أي مفتاح للخروج...
pause > nul
