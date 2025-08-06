#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل نافذة إدارة الموظفين المتقدمة والذكية
Advanced Smart Employee Management Window Launcher

ملف تشغيل مستقل لنافذة إدارة الموظفين المتقدمة والذكية
مع جميع الميزات الحديثة والتحليلات الذكية
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
        str(project_root / "core"),
        str(project_root / "ai")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"📁 مجلد المشروع: {project_root}")
    return project_root

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات المطلوبة للنافذة المتقدمة...")
    
    required = {
        'customtkinter': 'واجهة المستخدم الحديثة',
        'tkinter': 'واجهة المستخدم الأساسية',
        'PIL': 'معالجة الصور المتقدمة',
        'sqlite3': 'قاعدة البيانات',
        'numpy': 'العمليات الرياضية والتحليلات',
        'threading': 'المعالجة المتوازية',
        'datetime': 'التعامل مع التواريخ',
        'json': 'معالجة البيانات',
        'random': 'التوليد العشوائي',
        'math': 'العمليات الرياضية'
    }
    
    missing = []
    for module, desc in required.items():
        try:
            if module == 'PIL':
                from PIL import Image, ImageTk, ImageDraw, ImageFilter
            elif module == 'numpy':
                import numpy as np
            else:
                __import__(module)
            print(f"✅ {module} - {desc}")
        except ImportError:
            print(f"❌ {module} - {desc} (مطلوب)")
            missing.append(module)
    
    if missing:
        print(f"\n❌ مكتبات مطلوبة مفقودة: {', '.join(missing)}")
        print("💡 لتثبيت المكتبات المطلوبة:")
        print("   pip install customtkinter pillow numpy")
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
        "assets/photos",
        "backup",
        "reports",
        "temp"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ تم إنشاء مجلد: {directory}")
        else:
            print(f"✅ مجلد موجود: {directory}")

def run_advanced_employees_window():
    """تشغيل نافذة إدارة الموظفين المتقدمة"""
    print("\n🚀 بدء تشغيل نافذة إدارة الموظفين المتقدمة والذكية...")
    
    try:
        # إعداد البيئة
        setup_environment()
        
        # فحص المكتبات
        if not check_dependencies():
            return False
        
        # إنشاء المجلدات المطلوبة
        create_required_directories()
        
        # تحميل النافذة المتقدمة
        print("\n🎯 تحميل نافذة إدارة الموظفين المتقدمة...")
        from ui.views.advanced_employees_management import AdvancedEmployeesManagement
        
        print("✅ تم تحميل النافذة المتقدمة بنجاح")
        
        # إنشاء وتشغيل النافذة
        print("🎉 إنشاء نافذة إدارة الموظفين المتقدمة...")
        
        print("\n" + "="*100)
        print("🚀 مرحباً بك في نظام إدارة الموظفين المتقدم والذكي")
        print("📊 نافذة شاملة ومتطورة لإدارة جميع بيانات الموظفين")
        print("🎯 الميزات المتقدمة المتاحة:")
        print("   ✨ تصميم Material Design مع ألوان متدرجة")
        print("   🤖 خوارزميات ذكية لاقتراح الرواتب وتحليل الأداء")
        print("   📊 لوحة معلومات تفاعلية مع رسوم بيانية")
        print("   🔍 بحث ذكي وفلترة متقدمة")
        print("   📈 تحليل الأداء والإنتاجية")
        print("   🔮 التنبؤات الذكية للحضور والأداء")
        print("   💡 نظام التوصيات الذكية")
        print("   🎨 تأثيرات بصرية وانتقالات سلسة")
        print("   📱 واجهة متجاوبة وحديثة")
        print("   🔔 نظام إشعارات ذكي")
        print("   💾 قاعدة بيانات محسنة ومتقدمة")
        print("   🔧 تكامل كامل مع النظام الرئيسي")
        print("="*100)
        
        # تشغيل النافذة
        app = AdvancedEmployeesManagement()
        app.window.mainloop()
        
        print("\n✅ تم إغلاق نافذة إدارة الموظفين المتقدمة بنجاح")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البرنامج بواسطة المستخدم")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل النافذة المتقدمة: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 برنامج ست الكل للمحاسبة")
    print("🏢 نظام إدارة الموظفين المتقدم والذكي - الإصدار المحسن")
    print("="*100)
    
    success = run_advanced_employees_window()
    
    if not success:
        print("\n💡 نصائح لحل المشاكل:")
        print("   1. تأكد من تثبيت Python 3.8 أو أحدث")
        print("   2. ثبت المكتبات: pip install customtkinter pillow numpy")
        print("   3. تأكد من وجود ملف ui/views/advanced_employees_management.py")
        print("   4. تحقق من صلاحيات الكتابة في مجلد البرنامج")
        print("   5. تأكد من وجود مساحة كافية على القرص الصلب")
        
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
