#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل نافذة العرض الرئيسية مباشرة
Direct launcher for the main window
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """تشغيل النافذة الرئيسية مباشرة"""
    print("🎛️ برنامج ست الكل للمحاسبة")
    print("=" * 40)
    print("🚀 تشغيل النافذة الرئيسية...")
    print()
    
    try:
        # استيراد وتشغيل التطبيق
        from ui.main_window import MainApplication
        
        print("✅ تم تحميل التطبيق بنجاح")
        print("🎉 بدء التشغيل...")
        print()
        print("📝 ملاحظات:")
        print("   - لإغلاق التطبيق: أغلق النافذة")
        print("   - في حالة عدم ظهور النافذة: تحقق من شريط المهام")
        print("   - بيانات تسجيل الدخول الافتراضية:")
        print("     المستخدم: admin")
        print("     كلمة المرور: admin")
        print()
        
        # إنشاء وتشغيل التطبيق
        app = MainApplication()
        app.run()
        
        print("✅ تم إغلاق التطبيق بنجاح")
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد الوحدات: {e}")
        print()
        print("💡 تأكد من:")
        print("   - تثبيت Python")
        print("   - تثبيت customtkinter: pip install customtkinter")
        print("   - وجود جميع ملفات المشروع")
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        print()
        import traceback
        traceback.print_exc()
        
    finally:
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
