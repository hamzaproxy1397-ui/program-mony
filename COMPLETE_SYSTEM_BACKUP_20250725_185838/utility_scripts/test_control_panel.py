#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار لوحة التحكم المركزية الجذابة
"""

import customtkinter as ctk
import sys
import os

# إضافة مسار المشروع إلى sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_control_panel():
    """اختبار لوحة التحكم المركزية"""
    
    # إعداد customtkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # إنشاء نافذة رئيسية بسيطة للاختبار
    root = ctk.CTk()
    root.title("اختبار لوحة التحكم المركزية")
    root.geometry("400x300")
    root.configure(fg_color="#FFFEF7")  # أبيض دافئ
    
    # عنوان الاختبار
    title_label = ctk.CTkLabel(
        root,
        text="🎛️ اختبار لوحة التحكم المركزية",
        font=("Cairo", 20, "bold"),
        text_color="#E55555"  # مرجاني داكن
    )
    title_label.pack(pady=30)
    
    # وصف
    desc_label = ctk.CTkLabel(
        root,
        text="اضغط على الزر أدناه لفتح لوحة التحكم الجذابة",
        font=("Cairo", 14),
        text_color="#2C5F5D"  # تيل عميق
    )
    desc_label.pack(pady=10)
    
    # زر فتح لوحة التحكم
    def open_panel():
        try:
            from ui.central_control_panel import open_central_control_panel
            panel = open_central_control_panel(root)
            if panel:
                print("✅ تم فتح لوحة التحكم بنجاح!")
            else:
                print("❌ فشل في فتح لوحة التحكم")
        except Exception as e:
            print(f"❌ خطأ في فتح لوحة التحكم: {e}")
            import traceback
import traceback
            traceback.print_exc()
    
    open_button = ctk.CTkButton(
        root,
        text="🚀 فتح لوحة التحكم",
        font=("Cairo", 16, "bold"),
        fg_color="#FF6B6B",  # مرجاني دافئ
        hover_color="#FF8E8E",  # مرجاني فاتح
        height=50,
        width=200,
        command=open_panel
    )
    open_button.pack(pady=30)
    
    # معلومات إضافية
    info_frame = ctk.CTkFrame(root, fg_color="#FFF8E1", corner_radius=10)  # كريمي ناعم
    info_frame.pack(fill="x", padx=30, pady=20)
    
    info_text = """
🌟 المميزات:
• 11 قسم شامل للتحكم
• ألوان دافئة وجذابة
• دعم كامل للعربية RTL
• حفظ واستعادة الإعدادات
• معاينة التغييرات
• نسخ احتياطي متقدم
    """
    
    info_label = ctk.CTkLabel(
        info_frame,
        text=info_text.strip(),
        font=("Cairo", 11),
        text_color="#6A4C93",  # بنفسجي غني
        justify="right"
    )
    info_label.pack(pady=15)
    
    # تشغيل النافذة
    print("🎛️ بدء اختبار لوحة التحكم المركزية...")
    print("📋 تأكد من وجود الملفات المطلوبة:")
    print("   - ui/central_control_panel.py")
    print("   - themes/modern_theme.py")
    print("   - config/settings.py")
    print()
    
    root.mainloop()

if __name__ == "__main__":
    test_control_panel()
