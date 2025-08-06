# -*- coding: utf-8 -*-
"""
صفحة الإعدادات العامة
General Settings Page
"""

import sys
from pathlib import Path

# إضافة مسار المشروع للاستيراد
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import customtkinter as ctk
    from tkinter import messagebox
except ImportError as e:
    print(f"خطأ في استيراد المكتبات: {e}")
    sys.exit(1)

from core.settings_manager import settings_manager

class GeneralSettingsPage:
    """صفحة الإعدادات العامة"""
    
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.widgets = {}
        self.create_content()
        self.load_settings()
    
    def create_content(self):
        """إنشاء محتوى الصفحة"""
        # قسم اللغة والخط
        self.create_language_section()
        
        # قسم المظهر
        self.create_appearance_section()
        
        # قسم السلوك العام
        self.create_behavior_section()
    
    def create_language_section(self):
        """قسم إعدادات اللغة والخط"""
        # إطار القسم
        lang_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        lang_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            lang_frame,
            text="🌐 اللغة والخط",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(lang_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # اللغة
        lang_label = ctk.CTkLabel(
            grid_frame,
            text="اللغة:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        lang_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['language'] = ctk.CTkComboBox(
            grid_frame,
            values=["العربية", "English"],
            width=200,
            font=("Cairo", 12)
        )
        self.widgets['language'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # نوع الخط
        font_label = ctk.CTkLabel(
            grid_frame,
            text="نوع الخط:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        font_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['font_family'] = ctk.CTkComboBox(
            grid_frame,
            values=["Cairo", "Tajawal", "Amiri", "Noto Kufi Arabic", "Arial"],
            width=200,
            font=("Cairo", 12)
        )
        self.widgets['font_family'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # حجم الخط
        font_size_label = ctk.CTkLabel(
            grid_frame,
            text="حجم الخط:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        font_size_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['font_size'] = ctk.CTkComboBox(
            grid_frame,
            values=["10", "11", "12", "13", "14", "15", "16", "18", "20"],
            width=200,
            font=("Cairo", 12)
        )
        self.widgets['font_size'].grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        # اتجاه النص
        rtl_label = ctk.CTkLabel(
            grid_frame,
            text="اتجاه النص:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        rtl_label.grid(row=3, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['rtl_direction'] = ctk.CTkCheckBox(
            grid_frame,
            text="من اليمين إلى اليسار (RTL)",
            font=("Cairo", 12)
        )
        self.widgets['rtl_direction'].grid(row=3, column=0, sticky="w", padx=10, pady=5)
    
    def create_appearance_section(self):
        """قسم إعدادات المظهر"""
        # إطار القسم
        appearance_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        appearance_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            appearance_frame,
            text="🎨 المظهر",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # الثيم
        theme_label = ctk.CTkLabel(
            grid_frame,
            text="الثيم:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        theme_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['theme'] = ctk.CTkComboBox(
            grid_frame,
            values=["فاتح", "داكن", "تلقائي"],
            width=200,
            font=("Cairo", 12),
            command=self.on_theme_change
        )
        self.widgets['theme'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    def create_behavior_section(self):
        """قسم السلوك العام"""
        # إطار القسم
        behavior_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        behavior_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            behavior_frame,
            text="⚙️ السلوك العام",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(behavior_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # الحفظ التلقائي
        self.widgets['auto_save'] = ctk.CTkCheckBox(
            grid_frame,
            text="الحفظ التلقائي للبيانات",
            font=("Cairo", 12)
        )
        self.widgets['auto_save'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # النافذة الافتراضية عند البدء
        startup_label = ctk.CTkLabel(
            grid_frame,
            text="النافذة الافتراضية عند البدء:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        startup_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['startup_window'] = ctk.CTkComboBox(
            grid_frame,
            values=["الرئيسية", "المبيعات", "المشتريات", "التقارير"],
            width=200,
            font=("Cairo", 12)
        )
        self.widgets['startup_window'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # أزرار الحفظ والإلغاء
        buttons_frame = ctk.CTkFrame(behavior_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ الإعدادات",
            width=150,
            height=35,
            font=("Cairo", 12),
            fg_color="#28a745",
            hover_color="#218838",
            command=self.save_settings
        )
        save_btn.pack(side="left", padx=5)
        
        reset_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 إعادة تعيين",
            width=150,
            height=35,
            font=("Cairo", 12),
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.reset_settings
        )
        reset_btn.pack(side="left", padx=5)
    
    def load_settings(self):
        """تحميل الإعدادات الحالية"""
        general_settings = settings_manager.get_section("general")
        
        # تحميل القيم في الواجهة
        if 'language' in self.widgets:
            lang_value = "العربية" if general_settings.get("language") == "ar" else "English"
            self.widgets['language'].set(lang_value)
        
        if 'font_family' in self.widgets:
            self.widgets['font_family'].set(general_settings.get("font_family", "Cairo"))
        
        if 'font_size' in self.widgets:
            self.widgets['font_size'].set(str(general_settings.get("font_size", 12)))
        
        if 'rtl_direction' in self.widgets:
            if general_settings.get("rtl_direction", True):
                self.widgets['rtl_direction'].select()
            else:
                self.widgets['rtl_direction'].deselect()
        
        if 'theme' in self.widgets:
            theme_map = {"light": "فاتح", "dark": "داكن", "system": "تلقائي"}
            theme_value = theme_map.get(general_settings.get("theme", "light"), "فاتح")
            self.widgets['theme'].set(theme_value)
        
        if 'auto_save' in self.widgets:
            if general_settings.get("auto_save", True):
                self.widgets['auto_save'].select()
            else:
                self.widgets['auto_save'].deselect()
        
        if 'startup_window' in self.widgets:
            startup_map = {"main": "الرئيسية", "sales": "المبيعات", "purchases": "المشتريات", "reports": "التقارير"}
            startup_value = startup_map.get(general_settings.get("startup_window", "main"), "الرئيسية")
            self.widgets['startup_window'].set(startup_value)
    
    def save_settings(self):
        """حفظ الإعدادات"""
        try:
            # تحويل القيم من الواجهة
            language = "ar" if self.widgets['language'].get() == "العربية" else "en"
            font_family = self.widgets['font_family'].get()
            font_size = int(self.widgets['font_size'].get())
            rtl_direction = self.widgets['rtl_direction'].get() == 1
            
            theme_map = {"فاتح": "light", "داكن": "dark", "تلقائي": "system"}
            theme = theme_map.get(self.widgets['theme'].get(), "light")
            
            auto_save = self.widgets['auto_save'].get() == 1
            
            startup_map = {"الرئيسية": "main", "المبيعات": "sales", "المشتريات": "purchases", "التقارير": "reports"}
            startup_window = startup_map.get(self.widgets['startup_window'].get(), "main")
            
            # حفظ الإعدادات
            settings_manager.set_setting("general", "language", language)
            settings_manager.set_setting("general", "font_family", font_family)
            settings_manager.set_setting("general", "font_size", font_size)
            settings_manager.set_setting("general", "rtl_direction", rtl_direction)
            settings_manager.set_setting("general", "theme", theme)
            settings_manager.set_setting("general", "auto_save", auto_save)
            settings_manager.set_setting("general", "startup_window", startup_window)
            
            if settings_manager.save_settings():
                messagebox.showinfo("نجح", "تم حفظ الإعدادات العامة بنجاح!")
            else:
                messagebox.showerror("خطأ", "فشل في حفظ الإعدادات!")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ الإعدادات: {e}")
    
    def reset_settings(self):
        """إعادة تعيين الإعدادات للقيم الافتراضية"""
        result = messagebox.askyesno(
            "تأكيد",
            "هل أنت متأكد من إعادة تعيين الإعدادات العامة للقيم الافتراضية؟"
        )
        if result:
            settings_manager.reset_section("general")
            self.load_settings()
            messagebox.showinfo("تم", "تم إعادة تعيين الإعدادات العامة!")
    
    def on_theme_change(self, value):
        """تغيير الثيم فوراً"""
        theme_map = {"فاتح": "light", "داكن": "dark", "تلقائي": "system"}
        theme = theme_map.get(value, "light")
        ctk.set_appearance_mode(theme)
