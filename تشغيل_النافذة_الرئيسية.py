#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل النافذة الرئيسية للبرنامج المحاسبي
Main Window Launcher for Accounting Software

ملف تشغيل محسن ومبسط للنافذة الرئيسية
"""

import sys
import os
from pathlib import Path

def setup_environment():
    """إعداد البيئة والمسارات"""
    # إضافة مسار المشروع
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # تغيير المجلد الحالي
    os.chdir(project_root)
    
    print(f"📁 مجلد المشروع: {project_root}")
    print(f"🐍 إصدار Python: {sys.version}")

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات المطلوبة...")
    
    required_modules = {
        'customtkinter': 'واجهة المستخدم الحديثة',
        'PIL': 'معالجة الصور',
        'tkinter': 'واجهة المستخدم الأساسية'
    }
    
    missing_modules = []
    
    for module, description in required_modules.items():
        try:
            if module == 'PIL':
                from PIL import Image
            else:
                __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} (مفقود)")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ مكتبات مفقودة: {', '.join(missing_modules)}")
        print("💡 لتثبيت المكتبات المفقودة:")
        if 'customtkinter' in missing_modules:
            print("   pip install customtkinter")
        if 'PIL' in missing_modules:
            print("   pip install pillow")
        return False
    
    return True

def run_main_window():
    """تشغيل النافذة الرئيسية"""
    try:
        print("\n🎯 تحميل النافذة الرئيسية...")

        # محاولة تشغيل البرنامج الكامل أولاً
        try:
            from main import main as run_main_app
            print("✅ تم العثور على main.py")
            print("🚀 تشغيل البرنامج الكامل...")
            print("\n" + "="*50)
            print("🎉 مرحباً بك في برنامج ست الكل للمحاسبة")
            print("📊 البرنامج الكامل جاهز للاستخدام")
            print("="*50)

            run_main_app()
            return True

        except ImportError:
            print("⚠️ لم يتم العثور على main.py، محاولة تشغيل النافذة الرئيسية مباشرة...")

        # محاولة تشغيل النافذة الرئيسية مباشرة
        try:
            # استيراد الفئة الرئيسية مع معالجة الأخطاء
            import sys
            sys.path.append('ui')
            sys.path.append('ui/views')

            from ui.views.main_window import MainApplication
            print("✅ تم تحميل MainApplication بنجاح")

            # إنشاء التطبيق
            app = MainApplication()
            print("✅ تم إنشاء التطبيق بنجاح")

            # تعيين مستخدم افتراضي (تجاوز تسجيل الدخول)
            app.current_user = {
                'username': 'admin',
                'full_name': 'مدير النظام',
                'role': 'admin',
                'user_id': 1
            }
            print("✅ تم تعيين المستخدم الافتراضي")

            # تشغيل النافذة الرئيسية مباشرة
            print("🚀 تشغيل النافذة الرئيسية...")
            print("\n" + "="*50)
            print("🎉 مرحباً بك في برنامج ست الكل للمحاسبة")
            print("📊 النافذة الرئيسية جاهزة للاستخدام")
            print("="*50)

            app.create_main_window()
            return True

        except Exception as e:
            print(f"❌ خطأ في تشغيل النافذة الرئيسية: {e}")

        # محاولة أخيرة - تشغيل ملف تشغيل بديل
        try:
            print("🔄 محاولة تشغيل ملف بديل...")
            if os.path.exists('run_main_window.py'):
                import subprocess
                subprocess.run([sys.executable, 'run_main_window.py'])
                return True
        except:
            pass

    except Exception as e:
        print(f"❌ خطأ عام في التشغيل: {e}")
        import traceback
        traceback.print_exc()
        return False

    return False

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🚀 تشغيل النافذة الرئيسية المباشر")
    print("="*60)
    
    # إعداد البيئة
    setup_environment()
    
    # فحص المكتبات
    if not check_dependencies():
        input("\nاضغط Enter للخروج...")
        return
    
    # تشغيل النافذة الرئيسية
    success = run_main_window()
    
    if success:
        print("\n✅ تم إغلاق البرنامج بنجاح")
    else:
        print("\n❌ حدث خطأ في التشغيل")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
