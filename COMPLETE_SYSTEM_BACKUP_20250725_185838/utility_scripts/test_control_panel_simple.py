#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار بسيط للوحة التحكم المركزية
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """اختبار الاستيرادات"""
    print("🔍 اختبار الاستيرادات...")
    
    try:
        import customtkinter as ctk
        print("✅ customtkinter - تم الاستيراد بنجاح")
    except ImportError as e:
        print(f"❌ customtkinter - خطأ في الاستيراد: {e}")
        return False
    
    try:
        from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS
        print("✅ themes.modern_theme - تم الاستيراد بنجاح")
    except ImportError as e:
        print(f"❌ themes.modern_theme - خطأ في الاستيراد: {e}")
        return False
    
    try:
        from config.settings import PROJECT_ROOT, DATABASE_PATH
        print("✅ config.settings - تم الاستيراد بنجاح")
    except ImportError as e:
        print(f"❌ config.settings - خطأ في الاستيراد: {e}")
        return False
    
    try:
        from ui.central_control_panel import CentralControlPanel, WARM_COLORS
        print("✅ ui.central_control_panel - تم الاستيراد بنجاح")
        print(f"   📊 عدد الألوان الدافئة: {len(WARM_COLORS)}")
    except ImportError as e:
        print(f"❌ ui.central_control_panel - خطأ في الاستيراد: {e}")
        return False
    
    return True

def test_control_panel():
    """اختبار إنشاء لوحة التحكم"""
    print("\n🎛️ اختبار إنشاء لوحة التحكم...")
    
    try:
        import customtkinter as ctk
        from ui.central_control_panel import CentralControlPanel
        
        # إعداد customtkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        print("🚀 إنشاء لوحة التحكم...")
        panel = CentralControlPanel()
        
        print("✅ تم إنشاء لوحة التحكم بنجاح!")
        print(f"   📋 القسم الحالي: {panel.current_section}")
        print(f"   🎨 عدد أزرار الشريط الجانبي: {len(panel.sidebar_buttons)}")
        
        # اختبار تحميل الإعدادات
        print("📂 اختبار تحميل الإعدادات...")
        panel.load_settings()
        print(f"   ⚙️ عدد الإعدادات المحملة: {len(panel.current_settings)}")
        
        # اختبار عرض قسم
        print("🧩 اختبار عرض الإعدادات العامة...")
        panel.show_section("general")
        print("✅ تم عرض الإعدادات العامة بنجاح!")
        
        print("\n🎯 جاهز للاستخدام!")
        print("💡 لفتح لوحة التحكم، شغل البرنامج الرئيسي واضغط على أيقونة الإعدادات")
        
        # تشغيل النافذة
        panel.window.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء لوحة التحكم: {e}")
        import traceback
import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🎛️ اختبار لوحة التحكم المركزية الجذابة")
    print("=" * 60)
    
    # اختبار الاستيرادات
    if not test_imports():
        print("\n❌ فشل في اختبار الاستيرادات")
        return
    
    print("\n✅ جميع الاستيرادات تعمل بشكل صحيح!")
    
    # اختبار لوحة التحكم
    if test_control_panel():
        print("\n🎉 تم اختبار لوحة التحكم بنجاح!")
    else:
        print("\n❌ فشل في اختبار لوحة التحكم")

if __name__ == "__main__":
    main()
