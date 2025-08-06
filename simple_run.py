#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل مبسط لبرنامج ست الكل للمحاسبة
"""

import sys
import os
import tkinter as tk
import customtkinter as ctk
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    Image = None

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# إعداد customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# الخطوط والألوان - خطوط مكبرة للوضوح
FONTS = {
    'arabic': 'Cairo',
    'icon': 'Segoe UI Emoji',
    'sizes': {
        'small': 14,
        'normal': 16,
        'large': 20,
        'xlarge': 24
    }
}

class SimpleMainWindow:
    def __init__(self):
        self.main_window = ctk.CTk()
        self.setup_window()
        self.create_main_content()

    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.main_window.title("برنامج ست الكل للمحاسبة")

        # الحصول على أبعاد الشاشة
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()

        # جعل النافذة تملأ الشاشة بالكامل
        self.main_window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.main_window.configure(fg_color="#2C2C2C")
        self.main_window.resizable(True, True)

        # إضافة مفاتيح للتحكم في ملء الشاشة
        self.main_window.bind('<Escape>', self.toggle_fullscreen)
        self.main_window.bind('<F11>', self.toggle_fullscreen)
        self.is_fullscreen = True

        print(f"📺 حجم الشاشة: {screen_width}x{screen_height}")
        print("🔧 تم تفعيل ملء الشاشة - اضغط Escape أو F11 للتبديل")

    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.main_window.update_idletasks()
        width = 1412
        height = 768
        x = (self.main_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.main_window.winfo_screenheight() // 2) - (height // 2)
        self.main_window.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_fullscreen(self, event=None):
        """التبديل بين ملء الشاشة والحجم العادي"""
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            try:
                self.main_window.state('zoomed')
            except:
                try:
                    self.main_window.attributes('-zoomed', True)
                except:
                    try:
                        self.main_window.attributes('-fullscreen', True)
                    except:
                        screen_width = self.main_window.winfo_screenwidth()
                        screen_height = self.main_window.winfo_screenheight()
                        self.main_window.geometry(f"{screen_width}x{screen_height}+0+0")
        else:
            try:
                self.main_window.state('normal')
            except:
                try:
                    self.main_window.attributes('-zoomed', False)
                except:
                    try:
                        self.main_window.attributes('-fullscreen', False)
                    except:
                        pass
            self.center_window()

    def create_main_content(self):
        """إنشاء محتوى النافذة الرئيسية"""
        # الإطار الرئيسي
        main_frame = ctk.CTkFrame(self.main_window, fg_color="#2C2C2C")
        main_frame.pack(fill="both", expand=True)

        # الشريط العلوي الرمادي
        self.create_top_menu_bar(main_frame)
        
        # الشريط الأخضر
        self.create_green_bar(main_frame)
        
        # المنطقة الرئيسية
        self.create_main_grid(main_frame)

    def create_top_menu_bar(self, parent):
        """إنشاء الشريط العلوي"""
        top_bar = ctk.CTkFrame(parent, height=35, fg_color="#F5F5F5")
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        # شريط البحث
        search_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        search_frame.pack(side="left", padx=10, pady=5)

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="بحث...",
            width=220,
            height=30,
            fg_color="white",
            border_color="#CCCCCC",
            font=(FONTS['arabic'], 14)
        )
        search_entry.pack(side="left", padx=(0, 5))

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=35,
            height=30,
            fg_color="#4CAF50",
            font=(FONTS['icon'], 16)
        )
        search_btn.pack(side="left")

        # القائمة الرئيسية
        menu_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        menu_frame.pack(side="right", padx=20, pady=5)

        menu_items = [
            "تنشيط", "اشتراك", "مساعدة", "خدمة العملاء", "المشتريات", 
            "المبيعات", "المراكز", "التقارير", "الخزينة", "الحسابات", 
            "الرئيسية", "برنامج"
        ]

        for item in menu_items:
            menu_btn = ctk.CTkButton(
                menu_frame,
                text=item,
                width=90,
                height=30,
                fg_color="transparent",
                text_color="#333333",
                hover_color="#E0E0E0",
                corner_radius=0,
                border_width=0,
                font=(FONTS['arabic'], 14)
            )
            menu_btn.pack(side="right", padx=2)

    def create_green_bar(self, parent):
        """إنشاء الشريط الأخضر"""
        green_bar = ctk.CTkFrame(parent, height=160, fg_color="#2E8B57")
        green_bar.pack(fill="x")
        green_bar.pack_propagate(False)

        # الشعار
        logo_frame = ctk.CTkFrame(green_bar, width=280, height=140, fg_color="#1B5E20", corner_radius=15)
        logo_frame.pack(side="left", padx=20, pady=10)
        logo_frame.pack_propagate(False)

        # تحميل صورة الشعار
        try:
            if Image and os.path.exists("assets/logo/222555.png"):
                logo_image = ctk.CTkImage(
                    light_image=Image.open("assets/logo/222555.png"),
                    size=(280, 140)
                )
                logo_label = ctk.CTkLabel(
                    logo_frame,
                    image=logo_image,
                    text="",
                    fg_color="transparent"
                )
            else:
                raise FileNotFoundError
        except:
            # نص الشعار الاحتياطي
            logo_label = ctk.CTkLabel(
                logo_frame,
                text="برنامج ست الكل\nللمحاسبة",
                font=(FONTS['arabic'], 22, "bold"),
                text_color="white",
                justify="center"
            )
        logo_label.pack(expand=True)

        # الأيقونات
        icons_frame = ctk.CTkFrame(green_bar, fg_color="transparent")
        icons_frame.pack(expand=True, fill="both", padx=30, pady=15)

        green_icons = [
            ("assets/icons/14.png", "الموظفين"),
            ("assets/icons/3.png", "المحاسبة"),
            ("assets/icons/6.png", "الحسابات"),
            ("assets/icons/40.png", "الخزينة"),
            ("assets/icons/4.png", "الفواتير"),
            ("assets/icons/4.png", "التقارير")
        ]

        for icon_path, text in green_icons:
            icon_frame = ctk.CTkFrame(
                icons_frame,
                width=110,
                height=130,
                fg_color="transparent"
            )
            icon_frame.pack(side="right", padx=5, pady=5)
            icon_frame.pack_propagate(False)

            # تحميل الأيقونة
            try:
                if Image and os.path.exists(icon_path):
                    icon_image = ctk.CTkImage(
                        light_image=Image.open(icon_path),
                        size=(40, 40)
                    )
                    icon_label = ctk.CTkLabel(
                        icon_frame,
                        image=icon_image,
                        text="",
                        fg_color="transparent"
                    )
                else:
                    raise FileNotFoundError
            except:
                # أيقونة افتراضية
                icon_label = ctk.CTkLabel(
                    icon_frame,
                    text="📊",
                    font=("Segoe UI Emoji", 36),
                    text_color="white",
                    fg_color="transparent"
                )

            icon_label.pack(pady=(20, 5))

            # النص
            text_label = ctk.CTkLabel(
                icon_frame,
                text=text,
                font=(FONTS['arabic'], 16),
                text_color="white"
            )
            text_label.pack(pady=(0, 20))

    def create_main_grid(self, parent):
        """إنشاء الشبكة الرئيسية"""
        main_grid_frame = ctk.CTkFrame(parent, fg_color="#3C3C3C")
        main_grid_frame.pack(fill="both", expand=True)

        # عنوان التقارير
        reports_title = ctk.CTkLabel(
            main_grid_frame,
            text="تقارير",
            font=(FONTS['arabic'], 20, "bold"),
            text_color="white"
        )
        reports_title.pack(anchor="ne", padx=30, pady=(20, 10))

        # الشبكة
        grid_container = ctk.CTkFrame(main_grid_frame, fg_color="transparent")
        grid_container.pack(expand=True, fill="both", padx=50, pady=(5, 20))

        # الأيقونات الـ 18 مع مسارات الصور
        all_icons = [
            # الصف الأول
            ("assets/icons/16.png", "أهلاً بكم", "#5DADE2"),
            ("assets/icons/53.ico", "إعداد", "#5DADE2"),
            ("assets/icons/2.png", "إدخال الأصناف", "#4ECDC4"),
            ("assets/icons/3.png", "إدخال الحسابات", "#F39C12"),
            ("assets/icons/9.png", "الحركة اليومية", "#8E44AD"),
            ("assets/icons/22.png", "تحليل المبيعات", "#3498DB"),
            # الصف الثاني
            ("assets/icons/32.png", "مخزن", "#F39C12"),
            ("assets/icons/43.ico", "بيع", "#27AE60"),
            ("assets/icons/17.png", "شراء", "#E74C3C"),
            ("assets/icons/18.png", "صرف", "#E67E22"),
            ("assets/icons/24.png", "مؤشرات", "#16A085"),
            ("assets/icons/28.png", "مرتجع بيع", "#27AE60"),
            # الصف الثالث
            ("assets/icons/11.png", "عرض أسعار", "#16A085"),
            ("assets/icons/27.png", "مرتجع شراء", "#8E44AD"),
            ("assets/icons/10.png", "كمية", "#9B59B6"),
            ("assets/icons/32.png", "تحويل لمخزن", "#3498DB"),
            ("assets/icons/31.png", "تسوية مخزن", "#1ABC9C"),
            ("assets/icons/44.ico", "مؤشرات", "#16A085")
        ]

        # إنشاء الصفوف
        for row in range(3):
            row_frame = ctk.CTkFrame(grid_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=10)
            
            start_idx = row * 6
            end_idx = start_idx + 6
            
            for icon_path, text, color in all_icons[start_idx:end_idx]:
                self.create_grid_button(row_frame, icon_path, text, color)

    def create_grid_button(self, parent, icon_path, text, color):
        """إنشاء زر في الشبكة"""
        button_frame = ctk.CTkFrame(
            parent,
            width=120,
            height=120,
            fg_color=color,
            corner_radius=15
        )
        button_frame.pack(side="right", padx=8, pady=5)
        button_frame.pack_propagate(False)

        # تحميل الأيقونة
        try:
            if Image and os.path.exists(icon_path):
                icon_image = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    size=(50, 50)
                )
                icon_label = ctk.CTkLabel(
                    button_frame,
                    image=icon_image,
                    text="",
                    fg_color="transparent"
                )
            else:
                raise FileNotFoundError
        except:
            # أيقونة افتراضية
            icon_label = ctk.CTkLabel(
                button_frame,
                text="📊",
                font=("Segoe UI Emoji", 32),
                text_color="white",
                fg_color="transparent"
            )

        icon_label.pack(pady=(15, 5))

        # النص
        text_label = ctk.CTkLabel(
            button_frame,
            text=text,
            font=(FONTS['arabic'], 14, "bold"),
            text_color="white",
            wraplength=100
        )
        text_label.pack(pady=(5, 15))

        # تأثير النقر
        def on_click():
            print(f"تم النقر على: {text}")
            # يمكن إضافة المزيد من الوظائف هنا

        # تأثيرات التمرير
        def on_enter(event):
            button_frame.configure(fg_color=self.darken_color(color))

        def on_leave(event):
            button_frame.configure(fg_color=color)

        # ربط الأحداث
        button_frame.bind("<Button-1>", lambda e: on_click())
        icon_label.bind("<Button-1>", lambda e: on_click())
        text_label.bind("<Button-1>", lambda e: on_click())

        # ربط تأثيرات التمرير
        button_frame.bind("<Enter>", on_enter)
        button_frame.bind("<Leave>", on_leave)
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
        text_label.bind("<Enter>", on_enter)
        text_label.bind("<Leave>", on_leave)

    def darken_color(self, color):
        """تغميق اللون للتأثير عند التمرير"""
        # إزالة # من بداية اللون
        color = color.lstrip('#')
        # تحويل إلى RGB
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        # تغميق بنسبة 20%
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        # تحويل إلى hex
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    def run(self):
        """تشغيل التطبيق"""
        self.main_window.mainloop()

if __name__ == "__main__":
    app = SimpleMainWindow()
    app.run()
