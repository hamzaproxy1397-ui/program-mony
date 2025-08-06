#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فاحص شامل للتبعيات والملفات الداعمة للبرنامج المحاسبي
Comprehensive Dependency and Support Files Checker for Arabic Accounting Software
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path
from typing import List, Dict, Set, Tuple
import traceback

class ComprehensiveDependencyChecker:
    """فاحص شامل للتبعيات والملفات الداعمة"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.missing_files = []
        self.missing_imports = []
        self.broken_references = []
        self.created_files = []
        
        # قائمة الملفات المطلوبة من main_window.py
        self.required_ui_files = [
            'ui/login_window.py',
            'ui/window_utils.py',
            'ui/simple_welcome_window.py',
            'ui/warehouses_management_window.py',
            'ui/purchases_window.py',
            'ui/sales_window.py',
            'ui/reports_window.py',
            'ui/advanced_financial_reports_window.py',
            'ui/accounts_window.py',
            'ui/journal_entries_window.py',
            'ui/add_items_window.py',
            'ui/categories_management_window.py',
            'ui/units_management_window.py',
            'ui/stock_management_window.py',
            'ui/user_management.py',
            'ui/hr_management_window.py',
            'ui/invoices_main_window.py',
            'ui/central_control_panel.py'
        ]
        
        self.required_database_files = [
            'database/hybrid_database_manager.py',
            'database/database_manager.py',
            'database/accounts_manager.py',
            'database/products_manager.py',
            'database/invoices_manager.py',
            'database/reports_manager.py'
        ]
        
        self.required_config_files = [
            'themes/theme_manager.py',
            'themes/modern_theme.py',
            'config/settings.py',
            'core/error_handler.py',
            'core/barcode_scanner.py'
        ]
        
        self.required_packages = [
            'customtkinter',
            'PIL',
            'numpy',
            'matplotlib'
        ]

    def check_file_exists(self, file_path: str) -> bool:
        """فحص وجود ملف"""
        full_path = self.project_root / file_path
        return full_path.exists()

    def check_all_required_files(self) -> Dict[str, List[str]]:
        """فحص جميع الملفات المطلوبة"""
        results = {
            'ui_files': {'missing': [], 'existing': []},
            'database_files': {'missing': [], 'existing': []},
            'config_files': {'missing': [], 'existing': []},
            'asset_files': {'missing': [], 'existing': []}
        }
        
        # فحص ملفات UI
        for file_path in self.required_ui_files:
            if self.check_file_exists(file_path):
                results['ui_files']['existing'].append(file_path)
            else:
                results['ui_files']['missing'].append(file_path)
                self.missing_files.append(file_path)
        
        # فحص ملفات قاعدة البيانات
        for file_path in self.required_database_files:
            if self.check_file_exists(file_path):
                results['database_files']['existing'].append(file_path)
            else:
                results['database_files']['missing'].append(file_path)
                self.missing_files.append(file_path)
        
        # فحص ملفات التكوين
        for file_path in self.required_config_files:
            if self.check_file_exists(file_path):
                results['config_files']['existing'].append(file_path)
            else:
                results['config_files']['missing'].append(file_path)
                self.missing_files.append(file_path)
        
        # فحص ملفات الأصول
        asset_files = [
            'assets/logo/222555.png',
            'assets/icons/6.png',
            'assets/icons/3.png',
            'assets/icons/23.png',
            'assets/icons/26.png',
            'assets/icons/53.ico',
            'assets/icons/12.png'
        ]
        
        for file_path in asset_files:
            if self.check_file_exists(file_path):
                results['asset_files']['existing'].append(file_path)
            else:
                results['asset_files']['missing'].append(file_path)
                self.missing_files.append(file_path)
        
        return results

    def check_python_packages(self) -> Dict[str, bool]:
        """فحص المكتبات المطلوبة"""
        package_status = {}
        
        for package in self.required_packages:
            try:
                if package == 'PIL':
                    import PIL
                else:
                    __import__(package)
                package_status[package] = True
            except ImportError:
                package_status[package] = False
                self.missing_imports.append(package)
        
        return package_status

    def create_missing_ui_file(self, file_path: str) -> bool:
        """إنشاء ملف UI مفقود"""
        try:
            full_path = self.project_root / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # استخراج اسم الكلاس من اسم الملف
            file_name = Path(file_path).stem
            class_name = ''.join(word.capitalize() for word in file_name.split('_'))
            
            content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{file_name.replace('_', ' ').title()} - نافذة {file_name.replace('_', ' ')}
{class_name} Window for Arabic Accounting Software
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Any

class {class_name}:
    """
    نافذة {file_name.replace('_', ' ')}
    {class_name} Window
    """
    
    def __init__(self, parent: Optional[ctk.CTk] = None, db_manager: Optional[Any] = None):
        """
        تهيئة النافذة
        Initialize the window
        """
        self.parent = parent
        self.db_manager = db_manager
        self.window = None
        
        self.create_window()
    
    def create_window(self) -> None:
        """إنشاء النافذة"""
        self.window = ctk.CTkToplevel(self.parent) if self.parent else ctk.CTk()
        self.window.title("{file_name.replace('_', ' ').title()}")
        self.window.geometry("800x600")
        
        # إنشاء المحتوى
        self.create_content()
    
    def create_content(self) -> None:
        """إنشاء محتوى النافذة"""
        # إطار رئيسي
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # عنوان
        title_label = ctk.CTkLabel(
            main_frame,
            text="{file_name.replace('_', ' ').title()}",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=20)
        
        # رسالة مؤقتة
        info_label = ctk.CTkLabel(
            main_frame,
            text="هذه النافذة قيد التطوير\\nThis window is under development",
            font=("Arial", 14)
        )
        info_label.pack(pady=20)
        
        # أزرار
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)
        
        close_button = ctk.CTkButton(
            button_frame,
            text="إغلاق / Close",
            command=self.close_window
        )
        close_button.pack(side="left", padx=10)
    
    def close_window(self) -> None:
        """إغلاق النافذة"""
        if self.window:
            self.window.destroy()
    
    def show(self) -> None:
        """عرض النافذة"""
        if self.window:
            self.window.mainloop()

# للاختبار المباشر
if __name__ == "__main__":
    app = {class_name}()
    app.show()
'''
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.created_files.append(file_path)
            print(f"✅ تم إنشاء: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ فشل في إنشاء {file_path}: {e}")
            return False

    def create_missing_database_file(self, file_path: str) -> bool:
        """إنشاء ملف قاعدة بيانات مفقود"""
        try:
            full_path = self.project_root / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_name = Path(file_path).stem
            class_name = ''.join(word.capitalize() for word in file_name.split('_'))
            
            content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{file_name.replace('_', ' ').title()} - مدير {file_name.replace('_', ' ')}
{class_name} for Arabic Accounting Software
"""

import sqlite3
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

class {class_name}:
    """
    مدير {file_name.replace('_', ' ')}
    {class_name} Manager
    """
    
    def __init__(self, db_path: str = "database/accounting.db"):
        """
        تهيئة مدير قاعدة البيانات
        Initialize database manager
        """
        self.db_path = db_path
        self.connection = None
        self.setup_logging()
        self.connect()
    
    def setup_logging(self) -> None:
        """إعداد نظام السجلات"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def connect(self) -> bool:
        """الاتصال بقاعدة البيانات"""
        try:
            # إنشاء مجلد قاعدة البيانات إذا لم يكن موجوداً
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.logger.info(f"تم الاتصال بقاعدة البيانات: {{self.db_path}}")
            return True
            
        except Exception as e:
            self.logger.error(f"خطأ في الاتصال بقاعدة البيانات: {{e}}")
            return False
    
    def execute_query(self, query: str, params: Tuple = ()) -> Optional[List[Dict]]:
        """تنفيذ استعلام"""
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                results = [dict(row) for row in cursor.fetchall()]
                return results
            else:
                self.connection.commit()
                return None
                
        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ الاستعلام: {{e}}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def close(self) -> None:
        """إغلاق الاتصال"""
        if self.connection:
            self.connection.close()
            self.logger.info("تم إغلاق اتصال قاعدة البيانات")

# للاختبار المباشر
if __name__ == "__main__":
    manager = {class_name}()
    print("تم إنشاء مدير قاعدة البيانات بنجاح")
    manager.close()
'''
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.created_files.append(file_path)
            print(f"✅ تم إنشاء: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ فشل في إنشاء {file_path}: {e}")
            return False

    def create_missing_config_file(self, file_path: str) -> bool:
        """إنشاء ملف تكوين مفقود"""
        try:
            full_path = self.project_root / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)

            if file_path == 'core/error_handler.py':
                content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج الأخطاء المحسن
Enhanced Error Handler for Arabic Accounting Software
"""

import logging
import traceback
from typing import Any, Callable, Optional
from functools import wraps

# إعداد نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def error_handler(func: Callable) -> Callable:
    """مُزخرف لمعالجة الأخطاء"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"خطأ في {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            return None
    return wrapper

class DatabaseErrorHandler:
    """معالج أخطاء قاعدة البيانات"""

    @staticmethod
    def handle_db_error(operation: str, error: Exception, critical: bool = False):
        """معالجة أخطاء قاعدة البيانات"""
        error_msg = f"خطأ في عملية قاعدة البيانات '{operation}': {error}"
        if critical:
            logger.critical(error_msg)
        else:
            logger.error(error_msg)

db_error_handler = DatabaseErrorHandler()

def setup_global_exception_handler():
    """إعداد معالج الاستثناءات العام"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("استثناء غير معالج", exc_info=(exc_type, exc_value, exc_traceback))

    import sys
    sys.excepthook = handle_exception

def handle_ui_error(error: Exception, context: str = ""):
    """معالجة أخطاء واجهة المستخدم"""
    logger.error(f"خطأ في واجهة المستخدم {context}: {error}")

def handle_db_operation(operation: str):
    """مُزخرف لمعالجة عمليات قاعدة البيانات"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                db_error_handler.handle_db_error(operation, e)
                return None
        return wrapper
    return decorator

def log_error(message: str):
    """تسجيل خطأ"""
    logger.error(message)

def log_info(message: str):
    """تسجيل معلومة"""
    logger.info(message)

def log_warning(message: str):
    """تسجيل تحذير"""
    logger.warning(message)
'''

            elif file_path == 'core/barcode_scanner.py':
                content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ماسح الباركود
Barcode Scanner for Arabic Accounting Software
"""

import logging
from typing import Optional, Callable

class BarcodeScanner:
    """
    ماسح الباركود
    Barcode Scanner Class
    """

    def __init__(self):
        """تهيئة ماسح الباركود"""
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.callback = None

    def connect(self) -> bool:
        """الاتصال بماسح الباركود"""
        try:
            # محاولة الاتصال بماسح الباركود
            # هذا مثال بسيط - يمكن تطويره لاحقاً
            self.is_connected = True
            self.logger.info("تم الاتصال بماسح الباركود")
            return True
        except Exception as e:
            self.logger.error(f"فشل في الاتصال بماسح الباركود: {e}")
            return False

    def set_callback(self, callback: Callable[[str], None]):
        """تعيين دالة الاستدعاء عند قراءة باركود"""
        self.callback = callback

    def scan(self) -> Optional[str]:
        """قراءة باركود"""
        if not self.is_connected:
            self.logger.warning("ماسح الباركود غير متصل")
            return None

        # محاكاة قراءة باركود
        # في التطبيق الحقيقي، هذا سيقرأ من الجهاز
        return None

    def disconnect(self):
        """قطع الاتصال"""
        self.is_connected = False
        self.logger.info("تم قطع الاتصال مع ماسح الباركود")
'''

            else:
                # ملف تكوين عام
                content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{Path(file_path).stem.replace('_', ' ').title()}
Configuration file for Arabic Accounting Software
"""

# إعدادات افتراضية
DEFAULT_SETTINGS = {{
    "app_name": "برنامج ست الكل للمحاسبة",
    "version": "1.0.0",
    "language": "ar",
    "theme": "modern"
}}

# تصدير الإعدادات
__all__ = ['DEFAULT_SETTINGS']
'''

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.created_files.append(file_path)
            print(f"✅ تم إنشاء: {file_path}")
            return True

        except Exception as e:
            print(f"❌ فشل في إنشاء {file_path}: {e}")
            return False

    def install_missing_packages(self) -> bool:
        """تثبيت المكتبات المفقودة"""
        if not self.missing_imports:
            return True

        try:
            import subprocess
            import sys

            for package in self.missing_imports:
                package_name = 'Pillow' if package == 'PIL' else package
                print(f"تثبيت {package_name}...")

                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package_name
                ], capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"✅ تم تثبيت {package_name}")
                else:
                    print(f"❌ فشل في تثبيت {package_name}: {result.stderr}")
                    return False

            return True

        except Exception as e:
            print(f"❌ خطأ في تثبيت المكتبات: {e}")
            return False

    def run_comprehensive_check(self) -> Dict[str, Any]:
        """تشغيل فحص شامل وإصلاح المشاكل"""
        print("🔍 بدء الفحص الشامل للتبعيات والملفات الداعمة...")
        print("=" * 60)

        # 1. فحص الملفات المطلوبة
        print("\n📁 فحص الملفات المطلوبة...")
        file_results = self.check_all_required_files()

        # 2. فحص المكتبات
        print("\n📦 فحص المكتبات المطلوبة...")
        package_results = self.check_python_packages()

        # 3. إنشاء الملفات المفقودة
        print("\n🔧 إنشاء الملفات المفقودة...")

        # إنشاء ملفات UI
        for file_path in file_results['ui_files']['missing']:
            self.create_missing_ui_file(file_path)

        # إنشاء ملفات قاعدة البيانات
        for file_path in file_results['database_files']['missing']:
            self.create_missing_database_file(file_path)

        # إنشاء ملفات التكوين
        for file_path in file_results['config_files']['missing']:
            self.create_missing_config_file(file_path)

        # 4. تثبيت المكتبات المفقودة
        print("\n📦 تثبيت المكتبات المفقودة...")
        packages_installed = self.install_missing_packages()

        # 5. إنشاء المجلدات المطلوبة
        print("\n📁 إنشاء المجلدات المطلوبة...")
        required_dirs = ['logs', 'reports/generated', 'backups', 'assets/icons', 'assets/logo']
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ تم إنشاء مجلد: {dir_path}")

        # تقرير نهائي
        results = {
            'files_checked': file_results,
            'packages_checked': package_results,
            'files_created': self.created_files,
            'packages_installed': packages_installed,
            'missing_files_count': len(self.missing_files),
            'missing_packages_count': len(self.missing_imports),
            'success': len(self.missing_files) == 0 and packages_installed
        }

        return results

def main():
    """الدالة الرئيسية"""
    print("🔍 فاحص شامل للتبعيات والملفات الداعمة")
    print("=" * 50)

    checker = ComprehensiveDependencyChecker()
    results = checker.run_comprehensive_check()

    print("\n" + "=" * 60)
    print("📊 تقرير الفحص النهائي:")
    print("=" * 60)

    print(f"📁 الملفات المفحوصة:")
    for category, files in results['files_checked'].items():
        print(f"   {category}: {len(files['existing'])} موجود، {len(files['missing'])} مفقود")

    print(f"\n📦 المكتبات المفحوصة:")
    for package, status in results['packages_checked'].items():
        status_text = "✅ مثبت" if status else "❌ مفقود"
        print(f"   {package}: {status_text}")

    print(f"\n🔧 الملفات المُنشأة: {len(results['files_created'])}")
    for file_path in results['files_created']:
        print(f"   ✅ {file_path}")

    if results['success']:
        print("\n🎉 تم إصلاح جميع المشاكل بنجاح!")
        print("✅ البرنامج جاهز للتشغيل")
    else:
        print("\n⚠️ هناك مشاكل تحتاج إصلاح يدوي")

    input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
