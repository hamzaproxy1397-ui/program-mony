#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 نافذة إدارة الموظفين الموحدة والمتطورة
Unified Advanced Employee Management Window

نافذة شاملة تجمع بين البساطة والتقدم التقني
تدمج جميع ميزات النظام الأساسي والمتقدم في واجهة واحدة موحدة
"""

import sys
import os
import sqlite3
import traceback
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, List, Any
import json

# Third-party imports
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

# Optional imports with fallbacks
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("تحذير: مكتبة PIL غير متوفرة - بعض الميزات قد لا تعمل")

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("تحذير: مكتبة matplotlib غير متوفرة - الرسوم البيانية غير متاحة")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("تحذير: مكتبة numpy غير متوفرة - بعض التحليلات المتقدمة غير متاحة")

# Local imports with safe fallbacks
try:
    from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS
    from config.settings import WINDOW_EMPLOYEES_SIZE
except ImportError:
    # Fallback colors and settings
    MODERN_COLORS = {
        'primary': '#2E8B57',
        'secondary': '#4682B4', 
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'background': '#f8f9fa',
        'card': '#ffffff',
        'text_primary': '#212529',
        'text_secondary': '#6c757d'
    }
    FONTS = {'arabic': 'Arial', 'sizes': {'normal': 12, 'large': 14}}
    DIMENSIONS = {'button_width': 150, 'button_height': 40}
    WINDOW_EMPLOYEES_SIZE = (1800, 950)

# ==================== إعدادات النافذة الموحدة ====================

# ألوان النظام الموحد
UNIFIED_COLORS = {
    # الألوان الأساسية
    'primary': '#2E8B57',           # أخضر أساسي
    'primary_light': '#3CB371',     # أخضر فاتح
    'primary_dark': '#1B5E20',      # أخضر غامق
    'secondary': '#4682B4',         # أزرق ثانوي
    'accent': '#FF6B35',            # برتقالي للتمييز
    
    # ألوان الحالة
    'success': '#28a745',           # أخضر النجاح
    'warning': '#ffc107',           # أصفر التحذير
    'danger': '#dc3545',            # أحمر الخطر
    'info': '#17a2b8',              # أزرق المعلومات
    
    # ألوان الخلفية
    'background': '#f8f9fa',        # خلفية رئيسية
    'card': '#ffffff',              # خلفية البطاقات
    'sidebar': '#e9ecef',           # خلفية الشريط الجانبي
    'header': '#343a40',            # خلفية الهيدر
    
    # ألوان النص
    'text_primary': '#212529',      # نص أساسي
    'text_secondary': '#6c757d',    # نص ثانوي
    'text_light': '#ffffff',        # نص فاتح
    'text_muted': '#adb5bd',        # نص خافت
    
    # ألوان التدرج
    'gradient_start': '#667eea',    # بداية التدرج
    'gradient_end': '#764ba2',      # نهاية التدرج
    
    # ألوان الظلال
    'shadow_light': '#f1f3f4',     # ظل فاتح
    'shadow_medium': '#e2e8f0',    # ظل متوسط
    'shadow_dark': '#cbd5e1',      # ظل غامق
}

# خطوط النظام الموحد
UNIFIED_FONTS = {
    'title_large': ('Arial', 24, 'bold'),      # عناوين كبيرة
    'title_medium': ('Arial', 18, 'bold'),     # عناوين متوسطة
    'title_small': ('Arial', 14, 'bold'),      # عناوين صغيرة
    'button_large': ('Arial', 14, 'bold'),     # أزرار كبيرة
    'button_medium': ('Arial', 12, 'bold'),    # أزرار متوسطة
    'text_large': ('Arial', 14),               # نص كبير
    'text_medium': ('Arial', 12),              # نص متوسط
    'text_small': ('Arial', 10),               # نص صغير
    'input': ('Arial', 12),                    # حقول الإدخال
    'table': ('Arial', 11),                    # جداول
}

# أبعاد النظام الموحد - محسن لملء الشاشة
UNIFIED_DIMENSIONS = {
    'window_width': 0,                          # سيتم تحديده ديناميكياً (ملء الشاشة)
    'window_height': 0,                         # سيتم تحديده ديناميكياً (ملء الشاشة)
    'min_width': 1200,                          # الحد الأدنى للعرض
    'min_height': 700,                          # الحد الأدنى للارتفاع
    'header_height': 80,                        # ارتفاع الهيدر
    'toolbar_height': 70,                       # ارتفاع شريط الأدوات
    'sidebar_width': 350,                       # عرض الشريط الجانبي (محسن)
    'button_width': 140,                        # عرض الأزرار
    'button_height': 40,                        # ارتفاع الأزرار
    'input_height': 35,                         # ارتفاع حقول الإدخال
    'corner_radius': 10,                        # زوايا مستديرة
    'padding': 15,                              # مسافة داخلية
    'margin': 10,                               # مسافة خارجية
}

# ==================== الكلاس الرئيسي للنافذة الموحدة ====================

class UnifiedEmployeesManagement:
    """نافذة إدارة الموظفين الموحدة والمتطورة"""
    
    def __init__(self, parent=None):
        """تهيئة النافذة الموحدة"""
        self.parent = parent
        self.window = None
        self.db_connection = None
        
        # متغيرات البيانات
        self.employees_data = []
        self.current_employee = None
        self.filtered_employees = []
        
        # متغيرات النموذج
        self.form_vars = {}
        
        # متغيرات البحث والفلترة (سيتم تهيئتها بعد إنشاء النافذة)
        self.search_var = None
        self.department_filter_var = None
        self.status_filter_var = None
        
        # عناصر الواجهة
        self.tree = None
        self.form_frame = None
        self.analytics_frame = None
        
        # إحصائيات
        self.stats = {
            'total_employees': 0,
            'active_employees': 0,
            'total_salary': 0,
            'avg_performance': 0
        }
        
        # تهيئة النافذة
        self.init_unified_system()
    
    def init_unified_system(self):
        """تهيئة النظام الموحد"""
        try:
            print("🚀 تهيئة نظام إدارة الموظفين الموحد...")
            
            # إنشاء النافذة
            self.create_unified_window()

            # تهيئة المتغيرات بعد إنشاء النافذة
            self.init_variables()

            # تهيئة قاعدة البيانات
            self.init_unified_database()

            # إنشاء نسخة احتياطية تلقائية
            self.auto_backup_database()
            
            # إنشاء الواجهة
            self.create_unified_interface()

            # تحميل البيانات بعد إنشاء الواجهة
            self.load_employees_data()

            # تحديث الإحصائيات
            self.update_statistics()

            # ربط الأحداث
            self.bind_events()
            
            print("✅ تم تهيئة النظام الموحد بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تهيئة النظام الموحد: {e}")
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في تهيئة النظام: {e}")
    
    def create_unified_window(self):
        """إنشاء النافذة الموحدة"""
        try:
            # إنشاء النافذة
            if self.parent:
                self.window = ctk.CTkToplevel(self.parent)
                self.window.transient(self.parent)
                self.window.grab_set()
            else:
                self.window = ctk.CTk()
            
            # تكوين النافذة لملء الشاشة
            self.window.title("🏢 نظام إدارة الموظفين الموحد والمتطور")

            # الحصول على أبعاد الشاشة
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            # تحديث الأبعاد في القاموس
            UNIFIED_DIMENSIONS['window_width'] = screen_width
            UNIFIED_DIMENSIONS['window_height'] = screen_height

            # تعيين النافذة لملء الشاشة مع إمكانية التصغير والتكبير
            self.window.geometry(f"{screen_width}x{screen_height}+0+0")
            self.window.minsize(UNIFIED_DIMENSIONS['min_width'], UNIFIED_DIMENSIONS['min_height'])
            self.window.configure(fg_color=UNIFIED_COLORS['background'])

            # تمكين إمكانية تغيير الحجم
            self.window.resizable(True, True)

            # تعيين النافذة لتكون في المقدمة
            self.window.lift()
            self.window.focus_force()
            
            # إعداد إغلاق النافذة
            self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء النافذة: {e}")
            raise
    
    def center_window(self):
        """إعداد النافذة لملء الشاشة أو تحميل الإعدادات المحفوظة"""
        try:
            # محاولة تحميل الإعدادات المحفوظة أولاً
            if self.load_window_settings():
                print("✅ تم تحميل إعدادات النافذة المحفوظة")
                return

            # إذا لم تكن هناك إعدادات محفوظة، ملء الشاشة
            self.window.update_idletasks()

            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            # تعيين النافذة لملء الشاشة
            self.window.geometry(f"{screen_width}x{screen_height}+0+0")

            print(f"✅ تم تعيين النافذة لملء الشاشة: {screen_width}x{screen_height}")

        except Exception as e:
            print(f"تحذير: فشل في إعداد النافذة: {e}")

    def maximize_window(self):
        """تكبير النافذة لملء الشاشة"""
        try:
            self.window.state('zoomed')  # Windows
        except:
            try:
                self.window.attributes('-zoomed', True)  # Linux
            except:
                # Mac أو أنظمة أخرى
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()
                self.window.geometry(f"{screen_width}x{screen_height}+0+0")

    def toggle_fullscreen(self):
        """تبديل وضع ملء الشاشة"""
        try:
            current_state = self.window.attributes('-fullscreen')
            self.window.attributes('-fullscreen', not current_state)
        except:
            # إذا لم يكن مدعوماً، استخدم التكبير العادي
            self.maximize_window()

    def init_variables(self):
        """تهيئة المتغيرات بعد إنشاء النافذة"""
        try:
            # التأكد من وجود النافذة قبل إنشاء المتغيرات
            if self.window:
                self.search_var = tk.StringVar(master=self.window)
                self.department_filter_var = tk.StringVar(master=self.window, value="الكل")
                self.status_filter_var = tk.StringVar(master=self.window, value="الكل")
                print("✅ تم تهيئة المتغيرات مع النافذة الرئيسية")
            else:
                print("❌ لا يمكن تهيئة المتغيرات - النافذة غير موجودة")
        except Exception as e:
            print(f"❌ خطأ في تهيئة المتغيرات: {e}")
            # محاولة إنشاء المتغيرات بدون master كبديل
            try:
                self.search_var = tk.StringVar()
                self.department_filter_var = tk.StringVar(value="الكل")
                self.status_filter_var = tk.StringVar(value="الكل")
                print("⚠️ تم إنشاء المتغيرات بدون master")
            except Exception as fallback_error:
                print(f"❌ فشل في إنشاء المتغيرات: {fallback_error}")
                # إنشاء متغيرات وهمية لتجنب الأخطاء
                self.search_var = None
                self.department_filter_var = None
                self.status_filter_var = None

    def init_unified_database(self):
        """تهيئة قاعدة البيانات الموحدة"""
        try:
            # إنشاء مجلد البيانات إذا لم يكن موجوداً
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            # الاتصال بقاعدة البيانات
            db_path = data_dir / "unified_employees.db"
            self.db_connection = sqlite3.connect(str(db_path))
            self.db_connection.row_factory = sqlite3.Row
            
            # إنشاء الجداول
            self.create_unified_tables()
            
            # إدراج بيانات تجريبية إذا كانت قاعدة البيانات فارغة
            self.insert_sample_data()
            
            print("✅ تم تهيئة قاعدة البيانات الموحدة بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
            raise
    
    def create_unified_tables(self):
        """إنشاء جداول قاعدة البيانات الموحدة"""
        try:
            cursor = self.db_connection.cursor()
            
            # جدول الموظفين الموحد
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_number TEXT UNIQUE,
                    name TEXT NOT NULL,
                    department TEXT,
                    position TEXT,
                    salary REAL DEFAULT 0,
                    hire_date TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    status TEXT DEFAULT 'نشط',
                    performance_score REAL DEFAULT 0,
                    photo_path TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # جدول الحضور والغياب
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    date TEXT,
                    check_in TEXT,
                    check_out TEXT,
                    status TEXT DEFAULT 'حاضر',
                    notes TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            """)
            
            # جدول الرواتب
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS salaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    month TEXT,
                    year INTEGER,
                    basic_salary REAL,
                    allowances REAL DEFAULT 0,
                    deductions REAL DEFAULT 0,
                    net_salary REAL,
                    payment_date TEXT,
                    status TEXT DEFAULT 'معلق',
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            """)
            
            # جدول التقييمات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    evaluation_date TEXT,
                    performance_score REAL,
                    quality_score REAL,
                    punctuality_score REAL,
                    teamwork_score REAL,
                    overall_score REAL,
                    comments TEXT,
                    evaluator TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            """)
            
            self.db_connection.commit()
            print("✅ تم إنشاء جداول قاعدة البيانات الموحدة")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء الجداول: {e}")
            raise

    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        try:
            cursor = self.db_connection.cursor()

            # فحص وجود بيانات
            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]

            if count == 0:
                # إدراج موظفين تجريبيين
                sample_employees = [
                    {
                        'employee_number': 'EMP001',
                        'name': 'أحمد محمد علي',
                        'department': 'الإدارة',
                        'position': 'مدير عام',
                        'salary': 15000,
                        'hire_date': '2020-01-15',
                        'phone': '01234567890',
                        'email': 'ahmed@company.com',
                        'status': 'نشط',
                        'performance_score': 95
                    },
                    {
                        'employee_number': 'EMP002',
                        'name': 'فاطمة أحمد حسن',
                        'department': 'المحاسبة',
                        'position': 'محاسب أول',
                        'salary': 8000,
                        'hire_date': '2021-03-10',
                        'phone': '01234567891',
                        'email': 'fatima@company.com',
                        'status': 'نشط',
                        'performance_score': 88
                    },
                    {
                        'employee_number': 'EMP003',
                        'name': 'محمد عبدالله سالم',
                        'department': 'المبيعات',
                        'position': 'مندوب مبيعات',
                        'salary': 6000,
                        'hire_date': '2022-06-20',
                        'phone': '01234567892',
                        'email': 'mohammed@company.com',
                        'status': 'نشط',
                        'performance_score': 82
                    },
                    {
                        'employee_number': 'EMP004',
                        'name': 'سارة محمود أحمد',
                        'department': 'التقنية',
                        'position': 'مطور برمجيات',
                        'salary': 10000,
                        'hire_date': '2021-09-05',
                        'phone': '01234567893',
                        'email': 'sara@company.com',
                        'status': 'نشط',
                        'performance_score': 92
                    },
                    {
                        'employee_number': 'EMP005',
                        'name': 'خالد عبدالرحمن محمد',
                        'department': 'الموارد البشرية',
                        'position': 'أخصائي موارد بشرية',
                        'salary': 7500,
                        'hire_date': '2020-11-12',
                        'phone': '01234567894',
                        'email': 'khalid@company.com',
                        'status': 'نشط',
                        'performance_score': 85
                    }
                ]

                for emp in sample_employees:
                    cursor.execute("""
                        INSERT INTO employees (
                            employee_number, name, department, position, salary,
                            hire_date, phone, email, status, performance_score
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        emp['employee_number'], emp['name'], emp['department'],
                        emp['position'], emp['salary'], emp['hire_date'],
                        emp['phone'], emp['email'], emp['status'], emp['performance_score']
                    ))

                self.db_connection.commit()
                print("✅ تم إدراج البيانات التجريبية")

        except Exception as e:
            print(f"❌ خطأ في إدراج البيانات التجريبية: {e}")

    def create_unified_interface(self):
        """إنشاء الواجهة الموحدة"""
        try:
            # الإطار الرئيسي
            main_frame = ctk.CTkFrame(
                self.window,
                fg_color="transparent"
            )
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # إنشاء الهيدر
            self.create_unified_header(main_frame)

            # إنشاء شريط الأدوات
            self.create_unified_toolbar(main_frame)

            # إنشاء المحتوى الرئيسي
            self.create_unified_content(main_frame)

        except Exception as e:
            print(f"❌ خطأ في إنشاء الواجهة: {e}")
            raise

    def create_unified_header(self, parent):
        """إنشاء الهيدر الموحد"""
        try:
            header_frame = ctk.CTkFrame(
                parent,
                height=UNIFIED_DIMENSIONS['header_height'],
                fg_color=UNIFIED_COLORS['primary'],
                corner_radius=UNIFIED_DIMENSIONS['corner_radius']
            )
            header_frame.pack(fill="x", pady=(0, 10))
            header_frame.pack_propagate(False)

            # محتوى الهيدر
            content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=20, pady=15)

            # العنوان الرئيسي
            title_label = ctk.CTkLabel(
                content_frame,
                text="🏢 نظام إدارة الموظفين الموحد والمتطور",
                font=UNIFIED_FONTS['title_large'],
                text_color=UNIFIED_COLORS['text_light']
            )
            title_label.pack(side="right", anchor="e")

            # الإحصائيات السريعة
            stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            stats_frame.pack(side="left", anchor="w")

            # إنشاء عناصر الإحصائيات
            self.stats_labels = {}
            stats_info = [
                ("total", "إجمالي الموظفين", "👥"),
                ("active", "الموظفين النشطين", "✅"),
                ("avg_salary", "متوسط الراتب", "💰"),
                ("performance", "متوسط الأداء", "📊")
            ]

            for i, (key, text, icon) in enumerate(stats_info):
                stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
                stat_frame.pack(side="left", padx=(0, 15))

                icon_label = ctk.CTkLabel(
                    stat_frame,
                    text=icon,
                    font=("Arial", 16),
                    text_color=UNIFIED_COLORS['text_light']
                )
                icon_label.pack()

                value_label = ctk.CTkLabel(
                    stat_frame,
                    text="0",
                    font=UNIFIED_FONTS['text_large'],
                    text_color=UNIFIED_COLORS['text_light']
                )
                value_label.pack()

                desc_label = ctk.CTkLabel(
                    stat_frame,
                    text=text,
                    font=UNIFIED_FONTS['text_small'],
                    text_color=UNIFIED_COLORS['text_light']
                )
                desc_label.pack()

                self.stats_labels[key] = value_label

        except Exception as e:
            print(f"❌ خطأ في إنشاء الهيدر: {e}")

    def create_unified_toolbar(self, parent):
        """إنشاء شريط الأدوات الموحد"""
        try:
            toolbar_frame = ctk.CTkFrame(
                parent,
                height=UNIFIED_DIMENSIONS['toolbar_height'],
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=UNIFIED_DIMENSIONS['corner_radius']
            )
            toolbar_frame.pack(fill="x", pady=(0, 10))
            toolbar_frame.pack_propagate(False)

            # الجانب الأيسر - أزرار العمليات
            left_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
            left_frame.pack(side="left", fill="y", padx=15, pady=10)

            # أزرار العمليات الرئيسية
            buttons_data = [
                ("➕ إضافة", self.add_employee, UNIFIED_COLORS['success']),
                ("✏️ تعديل", self.edit_employee, UNIFIED_COLORS['info']),
                ("🗑️ حذف", self.delete_employee, UNIFIED_COLORS['danger']),
                ("📊 تقارير", self.show_reports, UNIFIED_COLORS['secondary']),
                ("💰 الرواتب", self.manage_salaries, UNIFIED_COLORS['warning']),
                ("🔄 تحديث", self.refresh_data, UNIFIED_COLORS['primary'])
            ]

            # أزرار التحكم في النافذة
            window_buttons_data = [
                ("🔳 تكبير", self.maximize_window, "#6c757d"),
                ("⛶ ملء الشاشة", self.toggle_fullscreen, "#6c757d")
            ]

            for text, command, color in buttons_data:
                btn = ctk.CTkButton(
                    left_frame,
                    text=text,
                    command=command,
                    width=UNIFIED_DIMENSIONS['button_width'],
                    height=UNIFIED_DIMENSIONS['button_height'],
                    font=UNIFIED_FONTS['button_medium'],
                    fg_color=color,
                    hover_color=self.get_hover_color(color),
                    corner_radius=8
                )
                btn.pack(side="left", padx=5)

            # إضافة أزرار التحكم في النافذة
            for text, command, color in window_buttons_data:
                btn = ctk.CTkButton(
                    left_frame,
                    text=text,
                    command=command,
                    width=120,
                    height=UNIFIED_DIMENSIONS['button_height'],
                    font=UNIFIED_FONTS['text_small'],
                    fg_color=color,
                    hover_color=self.get_hover_color(color),
                    corner_radius=8
                )
                btn.pack(side="left", padx=5)

            # الجانب الأيمن - البحث والفلترة
            right_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
            right_frame.pack(side="right", fill="y", padx=15, pady=10)

            # حقل البحث
            search_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
            search_frame.pack(side="right", padx=(0, 10))

            search_label = ctk.CTkLabel(
                search_frame,
                text="🔍 البحث:",
                font=UNIFIED_FONTS['text_medium']
            )
            search_label.pack(anchor="e")

            # إنشاء حقل البحث مع التحقق من المتغير
            if self.search_var:
                search_entry = ctk.CTkEntry(
                    search_frame,
                    textvariable=self.search_var,
                    placeholder_text="ابحث في أسماء الموظفين...",
                    width=200,
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
            else:
                search_entry = ctk.CTkEntry(
                    search_frame,
                    placeholder_text="ابحث في أسماء الموظفين...",
                    width=200,
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
            search_entry.pack()

            # فلتر القسم
            dept_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
            dept_frame.pack(side="right", padx=(0, 10))

            dept_label = ctk.CTkLabel(
                dept_frame,
                text="📋 القسم:",
                font=UNIFIED_FONTS['text_medium']
            )
            dept_label.pack(anchor="e")

            # إنشاء فلتر القسم مع التحقق من المتغير
            if self.department_filter_var:
                dept_combo = ctk.CTkComboBox(
                    dept_frame,
                    variable=self.department_filter_var,
                    values=["الكل", "الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية"],
                    width=150,
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input'],
                    command=self.apply_filters
                )
            else:
                dept_combo = ctk.CTkComboBox(
                    dept_frame,
                    values=["الكل", "الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية"],
                    width=150,
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
                dept_combo.set("الكل")
            dept_combo.pack()

            # فلتر الحالة
            status_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
            status_frame.pack(side="right")

            status_label = ctk.CTkLabel(
                status_frame,
                text="📊 الحالة:",
                font=UNIFIED_FONTS['text_medium']
            )
            status_label.pack(anchor="e")

            # إنشاء فلتر الحالة مع التحقق من المتغير
            if self.status_filter_var:
                status_combo = ctk.CTkComboBox(
                    status_frame,
                    variable=self.status_filter_var,
                    values=["الكل", "نشط", "غير نشط", "معلق"],
                    width=120,
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input'],
                    command=self.apply_filters
                )
            else:
                status_combo = ctk.CTkComboBox(
                    status_frame,
                    values=["الكل", "نشط", "غير نشط", "معلق"],
                    width=120,
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
                status_combo.set("الكل")
            status_combo.pack()

        except Exception as e:
            print(f"❌ خطأ في إنشاء شريط الأدوات: {e}")

    def create_unified_content(self, parent):
        """إنشاء المحتوى الرئيسي الموحد"""
        try:
            content_frame = ctk.CTkFrame(parent, fg_color="transparent")
            content_frame.pack(fill="both", expand=True)

            # الجزء الأيسر - جدول الموظفين
            left_frame = ctk.CTkFrame(
                content_frame,
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=UNIFIED_DIMENSIONS['corner_radius']
            )
            left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

            self.create_employees_table(left_frame)

            # الجزء الأيمن - نموذج التفاصيل والتحليلات
            right_frame = ctk.CTkFrame(
                content_frame,
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=UNIFIED_DIMENSIONS['corner_radius'],
                width=UNIFIED_DIMENSIONS['sidebar_width']
            )
            right_frame.pack(side="right", fill="y", padx=(5, 0))
            right_frame.pack_propagate(False)

            # إنشاء تبويبات للجزء الأيمن
            self.create_right_panel_tabs(right_frame)

        except Exception as e:
            print(f"❌ خطأ في إنشاء المحتوى: {e}")

    def create_employees_table(self, parent):
        """إنشاء جدول الموظفين"""
        try:
            # عنوان الجدول
            table_header = ctk.CTkFrame(
                parent,
                height=50,
                fg_color=UNIFIED_COLORS['primary'],
                corner_radius=UNIFIED_DIMENSIONS['corner_radius']
            )
            table_header.pack(fill="x")
            table_header.pack_propagate(False)

            header_label = ctk.CTkLabel(
                table_header,
                text="📋 قائمة الموظفين",
                font=UNIFIED_FONTS['title_medium'],
                text_color="white"
            )
            header_label.pack(pady=12)

            # إطار الجدول
            table_frame = ctk.CTkFrame(
                parent,
                fg_color=UNIFIED_COLORS['background'],
                corner_radius=UNIFIED_DIMENSIONS['corner_radius']
            )
            table_frame.pack(fill="both", expand=True)

            # إنشاء Treeview
            columns = ("ID", "الرقم", "الاسم", "القسم", "المنصب", "الراتب", "الحالة", "الأداء")

            tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # إنشاء الجدول مع شريط التمرير
            tree_container = tk.Frame(tree_frame, bg=UNIFIED_COLORS['background'])
            tree_container.pack(fill="both", expand=True)

            self.tree = ttk.Treeview(
                tree_container,
                columns=columns,
                show="headings",
                height=15
            )

            # تكوين الأعمدة
            column_widths = {
                "ID": 50,
                "الرقم": 80,
                "الاسم": 150,
                "القسم": 100,
                "المنصب": 120,
                "الراتب": 80,
                "الحالة": 80,
                "الأداء": 70
            }

            for col in columns:
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, width=column_widths.get(col, 100), anchor="center")

            # شريط التمرير العمودي
            v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=v_scrollbar.set)

            # شريط التمرير الأفقي
            h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=h_scrollbar.set)

            # تخطيط الجدول وأشرطة التمرير
            self.tree.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            tree_container.grid_rowconfigure(0, weight=1)
            tree_container.grid_columnconfigure(0, weight=1)

            # ربط أحداث الجدول
            self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)
            self.tree.bind("<Double-1>", self.on_employee_double_click)

        except Exception as e:
            print(f"❌ خطأ في إنشاء جدول الموظفين: {e}")

    def create_right_panel_tabs(self, parent):
        """إنشاء تبويبات الجزء الأيمن"""
        try:
            # إنشاء التبويبات
            tabview = ctk.CTkTabview(
                parent,
                corner_radius=UNIFIED_DIMENSIONS['corner_radius']
            )
            tabview.pack(fill="both", expand=True, padx=10, pady=10)

            # تبويب تفاصيل الموظف
            details_tab = tabview.add("📝 التفاصيل")
            self.create_employee_form(details_tab)

            # تبويب التحليلات
            analytics_tab = tabview.add("📊 التحليلات")
            self.create_analytics_panel(analytics_tab)

            # تبويب الإحصائيات
            stats_tab = tabview.add("📈 الإحصائيات")
            self.create_statistics_panel(stats_tab)

            # حفظ مرجع للتبويبات
            self.tabview = tabview

        except Exception as e:
            print(f"❌ خطأ في إنشاء التبويبات: {e}")

    def create_employee_form(self, parent):
        """إنشاء نموذج تفاصيل الموظف"""
        try:
            # إطار قابل للتمرير
            scroll_frame = ctk.CTkScrollableFrame(
                parent,
                fg_color="transparent"
            )
            scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

            # تهيئة متغيرات النموذج
            self.init_form_variables()

            # حقول النموذج
            form_fields = [
                ("employee_number", "رقم الموظف", "entry", True),
                ("name", "الاسم الكامل", "entry", True),
                ("department", "القسم", "combo", True, ["الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية"]),
                ("position", "المنصب", "entry", True),
                ("salary", "الراتب", "number", True),
                ("hire_date", "تاريخ التوظيف", "date", False),
                ("phone", "رقم الهاتف", "entry", False),
                ("email", "البريد الإلكتروني", "entry", False),
                ("address", "العنوان", "text", False),
                ("status", "الحالة", "combo", True, ["نشط", "غير نشط", "معلق"]),
                ("performance_score", "درجة الأداء", "slider", False),
                ("notes", "ملاحظات", "text", False)
            ]

            for field_data in form_fields:
                field_name = field_data[0]
                field_label = field_data[1]
                field_type = field_data[2]
                required = field_data[3]
                values = field_data[4] if len(field_data) > 4 else None

                self.create_form_field(scroll_frame, field_name, field_label, field_type, required, values)

            # أزرار النموذج
            buttons_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=20)

            save_btn = ctk.CTkButton(
                buttons_frame,
                text="💾 حفظ",
                command=self.save_employee,
                fg_color=UNIFIED_COLORS['success'],
                hover_color=self.get_hover_color(UNIFIED_COLORS['success']),
                font=UNIFIED_FONTS['button_medium']
            )
            save_btn.pack(side="right", padx=5)

            clear_btn = ctk.CTkButton(
                buttons_frame,
                text="🗑️ مسح",
                command=self.clear_form,
                fg_color=UNIFIED_COLORS['warning'],
                hover_color=self.get_hover_color(UNIFIED_COLORS['warning']),
                font=UNIFIED_FONTS['button_medium']
            )
            clear_btn.pack(side="right", padx=5)

        except Exception as e:
            print(f"❌ خطأ في إنشاء نموذج الموظف: {e}")

    def init_form_variables(self):
        """تهيئة متغيرات النموذج"""
        try:
            # التأكد من وجود النافذة
            master = self.window if self.window else None

            self.form_vars = {
                'employee_number': tk.StringVar(master=master),
                'name': tk.StringVar(master=master),
                'department': tk.StringVar(master=master, value="الإدارة"),
                'position': tk.StringVar(master=master),
                'salary': tk.StringVar(master=master, value="0"),
                'hire_date': tk.StringVar(master=master, value=datetime.now().strftime("%Y-%m-%d")),
                'phone': tk.StringVar(master=master),
                'email': tk.StringVar(master=master),
                'address': tk.StringVar(master=master),
                'status': tk.StringVar(master=master, value="نشط"),
                'performance_score': tk.DoubleVar(master=master, value=0),
                'notes': tk.StringVar(master=master)
            }
            print("✅ تم تهيئة متغيرات النموذج")
        except Exception as e:
            print(f"❌ خطأ في تهيئة متغيرات النموذج: {e}")
            # إنشاء متغيرات فارغة لتجنب الأخطاء
            self.form_vars = {}

    def create_form_field(self, parent, field_name, label, field_type, required=False, values=None):
        """إنشاء حقل في النموذج"""
        try:
            # إطار الحقل
            field_frame = ctk.CTkFrame(parent, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)

            # تسمية الحقل
            label_text = f"{label} {'*' if required else ''}"
            field_label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=UNIFIED_FONTS['text_medium'],
                anchor="e"
            )
            field_label.pack(anchor="e", pady=(0, 5))

            # إنشاء عنصر الإدخال حسب النوع
            if field_type == "entry":
                widget = ctk.CTkEntry(
                    field_frame,
                    textvariable=self.form_vars[field_name],
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
            elif field_type == "combo":
                widget = ctk.CTkComboBox(
                    field_frame,
                    variable=self.form_vars[field_name],
                    values=values or [],
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
            elif field_type == "text":
                widget = ctk.CTkTextbox(
                    field_frame,
                    height=80,
                    font=UNIFIED_FONTS['input']
                )
                # ربط النص بالمتغير
                widget.bind("<KeyRelease>", lambda e: self.form_vars[field_name].set(widget.get("1.0", "end-1c")))
            elif field_type == "number":
                widget = ctk.CTkEntry(
                    field_frame,
                    textvariable=self.form_vars[field_name],
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
                # التحقق من الأرقام فقط
                widget.bind("<KeyRelease>", lambda e: self.validate_number(field_name))
            elif field_type == "date":
                widget = ctk.CTkEntry(
                    field_frame,
                    textvariable=self.form_vars[field_name],
                    placeholder_text="YYYY-MM-DD",
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )
            elif field_type == "slider":
                widget = ctk.CTkSlider(
                    field_frame,
                    from_=0,
                    to=100,
                    variable=self.form_vars[field_name],
                    height=20
                )
                # إضافة تسمية للقيمة
                value_label = ctk.CTkLabel(
                    field_frame,
                    text="0%",
                    font=UNIFIED_FONTS['text_small']
                )
                value_label.pack(pady=(5, 0))

                def update_slider_label(value):
                    value_label.configure(text=f"{int(float(value))}%")

                widget.configure(command=update_slider_label)
            else:
                widget = ctk.CTkEntry(
                    field_frame,
                    textvariable=self.form_vars[field_name],
                    height=UNIFIED_DIMENSIONS['input_height'],
                    font=UNIFIED_FONTS['input']
                )

            widget.pack(fill="x")

        except Exception as e:
            print(f"❌ خطأ في إنشاء حقل {field_name}: {e}")

    def validate_number(self, field_name):
        """التحقق من صحة الأرقام"""
        try:
            value = self.form_vars[field_name].get()
            if value and not value.replace('.', '').replace('-', '').isdigit():
                # إزالة الأحرف غير الرقمية
                clean_value = ''.join(c for c in value if c.isdigit() or c in '.-')
                self.form_vars[field_name].set(clean_value)
        except Exception as e:
            print(f"خطأ في التحقق من الرقم: {e}")

    def create_analytics_panel(self, parent):
        """إنشاء لوحة التحليلات"""
        try:
            # إطار قابل للتمرير
            scroll_frame = ctk.CTkScrollableFrame(
                parent,
                fg_color="transparent"
            )
            scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

            # عنوان التحليلات
            title_label = ctk.CTkLabel(
                scroll_frame,
                text="📊 تحليلات الموظف المحدد",
                font=UNIFIED_FONTS['title_medium'],
                text_color=UNIFIED_COLORS['primary']
            )
            title_label.pack(pady=10)

            # معلومات الأداء
            performance_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=8
            )
            performance_frame.pack(fill="x", pady=5)

            perf_title = ctk.CTkLabel(
                performance_frame,
                text="📈 تحليل الأداء",
                font=UNIFIED_FONTS['title_small'],
                text_color=UNIFIED_COLORS['success']
            )
            perf_title.pack(pady=10)

            # شريط تقدم الأداء
            self.performance_progress = ctk.CTkProgressBar(
                performance_frame,
                width=200,
                height=20
            )
            self.performance_progress.pack(pady=5)
            self.performance_progress.set(0)

            self.performance_label = ctk.CTkLabel(
                performance_frame,
                text="0%",
                font=UNIFIED_FONTS['text_medium']
            )
            self.performance_label.pack(pady=(0, 10))

            # معلومات الراتب
            salary_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=8
            )
            salary_frame.pack(fill="x", pady=5)

            salary_title = ctk.CTkLabel(
                salary_frame,
                text="💰 معلومات الراتب",
                font=UNIFIED_FONTS['title_small'],
                text_color=UNIFIED_COLORS['warning']
            )
            salary_title.pack(pady=10)

            self.salary_info_label = ctk.CTkLabel(
                salary_frame,
                text="لم يتم تحديد موظف",
                font=UNIFIED_FONTS['text_medium']
            )
            self.salary_info_label.pack(pady=(0, 10))

            # معلومات إضافية
            info_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=8
            )
            info_frame.pack(fill="x", pady=5)

            info_title = ctk.CTkLabel(
                info_frame,
                text="ℹ️ معلومات إضافية",
                font=UNIFIED_FONTS['title_small'],
                text_color=UNIFIED_COLORS['info']
            )
            info_title.pack(pady=10)

            self.additional_info_label = ctk.CTkLabel(
                info_frame,
                text="اختر موظفاً لعرض التحليلات",
                font=UNIFIED_FONTS['text_medium'],
                wraplength=250
            )
            self.additional_info_label.pack(pady=(0, 10))

        except Exception as e:
            print(f"❌ خطأ في إنشاء لوحة التحليلات: {e}")

    def create_statistics_panel(self, parent):
        """إنشاء لوحة الإحصائيات"""
        try:
            # إطار قابل للتمرير
            scroll_frame = ctk.CTkScrollableFrame(
                parent,
                fg_color="transparent"
            )
            scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

            # عنوان الإحصائيات
            title_label = ctk.CTkLabel(
                scroll_frame,
                text="📈 إحصائيات عامة",
                font=UNIFIED_FONTS['title_medium'],
                text_color=UNIFIED_COLORS['primary']
            )
            title_label.pack(pady=10)

            # إحصائيات الأقسام
            dept_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=8
            )
            dept_frame.pack(fill="x", pady=5)

            dept_title = ctk.CTkLabel(
                dept_frame,
                text="🏢 توزيع الأقسام",
                font=UNIFIED_FONTS['title_small']
            )
            dept_title.pack(pady=10)

            self.dept_stats_frame = ctk.CTkFrame(dept_frame, fg_color="transparent")
            self.dept_stats_frame.pack(fill="x", padx=10, pady=(0, 10))

            # إحصائيات الرواتب
            salary_stats_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color=UNIFIED_COLORS['card'],
                corner_radius=8
            )
            salary_stats_frame.pack(fill="x", pady=5)

            salary_stats_title = ctk.CTkLabel(
                salary_stats_frame,
                text="💰 إحصائيات الرواتب",
                font=UNIFIED_FONTS['title_small']
            )
            salary_stats_title.pack(pady=10)

            self.salary_stats_label = ctk.CTkLabel(
                salary_stats_frame,
                text="جاري التحميل...",
                font=UNIFIED_FONTS['text_medium']
            )
            self.salary_stats_label.pack(pady=(0, 10))

        except Exception as e:
            print(f"❌ خطأ في إنشاء لوحة الإحصائيات: {e}")

    # ==================== وظائف البيانات ====================

    def load_employees_data(self):
        """تحميل بيانات الموظفين"""
        try:
            # عرض مؤشر التحميل
            self.show_loading_indicator("جاري تحميل بيانات الموظفين...")

            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT id, employee_number, name, department, position,
                       salary, hire_date, phone, email, address, status,
                       performance_score, notes
                FROM employees
                ORDER BY name
            """)

            # تحويل النتائج إلى قاموس للوصول السريع
            rows = cursor.fetchall()
            self.employees_data = []

            for row in rows:
                employee = {
                    'id': row[0],
                    'employee_number': row[1],
                    'name': row[2],
                    'department': row[3],
                    'position': row[4],
                    'salary': row[5],
                    'hire_date': row[6],
                    'phone': row[7],
                    'email': row[8],
                    'address': row[9],
                    'status': row[10],
                    'performance_score': row[11],
                    'notes': row[12]
                }
                self.employees_data.append(employee)

            self.filtered_employees = self.employees_data.copy()

            # تحديث الجدول
            self.update_employees_table()

            # إخفاء مؤشر التحميل
            self.hide_loading_indicator()

            print(f"✅ تم تحميل {len(self.employees_data)} موظف")

        except Exception as e:
            self.hide_loading_indicator()
            print(f"❌ خطأ في تحميل البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات: {e}")

    def show_loading_indicator(self, message="جاري التحميل..."):
        """عرض مؤشر التحميل"""
        try:
            if hasattr(self, 'window') and self.window:
                # يمكن إضافة مؤشر تحميل مرئي هنا
                self.window.configure(cursor="wait")
                self.window.update()
        except Exception as e:
            print(f"⚠️ خطأ في عرض مؤشر التحميل: {e}")

    def hide_loading_indicator(self):
        """إخفاء مؤشر التحميل"""
        try:
            if hasattr(self, 'window') and self.window:
                self.window.configure(cursor="")
                self.window.update()
        except Exception as e:
            print(f"⚠️ خطأ في إخفاء مؤشر التحميل: {e}")

    def update_employees_table(self):
        """تحديث جدول الموظفين"""
        try:
            # التحقق من وجود الجدول
            if not hasattr(self, 'tree') or self.tree is None:
                print("⚠️ الجدول غير موجود - تخطي التحديث")
                return

            # مسح البيانات الحالية
            for item in self.tree.get_children():
                self.tree.delete(item)

            # إضافة البيانات الجديدة
            for emp in self.filtered_employees:
                values = (
                    emp['id'],
                    emp['employee_number'],
                    emp['name'],
                    emp['department'],
                    emp['position'],
                    f"{emp['salary']:,.0f}",
                    emp['status'],
                    f"{emp['performance_score']:.0f}%"
                )

                # تلوين الصفوف حسب الحالة
                tags = []
                if emp['status'] == 'نشط':
                    tags = ['active']
                elif emp['status'] == 'غير نشط':
                    tags = ['inactive']
                else:
                    tags = ['pending']

                self.tree.insert("", "end", values=values, tags=tags)

            # تكوين ألوان الصفوف
            self.tree.tag_configure('active', background='#e8f5e8')
            self.tree.tag_configure('inactive', background='#ffe8e8')
            self.tree.tag_configure('pending', background='#fff3cd')

        except Exception as e:
            print(f"❌ خطأ في تحديث الجدول: {e}")

    def update_statistics(self):
        """تحديث الإحصائيات"""
        try:
            if not self.employees_data:
                return

            # حساب الإحصائيات
            total_employees = len(self.employees_data)
            active_employees = len([emp for emp in self.employees_data if emp['status'] == 'نشط'])
            total_salary = sum(emp['salary'] for emp in self.employees_data)
            avg_salary = total_salary / total_employees if total_employees > 0 else 0
            avg_performance = sum(emp['performance_score'] for emp in self.employees_data) / total_employees if total_employees > 0 else 0

            # تحديث تسميات الإحصائيات في الهيدر
            if hasattr(self, 'stats_labels'):
                self.stats_labels['total'].configure(text=str(total_employees))
                self.stats_labels['active'].configure(text=str(active_employees))
                self.stats_labels['avg_salary'].configure(text=f"{avg_salary:,.0f}")
                self.stats_labels['performance'].configure(text=f"{avg_performance:.0f}%")

            # تحديث إحصائيات الأقسام
            self.update_department_statistics()

            # تحديث إحصائيات الرواتب
            self.update_salary_statistics()

        except Exception as e:
            print(f"❌ خطأ في تحديث الإحصائيات: {e}")

    def update_department_statistics(self):
        """تحديث إحصائيات الأقسام"""
        try:
            if not hasattr(self, 'dept_stats_frame'):
                return

            # مسح الإحصائيات الحالية
            for widget in self.dept_stats_frame.winfo_children():
                widget.destroy()

            # حساب توزيع الأقسام
            dept_counts = {}
            for emp in self.employees_data:
                dept = emp['department']
                dept_counts[dept] = dept_counts.get(dept, 0) + 1

            # عرض الإحصائيات
            for dept, count in dept_counts.items():
                dept_frame = ctk.CTkFrame(self.dept_stats_frame, fg_color="transparent")
                dept_frame.pack(fill="x", pady=2)

                dept_label = ctk.CTkLabel(
                    dept_frame,
                    text=f"{dept}: {count}",
                    font=UNIFIED_FONTS['text_small']
                )
                dept_label.pack(side="right")

                # شريط تقدم
                progress = ctk.CTkProgressBar(
                    dept_frame,
                    width=150,
                    height=10
                )
                progress.pack(side="right", padx=(0, 10))
                progress.set(count / len(self.employees_data))

        except Exception as e:
            print(f"❌ خطأ في تحديث إحصائيات الأقسام: {e}")

    def update_salary_statistics(self):
        """تحديث إحصائيات الرواتب"""
        try:
            if not hasattr(self, 'salary_stats_label'):
                return

            if not self.employees_data:
                self.salary_stats_label.configure(text="لا توجد بيانات")
                return

            salaries = [emp['salary'] for emp in self.employees_data]

            min_salary = min(salaries)
            max_salary = max(salaries)
            avg_salary = sum(salaries) / len(salaries)
            total_salary = sum(salaries)

            stats_text = f"""
إجمالي الرواتب: {total_salary:,.0f}
متوسط الراتب: {avg_salary:,.0f}
أعلى راتب: {max_salary:,.0f}
أقل راتب: {min_salary:,.0f}
            """.strip()

            self.salary_stats_label.configure(text=stats_text)

        except Exception as e:
            print(f"❌ خطأ في تحديث إحصائيات الرواتب: {e}")

    # ==================== وظائف الأحداث ====================

    def bind_events(self):
        """ربط الأحداث"""
        try:
            # ربط البحث إذا كانت المتغيرات موجودة
            if self.search_var:
                self.search_var.trace("w", self.on_search_change)
                print("✅ تم ربط أحداث البحث")
            else:
                print("⚠️ لا يمكن ربط أحداث البحث - المتغيرات غير موجودة")

            # ربط اختصارات لوحة المفاتيح
            self.bind_keyboard_shortcuts()

        except Exception as e:
            print(f"❌ خطأ في ربط الأحداث: {e}")

    def bind_keyboard_shortcuts(self):
        """ربط اختصارات لوحة المفاتيح"""
        try:
            # اختصارات النافذة
            self.window.bind("<F11>", lambda e: self.toggle_fullscreen())
            self.window.bind("<Control-plus>", lambda e: self.maximize_window())
            self.window.bind("<Control-minus>", lambda e: self.window.state('normal'))

            # اختصارات العمليات
            self.window.bind("<Control-n>", lambda e: self.add_employee())
            self.window.bind("<Control-e>", lambda e: self.edit_employee())
            self.window.bind("<Delete>", lambda e: self.delete_employee())
            self.window.bind("<Control-s>", lambda e: self.save_employee())
            self.window.bind("<F5>", lambda e: self.refresh_data())

            # اختصارات البحث
            self.window.bind("<Control-f>", lambda e: self.focus_search())

            print("✅ تم ربط اختصارات لوحة المفاتيح")

        except Exception as e:
            print(f"❌ خطأ في ربط اختصارات لوحة المفاتيح: {e}")

    def focus_search(self):
        """تركيز على حقل البحث"""
        try:
            # البحث عن حقل البحث وتركيز عليه
            for widget in self.window.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkEntry) and hasattr(child, 'get'):
                            child.focus()
                            break
        except Exception as e:
            print(f"❌ خطأ في تركيز البحث: {e}")

    def on_search_change(self, *args):
        """عند تغيير نص البحث"""
        self.apply_filters()

    def apply_filters(self, *args):
        """تطبيق الفلاتر"""
        try:
            # التحقق من وجود المتغيرات
            if not self.search_var or not self.department_filter_var or not self.status_filter_var:
                print("⚠️ المتغيرات غير مهيأة - تخطي الفلترة")
                return

            search_text = self.search_var.get().lower() if self.search_var.get() else ""
            dept_filter = self.department_filter_var.get() if self.department_filter_var.get() else "الكل"
            status_filter = self.status_filter_var.get() if self.status_filter_var.get() else "الكل"

            self.filtered_employees = []

            for emp in self.employees_data:
                # فلتر البحث
                if search_text and search_text not in emp['name'].lower():
                    continue

                # فلتر القسم
                if dept_filter != "الكل" and emp['department'] != dept_filter:
                    continue

                # فلتر الحالة
                if status_filter != "الكل" and emp['status'] != status_filter:
                    continue

                self.filtered_employees.append(emp)

            # تحديث الجدول
            self.update_employees_table()

        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")

    def on_employee_select(self, event):
        """عند اختيار موظف من الجدول"""
        try:
            selection = self.tree.selection()
            if not selection:
                return

            item = self.tree.item(selection[0])
            emp_id = item['values'][0]

            # البحث عن الموظف
            self.current_employee = None
            for emp in self.employees_data:
                if emp['id'] == emp_id:
                    self.current_employee = emp
                    break

            if self.current_employee:
                # تحديث النموذج
                self.populate_form(self.current_employee)

                # تحديث التحليلات
                self.update_employee_analytics(self.current_employee)

        except Exception as e:
            print(f"❌ خطأ في اختيار الموظف: {e}")

    def on_employee_double_click(self, event):
        """عند النقر المزدوج على موظف"""
        self.edit_employee()

    def populate_form(self, employee):
        """ملء النموذج ببيانات الموظف"""
        try:
            self.form_vars['employee_number'].set(employee['employee_number'] or '')
            self.form_vars['name'].set(employee['name'] or '')
            self.form_vars['department'].set(employee['department'] or '')
            self.form_vars['position'].set(employee['position'] or '')
            self.form_vars['salary'].set(str(employee['salary'] or 0))
            self.form_vars['hire_date'].set(employee['hire_date'] or '')
            self.form_vars['phone'].set(employee['phone'] or '')
            self.form_vars['email'].set(employee['email'] or '')
            self.form_vars['address'].set(employee['address'] or '')
            self.form_vars['status'].set(employee['status'] or 'نشط')
            self.form_vars['performance_score'].set(employee['performance_score'] or 0)
            self.form_vars['notes'].set(employee['notes'] or '')

        except Exception as e:
            print(f"❌ خطأ في ملء النموذج: {e}")

    def update_employee_analytics(self, employee):
        """تحديث تحليلات الموظف"""
        try:
            # تحديث شريط الأداء
            if hasattr(self, 'performance_progress'):
                performance = employee['performance_score'] / 100
                self.performance_progress.set(performance)
                self.performance_label.configure(text=f"{employee['performance_score']:.0f}%")

            # تحديث معلومات الراتب
            if hasattr(self, 'salary_info_label'):
                salary_text = f"الراتب الحالي: {employee['salary']:,.0f}\nالقسم: {employee['department']}\nالمنصب: {employee['position']}"
                self.salary_info_label.configure(text=salary_text)

            # تحديث المعلومات الإضافية
            if hasattr(self, 'additional_info_label'):
                hire_date = employee['hire_date']
                if hire_date:
                    try:
                        hire_datetime = datetime.strptime(hire_date, "%Y-%m-%d")
                        years_of_service = (datetime.now() - hire_datetime).days // 365
                        info_text = f"سنوات الخدمة: {years_of_service}\nتاريخ التوظيف: {hire_date}\nالحالة: {employee['status']}"
                    except:
                        info_text = f"تاريخ التوظيف: {hire_date}\nالحالة: {employee['status']}"
                else:
                    info_text = f"الحالة: {employee['status']}"

                self.additional_info_label.configure(text=info_text)

        except Exception as e:
            print(f"❌ خطأ في تحديث التحليلات: {e}")

    # ==================== وظائف العمليات ====================

    def add_employee(self):
        """إضافة موظف جديد"""
        try:
            # مسح النموذج
            self.clear_form()

            # تركيز على حقل رقم الموظف
            self.tabview.set("📝 التفاصيل")

            # إنشاء رقم موظف تلقائي
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]
            new_number = f"EMP{count + 1:03d}"
            self.form_vars['employee_number'].set(new_number)

            messagebox.showinfo("إضافة موظف", "املأ بيانات الموظف الجديد ثم اضغط حفظ")

        except Exception as e:
            print(f"❌ خطأ في إضافة موظف: {e}")
            messagebox.showerror("خطأ", f"فشل في إضافة موظف: {e}")

    def edit_employee(self):
        """تعديل موظف محدد"""
        try:
            if not self.current_employee:
                messagebox.showwarning("تحذير", "يرجى اختيار موظف للتعديل")
                return

            # التبديل إلى تبويب التفاصيل
            self.tabview.set("📝 التفاصيل")

            messagebox.showinfo("تعديل موظف", f"يمكنك الآن تعديل بيانات {self.current_employee['name']}")

        except Exception as e:
            print(f"❌ خطأ في تعديل موظف: {e}")
            messagebox.showerror("خطأ", f"فشل في تعديل الموظف: {e}")

    def delete_employee(self):
        """حذف موظف محدد"""
        try:
            if not self.current_employee:
                messagebox.showwarning("تحذير", "يرجى اختيار موظف للحذف")
                return

            # تأكيد الحذف
            result = messagebox.askyesno(
                "تأكيد الحذف",
                f"هل أنت متأكد من حذف الموظف:\n{self.current_employee['name']}؟\n\nهذا الإجراء لا يمكن التراجع عنه."
            )

            if result:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM employees WHERE id = ?", (self.current_employee['id'],))
                self.db_connection.commit()

                messagebox.showinfo("نجح", f"تم حذف الموظف {self.current_employee['name']} بنجاح")

                # تحديث البيانات
                self.refresh_data()
                self.clear_form()

        except Exception as e:
            print(f"❌ خطأ في حذف موظف: {e}")
            messagebox.showerror("خطأ", f"فشل في حذف الموظف: {e}")

    def save_employee(self):
        """حفظ بيانات الموظف"""
        try:
            # التحقق من البيانات المطلوبة
            if not self.validate_form():
                return

            # جمع البيانات
            data = {
                'employee_number': self.form_vars['employee_number'].get().strip(),
                'name': self.form_vars['name'].get().strip(),
                'department': self.form_vars['department'].get(),
                'position': self.form_vars['position'].get().strip(),
                'salary': float(self.form_vars['salary'].get() or 0),
                'hire_date': self.form_vars['hire_date'].get().strip(),
                'phone': self.form_vars['phone'].get().strip(),
                'email': self.form_vars['email'].get().strip(),
                'address': self.form_vars['address'].get().strip(),
                'status': self.form_vars['status'].get(),
                'performance_score': float(self.form_vars['performance_score'].get()),
                'notes': self.form_vars['notes'].get().strip()
            }

            cursor = self.db_connection.cursor()

            if self.current_employee:
                # تحديث موظف موجود
                cursor.execute("""
                    UPDATE employees SET
                        employee_number = ?, name = ?, department = ?, position = ?,
                        salary = ?, hire_date = ?, phone = ?, email = ?, address = ?,
                        status = ?, performance_score = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    data['employee_number'], data['name'], data['department'], data['position'],
                    data['salary'], data['hire_date'], data['phone'], data['email'], data['address'],
                    data['status'], data['performance_score'], data['notes'], self.current_employee['id']
                ))

                messagebox.showinfo("نجح", f"تم تحديث بيانات {data['name']} بنجاح")

            else:
                # إضافة موظف جديد
                cursor.execute("""
                    INSERT INTO employees (
                        employee_number, name, department, position, salary,
                        hire_date, phone, email, address, status, performance_score, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['employee_number'], data['name'], data['department'], data['position'],
                    data['salary'], data['hire_date'], data['phone'], data['email'], data['address'],
                    data['status'], data['performance_score'], data['notes']
                ))

                messagebox.showinfo("نجح", f"تم إضافة الموظف {data['name']} بنجاح")

            self.db_connection.commit()

            # تحديث البيانات
            self.refresh_data()

        except ValueError as e:
            messagebox.showerror("خطأ في البيانات", "يرجى التأكد من صحة البيانات المدخلة")
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("خطأ", "رقم الموظف موجود مسبقاً")
            else:
                messagebox.showerror("خطأ في قاعدة البيانات", str(e))
        except Exception as e:
            print(f"❌ خطأ في حفظ الموظف: {e}")
            messagebox.showerror("خطأ", f"فشل في حفظ البيانات: {e}")

    def validate_form(self):
        """التحقق من صحة بيانات النموذج"""
        try:
            # الحقول المطلوبة
            required_fields = {
                'employee_number': 'رقم الموظف',
                'name': 'الاسم',
                'department': 'القسم',
                'position': 'المنصب'
            }

            for field, label in required_fields.items():
                value = self.form_vars[field].get().strip()
                if not value:
                    messagebox.showerror("خطأ", f"حقل {label} مطلوب")
                    return False

            # التحقق من الراتب
            try:
                salary = float(self.form_vars['salary'].get() or 0)
                if salary < 0:
                    messagebox.showerror("خطأ", "الراتب لا يمكن أن يكون سالباً")
                    return False
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال راتب صحيح")
                return False

            # التحقق من درجة الأداء
            performance = self.form_vars['performance_score'].get()
            if performance < 0 or performance > 100:
                messagebox.showerror("خطأ", "درجة الأداء يجب أن تكون بين 0 و 100")
                return False

            # التحقق من تاريخ التوظيف
            hire_date = self.form_vars['hire_date'].get().strip()
            if hire_date:
                try:
                    datetime.strptime(hire_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("خطأ", "تاريخ التوظيف يجب أن يكون بصيغة YYYY-MM-DD")
                    return False

            return True

        except Exception as e:
            print(f"❌ خطأ في التحقق من النموذج: {e}")
            return False

    def clear_form(self):
        """مسح النموذج"""
        try:
            for var in self.form_vars.values():
                if isinstance(var, tk.StringVar):
                    var.set("")
                elif isinstance(var, tk.DoubleVar):
                    var.set(0)

            # إعادة تعيين القيم الافتراضية
            self.form_vars['department'].set("الإدارة")
            self.form_vars['status'].set("نشط")
            self.form_vars['hire_date'].set(datetime.now().strftime("%Y-%m-%d"))

            # مسح الموظف الحالي
            self.current_employee = None

            # مسح التحليلات
            if hasattr(self, 'performance_progress'):
                self.performance_progress.set(0)
                self.performance_label.configure(text="0%")

            if hasattr(self, 'salary_info_label'):
                self.salary_info_label.configure(text="لم يتم تحديد موظف")

            if hasattr(self, 'additional_info_label'):
                self.additional_info_label.configure(text="اختر موظفاً لعرض التحليلات")

        except Exception as e:
            print(f"❌ خطأ في مسح النموذج: {e}")

    def refresh_data(self):
        """تحديث البيانات"""
        try:
            self.load_employees_data()
            self.update_statistics()
            messagebox.showinfo("تحديث", "تم تحديث البيانات بنجاح")

        except Exception as e:
            print(f"❌ خطأ في تحديث البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحديث البيانات: {e}")

    # ==================== الوظائف المتقدمة ====================

    def show_reports(self):
        """عرض التقارير"""
        try:
            # إنشاء نافذة التقارير
            reports_window = ctk.CTkToplevel(self.window)
            reports_window.title("📊 تقارير الموظفين")
            reports_window.geometry("800x600")
            reports_window.transient(self.window)
            reports_window.grab_set()

            # محتوى التقارير
            main_frame = ctk.CTkFrame(reports_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            title_label = ctk.CTkLabel(
                main_frame,
                text="📊 تقارير الموظفين",
                font=UNIFIED_FONTS['title_large']
            )
            title_label.pack(pady=20)

            # أزرار التقارير
            reports_data = [
                ("📋 تقرير شامل", self.generate_comprehensive_report),
                ("💰 تقرير الرواتب", self.generate_salary_report),
                ("📈 تقرير الأداء", self.generate_performance_report),
                ("🏢 تقرير الأقسام", self.generate_department_report)
            ]

            for text, command in reports_data:
                btn = ctk.CTkButton(
                    main_frame,
                    text=text,
                    command=command,
                    width=300,
                    height=50,
                    font=UNIFIED_FONTS['button_large']
                )
                btn.pack(pady=10)

        except Exception as e:
            print(f"❌ خطأ في عرض التقارير: {e}")
            messagebox.showerror("خطأ", f"فشل في عرض التقارير: {e}")

    def manage_salaries(self):
        """إدارة الرواتب"""
        try:
            # إنشاء نافذة إدارة الرواتب
            salary_window = ctk.CTkToplevel(self.window)
            salary_window.title("💰 إدارة الرواتب")
            salary_window.geometry("900x700")
            salary_window.transient(self.window)
            salary_window.grab_set()

            # محتوى إدارة الرواتب
            main_frame = ctk.CTkFrame(salary_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            title_label = ctk.CTkLabel(
                main_frame,
                text="💰 إدارة الرواتب",
                font=UNIFIED_FONTS['title_large']
            )
            title_label.pack(pady=20)

            # معلومات الرواتب
            info_text = f"""
إجمالي عدد الموظفين: {len(self.employees_data)}
إجمالي الرواتب الشهرية: {sum(emp['salary'] for emp in self.employees_data):,.0f}
متوسط الراتب: {sum(emp['salary'] for emp in self.employees_data) / len(self.employees_data) if self.employees_data else 0:,.0f}
            """.strip()

            info_label = ctk.CTkLabel(
                main_frame,
                text=info_text,
                font=UNIFIED_FONTS['text_large'],
                justify="right"
            )
            info_label.pack(pady=20)

            # أزرار إدارة الرواتب
            salary_buttons = [
                ("📊 عرض كشف الرواتب", lambda: self.show_salary_sheet()),
                ("💳 إنشاء كشف راتب", lambda: self.create_payslip()),
                ("📈 تحليل الرواتب", lambda: self.analyze_salaries()),
                ("📋 تصدير البيانات", lambda: self.export_salary_data())
            ]

            for text, command in salary_buttons:
                btn = ctk.CTkButton(
                    main_frame,
                    text=text,
                    command=command,
                    width=300,
                    height=40,
                    font=UNIFIED_FONTS['button_medium']
                )
                btn.pack(pady=5)

        except Exception as e:
            print(f"❌ خطأ في إدارة الرواتب: {e}")
            messagebox.showerror("خطأ", f"فشل في إدارة الرواتب: {e}")

    # ==================== وظائف التقارير ====================

    def generate_comprehensive_report(self):
        """إنشاء تقرير شامل"""
        try:
            report_data = []
            report_data.append("=" * 60)
            report_data.append("تقرير شامل عن الموظفين")
            report_data.append("=" * 60)
            report_data.append(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")

            # إحصائيات عامة
            report_data.append("الإحصائيات العامة:")
            report_data.append("-" * 20)
            report_data.append(f"إجمالي الموظفين: {len(self.employees_data)}")
            active_count = len([emp for emp in self.employees_data if emp['status'] == 'نشط'])
            report_data.append(f"الموظفين النشطين: {active_count}")
            report_data.append(f"إجمالي الرواتب: {sum(emp['salary'] for emp in self.employees_data):,.0f}")
            report_data.append("")

            # تفاصيل الموظفين
            report_data.append("تفاصيل الموظفين:")
            report_data.append("-" * 20)
            for emp in self.employees_data:
                report_data.append(f"الاسم: {emp['name']}")
                report_data.append(f"القسم: {emp['department']}")
                report_data.append(f"المنصب: {emp['position']}")
                report_data.append(f"الراتب: {emp['salary']:,.0f}")
                report_data.append(f"الأداء: {emp['performance_score']:.0f}%")
                report_data.append("")

            # حفظ التقرير
            self.save_report("تقرير_شامل", "\n".join(report_data))

        except Exception as e:
            print(f"❌ خطأ في إنشاء التقرير الشامل: {e}")
            messagebox.showerror("خطأ", f"فشل في إنشاء التقرير: {e}")

    def generate_salary_report(self):
        """إنشاء تقرير الرواتب"""
        try:
            report_data = []
            report_data.append("=" * 60)
            report_data.append("تقرير الرواتب")
            report_data.append("=" * 60)
            report_data.append(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")

            # ترتيب الموظفين حسب الراتب
            sorted_employees = sorted(self.employees_data, key=lambda x: x['salary'], reverse=True)

            total_salary = sum(emp['salary'] for emp in self.employees_data)
            report_data.append(f"إجمالي الرواتب الشهرية: {total_salary:,.0f}")
            report_data.append(f"متوسط الراتب: {total_salary / len(self.employees_data) if self.employees_data else 0:,.0f}")
            report_data.append("")

            report_data.append("تفاصيل الرواتب (مرتبة تنازلياً):")
            report_data.append("-" * 40)

            for i, emp in enumerate(sorted_employees, 1):
                report_data.append(f"{i}. {emp['name']} - {emp['department']} - {emp['salary']:,.0f}")

            # حفظ التقرير
            self.save_report("تقرير_الرواتب", "\n".join(report_data))

        except Exception as e:
            print(f"❌ خطأ في إنشاء تقرير الرواتب: {e}")
            messagebox.showerror("خطأ", f"فشل في إنشاء تقرير الرواتب: {e}")

    def generate_performance_report(self):
        """إنشاء تقرير الأداء"""
        try:
            report_data = []
            report_data.append("=" * 60)
            report_data.append("تقرير الأداء")
            report_data.append("=" * 60)
            report_data.append(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")

            # ترتيب الموظفين حسب الأداء
            sorted_employees = sorted(self.employees_data, key=lambda x: x['performance_score'], reverse=True)

            avg_performance = sum(emp['performance_score'] for emp in self.employees_data) / len(self.employees_data) if self.employees_data else 0
            report_data.append(f"متوسط الأداء العام: {avg_performance:.1f}%")
            report_data.append("")

            # تصنيف الأداء
            excellent = [emp for emp in self.employees_data if emp['performance_score'] >= 90]
            good = [emp for emp in self.employees_data if 70 <= emp['performance_score'] < 90]
            average = [emp for emp in self.employees_data if 50 <= emp['performance_score'] < 70]
            poor = [emp for emp in self.employees_data if emp['performance_score'] < 50]

            report_data.append("تصنيف الأداء:")
            report_data.append("-" * 20)
            report_data.append(f"ممتاز (90%+): {len(excellent)} موظف")
            report_data.append(f"جيد (70-89%): {len(good)} موظف")
            report_data.append(f"متوسط (50-69%): {len(average)} موظف")
            report_data.append(f"ضعيف (<50%): {len(poor)} موظف")
            report_data.append("")

            report_data.append("تفاصيل الأداء (مرتبة تنازلياً):")
            report_data.append("-" * 40)

            for i, emp in enumerate(sorted_employees, 1):
                report_data.append(f"{i}. {emp['name']} - {emp['department']} - {emp['performance_score']:.0f}%")

            # حفظ التقرير
            self.save_report("تقرير_الأداء", "\n".join(report_data))

        except Exception as e:
            print(f"❌ خطأ في إنشاء تقرير الأداء: {e}")
            messagebox.showerror("خطأ", f"فشل في إنشاء تقرير الأداء: {e}")

    def generate_department_report(self):
        """إنشاء تقرير الأقسام"""
        try:
            report_data = []
            report_data.append("=" * 60)
            report_data.append("تقرير الأقسام")
            report_data.append("=" * 60)
            report_data.append(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")

            # تجميع البيانات حسب القسم
            departments = {}
            for emp in self.employees_data:
                dept = emp['department']
                if dept not in departments:
                    departments[dept] = {
                        'employees': [],
                        'total_salary': 0,
                        'avg_performance': 0
                    }
                departments[dept]['employees'].append(emp)
                departments[dept]['total_salary'] += emp['salary']

            # حساب المتوسطات
            for dept_data in departments.values():
                dept_data['avg_performance'] = sum(emp['performance_score'] for emp in dept_data['employees']) / len(dept_data['employees'])

            report_data.append("ملخص الأقسام:")
            report_data.append("-" * 20)

            for dept, data in departments.items():
                report_data.append(f"القسم: {dept}")
                report_data.append(f"  عدد الموظفين: {len(data['employees'])}")
                report_data.append(f"  إجمالي الرواتب: {data['total_salary']:,.0f}")
                report_data.append(f"  متوسط الأداء: {data['avg_performance']:.1f}%")
                report_data.append("")

            # حفظ التقرير
            self.save_report("تقرير_الأقسام", "\n".join(report_data))

        except Exception as e:
            print(f"❌ خطأ في إنشاء تقرير الأقسام: {e}")
            messagebox.showerror("خطأ", f"فشل في إنشاء تقرير الأقسام: {e}")

    def save_report(self, report_name, content):
        """حفظ التقرير"""
        try:
            # إنشاء مجلد التقارير
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)

            # اسم الملف مع التاريخ
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_name}_{timestamp}.txt"
            filepath = reports_dir / filename

            # حفظ التقرير
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            messagebox.showinfo("نجح", f"تم حفظ التقرير في:\n{filepath}")

        except Exception as e:
            print(f"❌ خطأ في حفظ التقرير: {e}")
            messagebox.showerror("خطأ", f"فشل في حفظ التقرير: {e}")

    # ==================== وظائف الرواتب المتقدمة ====================

    def show_salary_sheet(self):
        """عرض كشف الرواتب"""
        messagebox.showinfo("قريباً", "هذه الميزة ستكون متاحة قريباً")

    def create_payslip(self):
        """إنشاء كشف راتب"""
        messagebox.showinfo("قريباً", "هذه الميزة ستكون متاحة قريباً")

    def analyze_salaries(self):
        """تحليل الرواتب"""
        messagebox.showinfo("قريباً", "هذه الميزة ستكون متاحة قريباً")

    def export_salary_data(self):
        """تصدير بيانات الرواتب"""
        try:
            # إنشاء مجلد التصدير
            exports_dir = Path("exports")
            exports_dir.mkdir(exist_ok=True)

            # اسم الملف مع التاريخ
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"رواتب_الموظفين_{timestamp}.csv"
            filepath = exports_dir / filename

            # تصدير البيانات
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                import csv
                writer = csv.writer(f)

                # كتابة العناوين
                headers = ['الرقم', 'الاسم', 'القسم', 'المنصب', 'الراتب', 'الحالة', 'الأداء']
                writer.writerow(headers)

                # كتابة البيانات
                for emp in self.employees_data:
                    row = [
                        emp['employee_number'],
                        emp['name'],
                        emp['department'],
                        emp['position'],
                        emp['salary'],
                        emp['status'],
                        f"{emp['performance_score']:.0f}%"
                    ]
                    writer.writerow(row)

            messagebox.showinfo("نجح", f"تم تصدير البيانات إلى:\n{filepath}")

        except Exception as e:
            print(f"❌ خطأ في تصدير البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تصدير البيانات: {e}")

    # ==================== وظائف مساعدة ====================

    def get_hover_color(self, color):
        """الحصول على لون التمرير"""
        try:
            # تحويل اللون إلى RGB وتعتيمه قليلاً
            if color.startswith('#'):
                # إزالة # وتحويل إلى RGB
                hex_color = color[1:]
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                # تعتيم اللون بنسبة 20%
                darker_rgb = tuple(max(0, int(c * 0.8)) for c in rgb)
                return f"#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}"
            else:
                return color
        except:
            return color

    def on_window_close(self):
        """عند إغلاق النافذة"""
        try:
            # حفظ إعدادات النافذة
            self.save_window_settings()

            # إغلاق اتصال قاعدة البيانات
            if self.db_connection:
                self.db_connection.close()
                print("✅ تم إغلاق اتصال قاعدة البيانات")

            # إغلاق النافذة
            self.window.destroy()

        except Exception as e:
            print(f"❌ خطأ في إغلاق النافذة: {e}")
            self.window.destroy()

    def save_window_settings(self):
        """حفظ إعدادات النافذة المحسنة"""
        try:
            if self.window:
                # حفظ موقع وحجم النافذة
                geometry = self.window.geometry()

                # فحص حالة النافذة
                window_state = 'normal'
                try:
                    if self.window.state() == 'zoomed':
                        window_state = 'maximized'
                    elif self.window.attributes('-fullscreen'):
                        window_state = 'fullscreen'
                except:
                    pass

                settings = {
                    'geometry': geometry,
                    'window_state': window_state,
                    'last_used': datetime.now().isoformat(),
                    'screen_width': self.window.winfo_screenwidth(),
                    'screen_height': self.window.winfo_screenheight()
                }

                # حفظ في ملف JSON
                settings_file = Path("data/window_settings.json")
                with open(settings_file, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(settings, f, ensure_ascii=False, indent=2)

                print("✅ تم حفظ إعدادات النافذة المحسنة")
        except Exception as e:
            print(f"⚠️ فشل في حفظ إعدادات النافذة: {e}")

    def load_window_settings(self):
        """تحميل إعدادات النافذة المحسنة"""
        try:
            settings_file = Path("data/window_settings.json")
            if settings_file.exists():
                import json
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                if 'geometry' in settings:
                    # فحص إذا كانت الشاشة تغيرت
                    current_screen_width = self.window.winfo_screenwidth()
                    current_screen_height = self.window.winfo_screenheight()

                    saved_screen_width = settings.get('screen_width', current_screen_width)
                    saved_screen_height = settings.get('screen_height', current_screen_height)

                    # إذا تغيرت الشاشة، استخدم ملء الشاشة
                    if (saved_screen_width != current_screen_width or
                        saved_screen_height != current_screen_height):
                        print("⚠️ تغيرت أبعاد الشاشة - استخدام ملء الشاشة")
                        return False

                    # تطبيق الإعدادات المحفوظة
                    self.window.geometry(settings['geometry'])

                    # تطبيق حالة النافذة
                    window_state = settings.get('window_state', 'normal')
                    if window_state == 'maximized':
                        self.window.after(100, self.maximize_window)
                    elif window_state == 'fullscreen':
                        self.window.after(100, self.toggle_fullscreen)

                    print("✅ تم تحميل إعدادات النافذة المحسنة")
                    return True
        except Exception as e:
            print(f"⚠️ فشل في تحميل إعدادات النافذة: {e}")

        return False

    def create_database_backup(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            # إنشاء مجلد النسخ الاحتياطية
            backups_dir = Path("backups")
            backups_dir.mkdir(exist_ok=True)

            # اسم ملف النسخة الاحتياطية
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"employees_backup_{timestamp}.db"
            backup_path = backups_dir / backup_filename

            # نسخ قاعدة البيانات
            import shutil
            db_path = Path("data/unified_employees.db")
            if db_path.exists():
                shutil.copy2(db_path, backup_path)
                print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
                return backup_path
            else:
                print("❌ ملف قاعدة البيانات غير موجود")
                return None

        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return None

    def auto_backup_database(self):
        """إنشاء نسخة احتياطية تلقائية"""
        try:
            # فحص آخر نسخة احتياطية
            backups_dir = Path("backups")
            if backups_dir.exists():
                backup_files = list(backups_dir.glob("employees_backup_*.db"))
                if backup_files:
                    # الحصول على أحدث نسخة احتياطية
                    latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
                    backup_age = datetime.now().timestamp() - latest_backup.stat().st_mtime

                    # إنشاء نسخة احتياطية جديدة إذا مر أكثر من يوم
                    if backup_age > 86400:  # 24 ساعة
                        self.create_database_backup()
                        print("✅ تم إنشاء نسخة احتياطية تلقائية")
                else:
                    # إنشاء أول نسخة احتياطية
                    self.create_database_backup()
                    print("✅ تم إنشاء أول نسخة احتياطية")
            else:
                # إنشاء أول نسخة احتياطية
                self.create_database_backup()
                print("✅ تم إنشاء أول نسخة احتياطية")

        except Exception as e:
            print(f"⚠️ فشل في النسخ الاحتياطي التلقائي: {e}")

    def run(self):
        """تشغيل النافذة"""
        try:
            if self.window:
                self.window.mainloop()
        except Exception as e:
            print(f"❌ خطأ في تشغيل النافذة: {e}")

# ==================== دالة التشغيل الرئيسية ====================

def main():
    """الدالة الرئيسية لتشغيل النظام الموحد"""
    try:
        print("🚀 بدء تشغيل نظام إدارة الموظفين الموحد...")

        # إنشاء النظام الموحد
        unified_system = UnifiedEmployeesManagement()

        # تشغيل النظام
        unified_system.run()

    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {e}")
        traceback.print_exc()
        messagebox.showerror("خطأ فادح", f"فشل في تشغيل النظام:\n{e}")

if __name__ == "__main__":
    main()
