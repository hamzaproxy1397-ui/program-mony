#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج ست الكل للمحاسبة - خطوط مكبرة للوضوح
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


class LargeFontMainWindow:
    def __init__(self):
        self.main_window = ctk.CTk()
        self.setup_window()
        self.create_main_content()

    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.main_window.title("برنامج ست الكل للمحاسبة - خطوط مكبرة")

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
        main_frame = ctk.CTkFrame(self.main_window, fg_color="#2C2C2C")
        main_frame.pack(fill="both", expand=True)

        self.create_top_menu_bar(main_frame)
        self.create_green_bar(main_frame)
        self.create_main_grid(main_frame)

    def create_top_menu_bar(self, parent):
        """إنشاء الشريط العلوي مع خطوط مكبرة"""
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
            font=("Cairo", 18)
        )
        self.search_entry.pack(side="left", padx=(0, 8))

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=40,
            height=35,
            fg_color="#4CAF50",
            font=("Segoe UI Emoji", 20),
            command=self.perform_search
        )
        search_btn.pack(side="left")

        # القائمة الرئيسية
        menu_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        menu_frame.pack(side="right", padx=25, pady=8)

        menu_items = [
            "الرئيسية", "برنامج", "الحسابات", "الخزينة", "التقارير",
            "المراكز", "المبيعات", "المشتريات", "خدمة العملاء", "مساعدة",
            "اشتراك", "تنشيط"
        ]

        for item in menu_items:
            menu_btn = ctk.CTkButton(
                menu_frame,
                text=item,
                width=85,
                height=35,
                fg_color="transparent",
                text_color="#333333",
                hover_color="#E0E0E0",
                corner_radius=0,
                border_width=0,
                font=("Cairo", 16, "bold"),
                command=lambda x=item: self.menu_click(x)
            )
            menu_btn.pack(side="right", padx=1)

    def create_green_bar(self, parent):
        """إنشاء الشريط الأخضر مع خطوط مكبرة"""
        green_bar = ctk.CTkFrame(parent, fg_color="#2E8B57")
        green_bar.pack(fill="x", pady=(0, 10))
        # إزالة pack_propagate(False) للسماح للمحتوى بتحديد الارتفاع

        # الشعار
        logo_frame = ctk.CTkFrame(
            green_bar,
            width=200,
            height=100,
            fg_color="#1B5E20",
            corner_radius=15
        )
        logo_frame.pack(side="left", padx=25, pady=10)
        logo_frame.pack_propagate(False)

        # تحميل صورة الشعار
        try:
            if Image and os.path.exists("assets/logo/222555.png"):
                logo_image = ctk.CTkImage(
                    light_image=Image.open("assets/logo/222555.png"),
                    size=(160, 70)
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
                font=("Cairo", 18, "bold"),
                text_color="white",
                justify="center"
            )
        logo_label.pack(expand=True)

        # الأيقونات
        icons_frame = ctk.CTkFrame(green_bar, fg_color="transparent")
        icons_frame.pack(fill="x", padx=50, pady=10)

        green_icons = [
            ("assets/icons/1.png", "الموظفين"), ("assets/icons/5.png", "المحاسبة"),
            ("assets/icons/6.png", "الحسابات"), ("assets/icons/7.png", "الخزينة"),
            ("assets/icons/4.png", "الفواتير"), ("assets/icons/8.png", "التقارير")
        ]

        for icon_path, text in green_icons:
            self.create_green_icon(icons_frame, icon_path, text)

    def create_green_icon(self, parent, icon_path, text):
        """إنشاء أيقونة في الشريط الأخضر مع أيقونة حقيقية وخط مكبر"""
        icon_frame = ctk.CTkFrame(
            parent, width=120, fg_color="transparent"
        )
        icon_frame.pack(side="right", padx=20, pady=5)
        # إزالة الارتفاع الثابت للسماح للأيقونة بالظهور كاملة

        # تحميل الأيقونة الحقيقية
        icon_image = self.load_icon(icon_path, (56, 56))
        if icon_image:
            icon_label = ctk.CTkLabel(
                icon_frame,
                image=icon_image,
                text="",
                fg_color="transparent"
            )
        else:
            # أيقونة احتياطية نصية
            icon_label = ctk.CTkLabel(
                icon_frame,
                text="📁",
                font=("Segoe UI Emoji", 42),
                text_color="white"
            )
        icon_label.pack(pady=(15, 5))

        # النص
        text_label = ctk.CTkLabel(
            icon_frame,
            text=text,
            font=("Cairo", 18, "bold"),
            text_color="white"
        )
        text_label.pack(pady=(0, 15))

        # تفاعل

        def on_click():
            messagebox.showinfo(text, f"تم النقر على {text}")

        for widget in [icon_frame, icon_label, text_label]:
            widget.bind("<Button-1>", lambda _: on_click())

    def create_main_grid(self, parent):
        """إنشاء الشبكة الرئيسية مع خطوط مكبرة"""
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

        # الأيقونات الـ 18 مع مسارات الصور الحقيقية
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
                self.create_large_grid_button(row_frame, icon_path, text, color)

    def create_large_grid_button(self, parent, icon_path, text, color):
        """إنشاء زر في الشبكة مع أيقونة حقيقية وخط مكبر"""
        # تحميل الأيقونة الحقيقية
        icon_image = self.load_icon(icon_path, (80, 80))

        button_frame = ctk.CTkButton(
            parent,
            width=140,
            height=140,
            fg_color=color,
            corner_radius=18,
            text=text,
            font=("Cairo", 12, "bold"),
            text_color="white",
            image=icon_image if icon_image else None,
            compound="top",
            command=lambda: self.menu_click(text)
        )
        button_frame.pack(side="right", padx=10, pady=8)



    def load_icon(self, icon_path, size=(32, 32)):
        """تحميل أيقونة من ملف"""
        try:
            if Image and os.path.exists(icon_path):
                return ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    size=size
                )
        except Exception as e:
            print(f"خطأ في تحميل الأيقونة {icon_path}: {e}")
        return None

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
        if item == "إعداد":
            self.open_settings_window()
        elif item == "إدخال الأصناف":
            self.open_item_entry_window()
        else:
            messagebox.showinfo(item, f"تم النقر على: {item}")

    def open_settings_window(self):
        """فتح نافذة الإعدادات"""
        try:
            from control_panel.control_panel_window import ControlPanelWindow
            self.settings_window = ControlPanelWindow(self.main_window)
            self.settings_window.show()
        except ImportError as e:
            messagebox.showerror("خطأ", f"لا يمكن تحميل نافذة الإعدادات: {e}")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح الإعدادات: {e}")

    def open_item_entry_window(self):
        """فتح نافذة إدخال الأصناف المتقدمة"""
        try:
            # محاولة تحميل النظام الشامل والمتقدم أولاً (الأحدث والأكثر تطوراً)
            try:
                from windows.advanced_item_entry_comprehensive import (
                    AdvancedItemEntryComprehensive
                )
                self.item_entry_window = AdvancedItemEntryComprehensive(
                    parent=self.main_window
                )
                print("🚀 تم فتح نظام إدخال الأصناف الشامل والمتقدم "
                      "(AI + Analytics + Comprehensive)")
                return
            except ImportError as e:
                print(f"⚠️ فشل تحميل النظام الشامل: {e}")

            # محاولة تحميل النافذة المتقدمة
            try:
                from windows.advanced_item_entry import AdvancedItemEntry
                self.item_entry_window = AdvancedItemEntry(parent=self.main_window)
                print("🚀 تم فتح نافذة إدخال الأصناف المتقدمة (AI-Powered)")
                return
            except ImportError as e:
                print(f"⚠️ فشل تحميل النافذة المتقدمة: {e}")

            # محاولة تحميل النافذة الاحترافية كبديل
            try:
                from windows.item_entry_professional import ProfessionalItemEntry
                self.item_entry_window = ProfessionalItemEntry(
                    parent=self.main_window
                )
                print("🎨 تم فتح نافذة إدخال الأصناف الاحترافية")
                return
            except ImportError as e:
                print(f"⚠️ فشل تحميل النافذة الاحترافية: {e}")

            # في حالة فشل النوافذ المتقدمة، استخدم النافذة العادية
            try:
                from windows.item_entry_tkinter import ItemEntryTkinter
                self.item_entry_window = ItemEntryTkinter(parent=self.main_window)
                print("📝 تم فتح نافذة إدخال الأصناف العادية")
                return
            except ImportError as e:
                print(f"❌ فشل تحميل النافذة العادية: {e}")
                raise e

        except ImportError as e:
            error_msg = (
                f"لا يمكن تحميل نافذة إدخال الأصناف: {e}\n\n"
                "تأكد من تثبيت المكتبات المطلوبة:\n"
                "pip install Pillow matplotlib numpy pandas scikit-learn"
            )
            messagebox.showerror("خطأ", error_msg)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح نافذة إدخال الأصناف: {e}")

    def run(self):
        """تشغيل التطبيق"""
        self.main_window.mainloop()

if __name__ == "__main__":
    print("تشغيل برنامج ست الكل للمحاسبة - خطوط مكبرة...")
    app = LargeFontMainWindow()
    app.run()
