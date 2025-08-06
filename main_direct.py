#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل البرنامج المحاسبي مع النافذة الرئيسية مباشرة
Direct Main Window Launch - Skip Login
"""

import sys
import os
from pathlib import Path

# إضافة المسار الحالي إلى Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """تشغيل البرنامج مع تخطي نافذة تسجيل الدخول"""
    try:
        print("🚀 تشغيل البرنامج المحاسبي - النافذة الرئيسية مباشرة")
        print("=" * 60)
        
        # استيراد التطبيق الرئيسي
        from ui.main_window import AccountingApp
        
        print("✅ تم تحميل التطبيق بنجاح")
        
        # إنشاء التطبيق
        app = AccountingApp()
        
        # تعيين المستخدم الافتراضي (تخطي تسجيل الدخول)
        app.current_user = {
            'username': 'admin',
            'user_id': 1,
            'role': 'admin',
            'permissions': ['all'],
            'full_name': 'مدير النظام',
            'email': 'admin@company.com'
        }
        
        print("✅ تم تعيين المستخدم الافتراضي: admin")
        
        # إنشاء النافذة الرئيسية مباشرة
        print("🖥️ إنشاء النافذة الرئيسية...")
        app.create_main_window()
        
        print("✅ تم تشغيل النافذة الرئيسية بنجاح!")
        print("🎉 استمتع بالبرنامج المحاسبي!")
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("💡 تأكد من وجود جميع ملفات البرنامج")
        
        # محاولة تشغيل التشخيص
        try:
            print("\n🔍 تشغيل التشخيص السريع...")
            os.system("python quick_diagnostic.py")
        except:
            pass
            
    except Exception as e:
        print(f"❌ خطأ في تشغيل البرنامج: {e}")
        print("💡 جرب الطرق البديلة:")
        print("   - python main.py")
        print("   - INSTALL_AND_RUN.bat")
        
        import traceback
        print("\n🔍 تفاصيل الخطأ:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
