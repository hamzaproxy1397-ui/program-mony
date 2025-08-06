#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل نافذة إدارة الموظفين البسيطة للاختبار
Simple Employee Management Window for Testing
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

def run_simple_employees_window():
    """تشغيل نافذة إدارة الموظفين البسيطة"""
    print("\n🚀 بدء تشغيل نافذة إدارة الموظفين البسيطة...")
    
    try:
        # إعداد البيئة
        setup_environment()
        
        # تحميل النافذة البسيطة
        print("\n🎯 تحميل نافذة إدارة الموظفين البسيطة...")
        from ui.views.employees_management_window import EmployeesManagementWindow
        
        print("✅ تم تحميل النافذة البسيطة بنجاح")
        
        # إنشاء وتشغيل النافذة
        print("🎉 إنشاء نافذة إدارة الموظفين البسيطة...")
        
        print("\n" + "="*80)
        print("🏢 مرحباً بك في نظام إدارة الموظفين البسيط")
        print("📊 نافذة أساسية لإدارة بيانات الموظفين")
        print("🎯 الميزات المتاحة:")
        print("   ✅ جدول عرض الموظفين مع البحث والفلترة")
        print("   ✅ نماذج إضافة وتعديل الموظفين")
        print("   ✅ إدارة الرواتب والمكافآت")
        print("   ✅ تقارير الموظفين")
        print("   ✅ واجهة عربية احترافية")
        print("="*80)
        
        # تشغيل النافذة
        app = EmployeesManagementWindow()
        app.window.mainloop()
        
        print("\n✅ تم إغلاق نافذة إدارة الموظفين البسيطة بنجاح")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البرنامج بواسطة المستخدم")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل النافذة البسيطة: {e}")
        import traceback
        traceback.print_exc()
        
        # محاولة تشغيل النافذة المتقدمة
        print("\n💡 جاري المحاولة مع النافذة المتقدمة...")
        try:
            from ui.views.advanced_employees_management import AdvancedEmployeesManagement
            app = AdvancedEmployeesManagement()
            app.window.mainloop()
            return True
        except Exception as e2:
            print(f"❌ خطأ في النافذة المتقدمة أيضاً: {e2}")
            return False

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("👥 نظام إدارة الموظفين البسيط")
    print("="*80)
    
    success = run_simple_employees_window()
    
    if not success:
        print("\n💡 نصائح لحل المشاكل:")
        print("   1. تأكد من تثبيت Python")
        print("   2. ثبت المكتبات: pip install customtkinter pillow")
        print("   3. تأكد من وجود ملفات النوافذ")
        print("   4. تحقق من صلاحيات الكتابة في مجلد البرنامج")
        
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
