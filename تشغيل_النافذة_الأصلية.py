#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل النافذة الرئيسية الأصلية للبرنامج المحاسبي
Original Main Window Launcher for Accounting Software

استعادة النافذة الأصلية الكاملة مع جميع المكونات:
- الشريط العلوي مع القائمة والبحث
- الشريط الأخضر مع 6 أيقونات سريعة  
- منطقة الأيقونات الرئيسية مع 18 وظيفة (3×6)
- معلومات المستخدم في الأسفل
- الشريط السفلي
"""

import sys
import os
import importlib.util
from pathlib import Path

def setup_environment():
    """إعداد البيئة والمسارات للنافذة الأصلية"""
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    # إضافة جميع المسارات المطلوبة للنافذة الأصلية
    paths_to_add = [
        str(project_root),
        str(project_root / "ui"),
        str(project_root / "ui" / "views"),
        str(project_root / "ui" / "components"),
        str(project_root / "themes"),
        str(project_root / "config"),
        str(project_root / "database"),
        str(project_root / "core"),
        str(project_root / "assets"),
        str(project_root / "assets" / "icons")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"📁 مجلد المشروع: {project_root}")
    return project_root

def check_dependencies():
    """فحص المكتبات المطلوبة للنافذة الأصلية"""
    print("\n📦 فحص المكتبات المطلوبة للنافذة الأصلية...")
    
    required = {
        'customtkinter': 'واجهة المستخدم الحديثة',
        'tkinter': 'واجهة المستخدم الأساسية',
        'PIL': 'معالجة الصور والأيقونات'
    }
    
    optional = {
        'numpy': 'معالجة الصور المتقدمة',
        'matplotlib': 'الرسوم البيانية'
    }
    
    missing = []
    for module, desc in required.items():
        try:
            if module == 'PIL':
                from PIL import Image, ImageTk
            else:
                __import__(module)
            print(f"✅ {module} - {desc}")
        except ImportError:
            print(f"❌ {module} - {desc} (مطلوب)")
            missing.append(module)
    
    for module, desc in optional.items():
        try:
            __import__(module)
            print(f"✅ {module} - {desc}")
        except ImportError:
            print(f"⚠️ {module} - {desc} (اختياري)")
    
    if missing:
        print(f"\n❌ مكتبات مطلوبة مفقودة: {', '.join(missing)}")
        print("💡 لتثبيت المكتبات المطلوبة:")
        print("   pip install customtkinter pillow")
        return False
    
    return True

def create_missing_files():
    """إنشاء الملفات المفقودة المطلوبة للنافذة الأصلية"""
    print("\n🔧 فحص وإنشاء الملفات المطلوبة...")
    
    # إنشاء مجلدات إذا لم تكن موجودة
    directories = [
        "assets",
        "assets/icons",
        "logs",
        "core"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 تم إنشاء مجلد: {directory}")
    
    # إنشاء ملفات مفقودة بسيطة
    missing_files = {
        "core/__init__.py": "# Core package",
        "core/scheduler_manager.py": '''# -*- coding: utf-8 -*-
"""مدير المهام المجدولة - مبسط"""

class SchedulerManager:
    def __init__(self):
        pass
    
    def start(self):
        pass
    
    def stop(self):
        pass
''',
        "core/error_handler.py": '''# -*- coding: utf-8 -*-
"""معالج الأخطاء - مبسط"""

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"خطأ في {func.__name__}: {e}")
            return None
    return wrapper

def db_error_handler(func):
    return error_handler(func)

def setup_global_exception_handler():
    pass

def handle_ui_error(error):
    print(f"خطأ في الواجهة: {error}")

def handle_db_operation(func):
    return error_handler(func)

def log_error(message):
    print(f"خطأ: {message}")

def log_info(message):
    print(f"معلومات: {message}")

def log_warning(message):
    print(f"تحذير: {message}")
''',
        "core/barcode_scanner.py": '''# -*- coding: utf-8 -*-
"""ماسح الباركود - مبسط"""

class BarcodeScanner:
    def __init__(self):
        pass
    
    def scan(self):
        return None
'''
    }
    
    for file_path, content in missing_files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📄 تم إنشاء ملف: {file_path}")

def load_original_main_window():
    """تحميل النافذة الرئيسية الأصلية"""
    print("\n🎯 تحميل النافذة الرئيسية الأصلية...")
    
    try:
        # تحميل النافذة الأصلية من ui/views/main_window.py
        from ui.views.main_window import MainApplication
        print("✅ تم تحميل MainApplication الأصلية بنجاح")
        return MainApplication
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد النافذة الأصلية: {e}")
        
        # محاولة إصلاح الاستيراد
        try:
            print("🔄 محاولة إصلاح الاستيراد...")
            
            # تحميل الملف مباشرة
            spec = importlib.util.spec_from_file_location(
                "main_window", 
                "ui/views/main_window.py"
            )
            module = importlib.util.module_from_spec(spec)
            
            # إضافة الوحدة إلى sys.modules لحل مشاكل الاستيراد
            sys.modules['ui.views.main_window'] = module
            
            spec.loader.exec_module(module)
            
            if hasattr(module, 'MainApplication'):
                print("✅ تم تحميل MainApplication بعد الإصلاح")
                return module.MainApplication
                
        except Exception as e2:
            print(f"❌ فشل في إصلاح الاستيراد: {e2}")
    
    return None

def run_original_application():
    """تشغيل التطبيق الأصلي"""
    print("\n🚀 بدء تشغيل النافذة الأصلية...")
    
    try:
        # إعداد البيئة
        setup_environment()
        
        # فحص المكتبات
        if not check_dependencies():
            return False
        
        # إنشاء الملفات المفقودة
        create_missing_files()
        
        # تحميل النافذة الأصلية
        MainApplication = load_original_main_window()
        if not MainApplication:
            print("❌ فشل في تحميل النافذة الأصلية")
            return False
        
        # إنشاء وتشغيل التطبيق الأصلي
        print("🎉 إنشاء التطبيق الأصلي...")
        app = MainApplication()
        
        # تعيين مستخدم افتراضي
        app.current_user = {
            'username': 'admin',
            'full_name': 'مدير النظام',
            'role': 'admin',
            'user_id': 1
        }
        
        print("✅ تم إعداد المستخدم الافتراضي")
        print("\n" + "="*70)
        print("🎉 مرحباً بك في برنامج ست الكل للمحاسبة - النافذة الأصلية")
        print("📊 النافذة الأصلية الكاملة جاهزة للاستخدام")
        print("🎨 الشريط الأخضر + 18 وظيفة + الشريط السفلي")
        print("🔐 تم تسجيل الدخول كمدير النظام")
        print("="*70)
        
        # تشغيل النافذة الأصلية مباشرة
        app.create_main_window()
        
        print("\n✅ تم إغلاق النافذة الأصلية بنجاح")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البرنامج بواسطة المستخدم")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل النافذة الأصلية: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🎨 استعادة النافذة الرئيسية الأصلية")
    print("="*70)
    
    success = run_original_application()
    
    if not success:
        print("\n💡 نصائح لحل المشاكل:")
        print("   1. تأكد من تثبيت Python")
        print("   2. ثبت المكتبات: pip install customtkinter pillow")
        print("   3. تأكد من وجود ملف ui/views/main_window.py")
        print("   4. جرب تشغيل: python main.py")
        
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
