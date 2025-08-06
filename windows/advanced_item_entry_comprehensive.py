#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدخال الأصناف الشامل والمتقدم - النسخة الأصلية
Advanced & Comprehensive Item Entry System - Original Version
"""

import queue
import threading
import uuid
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False


class AdvancedItemEntryComprehensive:
    """نافذة إدخال الأصناف الشاملة والمتقدمة"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.project_root = Path(__file__).parent.parent
        
        # متغيرات البيانات
        self.current_item_data = {}
        self.categories_data = []
        self.units_data = []
        self.validation_queue = queue.Queue()
        
        # إعدادات الواجهة
        self.ui_config = {
            'theme': 'modern',
            'rtl_support': True,
            'font_family': 'Segoe UI',
            'font_size': 11,
            'colors': {
                'primary': '#2E86AB',
                'secondary': '#A23B72',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336',
                'background': '#F5F5F5',
                'surface': '#FFFFFF',
                'text': '#212121'
            }
        }
        
        # إنشاء النافذة الرئيسية
        self.create_main_window()
        
        # تحميل البيانات الأساسية
        self.load_initial_data()

    def create_main_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Tk()
        self.window.title("نظام إدخال الأصناف الشامل والمتقدم")
        self.window.geometry("1400x900")
        self.window.configure(bg=self.ui_config['colors']['background'])
        
        # تعيين الخط
        self.window.option_add('*Font', f"{self.ui_config['font_family']} {self.ui_config['font_size']}")
        
        # إنشاء القوائم
        self.create_menu_bar()
        
        # إنشاء شريط الأدوات
        self.create_toolbar()
        
        # إنشاء المحتوى الرئيسي
        self.create_main_content()
        
        # إنشاء شريط الحالة
        self.create_status_bar()

    def create_menu_bar(self):
        """إنشاء شريط القوائم"""
        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)
        
        # قائمة الملف
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="جديد", command=self.new_item, accelerator="Ctrl+N")
        file_menu.add_command(label="حفظ", command=self.save_item, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="استيراد", command=self.import_items)
        file_menu.add_command(label="تصدير", command=self.export_items)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.close_window)
        
        # قائمة التحرير
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="تحرير", menu=edit_menu)
        edit_menu.add_command(label="نسخ", command=self.copy_item, accelerator="Ctrl+C")
        edit_menu.add_command(label="لصق", command=self.paste_item, accelerator="Ctrl+V")

    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        self.toolbar_frame = ttk.Frame(self.window)
        self.toolbar_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # أزرار الأدوات الرئيسية
        self.create_toolbar_button("جديد", self.new_item)
        self.create_toolbar_button("حفظ", self.save_item)
        self.create_toolbar_button("حذف", self.delete_item)

        ttk.Separator(self.toolbar_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, padx=5, fill=tk.Y)
        
        # أزرار إضافية
        self.create_toolbar_button("تحديث", self.refresh_data)
        self.create_toolbar_button("بيانات تجريبية", self.add_sample_data)
        
        # شريط البحث
        search_frame = ttk.Frame(self.toolbar_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="بحث:").pack(side=tk.LEFT, padx=2)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=2)
        search_entry.bind('<Return>', lambda e: self.perform_search())
        
        search_btn = ttk.Button(search_frame, text="بحث", command=self.perform_search)
        search_btn.pack(side=tk.LEFT, padx=2)

    def create_toolbar_button(self, text, command):
        """إنشاء زر في شريط الأدوات"""
        button = ttk.Button(self.toolbar_frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=2)
        return button

    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        # إطار رئيسي مع Paned Window
        self.main_paned = ttk.PanedWindow(self.window, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # إنشاء لوحة الإدخال
        self.create_input_panel()
        
        # إنشاء لوحة القائمة
        self.create_list_panel()

    def create_input_panel(self):
        """إنشاء لوحة الإدخال"""
        self.input_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.input_frame, weight=2)
        
        # إنشاء Notebook للتبويبات
        self.notebook = ttk.Notebook(self.input_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # تبويب المعلومات الأساسية
        self.create_basic_info_tab()

    def create_basic_info_tab(self):
        """إنشاء تبويب المعلومات الأساسية"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="المعلومات الأساسية")
        
        # إطار قابل للتمرير
        canvas = tk.Canvas(basic_frame)
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # حقول الإدخال
        self.create_input_fields(scrollable_frame)

    def create_input_fields(self, parent):
        """إنشاء حقول الإدخال"""
        # متغيرات النموذج
        self.code_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.barcode_var = tk.StringVar()
        self.cost_price_var = tk.StringVar()
        self.selling_price_var = tk.StringVar()
        self.current_stock_var = tk.StringVar()
        
        # رمز الصنف
        ttk.Label(parent, text="رمز الصنف:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        code_frame = ttk.Frame(parent)
        code_frame.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Entry(code_frame, textvariable=self.code_var, width=20).pack(side=tk.LEFT)
        ttk.Button(code_frame, text="توليد", command=self.generate_code).pack(side=tk.LEFT, padx=5)
        
        # اسم الصنف
        ttk.Label(parent, text="اسم الصنف:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        ttk.Entry(parent, textvariable=self.name_var, width=30).grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # الوصف
        ttk.Label(parent, text="الوصف:").grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        self.description_text = tk.Text(parent, width=30, height=3)
        self.description_text.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # الفئة
        ttk.Label(parent, text="الفئة:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        category_frame = ttk.Frame(parent)
        category_frame.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var, width=25)
        self.category_combo.pack(side=tk.LEFT)
        ttk.Button(category_frame, text="إضافة فئة", command=self.add_new_category).pack(side=tk.LEFT, padx=5)
        
        # الوحدة
        ttk.Label(parent, text="الوحدة:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        unit_frame = ttk.Frame(parent)
        unit_frame.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        self.unit_combo = ttk.Combobox(unit_frame, textvariable=self.unit_var, width=25)
        self.unit_combo.pack(side=tk.LEFT)
        ttk.Button(unit_frame, text="إضافة وحدة", command=self.add_new_unit).pack(side=tk.LEFT, padx=5)
        
        # الباركود
        ttk.Label(parent, text="الباركود:").grid(row=5, column=0, sticky='e', padx=5, pady=5)
        barcode_frame = ttk.Frame(parent)
        barcode_frame.grid(row=5, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Entry(barcode_frame, textvariable=self.barcode_var, width=20).pack(side=tk.LEFT)
        ttk.Button(barcode_frame, text="توليد باركود", command=self.generate_barcode).pack(side=tk.LEFT, padx=5)
        
        # سعر التكلفة
        ttk.Label(parent, text="سعر التكلفة:").grid(row=6, column=0, sticky='e', padx=5, pady=5)
        ttk.Entry(parent, textvariable=self.cost_price_var, width=15).grid(row=6, column=1, sticky='w', padx=5, pady=5)
        
        # سعر البيع
        ttk.Label(parent, text="سعر البيع:").grid(row=7, column=0, sticky='e', padx=5, pady=5)
        ttk.Entry(parent, textvariable=self.selling_price_var, width=15).grid(row=7, column=1, sticky='w', padx=5, pady=5)
        
        # الكمية الحالية
        ttk.Label(parent, text="الكمية الحالية:").grid(row=8, column=0, sticky='e', padx=5, pady=5)
        ttk.Entry(parent, textvariable=self.current_stock_var, width=15).grid(row=8, column=1, sticky='w', padx=5, pady=5)

    def create_list_panel(self):
        """إنشاء لوحة القائمة"""
        self.list_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.list_frame, weight=1)
        
        # عنوان القائمة
        ttk.Label(self.list_frame, text="قائمة الأصناف", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # إنشاء Treeview
        columns = ('الرمز', 'الاسم', 'الفئة', 'السعر', 'الكمية')
        self.items_tree = ttk.Treeview(self.list_frame, columns=columns, show='headings', height=20)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        # شريط التمرير
        scrollbar_tree = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar_tree.set)
        
        # تخطيط العناصر
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط الأحداث
        self.items_tree.bind('<Double-1>', self.on_item_double_click)
        self.items_tree.bind('<Button-3>', self.show_context_menu)

    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_frame = ttk.Frame(self.window)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.status_var.set("جاهز")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)

    def load_initial_data(self):
        """تحميل البيانات الأولية"""
        # تحميل الفئات
        self.categories_data = ["إلكترونيات", "ملابس", "أغذية", "كتب", "أدوات"]
        self.category_combo['values'] = self.categories_data
        
        # تحميل الوحدات
        self.units_data = ["قطعة", "كيلو", "متر", "لتر", "علبة"]
        self.unit_combo['values'] = self.units_data
        
        # تحميل قائمة الأصناف
        self.load_items_list()

    def load_items_list(self):
        """تحميل قائمة الأصناف"""
        # مسح القائمة الحالية
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # إضافة بيانات تجريبية
        sample_items = [
            ("ITM001", "لابتوب ديل", "إلكترونيات", "2500.00", "10"),
            ("ITM002", "قميص قطني", "ملابس", "85.00", "25"),
            ("ITM003", "أرز بسمتي", "أغذية", "15.50", "100"),
        ]
        
        for item in sample_items:
            self.items_tree.insert('', 'end', values=item)

    # وظائف الأزرار
    def new_item(self):
        """إنشاء صنف جديد"""
        self.clear_form()
        self.generate_code()
        self.update_status("جاهز لإدخال صنف جديد")

    def save_item(self):
        """حفظ الصنف"""
        if not self.validate_form():
            return
        
        # جمع البيانات
        item_data = {
            'code': self.code_var.get(),
            'name': self.name_var.get(),
            'description': self.description_text.get(1.0, tk.END).strip(),
            'category': self.category_var.get(),
            'unit': self.unit_var.get(),
            'barcode': self.barcode_var.get(),
            'cost_price': self.cost_price_var.get(),
            'selling_price': self.selling_price_var.get(),
            'current_stock': self.current_stock_var.get()
        }
        
        # إضافة إلى القائمة
        self.items_tree.insert('', 'end', values=(
            item_data['code'],
            item_data['name'],
            item_data['category'],
            item_data['selling_price'],
            item_data['current_stock']
        ))
        
        self.update_status("تم حفظ الصنف بنجاح")
        messagebox.showinfo("نجح", "تم حفظ الصنف بنجاح!")

    def delete_item(self):
        """حذف الصنف المحدد"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى تحديد صنف للحذف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", "هل تريد حذف الصنف المحدد؟"):
            self.items_tree.delete(selected[0])
            self.update_status("تم حذف الصنف")

    def validate_form(self):
        """التحقق من صحة البيانات"""
        if not self.code_var.get().strip():
            messagebox.showerror("خطأ", "يرجى إدخال رمز الصنف")
            return False
        
        if not self.name_var.get().strip():
            messagebox.showerror("خطأ", "يرجى إدخال اسم الصنف")
            return False
        
        return True

    def clear_form(self):
        """مسح النموذج"""
        self.code_var.set("")
        self.name_var.set("")
        self.description_text.delete(1.0, tk.END)
        self.category_var.set("")
        self.unit_var.set("")
        self.barcode_var.set("")
        self.cost_price_var.set("")
        self.selling_price_var.set("")
        self.current_stock_var.set("")

    def generate_code(self):
        """توليد رمز الصنف"""
        import random
        code = f"ITM{random.randint(1000, 9999)}"
        self.code_var.set(code)

    def generate_barcode(self):
        """توليد باركود"""
        import random
        barcode = f"{random.randint(100000000000, 999999999999)}"
        self.barcode_var.set(barcode)

    def add_new_category(self):
        """إضافة فئة جديدة"""
        from tkinter import simpledialog
        name = simpledialog.askstring("فئة جديدة", "اسم الفئة:")
        if name:
            self.categories_data.append(name)
            self.category_combo['values'] = self.categories_data
            self.category_var.set(name)

    def add_new_unit(self):
        """إضافة وحدة جديدة"""
        from tkinter import simpledialog
        name = simpledialog.askstring("وحدة جديدة", "اسم الوحدة:")
        if name:
            self.units_data.append(name)
            self.unit_combo['values'] = self.units_data
            self.unit_var.set(name)

    def refresh_data(self):
        """تحديث البيانات"""
        self.load_items_list()
        self.update_status("تم تحديث البيانات")

    def add_sample_data(self):
        """إضافة بيانات تجريبية"""
        self.load_items_list()
        self.update_status("تم إضافة البيانات التجريبية")

    def perform_search(self):
        """البحث في الأصناف"""
        search_text = self.search_var.get().strip()
        if not search_text:
            self.load_items_list()
            return
        
        # مسح القائمة الحالية
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # البحث في البيانات (محاكاة)
        sample_items = [
            ("ITM001", "لابتوب ديل", "إلكترونيات", "2500.00", "10"),
            ("ITM002", "قميص قطني", "ملابس", "85.00", "25"),
            ("ITM003", "أرز بسمتي", "أغذية", "15.50", "100"),
        ]
        
        for item in sample_items:
            if search_text.lower() in item[1].lower() or search_text in item[0]:
                self.items_tree.insert('', 'end', values=item)
        
        self.update_status(f"البحث عن: {search_text}")

    def on_item_double_click(self, event):
        """عند النقر المزدوج على صنف"""
        selected = self.items_tree.selection()
        if selected:
            item = self.items_tree.item(selected[0])
            values = item['values']
            
            # تحميل البيانات في النموذج
            self.code_var.set(values[0])
            self.name_var.set(values[1])
            self.category_var.set(values[2])
            self.selling_price_var.set(values[3])
            self.current_stock_var.set(values[4])
            
            self.update_status(f"تم تحميل: {values[1]}")

    def show_context_menu(self, event):
        """عرض القائمة السياقية"""
        context_menu = tk.Menu(self.window, tearoff=0)
        context_menu.add_command(label="تحرير", command=self.on_item_double_click)
        context_menu.add_command(label="حذف", command=self.delete_item)
        context_menu.add_separator()
        context_menu.add_command(label="نسخ", command=self.copy_item)
        context_menu.add_command(label="لصق", command=self.paste_item)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def copy_item(self):
        """نسخ الصنف"""
        messagebox.showinfo("نسخ", "تم نسخ الصنف")

    def paste_item(self):
        """لصق الصنف"""
        messagebox.showinfo("لصق", "تم لصق الصنف")

    def import_items(self):
        """استيراد الأصناف"""
        messagebox.showinfo("استيراد", "ميزة الاستيراد قيد التطوير")

    def export_items(self):
        """تصدير الأصناف"""
        messagebox.showinfo("تصدير", "ميزة التصدير قيد التطوير")

    def update_status(self, message):
        """تحديث رسالة الحالة"""
        self.status_var.set(message)
        self.window.update_idletasks()

    def close_window(self):
        """إغلاق النافذة"""
        if messagebox.askokcancel("إغلاق", "هل تريد إغلاق النافذة؟"):
            self.window.destroy()

    def run(self):
        """تشغيل التطبيق"""
        self.window.mainloop()


def main():
    """تشغيل النافذة"""
    print("تشغيل نظام إدخال الأصناف الشامل والمتقدم...")
    
    try:
        app = AdvancedItemEntryComprehensive()
        app.run()
    except Exception as e:
        print(f"خطأ في تشغيل النظام: {e}")
        messagebox.showerror("خطأ", f"فشل في تشغيل النظام: {e}")


if __name__ == "__main__":
    main()
