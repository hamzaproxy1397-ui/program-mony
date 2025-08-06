# -*- coding: utf-8 -*-
"""
الأقسام المتقدمة للوحة التحكم المركزية
تطوير مفصل وعميق لجميع الأقسام الـ11
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import json
import os
from pathlib import Path
from datetime import datetime
import sqlite3
from typing import Dict, Any, Optional

# استيراد الثيمات والإعدادات
from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS
from config.settings import PROJECT_ROOT, DATABASE_PATH

# ألوان دافئة وجذابة (بدون رمادي)
WARM_COLORS = {
    'coral': '#FF6B6B',           # مرجاني دافئ
    'sunset': '#FF8E53',          # برتقالي غروب
    'golden': '#FFD93D',          # ذهبي مشرق
    'mint': '#6BCF7F',            # نعناعي منعش
    'lavender': '#A8E6CF',        # لافندر هادئ
    'sky': '#4ECDC4',             # سماوي صافي
    'rose': '#FF8A95',            # وردي ناعم
    'peach': '#FFAAA5',           # خوخي فاتح
    'turquoise': '#45B7D1',       # تركوازي
    'violet': '#96CEB4',          # بنفسجي فاتح
    'cream': '#FFF8E1',           # كريمي دافئ
    'ivory': '#FFFEF7',           # عاجي
    'warm_white': '#FFFEF7',      # أبيض دافئ
    'soft_cream': '#FFF8E1',      # كريمي ناعم
    'light_peach': '#FFF5F5',     # خوخي فاتح جداً
    'mint_bg': '#F0FFF4',         # خلفية نعناعية
    'dark_coral': '#E55555',      # مرجاني داكن
    'warm_brown': '#8B4513',      # بني دافئ
    'deep_teal': '#2C5F5D',       # تيل عميق
    'rich_purple': '#6A4C93',     # بنفسجي غني
}

class AdvancedInvoicesSettings:
    """إعدادات الفواتير المتقدمة"""
    
    def __init__(self, parent_panel):
        self.parent = parent_panel
        self.invoice_templates = {}
        self.current_template = "حديث"
    
    def create_invoices_settings(self, scrollable_frame):
        """إنشاء إعدادات الفواتير المفصلة"""
        # رأس القسم
        self.create_section_header(
            scrollable_frame,
            "إعدادات الفواتير",
            "🧾",
            "تخصيص قوالب فواتير البيع والشراء و POS، إعدادات المرتجعات، تكوين التقارير",
            WARM_COLORS['golden']
        )
        
        # بطاقة قوالب الفواتير
        def invoice_templates_content(parent):
            # اختيار القالب
            template_frame = ctk.CTkFrame(parent, fg_color="transparent")
            template_frame.pack(fill="x", pady=10)
            
            template_label = ctk.CTkLabel(
                template_frame,
                text="اختر قالب الفاتورة:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            template_label.pack(anchor="e", pady=(0, 10))
            
            # قوالب الفواتير المتاحة
            templates = ["حديث", "كلاسيكي", "مبسط", "احترافي", "ملون", "مخصص"]
            
            template_dropdown = ctk.CTkComboBox(
                template_frame,
                values=templates,
                font=(FONTS['arabic'], 12),
                height=35,
                width=200,
                command=self.on_template_change
            )
            template_dropdown.pack(anchor="e", pady=(0, 10))
            template_dropdown.set(self.current_template)
            
            # معاينة القالب
            preview_btn = ctk.CTkButton(
                template_frame,
                text="👁️ معاينة القالب",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['turquoise'],
                hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                height=35,
                command=self.preview_template
            )
            preview_btn.pack(anchor="e", pady=5)
            
            # تخصيص القالب
            customize_btn = ctk.CTkButton(
                template_frame,
                text="🎨 تخصيص القالب",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['violet'],
                hover_color=self.lighten_color(WARM_COLORS['violet']),
                height=35,
                command=self.customize_template
            )
            customize_btn.pack(anchor="e", pady=5)
        
        self.create_settings_card(scrollable_frame, "📄 قوالب الفواتير", invoice_templates_content, WARM_COLORS['light_peach'])
        
        # بطاقة إعدادات الطباعة
        def print_settings_content(parent):
            # حجم الورق
            self.create_dropdown_field(parent, "حجم الورق:", "paper_size",
                                     ["A4", "A5", "Letter", "Legal", "A3"], "A4")
            
            # اتجاه الطباعة
            self.create_dropdown_field(parent, "اتجاه الطباعة:", "print_orientation",
                                     ["عمودي", "أفقي"], "عمودي")
            
            # جودة الطباعة
            self.create_dropdown_field(parent, "جودة الطباعة:", "print_quality",
                                     ["مسودة", "عادية", "عالية", "فائقة"], "عالية")
            
            # الهوامش
            self.create_input_field(parent, "الهامش العلوي (مم):", "margin_top", "20")
            self.create_input_field(parent, "الهامش السفلي (مم):", "margin_bottom", "20")
            self.create_input_field(parent, "الهامش الأيمن (مم):", "margin_right", "15")
            self.create_input_field(parent, "الهامش الأيسر (مم):", "margin_left", "15")
            
            # خيارات الطباعة
            self.create_switch_field(parent, "طباعة الشعار:", "print_logo", True)
            self.create_switch_field(parent, "طباعة الخلفية:", "print_background", False)
            self.create_switch_field(parent, "طباعة ملونة:", "color_print", True)
            self.create_switch_field(parent, "طباعة تلقائية:", "auto_print", False)
            self.create_switch_field(parent, "حفظ PDF تلقائياً:", "auto_save_pdf", True)
        
        self.create_settings_card(scrollable_frame, "🖨️ إعدادات الطباعة", print_settings_content, WARM_COLORS['mint_bg'])
        
        # بطاقة إعدادات الضرائب والخصومات
        def tax_discount_content(parent):
            # الضريبة الافتراضية
            self.create_input_field(parent, "معدل الضريبة الافتراضي (%):", "default_tax_rate", "15")
            
            # ضرائب إضافية
            self.create_input_field(parent, "ضريبة إضافية 1 (%):", "additional_tax_1", "0")
            self.create_input_field(parent, "اسم الضريبة الإضافية 1:", "additional_tax_1_name", "")
            
            self.create_input_field(parent, "ضريبة إضافية 2 (%):", "additional_tax_2", "0")
            self.create_input_field(parent, "اسم الضريبة الإضافية 2:", "additional_tax_2_name", "")
            
            # الخصومات
            self.create_input_field(parent, "الحد الأقصى للخصم (%):", "max_discount_percent", "50")
            self.create_input_field(parent, "خصم الكمية الافتراضي (%):", "quantity_discount", "5")
            self.create_input_field(parent, "خصم العميل المميز (%):", "vip_discount", "10")
            
            # إعدادات التقريب
            self.create_dropdown_field(parent, "تقريب المبلغ الإجمالي:", "amount_rounding",
                                     ["بدون تقريب", "أقرب 0.05", "أقرب 0.25", "أقرب 0.50", "أقرب 1.00"], "أقرب 0.05")
            
            # خيارات الضرائب
            self.create_switch_field(parent, "تضمين الضريبة في السعر:", "tax_inclusive", True)
            self.create_switch_field(parent, "عرض تفاصيل الضريبة:", "show_tax_details", True)
            self.create_switch_field(parent, "حساب ضريبة مركبة:", "compound_tax", False)
        
        self.create_settings_card(scrollable_frame, "💰 الضرائب والخصومات", tax_discount_content, WARM_COLORS['soft_cream'])
        
        # بطاقة إعدادات POS
        def pos_settings_content(parent):
            # إعدادات الشاشة
            self.create_dropdown_field(parent, "حجم شاشة POS:", "pos_screen_size",
                                     ["صغير (1024x768)", "متوسط (1366x768)", "كبير (1920x1080)", "ملء الشاشة"], "متوسط (1366x768)")
            
            # إعدادات الدفع
            self.create_switch_field(parent, "قبول الدفع النقدي:", "accept_cash", True)
            self.create_switch_field(parent, "قبول البطاقات:", "accept_cards", True)
            self.create_switch_field(parent, "قبول الدفع الإلكتروني:", "accept_digital", True)
            self.create_switch_field(parent, "قبول الدفع الآجل:", "accept_credit", False)
            
            # إعدادات الطابعة
            self.create_dropdown_field(parent, "نوع طابعة الإيصالات:", "receipt_printer_type",
                                     ["حرارية 58مم", "حرارية 80مم", "عادية A4", "بدون طابعة"], "حرارية 80مم")
            
            self.create_switch_field(parent, "طباعة إيصال العميل:", "print_customer_receipt", True)
            self.create_switch_field(parent, "طباعة نسخة المحل:", "print_store_copy", True)
            
            # إعدادات الباركود
            self.create_switch_field(parent, "قارئ الباركود:", "barcode_scanner", True)
            self.create_dropdown_field(parent, "نوع قارئ الباركود:", "barcode_scanner_type",
                                     ["USB", "Bluetooth", "WiFi", "مدمج"], "USB")
            
            # إعدادات الدرج النقدي
            self.create_switch_field(parent, "درج نقدي:", "cash_drawer", True)
            self.create_switch_field(parent, "فتح الدرج تلقائياً:", "auto_open_drawer", True)
        
        self.create_settings_card(scrollable_frame, "🏪 إعدادات نقاط البيع (POS)", pos_settings_content, WARM_COLORS['light_peach'])
    
    def create_section_header(self, parent, title, icon, description, color):
        """إنشاء رأس القسم"""
        header_frame = ctk.CTkFrame(
            parent,
            height=100,
            fg_color=color,
            corner_radius=15
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # الأيقونة
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=("Segoe UI Emoji", 36),
            text_color="white"
        )
        icon_label.pack(side="right", padx=30, pady=20)
        
        # النص
        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            font=(FONTS['arabic'], 24, "bold"),
            text_color="white",
            anchor="e"
        )
        title_label.pack(anchor="e", pady=(15, 5))
        
        desc_label = ctk.CTkLabel(
            text_frame,
            text=description,
            font=(FONTS['arabic'], 14),
            text_color=WARM_COLORS['cream'],
            anchor="e"
        )
        desc_label.pack(anchor="e")
    
    def create_settings_card(self, parent, title, content_func, color=None):
        """إنشاء بطاقة إعدادات"""
        if color is None:
            color = WARM_COLORS['light_peach']
            
        card_frame = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=12
        )
        card_frame.pack(fill="x", pady=10)
        
        # عنوان البطاقة
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=(FONTS['arabic'], 16, "bold"),
            text_color=WARM_COLORS['dark_coral'],
            anchor="e"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # محتوى البطاقة
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # استدعاء دالة المحتوى
        content_func(content_frame)
        
        return card_frame
    
    def create_input_field(self, parent, label, key, default_value=""):
        """إنشاء حقل إدخال نص"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)
        
        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))
        
        # حقل الإدخال
        entry = ctk.CTkEntry(
            field_frame,
            font=(FONTS['arabic'], 12),
            height=35,
            fg_color="white",
            border_color=WARM_COLORS['coral'],
            border_width=2
        )
        entry.pack(side="right", fill="x", expand=True)
        entry.insert(0, default_value)
        
        return entry
    
    def create_dropdown_field(self, parent, label, key, options, default_value=""):
        """إنشاء حقل قائمة منسدلة"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)
        
        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))
        
        # القائمة المنسدلة
        dropdown = ctk.CTkComboBox(
            field_frame,
            values=options,
            font=(FONTS['arabic'], 12),
            height=35,
            fg_color="white",
            border_color=WARM_COLORS['coral'],
            border_width=2,
            button_color=WARM_COLORS['coral'],
            button_hover_color=self.lighten_color(WARM_COLORS['coral'])
        )
        dropdown.pack(side="right", fill="x", expand=True)
        dropdown.set(default_value if default_value else options[0])
        
        return dropdown
    
    def create_switch_field(self, parent, label, key, default_value=False):
        """إنشاء حقل مفتاح تشغيل/إيقاف"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)
        
        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))
        
        # المفتاح
        switch = ctk.CTkSwitch(
            field_frame,
            text="",
            font=(FONTS['arabic'], 12),
            progress_color=WARM_COLORS['mint'],
            button_color=WARM_COLORS['coral'],
            button_hover_color=self.lighten_color(WARM_COLORS['coral'])
        )
        switch.pack(side="right")
        
        # تعيين القيمة الافتراضية
        if default_value:
            switch.select()
        else:
            switch.deselect()
        
        return switch
    
    def lighten_color(self, color):
        """تفتيح اللون للتأثير عند التمرير"""
        if color.startswith('#'):
            hex_color = color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        return color
    
    def on_template_change(self, template_name):
        """عند تغيير القالب"""
        self.current_template = template_name
        print(f"تم تغيير القالب إلى: {template_name}")
    
    def preview_template(self):
        """معاينة القالب"""
        messagebox.showinfo("معاينة القالب", f"سيتم عرض معاينة للقالب: {self.current_template}")
    
    def customize_template(self):
        """تخصيص القالب"""
        messagebox.showinfo("تخصيص القالب", f"سيتم فتح محرر تخصيص القالب: {self.current_template}")


class AdvancedPayrollSettings:
    """إعدادات الرواتب والضرائب المتقدمة"""

    def __init__(self, parent_panel):
        self.parent = parent_panel
        self.salary_scales = {}
        self.tax_brackets = []

    def create_payroll_settings(self, scrollable_frame):
        """إنشاء إعدادات الرواتب والضرائب المفصلة"""
        # رأس القسم
        self.create_section_header(
            scrollable_frame,
            "الرواتب والضرائب",
            "💰",
            "حاسبة الرواتب، إعدادات الضرائب والخصومات، نظام الإضافي والمكافآت",
            WARM_COLORS['mint']
        )

        # بطاقة سلالم الرواتب
        def salary_scales_content(parent):
            # إضافة سلم راتب جديد
            add_scale_btn = ctk.CTkButton(
                parent,
                text="➕ إضافة سلم راتب جديد",
                font=(FONTS['arabic'], 14, "bold"),
                fg_color=WARM_COLORS['mint'],
                hover_color=self.lighten_color(WARM_COLORS['mint']),
                height=40,
                command=self.add_salary_scale
            )
            add_scale_btn.pack(pady=10)

            # سلالم الرواتب الحالية
            scales_frame = ctk.CTkFrame(parent, fg_color="transparent")
            scales_frame.pack(fill="x", pady=10)

            scales_title = ctk.CTkLabel(
                scales_frame,
                text="💼 سلالم الرواتب الحالية:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            scales_title.pack(anchor="e", pady=(0, 10))

            # أمثلة على سلالم الرواتب
            sample_scales = [
                {"name": "الإدارة العليا", "min_salary": 15000, "max_salary": 50000, "levels": 10},
                {"name": "المحاسبة", "min_salary": 8000, "max_salary": 25000, "levels": 8},
                {"name": "المبيعات", "min_salary": 5000, "max_salary": 15000, "levels": 6},
                {"name": "الخدمات", "min_salary": 3000, "max_salary": 8000, "levels": 5}
            ]

            for scale in sample_scales:
                scale_card = ctk.CTkFrame(scales_frame, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
                scale_card.pack(fill="x", pady=5)

                scale_info = ctk.CTkLabel(
                    scale_card,
                    text=f"📊 {scale['name']} - من {scale['min_salary']:,} إلى {scale['max_salary']:,} ر.س ({scale['levels']} مستويات)",
                    font=(FONTS['arabic'], 12),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                scale_info.pack(side="right", padx=15, pady=10)

                # أزرار الإجراءات
                actions_frame = ctk.CTkFrame(scale_card, fg_color="transparent")
                actions_frame.pack(side="left", padx=15, pady=5)

                edit_btn = ctk.CTkButton(
                    actions_frame,
                    text="✏️ تعديل",
                    width=80,
                    height=30,
                    fg_color=WARM_COLORS['golden'],
                    hover_color=self.lighten_color(WARM_COLORS['golden']),
                    command=lambda s=scale: self.edit_salary_scale(s)
                )
                edit_btn.pack(side="left", padx=2)

        self.create_settings_card(scrollable_frame, "📊 سلالم الرواتب", salary_scales_content, WARM_COLORS['light_peach'])

        # بطاقة حاسبة الرواتب
        def salary_calculator_content(parent):
            # الراتب الأساسي
            self.create_input_field(parent, "الراتب الأساسي:", "basic_salary", "5000")

            # البدلات
            self.create_input_field(parent, "بدل السكن:", "housing_allowance", "1000")
            self.create_input_field(parent, "بدل المواصلات:", "transport_allowance", "500")
            self.create_input_field(parent, "بدل الطعام:", "food_allowance", "300")
            self.create_input_field(parent, "بدلات أخرى:", "other_allowances", "0")

            # الإضافي والمكافآت
            self.create_input_field(parent, "ساعات الإضافي:", "overtime_hours", "0")
            self.create_input_field(parent, "معدل ساعة الإضافي:", "overtime_rate", "25")
            self.create_input_field(parent, "مكافآت الأداء:", "performance_bonus", "0")
            self.create_input_field(parent, "مكافآت أخرى:", "other_bonus", "0")

            # الخصومات
            self.create_input_field(parent, "التأمينات الاجتماعية (%):", "social_insurance", "9")
            self.create_input_field(parent, "ضريبة الدخل (%):", "income_tax", "0")
            self.create_input_field(parent, "خصومات أخرى:", "other_deductions", "0")

            # زر الحساب
            calculate_btn = ctk.CTkButton(
                parent,
                text="🧮 حساب صافي الراتب",
                font=(FONTS['arabic'], 14, "bold"),
                fg_color=WARM_COLORS['turquoise'],
                hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                height=40,
                command=self.calculate_salary
            )
            calculate_btn.pack(pady=15)

            # عرض النتيجة
            self.result_label = ctk.CTkLabel(
                parent,
                text="💰 صافي الراتب: سيظهر بعد الحساب",
                font=(FONTS['arabic'], 16, "bold"),
                text_color=WARM_COLORS['mint']
            )
            self.result_label.pack(pady=10)

        self.create_settings_card(scrollable_frame, "🧮 حاسبة الرواتب", salary_calculator_content, WARM_COLORS['mint_bg'])

        # بطاقة إعدادات الضرائب
        def tax_settings_content(parent):
            # شرائح ضريبة الدخل
            tax_title = ctk.CTkLabel(
                parent,
                text="📊 شرائح ضريبة الدخل:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            tax_title.pack(anchor="e", pady=(0, 10))

            # شرائح الضريبة (مثال للسعودية)
            tax_brackets = [
                {"from": 0, "to": 30000, "rate": 0, "description": "معفى من الضريبة"},
                {"from": 30001, "to": 100000, "rate": 5, "description": "5% على الدخل الزائد"},
                {"from": 100001, "to": 300000, "rate": 10, "description": "10% على الدخل الزائد"},
                {"from": 300001, "to": 500000, "rate": 15, "description": "15% على الدخل الزائد"},
                {"from": 500001, "to": 1000000, "rate": 20, "description": "20% على الدخل الزائد"}
            ]

            for bracket in tax_brackets:
                bracket_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['soft_cream'], corner_radius=8)
                bracket_frame.pack(fill="x", pady=3)

                bracket_text = f"من {bracket['from']:,} إلى {bracket['to']:,} ر.س - {bracket['rate']}% ({bracket['description']})"
                bracket_label = ctk.CTkLabel(
                    bracket_frame,
                    text=bracket_text,
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                bracket_label.pack(padx=15, pady=8, anchor="e")

            # إعدادات ضريبية أخرى
            self.create_switch_field(parent, "تطبيق ضريبة الدخل:", "apply_income_tax", False)
            self.create_switch_field(parent, "ضريبة تصاعدية:", "progressive_tax", True)
            self.create_input_field(parent, "الحد الأدنى المعفى:", "tax_exemption_limit", "30000")

        self.create_settings_card(scrollable_frame, "📊 إعدادات الضرائب", tax_settings_content, WARM_COLORS['soft_cream'])

        # بطاقة إعدادات الإضافي
        def overtime_settings_content(parent):
            # أنواع الإضافي
            self.create_dropdown_field(parent, "نوع حساب الإضافي:", "overtime_calculation",
                                     ["ساعي", "يومي", "شهري", "مخصص"], "ساعي")

            # معدلات الإضافي
            self.create_input_field(parent, "معدل الإضافي العادي (%):", "normal_overtime_rate", "150")
            self.create_input_field(parent, "معدل إضافي العطل (%):", "holiday_overtime_rate", "200")
            self.create_input_field(parent, "معدل الإضافي الليلي (%):", "night_overtime_rate", "175")

            # حدود الإضافي
            self.create_input_field(parent, "الحد الأقصى للإضافي اليومي (ساعة):", "max_daily_overtime", "4")
            self.create_input_field(parent, "الحد الأقصى للإضافي الشهري (ساعة):", "max_monthly_overtime", "60")

            # إعدادات الإضافي
            self.create_switch_field(parent, "حساب الإضافي تلقائياً:", "auto_calculate_overtime", True)
            self.create_switch_field(parent, "تطبيق حد أقصى للإضافي:", "apply_overtime_limit", True)
            self.create_switch_field(parent, "إضافي العطل الرسمية:", "holiday_overtime", True)

        self.create_settings_card(scrollable_frame, "⏰ إعدادات الإضافي", overtime_settings_content, WARM_COLORS['light_peach'])

    def add_salary_scale(self):
        """إضافة سلم راتب جديد"""
        messagebox.showinfo("إضافة سلم راتب", "سيتم فتح نافذة إضافة سلم راتب جديد")

    def edit_salary_scale(self, scale):
        """تعديل سلم راتب"""
        messagebox.showinfo("تعديل سلم الراتب", f"سيتم فتح نافذة تعديل سلم الراتب: {scale['name']}")

    def calculate_salary(self):
        """حساب صافي الراتب"""
        # هذه دالة مبسطة للحساب - يمكن تطويرها أكثر
        basic_salary = 5000  # يجب أخذها من الحقل الفعلي
        allowances = 1800    # مجموع البدلات
        overtime = 0         # الإضافي
        deductions = basic_salary * 0.09  # التأمينات

        net_salary = basic_salary + allowances + overtime - deductions

        self.result_label.configure(text=f"💰 صافي الراتب: {net_salary:,.2f} ر.س")

    # نفس الدوال المساعدة من الكلاس السابق
    def create_section_header(self, parent, title, icon, description, color):
        """إنشاء رأس القسم"""
        header_frame = ctk.CTkFrame(parent, height=100, fg_color=color, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        icon_label = ctk.CTkLabel(header_frame, text=icon, font=("Segoe UI Emoji", 36), text_color="white")
        icon_label.pack(side="right", padx=30, pady=20)

        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        title_label = ctk.CTkLabel(text_frame, text=title, font=(FONTS['arabic'], 24, "bold"), text_color="white", anchor="e")
        title_label.pack(anchor="e", pady=(15, 5))

        desc_label = ctk.CTkLabel(text_frame, text=description, font=(FONTS['arabic'], 14), text_color=WARM_COLORS['cream'], anchor="e")
        desc_label.pack(anchor="e")

    def create_settings_card(self, parent, title, content_func, color=None):
        """إنشاء بطاقة إعدادات"""
        if color is None:
            color = WARM_COLORS['light_peach']

        card_frame = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
        card_frame.pack(fill="x", pady=10)

        title_label = ctk.CTkLabel(card_frame, text=title, font=(FONTS['arabic'], 16, "bold"), text_color=WARM_COLORS['dark_coral'], anchor="e")
        title_label.pack(anchor="e", padx=20, pady=(15, 10))

        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 15))

        content_func(content_frame)
        return card_frame

    def create_input_field(self, parent, label, key, default_value=""):
        """إنشاء حقل إدخال نص"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        label_widget = ctk.CTkLabel(field_frame, text=label, font=(FONTS['arabic'], 12, "bold"), text_color=WARM_COLORS['deep_teal'], anchor="e", width=150)
        label_widget.pack(side="right", padx=(0, 10))

        entry = ctk.CTkEntry(field_frame, font=(FONTS['arabic'], 12), height=35, fg_color="white", border_color=WARM_COLORS['coral'], border_width=2)
        entry.pack(side="right", fill="x", expand=True)
        entry.insert(0, default_value)

        return entry

    def create_dropdown_field(self, parent, label, key, options, default_value=""):
        """إنشاء حقل قائمة منسدلة"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        label_widget = ctk.CTkLabel(field_frame, text=label, font=(FONTS['arabic'], 12, "bold"), text_color=WARM_COLORS['deep_teal'], anchor="e", width=150)
        label_widget.pack(side="right", padx=(0, 10))

        dropdown = ctk.CTkComboBox(field_frame, values=options, font=(FONTS['arabic'], 12), height=35, fg_color="white", border_color=WARM_COLORS['coral'], border_width=2, button_color=WARM_COLORS['coral'], button_hover_color=self.lighten_color(WARM_COLORS['coral']))
        dropdown.pack(side="right", fill="x", expand=True)
        dropdown.set(default_value if default_value else options[0])

        return dropdown

    def create_switch_field(self, parent, label, key, default_value=False):
        """إنشاء حقل مفتاح تشغيل/إيقاف"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        label_widget = ctk.CTkLabel(field_frame, text=label, font=(FONTS['arabic'], 12, "bold"), text_color=WARM_COLORS['deep_teal'], anchor="e", width=150)
        label_widget.pack(side="right", padx=(0, 10))

        switch = ctk.CTkSwitch(field_frame, text="", font=(FONTS['arabic'], 12), progress_color=WARM_COLORS['mint'], button_color=WARM_COLORS['coral'], button_hover_color=self.lighten_color(WARM_COLORS['coral']))
        switch.pack(side="right")

        if default_value:
            switch.select()
        else:
            switch.deselect()

        return switch

    def lighten_color(self, color):
        """تفتيح اللون للتأثير عند التمرير"""
        if color.startswith('#'):
            hex_color = color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        return color


class AdvancedWarehouseSettings:
    """إعدادات المخازن المتقدمة"""

    def __init__(self, parent_panel):
        self.parent = parent_panel
        self.warehouses = {}
        self.stock_movements = []

    def create_warehouse_settings(self, scrollable_frame):
        """إنشاء إعدادات المخازن المفصلة"""
        # رأس القسم
        self.create_section_header(
            scrollable_frame,
            "إعدادات المخازن",
            "🏪",
            "إدارة أذون الصرف والإضافة والتحويل، نظام الجرد، تكامل الباركود، تحديد حدود الطلب",
            WARM_COLORS['sky']
        )

        # بطاقة إدارة المخازن
        def warehouses_management_content(parent):
            # زر إضافة مخزن جديد
            add_warehouse_btn = ctk.CTkButton(
                parent,
                text="🏪 إضافة مخزن جديد",
                font=(FONTS['arabic'], 14, "bold"),
                fg_color=WARM_COLORS['sky'],
                hover_color=self.lighten_color(WARM_COLORS['sky']),
                height=40,
                command=self.add_warehouse
            )
            add_warehouse_btn.pack(pady=10)

            # المخازن الحالية
            warehouses_frame = ctk.CTkFrame(parent, fg_color="transparent")
            warehouses_frame.pack(fill="x", pady=10)

            warehouses_title = ctk.CTkLabel(
                warehouses_frame,
                text="🏪 المخازن الحالية:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            warehouses_title.pack(anchor="e", pady=(0, 10))

            # أمثلة على المخازن
            sample_warehouses = [
                {"name": "المخزن الرئيسي", "code": "WH001", "location": "الرياض", "capacity": "1000 متر مكعب", "status": "نشط"},
                {"name": "مخزن الفرع الشمالي", "code": "WH002", "location": "الدمام", "capacity": "500 متر مكعب", "status": "نشط"},
                {"name": "مخزن المواد الخام", "code": "WH003", "location": "جدة", "capacity": "750 متر مكعب", "status": "صيانة"}
            ]

            for warehouse in sample_warehouses:
                warehouse_card = ctk.CTkFrame(warehouses_frame, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
                warehouse_card.pack(fill="x", pady=5)

                warehouse_info = ctk.CTkLabel(
                    warehouse_card,
                    text=f"🏪 {warehouse['name']} ({warehouse['code']}) - {warehouse['location']} - {warehouse['capacity']} - {warehouse['status']}",
                    font=(FONTS['arabic'], 12),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                warehouse_info.pack(side="right", padx=15, pady=10)

                # أزرار الإجراءات
                actions_frame = ctk.CTkFrame(warehouse_card, fg_color="transparent")
                actions_frame.pack(side="left", padx=15, pady=5)

                edit_btn = ctk.CTkButton(
                    actions_frame,
                    text="✏️ تعديل",
                    width=80,
                    height=30,
                    fg_color=WARM_COLORS['golden'],
                    hover_color=self.lighten_color(WARM_COLORS['golden']),
                    command=lambda w=warehouse: self.edit_warehouse(w)
                )
                edit_btn.pack(side="left", padx=2)

                inventory_btn = ctk.CTkButton(
                    actions_frame,
                    text="📦 الجرد",
                    width=80,
                    height=30,
                    fg_color=WARM_COLORS['turquoise'],
                    hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                    command=lambda w=warehouse: self.view_inventory(w)
                )
                inventory_btn.pack(side="left", padx=2)

        self.create_settings_card(scrollable_frame, "🏪 إدارة المخازن", warehouses_management_content, WARM_COLORS['light_peach'])

        # بطاقة أذون الحركة
        def movement_permits_content(parent):
            # أنواع الأذون
            permits_title = ctk.CTkLabel(
                parent,
                text="📋 أنواع أذون الحركة:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            permits_title.pack(anchor="e", pady=(0, 10))

            # أذون الصرف
            issue_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['mint_bg'], corner_radius=8)
            issue_frame.pack(fill="x", pady=5)

            issue_title = ctk.CTkLabel(
                issue_frame,
                text="📤 أذون الصرف",
                font=(FONTS['arabic'], 12, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            issue_title.pack(anchor="e", padx=15, pady=(10, 5))

            issue_settings = [
                "✅ تطلب موافقة المدير", "✅ فحص الكمية المتاحة", "✅ تحديث المخزون تلقائياً",
                "✅ طباعة الإذن", "✅ إشعار المخزن المستلم"
            ]

            for setting in issue_settings:
                setting_label = ctk.CTkLabel(
                    issue_frame,
                    text=setting,
                    font=(FONTS['arabic'], 10),
                    text_color=WARM_COLORS['mint'],
                    anchor="e"
                )
                setting_label.pack(anchor="e", padx=25, pady=1)

            ctk.CTkLabel(issue_frame, text="", height=5).pack()

            # أذون الإضافة
            receive_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['soft_cream'], corner_radius=8)
            receive_frame.pack(fill="x", pady=5)

            receive_title = ctk.CTkLabel(
                receive_frame,
                text="📥 أذون الإضافة",
                font=(FONTS['arabic'], 12, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            receive_title.pack(anchor="e", padx=15, pady=(10, 5))

            receive_settings = [
                "✅ فحص جودة البضاعة", "✅ تسجيل تاريخ الانتهاء", "✅ تحديث المخزون تلقائياً",
                "✅ طباعة ملصقات الباركود", "✅ إشعار قسم المشتريات"
            ]

            for setting in receive_settings:
                setting_label = ctk.CTkLabel(
                    receive_frame,
                    text=setting,
                    font=(FONTS['arabic'], 10),
                    text_color=WARM_COLORS['turquoise'],
                    anchor="e"
                )
                setting_label.pack(anchor="e", padx=25, pady=1)

            ctk.CTkLabel(receive_frame, text="", height=5).pack()

            # أذون التحويل
            transfer_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
            transfer_frame.pack(fill="x", pady=5)

            transfer_title = ctk.CTkLabel(
                transfer_frame,
                text="🔄 أذون التحويل",
                font=(FONTS['arabic'], 12, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            transfer_title.pack(anchor="e", padx=15, pady=(10, 5))

            transfer_settings = [
                "✅ تأكيد الاستلام", "✅ تتبع الشحنة", "✅ تحديث المخزونين",
                "✅ حساب تكلفة النقل", "✅ تقرير التحويل"
            ]

            for setting in transfer_settings:
                setting_label = ctk.CTkLabel(
                    transfer_frame,
                    text=setting,
                    font=(FONTS['arabic'], 10),
                    text_color=WARM_COLORS['violet'],
                    anchor="e"
                )
                setting_label.pack(anchor="e", padx=25, pady=1)

            ctk.CTkLabel(transfer_frame, text="", height=5).pack()

        self.create_settings_card(scrollable_frame, "📋 أذون الحركة", movement_permits_content, WARM_COLORS['mint_bg'])

        # بطاقة نظام الجرد
        def inventory_system_content(parent):
            # أنواع الجرد
            self.create_dropdown_field(parent, "نوع الجرد:", "inventory_type",
                                     ["جرد دوري", "جرد مستمر", "جرد عشوائي", "جرد سنوي"], "جرد دوري")

            # تكرار الجرد
            self.create_dropdown_field(parent, "تكرار الجرد:", "inventory_frequency",
                                     ["شهري", "ربع سنوي", "نصف سنوي", "سنوي"], "ربع سنوي")

            # طريقة التقييم
            self.create_dropdown_field(parent, "طريقة تقييم المخزون:", "valuation_method",
                                     ["FIFO", "LIFO", "متوسط مرجح", "التكلفة المحددة"], "FIFO")

            # حدود التنبيه
            self.create_input_field(parent, "الحد الأدنى للمخزون:", "min_stock_level", "10")
            self.create_input_field(parent, "الحد الأقصى للمخزون:", "max_stock_level", "1000")
            self.create_input_field(parent, "نقطة إعادة الطلب:", "reorder_point", "50")
            self.create_input_field(parent, "كمية إعادة الطلب:", "reorder_quantity", "100")

            # إعدادات التنبيهات
            self.create_switch_field(parent, "تنبيه نفاد المخزون:", "low_stock_alert", True)
            self.create_switch_field(parent, "تنبيه انتهاء الصلاحية:", "expiry_alert", True)
            self.create_switch_field(parent, "تنبيه المخزون الزائد:", "overstock_alert", False)
            self.create_switch_field(parent, "تقرير الجرد التلقائي:", "auto_inventory_report", True)

            # زر بدء الجرد
            inventory_btn = ctk.CTkButton(
                parent,
                text="📊 بدء عملية الجرد",
                font=(FONTS['arabic'], 14, "bold"),
                fg_color=WARM_COLORS['turquoise'],
                hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                height=40,
                command=self.start_inventory
            )
            inventory_btn.pack(pady=15)

        self.create_settings_card(scrollable_frame, "📊 نظام الجرد", inventory_system_content, WARM_COLORS['soft_cream'])

        # بطاقة تكامل الباركود
        def barcode_integration_content(parent):
            # إعدادات الباركود
            self.create_dropdown_field(parent, "نوع الباركود:", "barcode_type",
                                     ["Code 128", "Code 39", "EAN-13", "QR Code"], "Code 128")

            self.create_dropdown_field(parent, "حجم الباركود:", "barcode_size",
                                     ["صغير", "متوسط", "كبير"], "متوسط")

            # قارئ الباركود
            self.create_dropdown_field(parent, "نوع قارئ الباركود:", "scanner_type",
                                     ["USB", "Bluetooth", "WiFi", "مدمج في الكاميرا"], "USB")

            # إعدادات الطباعة
            self.create_dropdown_field(parent, "طابعة الملصقات:", "label_printer",
                                     ["حرارية", "نافثة حبر", "ليزر", "بدون طابعة"], "حرارية")

            self.create_input_field(parent, "عرض الملصق (مم):", "label_width", "40")
            self.create_input_field(parent, "ارتفاع الملصق (مم):", "label_height", "20")

            # خيارات الباركود
            self.create_switch_field(parent, "تفعيل قارئ الباركود:", "enable_barcode_scanner", True)
            self.create_switch_field(parent, "طباعة الباركود تلقائياً:", "auto_print_barcode", True)
            self.create_switch_field(parent, "تضمين اسم المنتج:", "include_product_name", True)
            self.create_switch_field(parent, "تضمين السعر:", "include_price", False)

            # أزرار الإجراءات
            buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=10)

            test_scanner_btn = ctk.CTkButton(
                buttons_frame,
                text="🔍 اختبار القارئ",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['mint'],
                hover_color=self.lighten_color(WARM_COLORS['mint']),
                height=35,
                command=self.test_barcode_scanner
            )
            test_scanner_btn.pack(side="right", padx=5)

            print_test_btn = ctk.CTkButton(
                buttons_frame,
                text="🖨️ طباعة تجريبية",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['golden'],
                hover_color=self.lighten_color(WARM_COLORS['golden']),
                height=35,
                command=self.print_test_barcode
            )
            print_test_btn.pack(side="right", padx=5)

        self.create_settings_card(scrollable_frame, "📱 تكامل الباركود", barcode_integration_content, WARM_COLORS['light_peach'])

    def add_warehouse(self):
        """إضافة مخزن جديد"""
        messagebox.showinfo("إضافة مخزن", "سيتم فتح نافذة إضافة مخزن جديد")

    def edit_warehouse(self, warehouse):
        """تعديل مخزن"""
        messagebox.showinfo("تعديل المخزن", f"سيتم فتح نافذة تعديل المخزن: {warehouse['name']}")

    def view_inventory(self, warehouse):
        """عرض جرد المخزن"""
        messagebox.showinfo("جرد المخزن", f"سيتم عرض جرد المخزن: {warehouse['name']}")

    def start_inventory(self):
        """بدء عملية الجرد"""
        messagebox.showinfo("بدء الجرد", "سيتم بدء عملية الجرد الشاملة")

    def test_barcode_scanner(self):
        """اختبار قارئ الباركود"""
        messagebox.showinfo("اختبار القارئ", "سيتم اختبار قارئ الباركود")

    def print_test_barcode(self):
        """طباعة باركود تجريبي"""
        messagebox.showinfo("طباعة تجريبية", "سيتم طباعة باركود تجريبي")

    # نفس الدوال المساعدة
    def create_section_header(self, parent, title, icon, description, color):
        """إنشاء رأس القسم"""
        header_frame = ctk.CTkFrame(parent, height=100, fg_color=color, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        icon_label = ctk.CTkLabel(header_frame, text=icon, font=("Segoe UI Emoji", 36), text_color="white")
        icon_label.pack(side="right", padx=30, pady=20)

        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        title_label = ctk.CTkLabel(text_frame, text=title, font=(FONTS['arabic'], 24, "bold"), text_color="white", anchor="e")
        title_label.pack(anchor="e", pady=(15, 5))

        desc_label = ctk.CTkLabel(text_frame, text=description, font=(FONTS['arabic'], 14), text_color=WARM_COLORS['cream'], anchor="e")
        desc_label.pack(anchor="e")

    def create_settings_card(self, parent, title, content_func, color=None):
        """إنشاء بطاقة إعدادات"""
        if color is None:
            color = WARM_COLORS['light_peach']

        card_frame = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
        card_frame.pack(fill="x", pady=10)

        title_label = ctk.CTkLabel(card_frame, text=title, font=(FONTS['arabic'], 16, "bold"), text_color=WARM_COLORS['dark_coral'], anchor="e")
        title_label.pack(anchor="e", padx=20, pady=(15, 10))

        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 15))

        content_func(content_frame)
        return card_frame

    def create_input_field(self, parent, label, key, default_value=""):
        """إنشاء حقل إدخال نص"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        label_widget = ctk.CTkLabel(field_frame, text=label, font=(FONTS['arabic'], 12, "bold"), text_color=WARM_COLORS['deep_teal'], anchor="e", width=150)
        label_widget.pack(side="right", padx=(0, 10))

        entry = ctk.CTkEntry(field_frame, font=(FONTS['arabic'], 12), height=35, fg_color="white", border_color=WARM_COLORS['coral'], border_width=2)
        entry.pack(side="right", fill="x", expand=True)
        entry.insert(0, default_value)

        return entry

    def create_dropdown_field(self, parent, label, key, options, default_value=""):
        """إنشاء حقل قائمة منسدلة"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        label_widget = ctk.CTkLabel(field_frame, text=label, font=(FONTS['arabic'], 12, "bold"), text_color=WARM_COLORS['deep_teal'], anchor="e", width=150)
        label_widget.pack(side="right", padx=(0, 10))

        dropdown = ctk.CTkComboBox(field_frame, values=options, font=(FONTS['arabic'], 12), height=35, fg_color="white", border_color=WARM_COLORS['coral'], border_width=2, button_color=WARM_COLORS['coral'], button_hover_color=self.lighten_color(WARM_COLORS['coral']))
        dropdown.pack(side="right", fill="x", expand=True)
        dropdown.set(default_value if default_value else options[0])

        return dropdown

    def create_switch_field(self, parent, label, key, default_value=False):
        """إنشاء حقل مفتاح تشغيل/إيقاف"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        label_widget = ctk.CTkLabel(field_frame, text=label, font=(FONTS['arabic'], 12, "bold"), text_color=WARM_COLORS['deep_teal'], anchor="e", width=150)
        label_widget.pack(side="right", padx=(0, 10))

        switch = ctk.CTkSwitch(field_frame, text="", font=(FONTS['arabic'], 12), progress_color=WARM_COLORS['mint'], button_color=WARM_COLORS['coral'], button_hover_color=self.lighten_color(WARM_COLORS['coral']))
        switch.pack(side="right")

        if default_value:
            switch.select()
        else:
            switch.deselect()

        return switch

    def lighten_color(self, color):
        """تفتيح اللون للتأثير عند التمرير"""
        if color.startswith('#'):
            hex_color = color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        return color


# يمكن إضافة المزيد من الأقسام المتقدمة هنا...
