#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏢 تشغيل نافذة إدارة الموظفين المتقدمة
Advanced Employee Management Window Launcher

ملف تشغيل مستقل لنافذة إدارة الموظفين الاحترافية
"""

import sys
import os
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
        str(project_root / "database"),
        str(project_root / "core")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"📁 مجلد المشروع: {project_root}")
    return project_root

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات المطلوبة...")
    
    required = {
        'customtkinter': 'واجهة المستخدم الحديثة',
        'tkinter': 'واجهة المستخدم الأساسية',
        'PIL': 'معالجة الصور',
        'sqlite3': 'قاعدة البيانات'
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

def create_required_directories():
    """إنشاء المجلدات المطلوبة"""
    print("\n📁 إنشاء المجلدات المطلوبة...")
    
    directories = [
        "data",
        "logs",
        "assets",
        "assets/icons",
        "backup"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ تم إنشاء مجلد: {directory}")
        else:
            print(f"✅ مجلد موجود: {directory}")

def run_employees_window():
    """تشغيل نافذة إدارة الموظفين"""
    print("\n🚀 بدء تشغيل نافذة إدارة الموظفين...")
    
    try:
        # إعداد البيئة
        setup_environment()
        
        # فحص المكتبات
        if not check_dependencies():
            return False
        
        # إنشاء المجلدات المطلوبة
        create_required_directories()
        
        # تحميل نافذة الموظفين
        print("\n🎯 تحميل نافذة إدارة الموظفين...")
        from ui.views.employees_management_window import EmployeesManagementWindow
        
        print("✅ تم تحميل نافذة الموظفين بنجاح")
        
        # إنشاء وتشغيل النافذة
        print("🎉 إنشاء نافذة إدارة الموظفين...")
        
        print("\n" + "="*80)
        print("🏢 مرحباً بك في نظام إدارة الموظفين المتقدم")
        print("📊 نافذة شاملة لإدارة جميع بيانات الموظفين")
        print("🎯 الميزات المتاحة:")
        print("   ✅ جدول عرض الموظفين مع البحث والفلترة")
        print("   ✅ نماذج إضافة وتعديل الموظفين")
        print("   ✅ إدارة الرواتب والمكافآت")
        print("   ✅ تقارير شاملة للموظفين")
        print("   ✅ واجهة عربية احترافية")
        print("="*80)
        
        # تشغيل النافذة
        app = EmployeesManagementWindow()
        app.window.mainloop()
        
        print("\n✅ تم إغلاق نافذة إدارة الموظفين بنجاح")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البرنامج بواسطة المستخدم")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل نافذة الموظفين: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("👥 نظام إدارة الموظفين المتقدم")
    print("="*80)
    
    success = run_employees_window()
    
    if not success:
        print("\n💡 نصائح لحل المشاكل:")
        print("   1. تأكد من تثبيت Python")
        print("   2. ثبت المكتبات: pip install customtkinter pillow")
        print("   3. تأكد من وجود ملف ui/views/employees_management_window.py")
        print("   4. تحقق من صلاحيات الكتابة في مجلد البرنامج")
        
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
