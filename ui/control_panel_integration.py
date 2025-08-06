# -*- coding: utf-8 -*-
"""
تكامل الأقسام المتقدمة مع لوحة التحكم المركزية
ربط جميع الأقسام الـ11 المطورة بالتفصيل
"""

import customtkinter as ctk
from ui.advanced_sections import AdvancedInvoicesSettings, AdvancedPayrollSettings, AdvancedWarehouseSettings
from ui.advanced_sections_part2 import AdvancedModulesControl, AdvancedBackupSystem

class AdvancedControlPanelIntegration:
    """تكامل الأقسام المتقدمة"""
    
    def __init__(self, main_panel):
        self.main_panel = main_panel
        
        # إنشاء كائنات الأقسام المتقدمة
        self.invoices_settings = AdvancedInvoicesSettings(main_panel)
        self.payroll_settings = AdvancedPayrollSettings(main_panel)
        self.warehouse_settings = AdvancedWarehouseSettings(main_panel)
        self.modules_control = AdvancedModulesControl(main_panel)
        self.backup_system = AdvancedBackupSystem(main_panel)
    
    def integrate_advanced_sections(self):
        """دمج الأقسام المتقدمة مع لوحة التحكم الرئيسية"""
        
        # استبدال الدوال الأساسية بالمتقدمة
        self.main_panel.create_invoices_settings = self.create_advanced_invoices_settings
        self.main_panel.create_payroll_settings = self.create_advanced_payroll_settings
        self.main_panel.create_warehouses_settings = self.create_advanced_warehouses_settings
        self.main_panel.create_modules_settings = self.create_advanced_modules_settings
        self.main_panel.create_backup_settings = self.create_advanced_backup_settings
        
        # إضافة الأقسام الجديدة
        self.main_panel.create_import_export_settings = self.create_advanced_import_export_settings
        self.main_panel.create_appearance_settings = self.create_advanced_appearance_settings
        self.main_panel.create_security_settings = self.create_advanced_security_settings
        self.main_panel.create_numbering_settings = self.create_advanced_numbering_settings
    
    def create_advanced_invoices_settings(self):
        """إعدادات الفواتير المتقدمة"""
        self.invoices_settings.create_invoices_settings(self.main_panel.scrollable_frame)
    
    def create_advanced_payroll_settings(self):
        """إعدادات الرواتب المتقدمة"""
        self.payroll_settings.create_payroll_settings(self.main_panel.scrollable_frame)
    
    def create_advanced_warehouses_settings(self):
        """إعدادات المخازن المتقدمة"""
        self.warehouse_settings.create_warehouse_settings(self.main_panel.scrollable_frame)
    
    def create_advanced_modules_settings(self):
        """إعدادات الموديلات المتقدمة"""
        self.modules_control.create_modules_settings(self.main_panel.scrollable_frame)
    
    def create_advanced_backup_settings(self):
        """إعدادات النسخ الاحتياطي المتقدمة"""
        self.backup_system.create_backup_settings(self.main_panel.scrollable_frame)
    
    def create_advanced_import_export_settings(self):
        """إعدادات استيراد وتصدير البيانات المتقدمة"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
        # رأس القسم
        self.create_section_header(
            "استيراد من Excel",
            "📊",
            "واجهة شاملة لاستيراد البيانات مع التحقق والتصحيح التلقائي",
            WARM_COLORS['turquoise']
        )
        
        # بطاقة إعدادات الاستيراد
        def import_settings_content(parent):
            # أنواع البيانات المدعومة
            data_types_title = ctk.CTkLabel(
                parent,
                text="📋 أنواع البيانات المدعومة:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            data_types_title.pack(anchor="e", pady=(0, 10))
            
            # قائمة أنواع البيانات
            data_types = [
                {"name": "المنتجات والخدمات", "icon": "📦", "supported": True},
                {"name": "العملاء والموردين", "icon": "👥", "supported": True},
                {"name": "الفواتير والمعاملات", "icon": "🧾", "supported": True},
                {"name": "حركات المخزون", "icon": "📊", "supported": True},
                {"name": "بيانات الموظفين", "icon": "👨‍💼", "supported": False},
                {"name": "الحسابات المالية", "icon": "💰", "supported": True}
            ]
            
            for data_type in data_types:
                type_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
                type_frame.pack(fill="x", pady=3)
                
                status_icon = "✅" if data_type['supported'] else "❌"
                type_text = f"{data_type['icon']} {data_type['name']} {status_icon}"
                
                type_label = ctk.CTkLabel(
                    type_frame,
                    text=type_text,
                    font=(FONTS['arabic'], 12),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                type_label.pack(padx=15, pady=8, anchor="e")
            
            # إعدادات الاستيراد
            self.create_switch_field(parent, "التحقق من صحة البيانات:", "validate_import_data", True)
            self.create_switch_field(parent, "إنشاء نسخة احتياطية قبل الاستيراد:", "backup_before_import", True)
            self.create_switch_field(parent, "تجاهل الصفوف الفارغة:", "skip_empty_rows", True)
            self.create_input_field(parent, "الحد الأقصى للصفوف:", "max_import_rows", "10000")
            
            # زر الاستيراد
            import_btn = ctk.CTkButton(
                parent,
                text="📥 بدء عملية الاستيراد",
                font=(FONTS['arabic'], 14, "bold"),
                fg_color=WARM_COLORS['turquoise'],
                hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                height=40,
                command=self.start_import_process
            )
            import_btn.pack(pady=15)
        
        self.create_settings_card("📥 إعدادات الاستيراد", import_settings_content, WARM_COLORS['light_peach'])
    
    def create_advanced_appearance_settings(self):
        """إعدادات تخصيص الواجهة المتقدمة"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
        # رأس القسم
        self.create_section_header(
            "تخصيص الواجهة",
            "🎨",
            "منتقي الألوان المتقدم، اختيار الخطوط العربية، تخصيص الثيمات",
            WARM_COLORS['violet']
        )
        
        # بطاقة الثيمات الجاهزة
        def themes_content(parent):
            themes_title = ctk.CTkLabel(
                parent,
                text="🎨 الثيمات الجاهزة:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            themes_title.pack(anchor="e", pady=(0, 10))
            
            # الثيمات المتاحة
            themes = [
                {"name": "الثيم الدافئ", "colors": ["#FF6B6B", "#FF8E53", "#FFD93D"], "description": "ألوان دافئة وجذابة"},
                {"name": "الثيم الطبيعي", "colors": ["#6BCF7F", "#4ECDC4", "#A8E6CF"], "description": "ألوان طبيعية منعشة"},
                {"name": "الثيم الملكي", "colors": ["#96CEB4", "#6A4C93", "#45B7D1"], "description": "ألوان أنيقة وراقية"},
                {"name": "ثيم مخصص", "colors": ["#CUSTOM"], "description": "اختر ألوانك المفضلة"}
            ]
            
            for theme in themes:
                theme_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
                theme_frame.pack(fill="x", pady=5)
                
                # معلومات الثيم
                info_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
                info_frame.pack(side="right", fill="both", expand=True, padx=15, pady=10)
                
                theme_name = ctk.CTkLabel(
                    info_frame,
                    text=theme['name'],
                    font=(FONTS['arabic'], 12, "bold"),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                theme_name.pack(anchor="e")
                
                theme_desc = ctk.CTkLabel(
                    info_frame,
                    text=theme['description'],
                    font=(FONTS['arabic'], 10),
                    text_color=WARM_COLORS['rich_purple'],
                    anchor="e"
                )
                theme_desc.pack(anchor="e", pady=(2, 0))
                
                # عينة الألوان
                colors_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
                colors_frame.pack(side="left", padx=15, pady=10)
                
                if theme['colors'][0] != "#CUSTOM":
                    for color in theme['colors']:
                        color_sample = ctk.CTkFrame(colors_frame, width=20, height=20, fg_color=color, corner_radius=10)
                        color_sample.pack(side="left", padx=2)
                else:
                    custom_btn = ctk.CTkButton(
                        colors_frame,
                        text="🎨",
                        width=30,
                        height=30,
                        fg_color=WARM_COLORS['violet'],
                        hover_color=self.lighten_color(WARM_COLORS['violet']),
                        command=self.customize_theme
                    )
                    custom_btn.pack(side="left")
        
        self.create_settings_card("🎨 الثيمات الجاهزة", themes_content, WARM_COLORS['light_peach'])
    
    def create_advanced_security_settings(self):
        """إعدادات نظام الأمان المتقدمة"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
        # رأس القسم
        self.create_section_header(
            "نظام الأمان",
            "🛡️",
            "الإقفال الجزئي، إعادة ضبط المصنع مع الحماية، سجل العمليات التفصيلي",
            WARM_COLORS['lavender']
        )
        
        # بطاقة مستويات الأمان
        def security_levels_content(parent):
            levels_title = ctk.CTkLabel(
                parent,
                text="🔒 مستويات الأمان:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            levels_title.pack(anchor="e", pady=(0, 10))
            
            # مستويات الأمان
            security_levels = [
                {"level": "أساسي", "description": "حماية أساسية للبيانات", "color": WARM_COLORS['mint']},
                {"level": "متوسط", "description": "حماية متقدمة مع التشفير", "color": WARM_COLORS['golden']},
                {"level": "عالي", "description": "حماية قصوى مع مراقبة شاملة", "color": WARM_COLORS['coral']},
                {"level": "عسكري", "description": "أعلى مستوى حماية متاح", "color": WARM_COLORS['deep_teal']}
            ]
            
            for level in security_levels:
                level_frame = ctk.CTkFrame(parent, fg_color=level['color'], corner_radius=8)
                level_frame.pack(fill="x", pady=3)
                
                level_text = f"🔐 {level['level']} - {level['description']}"
                level_label = ctk.CTkLabel(
                    level_frame,
                    text=level_text,
                    font=(FONTS['arabic'], 12, "bold"),
                    text_color="white",
                    anchor="e"
                )
                level_label.pack(padx=15, pady=8, anchor="e")
        
        self.create_settings_card("🔒 مستويات الأمان", security_levels_content, WARM_COLORS['light_peach'])
    
    def create_advanced_numbering_settings(self):
        """إعدادات الأرقام التسلسلية المتقدمة"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
        # رأس القسم
        self.create_section_header(
            "الأرقام التسلسلية",
            "🔢",
            "نظام توليد الأرقام التلقائي القابل للتخصيص لجميع الفواتير والموظفين والعملاء",
            WARM_COLORS['turquoise']
        )
        
        # بطاقة قوالب الترقيم
        def numbering_templates_content(parent):
            templates_title = ctk.CTkLabel(
                parent,
                text="📋 قوالب الترقيم:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            templates_title.pack(anchor="e", pady=(0, 10))
            
            # أمثلة على القوالب
            templates = [
                {"type": "فواتير البيع", "template": "INV-{YYYY}-{MM}-{###}", "example": "INV-2025-07-001"},
                {"type": "فواتير الشراء", "template": "PUR-{YYYY}-{###}", "example": "PUR-2025-001"},
                {"type": "الموظفين", "template": "EMP-{##}-{####}", "example": "EMP-HZ-0012"},
                {"type": "العملاء", "template": "CUS-{YYYY}-{###}", "example": "CUS-2025-001"},
                {"type": "المرتجعات", "template": "RET-{MM}-{YYYY}-{###}", "example": "RET-07-2025-003"}
            ]
            
            for template in templates:
                template_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
                template_frame.pack(fill="x", pady=3)
                
                template_text = f"🔢 {template['type']}: {template['template']} → {template['example']}"
                template_label = ctk.CTkLabel(
                    template_frame,
                    text=template_text,
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                template_label.pack(padx=15, pady=8, anchor="e")
        
        self.create_settings_card("📋 قوالب الترقيم", numbering_templates_content, WARM_COLORS['light_peach'])
    
    # الدوال المساعدة
    def create_section_header(self, title, icon, description, color):
        """إنشاء رأس القسم"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
        header_frame = ctk.CTkFrame(
            self.main_panel.scrollable_frame,
            height=100,
            fg_color=color,
            corner_radius=15
        )
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
    
    def create_settings_card(self, title, content_func, color=None):
        """إنشاء بطاقة إعدادات"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
        if color is None:
            color = WARM_COLORS['light_peach']
            
        card_frame = ctk.CTkFrame(self.main_panel.scrollable_frame, fg_color=color, corner_radius=12)
        card_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(card_frame, text=title, font=(FONTS['arabic'], 16, "bold"), text_color=WARM_COLORS['dark_coral'], anchor="e")
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        content_func(content_frame)
        return card_frame
    
    def create_switch_field(self, parent, label, key, default_value=False):
        """إنشاء حقل مفتاح تشغيل/إيقاف"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
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
    
    def create_input_field(self, parent, label, key, default_value=""):
        """إنشاء حقل إدخال نص"""
        from themes.modern_theme import FONTS
        from ui.advanced_sections import WARM_COLORS
        
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
    
    # دوال الإجراءات
    def start_import_process(self):
        """بدء عملية الاستيراد"""
        from tkinter import messagebox
        messagebox.showinfo("استيراد البيانات", "سيتم فتح معالج استيراد البيانات من Excel")
    
    def customize_theme(self):
        """تخصيص الثيم"""
        from tkinter import messagebox
        messagebox.showinfo("تخصيص الثيم", "سيتم فتح محرر الثيمات المخصصة")


# دالة التكامل الرئيسية
def integrate_advanced_control_panel(main_panel):
    """دمج الأقسام المتقدمة مع لوحة التحكم الرئيسية"""
    integration = AdvancedControlPanelIntegration(main_panel)
    integration.integrate_advanced_sections()
    return integration
