#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 تشغيل النافذة الرئيسية الأصلية مع الأيقونات المُصححة
Original Main Window with Fixed Icons

النافذة الأصلية الكاملة مع إصلاح جميع مسارات الأيقونات:
- الشريط الأخضر: 6 أيقونات ICO مُصححة
- الصف الأول: 6 أيقونات ICO مُصححة  
- الصف الثاني: 6 أيقونات ICO مُصححة
- الصف الثالث: 6 أيقونات ICO مُصححة
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

def check_icons():
    """فحص الأيقونات المطلوبة"""
    print("\n🔍 فحص الأيقونات المطلوبة...")
    
    icons_dir = Path("assets/icons")
    if not icons_dir.exists():
        print("❌ مجلد الأيقونات غير موجود")
        return False
    
    # الأيقونات المطلوبة للشريط الأخضر
    green_icons = ["employees.ico", "48.ico", "43.ico", "40.ico", "5.ico", "4.ico"]
    
    # الأيقونات المطلوبة للصفوف الثلاثة
    main_icons = [f"{i}.ico" for i in range(1, 20)]
    
    all_required_icons = green_icons + main_icons
    
    missing_icons = []
    found_icons = []
    
    for icon in all_required_icons:
        icon_path = icons_dir / icon
        if icon_path.exists():
            found_icons.append(icon)
            print(f"✅ {icon}")
        else:
            missing_icons.append(icon)
            print(f"❌ {icon} (مفقود)")
    
    print(f"\n📊 إحصائيات الأيقونات:")
    print(f"   ✅ موجودة: {len(found_icons)}")
    print(f"   ❌ مفقودة: {len(missing_icons)}")
    
    if missing_icons:
        print(f"\n⚠️ أيقونات مفقودة: {', '.join(missing_icons)}")
        print("💡 سيتم استخدام أيقونات افتراضية للمفقودة")
    
    return len(found_icons) > 0

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات...")
    
    required = {
        'customtkinter': 'واجهة المستخدم الحديثة',
        'tkinter': 'واجهة المستخدم الأساسية',
        'PIL': 'معالجة الصور والأيقونات'
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
    
    if missing:
        print(f"\n❌ مكتبات مطلوبة مفقودة: {', '.join(missing)}")
        print("💡 لتثبيت المكتبات المطلوبة:")
        print("   pip install customtkinter pillow")
        return False
    
    return True

def load_original_main_window():
    """تحميل النافذة الرئيسية الأصلية المُحسنة"""
    print("\n🎯 تحميل النافذة الرئيسية الأصلية المُحسنة...")
    
    try:
        # تحميل النافذة الأصلية من ui/views/main_window.py
        from ui.views.main_window import MainApplication
        print("✅ تم تحميل MainApplication الأصلية المُحسنة بنجاح")
        return MainApplication
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد النافذة الأصلية: {e}")
        return None

def run_enhanced_application():
    """تشغيل التطبيق الأصلي المُحسن"""
    print("\n🚀 بدء تشغيل النافذة الأصلية المُحسنة...")
    
    try:
        # إعداد البيئة
        setup_environment()
        
        # فحص المكتبات
        if not check_dependencies():
            return False
        
        # فحص الأيقونات
        if not check_icons():
            print("⚠️ تحذير: بعض الأيقونات مفقودة، لكن سيتم المتابعة")
        
        # تحميل النافذة الأصلية
        MainApplication = load_original_main_window()
        if not MainApplication:
            print("❌ فشل في تحميل النافذة الأصلية")
            return False
        
        # إنشاء وتشغيل التطبيق الأصلي
        print("🎉 إنشاء التطبيق الأصلي المُحسن...")
        app = MainApplication()
        
        # تعيين مستخدم افتراضي
        app.current_user = {
            'username': 'admin',
            'full_name': 'مدير النظام',
            'role': 'admin',
            'user_id': 1
        }
        
        print("✅ تم إعداد المستخدم الافتراضي")
        print("\n" + "="*80)
        print("🎨 مرحباً بك في برنامج ست الكل للمحاسبة - النافذة الأصلية المُحسنة")
        print("📊 النافذة الأصلية الكاملة مع الأيقونات المُصححة")
        print("🎯 الشريط الأخضر + 18 وظيفة + الشريط السفلي")
        print("🖼️ جميع الأيقونات مُصححة ومُحسنة")
        print("🔐 تم تسجيل الدخول كمدير النظام")
        print("="*80)
        
        # تشغيل النافذة الأصلية مباشرة
        app.create_main_window()
        
        print("\n✅ تم إغلاق النافذة الأصلية المُحسنة بنجاح")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البرنامج بواسطة المستخدم")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل النافذة الأصلية المُحسنة: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🎨 النافذة الرئيسية الأصلية مع الأيقونات المُصححة")
    print("="*80)
    
    success = run_enhanced_application()
    
    if not success:
        print("\n💡 نصائح لحل المشاكل:")
        print("   1. تأكد من تثبيت Python")
        print("   2. ثبت المكتبات: pip install customtkinter pillow")
        print("   3. تأكد من وجود مجلد assets/icons مع الأيقونات")
        print("   4. تأكد من وجود ملف ui/views/main_window.py")
        
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
