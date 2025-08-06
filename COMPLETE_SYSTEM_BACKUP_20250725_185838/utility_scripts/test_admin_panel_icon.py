#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار أيقونة لوحة التحكم الشاملة
Test Admin Panel Icon Integration
"""

import customtkinter as ctk
from ui.advanced_settings_window import ComprehensiveAdminPanel

def test_admin_panel_icon():
    """اختبار أيقونة لوحة التحكم الشاملة"""
    
    # إنشاء نافذة اختبار
    test_window = ctk.CTk()
    test_window.title("🎛️ اختبار أيقونة لوحة التحكم الشاملة")
    test_window.geometry("400x300")
    
    # تكوين النافذة
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # إطار رئيسي
    main_frame = ctk.CTkFrame(test_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # عنوان
    title_label = ctk.CTkLabel(
        main_frame,
        text="🎛️ اختبار لوحة التحكم الشاملة",
        font=("Cairo", 20, "bold")
    )
    title_label.pack(pady=20)
    
    # وصف
    desc_label = ctk.CTkLabel(
        main_frame,
        text="اضغط على الزر أدناه لفتح لوحة التحكم الشاملة المتطورة",
        font=("Cairo", 12),
        wraplength=300
    )
    desc_label.pack(pady=10)
    
    def open_admin_panel():
        """فتح لوحة التحكم الشاملة"""
        try:
            admin_panel = ComprehensiveAdminPanel()
            print("✅ تم فتح لوحة التحكم الشاملة بنجاح!")
        except Exception as e:
            print(f"❌ خطأ في فتح لوحة التحكم: {e}")
    
    # زر فتح لوحة التحكم
    admin_button = ctk.CTkButton(
        main_frame,
        text="🎛️ فتح لوحة التحكم الشاملة",
        font=("Cairo", 14, "bold"),
        fg_color="#FF8C00",  # اللون البرتقالي الجديد
        hover_color="#FFA533",
        width=250,
        height=50,
        command=open_admin_panel
    )
    admin_button.pack(pady=20)
    
    # معلومات الميزات
    features_label = ctk.CTkLabel(
        main_frame,
        text="الميزات المتاحة:\n• الإعدادات العامة\n• النسخ الاحتياطي المتقدم\n• إحصائيات النظام",
        font=("Cairo", 10),
        justify="right"
    )
    features_label.pack(pady=10)
    
    # زر إغلاق
    close_button = ctk.CTkButton(
        main_frame,
        text="إغلاق",
        font=("Cairo", 12),
        fg_color="#dc3545",
        hover_color="#c82333",
        width=100,
        command=test_window.destroy
    )
    close_button.pack(pady=10)
    
    print("🎛️ نافذة اختبار لوحة التحكم الشاملة جاهزة!")
    print("✅ الأيقونة البرتقالية الجديدة متاحة")
    print("🔗 يمكن الوصول إليها من:")
    print("   - الواجهة الرئيسية (الصف الأول من الأيقونات)")
    print("   - القائمة المنسدلة للرئيسية")
    print("   - القائمة البسيطة للرئيسية")
    
    test_window.mainloop()

if __name__ == "__main__":
    test_admin_panel_icon()
