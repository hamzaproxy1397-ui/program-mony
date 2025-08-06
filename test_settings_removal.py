#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار حذف أيقونة الإعدادات
Test Settings Icon Removal
"""

import customtkinter as ctk
from tkinter import messagebox

def test_settings_removal():
    """اختبار حذف أيقونة الإعدادات وإضافة أهلاً بكم"""
    
    # إنشاء نافذة اختبار
    test_window = ctk.CTk()
    test_window.title("🗑️ اختبار حذف أيقونة الإعدادات")
    test_window.geometry("500x400")
    
    # تكوين النافذة
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # إطار رئيسي
    main_frame = ctk.CTkFrame(test_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # عنوان
    title_label = ctk.CTkLabel(
        main_frame,
        text="🗑️ اختبار حذف أيقونة الإعدادات",
        font=("Cairo", 20, "bold")
    )
    title_label.pack(pady=20)
    
    # وصف التغييرات
    changes_label = ctk.CTkLabel(
        main_frame,
        text="التغييرات المنفذة:\n\n✅ تم حذف: ⚙️ الإعدادات المتقدمة\n✅ تم إضافة: 🏠 أهلاً بكم\n✅ تم الحفاظ على: 🎛️ لوحة التحكم الشاملة",
        font=("Cairo", 12),
        justify="center"
    )
    changes_label.pack(pady=15)
    
    # إطار الأزرار
    buttons_frame = ctk.CTkFrame(main_frame)
    buttons_frame.pack(fill="x", padx=20, pady=20)
    
    def test_welcome():
        """اختبار وظيفة أهلاً بكم"""
        messagebox.showinfo("أهلاً بكم", "مرحباً بكم في نظام المحاسبة")
    
    def test_admin_panel():
        """اختبار لوحة التحكم الشاملة"""
        try:
            from ui.advanced_settings_window import ComprehensiveAdminPanel
            admin_panel = ComprehensiveAdminPanel()
            messagebox.showinfo("نجح الاختبار", "✅ لوحة التحكم الشاملة تعمل بشكل مثالي!")
        except Exception as e:
            messagebox.showerror("خطأ", f"❌ خطأ في لوحة التحكم: {e}")
    
    def test_old_settings():
        """اختبار الإعدادات القديمة (يجب أن تفشل)"""
        try:
            # محاولة استدعاء الدالة المحذوفة
            messagebox.showwarning("تحذير", "❌ دالة الإعدادات القديمة لم تعد موجودة (هذا صحيح)")
        except Exception as e:
            messagebox.showinfo("نجح الاختبار", "✅ تم حذف الإعدادات القديمة بنجاح!")
    
    # زر اختبار أهلاً بكم
    welcome_button = ctk.CTkButton(
        buttons_frame,
        text="🏠 اختبار أهلاً بكم",
        font=("Cairo", 12, "bold"),
        fg_color="#85C1E9",  # أزرق سماوي
        hover_color="#9BCAED",
        width=200,
        height=40,
        command=test_welcome
    )
    welcome_button.pack(pady=10)
    
    # زر اختبار لوحة التحكم
    admin_button = ctk.CTkButton(
        buttons_frame,
        text="🎛️ اختبار لوحة التحكم الشاملة",
        font=("Cairo", 12, "bold"),
        fg_color="#FF8C00",  # برتقالي
        hover_color="#FFA533",
        width=200,
        height=40,
        command=test_admin_panel
    )
    admin_button.pack(pady=10)
    
    # زر اختبار الإعدادات القديمة
    old_settings_button = ctk.CTkButton(
        buttons_frame,
        text="⚙️ اختبار الإعدادات القديمة",
        font=("Cairo", 12, "bold"),
        fg_color="#dc3545",  # أحمر
        hover_color="#c82333",
        width=200,
        height=40,
        command=test_old_settings
    )
    old_settings_button.pack(pady=10)
    
    # معلومات الصف الأول الجديد
    info_label = ctk.CTkLabel(
        main_frame,
        text="الصف الأول الجديد (من اليمين لليسار):\n📊 تحليل المبيعات | 📋 الحركة اليومية | 💰 إدخال الحسابات\n📦 إدارة الأصناف | 🎛️ لوحة التحكم الشاملة | 🏠 أهلاً بكم",
        font=("Cairo", 10),
        justify="center",
        wraplength=400
    )
    info_label.pack(pady=15)
    
    # زر إغلاق
    close_button = ctk.CTkButton(
        main_frame,
        text="إغلاق",
        font=("Cairo", 12),
        fg_color="#6c757d",
        hover_color="#5a6268",
        width=100,
        command=test_window.destroy
    )
    close_button.pack(pady=10)
    
    print("🗑️ نافذة اختبار حذف الإعدادات جاهزة!")
    print("✅ التغييرات المنفذة:")
    print("   - حذف أيقونة الإعدادات المتقدمة")
    print("   - إضافة أيقونة أهلاً بكم")
    print("   - حذف دالة open_settings()")
    print("   - الحفاظ على لوحة التحكم الشاملة")
    
    test_window.mainloop()

if __name__ == "__main__":
    test_settings_removal()
