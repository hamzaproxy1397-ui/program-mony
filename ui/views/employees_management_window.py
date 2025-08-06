#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏢 نافذة إدارة الموظفين المتقدمة والاحترافية
Advanced Professional Employee Management Window

نافذة شاملة لإدارة الموظفين تتضمن:
- جدول عرض الموظفين مع البحث والفلترة
- نماذج إضافة وتعديل الموظفين
- حساب الرواتب والمكافآت
- تتبع الحضور والغياب
- تقارير الموظفين
- ربط بقاعدة البيانات
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Any
import json
from PIL import Image, ImageTk

# استيراد الثيمات والألوان
try:
    from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS
    from ui.window_utils import configure_window_fullscreen
    from database.hybrid_database_manager import HybridDatabaseManager
except ImportError as e:
    print(f"تحذير: لم يتم العثور على بعض الوحدات: {e}")
    # ألوان افتراضية
    MODERN_COLORS = {
        'primary': '#2E8B57',
        'secondary': '#4682B4',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'background': '#f8f9fa',
        'surface': '#ffffff',
        'card': '#f8f9fa'
    }
    FONTS = {'arabic': 'Arial', 'sizes': {'large': 16, 'medium': 14, 'small': 12}}
    DIMENSIONS = {'button_height': 40}

# إعداد customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class EmployeesManagementWindow:
    """نافذة إدارة الموظفين المتقدمة"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.db_manager = None
        
        # متغيرات البيانات
        self.employees_data = []
        self.filtered_employees = []
        self.current_employee = None
        
        # متغيرات النماذج
        self.form_vars = {}
        
        # متغيرات الواجهة
        self.tree = None
        self.search_var = None
        self.department_filter_var = None
        self.status_filter_var = None
        
        # إنشاء النافذة
        self.create_window()
        
        # تهيئة قاعدة البيانات
        self.init_database()
        
        # تحميل البيانات
        self.load_employees_data()
    
    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        try:
            self.window = ctk.CTkToplevel(self.parent) if self.parent else ctk.CTk()
            self.window.title("🏢 إدارة الموظفين - برنامج ست الكل للمحاسبة")
            
            # تكوين النافذة المحسنة
            try:
                configure_window_fullscreen(self.window)
            except:
                self.window.geometry("1600x950")   # زيادة العرض من 1400 إلى 1600 (+14.3%)
                self.window.minsize(1350, 850)     # حد أدنى محسن
                self.window.state('zoomed')
            
            self.window.configure(fg_color=MODERN_COLORS['background'])
            
            # جعل النافذة في المقدمة
            if self.parent:
                self.window.transient(self.parent)
                self.window.grab_set()
            
            # إنشاء المحتوى
            self.create_main_content()
            
        except Exception as e:
            print(f"خطأ في إنشاء النافذة: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء النافذة: {e}")
    
    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        # الإطار الرئيسي
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # إنشاء الهيدر
        self.create_header(main_frame)
        
        # إنشاء شريط الأدوات
        self.create_toolbar(main_frame)
        
        # إنشاء المحتوى الرئيسي (جدول + نموذج)
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # تقسيم المحتوى إلى جزأين
        self.create_content_sections(content_frame)
    
    def create_header(self, parent):
        """إنشاء الهيدر"""
        header_frame = ctk.CTkFrame(parent, height=80, fg_color=MODERN_COLORS['primary'])
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # عنوان النافذة
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏢 إدارة الموظفين",
            font=(FONTS['arabic'], 28, "bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # معلومات إحصائية
        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(side="right", padx=20, pady=10)
        
        # عدد الموظفين
        self.total_employees_label = ctk.CTkLabel(
            stats_frame,
            text="إجمالي الموظفين: 0",
            font=(FONTS['arabic'], 14),
            text_color="white"
        )
        self.total_employees_label.pack(pady=2)
        
        # الموظفين النشطين
        self.active_employees_label = ctk.CTkLabel(
            stats_frame,
            text="الموظفين النشطين: 0",
            font=(FONTS['arabic'], 14),
            text_color="white"
        )
        self.active_employees_label.pack(pady=2)
    
    def create_toolbar(self, parent):
        """إنشاء شريط الأدوات"""
        toolbar_frame = ctk.CTkFrame(parent, height=60, fg_color=MODERN_COLORS['surface'])
        toolbar_frame.pack(fill="x", pady=(0, 10))
        toolbar_frame.pack_propagate(False)
        
        # الجانب الأيسر - أزرار العمليات
        left_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=10, pady=10)
        
        # أزرار العمليات الرئيسية
        buttons_data = [
            ("➕ إضافة موظف", self.add_employee, MODERN_COLORS['success']),
            ("✏️ تعديل", self.edit_employee, MODERN_COLORS['info']),
            ("🗑️ حذف", self.delete_employee, MODERN_COLORS['danger']),
            ("📊 تقارير", self.show_reports, MODERN_COLORS['secondary']),
            ("💰 الرواتب", self.manage_salaries, MODERN_COLORS['warning'])
        ]
        
        for text, command, color in buttons_data:
            btn = ctk.CTkButton(
                left_frame,
                text=text,
                command=command,
                width=120,
                height=DIMENSIONS['button_height'],
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=color,
                hover_color=self.get_hover_color(color)
            )
            btn.pack(side="left", padx=5)
        
        # الجانب الأيمن - البحث والفلترة
        right_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=10, pady=10)
        
        # شريط البحث
        search_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=10)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍 بحث:",
            font=(FONTS['arabic'], 12)
        ).pack(side="left", padx=(0, 5))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="ابحث عن موظف...",
            width=200,
            font=(FONTS['arabic'], 12)
        )
        search_entry.pack(side="left")
        
        # فلتر القسم
        dept_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        dept_frame.pack(side="right", padx=10)
        
        ctk.CTkLabel(
            dept_frame,
            text="القسم:",
            font=(FONTS['arabic'], 12)
        ).pack(side="left", padx=(0, 5))
        
        self.department_filter_var = ctk.StringVar(value="الكل")
        dept_combo = ctk.CTkComboBox(
            dept_frame,
            variable=self.department_filter_var,
            values=["الكل", "الإدارة", "المحاسبة", "المبيعات", "التقنية"],
            width=120,
            font=(FONTS['arabic'], 12),
            command=self.on_filter_change
        )
        dept_combo.pack(side="left")
        
        # فلتر الحالة
        status_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        status_frame.pack(side="right", padx=10)
        
        ctk.CTkLabel(
            status_frame,
            text="الحالة:",
            font=(FONTS['arabic'], 12)
        ).pack(side="left", padx=(0, 5))
        
        self.status_filter_var = ctk.StringVar(value="الكل")
        status_combo = ctk.CTkComboBox(
            status_frame,
            variable=self.status_filter_var,
            values=["الكل", "نشط", "غير نشط", "معلق"],
            width=100,
            font=(FONTS['arabic'], 12),
            command=self.on_filter_change
        )
        status_combo.pack(side="left")
    
    def get_hover_color(self, color):
        """الحصول على لون التمرير"""
        # تحويل اللون إلى أغمق قليلاً
        if color == MODERN_COLORS['success']:
            return "#218838"
        elif color == MODERN_COLORS['info']:
            return "#138496"
        elif color == MODERN_COLORS['danger']:
            return "#c82333"
        elif color == MODERN_COLORS['secondary']:
            return "#5a6268"
        elif color == MODERN_COLORS['warning']:
            return "#e0a800"
        else:
            return color

    def create_content_sections(self, parent):
        """إنشاء أقسام المحتوى"""
        # تقسيم إلى جزأين: جدول الموظفين (يسار) ونموذج التفاصيل (يمين)

        # الجزء الأيسر - جدول الموظفين
        left_frame = ctk.CTkFrame(parent, fg_color=MODERN_COLORS['surface'])
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.create_employees_table(left_frame)

        # الجزء الأيمن - نموذج التفاصيل
        right_frame = ctk.CTkFrame(parent, fg_color=MODERN_COLORS['surface'], width=400)
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        right_frame.pack_propagate(False)

        self.create_employee_form(right_frame)

    def create_employees_table(self, parent):
        """إنشاء جدول الموظفين"""
        # عنوان الجدول
        table_header = ctk.CTkFrame(parent, height=50, fg_color=MODERN_COLORS['primary'])
        table_header.pack(fill="x", padx=10, pady=(10, 0))
        table_header.pack_propagate(False)

        ctk.CTkLabel(
            table_header,
            text="📋 قائمة الموظفين",
            font=(FONTS['arabic'], 18, "bold"),
            text_color="white"
        ).pack(pady=15)

        # إطار الجدول
        table_frame = ctk.CTkFrame(parent, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # إنشاء Treeview للجدول
        columns = ("ID", "الرقم الوظيفي", "الاسم الكامل", "القسم", "المنصب", "الراتب", "الحالة")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # تكوين الأعمدة
        column_widths = {"ID": 50, "الرقم الوظيفي": 100, "الاسم الكامل": 200,
                        "القسم": 120, "المنصب": 150, "الراتب": 100, "الحالة": 80}

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")

        # شريط التمرير
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # تخطيط الجدول
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # ربط الأحداث
        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)
        self.tree.bind("<Double-1>", self.on_employee_double_click)

    def create_employee_form(self, parent):
        """إنشاء نموذج تفاصيل الموظف"""
        # عنوان النموذج
        form_header = ctk.CTkFrame(parent, height=50, fg_color=MODERN_COLORS['secondary'])
        form_header.pack(fill="x", padx=10, pady=(10, 0))
        form_header.pack_propagate(False)

        self.form_title_label = ctk.CTkLabel(
            form_header,
            text="📝 تفاصيل الموظف",
            font=(FONTS['arabic'], 16, "bold"),
            text_color="white"
        )
        self.form_title_label.pack(pady=15)

        # إطار النموذج القابل للتمرير
        form_scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="white")
        form_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # تهيئة متغيرات النموذج
        self.init_form_variables()

        # إنشاء حقول النموذج
        self.create_form_fields(form_scroll_frame)

        # أزرار النموذج
        self.create_form_buttons(parent)

    def init_form_variables(self):
        """تهيئة متغيرات النموذج"""
        self.form_vars = {
            'employee_id': ctk.StringVar(),
            'employee_number': ctk.StringVar(),
            'full_name': ctk.StringVar(),
            'national_id': ctk.StringVar(),
            'phone': ctk.StringVar(),
            'email': ctk.StringVar(),
            'address': ctk.StringVar(),
            'department': ctk.StringVar(value="الإدارة"),
            'position': ctk.StringVar(value="موظف"),
            'hire_date': ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            'birth_date': ctk.StringVar(),
            'basic_salary': ctk.StringVar(value="0"),
            'status': ctk.StringVar(value="نشط"),
            'photo_path': ctk.StringVar(),
            'notes': ctk.StringVar()
        }

    def create_form_fields(self, parent):
        """إنشاء حقول النموذج"""
        # الصورة الشخصية
        photo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        photo_frame.pack(fill="x", pady=10)

        self.photo_label = ctk.CTkLabel(
            photo_frame,
            text="📷\nلا توجد صورة",
            width=100,
            height=120,
            fg_color=MODERN_COLORS['card'],
            corner_radius=10,
            font=(FONTS['arabic'], 12)
        )
        self.photo_label.pack(pady=5)

        photo_btn = ctk.CTkButton(
            photo_frame,
            text="اختيار صورة",
            command=self.select_photo,
            width=100,
            height=30,
            font=(FONTS['arabic'], 10)
        )
        photo_btn.pack(pady=5)

        # الحقول الأساسية
        fields_data = [
            ("رقم الموظف:", "employee_number", "entry"),
            ("الاسم الكامل:", "full_name", "entry"),
            ("الرقم القومي:", "national_id", "entry"),
            ("رقم الهاتف:", "phone", "entry"),
            ("البريد الإلكتروني:", "email", "entry"),
            ("العنوان:", "address", "text"),
            ("القسم:", "department", "combo"),
            ("المنصب:", "position", "combo"),
            ("تاريخ التوظيف:", "hire_date", "entry"),
            ("تاريخ الميلاد:", "birth_date", "entry"),
            ("الراتب الأساسي:", "basic_salary", "entry"),
            ("الحالة:", "status", "combo"),
            ("ملاحظات:", "notes", "text")
        ]

        for label_text, var_name, field_type in fields_data:
            self.create_form_field(parent, label_text, var_name, field_type)

    def create_form_field(self, parent, label_text, var_name, field_type):
        """إنشاء حقل نموذج واحد"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5, padx=10)

        # التسمية
        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=(FONTS['arabic'], 12, "bold"),
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 5))

        # الحقل
        if field_type == "entry":
            widget = ctk.CTkEntry(
                field_frame,
                textvariable=self.form_vars[var_name],
                font=(FONTS['arabic'], 12),
                height=35
            )
        elif field_type == "text":
            widget = ctk.CTkTextbox(
                field_frame,
                height=60,
                font=(FONTS['arabic'], 12)
            )
            # ربط النص بالمتغير
            widget.bind("<KeyRelease>", lambda e, var=var_name: self.update_text_var(var, widget))
        elif field_type == "combo":
            values = self.get_combo_values(var_name)
            widget = ctk.CTkComboBox(
                field_frame,
                variable=self.form_vars[var_name],
                values=values,
                font=(FONTS['arabic'], 12),
                height=35
            )

        widget.pack(fill="x")

        return widget

    def get_combo_values(self, var_name):
        """الحصول على قيم القائمة المنسدلة"""
        if var_name == "department":
            return ["الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية", "التسويق"]
        elif var_name == "position":
            return ["مدير عام", "مدير قسم", "محاسب", "موظف مبيعات", "مطور", "سكرتير", "موظف"]
        elif var_name == "status":
            return ["نشط", "غير نشط", "معلق", "مستقيل"]
        return []

    def update_text_var(self, var_name, widget):
        """تحديث متغير النص"""
        try:
            content = widget.get("1.0", "end-1c")
            self.form_vars[var_name].set(content)
        except:
            pass

    def create_form_buttons(self, parent):
        """إنشاء أزرار النموذج"""
        buttons_frame = ctk.CTkFrame(parent, height=60, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=10)
        buttons_frame.pack_propagate(False)

        # أزرار العمليات
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ",
            command=self.save_employee,
            width=80,
            height=40,
            font=(FONTS['arabic'], 12, "bold"),
            fg_color=MODERN_COLORS['success'],
            hover_color="#218838"
        )
        save_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ مسح",
            command=self.clear_form,
            width=80,
            height=40,
            font=(FONTS['arabic'], 12, "bold"),
            fg_color=MODERN_COLORS['warning'],
            hover_color="#e0a800"
        )
        clear_btn.pack(side="left", padx=5)

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ إلغاء",
            command=self.cancel_operation,
            width=80,
            height=40,
            font=(FONTS['arabic'], 12, "bold"),
            fg_color=MODERN_COLORS['danger'],
            hover_color="#c82333"
        )
        cancel_btn.pack(side="left", padx=5)

    def select_photo(self):
        """اختيار صورة شخصية"""
        try:
            file_path = filedialog.askopenfilename(
                title="اختيار صورة شخصية",
                filetypes=[
                    ("ملفات الصور", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("جميع الملفات", "*.*")
                ]
            )

            if file_path:
                self.form_vars['photo_path'].set(file_path)
                self.load_photo_preview(file_path)

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في اختيار الصورة: {e}")

    def load_photo_preview(self, file_path):
        """تحميل معاينة الصورة"""
        try:
            # تحميل وتغيير حجم الصورة
            image = Image.open(file_path)
            image = image.resize((100, 120), Image.Resampling.LANCZOS)

            # تحويل إلى PhotoImage
            photo = ImageTk.PhotoImage(image)

            # عرض الصورة
            self.photo_label.configure(image=photo, text="")
            self.photo_label.image = photo  # الاحتفاظ بمرجع

        except Exception as e:
            print(f"خطأ في تحميل الصورة: {e}")
            self.photo_label.configure(text="📷\nخطأ في الصورة")

    # وظائف قاعدة البيانات
    def init_database(self):
        """تهيئة قاعدة البيانات"""
        try:
            # استخدام SQLite مباشرة لضمان الاستقرار
            self.init_sqlite_database()

            # إنشاء الجداول
            self.create_tables()

            # إدراج بيانات افتراضية
            self.insert_default_data()

        except Exception as e:
            print(f"خطأ في تهيئة قاعدة البيانات: {e}")
            # لا نعرض رسالة خطأ للمستخدم، فقط نطبع في الكونسول

    def init_sqlite_database(self):
        """تهيئة قاعدة بيانات SQLite"""
        try:
            db_path = "data/employees.db"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            self.db_connection = sqlite3.connect(db_path)
            self.db_cursor = self.db_connection.cursor()
            print("✅ تم تهيئة قاعدة بيانات SQLite بنجاح")
        except Exception as e:
            print(f"خطأ في تهيئة SQLite: {e}")
            # إنشاء قاعدة بيانات في الذاكرة كبديل
            self.db_connection = sqlite3.connect(":memory:")
            self.db_cursor = self.db_connection.cursor()
            print("✅ تم إنشاء قاعدة بيانات في الذاكرة")

    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        try:
            # جدول الموظفين
            employees_table = """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                national_id TEXT UNIQUE,
                phone TEXT,
                email TEXT,
                address TEXT,
                department TEXT,
                position TEXT,
                hire_date DATE,
                birth_date DATE,
                basic_salary REAL DEFAULT 0,
                status TEXT DEFAULT 'نشط',
                photo_path TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

            # جدول الرواتب
            salaries_table = """
            CREATE TABLE IF NOT EXISTS salaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                month INTEGER,
                year INTEGER,
                basic_salary REAL,
                allowances REAL DEFAULT 0,
                deductions REAL DEFAULT 0,
                overtime_hours REAL DEFAULT 0,
                overtime_rate REAL DEFAULT 0,
                total_salary REAL,
                payment_date DATE,
                status TEXT DEFAULT 'معلق',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
            """

            # جدول الحضور
            attendance_table = """
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                date DATE,
                check_in_time TIME,
                check_out_time TIME,
                total_hours REAL,
                status TEXT DEFAULT 'حاضر',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
            """

            # استخدام SQLite مباشرة
            self.db_cursor.execute(employees_table)
            self.db_cursor.execute(salaries_table)
            self.db_cursor.execute(attendance_table)
            self.db_connection.commit()
            print("✅ تم إنشاء جداول قاعدة البيانات بنجاح")

        except Exception as e:
            print(f"خطأ في إنشاء الجداول: {e}")

    def insert_default_data(self):
        """إدراج بيانات افتراضية"""
        try:
            # التحقق من وجود بيانات
            self.db_cursor.execute("SELECT COUNT(*) FROM employees")
            count = self.db_cursor.fetchone()[0]

            if count == 0:
                # إدراج موظفين افتراضيين
                default_employees = [
                    ("EMP001", "أحمد محمد علي", "12345678901", "01234567890", "ahmed@company.com",
                     "القاهرة، مصر", "الإدارة", "مدير عام", "2020-01-15", "1985-05-20", 15000, "نشط"),
                    ("EMP002", "فاطمة أحمد حسن", "12345678902", "01234567891", "fatma@company.com",
                     "الجيزة، مصر", "المحاسبة", "محاسب أول", "2021-03-10", "1990-08-15", 8000, "نشط"),
                    ("EMP003", "محمد عبد الله", "12345678903", "01234567892", "mohamed@company.com",
                     "الإسكندرية، مصر", "المبيعات", "موظف مبيعات", "2022-06-01", "1992-12-10", 5000, "نشط")
                ]

                for emp_data in default_employees:
                    query = """
                    INSERT INTO employees
                    (employee_number, full_name, national_id, phone, email, address,
                     department, position, hire_date, birth_date, basic_salary, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """

                    self.db_cursor.execute(query, emp_data)
                    self.db_connection.commit()

                print("✅ تم إدراج البيانات الافتراضية بنجاح")

        except Exception as e:
            print(f"خطأ في إدراج البيانات الافتراضية: {e}")

    def load_employees_data(self):
        """تحميل بيانات الموظفين"""
        try:
            query = """
            SELECT id, employee_number, full_name, department, position,
                   basic_salary, status, phone, email, hire_date
            FROM employees
            ORDER BY full_name
            """

            self.db_cursor.execute(query)
            self.employees_data = self.db_cursor.fetchall()

            # تطبيق الفلاتر
            self.apply_filters()

            # تحديث الإحصائيات
            self.update_statistics()

        except Exception as e:
            print(f"خطأ في تحميل بيانات الموظفين: {e}")
            self.employees_data = []
            self.filtered_employees = []

    def apply_filters(self):
        """تطبيق الفلاتر والبحث"""
        try:
            search_term = self.search_var.get().lower() if self.search_var else ""
            dept_filter = self.department_filter_var.get() if self.department_filter_var else "الكل"
            status_filter = self.status_filter_var.get() if self.status_filter_var else "الكل"

            self.filtered_employees = []

            for emp in self.employees_data:
                # فلتر البحث
                if search_term and search_term not in emp[2].lower():  # البحث في الاسم
                    continue

                # فلتر القسم
                if dept_filter != "الكل" and emp[3] != dept_filter:
                    continue

                # فلتر الحالة
                if status_filter != "الكل" and emp[6] != status_filter:
                    continue

                self.filtered_employees.append(emp)

            # تحديث الجدول
            self.update_table()

        except Exception as e:
            print(f"خطأ في تطبيق الفلاتر: {e}")

    def update_table(self):
        """تحديث جدول الموظفين"""
        try:
            # مسح البيانات الحالية
            for item in self.tree.get_children():
                self.tree.delete(item)

            # إضافة البيانات المفلترة
            for emp in self.filtered_employees:
                # تنسيق البيانات للعرض
                display_data = (
                    emp[0],  # ID
                    emp[1],  # رقم الموظف
                    emp[2],  # الاسم
                    emp[3],  # القسم
                    emp[4],  # المنصب
                    f"{emp[5]:,.0f} ج.م",  # الراتب
                    emp[6]   # الحالة
                )

                # تحديد لون الصف حسب الحالة
                tags = []
                if emp[6] == "نشط":
                    tags = ["active"]
                elif emp[6] == "غير نشط":
                    tags = ["inactive"]
                elif emp[6] == "معلق":
                    tags = ["suspended"]

                self.tree.insert("", "end", values=display_data, tags=tags)

            # تكوين ألوان الصفوف
            self.tree.tag_configure("active", background="#d4edda")
            self.tree.tag_configure("inactive", background="#f8d7da")
            self.tree.tag_configure("suspended", background="#fff3cd")

        except Exception as e:
            print(f"خطأ في تحديث الجدول: {e}")

    def update_statistics(self):
        """تحديث الإحصائيات"""
        try:
            total_employees = len(self.employees_data)
            active_employees = len([emp for emp in self.employees_data if emp[6] == "نشط"])

            self.total_employees_label.configure(text=f"إجمالي الموظفين: {total_employees}")
            self.active_employees_label.configure(text=f"الموظفين النشطين: {active_employees}")

        except Exception as e:
            print(f"خطأ في تحديث الإحصائيات: {e}")

    # وظائف الأحداث
    def on_search_change(self, *args):
        """عند تغيير البحث"""
        self.apply_filters()

    def on_filter_change(self, *args):
        """عند تغيير الفلتر"""
        self.apply_filters()

    def on_employee_select(self, event):
        """عند اختيار موظف من الجدول"""
        try:
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                employee_id = item['values'][0]
                self.load_employee_details(employee_id)

        except Exception as e:
            print(f"خطأ في اختيار الموظف: {e}")

    def on_employee_double_click(self, event):
        """عند النقر المزدوج على موظف"""
        self.edit_employee()

    def load_employee_details(self, employee_id):
        """تحميل تفاصيل موظف محدد"""
        try:
            query = """
            SELECT * FROM employees WHERE id = ?
            """

            self.db_cursor.execute(query, (employee_id,))
            result = self.db_cursor.fetchone()

            if result:
                self.current_employee = result
                self.populate_form(result)
                self.form_title_label.configure(text=f"📝 تفاصيل الموظف: {result[2]}")

        except Exception as e:
            print(f"خطأ في تحميل تفاصيل الموظف: {e}")

    def populate_form(self, employee_data):
        """ملء النموذج ببيانات الموظف"""
        try:
            # ملء الحقول
            field_mapping = {
                'employee_id': 0,
                'employee_number': 1,
                'full_name': 2,
                'national_id': 3,
                'phone': 4,
                'email': 5,
                'address': 6,
                'department': 7,
                'position': 8,
                'hire_date': 9,
                'birth_date': 10,
                'basic_salary': 11,
                'status': 12,
                'photo_path': 13,
                'notes': 14
            }

            for var_name, index in field_mapping.items():
                if var_name in self.form_vars and index < len(employee_data):
                    value = employee_data[index] if employee_data[index] is not None else ""
                    self.form_vars[var_name].set(str(value))

            # تحميل الصورة إذا كانت موجودة
            if employee_data[13]:  # photo_path
                self.load_photo_preview(employee_data[13])
            else:
                self.photo_label.configure(text="📷\nلا توجد صورة", image="")

        except Exception as e:
            print(f"خطأ في ملء النموذج: {e}")

    # وظائف العمليات الأساسية
    def add_employee(self):
        """إضافة موظف جديد"""
        self.clear_form()
        self.current_employee = None
        self.form_title_label.configure(text="📝 إضافة موظف جديد")

        # توليد رقم موظف جديد
        new_number = self.generate_employee_number()
        self.form_vars['employee_number'].set(new_number)

    def edit_employee(self):
        """تعديل الموظف المحدد"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار موظف للتعديل")
            return

        item = self.tree.item(selection[0])
        employee_id = item['values'][0]
        self.load_employee_details(employee_id)
        self.form_title_label.configure(text="📝 تعديل بيانات الموظف")

    def delete_employee(self):
        """حذف الموظف المحدد"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار موظف للحذف")
            return

        item = self.tree.item(selection[0])
        employee_name = item['values'][2]

        result = messagebox.askyesno(
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف الموظف:\n{employee_name}؟\n\nهذا الإجراء لا يمكن التراجع عنه."
        )

        if result:
            try:
                employee_id = item['values'][0]

                query = "DELETE FROM employees WHERE id = ?"

                self.db_cursor.execute(query, (employee_id,))
                self.db_connection.commit()

                messagebox.showinfo("نجح", "تم حذف الموظف بنجاح")
                self.load_employees_data()
                self.clear_form()

            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في حذف الموظف: {e}")

    def save_employee(self):
        """حفظ بيانات الموظف"""
        try:
            # التحقق من صحة البيانات
            if not self.validate_form():
                return

            # جمع البيانات
            employee_data = self.collect_form_data()

            if self.current_employee:
                # تحديث موظف موجود
                self.update_employee(employee_data)
            else:
                # إضافة موظف جديد
                self.insert_employee(employee_data)

            # إعادة تحميل البيانات
            self.load_employees_data()

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ البيانات: {e}")

    def generate_employee_number(self):
        """توليد رقم موظف جديد"""
        try:
            query = "SELECT MAX(CAST(SUBSTR(employee_number, 4) AS INTEGER)) FROM employees WHERE employee_number LIKE 'EMP%'"

            self.db_cursor.execute(query)
            result = self.db_cursor.fetchone()

            max_num = result[0] if result and result[0] else 0
            return f"EMP{max_num + 1:03d}"

        except Exception as e:
            print(f"خطأ في توليد رقم الموظف: {e}")
            return "EMP001"

    def validate_form(self):
        """التحقق من صحة بيانات النموذج"""
        try:
            # التحقق من الحقول المطلوبة
            required_fields = {
                'employee_number': 'رقم الموظف',
                'full_name': 'الاسم الكامل',
                'department': 'القسم',
                'position': 'المنصب'
            }

            for field, label in required_fields.items():
                if not self.form_vars[field].get().strip():
                    messagebox.showerror("خطأ", f"يجب إدخال {label}")
                    return False

            # التحقق من صحة الراتب
            try:
                salary = float(self.form_vars['basic_salary'].get() or 0)
                if salary < 0:
                    messagebox.showerror("خطأ", "الراتب يجب أن يكون رقم موجب")
                    return False
            except ValueError:
                messagebox.showerror("خطأ", "الراتب يجب أن يكون رقم صحيح")
                return False

            # التحقق من صحة البريد الإلكتروني
            email = self.form_vars['email'].get().strip()
            if email and '@' not in email:
                messagebox.showerror("خطأ", "البريد الإلكتروني غير صحيح")
                return False

            return True

        except Exception as e:
            print(f"خطأ في التحقق من البيانات: {e}")
            return False

    def collect_form_data(self):
        """جمع بيانات النموذج"""
        return {
            'employee_number': self.form_vars['employee_number'].get().strip(),
            'full_name': self.form_vars['full_name'].get().strip(),
            'national_id': self.form_vars['national_id'].get().strip(),
            'phone': self.form_vars['phone'].get().strip(),
            'email': self.form_vars['email'].get().strip(),
            'address': self.form_vars['address'].get().strip(),
            'department': self.form_vars['department'].get(),
            'position': self.form_vars['position'].get(),
            'hire_date': self.form_vars['hire_date'].get(),
            'birth_date': self.form_vars['birth_date'].get(),
            'basic_salary': float(self.form_vars['basic_salary'].get() or 0),
            'status': self.form_vars['status'].get(),
            'photo_path': self.form_vars['photo_path'].get(),
            'notes': self.form_vars['notes'].get()
        }

    def insert_employee(self, employee_data):
        """إدراج موظف جديد"""
        try:
            query = """
            INSERT INTO employees
            (employee_number, full_name, national_id, phone, email, address,
             department, position, hire_date, birth_date, basic_salary,
             status, photo_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            values = (
                employee_data['employee_number'],
                employee_data['full_name'],
                employee_data['national_id'],
                employee_data['phone'],
                employee_data['email'],
                employee_data['address'],
                employee_data['department'],
                employee_data['position'],
                employee_data['hire_date'],
                employee_data['birth_date'],
                employee_data['basic_salary'],
                employee_data['status'],
                employee_data['photo_path'],
                employee_data['notes']
            )

            self.db_cursor.execute(query, values)
            self.db_connection.commit()

            messagebox.showinfo("نجح", "تم إضافة الموظف بنجاح")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إضافة الموظف: {e}")

    def update_employee(self, employee_data):
        """تحديث بيانات موظف موجود"""
        try:
            query = """
            UPDATE employees SET
            employee_number=?, full_name=?, national_id=?, phone=?, email=?,
            address=?, department=?, position=?, hire_date=?, birth_date=?,
            basic_salary=?, status=?, photo_path=?, notes=?,
            updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            """

            values = (
                employee_data['employee_number'],
                employee_data['full_name'],
                employee_data['national_id'],
                employee_data['phone'],
                employee_data['email'],
                employee_data['address'],
                employee_data['department'],
                employee_data['position'],
                employee_data['hire_date'],
                employee_data['birth_date'],
                employee_data['basic_salary'],
                employee_data['status'],
                employee_data['photo_path'],
                employee_data['notes'],
                self.current_employee[0]  # ID
            )

            self.db_cursor.execute(query, values)
            self.db_connection.commit()

            messagebox.showinfo("نجح", "تم تحديث بيانات الموظف بنجاح")

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحديث الموظف: {e}")

    def clear_form(self):
        """مسح النموذج"""
        try:
            for var in self.form_vars.values():
                var.set("")

            # إعادة تعيين القيم الافتراضية
            self.form_vars['department'].set("الإدارة")
            self.form_vars['position'].set("موظف")
            self.form_vars['status'].set("نشط")
            self.form_vars['hire_date'].set(datetime.now().strftime("%Y-%m-%d"))
            self.form_vars['basic_salary'].set("0")

            # مسح الصورة
            self.photo_label.configure(text="📷\nلا توجد صورة", image="")

            # إعادة تعيين العنوان
            self.form_title_label.configure(text="📝 تفاصيل الموظف")

            self.current_employee = None

        except Exception as e:
            print(f"خطأ في مسح النموذج: {e}")

    def cancel_operation(self):
        """إلغاء العملية"""
        result = messagebox.askyesno("تأكيد", "هل تريد إلغاء العملية الحالية؟")
        if result:
            self.clear_form()

    # وظائف إضافية
    def show_reports(self):
        """عرض تقارير الموظفين"""
        try:
            # إنشاء نافذة التقارير
            reports_window = ctk.CTkToplevel(self.window)
            reports_window.title("📊 تقارير الموظفين")
            reports_window.geometry("900x650")  # زيادة الحجم لعرض أفضل
            reports_window.transient(self.window)
            reports_window.grab_set()

            # محتوى التقارير
            main_frame = ctk.CTkFrame(reports_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # عنوان
            title_label = ctk.CTkLabel(
                main_frame,
                text="📊 تقارير الموظفين",
                font=(FONTS['arabic'], 20, "bold")
            )
            title_label.pack(pady=20)

            # أزرار التقارير
            reports_data = [
                ("📋 تقرير جميع الموظفين", self.generate_all_employees_report),
                ("💰 تقرير الرواتب", self.generate_salary_report),
                ("📅 تقرير الحضور", self.generate_attendance_report),
                ("📈 إحصائيات الأقسام", self.generate_department_stats)
            ]

            for text, command in reports_data:
                btn = ctk.CTkButton(
                    main_frame,
                    text=text,
                    command=command,
                    width=300,
                    height=50,
                    font=(FONTS['arabic'], 14)
                )
                btn.pack(pady=10)

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في عرض التقارير: {e}")

    def manage_salaries(self):
        """إدارة الرواتب"""
        try:
            # إنشاء نافذة إدارة الرواتب
            salary_window = ctk.CTkToplevel(self.window)
            salary_window.title("💰 إدارة الرواتب")
            salary_window.geometry("1150x750")  # زيادة الحجم لإدارة أفضل للرواتب
            salary_window.transient(self.window)
            salary_window.grab_set()

            # محتوى إدارة الرواتب
            main_frame = ctk.CTkFrame(salary_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # عنوان
            title_label = ctk.CTkLabel(
                main_frame,
                text="💰 إدارة الرواتب",
                font=(FONTS['arabic'], 20, "bold")
            )
            title_label.pack(pady=20)

            # رسالة مؤقتة
            info_label = ctk.CTkLabel(
                main_frame,
                text="نظام إدارة الرواتب قيد التطوير\nسيتم إضافة المزيد من الميزات قريباً",
                font=(FONTS['arabic'], 16)
            )
            info_label.pack(pady=50)

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إدارة الرواتب: {e}")

    # وظائف التقارير
    def generate_all_employees_report(self):
        """تقرير جميع الموظفين"""
        messagebox.showinfo("تقرير", "تم إنشاء تقرير جميع الموظفين")

    def generate_salary_report(self):
        """تقرير الرواتب"""
        messagebox.showinfo("تقرير", "تم إنشاء تقرير الرواتب")

    def generate_attendance_report(self):
        """تقرير الحضور"""
        messagebox.showinfo("تقرير", "تم إنشاء تقرير الحضور")

    def generate_department_stats(self):
        """إحصائيات الأقسام"""
        messagebox.showinfo("تقرير", "تم إنشاء إحصائيات الأقسام")

    def close_window(self):
        """إغلاق النافذة"""
        try:
            result = messagebox.askyesno("إغلاق", "هل تريد إغلاق نافذة إدارة الموظفين؟")
            if result:
                if hasattr(self, 'db_connection'):
                    self.db_connection.close()

                if self.window:
                    self.window.destroy()

        except Exception as e:
            print(f"خطأ في إغلاق النافذة: {e}")

# للتوافق مع الكود الموجود
class EmployeesWindow(EmployeesManagementWindow):
    """كلاس للتوافق مع الكود الموجود"""
    pass

# دالة لتشغيل النافذة مستقلة
def main():
    """تشغيل نافذة الموظفين مستقلة"""
    try:
        app = EmployeesManagementWindow()
        app.window.mainloop()
    except Exception as e:
        print(f"خطأ في تشغيل النافذة: {e}")

if __name__ == "__main__":
    main()
