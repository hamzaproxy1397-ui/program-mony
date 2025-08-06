#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل سريع للوحة التحكم المركزية الجذابة
"""

import customtkinter as ctk
import sys
import os
from pathlib import Path

# إعداد المسارات
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """تشغيل لوحة التحكم المركزية"""
    
    print("🎛️ لوحة التحكم المركزية الجذابة")
    print("=" * 50)
    print("🚀 بدء التشغيل...")
    
    # إعداد customtkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    try:
        # استيراد لوحة التحكم
        from ui.central_control_panel import CentralControlPanel

    
    except Exception as e:

    
        pass
        
        print("✅ تم تحميل لوحة التحكم بنجاح")
        
        # إنشاء لوحة التحكم
        panel = CentralControlPanel()
        
        print("✅ تم إنشاء لوحة التحكم")
        print("🎨 الألوان المستخدمة: دافئة وجذابة (بدون رمادي)")
        print("🌐 دعم كامل للعربية RTL")
        print("🧩 11 قسم شامل للتحكم")
        print()
        print("📋 الأقسام المتاحة:")
        print("   1. 🧩 الإعدادات العامة")
        print("   2. 👥 المستخدمون والصلاحيات")
        print("   3. 🧾 إعدادات الفواتير")
        print("   4. 💰 الرواتب والضرائب")
        print("   5. 🏪 إعدادات المخازن")
        print("   6. 🔧 التحكم في الموديلات")
        print("   7. 💾 النسخ الاحتياطي")
        print("   8. 📊 استيراد من Excel")
        print("   9. 🎨 تخصيص الواجهة")
        print("   10. 🛡️ نظام الأمان")
        print("   11. 🔢 الأرقام التسلسلية")
        print()
        print("💡 نصائح الاستخدام:")
        print("   • استخدم الشريط الجانبي للتنقل")
        print("   • اضغط 'تجربة الإعدادات' لمعاينة التغييرات")
        print("   • احفظ الإعدادات بانتظام")
        print("   • استخدم النسخ الاحتياطي للحماية")
        print()
        print("🎯 جاهز للاستخدام!")
        
        # تشغيل النافذة
        panel.window.mainloop()
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("تأكد من وجود الملفات المطلوبة:")
        print("   - ui/central_control_panel.py")
        print("   - themes/modern_theme.py")
        print("   - config/settings.py")
        
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
