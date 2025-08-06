#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج ست الكل للمحاسبة - النسخة المحسنة
مطابق تماماً للصورة المرجعية مع تحسينات إضافية
"""

import os

import customtkinter as ctk

from tkinter import messagebox

try:
    from PIL import Image
except ImportError:
    Image = None

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

# الألوان مطابقة للصورة
COLORS = {
    'top_bar': '#F5F5F5',
    'green_bar': '#2E8B57',
    'logo_bg': '#1B5E20',
    'main_bg': '#3C3C3C',
    'dark_bg': '#2C2C2C',
    'search_btn': '#4CAF50',
    'text_dark': '#333333',
    'text_light': '#FFFFFF',
    'border': '#CCCCCC',
    'hover': '#E0E0E0'
}


class EnhancedMainWindow:
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
        self.main_window.configure(fg_color=COLORS['dark_bg'])

        # تفعيل إمكانية التكبير والتصغير
        self.main_window.resizable(True, True)

        # تعيين الحد الأدنى والأقصى لحجم النافذة
        self.main_window.minsize(1200, 700)
        self.main_window.maxsize(screen_width, screen_height)

        # إضافة مفاتيح للتحكم
        self.main_window.bind('<Escape>', self.toggle_fullscreen)
        self.main_window.bind('<F11>', self.toggle_fullscreen)
        self.main_window.bind('<Control-plus>', self.zoom_in)
        self.main_window.bind('<Control-minus>', self.zoom_out)
        self.main_window.bind('<Control-0>', self.reset_zoom)

        # متغيرات التحكم
        self.is_fullscreen = True
        self.zoom_level = 1.0

        # إعداد أيقونة النافذة (إذا كانت متوفرة)
        try:
            self.main_window.iconbitmap("assets/icons/app_icon.ico")
        except:
            pass

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

    def toggle_fullscreen(self, _=None):
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
                        geometry = f"{screen_width}x{screen_height}+0+0"
                        self.main_window.geometry(geometry)
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
        main_frame = ctk.CTkFrame(self.main_window, fg_color=COLORS['dark_bg'])
        main_frame.pack(fill="both", expand=True)

        # الشريط العلوي الرمادي
        self.create_top_menu_bar(main_frame)
        
        # الشريط الأخضر
        self.create_green_bar(main_frame)
        
        # المنطقة الرئيسية
        self.create_main_grid(main_frame)

    def create_top_menu_bar(self, parent):
        """إنشاء الشريط العلوي مطابق للصورة"""
        top_bar = ctk.CTkFrame(parent, height=35, fg_color=COLORS['top_bar'])
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        # شريط البحث في الجانب الأيسر
        search_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        search_frame.pack(side="left", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="بحث...",
            width=220,
            height=30,
            fg_color="white",
            border_color=COLORS['border'],
            font=(FONTS['arabic'], 16)
        )
        self.search_entry.pack(side="left", padx=(0, 5))
        self.search_entry.bind("<Return>", self.perform_search)

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=35,
            height=30,
            fg_color=COLORS['search_btn'],
            hover_color="#45A049",
            command=self.perform_search,
            font=(FONTS['icon'], 18)
        )
        search_btn.pack(side="left")

        # القائمة الرئيسية من اليمين إلى اليسار
        menu_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        menu_frame.pack(side="right", padx=20, pady=5)

        # عناصر القائمة مطابقة للصورة
        menu_items = [
            ("تنشيط", self.show_activation),
            ("اشتراك", self.show_subscription),
            ("مساعدة", self.show_help),
            ("خدمة العملاء", self.show_customer_service),
            ("المشتريات", self.show_purchases),
            ("المبيعات", self.show_sales),
            ("المراكز", self.show_centers),
            ("التقارير", self.show_reports),
            ("الخزينة", self.show_treasury),
            ("الحسابات", self.show_accounts),
            ("الرئيسية", self.show_main),
            ("برنامج", self.show_program_menu)
        ]

        for text, command in menu_items:
            menu_btn = ctk.CTkButton(
                menu_frame,
                text=text,
                command=command,
                width=90,
                height=30,
                fg_color="transparent",
                text_color=COLORS['text_dark'],
                hover_color=COLORS['hover'],
                font=(FONTS['arabic'], 16),
                corner_radius=0,
                border_width=0
            )
            menu_btn.pack(side="right", padx=2)

    def create_green_bar(self, parent):
        """إنشاء الشريط الأخضر مطابق للصورة"""
        green_bar = ctk.CTkFrame(parent, height=160, fg_color=COLORS['green_bar'])
        green_bar.pack(fill="x")
        green_bar.pack_propagate(False)

        # الشعار في الجانب الأيسر
        logo_frame = ctk.CTkFrame(
            green_bar, 
            width=280, 
            height=140, 
            fg_color=COLORS['logo_bg'], 
            corner_radius=15
        )
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
                font=(FONTS['arabic'], 24, "bold"),
                text_color=COLORS['text_light'],
                justify="center"
            )
        logo_label.pack(expand=True)

        # الأيقونات الست في الشريط الأخضر
        icons_frame = ctk.CTkFrame(green_bar, fg_color="transparent")
        icons_frame.pack(expand=True, fill="both", padx=30, pady=15)

        # الأيقونات مطابقة للصورة
        green_icons = [
            ("assets/icons/14.png", "الموظفين", self.show_employees),
            ("assets/icons/3.png", "المحاسبة", self.show_accounting),
            ("assets/icons/6.png", "الحسابات", self.show_accounts),
            ("assets/icons/40.png", "الخزينة", self.show_treasury),
            ("assets/icons/4.png", "الفواتير", self.show_invoices),
            ("assets/icons/4.png", "التقارير", self.show_reports)
        ]

        for icon_path, text, command in green_icons:
            self.create_green_icon(icons_frame, icon_path, text, command)

    def create_green_icon(self, parent, icon_path, text, command):
        """إنشاء أيقونة في الشريط الأخضر"""
        icon_frame = ctk.CTkFrame(
            parent,
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
            # أيقونة افتراضية في حالة فشل التحميل
            icon_label = ctk.CTkLabel(
                icon_frame,
                text="📊",
                font=(FONTS['icon'], 30),
                text_color=COLORS['text_light'],
                fg_color="transparent"
            )

        icon_label.pack(pady=(20, 5))

        # النص
        text_label = ctk.CTkLabel(
            icon_frame,
            text=text,
            font=(FONTS['arabic'], 12),
            text_color=COLORS['text_light']
        )
        text_label.pack(pady=(0, 20))

        # تأثيرات التفاعل

        def on_click():
            command()

        def on_enter(_):
            icon_frame.configure(fg_color="rgba(255,255,255,0.1)")

        def on_leave(_):
            icon_frame.configure(fg_color="transparent")

        # ربط الأحداث
        for widget in [icon_frame, icon_label, text_label]:
            widget.bind("<Button-1>", lambda _: on_click())
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_main_grid(self, parent):
        """إنشاء الشبكة الرئيسية مطابقة للصورة"""
        main_grid_frame = ctk.CTkFrame(parent, fg_color=COLORS['main_bg'])
        main_grid_frame.pack(fill="both", expand=True)

        # عنوان التقارير في الزاوية اليمنى العلوية
        reports_title = ctk.CTkLabel(
            main_grid_frame,
            text="تقارير",
            font=(FONTS['arabic'], 16, "bold"),
            text_color=COLORS['text_light']
        )
        reports_title.pack(anchor="ne", padx=30, pady=(20, 10))

        # الشبكة
        grid_container = ctk.CTkFrame(main_grid_frame, fg_color="transparent")
        grid_container.pack(expand=True, fill="both", padx=50, pady=(5, 20))

        # الأيقونات الـ 18 مطابقة للصورة تماماً
        all_icons = [
            # الصف الأول
            ("assets/icons/16.png", "أهلاً بكم", "#5DADE2", self.show_welcome),
            ("assets/icons/53.ico", "إعداد", "#5DADE2", self.show_settings),
            ("assets/icons/2.png", "إدخال الأصناف", "#4ECDC4", self.show_items),
            ("assets/icons/3.png", "إدخال الحسابات", "#F39C12",
             self.show_accounts_entry),
            ("assets/icons/9.png", "الحركة اليومية", "#8E44AD", self.show_daily),
            ("assets/icons/22.png", "تحليل المبيعات", "#3498DB",
             self.show_sales_analysis),
            # الصف الثاني
            ("assets/icons/32.png", "مخزن", "#F39C12", self.show_warehouse),
            ("assets/icons/43.ico", "بيع", "#27AE60", self.show_sales),
            ("assets/icons/17.png", "شراء", "#E74C3C", self.show_purchases),
            ("assets/icons/18.png", "صرف", "#E67E22", self.show_expenses),
            ("assets/icons/24.png", "مؤشرات", "#16A085", self.show_indicators),
            ("assets/icons/28.png", "مرتجع بيع", "#27AE60", self.show_sales_return),
            # الصف الثالث
            ("assets/icons/11.png", "عرض أسعار", "#16A085", self.show_quotes),
            ("assets/icons/27.png", "مرتجع شراء", "#8E44AD",
             self.show_purchase_return),
            ("assets/icons/10.png", "كمية", "#9B59B6", self.show_quantity),
            ("assets/icons/32.png", "تحويل لمخزن", "#3498DB", self.show_transfer),
            ("assets/icons/31.png", "تسوية مخزن", "#1ABC9C", self.show_adjustment),
            ("assets/icons/44.ico", "مؤشرات", "#16A085", self.show_indicators)
        ]

        # إنشاء الصفوف
        for row in range(3):
            row_frame = ctk.CTkFrame(grid_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=10)
            
            start_idx = row * 6
            end_idx = start_idx + 6
            
            for icon_path, text, color, command in all_icons[start_idx:end_idx]:
                self.create_grid_button(row_frame, icon_path, text, color, command)

    def create_grid_button(self, parent, icon_path, text, color, command):
        """إنشاء زر في الشبكة مع تأثيرات محسنة"""
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
            # أيقونة افتراضية في حالة فشل التحميل
            icon_label = ctk.CTkLabel(
                button_frame,
                text="📊",
                font=(FONTS['icon'], 24),
                text_color=COLORS['text_light'],
                fg_color="transparent"
            )

        icon_label.pack(pady=(15, 5))

        # النص
        text_label = ctk.CTkLabel(
            button_frame,
            text=text,
            font=(FONTS['arabic'], 11),
            text_color=COLORS['text_light'],
            wraplength=100
        )
        text_label.pack(pady=(5, 15))

        # تأثيرات التفاعل المحسنة
        original_color = color
        
        def on_click():
            command()

        def on_enter(_):
            darkened = self.darken_color(original_color)
            button_frame.configure(fg_color=darkened)

        def on_leave(_):
            button_frame.configure(fg_color=original_color)

        # ربط الأحداث
        for widget in [button_frame, icon_label, text_label]:
            widget.bind("<Button-1>", lambda _: on_click())
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def darken_color(self, color):
        """تغميق اللون للتأثير عند التمرير"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    # دوال الأحداث

    def perform_search(self, _=None):
        """تنفيذ البحث"""
        search_text = self.search_entry.get()
        if search_text:
            messagebox.showinfo("بحث", f"البحث عن: {search_text}")
        else:
            messagebox.showwarning("تحذير", "يرجى إدخال نص للبحث")

    # دوال القائمة العلوية

    def show_activation(self):
        messagebox.showinfo("تنشيط", "صفحة التنشيط")

    def show_subscription(self):
        messagebox.showinfo("اشتراك", "صفحة الاشتراك")

    def show_help(self):
        messagebox.showinfo("مساعدة", "صفحة المساعدة")

    def show_customer_service(self):
        messagebox.showinfo("خدمة العملاء", "صفحة خدمة العملاء")

    def show_centers(self):
        messagebox.showinfo("المراكز", "صفحة المراكز")

    def show_main(self):
        messagebox.showinfo("الرئيسية", "الصفحة الرئيسية")

    def show_program_menu(self):
        messagebox.showinfo("برنامج", "قائمة البرنامج")

    # دوال الشريط الأخضر

    def show_employees(self):
        messagebox.showinfo("الموظفين", "إدارة الموظفين")

    def show_accounting(self):
        messagebox.showinfo("المحاسبة", "نظام المحاسبة")

    def show_accounts(self):
        messagebox.showinfo("الحسابات", "إدارة الحسابات")

    def show_treasury(self):
        messagebox.showinfo("الخزينة", "إدارة الخزينة")

    def show_invoices(self):
        messagebox.showinfo("الفواتير", "إدارة الفواتير")

    def show_reports(self):
        messagebox.showinfo("التقارير", "عرض التقارير")

    # دوال الشبكة الرئيسية

    def show_welcome(self):
        messagebox.showinfo("أهلاً بكم", "مرحباً بكم في برنامج ست الكل")

    def show_settings(self):
        messagebox.showinfo("إعداد", "إعدادات البرنامج")

    def show_items(self):
        messagebox.showinfo("إدخال الأصناف", "إدارة الأصناف")

    def show_accounts_entry(self):
        messagebox.showinfo("إدخال الحسابات", "إدخال حسابات جديدة")

    def show_daily(self):
        messagebox.showinfo("الحركة اليومية", "الحركة اليومية")

    def show_sales_analysis(self):
        messagebox.showinfo("تحليل المبيعات", "تحليل المبيعات")

    def show_warehouse(self):
        messagebox.showinfo("مخزن", "إدارة المخزن")

    def show_sales(self):
        messagebox.showinfo("بيع", "عمليات البيع")

    def show_purchases(self):
        messagebox.showinfo("شراء", "عمليات الشراء")

    def show_expenses(self):
        messagebox.showinfo("صرف", "إدارة المصروفات")

    def show_indicators(self):
        messagebox.showinfo("مؤشرات", "المؤشرات والإحصائيات")

    def show_sales_return(self):
        messagebox.showinfo("مرتجع بيع", "مرتجعات البيع")

    def show_quotes(self):
        messagebox.showinfo("عرض أسعار", "عروض الأسعار")

    def show_purchase_return(self):
        messagebox.showinfo("مرتجع شراء", "مرتجعات الشراء")

    def show_quantity(self): messagebox.showinfo("كمية", "إدارة الكميات")

    def show_transfer(self): messagebox.showinfo("تحويل لمخزن", "تحويل المخزون")

    def show_adjustment(self): messagebox.showinfo("تسوية مخزن", "تسوية المخزون")

    def run(self):
        """تشغيل التطبيق"""
        self.main_window.mainloop()

if __name__ == "__main__":
    app = EnhancedMainWindow()
    app.run()
