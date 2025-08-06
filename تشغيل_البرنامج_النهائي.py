#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل البرنامج المحاسبي النهائي
Final Accounting Software Launcher

ملف تشغيل نهائي ومحسن للبرنامج المحاسبي
"""

import sys
import os
import importlib.util
from pathlib import Path

def setup_environment():
    """إعداد البيئة والمسارات"""
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    # إضافة جميع المسارات المطلوبة
    paths_to_add = [
        str(project_root),
        str(project_root / "ui"),
        str(project_root / "ui" / "views"),
        str(project_root / "themes"),
        str(project_root / "config"),
        str(project_root / "database")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"📁 مجلد المشروع: {project_root}")
    return project_root

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات...")
    
    required = {
        'customtkinter': 'واجهة المستخدم الحديثة',
        'tkinter': 'واجهة المستخدم الأساسية',
        'PIL': 'معالجة الصور'
    }
    
    missing = []
    for module, desc in required.items():
        try:
            if module == 'PIL':
                from PIL import Image
            else:
                __import__(module)
            print(f"✅ {module} - {desc}")
        except ImportError:
            print(f"❌ {module} - {desc} (مفقود)")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️ مكتبات مفقودة: {', '.join(missing)}")
        print("💡 لتثبيت المكتبات:")
        print("   pip install customtkinter pillow")
        return False
    
    return True

def load_main_application():
    """تحميل التطبيق الرئيسي"""
    print("\n🎯 تحميل التطبيق الرئيسي...")
    
    # محاولة تحميل من مسارات مختلفة
    possible_paths = [
        "ui/views/main_window.py",
        "ui/main_window.py",
        "main_window.py"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"📄 وجد ملف: {path}")
            try:
                # تحميل الملف مباشرة
                spec = importlib.util.spec_from_file_location("main_window", path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # البحث عن فئة MainApplication
                if hasattr(module, 'MainApplication'):
                    print("✅ تم تحميل MainApplication بنجاح")
                    return module.MainApplication
                    
            except Exception as e:
                print(f"❌ خطأ في تحميل {path}: {e}")
                continue
    
    return None

def run_application():
    """تشغيل التطبيق"""
    print("\n🚀 بدء تشغيل البرنامج...")
    
    try:
        # إعداد البيئة
        setup_environment()
        
        # فحص المكتبات
        if not check_dependencies():
            return False
        
        # تحميل التطبيق
        MainApplication = load_main_application()
        if not MainApplication:
            print("❌ فشل في تحميل التطبيق الرئيسي")
            return False
        
        # إنشاء وتشغيل التطبيق
        print("🎉 إنشاء التطبيق...")
        app = MainApplication()
        
        # تعيين مستخدم افتراضي
        app.current_user = {
            'username': 'admin',
            'full_name': 'مدير النظام',
            'role': 'admin',
            'user_id': 1
        }
        
        print("✅ تم إعداد المستخدم الافتراضي")
        print("\n" + "="*60)
        print("🎉 مرحباً بك في برنامج ست الكل للمحاسبة")
        print("📊 البرنامج جاهز للاستخدام")
        print("🔐 تم تسجيل الدخول كمدير النظام")
        print("="*60)
        
        # تشغيل التطبيق
        app.run()
        
        print("\n✅ تم إغلاق البرنامج بنجاح")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البرنامج بواسطة المستخدم")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البرنامج: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🚀 التشغيل النهائي المحسن")
    print("="*60)
    
    success = run_application()
    
    if not success:
        print("\n💡 نصائح لحل المشاكل:")
        print("   1. تأكد من تثبيت Python")
        print("   2. ثبت المكتبات: pip install customtkinter pillow")
        print("   3. تأكد من وجود جميع ملفات المشروع")
        print("   4. جرب تشغيل: python main.py")
        
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
