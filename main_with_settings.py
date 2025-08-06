#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج ست الكل للمحاسبة - مع نافذة الإعدادات المدمجة
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

class MainWindowWithSettings:
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
        
        print(f"📺 حجم الشاشة: {screen_width}x{screen_height}")
        
        # تعيين النافذة لملء الشاشة
        self.main_window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.main_window.state('zoomed')
        
        # ربط مفاتيح الاختصار
        self.main_window.bind('<Escape>', lambda e: self.toggle_fullscreen())
        self.main_window.bind('<F11>', lambda e: self.toggle_fullscreen())
        
        print("🔧 تم تفعيل ملء الشاشة - اضغط Escape أو F11 للتبديل")

    def toggle_fullscreen(self):
        """تبديل وضع ملء الشاشة"""
        current_state = self.main_window.state()
        if current_state == 'zoomed':
            self.main_window.state('normal')
            self.main_window.geometry("1200x800+100+50")
        else:
            self.main_window.state('zoomed')

    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        # إطار رئيسي
        main_frame = ctk.CTkFrame(self.main_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # العنوان
        title_label = ctk.CTkLabel(
            main_frame,
            text="برنامج ست الكل للمحاسبة",
            font=("Cairo", 32, "bold"),
            text_color="#2C3E50"
        )
        title_label.pack(pady=(0, 30))
        
        # شبكة الأزرار
        self.create_button_grid(main_frame)

    def create_button_grid(self, parent):
        """إنشاء شبكة الأزرار"""
        # إطار الشبكة
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(expand=True, fill="both")
        
        # الأزرار الرئيسية
        buttons = [
            ("🏠", "الرئيسية", "#3498DB"),
            ("⚙️", "إعداد", "#E74C3C"),  # زر الإعدادات
            ("📊", "التقارير", "#2ECC71"),
            ("💰", "المبيعات", "#F39C12"),
            ("📦", "المخزون", "#9B59B6"),
            ("👥", "العملاء", "#1ABC9C")
        ]
        
        # إنشاء الأزرار في شبكة 3x2
        for i, (icon, text, color) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            button = ctk.CTkButton(
                grid_frame,
                text=f"{icon}\n{text}",
                width=200,
                height=150,
                font=("Cairo", 18, "bold"),
                fg_color=color,
                corner_radius=15,
                command=lambda t=text: self.button_click(t)
            )
            button.grid(row=row, col=col, padx=20, pady=20, sticky="nsew")
        
        # تكوين الشبكة
        for i in range(3):
            grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            grid_frame.grid_rowconfigure(i, weight=1)

    def button_click(self, button_text):
        """معالجة النقر على الأزرار"""
        if button_text == "إعداد":
            self.open_settings()
        else:
            messagebox.showinfo(button_text, f"تم النقر على: {button_text}")

    def open_settings(self):
        """فتح نافذة الإعدادات"""
        try:
            from control_panel.control_panel_window import ControlPanelWindow
            self.settings_window = ControlPanelWindow(self.main_window)
            self.settings_window.show()
        except ImportError as e:
            messagebox.showerror("خطأ", f"لا يمكن تحميل نافذة الإعدادات: {e}")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح الإعدادات: {e}")

    def run(self):
        """تشغيل التطبيق"""
        self.main_window.mainloop()

if __name__ == "__main__":
    print("تشغيل برنامج ست الكل للمحاسبة مع الإعدادات...")
    app = MainWindowWithSettings()
    app.run()
