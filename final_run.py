#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج ست الكل للمحاسبة - النسخة النهائية
مع الأيقونات الحقيقية والخطوط المكبرة
"""

import os
import customtkinter as ctk
from tkinter import messagebox

# استيراد PIL للصور
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("تحذير: مكتبة Pillow غير متوفرة - سيتم استخدام أيقونات نصية")

# إعداد customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class FinalMainWindow:
    def __init__(self):
        self.main_window = ctk.CTk()
        self.setup_window()
        self.create_main_content()

    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.main_window.title("برنامج ست الكل للمحاسبة - النسخة النهائية")

        # الحصول على أبعاد الشاشة
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()

        # جعل النافذة تملأ الشاشة بالكامل مع إمكانية التحكم
        self.main_window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.main_window.configure(fg_color="#2C2C2C")

        # تفعيل إمكانية التكبير والتصغير
        self.main_window.resizable(True, True)

        # تعيين الحد الأدنى لحجم النافذة
        self.main_window.minsize(1200, 700)

        # تعيين الحد الأقصى (حجم الشاشة)
        self.main_window.maxsize(screen_width, screen_height)

        # إضافة مفاتيح للتحكم في ملء الشاشة
        self.main_window.bind('<Escape>', self.toggle_fullscreen)
        self.main_window.bind('<F11>', self.toggle_fullscreen)
        self.main_window.bind('<Control-plus>', self.zoom_in)
        self.main_window.bind('<Control-minus>', self.zoom_out)
        self.main_window.bind('<Control-0>', self.reset_zoom)

        # متغير لتتبع حالة ملء الشاشة والتكبير
        self.is_fullscreen = True
        self.zoom_level = 1.0

        print(f"📺 حجم الشاشة: {screen_width}x{screen_height}")
        print("🔧 تم تفعيل ملء الشاشة - اضغط Escape أو F11 للتبديل")
        print("🔍 التحكم: Ctrl+Plus (تكبير), Ctrl+Minus (تصغير), Ctrl+0 (إعادة تعيين)")

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
            # تفعيل ملء الشاشة
            try:
                self.main_window.state('zoomed')  # Windows
            except:
                try:
                    self.main_window.attributes('-zoomed', True)  # Linux
                except:
                    try:
                        self.main_window.attributes('-fullscreen', True)  # macOS
                    except:
                        # fallback للأنظمة الأخرى
                        screen_width = self.main_window.winfo_screenwidth()
                        screen_height = self.main_window.winfo_screenheight()
                        self.main_window.geometry(f"{screen_width}x{screen_height}+0+0")
        else:
            # العودة للحجم العادي
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

    def zoom_in(self, event=None):
        """تكبير النافذة"""
        if self.zoom_level < 1.5:  # حد أقصى للتكبير
            self.zoom_level += 0.1
            self.apply_zoom()

    def zoom_out(self, event=None):
        """تصغير النافذة"""
        if self.zoom_level > 0.7:  # حد أدنى للتصغير
            self.zoom_level -= 0.1
            self.apply_zoom()

    def reset_zoom(self, event=None):
        """إعادة تعيين التكبير"""
        self.zoom_level = 1.0
        self.apply_zoom()

    def apply_zoom(self):
        """تطبيق مستوى التكبير"""
        if not self.is_fullscreen:
            base_width = 1412
            base_height = 768
            new_width = int(base_width * self.zoom_level)
            new_height = int(base_height * self.zoom_level)

            # التأكد من عدم تجاوز حدود الشاشة
            screen_width = self.main_window.winfo_screenwidth()
            screen_height = self.main_window.winfo_screenheight()

            if new_width > screen_width:
                new_width = screen_width
            if new_height > screen_height:
                new_height = screen_height

            # توسيط النافذة
            x = (screen_width - new_width) // 2
            y = (screen_height - new_height) // 2

            self.main_window.geometry(f"{new_width}x{new_height}+{x}+{y}")
            print(f"🔍 مستوى التكبير: {self.zoom_level:.1f}x ({new_width}×{new_height})")

    def load_icon(self, icon_path, size=(50, 50)):
        """تحميل أيقونة من ملف"""
        try:
            if PIL_AVAILABLE and os.path.exists(icon_path):
                return ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    size=size
                )
            return None
        except Exception as e:
            print(f"خطأ في تحميل الأيقونة {icon_path}: {e}")
            return None

    def create_main_content(self):
        """إنشاء محتوى النافذة الرئيسية"""
        # إطار رئيسي مرن
        main_frame = ctk.CTkFrame(self.main_window, fg_color="#2C2C2C")
        main_frame.pack(fill="both", expand=True)

        # تكوين الصفوف والأعمدة للتكيف
        main_frame.grid_rowconfigure(2, weight=1)  # الصف الرئيسي قابل للتمدد
        main_frame.grid_columnconfigure(0, weight=1)  # العمود قابل للتمدد

        self.create_top_menu_bar(main_frame)
        self.create_green_bar(main_frame)
        self.create_main_grid(main_frame)

        # ربط تغيير حجم النافذة بتحديث التخطيط
        self.main_window.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event=None):
        """التعامل مع تغيير حجم النافذة"""
        if event and event.widget == self.main_window:
            # الحصول على الحجم الجديد
            width = self.main_window.winfo_width()
            height = self.main_window.winfo_height()

            # تحديث أحجام العناصر بناءً على حجم النافذة
            self.update_responsive_layout(width, height)

    def update_responsive_layout(self, width, height):
        """تحديث التخطيط ليتكيف مع حجم النافذة"""
        # حساب عامل التكيف
        base_width = 1412
        base_height = 768

        width_factor = width / base_width
        height_factor = height / base_height

        # تحديث أحجام الخطوط بناءً على حجم النافذة
        if hasattr(self, 'search_entry'):
            font_size = max(12, int(16 * min(width_factor, height_factor)))
            try:
                self.search_entry.configure(font=("Cairo", font_size))
            except:
                pass

    def create_top_menu_bar(self, parent):
        """إنشاء الشريط العلوي"""
        top_bar = ctk.CTkFrame(parent, height=40, fg_color="#F5F5F5")
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        # شريط البحث
        search_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        search_frame.pack(side="left", padx=15, pady=8)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="بحث...",
            width=250,
            height=35,
            fg_color="white",
            border_color="#CCCCCC",
            font=("Cairo", 16)
        )
        self.search_entry.pack(side="left", padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self.perform_search())

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=40,
            height=35,
            fg_color="#4CAF50",
            font=("Segoe UI Emoji", 18),
            command=self.perform_search
        )
        search_btn.pack(side="left")

        # القائمة الرئيسية
        menu_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        menu_frame.pack(side="right", padx=25, pady=8)

        menu_items = [
            "تنشيط", "اشتراك", "مساعدة", "خدمة العملاء", "المشتريات", 
            "المبيعات", "المراكز", "التقارير", "الخزينة", "الحسابات", 
            "الرئيسية", "برنامج"
        ]

        for item in menu_items:
            menu_btn = ctk.CTkButton(
                menu_frame,
                text=item,
                width=100,
                height=35,
                fg_color="transparent",
                text_color="#333333",
                hover_color="#E0E0E0",
                corner_radius=0,
                border_width=0,
                font=("Cairo", 16, "bold"),
                command=lambda x=item: self.menu_click(x)
            )
            menu_btn.pack(side="right", padx=3)

    def create_green_bar(self, parent):
        """إنشاء الشريط الأخضر"""
        green_bar = ctk.CTkFrame(parent, height=180, fg_color="#2E8B57")
        green_bar.pack(fill="x")
        green_bar.pack_propagate(False)

        # الشعار
        logo_frame = ctk.CTkFrame(
            green_bar,
            width=280,
            height=120,
            fg_color="#1B5E20",
            corner_radius=15
        )
        logo_frame.pack(side="left", padx=20, pady=10)
        logo_frame.pack_propagate(False)

        # تحميل صورة الشعار
        logo_image = self.load_icon("assets/logo/222555.png", (260, 110))
        if logo_image:
            logo_label = ctk.CTkLabel(
                logo_frame,
                image=logo_image,
                text="",
                fg_color="transparent"
            )
        else:
            # نص الشعار الاحتياطي
            logo_label = ctk.CTkLabel(
                logo_frame,
                text="برنامج ست الكل\nللمحاسبة",
                font=("Cairo", 28, "bold"),
                text_color="white",
                justify="center"
            )
        logo_label.pack(expand=True)

        # الأيقونات
        icons_frame = ctk.CTkFrame(green_bar, fg_color="transparent")
        icons_frame.pack(expand=True, fill="both", padx=40, pady=20)

        green_icons = [
            ("assets/icons/14.png", "الموظفين"),
            ("assets/icons/3.png", "المحاسبة"),
            ("assets/icons/6.png", "الحسابات"),
            ("assets/icons/40.png", "الخزينة"),
            ("assets/icons/4.png", "الفواتير"),
            ("assets/icons/4.png", "التقارير")
        ]

        for icon_path, text in green_icons:
            self.create_green_icon(icons_frame, icon_path, text)

    def create_green_icon(self, parent, icon_path, text):
        """إنشاء أيقونة في الشريط الأخضر"""
        icon_frame = ctk.CTkFrame(parent, width=130, height=150, fg_color="transparent")
        icon_frame.pack(side="right", padx=8, pady=8)
        icon_frame.pack_propagate(False)

        # تحميل الأيقونة
        icon_image = self.load_icon(icon_path, (45, 45))
        if icon_image:
            icon_label = ctk.CTkLabel(
                icon_frame,
                image=icon_image,
                text="",
                fg_color="transparent"
            )
        else:
            # أيقونة افتراضية
            icon_label = ctk.CTkLabel(
                icon_frame,
                text="📊",
                font=("Segoe UI Emoji", 42),
                text_color="white",
                fg_color="transparent"
            )

        icon_label.pack(pady=(25, 8))

        # النص
        text_label = ctk.CTkLabel(
            icon_frame,
            text=text,
            font=("Cairo", 18, "bold"),
            text_color="white"
        )
        text_label.pack(pady=(0, 25))

        # تفاعل
        def on_click():
            messagebox.showinfo(text, f"تم النقر على {text}")

        def on_enter(event):
            icon_frame.configure(fg_color="rgba(255,255,255,0.1)")

        def on_leave(event):
            icon_frame.configure(fg_color="transparent")

        for widget in [icon_frame, icon_label, text_label]:
            widget.bind("<Button-1>", lambda e: on_click())
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_main_grid(self, parent):
        """إنشاء الشبكة الرئيسية"""
        main_grid_frame = ctk.CTkFrame(parent, fg_color="#3C3C3C")
        main_grid_frame.pack(fill="both", expand=True)

        # عنوان التقارير
        reports_title = ctk.CTkLabel(
            main_grid_frame,
            text="تقارير",
            font=("Cairo", 24, "bold"),
            text_color="white"
        )
        reports_title.pack(anchor="ne", padx=40, pady=(25, 15))

        # الشبكة
        grid_container = ctk.CTkFrame(main_grid_frame, fg_color="transparent")
        grid_container.pack(expand=True, fill="both", padx=60, pady=(5, 25))

        # الأيقونات الـ 18
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
            row_frame.pack(fill="x", pady=12)
            
            start_idx = row * 6
            end_idx = start_idx + 6
            
            for icon_path, text, color in all_icons[start_idx:end_idx]:
                self.create_grid_button(row_frame, icon_path, text, color)

    def create_grid_button(self, parent, icon_path, text, color):
        """إنشاء زر في الشبكة"""
        button_frame = ctk.CTkFrame(
            parent,
            width=140,
            height=140,
            fg_color=color,
            corner_radius=18
        )
        button_frame.pack(side="right", padx=10, pady=8)
        button_frame.pack_propagate(False)

        # تحميل الأيقونة
        icon_image = self.load_icon(icon_path, (55, 55))
        if icon_image:
            icon_label = ctk.CTkLabel(
                button_frame,
                image=icon_image,
                text="",
                fg_color="transparent"
            )
        else:
            # أيقونة افتراضية
            icon_label = ctk.CTkLabel(
                button_frame,
                text="📊",
                font=("Segoe UI Emoji", 38),
                text_color="white",
                fg_color="transparent"
            )

        icon_label.pack(pady=(20, 8))

        # النص
        text_label = ctk.CTkLabel(
            button_frame,
            text=text,
            font=("Cairo", 16, "bold"),
            text_color="white",
            wraplength=120
        )
        text_label.pack(pady=(8, 20))

        # تفاعل محسن
        original_color = color
        
        def on_click():
            messagebox.showinfo(text, f"تم النقر على: {text}")

        def on_enter(event):
            darkened = self.darken_color(original_color)
            button_frame.configure(fg_color=darkened)

        def on_leave(event):
            button_frame.configure(fg_color=original_color)

        # ربط الأحداث
        for widget in [button_frame, icon_label, text_label]:
            widget.bind("<Button-1>", lambda e: on_click())
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def darken_color(self, color):
        """تغميق اللون للتأثير عند التمرير"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    def perform_search(self):
        """تنفيذ البحث"""
        search_text = self.search_entry.get()
        if search_text:
            messagebox.showinfo("بحث", f"البحث عن: {search_text}")
        else:
            messagebox.showwarning("تحذير", "يرجى إدخال نص للبحث")

    def menu_click(self, item):
        """معالجة النقر على عناصر القائمة"""
        messagebox.showinfo(item, f"تم النقر على: {item}")

    def run(self):
        """تشغيل التطبيق"""
        print("🚀 تشغيل برنامج ست الكل للمحاسبة - النسخة النهائية")
        print("✅ الأيقونات الحقيقية مفعلة" if PIL_AVAILABLE else "⚠️ أيقونات نصية احتياطية")
        self.main_window.mainloop()

if __name__ == "__main__":
    app = FinalMainWindow()
    app.run()
