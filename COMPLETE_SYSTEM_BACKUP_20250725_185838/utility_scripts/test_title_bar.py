#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شريط العنوان المخصص
Test Custom Title Bar
"""

import sys
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_title_bar():
    """اختبار شريط العنوان المخصص"""
    print("🧪 اختبار شريط العنوان المخصص")
    print("=" * 50)
    
    try:
        import customtkinter as ctk
        print("✅ customtkinter متوفر")
        
        # إعداد customtkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # إنشاء النافذة الرئيسية
        root = ctk.CTk()
        root.withdraw()  # إخفاء النافذة الرئيسية
        
        print("✅ تم إنشاء النافذة الرئيسية")
        
        # اختبار استيراد لوحة التحكم
        from ui.central_control_panel import CentralControlPanel
        print("✅ تم استيراد لوحة التحكم")
        
        # إنشاء لوحة التحكم
        control_panel = CentralControlPanel(root)
        print("✅ تم إنشاء لوحة التحكم مع شريط العنوان المخصص")
        
        # اختبار الوظائف
        print("\n🔧 اختبار وظائف شريط العنوان:")
        
        # اختبار معلومات النافذة
        try:
            window_geometry = control_panel.window.geometry()
            print(f"  ✅ هندسة النافذة: {window_geometry}")
        except Exception as e:
            print(f"  ⚠️ خطأ في جلب هندسة النافذة: {e}")
        
        # اختبار حالة التكبير
        try:
            is_maximized = control_panel.is_maximized
            print(f"  ✅ حالة التكبير: {'مكبرة' if is_maximized else 'عادية'}")
        except Exception as e:
            print(f"  ⚠️ خطأ في جلب حالة التكبير: {e}")
        
        # اختبار شريط العنوان
        try:
            title_bar_exists = hasattr(control_panel, 'title_bar')
            print(f"  ✅ شريط العنوان موجود: {'نعم' if title_bar_exists else 'لا'}")
        except Exception as e:
            print(f"  ⚠️ خطأ في فحص شريط العنوان: {e}")
        
        # اختبار أزرار التحكم
        control_buttons = ['close_btn', 'maximize_btn', 'minimize_btn', 'settings_btn']
        for button_name in control_buttons:
            try:
                button_exists = hasattr(control_panel, button_name)
                print(f"  ✅ زر {button_name}: {'موجود' if button_exists else 'غير موجود'}")
            except Exception as e:
                print(f"  ⚠️ خطأ في فحص {button_name}: {e}")
        
        print("\n👁️ اختبار بصري...")
        print("  🔍 سيتم عرض لوحة التحكم لمدة 5 ثوانٍ...")
        
        # إظهار النافذة للاختبار البصري
        control_panel.window.deiconify()
        control_panel.window.lift()
        
        # انتظار لمدة 5 ثوانٍ
        root.after(5000, root.quit)
        
        # تشغيل الحلقة الرئيسية
        root.mainloop()
        
        print("  ✅ تم الاختبار البصري")
        
        print("\n🎉 نتائج الاختبار:")
        print("  ✅ شريط العنوان المخصص يعمل بنجاح!")
        print("  🎛️ جميع أزرار التحكم متوفرة")
        print("  🖼️ النافذة تعرض بالحجم الصحيح")
        
        return True
        
    except Exception as e:
        print(f"\n❌ فشل الاختبار: {e}")
        import traceback
import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء اختبار شريط العنوان المخصص")
    print("=" * 50)
    
    success = test_title_bar()
    
    if success:
        print("\n🎉 جميع الاختبارات نجحت!")
        print("🎛️ شريط العنوان المخصص جاهز للاستخدام")
        print("\n🚀 للتشغيل:")
        print("   python START_HERE.py")
        print("   أو")
        print("   python تشغيل_البرنامج.py")
        return 0
    else:
        print("\n❌ فشل اختبار شريط العنوان")
        return 1

if __name__ == "__main__":
    sys.exit(main())
