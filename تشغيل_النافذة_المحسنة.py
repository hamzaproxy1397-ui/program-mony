#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل نافذة إدارة الموظفين المحسنة والمطورة
Enhanced Employee Management Window Launcher

نافذة احترافية ومتطورة مع جميع التحسينات المطلوبة:
✅ أزرار محسنة بأحجام أكبر وتأثيرات بصرية جميلة
✅ نظام ألوان متدرج حديث وجذاب
✅ خطوط مكبرة وواضحة للقراءة السهلة
✅ إصلاح جميع الأخطاء البرمجية
✅ تحسينات شاملة لتجربة المستخدم
✅ واجهة متجاوبة وحديثة
"""

import sys
import os
from pathlib import Path
import traceback

def setup_environment():
    """إعداد البيئة والمسارات"""
    try:
        # تحديد مجلد المشروع
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
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إعداد البيئة: {e}")
        return False

def check_requirements():
    """فحص المتطلبات والمكتبات"""
    print("\n📦 فحص المكتبات المطلوبة...")
    
    required_modules = {
        'customtkinter': 'واجهة المستخدم الحديثة',
        'tkinter': 'واجهة المستخدم الأساسية',
        'PIL': 'معالجة الصور المتقدمة',
        'sqlite3': 'قاعدة البيانات',
        'datetime': 'التعامل مع التواريخ',
        'json': 'معالجة البيانات',
        'threading': 'المعالجة المتوازية',
        'pathlib': 'إدارة المسارات'
    }
    
    missing_modules = []
    
    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} (غير مثبت)")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ المكتبات المفقودة: {', '.join(missing_modules)}")
        print("💡 لتثبيت المكتبات المفقودة:")
        for module in missing_modules:
            if module == 'PIL':
                print(f"   pip install Pillow")
            elif module not in ['tkinter', 'sqlite3', 'datetime', 'json', 'threading', 'pathlib']:
                print(f"   pip install {module}")
        return False
    
    return True

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    try:
        directories = [
            "database",
            "ui",
            "ui/views",
            "themes",
            "config",
            "core",
            "assets",
            "assets/images"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ تم إنشاء المجلدات المطلوبة")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء المجلدات: {e}")
        return False

def run_enhanced_window():
    """تشغيل النافذة المحسنة"""
    try:
        print("\n🚀 بدء تشغيل نافذة إدارة الموظفين المحسنة...")
        
        # تحميل النافذة المحسنة
        from ui.views.enhanced_employees_window import EnhancedEmployeesWindow
        
        print("✅ تم تحميل النافذة المحسنة بنجاح")
        
        # عرض معلومات النافذة
        print("\n" + "="*100)
        print("🏢 مرحباً بك في نظام إدارة الموظفين المحسن والمتطور")
        print("="*100)
        print("🎨 الميزات المحسنة:")
        print("   ✨ أزرار محسنة بأحجام أكبر وتأثيرات بصرية جميلة")
        print("   🌈 نظام ألوان متدرج حديث وجذاب")
        print("   📝 خطوط مكبرة وواضحة للقراءة السهلة")
        print("   🔧 إصلاح جميع الأخطاء البرمجية")
        print("   🎯 تحسينات شاملة لتجربة المستخدم")
        print("   📱 واجهة متجاوبة وحديثة")
        print("   🚀 أداء محسن وسرعة عالية")
        print("   💎 تصميم احترافي وأنيق")
        print("\n📊 الوظائف المتاحة:")
        print("   👥 إدارة شاملة لبيانات الموظفين")
        print("   🔍 بحث ذكي وفلترة متقدمة")
        print("   📈 لوحة معلومات تفاعلية")
        print("   💰 إدارة الرواتب والمكافآت")
        print("   📊 تقارير وتحليلات متقدمة")
        print("   🔔 نظام تنبيهات ذكي")
        print("="*100)
        
        # إنشاء وتشغيل النافذة
        app = EnhancedEmployeesWindow()
        
        if app.window:
            print("🎉 تم إنشاء النافذة المحسنة بنجاح!")
            print("💡 استمتع بالتجربة المحسنة والمطورة")
            
            # تشغيل النافذة
            app.window.mainloop()
            
            print("\n✅ تم إغلاق نافذة إدارة الموظفين المحسنة بنجاح")
            return True
        else:
            print("❌ فشل في إنشاء النافذة المحسنة")
            return False
            
    except ImportError as e:
        print(f"❌ خطأ في استيراد النافذة المحسنة: {e}")
        print("💡 تأكد من وجود ملف enhanced_employees_window.py")
        return False
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل النافذة المحسنة: {e}")
        print("📋 تفاصيل الخطأ:")
        traceback.print_exc()
        return False

def show_fallback_options():
    """إظهار خيارات بديلة"""
    print("\n💡 خيارات بديلة:")
    print("1. تشغيل النافذة المتقدمة: python تشغيل_نافذة_الموظفين_المتقدمة.py")
    print("2. تشغيل النافذة الأساسية: python تشغيل_نافذة_الموظفين.py")
    print("3. تشغيل النافذة الرئيسية: python تشغيل_النافذة_الأصلية.py")
    print("\n🔧 نصائح لحل المشاكل:")
    print("   1. تأكد من تثبيت Python 3.8 أو أحدث")
    print("   2. ثبت المكتبات المطلوبة: pip install customtkinter pillow")
    print("   3. تأكد من وجود جميع ملفات النوافذ")
    print("   4. تحقق من صلاحيات الكتابة في مجلد البرنامج")
    print("   5. تأكد من وجود مساحة كافية على القرص الصلب")

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🚀 نظام إدارة الموظفين المحسن والمتطور - الإصدار النهائي")
    print("="*100)
    
    try:
        # إعداد البيئة
        if not setup_environment():
            print("❌ فشل في إعداد البيئة")
            show_fallback_options()
            input("\nاضغط Enter للخروج...")
            return
        
        # فحص المتطلبات
        if not check_requirements():
            print("❌ بعض المكتبات المطلوبة غير مثبتة")
            show_fallback_options()
            input("\nاضغط Enter للخروج...")
            return
        
        # إنشاء المجلدات
        if not create_directories():
            print("❌ فشل في إنشاء المجلدات المطلوبة")
            show_fallback_options()
            input("\nاضغط Enter للخروج...")
            return
        
        # تشغيل النافذة المحسنة
        success = run_enhanced_window()
        
        if not success:
            print("\n❌ فشل في تشغيل النافذة المحسنة")
            show_fallback_options()
            input("\nاضغط Enter للخروج...")
        else:
            print("\n🎉 شكراً لاستخدام نظام إدارة الموظفين المحسن!")
            print("📞 للدعم الفني: تواصل مع فريق التطوير")
            print("🌐 الموقع الإلكتروني: www.setalkol.com")
    
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البرنامج بواسطة المستخدم")
    
    except Exception as e:
        print(f"\n❌ خطأ عام في البرنامج: {e}")
        print("📋 تفاصيل الخطأ:")
        traceback.print_exc()
        show_fallback_options()
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
