#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل مباشر وبسيط للبرنامج المحاسبي
Direct Simple Launch for Accounting Software

ملف تشغيل مبسط يتجاوز جميع المشاكل
"""

import sys
import os
from pathlib import Path

def create_simple_accounting_app():
    """إنشاء تطبيق محاسبي مبسط"""
    try:
        import customtkinter as ctk
        from tkinter import messagebox
        
        print("✅ تم تحميل المكتبات بنجاح")
        
        # إنشاء النافذة الرئيسية
        root = ctk.CTk()
        root.title("🏢 برنامج ست الكل للمحاسبة - الإصدار المبسط")
        root.geometry("1200x800")
        
        # تعيين الثيم
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # الإطار الرئيسي
        main_frame = ctk.CTkFrame(root, fg_color="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # الشريط العلوي
        header_frame = ctk.CTkFrame(main_frame, height=80, fg_color="#2E8B57")
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # عنوان البرنامج
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏢 برنامج ست الكل للمحاسبة",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        title_label.pack(expand=True)
        
        # إطار المحتوى الرئيسي
        content_frame = ctk.CTkFrame(main_frame, fg_color="white")
        content_frame.pack(fill="both", expand=True)
        
        # شبكة الوظائف الرئيسية
        functions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        functions_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # عنوان الوظائف
        functions_title = ctk.CTkLabel(
            functions_frame,
            text="📊 الوظائف الرئيسية",
            font=("Arial", 20, "bold"),
            text_color="#2E8B57"
        )
        functions_title.pack(pady=(0, 20))
        
        # إنشاء شبكة الأزرار
        buttons_grid = ctk.CTkFrame(functions_frame, fg_color="transparent")
        buttons_grid.pack(expand=True)
        
        # قائمة الوظائف
        functions = [
            ("💰 المبيعات", "#27AE60", "إدارة عمليات البيع والفواتير"),
            ("🛒 المشتريات", "#E74C3C", "إدارة عمليات الشراء والموردين"),
            ("📦 المخازن", "#F39C12", "إدارة المخزون والمواد"),
            ("💳 الحسابات", "#3498DB", "إدارة الحسابات المالية"),
            ("📊 التقارير", "#9B59B6", "تقارير مالية ومحاسبية"),
            ("👥 الموظفين", "#1ABC9C", "إدارة الموارد البشرية"),
            ("⚙️ الإعدادات", "#34495E", "إعدادات النظام والتحكم"),
            ("📈 التحليلات", "#E67E22", "تحليل البيانات والمبيعات"),
            ("🏪 نقاط البيع", "#2ECC71", "نظام نقاط البيع"),
            ("💼 العملاء", "#8E44AD", "إدارة بيانات العملاء"),
            ("🚚 الموردين", "#16A085", "إدارة بيانات الموردين"),
            ("📋 الفواتير", "#D35400", "إدارة الفواتير والمستندات")
        ]
        
        # إنشاء الأزرار في شبكة 4x3
        for i, (text, color, description) in enumerate(functions):
            row = i // 4
            col = i % 4
            
            # إطار الزر
            button_frame = ctk.CTkFrame(buttons_grid, width=250, height=120, fg_color=color, corner_radius=15)
            button_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            button_frame.pack_propagate(False)
            
            # نص الزر
            button_label = ctk.CTkLabel(
                button_frame,
                text=text,
                font=("Arial", 16, "bold"),
                text_color="white"
            )
            button_label.pack(pady=(20, 5))
            
            # وصف الزر
            desc_label = ctk.CTkLabel(
                button_frame,
                text=description,
                font=("Arial", 10),
                text_color="white",
                wraplength=200
            )
            desc_label.pack(pady=(0, 15))
            
            # جعل الزر قابل للنقر
            def on_click(func_name=text):
                messagebox.showinfo("معلومات", f"تم النقر على: {func_name}\n\nهذه الميزة قيد التطوير")
            
            button_frame.bind("<Button-1>", lambda e, fn=text: on_click(fn))
            button_label.bind("<Button-1>", lambda e, fn=text: on_click(fn))
            desc_label.bind("<Button-1>", lambda e, fn=text: on_click(fn))
            
            # تأثير التمرير
            def on_enter(e, frame=button_frame, original_color=color):
                frame.configure(fg_color=darken_color(original_color))
            
            def on_leave(e, frame=button_frame, original_color=color):
                frame.configure(fg_color=original_color)
            
            button_frame.bind("<Enter>", on_enter)
            button_frame.bind("<Leave>", on_leave)
        
        # تكوين الشبكة
        for i in range(4):
            buttons_grid.grid_columnconfigure(i, weight=1)
        for i in range(3):
            buttons_grid.grid_rowconfigure(i, weight=1)
        
        # الشريط السفلي
        footer_frame = ctk.CTkFrame(main_frame, height=50, fg_color="#34495E")
        footer_frame.pack(fill="x", pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        # معلومات الحالة
        status_label = ctk.CTkLabel(
            footer_frame,
            text="✅ البرنامج جاهز للاستخدام | 👤 المستخدم: مدير النظام | 📅 التاريخ: اليوم",
            font=("Arial", 12),
            text_color="white"
        )
        status_label.pack(expand=True)
        
        print("✅ تم إنشاء الواجهة بنجاح")
        print("🎉 البرنامج جاهز للاستخدام!")
        
        # تشغيل التطبيق
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء التطبيق: {e}")
        import traceback
        traceback.print_exc()
        return False

def darken_color(hex_color):
    """تغميق اللون"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
    return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

def main():
    """الدالة الرئيسية"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🚀 التشغيل المباشر البسيط")
    print("="*50)
    
    # إعداد المسارات
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    sys.path.insert(0, str(project_root))
    
    print(f"📁 مجلد المشروع: {project_root}")
    
    # فحص المكتبات
    try:
        import customtkinter
        print("✅ customtkinter متوفر")
    except ImportError:
        print("❌ customtkinter غير متوفر")
        print("💡 ثبت المكتبة: pip install customtkinter")
        input("اضغط Enter للخروج...")
        return
    
    # تشغيل التطبيق
    print("\n🚀 بدء تشغيل التطبيق...")
    success = create_simple_accounting_app()
    
    if success:
        print("\n✅ تم إغلاق البرنامج بنجاح")
    else:
        print("\n❌ حدث خطأ في التشغيل")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
