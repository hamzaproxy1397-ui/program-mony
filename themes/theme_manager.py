# -*- coding: utf-8 -*-
"""
مدير الثيمات والألوان
"""

import customtkinter as ctk
from themes.font_manager import font_manager, get_arabic_font

class ThemeManager:
    """مدير الثيمات والألوان"""

    def __init__(self):
        self.current_theme = "light"
        self.themes = self.load_themes()
        self.apply_theme(self.current_theme)

    def load_themes(self):
        """تحميل الثيمات المتاحة"""
        return {
            "light": {
                "name": "الثيم الفاتح",
                "colors": {
                    # الألوان الأساسية
                    "primary": "#2E8B57",           # أخضر البرنامج الرئيسي
                    "secondary": "#4682B4",         # أزرق ثانوي
                    "background": "#F5F5F5",        # خلفية رئيسية
                    "surface": "#FFFFFF",           # خلفية الأسطح
                    "card": "#FFFFFF",              # خلفية البطاقات

                    # ألوان النصوص
                    "text_primary": "#212121",      # نص رئيسي
                    "text_secondary": "#757575",    # نص ثانوي
                    "text_on_primary": "#FFFFFF",   # نص على اللون الأساسي

                    # ألوان الحالة
                    "success": "#4CAF50",           # نجاح
                    "warning": "#FF9800",           # تحذير
                    "error": "#F44336",             # خطأ
                    "info": "#2196F3",              # معلومات

                    # ألوان الحدود والظلال
                    "border": "#E0E0E0",            # حدود
                    "shadow": "#00000020",          # ظل
                    "hover": "#F0F0F0",             # تمرير الماوس
                    "selected": "#E3F2FD",          # محدد

                    # ألوان الأزرار المختلفة
                    "btn_sales": "#4CAF50",         # زر المبيعات
                    "btn_purchase": "#2196F3",      # زر المشتريات
                    "btn_treasury": "#FF9800",      # زر الخزينة
                    "btn_inventory": "#9C27B0",     # زر المخزون
                    "btn_reports": "#607D8B",       # زر التقارير
                    "btn_customers": "#795548",     # زر العملاء
                    "btn_suppliers": "#3F51B5",     # زر الموردين
                    "btn_settings": "#757575"       # زر الإعدادات
                }
            },

            "dark": {
                "name": "الثيم الداكن",
                "colors": {
                    # الألوان الأساسية
                    "primary": "#4CAF50",           # أخضر البرنامج الرئيسي
                    "secondary": "#64B5F6",         # أزرق ثانوي
                    "background": "#121212",        # خلفية رئيسية
                    "surface": "#1E1E1E",           # خلفية الأسطح
                    "card": "#2D2D2D",              # خلفية البطاقات

                    # ألوان النصوص
                    "text_primary": "#FFFFFF",      # نص رئيسي
                    "text_secondary": "#B0B0B0",    # نص ثانوي
                    "text_on_primary": "#000000",   # نص على اللون الأساسي

                    # ألوان الحالة
                    "success": "#66BB6A",           # نجاح
                    "warning": "#FFB74D",           # تحذير
                    "error": "#EF5350",             # خطأ
                    "info": "#42A5F5",              # معلومات

                    # ألوان الحدود والظلال
                    "border": "#404040",            # حدود
                    "shadow": "#00000040",          # ظل
                    "hover": "#333333",             # تمرير الماوس
                    "selected": "#1565C0",          # محدد

                    # ألوان الأزرار المختلفة
                    "btn_sales": "#66BB6A",         # زر المبيعات
                    "btn_purchase": "#42A5F5",      # زر المشتريات
                    "btn_treasury": "#FFB74D",      # زر الخزينة
                    "btn_inventory": "#BA68C8",     # زر المخزون
                    "btn_reports": "#78909C",       # زر التقارير
                    "btn_customers": "#8D6E63",     # زر العملاء
                    "btn_suppliers": "#7986CB",     # زر الموردين
                    "btn_settings": "#9E9E9E"       # زر الإعدادات
                }
            }
        }

    def apply_theme(self, theme_name):
        """تطبيق الثيم"""
        if theme_name not in self.themes:
            theme_name = "light"

        self.current_theme = theme_name
        theme = self.themes[theme_name]

        # تطبيق الثيم على customtkinter
        if theme_name == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

        # تعيين الألوان المخصصة
        self.colors = theme["colors"]

        return True

    def get_color(self, color_name):
        """الحصول على لون معين"""
        return self.colors.get(color_name, "#000000")

    def get_button_colors(self, button_type):
        """الحصول على ألوان زر معين"""
        base_color = self.get_color(f"btn_{button_type}")

        return {
            "fg_color": base_color,
            "hover_color": self.adjust_color_brightness(base_color, -20),
            "text_color": self.get_color("text_on_primary"),
            "border_color": self.adjust_color_brightness(base_color, -30)
        }

    def adjust_color_brightness(self, hex_color, adjustment):
        """تعديل سطوع اللون"""
        # إزالة # إذا كانت موجودة
        hex_color = hex_color.lstrip('#')

        # تحويل إلى RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # تعديل السطوع
        adjusted_rgb = tuple(max(0, min(255, c + adjustment)) for c in rgb)

        # تحويل إلى hex
        return f"#{adjusted_rgb[0]:02x}{adjusted_rgb[1]:02x}{adjusted_rgb[2]:02x}"

    def get_font_config(self, size=12, weight="normal"):
        """الحصول على تكوين الخط"""
        return ("Cairo", size, weight)

    def get_rtl_config(self):
        """الحصول على تكوين RTL"""
        return {
            "justify": "right",
            "anchor": "e"
        }

    def create_styled_button(self, parent, text, command=None, button_type="primary", **kwargs):
        """إنشاء زر مع التنسيق المناسب"""
        colors = self.get_button_colors(button_type)
        font_config = self.get_font_config(size=kwargs.get('font_size', 12))

        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=colors["fg_color"],
            hover_color=colors["hover_color"],
            text_color=colors["text_color"],
            border_color=colors["border_color"],
            font=font_config,
            **{k: v for k, v in kwargs.items() if k not in ['font_size', 'button_type']}
        )

        return button

    def create_styled_frame(self, parent, **kwargs):
        """إنشاء إطار مع التنسيق المناسب"""
        return ctk.CTkFrame(
            parent,
            fg_color=self.get_color("surface"),
            border_color=self.get_color("border"),
            **kwargs
        )

    def create_styled_label(self, parent, text, **kwargs):
        """إنشاء تسمية مع التنسيق المناسب"""
        font_config = self.get_font_config(size=kwargs.get('font_size', 12))

        return ctk.CTkLabel(
            parent,
            text=text,
            text_color=self.get_color("text_primary"),
            font=font_config,
            **{k: v for k, v in kwargs.items() if k != 'font_size'}
        )

    def create_styled_entry(self, parent, **kwargs):
        """إنشاء حقل إدخال مع التنسيق المناسب"""
        font_config = self.get_font_config(size=kwargs.get('font_size', 12))

        return ctk.CTkEntry(
            parent,
            fg_color=self.get_color("surface"),
            border_color=self.get_color("border"),
            text_color=self.get_color("text_primary"),
            font=font_config,
            **{k: v for k, v in kwargs.items() if k != 'font_size'}
        )

    def toggle_theme(self):
        """تبديل الثيم"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        return self.apply_theme(new_theme)

    def get_current_theme_name(self):
        """الحصول على اسم الثيم الحالي"""
        return self.themes[self.current_theme]["name"]

    def get_available_themes(self):
        """الحصول على قائمة الثيمات المتاحة"""
        return [(name, theme["name"]) for name, theme in self.themes.items()]

    def get_arabic_font(self, size: int = 12, style: str = "regular", font_family: str = None):
        """الحصول على خط عربي مع حجم ونمط محددين"""
        return get_arabic_font(size, style, font_family)

    def get_font_set(self, base_font: str = None, base_size: int = 12):
        """الحصول على مجموعة خطوط بأحجام مختلفة"""
        if base_font is None:
            base_font = font_manager.get_default_font()

        return font_manager.create_font_set(base_font, base_size)

    def get_available_fonts(self):
        """الحصول على قائمة الخطوط المتاحة"""
        return font_manager.get_available_fonts()

    def is_font_available(self, font_family: str):
        """التحقق من توفر خط معين"""
        return font_manager.is_font_available(font_family)
