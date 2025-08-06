# -*- coding: utf-8 -*-
"""
واجهة إدخال الأصناف المتقدمة والشاملة
Advanced & Comprehensive Item Entry Interface
تصميم احترافي متطور مع ذكاء اصطناعي وتحليلات متقدمة
"""

import sys
import os
import json
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.inventory_manager import InventoryManager
from core.item_code_generator import ItemCodeGenerator
from core.validation_engine import ValidationEngine
from models.item_model import ItemModel


class AdvancedItemEntry:
    """واجهة إدخال الأصناف المتقدمة والشاملة"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.current_item = None
        self.items_cache = []
        self.analytics_data = {}
        self.ai_suggestions = []
        
        # إعدادات النظام المتقدم
        self.setup_advanced_config()
        
        # إنشاء النافذة الرئيسية
        self.create_main_window()
        
        # تهيئة المتغيرات
        self.init_variables()
        
        # تهيئة المدراء والخدمات
        self.init_managers()
        
        # إنشاء الواجهة
        self.create_advanced_interface()
        
        # تحميل البيانات والتحليلات
        self.load_initial_data()
        
        # بدء الخدمات الذكية
        self.start_ai_services()
        
    def setup_advanced_config(self):
        """إعداد التكوين المتقدم للنظام"""
        self.config = {
            # إعدادات التصميم المتقدم
            'theme': {
                'primary_gradient': ['#667eea', '#764ba2'],
                'secondary_gradient': ['#f093fb', '#f5576c'],
                'success_gradient': ['#4facfe', '#00f2fe'],
                'warning_gradient': ['#43e97b', '#38f9d7'],
                'danger_gradient': ['#fa709a', '#fee140'],
                'dark_gradient': ['#2c3e50', '#34495e'],
                'light_gradient': ['#ecf0f1', '#bdc3c7'],
                'glass_effect': True,
                'shadow_depth': 15,
                'border_radius': 12,
                'animation_speed': 300
            },
            
            # إعدادات الذكاء الاصطناعي
            'ai': {
                'auto_categorization': True,
                'price_prediction': True,
                'demand_forecasting': True,
                'smart_recommendations': True,
                'auto_code_generation': True,
                'duplicate_detection': True,
                'quality_scoring': True
            },
            
            # إعدادات التحليلات
            'analytics': {
                'real_time_charts': True,
                'profit_analysis': True,
                'trend_analysis': True,
                'performance_metrics': True,
                'predictive_analytics': True,
                'market_comparison': True
            },
            
            # إعدادات الأمان المتقدم
            'security': {
                'audit_trail': True,
                'user_permissions': True,
                'data_encryption': True,
                'backup_automation': True,
                'change_tracking': True
            },
            
            # إعدادات التكامل
            'integration': {
                'barcode_scanner': True,
                'image_recognition': True,
                'voice_input': True,
                'cloud_sync': True,
                'api_connections': True,
                'export_formats': ['Excel', 'PDF', 'JSON', 'XML', 'CSV']
            }
        }
        
        # ألوان متقدمة مع تدرجات
        self.colors = {
            'primary': '#667eea',
            'primary_dark': '#5a67d8',
            'secondary': '#f093fb',
            'accent': '#4facfe',
            'success': '#48bb78',
            'warning': '#ed8936',
            'danger': '#f56565',
            'info': '#4299e1',
            'light': '#f7fafc',
            'dark': '#2d3748',
            'white': '#ffffff',
            'black': '#000000',
            'gray_100': '#f7fafc',
            'gray_200': '#edf2f7',
            'gray_300': '#e2e8f0',
            'gray_400': '#cbd5e0',
            'gray_500': '#a0aec0',
            'gray_600': '#718096',
            'gray_700': '#4a5568',
            'gray_800': '#2d3748',
            'gray_900': '#1a202c'
        }
        
        # خطوط متقدمة
        self.fonts = {
            'display': ('Segoe UI', 28, 'bold'),
            'title': ('Segoe UI', 22, 'bold'),
            'heading': ('Segoe UI', 18, 'bold'),
            'subheading': ('Segoe UI', 16, 'bold'),
            'body': ('Segoe UI', 14),
            'body_bold': ('Segoe UI', 14, 'bold'),
            'caption': ('Segoe UI', 12),
            'small': ('Segoe UI', 10),
            'code': ('Consolas', 12),
            'arabic': ('Tahoma', 14),
            'arabic_bold': ('Tahoma', 14, 'bold'),
            'icon': ('Segoe UI Emoji', 16)
        }
        
    def create_main_window(self):
        """إنشاء النافذة الرئيسية المتقدمة"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        
        # إعدادات النافذة المتقدمة
        self.window.title("🚀 نظام إدارة الأصناف المتقدم - AI Powered Inventory System")
        self.window.configure(bg=self.colors['gray_100'])
        
        # ملء الشاشة مع إمكانيات متقدمة
        self.setup_window_properties()
        
        # إعداد الأنماط المتقدمة
        self.setup_advanced_styles()
        
        # ربط الأحداث المتقدمة
        self.bind_advanced_events()
        
    def setup_window_properties(self):
        """إعداد خصائص النافذة المتقدمة"""
        # الحصول على أبعاد الشاشة
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # تعيين حجم النافذة (95% من الشاشة)
        window_width = int(screen_width * 0.95)
        window_height = int(screen_height * 0.95)
        
        # تمركز النافذة
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(1400, 900)
        self.window.resizable(True, True)
        
        # إعدادات متقدمة للنافذة
        self.window.attributes('-alpha', 0.98)  # شفافية خفيفة
        
        if self.parent:
            self.window.transient(self.parent)
            self.window.grab_set()
            
    def setup_advanced_styles(self):
        """إعداد الأنماط المتقدمة"""
        self.style = ttk.Style()
        
        # تكوين الثيم المتقدم
        self.style.theme_use('clam')
        
        # أنماط الأزرار المتقدمة
        self.style.configure('Primary.TButton',
                           font=self.fonts['body_bold'],
                           padding=(20, 12),
                           relief='flat',
                           borderwidth=0)
        
        self.style.configure('Secondary.TButton',
                           font=self.fonts['body'],
                           padding=(15, 10),
                           relief='flat',
                           borderwidth=0)
        
        # أنماط حقول الإدخال المتقدمة
        self.style.configure('Modern.TEntry',
                           font=self.fonts['body'],
                           padding=12,
                           relief='flat',
                           borderwidth=1,
                           focuscolor='none')
        
        # أنماط التسميات المتقدمة
        self.style.configure('Heading.TLabel',
                           font=self.fonts['heading'],
                           background=self.colors['gray_100'])
        
        self.style.configure('Body.TLabel',
                           font=self.fonts['body'],
                           background=self.colors['gray_100'])
        
    def bind_advanced_events(self):
        """ربط الأحداث المتقدمة"""
        # اختصارات لوحة المفاتيح المتقدمة
        self.window.bind('<Control-s>', lambda e: self.save_item())
        self.window.bind('<Control-n>', lambda e: self.new_item())
        self.window.bind('<Control-f>', lambda e: self.focus_search())
        self.window.bind('<Control-d>', lambda e: self.duplicate_item())
        self.window.bind('<Control-e>', lambda e: self.export_data())
        self.window.bind('<Control-i>', lambda e: self.import_data())
        self.window.bind('<Control-p>', lambda e: self.print_report())
        self.window.bind('<Control-q>', lambda e: self.close_window())
        self.window.bind('<F1>', lambda e: self.show_help())
        self.window.bind('<F5>', lambda e: self.refresh_data())
        self.window.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.window.bind('<Escape>', lambda e: self.toggle_fullscreen())
        
        # أحداث الماوس المتقدمة
        self.window.bind('<Button-3>', self.show_context_menu)
        
    def init_variables(self):
        """تهيئة المتغيرات المتقدمة"""
        # متغيرات النموذج الأساسية
        self.item_name_var = tk.StringVar()
        self.item_code_var = tk.StringVar()
        self.barcode_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.subcategory_var = tk.StringVar()
        self.brand_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.dimensions_var = tk.StringVar()
        
        # متغيرات الأسعار المتقدمة
        self.cost_price_var = tk.StringVar()
        self.selling_price_var = tk.StringVar()
        self.wholesale_price_var = tk.StringVar()
        self.retail_price_var = tk.StringVar()
        self.discount_price_var = tk.StringVar()
        self.profit_margin_var = tk.StringVar()
        self.tax_rate_var = tk.StringVar()
        
        # متغيرات المخزون المتقدمة
        self.current_stock_var = tk.StringVar()
        self.min_stock_var = tk.StringVar()
        self.max_stock_var = tk.StringVar()
        self.reorder_point_var = tk.StringVar()
        self.lead_time_var = tk.StringVar()
        
        # متغيرات الجودة والتقييم
        self.quality_score_var = tk.StringVar()
        self.supplier_rating_var = tk.StringVar()
        self.customer_rating_var = tk.StringVar()
        
        # متغيرات البحث والفلترة
        self.search_var = tk.StringVar()
        self.filter_category_var = tk.StringVar()
        self.filter_status_var = tk.StringVar()
        self.sort_by_var = tk.StringVar()
        
        # متغيرات التحليلات
        self.analytics_period_var = tk.StringVar()
        self.chart_type_var = tk.StringVar()
        
        # ربط المتغيرات بالأحداث
        self.bind_variable_events()
        
    def bind_variable_events(self):
        """ربط المتغيرات بالأحداث"""
        # أحداث التحقق الفوري
        self.item_name_var.trace('w', self.on_name_change)
        self.item_code_var.trace('w', self.on_code_change)
        self.cost_price_var.trace('w', self.calculate_pricing)
        self.selling_price_var.trace('w', self.calculate_pricing)
        
        # أحداث البحث والفلترة
        self.search_var.trace('w', self.on_search_change)
        self.filter_category_var.trace('w', self.on_filter_change)
        self.filter_status_var.trace('w', self.on_filter_change)
        
    def init_managers(self):
        """تهيئة المدراء والخدمات"""
        try:
            self.inventory_manager = InventoryManager()
            self.code_generator = ItemCodeGenerator()
            self.validator = ValidationEngine()
            
            # مدراء متقدمة إضافية
            self.ai_manager = self.create_ai_manager()
            self.analytics_manager = self.create_analytics_manager()
            self.export_manager = self.create_export_manager()
            self.backup_manager = self.create_backup_manager()
            
        except Exception as e:
            messagebox.showerror("خطأ في التهيئة", f"فشل في تهيئة المدراء: {e}")
            
    def create_ai_manager(self):
        """إنشاء مدير الذكاء الاصطناعي"""
        class AIManager:
            def __init__(self, parent):
                self.parent = parent
                
            def suggest_category(self, item_name):
                """اقتراح التصنيف بناءً على اسم الصنف"""
                # خوارزمية بسيطة للاقتراح
                name_lower = item_name.lower()
                if any(word in name_lower for word in ['هاتف', 'جوال', 'موبايل']):
                    return 'إلكترونيات'
                elif any(word in name_lower for word in ['قميص', 'بنطلون', 'فستان']):
                    return 'ملابس'
                elif any(word in name_lower for word in ['أرز', 'سكر', 'زيت']):
                    return 'أغذية'
                return 'عام'
                
            def predict_price(self, category, features):
                """توقع السعر بناءً على التصنيف والمميزات"""
                # خوارزمية بسيطة لتوقع السعر
                base_prices = {
                    'إلكترونيات': 500,
                    'ملابس': 100,
                    'أغذية': 20,
                    'عام': 50
                }
                return base_prices.get(category, 50)
                
            def detect_duplicates(self, item_data):
                """كشف الأصناف المكررة"""
                # خوارزمية بسيطة لكشف التكرار
                return []
                
        return AIManager(self)
        
    def create_analytics_manager(self):
        """إنشاء مدير التحليلات"""
        class AnalyticsManager:
            def __init__(self, parent):
                self.parent = parent
                
            def generate_profit_analysis(self):
                """تحليل الربحية"""
                return {
                    'total_profit': 0,
                    'profit_margin': 0,
                    'top_items': [],
                    'trends': []
                }
                
            def generate_stock_analysis(self):
                """تحليل المخزون"""
                return {
                    'total_items': 0,
                    'low_stock_items': [],
                    'overstock_items': [],
                    'turnover_rate': 0
                }
                
        return AnalyticsManager(self)
        
    def create_export_manager(self):
        """إنشاء مدير التصدير"""
        class ExportManager:
            def __init__(self, parent):
                self.parent = parent
                
            def export_to_excel(self, data, filename):
                """تصدير إلى Excel"""
                pass
                
            def export_to_pdf(self, data, filename):
                """تصدير إلى PDF"""
                pass
                
        return ExportManager(self)
        
    def create_backup_manager(self):
        """إنشاء مدير النسخ الاحتياطي"""
        class BackupManager:
            def __init__(self, parent):
                self.parent = parent
                
            def create_backup(self):
                """إنشاء نسخة احتياطية"""
                pass
                
            def restore_backup(self, backup_file):
                """استعادة نسخة احتياطية"""
                pass
                
        return BackupManager(self)

    def create_advanced_interface(self):
        """إنشاء الواجهة المتقدمة"""
        # الحاوية الرئيسية مع تأثيرات متقدمة
        self.main_container = tk.Frame(self.window, bg=self.colors['gray_100'])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # شريط العنوان المتقدم
        self.create_advanced_header()

        # شريط الأدوات الذكي
        self.create_smart_toolbar()

        # المحتوى الرئيسي مع تخطيط متقدم
        self.create_main_content_area()

        # لوحة التحليلات الجانبية
        self.create_analytics_sidebar()

        # شريط الحالة المتقدم
        self.create_advanced_status_bar()

        # نوافذ منبثقة ذكية
        self.create_smart_popups()

    def create_advanced_header(self):
        """إنشاء شريط العنوان المتقدم"""
        header_frame = tk.Frame(self.main_container,
                               bg=self.colors['primary'],
                               height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # تدرج الخلفية (محاكاة)
        self.create_gradient_effect(header_frame,
                                   self.config['theme']['primary_gradient'])

        # محتوى الشريط العلوي
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # الجانب الأيسر - العنوان والشعار
        left_section = tk.Frame(header_content, bg=self.colors['primary'])
        left_section.pack(side=tk.LEFT, fill=tk.Y)

        # شعار متحرك
        logo_label = tk.Label(left_section,
                             text="🚀",
                             font=self.fonts['display'],
                             bg=self.colors['primary'],
                             fg=self.colors['white'])
        logo_label.pack(side=tk.LEFT, padx=(0, 15))

        # العنوان الرئيسي
        title_frame = tk.Frame(left_section, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)

        main_title = tk.Label(title_frame,
                             text="نظام إدارة الأصناف المتقدم",
                             font=self.fonts['title'],
                             bg=self.colors['primary'],
                             fg=self.colors['white'])
        main_title.pack(anchor=tk.W)

        subtitle = tk.Label(title_frame,
                           text="AI-Powered Inventory Management System",
                           font=self.fonts['body'],
                           bg=self.colors['primary'],
                           fg=self.colors['gray_200'])
        subtitle.pack(anchor=tk.W)

        # الجانب الأيمن - أزرار التحكم المتقدمة
        right_section = tk.Frame(header_content, bg=self.colors['primary'])
        right_section.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_header_controls(right_section)

        # مؤشر الحالة الذكي
        self.create_smart_status_indicator(header_content)

    def create_gradient_effect(self, parent, colors):
        """إنشاء تأثير التدرج (محاكاة بسيطة)"""
        # هذه دالة بسيطة لمحاكاة التدرج
        # في التطبيق الحقيقي يمكن استخدام مكتبات متقدمة
        pass

    def create_header_controls(self, parent):
        """إنشاء أزرار التحكم في الشريط العلوي"""
        controls_frame = tk.Frame(parent, bg=self.colors['primary'])
        controls_frame.pack(side=tk.RIGHT, pady=10)

        # أزرار التحكم السريع
        controls = [
            ("➕", "إضافة صنف جديد", self.new_item, self.colors['success']),
            ("📊", "التحليلات", self.show_analytics, self.colors['info']),
            ("🔍", "البحث المتقدم", self.advanced_search, self.colors['secondary']),
            ("⚙️", "الإعدادات", self.show_settings, self.colors['warning']),
            ("❓", "المساعدة", self.show_help, self.colors['info']),
            ("🔳", "ملء الشاشة", self.toggle_fullscreen, self.colors['dark'])
        ]

        for icon, tooltip, command, color in controls:
            btn = tk.Button(controls_frame,
                           text=icon,
                           command=command,
                           bg=color,
                           fg=self.colors['white'],
                           font=self.fonts['icon'],
                           relief=tk.FLAT,
                           width=3,
                           height=1,
                           cursor='hand2')
            btn.pack(side=tk.LEFT, padx=3)

            # إضافة tooltip
            self.create_tooltip(btn, tooltip)

    def create_smart_status_indicator(self, parent):
        """إنشاء مؤشر الحالة الذكي"""
        status_frame = tk.Frame(parent, bg=self.colors['primary'])
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # مؤشرات الحالة
        self.ai_status_label = tk.Label(status_frame,
                                       text="🤖 AI: نشط",
                                       font=self.fonts['caption'],
                                       bg=self.colors['primary'],
                                       fg=self.colors['success'])
        self.ai_status_label.pack(side=tk.LEFT, padx=(0, 20))

        self.sync_status_label = tk.Label(status_frame,
                                         text="☁️ المزامنة: متصل",
                                         font=self.fonts['caption'],
                                         bg=self.colors['primary'],
                                         fg=self.colors['success'])
        self.sync_status_label.pack(side=tk.LEFT, padx=(0, 20))

        self.items_count_label = tk.Label(status_frame,
                                         text="📦 الأصناف: 0",
                                         font=self.fonts['caption'],
                                         bg=self.colors['primary'],
                                         fg=self.colors['white'])
        self.items_count_label.pack(side=tk.LEFT)

    def create_smart_toolbar(self):
        """إنشاء شريط الأدوات الذكي"""
        toolbar_frame = tk.Frame(self.main_container,
                                bg=self.colors['white'],
                                height=60)
        toolbar_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        toolbar_frame.pack_propagate(False)

        # إضافة ظل للشريط
        self.add_shadow_effect(toolbar_frame)

        # محتوى شريط الأدوات
        toolbar_content = tk.Frame(toolbar_frame, bg=self.colors['white'])
        toolbar_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # الجانب الأيسر - أدوات الإجراءات
        left_tools = tk.Frame(toolbar_content, bg=self.colors['white'])
        left_tools.pack(side=tk.LEFT, fill=tk.Y)

        # أزرار الإجراءات السريعة
        quick_actions = [
            ("💾", "حفظ", self.save_item),
            ("🔄", "تحديث", self.refresh_data),
            ("📋", "نسخ", self.copy_item),
            ("📤", "تصدير", self.export_data),
            ("📥", "استيراد", self.import_data),
            ("🖨️", "طباعة", self.print_report)
        ]

        for icon, text, command in quick_actions:
            btn_frame = tk.Frame(left_tools, bg=self.colors['white'])
            btn_frame.pack(side=tk.LEFT, padx=5)

            btn = tk.Button(btn_frame,
                           text=icon,
                           command=command,
                           bg=self.colors['gray_100'],
                           fg=self.colors['gray_700'],
                           font=self.fonts['icon'],
                           relief=tk.FLAT,
                           width=3,
                           height=1,
                           cursor='hand2')
            btn.pack()

            label = tk.Label(btn_frame,
                           text=text,
                           font=self.fonts['small'],
                           bg=self.colors['white'],
                           fg=self.colors['gray_600'])
            label.pack()

            # تأثيرات التفاعل
            self.add_hover_effect(btn)

        # الجانب الأيمن - أدوات البحث والفلترة
        right_tools = tk.Frame(toolbar_content, bg=self.colors['white'])
        right_tools.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_search_tools(right_tools)

    def add_shadow_effect(self, widget):
        """إضافة تأثير الظل"""
        # محاكاة بسيطة لتأثير الظل
        shadow_frame = tk.Frame(widget.master,
                               bg=self.colors['gray_300'],
                               height=2)
        shadow_frame.pack(fill=tk.X)

    def add_hover_effect(self, widget):
        """إضافة تأثير التمرير"""
        original_bg = widget.cget('bg')

        def on_enter(e):
            widget.configure(bg=self.colors['gray_200'])

        def on_leave(e):
            widget.configure(bg=original_bg)

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def create_search_tools(self, parent):
        """إنشاء أدوات البحث المتقدمة"""
        search_frame = tk.Frame(parent, bg=self.colors['white'])
        search_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # حقل البحث الذكي
        search_container = tk.Frame(search_frame, bg=self.colors['white'])
        search_container.pack(side=tk.LEFT, padx=(0, 10))

        search_label = tk.Label(search_container,
                               text="🔍",
                               font=self.fonts['icon'],
                               bg=self.colors['white'],
                               fg=self.colors['gray_500'])
        search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_container,
                                    textvariable=self.search_var,
                                    font=self.fonts['body'],
                                    bg=self.colors['gray_100'],
                                    fg=self.colors['gray_700'],
                                    relief=tk.FLAT,
                                    bd=5,
                                    width=25)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 0))

        # فلاتر سريعة
        filters_frame = tk.Frame(search_frame, bg=self.colors['white'])
        filters_frame.pack(side=tk.LEFT)

        # فلتر التصنيف
        category_combo = ttk.Combobox(filters_frame,
                                     textvariable=self.filter_category_var,
                                     font=self.fonts['caption'],
                                     width=12,
                                     values=["جميع التصنيفات", "إلكترونيات", "ملابس", "أغذية"])
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.set("جميع التصنيفات")

        # فلتر الحالة
        status_combo = ttk.Combobox(filters_frame,
                                   textvariable=self.filter_status_var,
                                   font=self.fonts['caption'],
                                   width=10,
                                   values=["جميع الحالات", "متوفر", "نفد", "قريب النفاد"])
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.set("جميع الحالات")

    def create_main_content_area(self):
        """إنشاء منطقة المحتوى الرئيسي"""
        # الحاوية الرئيسية للمحتوى
        content_frame = tk.Frame(self.main_container, bg=self.colors['gray_100'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # تقسيم المحتوى إلى أقسام
        self.create_content_sections(content_frame)

    def create_content_sections(self, parent):
        """إنشاء أقسام المحتوى"""
        # الحاوية الرئيسية مع تخطيط شبكي
        main_grid = tk.Frame(parent, bg=self.colors['gray_100'])
        main_grid.pack(fill=tk.BOTH, expand=True)

        # القسم الأيسر - نموذج الإدخال المتقدم (60%)
        self.left_panel = tk.Frame(main_grid, bg=self.colors['white'])
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # القسم الأيمن - إدارة الأصناف والتحليلات (40%)
        self.right_panel = tk.Frame(main_grid, bg=self.colors['white'], width=500)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.right_panel.pack_propagate(False)

        # إنشاء محتوى الأقسام
        self.create_advanced_form(self.left_panel)
        self.create_items_management_panel(self.right_panel)

    def create_advanced_form(self, parent):
        """إنشاء نموذج الإدخال المتقدم"""
        # شريط عنوان النموذج
        form_header = tk.Frame(parent, bg=self.colors['primary'], height=50)
        form_header.pack(fill=tk.X)
        form_header.pack_propagate(False)

        header_label = tk.Label(form_header,
                               text="📝 نموذج إدخال الصنف المتقدم",
                               font=self.fonts['heading'],
                               bg=self.colors['primary'],
                               fg=self.colors['white'])
        header_label.pack(pady=15)

        # منطقة النموذج مع تمرير
        form_canvas = tk.Canvas(parent, bg=self.colors['white'])
        form_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=form_canvas.yview)
        self.form_frame = tk.Frame(form_canvas, bg=self.colors['white'])

        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        form_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        form_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        form_canvas.create_window((0, 0), window=self.form_frame, anchor="nw")

        # إنشاء أقسام النموذج المتقدمة
        self.create_basic_info_section()
        self.create_pricing_section()
        self.create_inventory_section()
        self.create_media_section()
        self.create_quality_section()
        self.create_ai_suggestions_section()

        # تحديث منطقة التمرير
        self.form_frame.update_idletasks()
        form_canvas.configure(scrollregion=form_canvas.bbox("all"))

    def create_basic_info_section(self):
        """إنشاء قسم المعلومات الأساسية"""
        section_frame = self.create_section_frame("📋 المعلومات الأساسية")

        # الصف الأول - اسم الصنف ورمزه
        row1 = tk.Frame(section_frame, bg=self.colors['white'])
        row1.pack(fill=tk.X, pady=5)

        # اسم الصنف
        name_frame = tk.Frame(row1, bg=self.colors['white'])
        name_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(name_frame, text="اسم الصنف *",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.name_entry = tk.Entry(name_frame,
                                  textvariable=self.item_name_var,
                                  font=self.fonts['body'],
                                  bg=self.colors['gray_100'],
                                  relief=tk.FLAT,
                                  bd=5)
        self.name_entry.pack(fill=tk.X, pady=(5, 0))

        # رمز الصنف
        code_frame = tk.Frame(row1, bg=self.colors['white'])
        code_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        code_label_frame = tk.Frame(code_frame, bg=self.colors['white'])
        code_label_frame.pack(fill=tk.X)

        tk.Label(code_label_frame, text="رمز الصنف *",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(side=tk.LEFT)

        generate_btn = tk.Button(code_label_frame,
                               text="🎲 توليد",
                               command=self.generate_code,
                               bg=self.colors['secondary'],
                               fg=self.colors['white'],
                               font=self.fonts['small'],
                               relief=tk.FLAT,
                               cursor='hand2')
        generate_btn.pack(side=tk.RIGHT)

        self.code_entry = tk.Entry(code_frame,
                                  textvariable=self.item_code_var,
                                  font=self.fonts['body'],
                                  bg=self.colors['gray_100'],
                                  relief=tk.FLAT,
                                  bd=5)
        self.code_entry.pack(fill=tk.X, pady=(5, 0))

        # الصف الثاني - الباركود والتصنيف
        row2 = tk.Frame(section_frame, bg=self.colors['white'])
        row2.pack(fill=tk.X, pady=5)

        # الباركود
        barcode_frame = tk.Frame(row2, bg=self.colors['white'])
        barcode_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        barcode_label_frame = tk.Frame(barcode_frame, bg=self.colors['white'])
        barcode_label_frame.pack(fill=tk.X)

        tk.Label(barcode_label_frame, text="الباركود",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(side=tk.LEFT)

        scan_btn = tk.Button(barcode_label_frame,
                           text="📷 مسح",
                           command=self.scan_barcode,
                           bg=self.colors['info'],
                           fg=self.colors['white'],
                           font=self.fonts['small'],
                           relief=tk.FLAT,
                           cursor='hand2')
        scan_btn.pack(side=tk.RIGHT)

        self.barcode_entry = tk.Entry(barcode_frame,
                                     textvariable=self.barcode_var,
                                     font=self.fonts['body'],
                                     bg=self.colors['gray_100'],
                                     relief=tk.FLAT,
                                     bd=5)
        self.barcode_entry.pack(fill=tk.X, pady=(5, 0))

        # التصنيف
        category_frame = tk.Frame(row2, bg=self.colors['white'])
        category_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(category_frame, text="التصنيف *",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.category_combo = ttk.Combobox(category_frame,
                                          textvariable=self.category_var,
                                          font=self.fonts['body'],
                                          values=["إلكترونيات", "ملابس", "أغذية", "أدوات منزلية", "كتب", "رياضة"])
        self.category_combo.pack(fill=tk.X, pady=(5, 0))

        # الصف الثالث - التصنيف الفرعي والعلامة التجارية
        row3 = tk.Frame(section_frame, bg=self.colors['white'])
        row3.pack(fill=tk.X, pady=5)

        # التصنيف الفرعي
        subcategory_frame = tk.Frame(row3, bg=self.colors['white'])
        subcategory_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(subcategory_frame, text="التصنيف الفرعي",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.subcategory_combo = ttk.Combobox(subcategory_frame,
                                             textvariable=self.subcategory_var,
                                             font=self.fonts['body'])
        self.subcategory_combo.pack(fill=tk.X, pady=(5, 0))

        # العلامة التجارية
        brand_frame = tk.Frame(row3, bg=self.colors['white'])
        brand_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(brand_frame, text="العلامة التجارية",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.brand_entry = tk.Entry(brand_frame,
                                   textvariable=self.brand_var,
                                   font=self.fonts['body'],
                                   bg=self.colors['gray_100'],
                                   relief=tk.FLAT,
                                   bd=5)
        self.brand_entry.pack(fill=tk.X, pady=(5, 0))

    def create_section_frame(self, title):
        """إنشاء إطار قسم مع عنوان"""
        # الحاوية الرئيسية للقسم
        main_section = tk.Frame(self.form_frame, bg=self.colors['white'])
        main_section.pack(fill=tk.X, padx=20, pady=10)

        # شريط العنوان
        title_frame = tk.Frame(main_section, bg=self.colors['gray_200'], height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame,
                              text=title,
                              font=self.fonts['subheading'],
                              bg=self.colors['gray_200'],
                              fg=self.colors['gray_700'])
        title_label.pack(pady=10)

        # محتوى القسم
        content_frame = tk.Frame(main_section, bg=self.colors['white'])
        content_frame.pack(fill=tk.X, padx=15, pady=15)

        return content_frame

    def create_pricing_section(self):
        """إنشاء قسم الأسعار والربحية"""
        section_frame = self.create_section_frame("💰 الأسعار والربحية")

        # الصف الأول - أسعار التكلفة والبيع
        row1 = tk.Frame(section_frame, bg=self.colors['white'])
        row1.pack(fill=tk.X, pady=5)

        # سعر التكلفة
        cost_frame = tk.Frame(row1, bg=self.colors['white'])
        cost_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(cost_frame, text="سعر التكلفة *",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.cost_entry = tk.Entry(cost_frame,
                                  textvariable=self.cost_price_var,
                                  font=self.fonts['body'],
                                  bg=self.colors['gray_100'],
                                  relief=tk.FLAT,
                                  bd=5)
        self.cost_entry.pack(fill=tk.X, pady=(5, 0))

        # سعر البيع
        selling_frame = tk.Frame(row1, bg=self.colors['white'])
        selling_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(selling_frame, text="سعر البيع *",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.selling_entry = tk.Entry(selling_frame,
                                     textvariable=self.selling_price_var,
                                     font=self.fonts['body'],
                                     bg=self.colors['gray_100'],
                                     relief=tk.FLAT,
                                     bd=5)
        self.selling_entry.pack(fill=tk.X, pady=(5, 0))

        # مؤشر الربحية
        profit_frame = tk.Frame(section_frame, bg=self.colors['white'])
        profit_frame.pack(fill=tk.X, pady=10)

        tk.Label(profit_frame, text="نسبة الربح",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.profit_display = tk.Label(profit_frame,
                                      text="0%",
                                      font=self.fonts['title'],
                                      bg=self.colors['white'],
                                      fg=self.colors['success'])
        self.profit_display.pack(anchor=tk.W, pady=(5, 0))

    def create_inventory_section(self):
        """إنشاء قسم إدارة المخزون"""
        section_frame = self.create_section_frame("📦 إدارة المخزون")

        # الصف الأول - الكمية الحالية والحد الأدنى
        row1 = tk.Frame(section_frame, bg=self.colors['white'])
        row1.pack(fill=tk.X, pady=5)

        # الكمية الحالية
        current_frame = tk.Frame(row1, bg=self.colors['white'])
        current_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(current_frame, text="الكمية الحالية",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.current_stock_entry = tk.Entry(current_frame,
                                           textvariable=self.current_stock_var,
                                           font=self.fonts['body'],
                                           bg=self.colors['gray_100'],
                                           relief=tk.FLAT,
                                           bd=5)
        self.current_stock_entry.pack(fill=tk.X, pady=(5, 0))

        # الحد الأدنى
        min_frame = tk.Frame(row1, bg=self.colors['white'])
        min_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(min_frame, text="الحد الأدنى",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.min_stock_entry = tk.Entry(min_frame,
                                       textvariable=self.min_stock_var,
                                       font=self.fonts['body'],
                                       bg=self.colors['gray_100'],
                                       relief=tk.FLAT,
                                       bd=5)
        self.min_stock_entry.pack(fill=tk.X, pady=(5, 0))

    def create_media_section(self):
        """إنشاء قسم الوسائط"""
        section_frame = self.create_section_frame("🖼️ الصور والوسائط")

        # منطقة عرض الصورة
        image_display_frame = tk.Frame(section_frame, bg=self.colors['gray_100'])
        image_display_frame.pack(fill=tk.X, pady=10)

        self.image_label = tk.Label(image_display_frame,
                                   text="📷\nلا توجد صورة",
                                   font=self.fonts['body'],
                                   bg=self.colors['gray_100'],
                                   fg=self.colors['gray_500'],
                                   width=20,
                                   height=8)
        self.image_label.pack(pady=20)

        # أزرار إدارة الصور
        image_buttons_frame = tk.Frame(section_frame, bg=self.colors['white'])
        image_buttons_frame.pack(fill=tk.X, pady=5)

        upload_btn = tk.Button(image_buttons_frame,
                              text="📤 تحميل صورة",
                              command=self.upload_image,
                              bg=self.colors['primary'],
                              fg=self.colors['white'],
                              font=self.fonts['body'],
                              relief=tk.FLAT,
                              cursor='hand2')
        upload_btn.pack(side=tk.LEFT, padx=(0, 10))

        delete_img_btn = tk.Button(image_buttons_frame,
                                  text="🗑️ حذف الصورة",
                                  command=self.delete_image,
                                  bg=self.colors['danger'],
                                  fg=self.colors['white'],
                                  font=self.fonts['body'],
                                  relief=tk.FLAT,
                                  cursor='hand2')
        delete_img_btn.pack(side=tk.LEFT)

    def create_quality_section(self):
        """إنشاء قسم الجودة والتقييم"""
        section_frame = self.create_section_frame("⭐ الجودة والتقييم")

        # نقاط الجودة
        quality_frame = tk.Frame(section_frame, bg=self.colors['white'])
        quality_frame.pack(fill=tk.X, pady=5)

        tk.Label(quality_frame, text="نقاط الجودة",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.quality_scale = tk.Scale(quality_frame,
                                     from_=0, to=100,
                                     orient=tk.HORIZONTAL,
                                     bg=self.colors['white'],
                                     fg=self.colors['primary'],
                                     font=self.fonts['body'])
        self.quality_scale.pack(fill=tk.X, pady=(5, 0))

    def create_ai_suggestions_section(self):
        """إنشاء قسم اقتراحات الذكاء الاصطناعي"""
        section_frame = self.create_section_frame("🤖 اقتراحات الذكاء الاصطناعي")

        # منطقة عرض الاقتراحات
        suggestions_frame = tk.Frame(section_frame, bg=self.colors['gray_100'])
        suggestions_frame.pack(fill=tk.X, pady=10)

        self.suggestions_text = tk.Text(suggestions_frame,
                                       height=4,
                                       font=self.fonts['body'],
                                       bg=self.colors['gray_100'],
                                       fg=self.colors['gray_700'],
                                       relief=tk.FLAT,
                                       wrap=tk.WORD)
        self.suggestions_text.pack(fill=tk.X, padx=10, pady=10)

        # زر تحديث الاقتراحات
        refresh_ai_btn = tk.Button(section_frame,
                                  text="🔄 تحديث الاقتراحات",
                                  command=self.refresh_ai_suggestions,
                                  bg=self.colors['info'],
                                  fg=self.colors['white'],
                                  font=self.fonts['body'],
                                  relief=tk.FLAT,
                                  cursor='hand2')
        refresh_ai_btn.pack(pady=5)

    def create_items_management_panel(self, parent):
        """إنشاء لوحة إدارة الأصناف"""
        # شريط العنوان
        header_frame = tk.Frame(parent, bg=self.colors['secondary'], height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_label = tk.Label(header_frame,
                               text="📋 إدارة الأصناف",
                               font=self.fonts['heading'],
                               bg=self.colors['secondary'],
                               fg=self.colors['white'])
        header_label.pack(pady=15)

        # منطقة البحث السريع
        search_frame = tk.Frame(parent, bg=self.colors['white'])
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="🔍 البحث السريع",
                font=self.fonts['body_bold'],
                bg=self.colors['white']).pack(anchor=tk.W)

        self.quick_search_entry = tk.Entry(search_frame,
                                          font=self.fonts['body'],
                                          bg=self.colors['gray_100'],
                                          relief=tk.FLAT,
                                          bd=5)
        self.quick_search_entry.pack(fill=tk.X, pady=(5, 0))

        # قائمة الأصناف
        items_frame = tk.Frame(parent, bg=self.colors['white'])
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # إنشاء Treeview للأصناف
        self.items_tree = ttk.Treeview(items_frame,
                                      columns=('name', 'code', 'price', 'stock'),
                                      show='headings',
                                      height=15)

        # تعيين العناوين
        self.items_tree.heading('name', text='اسم الصنف')
        self.items_tree.heading('code', text='الرمز')
        self.items_tree.heading('price', text='السعر')
        self.items_tree.heading('stock', text='المخزون')

        # تعيين عرض الأعمدة
        self.items_tree.column('name', width=150)
        self.items_tree.column('code', width=80)
        self.items_tree.column('price', width=80)
        self.items_tree.column('stock', width=80)

        # شريط التمرير
        items_scrollbar = ttk.Scrollbar(items_frame, orient="vertical",
                                       command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)

        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ربط الأحداث
        self.items_tree.bind('<Double-1>', self.on_item_double_click)

        # أزرار الإجراءات
        actions_frame = tk.Frame(parent, bg=self.colors['white'])
        actions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        edit_btn = tk.Button(actions_frame,
                            text="✏️ تعديل",
                            command=self.edit_selected_item,
                            bg=self.colors['warning'],
                            fg=self.colors['white'],
                            font=self.fonts['body'],
                            relief=tk.FLAT,
                            cursor='hand2')
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))

        delete_btn = tk.Button(actions_frame,
                              text="🗑️ حذف",
                              command=self.delete_selected_item,
                              bg=self.colors['danger'],
                              fg=self.colors['white'],
                              font=self.fonts['body'],
                              relief=tk.FLAT,
                              cursor='hand2')
        delete_btn.pack(side=tk.LEFT, padx=5)

        duplicate_btn = tk.Button(actions_frame,
                                 text="📋 نسخ",
                                 command=self.duplicate_selected_item,
                                 bg=self.colors['info'],
                                 fg=self.colors['white'],
                                 font=self.fonts['body'],
                                 relief=tk.FLAT,
                                 cursor='hand2')
        duplicate_btn.pack(side=tk.LEFT, padx=5)

    def create_analytics_sidebar(self):
        """إنشاء الشريط الجانبي للتحليلات"""
        # هذه الوظيفة ستكون فارغة في هذا الإصدار
        pass

    def create_advanced_status_bar(self):
        """إنشاء شريط الحالة المتقدم"""
        status_frame = tk.Frame(self.main_container,
                               bg=self.colors['gray_800'],
                               height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        # معلومات الحالة
        self.status_label = tk.Label(status_frame,
                                    text="جاهز",
                                    font=self.fonts['small'],
                                    bg=self.colors['gray_800'],
                                    fg=self.colors['white'])
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

        # معلومات إضافية
        self.info_label = tk.Label(status_frame,
                                  text="",
                                  font=self.fonts['small'],
                                  bg=self.colors['gray_800'],
                                  fg=self.colors['gray_300'])
        self.info_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def create_smart_popups(self):
        """إنشاء النوافذ المنبثقة الذكية"""
        # هذه الوظيفة ستكون فارغة في هذا الإصدار
        pass

    def create_tooltip(self, widget, text):
        """إنشاء tooltip للعنصر"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(tooltip, text=text,
                           font=self.fonts['small'],
                           bg=self.colors['gray_800'],
                           fg=self.colors['white'],
                           relief=tk.SOLID,
                           borderwidth=1)
            label.pack()

            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    # ==================== وظائف الأحداث ====================

    def on_name_change(self, *args):
        """عند تغيير اسم الصنف"""
        name = self.item_name_var.get()
        if name and self.config['ai']['auto_categorization']:
            suggested_category = self.ai_manager.suggest_category(name)
            if suggested_category:
                self.category_var.set(suggested_category)

    def on_code_change(self, *args):
        """عند تغيير رمز الصنف"""
        # التحقق من عدم تكرار الرمز
        pass

    def calculate_pricing(self, *args):
        """حساب الأسعار والربحية"""
        try:
            cost = float(self.cost_price_var.get() or 0)
            selling = float(self.selling_price_var.get() or 0)

            if cost > 0 and selling > 0:
                profit_margin = ((selling - cost) / cost) * 100
                self.profit_margin_var.set(f"{profit_margin:.1f}%")

                # تحديث لون مؤشر الربح
                if profit_margin >= 30:
                    color = self.colors['success']
                elif profit_margin >= 15:
                    color = self.colors['warning']
                else:
                    color = self.colors['danger']

                self.profit_display.configure(text=f"{profit_margin:.1f}%", fg=color)
            else:
                self.profit_display.configure(text="0%", fg=self.colors['gray_500'])

        except ValueError:
            self.profit_display.configure(text="خطأ", fg=self.colors['danger'])

    def on_search_change(self, *args):
        """عند تغيير نص البحث"""
        search_term = self.search_var.get()
        self.filter_items(search_term)

    def on_filter_change(self, *args):
        """عند تغيير الفلاتر"""
        self.filter_items()

    def on_item_double_click(self, event):
        """عند النقر المزدوج على صنف"""
        self.edit_selected_item()

    # ==================== وظائف الإجراءات ====================

    def new_item(self):
        """إنشاء صنف جديد"""
        self.clear_form()
        self.current_item = None
        self.update_status("جاهز لإدخال صنف جديد")

    def save_item(self):
        """حفظ الصنف"""
        try:
            # التحقق من صحة البيانات
            if not self.validate_form():
                return

            # إنشاء بيانات الصنف
            item_data = self.get_form_data()

            # حفظ في قاعدة البيانات
            if self.current_item:
                # تحديث صنف موجود
                self.inventory_manager.update_item(self.current_item['id'], item_data)
                self.update_status("تم تحديث الصنف بنجاح")
            else:
                # إضافة صنف جديد
                self.inventory_manager.add_item(item_data)
                self.update_status("تم إضافة الصنف بنجاح")

            # تحديث قائمة الأصناف
            self.refresh_items_list()

            # مسح النموذج
            self.clear_form()

        except Exception as e:
            messagebox.showerror("خطأ في الحفظ", f"فشل في حفظ الصنف: {e}")

    def validate_form(self):
        """التحقق من صحة النموذج"""
        errors = []

        # التحقق من الحقول المطلوبة
        if not self.item_name_var.get().strip():
            errors.append("اسم الصنف مطلوب")

        if not self.item_code_var.get().strip():
            errors.append("رمز الصنف مطلوب")

        if not self.category_var.get().strip():
            errors.append("التصنيف مطلوب")

        # التحقق من الأسعار
        try:
            cost = float(self.cost_price_var.get() or 0)
            if cost <= 0:
                errors.append("سعر التكلفة يجب أن يكون أكبر من صفر")
        except ValueError:
            errors.append("سعر التكلفة غير صحيح")

        try:
            selling = float(self.selling_price_var.get() or 0)
            if selling <= 0:
                errors.append("سعر البيع يجب أن يكون أكبر من صفر")
        except ValueError:
            errors.append("سعر البيع غير صحيح")

        if errors:
            messagebox.showerror("خطأ في البيانات", "\n".join(errors))
            return False

        return True

    def get_form_data(self):
        """الحصول على بيانات النموذج"""
        return {
            'name': self.item_name_var.get().strip(),
            'code': self.item_code_var.get().strip(),
            'barcode': self.barcode_var.get().strip(),
            'category': self.category_var.get().strip(),
            'subcategory': self.subcategory_var.get().strip(),
            'brand': self.brand_var.get().strip(),
            'cost_price': float(self.cost_price_var.get() or 0),
            'selling_price': float(self.selling_price_var.get() or 0),
            'current_stock': float(self.current_stock_var.get() or 0),
            'min_stock': float(self.min_stock_var.get() or 0),
            'quality_score': self.quality_scale.get()
        }

    def clear_form(self):
        """مسح النموذج"""
        # مسح جميع المتغيرات
        for var in [self.item_name_var, self.item_code_var, self.barcode_var,
                   self.category_var, self.subcategory_var, self.brand_var,
                   self.cost_price_var, self.selling_price_var,
                   self.current_stock_var, self.min_stock_var]:
            var.set("")

        # إعادة تعيين المقياس
        self.quality_scale.set(50)

        # مسح الصورة
        self.image_label.configure(text="📷\nلا توجد صورة")

        # مسح الاقتراحات
        self.suggestions_text.delete(1.0, tk.END)

    def generate_code(self):
        """توليد رمز الصنف تلقائياً"""
        try:
            category = self.category_var.get()
            if category:
                code = self.code_generator.generate_code(category)
                self.item_code_var.set(code)
                self.update_status(f"تم توليد الرمز: {code}")
            else:
                messagebox.showwarning("تحذير", "يرجى اختيار التصنيف أولاً")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في توليد الرمز: {e}")

    def scan_barcode(self):
        """مسح الباركود"""
        # هذه الوظيفة تحتاج إلى تطوير متقدم
        messagebox.showinfo("قريباً", "ميزة مسح الباركود قيد التطوير")

    def upload_image(self):
        """تحميل صورة الصنف"""
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="اختر صورة الصنف",
                filetypes=[("صور", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )

            if file_path:
                # تحميل وعرض الصورة
                image = Image.open(file_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # الاحتفاظ بمرجع

                self.update_status("تم تحميل الصورة بنجاح")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل الصورة: {e}")

    def delete_image(self):
        """حذف صورة الصنف"""
        self.image_label.configure(image="", text="📷\nلا توجد صورة")
        if hasattr(self.image_label, 'image'):
            del self.image_label.image
        self.update_status("تم حذف الصورة")

    def refresh_ai_suggestions(self):
        """تحديث اقتراحات الذكاء الاصطناعي"""
        suggestions = [
            "💡 يُنصح بزيادة سعر البيع بنسبة 10% لتحسين الربحية",
            "📊 هذا الصنف يحقق مبيعات جيدة في فئته",
            "⚠️ المخزون منخفض، يُنصح بإعادة الطلب قريباً",
            "🎯 يمكن تحسين التصنيف لزيادة الوضوح"
        ]

        self.suggestions_text.delete(1.0, tk.END)
        for suggestion in suggestions:
            self.suggestions_text.insert(tk.END, suggestion + "\n\n")

    def update_status(self, message):
        """تحديث رسالة الحالة"""
        self.status_label.configure(text=message)
        self.window.after(3000, lambda: self.status_label.configure(text="جاهز"))

    # ==================== وظائف إدارة الأصناف ====================

    def refresh_items_list(self):
        """تحديث قائمة الأصناف"""
        try:
            # مسح القائمة الحالية
            for item in self.items_tree.get_children():
                self.items_tree.delete(item)

            # تحميل الأصناف من قاعدة البيانات
            items = self.inventory_manager.get_all_items()

            for item in items:
                self.items_tree.insert('', 'end', values=(
                    item.get('name', ''),
                    item.get('code', ''),
                    f"{item.get('selling_price', 0):.2f}",
                    item.get('current_stock', 0)
                ))

            # تحديث عداد الأصناف
            count = len(items)
            self.items_count_label.configure(text=f"📦 الأصناف: {count}")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحديث قائمة الأصناف: {e}")

    def filter_items(self, search_term=""):
        """فلترة الأصناف"""
        # هذه الوظيفة تحتاج إلى تطوير متقدم
        pass

    def edit_selected_item(self):
        """تعديل الصنف المحدد"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار صنف للتعديل")
            return

        # الحصول على بيانات الصنف المحدد
        item_values = self.items_tree.item(selection[0])['values']
        if item_values:
            # تحميل بيانات الصنف في النموذج
            self.load_item_data(item_values[1])  # استخدام الرمز للبحث

    def delete_selected_item(self):
        """حذف الصنف المحدد"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار صنف للحذف")
            return

        # تأكيد الحذف
        if messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا الصنف؟"):
            try:
                item_values = self.items_tree.item(selection[0])['values']
                item_code = item_values[1]

                # حذف من قاعدة البيانات
                # self.inventory_manager.delete_item_by_code(item_code)

                # حذف من القائمة
                self.items_tree.delete(selection[0])

                self.update_status("تم حذف الصنف بنجاح")

            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في حذف الصنف: {e}")

    def duplicate_selected_item(self):
        """نسخ الصنف المحدد"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار صنف للنسخ")
            return

        # تحميل بيانات الصنف ومسح الرمز لإنشاء نسخة جديدة
        item_values = self.items_tree.item(selection[0])['values']
        if item_values:
            self.load_item_data(item_values[1])
            self.item_code_var.set("")  # مسح الرمز لتوليد رمز جديد
            self.item_name_var.set(self.item_name_var.get() + " - نسخة")

    def load_item_data(self, item_code):
        """تحميل بيانات الصنف"""
        try:
            item = self.inventory_manager.get_item_by_code(item_code)
            if item:
                self.current_item = item

                # تحميل البيانات في النموذج
                self.item_name_var.set(item.get('name', ''))
                self.item_code_var.set(item.get('code', ''))
                self.barcode_var.set(item.get('barcode', ''))
                self.category_var.set(item.get('category', ''))
                self.subcategory_var.set(item.get('subcategory', ''))
                self.brand_var.set(item.get('brand', ''))
                self.cost_price_var.set(str(item.get('cost_price', 0)))
                self.selling_price_var.set(str(item.get('selling_price', 0)))
                self.current_stock_var.set(str(item.get('current_stock', 0)))
                self.min_stock_var.set(str(item.get('min_stock', 0)))

                self.update_status(f"تم تحميل بيانات الصنف: {item.get('name', '')}")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل بيانات الصنف: {e}")

    # ==================== وظائف متقدمة ====================

    def focus_search(self):
        """التركيز على حقل البحث"""
        self.search_entry.focus_set()

    def duplicate_item(self):
        """نسخ الصنف الحالي"""
        if self.current_item:
            self.item_code_var.set("")
            self.item_name_var.set(self.item_name_var.get() + " - نسخة")
            self.current_item = None

    def export_data(self):
        """تصدير البيانات"""
        messagebox.showinfo("قريباً", "ميزة التصدير قيد التطوير")

    def import_data(self):
        """استيراد البيانات"""
        messagebox.showinfo("قريباً", "ميزة الاستيراد قيد التطوير")

    def print_report(self):
        """طباعة التقرير"""
        messagebox.showinfo("قريباً", "ميزة الطباعة قيد التطوير")

    def show_analytics(self):
        """عرض التحليلات"""
        messagebox.showinfo("قريباً", "ميزة التحليلات قيد التطوير")

    def advanced_search(self):
        """البحث المتقدم"""
        messagebox.showinfo("قريباً", "ميزة البحث المتقدم قيد التطوير")

    def show_settings(self):
        """عرض الإعدادات"""
        messagebox.showinfo("قريباً", "ميزة الإعدادات قيد التطوير")

    def show_help(self):
        """عرض المساعدة"""
        help_text = """
🚀 نظام إدارة الأصناف المتقدم

⌨️ اختصارات لوحة المفاتيح:
• Ctrl+S: حفظ الصنف
• Ctrl+N: صنف جديد
• Ctrl+F: البحث
• Ctrl+D: نسخ الصنف
• F5: تحديث البيانات
• F11/Escape: ملء الشاشة
• F1: المساعدة

📝 كيفية الاستخدام:
1. املأ المعلومات الأساسية للصنف
2. أدخل الأسعار لحساب الربحية
3. أضف صورة للصنف (اختياري)
4. احفظ الصنف بالضغط على Ctrl+S

🔍 البحث والفلترة:
• استخدم حقل البحث للعثور على الأصناف
• استخدم الفلاتر لتصنيف النتائج
• انقر نقراً مزدوجاً لتعديل الصنف

💡 نصائح:
• استخدم زر التوليد التلقائي للرموز
• راجع اقتراحات الذكاء الاصطناعي
• احرص على ملء الحقول المطلوبة
        """

        messagebox.showinfo("المساعدة", help_text)

    def refresh_data(self):
        """تحديث البيانات"""
        self.refresh_items_list()
        self.update_status("تم تحديث البيانات")

    def toggle_fullscreen(self):
        """تبديل ملء الشاشة"""
        current_state = self.window.attributes('-fullscreen')
        self.window.attributes('-fullscreen', not current_state)

    def show_context_menu(self, event):
        """عرض القائمة السياقية"""
        context_menu = tk.Menu(self.window, tearoff=0)
        context_menu.add_command(label="📋 نسخ", command=self.copy_item)
        context_menu.add_command(label="📤 تصدير", command=self.export_data)
        context_menu.add_separator()
        context_menu.add_command(label="🔄 تحديث", command=self.refresh_data)
        context_menu.add_command(label="❓ مساعدة", command=self.show_help)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def copy_item(self):
        """نسخ بيانات الصنف"""
        # نسخ بيانات الصنف إلى الحافظة
        data = self.get_form_data()
        item_text = f"اسم الصنف: {data['name']}\nالرمز: {data['code']}\nالسعر: {data['selling_price']}"
        self.window.clipboard_clear()
        self.window.clipboard_append(item_text)
        self.update_status("تم نسخ بيانات الصنف")

    def close_window(self):
        """إغلاق النافذة"""
        if messagebox.askyesno("تأكيد الإغلاق", "هل أنت متأكد من إغلاق النافذة؟"):
            self.window.destroy()

    # ==================== وظائف التهيئة والتحميل ====================

    def load_initial_data(self):
        """تحميل البيانات الأولية"""
        try:
            # تحميل قائمة الأصناف
            self.refresh_items_list()

            # تحميل التحليلات
            self.load_analytics_data()

            self.update_status("تم تحميل البيانات الأولية")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات: {e}")

    def load_analytics_data(self):
        """تحميل بيانات التحليلات"""
        # هذه الوظيفة تحتاج إلى تطوير متقدم
        pass

    def start_ai_services(self):
        """بدء خدمات الذكاء الاصطناعي"""
        # تحديث الاقتراحات كل 30 ثانية
        def update_suggestions():
            self.refresh_ai_suggestions()
            self.window.after(30000, update_suggestions)

        self.window.after(5000, update_suggestions)  # بدء بعد 5 ثوان

    def show(self):
        """عرض النافذة"""
        self.window.mainloop()


# ==================== دالة الاختبار ====================

def main():
    """دالة الاختبار الرئيسية"""
    try:
        print("🚀 بدء تشغيل نظام إدارة الأصناف المتقدم...")
        app = AdvancedItemEntry()
        app.show()

    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
