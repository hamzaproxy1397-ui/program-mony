# -*- coding: utf-8 -*-
"""
نافذة إدخال الأصناف الاحترافية - Professional Item Entry Window
تصميم حديث ومتطور مع واجهة جمالية احترافية
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.inventory_manager import InventoryManager
from core.item_code_generator import ItemCodeGenerator
from core.validation_engine import ValidationEngine
from models.item_model import ItemModel


class ProfessionalItemEntry:
    """نافذة إدخال الأصناف الاحترافية"""
    
    def __init__(self, parent=None, item_id=None):
        self.parent = parent
        self.item_id = item_id
        self.window = None
        self.image_path = None
        self.current_item = None
        self.items_list = []

        # ألوان التصميم الحديث (تعريف مبكر)
        self.colors = {
            'primary': '#2c3e50',      # أزرق داكن
            'secondary': '#3498db',    # أزرق فاتح
            'accent': '#e74c3c',       # أحمر
            'success': '#27ae60',      # أخضر
            'warning': '#f39c12',      # برتقالي
            'light': '#ecf0f1',        # رمادي فاتح
            'dark': '#34495e',         # رمادي داكن
            'white': '#ffffff',        # أبيض
            'gradient_start': '#667eea', # بداية التدرج
            'gradient_end': '#764ba2',   # نهاية التدرج
            'hover': '#5dade2',        # لون التمرير
            'border': '#bdc3c7'        # لون الحدود
        }

        # خطوط التصميم
        self.fonts = {
            'title': ('Cairo', 20, 'bold'),
            'subtitle': ('Cairo', 14, 'bold'),
            'body': ('Cairo', 12),
            'small': ('Cairo', 10),
            'button': ('Cairo', 11, 'bold'),
            'icon': ('Segoe UI Emoji', 16)
        }

        # إنشاء النافذة
        self.create_window()

        # متغيرات النموذج (بعد إنشاء النافذة)
        self.item_name_var = tk.StringVar()
        self.item_code_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.cost_price_var = tk.StringVar()
        self.selling_price_var = tk.StringVar()
        self.profit_margin_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # تهيئة المدراء
        self.inventory_manager = InventoryManager()
        self.code_generator = ItemCodeGenerator()
        self.validator = ValidationEngine()

        self.setup_styles()
        self.create_layout()
        self.load_items_list()
        self.bind_events()
        
    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("🏪 إدارة الأصناف الاحترافية - نظام المحاسبة المتقدم")
        
        # ملء الشاشة بالكامل
        self.window.state('zoomed')
        self.window.configure(bg=self.colors['light'])
        
        # تمكين تغيير الحجم
        self.window.resizable(True, True)
        self.window.minsize(1200, 800)
        
        # جعل النافذة في المقدمة
        if self.parent:
            self.window.transient(self.parent)
            self.window.grab_set()
        
        # ربط مفاتيح التحكم
        self.bind_window_controls()
        
        # تركيز النافذة
        self.window.focus_set()
        
    def bind_window_controls(self):
        """ربط مفاتيح التحكم في النافذة"""
        self.window.bind('<F11>', self.toggle_fullscreen)
        self.window.bind('<Escape>', self.toggle_fullscreen)
        self.window.bind('<Control-s>', lambda e: self.save_item())
        self.window.bind('<Control-q>', lambda e: self.close_window())
        self.window.bind('<Control-n>', lambda e: self.new_item())
        self.window.bind('<Control-f>', lambda e: self.focus_search())
        
    def toggle_fullscreen(self, event=None):
        """التبديل بين ملء الشاشة والنافذة العادية"""
        current_state = self.window.state()
        if current_state == 'zoomed':
            self.window.state('normal')
            self.window.geometry("1200x900")
            self.center_window()
        else:
            self.window.state('zoomed')
            
    def center_window(self):
        """تمركز النافذة في الشاشة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """إعداد أنماط التصميم"""
        style = ttk.Style()
        
        # نمط الأزرار الحديث
        style.configure('Modern.TButton',
                       font=self.fonts['button'],
                       padding=(20, 10),
                       relief='flat')
        
        # نمط حقول الإدخال
        style.configure('Modern.TEntry',
                       font=self.fonts['body'],
                       padding=10,
                       relief='flat',
                       borderwidth=1)
        
        # نمط التسميات
        style.configure('Modern.TLabel',
                       font=self.fonts['body'],
                       background=self.colors['light'])
        
        # نمط العناوين
        style.configure('Title.TLabel',
                       font=self.fonts['title'],
                       background=self.colors['primary'],
                       foreground=self.colors['white'])
        
    def create_layout(self):
        """إنشاء التخطيط الرئيسي"""
        # الحاوية الرئيسية
        main_container = tk.Frame(self.window, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # شريط العنوان العلوي
        self.create_header(main_container)
        
        # المحتوى الرئيسي
        content_frame = tk.Frame(main_container, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # تقسيم المحتوى: يسار (70%) ويمين (30%)
        self.create_main_content(content_frame)
        
        # شريط الأزرار السفلي
        self.create_footer(main_container)
        
    def create_header(self, parent):
        """إنشاء شريط العنوان الاحترافي"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # إطار المحتوى
        content_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # الجانب الأيسر - العنوان والوصف
        left_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # العنوان الرئيسي
        title_text = "🏪 إدارة الأصناف الاحترافية" if not self.item_id else "✏️ تعديل الصنف"
        title_label = tk.Label(
            left_frame,
            text=title_text,
            font=self.fonts['title'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(anchor=tk.W)
        
        # الوصف
        desc_label = tk.Label(
            left_frame,
            text="إضافة وتعديل الأصناف بواجهة احترافية حديثة",
            font=self.fonts['body'],
            bg=self.colors['primary'],
            fg=self.colors['light']
        )
        desc_label.pack(anchor=tk.W, pady=(5, 0))
        
        # الجانب الأيمن - أزرار التحكم
        right_frame = tk.Frame(content_frame, bg=self.colors['primary'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # أزرار التحكم
        self.create_control_buttons(right_frame)
        
    def create_control_buttons(self, parent):
        """إنشاء أزرار التحكم في الشريط العلوي"""
        buttons_frame = tk.Frame(parent, bg=self.colors['primary'])
        buttons_frame.pack(side=tk.RIGHT, pady=10)
        
        # زر صنف جديد
        new_btn = tk.Button(
            buttons_frame,
            text="➕ جديد",
            command=self.new_item,
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        new_btn.pack(side=tk.LEFT, padx=5)
        
        # زر ملء الشاشة
        fullscreen_btn = tk.Button(
            buttons_frame,
            text="🔳 ملء الشاشة",
            command=self.toggle_fullscreen,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        fullscreen_btn.pack(side=tk.LEFT, padx=5)
        
        # زر المساعدة
        help_btn = tk.Button(
            buttons_frame,
            text="❓ مساعدة",
            command=self.show_help,
            bg=self.colors['warning'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        
    def create_main_content(self, parent):
        """إنشاء المحتوى الرئيسي"""
        # الجانب الأيسر - نموذج الإدخال (70%)
        left_panel = tk.Frame(parent, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # الجانب الأيمن - قائمة الأصناف (30%)
        right_panel = tk.Frame(parent, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.configure(width=400)
        right_panel.pack_propagate(False)
        
        # إنشاء محتوى كل جانب
        self.create_input_form(left_panel)
        self.create_items_list_panel(right_panel)
        
    def create_input_form(self, parent):
        """إنشاء نموذج الإدخال"""
        # شريط تمرير للنموذج
        canvas = tk.Canvas(parent, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # محتوى النموذج
        self.create_form_sections(scrollable_frame)
        
        # ربط عجلة الماوس
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_form_sections(self, parent):
        """إنشاء أقسام النموذج"""
        # قسم المعلومات الأساسية
        self.create_basic_info_section(parent)
        
        # قسم الأسعار والتكلفة
        self.create_pricing_section(parent)
        
        # قسم الصورة
        self.create_image_section(parent)
        
        # قسم الوصف
        self.create_description_section(parent)

    def create_section_header(self, parent, title, icon):
        """إنشاء رأس القسم"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=50)
        header_frame.pack(fill=tk.X, pady=(20, 0))
        header_frame.pack_propagate(False)

        # الأيقونة والعنوان
        content_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title_label = tk.Label(
            content_frame,
            text=f"{icon} {title}",
            font=self.fonts['subtitle'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(side=tk.LEFT)

        return header_frame

    def create_basic_info_section(self, parent):
        """إنشاء قسم المعلومات الأساسية"""
        # رأس القسم
        self.create_section_header(parent, "المعلومات الأساسية", "📋")

        # محتوى القسم
        section_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RIDGE, bd=1)
        section_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        # إطار المحتوى الداخلي
        content_frame = tk.Frame(section_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.X, padx=20, pady=20)

        # تكوين الشبكة
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(3, weight=1)

        # اسم الصنف
        tk.Label(content_frame, text="📝 اسم الصنف *:",
                font=self.fonts['body'], bg=self.colors['white']).grid(
                row=0, column=0, sticky=tk.W, pady=10, padx=(0, 10))

        self.item_name_entry = tk.Entry(
            content_frame,
            textvariable=self.item_name_var,
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=5,
            bg=self.colors['light']
        )
        self.item_name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=10, padx=(0, 20))

        # رمز الصنف
        tk.Label(content_frame, text="🔢 رمز الصنف *:",
                font=self.fonts['body'], bg=self.colors['white']).grid(
                row=0, column=2, sticky=tk.W, pady=10, padx=(0, 10))

        code_frame = tk.Frame(content_frame, bg=self.colors['white'])
        code_frame.grid(row=0, column=3, sticky=tk.W+tk.E, pady=10)
        code_frame.columnconfigure(0, weight=1)

        self.item_code_entry = tk.Entry(
            code_frame,
            textvariable=self.item_code_var,
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=5,
            bg=self.colors['light']
        )
        self.item_code_entry.grid(row=0, column=0, sticky=tk.W+tk.E, padx=(0, 10))

        # زر توليد الرمز
        generate_btn = tk.Button(
            code_frame,
            text="🎲",
            command=self.generate_code,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=self.fonts['icon'],
            relief=tk.FLAT,
            width=3,
            cursor='hand2'
        )
        generate_btn.grid(row=0, column=1)

        # التصنيف
        tk.Label(content_frame, text="📂 التصنيف:",
                font=self.fonts['body'], bg=self.colors['white']).grid(
                row=1, column=0, sticky=tk.W, pady=10, padx=(0, 10))

        self.category_combo = ttk.Combobox(
            content_frame,
            textvariable=self.category_var,
            font=self.fonts['body'],
            values=["إلكترونيات", "ملابس", "أغذية", "مكتبية", "منزلية", "أخرى"]
        )
        self.category_combo.grid(row=1, column=1, sticky=tk.W+tk.E, pady=10, padx=(0, 20))

        # الوحدة
        tk.Label(content_frame, text="📏 الوحدة:",
                font=self.fonts['body'], bg=self.colors['white']).grid(
                row=1, column=2, sticky=tk.W, pady=10, padx=(0, 10))

        self.unit_combo = ttk.Combobox(
            content_frame,
            textvariable=self.unit_var,
            font=self.fonts['body'],
            values=["قطعة", "كيلو", "متر", "لتر", "علبة", "كرتون", "دزينة"]
        )
        self.unit_combo.grid(row=1, column=3, sticky=tk.W+tk.E, pady=10)

    def create_pricing_section(self, parent):
        """إنشاء قسم الأسعار والتكلفة"""
        # رأس القسم
        self.create_section_header(parent, "الأسعار والربحية", "💰")

        # محتوى القسم
        section_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RIDGE, bd=1)
        section_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        # إطار المحتوى الداخلي
        content_frame = tk.Frame(section_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.X, padx=20, pady=20)

        # تكوين الشبكة
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(3, weight=1)
        content_frame.columnconfigure(5, weight=1)

        # سعر التكلفة
        tk.Label(content_frame, text="💸 سعر التكلفة:",
                font=self.fonts['body'], bg=self.colors['white']).grid(
                row=0, column=0, sticky=tk.W, pady=10, padx=(0, 10))

        self.cost_price_entry = tk.Entry(
            content_frame,
            textvariable=self.cost_price_var,
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=5,
            bg=self.colors['light']
        )
        self.cost_price_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=10, padx=(0, 20))
        self.cost_price_entry.bind('<KeyRelease>', self.calculate_profit)

        # سعر البيع
        tk.Label(content_frame, text="💵 سعر البيع:",
                font=self.fonts['body'], bg=self.colors['white']).grid(
                row=0, column=2, sticky=tk.W, pady=10, padx=(0, 10))

        self.selling_price_entry = tk.Entry(
            content_frame,
            textvariable=self.selling_price_var,
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=5,
            bg=self.colors['light']
        )
        self.selling_price_entry.grid(row=0, column=3, sticky=tk.W+tk.E, pady=10, padx=(0, 20))
        self.selling_price_entry.bind('<KeyRelease>', self.calculate_profit)

        # نسبة الربح
        tk.Label(content_frame, text="📈 نسبة الربح:",
                font=self.fonts['body'], bg=self.colors['white']).grid(
                row=0, column=4, sticky=tk.W, pady=10, padx=(0, 10))

        self.profit_margin_label = tk.Label(
            content_frame,
            textvariable=self.profit_margin_var,
            font=self.fonts['subtitle'],
            bg=self.colors['success'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.profit_margin_label.grid(row=0, column=5, sticky=tk.W+tk.E, pady=10)

    def create_image_section(self, parent):
        """إنشاء قسم الصورة"""
        # رأس القسم
        self.create_section_header(parent, "صورة الصنف", "🖼️")

        # محتوى القسم
        section_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RIDGE, bd=1)
        section_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        # إطار المحتوى الداخلي
        content_frame = tk.Frame(section_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.X, padx=20, pady=20)

        # إطار الصورة
        image_frame = tk.Frame(content_frame, bg=self.colors['light'], relief=tk.SUNKEN, bd=2)
        image_frame.pack(side=tk.LEFT, padx=(0, 20))

        # عرض الصورة
        self.image_label = tk.Label(
            image_frame,
            text="📷\nلا توجد صورة\nانقر لإضافة صورة",
            font=self.fonts['body'],
            bg=self.colors['light'],
            fg=self.colors['dark'],
            width=20,
            height=10,
            cursor='hand2'
        )
        self.image_label.pack(padx=10, pady=10)
        self.image_label.bind('<Button-1>', self.upload_image)

        # أزرار الصورة
        buttons_frame = tk.Frame(content_frame, bg=self.colors['white'])
        buttons_frame.pack(side=tk.LEFT, fill=tk.Y)

        # زر تحميل صورة
        upload_btn = tk.Button(
            buttons_frame,
            text="📁 تحميل صورة",
            command=self.upload_image,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        upload_btn.pack(pady=5, fill=tk.X)

        # زر حذف صورة
        delete_img_btn = tk.Button(
            buttons_frame,
            text="🗑️ حذف صورة",
            command=self.delete_image,
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        delete_img_btn.pack(pady=5, fill=tk.X)

    def create_description_section(self, parent):
        """إنشاء قسم الوصف"""
        # رأس القسم
        self.create_section_header(parent, "وصف الصنف", "📝")

        # محتوى القسم
        section_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RIDGE, bd=1)
        section_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        # إطار المحتوى الداخلي
        content_frame = tk.Frame(section_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.X, padx=20, pady=20)

        # حقل الوصف
        self.description_text = tk.Text(
            content_frame,
            font=self.fonts['body'],
            height=4,
            relief=tk.FLAT,
            bd=5,
            bg=self.colors['light'],
            wrap=tk.WORD
        )
        self.description_text.pack(fill=tk.X)

    def create_items_list_panel(self, parent):
        """إنشاء لوحة قائمة الأصناف"""
        # رأس اللوحة
        header_frame = tk.Frame(parent, bg=self.colors['dark'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # عنوان اللوحة
        title_label = tk.Label(
            header_frame,
            text="📦 قائمة الأصناف",
            font=self.fonts['subtitle'],
            bg=self.colors['dark'],
            fg=self.colors['white']
        )
        title_label.pack(pady=15)

        # شريط البحث
        search_frame = tk.Frame(parent, bg=self.colors['white'])
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="🔍", font=self.fonts['icon'],
                bg=self.colors['white']).pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=5,
            bg=self.colors['light']
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.filter_items)

        # قائمة الأصناف
        list_frame = tk.Frame(parent, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # شريط تمرير للقائمة
        list_canvas = tk.Canvas(list_frame, bg=self.colors['white'])
        list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=list_canvas.yview)
        self.items_list_frame = tk.Frame(list_canvas, bg=self.colors['white'])

        self.items_list_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )

        list_canvas.create_window((0, 0), window=self.items_list_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=list_scrollbar.set)

        list_canvas.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")

        # ربط عجلة الماوس للقائمة
        def _on_list_mousewheel(event):
            list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        list_canvas.bind_all("<MouseWheel>", _on_list_mousewheel)

    def create_footer(self, parent):
        """إنشاء شريط الأزرار السفلي"""
        footer_frame = tk.Frame(parent, bg=self.colors['light'], height=80)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        # إطار الأزرار
        buttons_frame = tk.Frame(footer_frame, bg=self.colors['light'])
        buttons_frame.pack(expand=True, pady=20)

        # زر الحفظ
        save_btn = tk.Button(
            buttons_frame,
            text="💾 حفظ الصنف",
            command=self.save_item,
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=10)

        # زر الإلغاء
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ إلغاء",
            command=self.clear_form,
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # زر الإغلاق
        close_btn = tk.Button(
            buttons_frame,
            text="🚪 إغلاق",
            command=self.close_window,
            bg=self.colors['dark'],
            fg=self.colors['white'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        close_btn.pack(side=tk.LEFT, padx=10)

    def bind_events(self):
        """ربط الأحداث"""
        # ربط أحداث التحقق
        self.item_name_var.trace('w', self.validate_form)
        self.item_code_var.trace('w', self.validate_form)

    def generate_code(self):
        """توليد رمز الصنف تلقائياً"""
        try:
            category = self.category_var.get() or "عام"
            code = self.code_generator.generate_code(category)
            self.item_code_var.set(code)
            print(f"✅ تم توليد الرمز: {code}")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في توليد الرمز: {e}")

    def calculate_profit(self, event=None):
        """حساب نسبة الربح"""
        try:
            cost = float(self.cost_price_var.get() or 0)
            selling = float(self.selling_price_var.get() or 0)

            if cost > 0 and selling > 0:
                profit = ((selling - cost) / cost) * 100
                self.profit_margin_var.set(f"{profit:.1f}%")

                # تغيير لون المؤشر حسب الربحية
                if profit > 30:
                    self.profit_margin_label.configure(bg=self.colors['success'])
                elif profit > 15:
                    self.profit_margin_label.configure(bg=self.colors['warning'])
                else:
                    self.profit_margin_label.configure(bg=self.colors['accent'])
            else:
                self.profit_margin_var.set("0.0%")
                self.profit_margin_label.configure(bg=self.colors['dark'])

        except ValueError:
            self.profit_margin_var.set("غير صحيح")
            self.profit_margin_label.configure(bg=self.colors['accent'])

    def upload_image(self, event=None):
        """تحميل صورة الصنف"""
        try:
            file_path = filedialog.askopenfilename(
                title="اختر صورة الصنف",
                filetypes=[
                    ("صور", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("جميع الملفات", "*.*")
                ]
            )

            if file_path:
                # تحميل وعرض الصورة
                image = Image.open(file_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # حفظ مرجع للصورة
                self.image_path = file_path

                print(f"✅ تم تحميل الصورة: {file_path}")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل الصورة: {e}")

    def delete_image(self):
        """حذف صورة الصنف"""
        self.image_label.configure(
            image="",
            text="📷\nلا توجد صورة\nانقر لإضافة صورة"
        )
        self.image_label.image = None
        self.image_path = None
        print("🗑️ تم حذف الصورة")

    def validate_form(self, *args):
        """التحقق من صحة النموذج"""
        # يمكن إضافة منطق التحقق هنا
        pass

    def load_items_list(self):
        """تحميل قائمة الأصناف"""
        try:
            # مسح القائمة الحالية
            for widget in self.items_list_frame.winfo_children():
                widget.destroy()

            # تحميل الأصناف من قاعدة البيانات
            items = self.inventory_manager.get_all_items()
            self.items_list = items

            # عرض الأصناف
            for i, item in enumerate(items):
                self.create_item_card(item, i)

        except Exception as e:
            print(f"خطأ في تحميل الأصناف: {e}")

    def create_item_card(self, item, index):
        """إنشاء بطاقة صنف في القائمة"""
        # إطار البطاقة
        card_frame = tk.Frame(
            self.items_list_frame,
            bg=self.colors['white'],
            relief=tk.RIDGE,
            bd=1
        )
        card_frame.pack(fill=tk.X, pady=5, padx=5)

        # لون خلفية متناوب
        bg_color = self.colors['light'] if index % 2 == 0 else self.colors['white']
        card_frame.configure(bg=bg_color)

        # محتوى البطاقة
        content_frame = tk.Frame(card_frame, bg=bg_color)
        content_frame.pack(fill=tk.X, padx=10, pady=8)

        # اسم الصنف
        name_label = tk.Label(
            content_frame,
            text=item.get('name', 'غير محدد'),
            font=self.fonts['body'],
            bg=bg_color,
            anchor=tk.W
        )
        name_label.pack(fill=tk.X)

        # رمز الصنف
        code_label = tk.Label(
            content_frame,
            text=f"الرمز: {item.get('code', 'غير محدد')}",
            font=self.fonts['small'],
            bg=bg_color,
            fg=self.colors['dark'],
            anchor=tk.W
        )
        code_label.pack(fill=tk.X)

        # أزرار العمليات
        buttons_frame = tk.Frame(content_frame, bg=bg_color)
        buttons_frame.pack(fill=tk.X, pady=(5, 0))

        # زر التعديل
        edit_btn = tk.Button(
            buttons_frame,
            text="✏️",
            command=lambda: self.edit_item(item),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=self.fonts['small'],
            relief=tk.FLAT,
            width=3,
            cursor='hand2'
        )
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))

        # زر الحذف
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️",
            command=lambda: self.delete_item(item),
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=self.fonts['small'],
            relief=tk.FLAT,
            width=3,
            cursor='hand2'
        )
        delete_btn.pack(side=tk.LEFT)

    def filter_items(self, event=None):
        """فلترة الأصناف حسب البحث"""
        search_term = self.search_var.get().lower()

        # مسح القائمة الحالية
        for widget in self.items_list_frame.winfo_children():
            widget.destroy()

        # عرض الأصناف المفلترة
        filtered_items = []
        for item in self.items_list:
            if (search_term in item.get('name', '').lower() or
                search_term in item.get('code', '').lower()):
                filtered_items.append(item)

        for i, item in enumerate(filtered_items):
            self.create_item_card(item, i)

    def edit_item(self, item):
        """تعديل صنف موجود"""
        try:
            # تحميل بيانات الصنف في النموذج
            self.current_item = item
            self.item_id = item.get('id')

            self.item_name_var.set(item.get('name', ''))
            self.item_code_var.set(item.get('code', ''))
            self.category_var.set(item.get('category', ''))
            self.unit_var.set(item.get('unit', ''))
            self.cost_price_var.set(str(item.get('cost_price', '')))
            self.selling_price_var.set(str(item.get('selling_price', '')))

            # تحميل الوصف
            if hasattr(self, 'description_text'):
                self.description_text.delete(1.0, tk.END)
                self.description_text.insert(1.0, item.get('description', ''))

            # تحميل الصورة إذا وجدت
            image_path = item.get('image_path')
            if image_path and os.path.exists(image_path):
                self.load_item_image(image_path)

            # حساب الربح
            self.calculate_profit()

            print(f"📝 تم تحميل بيانات الصنف: {item.get('name')}")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل بيانات الصنف: {e}")

    def load_item_image(self, image_path):
        """تحميل صورة الصنف"""
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo
                self.image_path = image_path
        except Exception as e:
            print(f"خطأ في تحميل صورة الصنف: {e}")

    def delete_item(self, item):
        """حذف صنف"""
        try:
            result = messagebox.askyesno(
                "تأكيد الحذف",
                f"هل أنت متأكد من حذف الصنف '{item.get('name')}'؟\n"
                "هذا الإجراء لا يمكن التراجع عنه."
            )

            if result:
                # حذف من قاعدة البيانات
                self.inventory_manager.delete_item(item.get('id'))

                # إعادة تحميل القائمة
                self.load_items_list()

                # مسح النموذج إذا كان الصنف المحذوف محملاً
                if self.current_item and self.current_item.get('id') == item.get('id'):
                    self.clear_form()

                messagebox.showinfo("نجح", f"تم حذف الصنف '{item.get('name')}' بنجاح")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حذف الصنف: {e}")

    def save_item(self):
        """حفظ الصنف"""
        try:
            # التحقق من البيانات المطلوبة
            if not self.item_name_var.get().strip():
                messagebox.showerror("خطأ", "اسم الصنف مطلوب")
                self.item_name_entry.focus()
                return

            if not self.item_code_var.get().strip():
                messagebox.showerror("خطأ", "رمز الصنف مطلوب")
                self.item_code_entry.focus()
                return

            # إعداد بيانات الصنف
            item_data = {
                'name': self.item_name_var.get().strip(),
                'code': self.item_code_var.get().strip(),
                'category': self.category_var.get() or 'عام',
                'unit': self.unit_var.get() or 'قطعة',
                'cost_price': float(self.cost_price_var.get() or 0),
                'selling_price': float(self.selling_price_var.get() or 0),
                'description': self.description_text.get(1.0, tk.END).strip() if hasattr(self, 'description_text') else '',
                'image_path': self.image_path,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            # حفظ أو تحديث الصنف
            if self.item_id:
                # تحديث صنف موجود
                item_data['id'] = self.item_id
                self.inventory_manager.update_item(self.item_id, item_data)
                message = f"تم تحديث الصنف '{item_data['name']}' بنجاح"
            else:
                # إضافة صنف جديد
                self.inventory_manager.add_item(item_data)
                message = f"تم إضافة الصنف '{item_data['name']}' بنجاح"

            # إعادة تحميل القائمة
            self.load_items_list()

            # مسح النموذج
            self.clear_form()

            messagebox.showinfo("نجح", message)
            print(f"✅ {message}")

        except ValueError as e:
            messagebox.showerror("خطأ", "تأكد من صحة الأسعار المدخلة")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الصنف: {e}")

    def clear_form(self):
        """مسح النموذج"""
        self.item_id = None
        self.current_item = None

        # مسح المتغيرات
        self.item_name_var.set("")
        self.item_code_var.set("")
        self.category_var.set("")
        self.unit_var.set("")
        self.cost_price_var.set("")
        self.selling_price_var.set("")
        self.profit_margin_var.set("0.0%")

        # مسح الوصف
        if hasattr(self, 'description_text'):
            self.description_text.delete(1.0, tk.END)

        # مسح الصورة
        self.delete_image()

        print("🧹 تم مسح النموذج")

    def new_item(self):
        """إنشاء صنف جديد"""
        self.clear_form()
        self.item_name_entry.focus()

    def focus_search(self):
        """تركيز حقل البحث"""
        self.search_entry.focus()

    def show_help(self):
        """عرض المساعدة"""
        help_text = """
🏪 مساعدة نافذة إدارة الأصناف

⌨️ اختصارات لوحة المفاتيح:
• F11/Escape: تبديل ملء الشاشة
• Ctrl+S: حفظ الصنف
• Ctrl+N: صنف جديد
• Ctrl+F: البحث
• Ctrl+Q: إغلاق النافذة

📝 إرشادات الاستخدام:
• املأ اسم الصنف ورمزه (مطلوب)
• اختر التصنيف والوحدة
• أدخل الأسعار لحساب الربح تلقائياً
• أضف صورة ووصف (اختياري)
• استخدم البحث للعثور على الأصناف

💡 نصائح:
• استخدم زر 🎲 لتوليد رمز تلقائي
• نسبة الربح تتغير لونها حسب القيمة
• يمكن تعديل أو حذف الأصناف من القائمة
        """

        messagebox.showinfo("المساعدة", help_text)

    def close_window(self):
        """إغلاق النافذة"""
        if self.parent:
            self.window.grab_release()
        self.window.destroy()

    def show(self):
        """عرض النافذة"""
        self.window.mainloop()
