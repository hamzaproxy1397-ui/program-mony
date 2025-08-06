@echo off
chcp 65001 > nul
title لوحة التحكم المركزية المطورة

echo.
echo ========================================
echo 🎛️ لوحة التحكم المركزية المطورة
echo ========================================
echo.
echo 🚀 تشغيل البرنامج...
echo.

REM محاولة تشغيل بطرق مختلفة
python test_advanced_control_panel.py
if %errorlevel% equ 0 goto success

py test_advanced_control_panel.py  
if %errorlevel% equ 0 goto success

python3 test_advanced_control_panel.py
if %errorlevel% equ 0 goto success

C:\Python\python.exe test_advanced_control_panel.py
if %errorlevel% equ 0 goto success

C:\Python39\python.exe test_advanced_control_panel.py
if %errorlevel% equ 0 goto success

C:\Python310\python.exe test_advanced_control_panel.py
if %errorlevel% equ 0 goto success

C:\Python311\python.exe test_advanced_control_panel.py
if %errorlevel% equ 0 goto success

C:\Python312\python.exe test_advanced_control_panel.py
if %errorlevel% equ 0 goto success

echo.
echo ❌ لم يتم العثور على Python
echo.
echo 💡 حلول مقترحة:
echo 1. تأكد من تثبيت Python من: https://python.org
echo 2. أضف Python إلى متغير PATH
echo 3. أعد تشغيل الكمبيوتر بعد التثبيت
echo 4. جرب النقر المزدوج على test_advanced_control_panel.py
echo.
goto end

:success
echo.
echo ✅ تم تشغيل البرنامج بنجاح!
echo.

:end
pause
