#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 نافذة إدارة الموظفين المحسنة البسيطة
Simple Enhanced Employee Management Window

نافذة محسنة مع:
- أزرار أكبر وأجمل
- ألوان متدرجة جميلة
- خطوط مكبرة وواضحة
- تصميم احترافي
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from datetime import datetime

# إعداد customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# الألوان المحسنة
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2', 
    'success': '#00b894',
    'warning': '#fdcb6e',
    'danger': '#e84393',
    'info': '#74b9ff',
    'light': '#f8f9fa',
    'dark': '#2d3436',
    'white': '#ffffff'
}

# الخطوط المحسنة
FONTS = {
    'title': ('Arial', 28, 'bold'),
    'header': ('Arial', 20, 'bold'),
    'button': ('Arial', 16, 'bold'),
    'text': ('Arial', 14),
    'label': ('Arial', 14, 'bold')
}

class SimpleEnhancedWindow:
    def __init__(self):
        self.window = None
        self.db_connection = None
        self.employees_data = []
        self.form_vars = {}
        self.tree = None
        
        self.create_window()
        self.init_database()
        self.load_data()
    
    def create_window(self):
        """إنشاء النافذة الرئيسية المحسنة"""
        self.window = ctk.CTk()
        self.window.title("🚀 نظام إدارة الموظفين المحسن والمتطور")
        self.window.geometry("1800x950")  # زيادة العرض من 1600 إلى 1800 (+12.5%)
        self.window.minsize(1400, 900)   # حد أدنى محسن للحجم
        self.window.configure(fg_color=COLORS['light'])

        # توسيط النافذة في الشاشة
        self.center_window()
        
        # إنشاء المحتوى
        self.create_header()
        self.create_toolbar()
        self.create_content()

    def center_window(self):
        """توسيط النافذة في الشاشة"""
        try:
            self.window.update_idletasks()
            width = self.window.winfo_width()
            height = self.window.winfo_height()

            # الحصول على أبعاد الشاشة
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            # حساب الموضع للتوسيط
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2

            # تطبيق الموضع الجديد
            self.window.geometry(f"{width}x{height}+{x}+{y}")

        except Exception as e:
            print(f"تحذير: فشل في توسيط النافذة: {e}")
    
    def create_header(self):
        """إنشاء الهيدر"""
        header_frame = ctk.CTkFrame(
            self.window,
            height=100,
            fg_color=COLORS['primary'],
            corner_radius=20
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🚀 نظام إدارة الموظفين المحسن والمتطور",
            font=FONTS['title'],
            text_color="white"
        )
        title_label.pack(pady=30)
    
    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        toolbar_frame = ctk.CTkFrame(
            self.window,
            height=80,
            fg_color=COLORS['white'],
            corner_radius=20
        )
        toolbar_frame.pack(fill="x", padx=20, pady=10)
        toolbar_frame.pack_propagate(False)
        
        # إطار الأزرار
        buttons_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # الأزرار المحسنة
        buttons = [
            ("➕ إضافة موظف", self.add_employee, COLORS['success']),
            ("✏️ تعديل بيانات", self.edit_employee, COLORS['info']),
            ("🗑️ حذف موظف", self.delete_employee, COLORS['danger']),
            ("📊 التقارير", self.show_reports, COLORS['warning']),
            ("🔄 تحديث", self.refresh_data, COLORS['primary'])
        ]
        
        for text, command, color in buttons:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                width=180,
                height=50,
                font=FONTS['button'],
                fg_color=color,
                hover_color=self.darken_color(color),
                corner_radius=15
            )
            btn.pack(side="left", padx=10, expand=True)
    
    def create_content(self):
        """إنشاء المحتوى الرئيسي"""
        content_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # الجانب الأيسر - الجدول
        left_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS['white'],
            corner_radius=20
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # عنوان الجدول
        table_title = ctk.CTkLabel(
            left_frame,
            text="👥 قائمة الموظفين",
            font=FONTS['header'],
            text_color=COLORS['dark']
        )
        table_title.pack(pady=20)
        
        # إنشاء الجدول
        self.create_table(left_frame)
        
        # الجانب الأيمن - النموذج
        right_frame = ctk.CTkFrame(
            content_frame,
            width=400,
            fg_color=COLORS['white'],
            corner_radius=20
        )
        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)
        
        # عنوان النموذج
        form_title = ctk.CTkLabel(
            right_frame,
            text="📝 بيانات الموظف",
            font=FONTS['header'],
            text_color=COLORS['dark']
        )
        form_title.pack(pady=20)
        
        # إنشاء النموذج
        self.create_form(right_frame)
    
    def create_table(self, parent):
        """إنشاء جدول الموظفين"""
        # إطار الجدول
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # الأعمدة
        columns = ("ID", "الاسم", "القسم", "المنصب", "الراتب", "الحالة")
        
        # إنشاء Treeview
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # تكوين الأعمدة
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=120, anchor="center")
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط الجدول
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ربط الأحداث
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
    
    def create_form(self, parent):
        """إنشاء نموذج البيانات"""
        # إطار النموذج القابل للتمرير
        form_frame = ctk.CTkScrollableFrame(parent)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # متغيرات النموذج
        self.form_vars = {
            'name': ctk.StringVar(),
            'department': ctk.StringVar(),
            'position': ctk.StringVar(),
            'salary': ctk.StringVar(),
            'phone': ctk.StringVar(),
            'email': ctk.StringVar(),
            'status': ctk.StringVar(value="نشط")
        }
        
        # الحقول
        fields = [
            ("الاسم الكامل", "name", "entry"),
            ("القسم", "department", "combo"),
            ("المنصب", "position", "entry"),
            ("الراتب", "salary", "entry"),
            ("الهاتف", "phone", "entry"),
            ("البريد الإلكتروني", "email", "entry"),
            ("الحالة", "status", "combo")
        ]
        
        for label_text, var_name, field_type in fields:
            # التسمية
            label = ctk.CTkLabel(
                form_frame,
                text=label_text,
                font=FONTS['label'],
                text_color=COLORS['dark']
            )
            label.pack(anchor="w", pady=(10, 5))
            
            # الحقل
            if field_type == "entry":
                widget = ctk.CTkEntry(
                    form_frame,
                    textvariable=self.form_vars[var_name],
                    font=FONTS['text'],
                    height=40,
                    corner_radius=10
                )
            elif field_type == "combo":
                values = self.get_combo_values(var_name)
                widget = ctk.CTkComboBox(
                    form_frame,
                    variable=self.form_vars[var_name],
                    values=values,
                    font=FONTS['text'],
                    height=40,
                    corner_radius=10
                )
            
            widget.pack(fill="x", pady=(0, 5))
        
        # أزرار النموذج
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ",
            command=self.save_employee,
            width=120,
            height=40,
            font=FONTS['button'],
            fg_color=COLORS['success'],
            corner_radius=10
        )
        save_btn.pack(side="left", padx=5, expand=True)
        
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ مسح",
            command=self.clear_form,
            width=120,
            height=40,
            font=FONTS['button'],
            fg_color=COLORS['warning'],
            corner_radius=10
        )
        clear_btn.pack(side="right", padx=5, expand=True)
    
    def init_database(self):
        """تهيئة قاعدة البيانات"""
        try:
            if not os.path.exists("database"):
                os.makedirs("database")
            
            self.db_connection = sqlite3.connect("database/employees.db")
            cursor = self.db_connection.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    position TEXT NOT NULL,
                    salary REAL NOT NULL,
                    phone TEXT,
                    email TEXT,
                    status TEXT DEFAULT 'نشط'
                )
            """)
            
            self.db_connection.commit()
            print("✅ تم تهيئة قاعدة البيانات")
            
        except Exception as e:
            print(f"❌ خطأ في قاعدة البيانات: {e}")
    
    def load_data(self):
        """تحميل البيانات"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM employees")
            self.employees_data = cursor.fetchall()
            self.update_table()
            print(f"✅ تم تحميل {len(self.employees_data)} موظف")
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
    
    def update_table(self):
        """تحديث الجدول"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # إدراج البيانات الجديدة
        for employee in self.employees_data:
            self.tree.insert("", "end", values=employee)
    
    def get_combo_values(self, var_name):
        """الحصول على قيم القوائم المنسدلة"""
        values = {
            'department': ["الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية"],
            'status': ["نشط", "غير نشط", "معلق", "مستقيل"]
        }
        return values.get(var_name, [])
    
    def darken_color(self, color):
        """تغميق اللون للتأثير عند التمرير"""
        # تحويل بسيط للون
        if color == COLORS['success']:
            return '#00a085'
        elif color == COLORS['info']:
            return '#5a9bd4'
        elif color == COLORS['danger']:
            return '#d63384'
        elif color == COLORS['warning']:
            return '#e0ac69'
        else:
            return '#5a6fd8'
    
    # وظائف الأحداث
    def on_select(self, event):
        """عند تحديد صف في الجدول"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # تحديث النموذج
            self.form_vars['name'].set(values[1])
            self.form_vars['department'].set(values[2])
            self.form_vars['position'].set(values[3])
            self.form_vars['salary'].set(str(values[4]))
            self.form_vars['phone'].set(values[5] or "")
            self.form_vars['email'].set(values[6] or "")
            self.form_vars['status'].set(values[7])
    
    def add_employee(self):
        """إضافة موظف جديد"""
        self.clear_form()
        messagebox.showinfo("إضافة موظف", "تم تحضير النموذج لإضافة موظف جديد")
    
    def edit_employee(self):
        """تعديل موظف"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد موظف للتعديل")
            return
        messagebox.showinfo("تعديل موظف", "تم تحميل بيانات الموظف للتعديل")
    
    def delete_employee(self):
        """حذف موظف"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد موظف للحذف")
            return
        
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا الموظف؟")
        if result:
            item = self.tree.item(selection[0])
            employee_id = item['values'][0]
            
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            self.db_connection.commit()
            
            self.load_data()
            self.clear_form()
            messagebox.showinfo("نجح", "تم حذف الموظف بنجاح")
    
    def save_employee(self):
        """حفظ الموظف"""
        # التحقق من البيانات
        if not all([
            self.form_vars['name'].get(),
            self.form_vars['department'].get(),
            self.form_vars['position'].get(),
            self.form_vars['salary'].get()
        ]):
            messagebox.showwarning("تحذير", "يرجى ملء جميع الحقول المطلوبة")
            return
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                INSERT INTO employees (name, department, position, salary, phone, email, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.form_vars['name'].get(),
                self.form_vars['department'].get(),
                self.form_vars['position'].get(),
                float(self.form_vars['salary'].get()),
                self.form_vars['phone'].get(),
                self.form_vars['email'].get(),
                self.form_vars['status'].get()
            ))
            
            self.db_connection.commit()
            self.load_data()
            self.clear_form()
            messagebox.showinfo("نجح", "تم حفظ الموظف بنجاح")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في حفظ الموظف: {e}")
    
    def clear_form(self):
        """مسح النموذج"""
        for var in self.form_vars.values():
            var.set("")
        self.form_vars['status'].set("نشط")
    
    def show_reports(self):
        """إظهار التقارير"""
        messagebox.showinfo("التقارير", "ميزة التقارير قيد التطوير")
    
    def refresh_data(self):
        """تحديث البيانات"""
        self.load_data()
        messagebox.showinfo("تحديث", "تم تحديث البيانات بنجاح")

def main():
    """الدالة الرئيسية"""
    print("🚀 تشغيل نافذة إدارة الموظفين المحسنة البسيطة...")
    
    try:
        app = SimpleEnhancedWindow()
        app.window.mainloop()
        print("✅ تم إغلاق النافذة بنجاح")
    except Exception as e:
        print(f"❌ خطأ: {e}")
        messagebox.showerror("خطأ", f"حدث خطأ: {e}")

if __name__ == "__main__":
    main()
