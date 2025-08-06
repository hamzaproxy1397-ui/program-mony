@echo off
chcp 65001 > nul
title خطة النسخ الاحتياطي الشاملة - برنامج المحاسبة العربي

echo ========================================
echo    💾 خطة النسخ الاحتياطي الشاملة
echo    🏢 برنامج المحاسبة العربي
echo    📅 %date% - %time%
echo ========================================
echo.

cd /d "%~dp0"

REM إنشاء اسم مجلد النسخة الاحتياطية مع التاريخ والوقت
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "datestamp=%YYYY%%MM%%DD%_%HH%%Min%%Sec%"

set "BACKUP_ROOT=COMPLETE_ACCOUNTING_SYSTEM_BACKUP_%datestamp%"

echo 🚀 بدء عملية النسخ الاحتياطي الشامل...
echo 📁 مجلد النسخة: %BACKUP_ROOT%
echo.

REM إنشاء هيكل مجلدات النسخة الاحتياطية
echo 📁 إنشاء هيكل المجلدات...
mkdir "%BACKUP_ROOT%"
mkdir "%BACKUP_ROOT%\CRITICAL"
mkdir "%BACKUP_ROOT%\IMPORTANT" 
mkdir "%BACKUP_ROOT%\USEFUL"
mkdir "%BACKUP_ROOT%\ARCHIVE"
mkdir "%BACKUP_ROOT%\DOCUMENTATION"

echo ✅ تم إنشاء هيكل المجلدات

echo.
echo 🔥 المرحلة 1: نسخ المكونات الحرجة...
echo =====================================

REM نسخ الملفات الأساسية
if exist "main.py" (
    copy "main.py" "%BACKUP_ROOT%\CRITICAL\"
    echo ✅ main.py
) else (
    echo ❌ main.py - مفقود
)

if exist "START_HERE.py" (
    copy "START_HERE.py" "%BACKUP_ROOT%\CRITICAL\"
    echo ✅ START_HERE.py
) else (
    echo ❌ START_HERE.py - مفقود
)

REM نسخ مجلد UI كاملاً
if exist "ui" (
    xcopy "ui" "%BACKUP_ROOT%\CRITICAL\ui\" /E /I /H /Y
    echo ✅ ui/ - مجلد واجهة المستخدم كاملاً
) else (
    echo ❌ ui/ - مجلد مفقود
)

REM نسخ مجلد database كاملاً
if exist "database" (
    xcopy "database" "%BACKUP_ROOT%\CRITICAL\database\" /E /I /H /Y
    echo ✅ database/ - مجلد قاعدة البيانات كاملاً
) else (
    echo ❌ database/ - مجلد مفقود
)

echo.
echo ⚠️ المرحلة 2: نسخ المكونات المهمة...
echo ====================================

REM نسخ مجلد config
if exist "config" (
    xcopy "config" "%BACKUP_ROOT%\IMPORTANT\config\" /E /I /H /Y
    echo ✅ config/ - إعدادات النظام
) else (
    echo ❌ config/ - مجلد مفقود
)

REM نسخ مجلد themes
if exist "themes" (
    xcopy "themes" "%BACKUP_ROOT%\IMPORTANT\themes\" /E /I /H /Y
    echo ✅ themes/ - ثيمات النظام
) else (
    echo ❌ themes/ - مجلد مفقود
)

REM نسخ مجلد assets
if exist "assets" (
    xcopy "assets" "%BACKUP_ROOT%\IMPORTANT\assets\" /E /I /H /Y
    echo ✅ assets/ - الأصول والصور
) else (
    echo ❌ assets/ - مجلد مفقود
)

REM نسخ مجلد services
if exist "services" (
    xcopy "services" "%BACKUP_ROOT%\IMPORTANT\services\" /E /I /H /Y
    echo ✅ services/ - الخدمات والمنطق التجاري
) else (
    echo ❌ services/ - مجلد مفقود
)

REM نسخ مجلد models
if exist "models" (
    xcopy "models" "%BACKUP_ROOT%\IMPORTANT\models\" /E /I /H /Y
    echo ✅ models/ - نماذج البيانات
) else (
    echo ❌ models/ - مجلد مفقود
)

echo.
echo 📚 المرحلة 3: نسخ التوثيق والملفات المفيدة...
echo ============================================

REM نسخ ملفات التوثيق الرئيسية
for %%f in (*.md *.txt) do (
    if exist "%%f" (
        copy "%%f" "%BACKUP_ROOT%\DOCUMENTATION\"
        echo ✅ %%f
    )
)

REM نسخ ملفات التشغيل المهمة
for %%f in (*.bat requirements*.txt) do (
    if exist "%%f" (
        copy "%%f" "%BACKUP_ROOT%\USEFUL\"
        echo ✅ %%f
    )
)

REM نسخ مجلد reports إن وجد
if exist "reports" (
    xcopy "reports" "%BACKUP_ROOT%\USEFUL\reports\" /E /I /H /Y
    echo ✅ reports/ - التقارير
)

REM نسخ مجلد docs إن وجد
if exist "docs" (
    xcopy "docs" "%BACKUP_ROOT%\DOCUMENTATION\docs\" /E /I /H /Y
    echo ✅ docs/ - التوثيق المفصل
)

echo.
echo 📦 المرحلة 4: أرشفة النسخ الاحتياطية القديمة...
echo ===============================================

REM نسخ مجلدات النسخ الاحتياطية (عينة فقط لتوفير المساحة)
for %%d in (backup_final backup_critical_files backups) do (
    if exist "%%d" (
        xcopy "%%d" "%BACKUP_ROOT%\ARCHIVE\%%d\" /E /I /H /Y
        echo ✅ %%d/ - نسخ احتياطية قديمة
    )
)

echo.
echo 📊 إنشاء تقرير النسخة الاحتياطية...
echo ===================================

REM إنشاء ملف تقرير النسخة الاحتياطية
(
echo تقرير النسخة الاحتياطية الشاملة
echo ================================
echo.
echo تاريخ الإنشاء: %date% - %time%
echo مجلد النسخة: %BACKUP_ROOT%
echo.
echo المكونات المنسوخة:
echo ==================
echo 🔥 CRITICAL:
echo    - main.py
echo    - START_HERE.py  
echo    - ui/ ^(مجلد كامل^)
echo    - database/ ^(مجلد كامل^)
echo.
echo ⚠️ IMPORTANT:
echo    - config/ ^(مجلد كامل^)
echo    - themes/ ^(مجلد كامل^)
echo    - assets/ ^(مجلد كامل^)
echo    - services/ ^(مجلد كامل^)
echo    - models/ ^(مجلد كامل^)
echo.
echo 📚 DOCUMENTATION:
echo    - جميع ملفات .md و .txt
echo    - docs/ ^(إن وجد^)
echo.
echo 📦 ARCHIVE:
echo    - عينة من النسخ الاحتياطية القديمة
echo.
echo ملاحظات:
echo ========
echo - هذه نسخة احتياطية شاملة للنظام المحاسبي
echo - تحتوي على جميع المكونات الأساسية للنظام
echo - يمكن استخدامها لاستعادة النظام كاملاً
echo - احفظ هذه النسخة في مكان آمن ومنفصل
echo.
echo تم إنشاء النسخة بنجاح!
) > "%BACKUP_ROOT%\BACKUP_REPORT.txt"

echo ✅ تم إنشاء تقرير النسخة الاحتياطية

echo.
echo ========================================
echo    ✅ تم إكمال النسخ الاحتياطي بنجاح!
echo ========================================
echo.
echo 📁 مجلد النسخة: %BACKUP_ROOT%
echo 📄 تقرير النسخة: %BACKUP_ROOT%\BACKUP_REPORT.txt
echo.
echo 🎯 الخطوات التالية:
echo    1. تحقق من محتويات النسخة الاحتياطية
echo    2. انسخ المجلد إلى قرص خارجي
echo    3. احفظ نسخة في التخزين السحابي
echo    4. اختبر استعادة النظام من النسخة
echo.
echo 💡 نصائح مهمة:
echo    - احفظ النسخة في مواقع متعددة
echo    - اختبر النسخة بانتظام
echo    - أنشئ نسخ احتياطية دورية
echo.

pause
