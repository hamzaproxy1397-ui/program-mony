# -*- coding: utf-8 -*-
"""
الأقسام المتقدمة للوحة التحكم المركزية - الجزء الثاني
تطوير مفصل وعميق للأقسام المتبقية
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

class AdvancedModulesControl:
    """التحكم في الموديلات المتقدم"""
    
    def __init__(self, parent_panel):
        self.parent = parent_panel
        self.modules_status = {}
    
    def create_modules_settings(self, scrollable_frame):
        """إنشاء إعدادات التحكم في الموديلات"""
        # رأس القسم
        self.create_section_header(
            scrollable_frame,
            "التحكم في الموديلات",
            "🔧",
            "واجهة لإظهار/إخفاء جميع الميزات والموديلات النشطة في البرنامج",
            WARM_COLORS['rose']
        )
        
        # بطاقة الموديلات الأساسية
        def basic_modules_content(parent):
            modules = [
                {"key": "sales", "name": "موديل المبيعات", "description": "إدارة فواتير البيع والعملاء", "icon": "🛒", "enabled": True},
                {"key": "purchases", "name": "موديل المشتريات", "description": "إدارة فواتير الشراء والموردين", "icon": "🛍️", "enabled": True},
                {"key": "inventory", "name": "موديل المخازن", "description": "إدارة المخزون والمنتجات", "icon": "📦", "enabled": True},
                {"key": "accounts", "name": "موديل الحسابات", "description": "النظام المحاسبي والتقارير المالية", "icon": "💰", "enabled": True},
                {"key": "payroll", "name": "موديل الرواتب", "description": "إدارة رواتب الموظفين", "icon": "💼", "enabled": True}
            ]
            
            for module in modules:
                self.create_module_card(parent, module)
        
        self.create_settings_card(scrollable_frame, "🧩 الموديلات الأساسية", basic_modules_content, WARM_COLORS['light_peach'])
        
        # بطاقة الموديلات المتقدمة
        def advanced_modules_content(parent):
            modules = [
                {"key": "pos", "name": "نقاط البيع (POS)", "description": "نظام نقاط البيع التفاعلي", "icon": "🏪", "enabled": True},
                {"key": "reports", "name": "التقارير المتقدمة", "description": "تقارير تحليلية ومخصصة", "icon": "📊", "enabled": True},
                {"key": "crm", "name": "إدارة العملاء (CRM)", "description": "نظام إدارة علاقات العملاء", "icon": "👥", "enabled": False},
                {"key": "barcode", "name": "نظام الباركود", "description": "قراءة وطباعة الباركود", "icon": "📱", "enabled": True},
                {"key": "excel", "name": "تكامل Excel", "description": "استيراد وتصدير البيانات", "icon": "📈", "enabled": True}
            ]
            
            for module in modules:
                self.create_module_card(parent, module)
        
        self.create_settings_card(scrollable_frame, "⚡ الموديلات المتقدمة", advanced_modules_content, WARM_COLORS['mint_bg'])
        
        # بطاقة الموديلات الإضافية
        def additional_modules_content(parent):
            modules = [
                {"key": "manufacturing", "name": "موديل التصنيع", "description": "إدارة عمليات التصنيع والإنتاج", "icon": "🏭", "enabled": False},
                {"key": "projects", "name": "إدارة المشاريع", "description": "تتبع المشاريع والمهام", "icon": "📋", "enabled": False},
                {"key": "hr", "name": "الموارد البشرية", "description": "إدارة شاملة للموظفين", "icon": "👨‍💼", "enabled": False},
                {"key": "assets", "name": "إدارة الأصول", "description": "تتبع الأصول الثابتة", "icon": "🏢", "enabled": False},
                {"key": "quality", "name": "ضمان الجودة", "description": "نظام إدارة الجودة", "icon": "✅", "enabled": False}
            ]
            
            for module in modules:
                self.create_module_card(parent, module)
        
        self.create_settings_card(scrollable_frame, "🔮 الموديلات الإضافية", additional_modules_content, WARM_COLORS['soft_cream'])
    
    def create_module_card(self, parent, module):
        """إنشاء بطاقة موديل"""
        module_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
        module_frame.pack(fill="x", pady=5)
        
        # معلومات الموديل
        info_frame = ctk.CTkFrame(module_frame, fg_color="transparent")
        info_frame.pack(side="right", fill="both", expand=True, padx=15, pady=10)
        
        # العنوان والأيقونة
        title_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        title_frame.pack(fill="x")
        
        icon_label = ctk.CTkLabel(
            title_frame,
            text=module['icon'],
            font=("Segoe UI Emoji", 20),
            text_color=WARM_COLORS['deep_teal']
        )
        icon_label.pack(side="right", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=module['name'],
            font=(FONTS['arabic'], 14, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e"
        )
        title_label.pack(side="right", fill="x", expand=True)
        
        # الوصف
        desc_label = ctk.CTkLabel(
            info_frame,
            text=module['description'],
            font=(FONTS['arabic'], 11),
            text_color=WARM_COLORS['rich_purple'],
            anchor="e"
        )
        desc_label.pack(fill="x", pady=(5, 0))
        
        # مفتاح التفعيل
        switch_frame = ctk.CTkFrame(module_frame, fg_color="transparent")
        switch_frame.pack(side="left", padx=15, pady=10)
        
        switch = ctk.CTkSwitch(
            switch_frame,
            text="",
            progress_color=WARM_COLORS['mint'],
            button_color=WARM_COLORS['coral'],
            button_hover_color=self.lighten_color(WARM_COLORS['coral']),
            command=lambda: self.toggle_module(module['key'], switch)
        )
        switch.pack()
        
        if module['enabled']:
            switch.select()
        else:
            switch.deselect()
        
        # حالة الموديل
        status_text = "🟢 مفعل" if module['enabled'] else "🔴 معطل"
        status_label = ctk.CTkLabel(
            switch_frame,
            text=status_text,
            font=(FONTS['arabic'], 10),
            text_color=WARM_COLORS['mint'] if module['enabled'] else WARM_COLORS['coral']
        )
        status_label.pack(pady=(5, 0))
    
    def toggle_module(self, module_key, switch):
        """تبديل حالة الموديل"""
        is_enabled = switch.get() == 1
        self.modules_status[module_key] = is_enabled
        
        status = "تم تفعيل" if is_enabled else "تم إلغاء تفعيل"
        messagebox.showinfo("تغيير حالة الموديل", f"{status} الموديل بنجاح!")
    
    # الدوال المساعدة
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
    
    def lighten_color(self, color):
        """تفتيح اللون للتأثير عند التمرير"""
        if color.startswith('#'):
            hex_color = color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        return color


class AdvancedBackupSystem:
    """نظام النسخ الاحتياطي المتقدم"""
    
    def __init__(self, parent_panel):
        self.parent = parent_panel
        self.backup_schedule = {}
    
    def create_backup_settings(self, scrollable_frame):
        """إنشاء إعدادات النسخ الاحتياطي المتقدمة"""
        # رأس القسم
        self.create_section_header(
            scrollable_frame,
            "النسخ الاحتياطي",
            "💾",
            "نظام النسخ التلقائي المتقدم، استرجاع النظام، جدولة النسخ",
            WARM_COLORS['peach']
        )
        
        # بطاقة الجدولة التلقائية
        def auto_schedule_content(parent):
            # تفعيل النسخ التلقائي
            self.create_switch_field(parent, "تفعيل النسخ التلقائي:", "auto_backup_enabled", True)
            
            # تكرار النسخ
            self.create_dropdown_field(parent, "تكرار النسخ:", "backup_frequency",
                                     ["كل ساعة", "كل 6 ساعات", "يومياً", "أسبوعياً", "شهرياً"], "يومياً")
            
            # وقت النسخ
            self.create_dropdown_field(parent, "وقت النسخ:", "backup_time",
                                     ["01:00", "02:00", "03:00", "04:00", "23:00", "00:00"], "02:00")
            
            # أيام النسخ (للنسخ الأسبوعي)
            days_frame = ctk.CTkFrame(parent, fg_color="transparent")
            days_frame.pack(fill="x", pady=10)
            
            days_label = ctk.CTkLabel(
                days_frame,
                text="أيام النسخ الأسبوعي:",
                font=(FONTS['arabic'], 12, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            days_label.pack(anchor="e", pady=(0, 5))
            
            days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"]
            self.day_vars = {}
            
            for day in days:
                day_frame = ctk.CTkFrame(days_frame, fg_color="transparent")
                day_frame.pack(fill="x", pady=2)
                
                var = ctk.BooleanVar(value=True if day in ["السبت", "الأربعاء"] else False)
                self.day_vars[day] = var
                
                checkbox = ctk.CTkCheckBox(
                    day_frame,
                    text=day,
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['deep_teal'],
                    variable=var,
                    checkbox_width=20,
                    checkbox_height=20,
                    fg_color=WARM_COLORS['mint'],
                    hover_color=self.lighten_color(WARM_COLORS['mint'])
                )
                checkbox.pack(anchor="e")
            
            # إعدادات إضافية
            self.create_input_field(parent, "عدد النسخ المحفوظة:", "max_backups", "30")
            self.create_switch_field(parent, "ضغط النسخ:", "compress_backups", True)
            self.create_switch_field(parent, "تشفير النسخ:", "encrypt_backups", False)
        
        self.create_settings_card(scrollable_frame, "⏰ الجدولة التلقائية", auto_schedule_content, WARM_COLORS['light_peach'])
        
        # بطاقة إدارة النسخ
        def backup_management_content(parent):
            # أزرار الإجراءات السريعة
            quick_actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
            quick_actions_frame.pack(fill="x", pady=10)
            
            # نسخة احتياطية فورية
            instant_backup_btn = ctk.CTkButton(
                quick_actions_frame,
                text="💾 نسخة احتياطية فورية",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['mint'],
                hover_color=self.lighten_color(WARM_COLORS['mint']),
                height=40,
                command=self.create_instant_backup
            )
            instant_backup_btn.pack(side="right", padx=5, pady=5)
            
            # استعادة من نسخة
            restore_btn = ctk.CTkButton(
                quick_actions_frame,
                text="🔄 استعادة من نسخة",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['sunset'],
                hover_color=self.lighten_color(WARM_COLORS['sunset']),
                height=40,
                command=self.restore_from_backup
            )
            restore_btn.pack(side="right", padx=5, pady=5)
            
            # عرض النسخ المتاحة
            backups_title = ctk.CTkLabel(
                parent,
                text="📂 النسخ الاحتياطية المتاحة:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            backups_title.pack(anchor="e", pady=(20, 10))
            
            # قائمة النسخ (مثال)
            sample_backups = [
                {"name": "backup_20250722_020000.db", "size": "15.2 MB", "date": "2025-07-22 02:00:00", "type": "تلقائي"},
                {"name": "backup_20250721_020000.db", "size": "14.8 MB", "date": "2025-07-21 02:00:00", "type": "تلقائي"},
                {"name": "backup_manual_20250720.db", "size": "14.5 MB", "date": "2025-07-20 15:30:00", "type": "يدوي"}
            ]
            
            for backup in sample_backups:
                backup_card = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
                backup_card.pack(fill="x", pady=3)
                
                backup_info = ctk.CTkLabel(
                    backup_card,
                    text=f"📁 {backup['name']} - {backup['size']} - {backup['date']} ({backup['type']})",
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                backup_info.pack(side="right", padx=15, pady=8)
                
                # أزرار الإجراءات
                actions_frame = ctk.CTkFrame(backup_card, fg_color="transparent")
                actions_frame.pack(side="left", padx=15, pady=5)
                
                restore_btn = ctk.CTkButton(
                    actions_frame,
                    text="🔄",
                    width=30,
                    height=25,
                    fg_color=WARM_COLORS['turquoise'],
                    hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                    command=lambda b=backup: self.restore_specific_backup(b)
                )
                restore_btn.pack(side="left", padx=1)
                
                delete_btn = ctk.CTkButton(
                    actions_frame,
                    text="🗑️",
                    width=30,
                    height=25,
                    fg_color=WARM_COLORS['coral'],
                    hover_color=self.lighten_color(WARM_COLORS['coral']),
                    command=lambda b=backup: self.delete_backup(b)
                )
                delete_btn.pack(side="left", padx=1)
        
        self.create_settings_card(scrollable_frame, "🛠️ إدارة النسخ", backup_management_content, WARM_COLORS['mint_bg'])
    
    def create_instant_backup(self):
        """إنشاء نسخة احتياطية فورية"""
        messagebox.showinfo("نسخة احتياطية فورية", "سيتم إنشاء نسخة احتياطية فورية")
    
    def restore_from_backup(self):
        """استعادة من نسخة احتياطية"""
        messagebox.showinfo("استعادة النسخة", "سيتم فتح نافذة اختيار النسخة الاحتياطية")
    
    def restore_specific_backup(self, backup):
        """استعادة نسخة احتياطية محددة"""
        result = messagebox.askyesno("تأكيد الاستعادة", f"هل تريد استعادة النسخة:\n{backup['name']}؟")
        if result:
            messagebox.showinfo("تم", "تم استعادة النسخة الاحتياطية بنجاح")
    
    def delete_backup(self, backup):
        """حذف نسخة احتياطية"""
        result = messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف النسخة:\n{backup['name']}؟")
        if result:
            messagebox.showinfo("تم", "تم حذف النسخة الاحتياطية")
    
    # نفس الدوال المساعدة من الأقسام السابقة
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
    
    def lighten_color(self, color):
        """تفتيح اللون للتأثير عند التمرير"""
        if color.startswith('#'):
            hex_color = color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        return color


# يمكن إضافة المزيد من الأقسام هنا...
