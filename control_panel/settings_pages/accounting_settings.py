# -*- coding: utf-8 -*-
"""
صفحة إعدادات المحاسبة
Accounting Settings Page
"""

import sys
from pathlib import Path
from datetime import datetime, date

# إضافة مسار المشروع للاستيراد
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import customtkinter as ctk
    from tkinter import messagebox
    from tkcalendar import DateEntry
except ImportError as e:
    print(f"خطأ في استيراد المكتبات: {e}")
    # استخدام Entry عادي إذا لم تكن tkcalendar متوفرة
    DateEntry = None

from core.settings_manager import settings_manager

class AccountingSettingsPage:
    """صفحة إعدادات المحاسبة"""
    
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.widgets = {}
        self.create_content()
        self.load_settings()
    
    def create_content(self):
        """إنشاء محتوى الصفحة"""
        # قسم السنة المالية
        self.create_fiscal_year_section()
        
        # قسم العملة والتقييم
        self.create_currency_section()
        
        # قسم طرق القيد
        self.create_entry_methods_section()
        
        # قسم الحسابات الافتراضية
        self.create_default_accounts_section()
    
    def create_fiscal_year_section(self):
        """قسم السنة المالية"""
        # إطار القسم
        fiscal_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        fiscal_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            fiscal_frame,
            text="📅 السنة المالية",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(fiscal_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # تاريخ بداية السنة المالية
        start_label = ctk.CTkLabel(
            grid_frame,
            text="تاريخ بداية السنة المالية:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        start_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        if DateEntry:
            self.widgets['fiscal_year_start'] = DateEntry(
                grid_frame,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                year=datetime.now().year,
                month=1,
                day=1
            )
        else:
            self.widgets['fiscal_year_start'] = ctk.CTkEntry(
                grid_frame,
                width=200,
                height=35,
                font=("Cairo", 12),
                placeholder_text="YYYY-MM-DD"
            )
        self.widgets['fiscal_year_start'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # تاريخ نهاية السنة المالية
        end_label = ctk.CTkLabel(
            grid_frame,
            text="تاريخ نهاية السنة المالية:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        end_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        if DateEntry:
            self.widgets['fiscal_year_end'] = DateEntry(
                grid_frame,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                year=datetime.now().year,
                month=12,
                day=31
            )
        else:
            self.widgets['fiscal_year_end'] = ctk.CTkEntry(
                grid_frame,
                width=200,
                height=35,
                font=("Cairo", 12),
                placeholder_text="YYYY-MM-DD"
            )
        self.widgets['fiscal_year_end'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # إقفال السنة المالية
        self.widgets['fiscal_year_locked'] = ctk.CTkCheckBox(
            grid_frame,
            text="إقفال السنة المالية الحالية",
            font=("Cairo", 12)
        )
        self.widgets['fiscal_year_locked'].grid(row=2, column=0, columnspan=2, sticky="e", padx=10, pady=5)
    
    def create_currency_section(self):
        """قسم العملة والتقييم"""
        # إطار القسم
        currency_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        currency_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            currency_frame,
            text="💰 العملة والتقييم",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(currency_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # العملة الافتراضية
        currency_label = ctk.CTkLabel(
            grid_frame,
            text="العملة الافتراضية:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        currency_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['default_currency'] = ctk.CTkComboBox(
            grid_frame,
            values=["SAR - ريال سعودي", "USD - دولار أمريكي", "EUR - يورو", "AED - درهم إماراتي", "KWD - دينار كويتي"],
            width=250,
            font=("Cairo", 12)
        )
        self.widgets['default_currency'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # عدد الخانات العشرية
        decimal_label = ctk.CTkLabel(
            grid_frame,
            text="عدد الخانات العشرية:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        decimal_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['decimal_places'] = ctk.CTkComboBox(
            grid_frame,
            values=["2", "3", "4"],
            width=100,
            font=("Cairo", 12)
        )
        self.widgets['decimal_places'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # طريقة التقريب
        rounding_label = ctk.CTkLabel(
            grid_frame,
            text="طريقة التقريب:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        rounding_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['rounding_method'] = ctk.CTkComboBox(
            grid_frame,
            values=["تقريب عادي", "تقريب لأعلى", "تقريب لأسفل"],
            width=200,
            font=("Cairo", 12)
        )
        self.widgets['rounding_method'].grid(row=2, column=0, sticky="w", padx=10, pady=5)
    
    def create_entry_methods_section(self):
        """قسم طرق القيد"""
        # إطار القسم
        entry_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        entry_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            entry_frame,
            text="📝 طرق القيد",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # طريقة القيد
        method_label = ctk.CTkLabel(
            grid_frame,
            text="طريقة القيد:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        method_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['entry_method'] = ctk.CTkComboBox(
            grid_frame,
            values=["قيد يدوي", "قيد تلقائي", "قيد مختلط"],
            width=200,
            font=("Cairo", 12)
        )
        self.widgets['entry_method'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # ترقيم القيود
        numbering_label = ctk.CTkLabel(
            grid_frame,
            text="ترقيم القيود:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        numbering_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['entry_numbering'] = ctk.CTkComboBox(
            grid_frame,
            values=["تلقائي", "يدوي", "حسب التاريخ"],
            width=200,
            font=("Cairo", 12)
        )
        self.widgets['entry_numbering'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # السماح بتعديل القيود
        self.widgets['allow_edit_entries'] = ctk.CTkCheckBox(
            grid_frame,
            text="السماح بتعديل القيود المحفوظة",
            font=("Cairo", 12)
        )
        self.widgets['allow_edit_entries'].grid(row=2, column=0, columnspan=2, sticky="e", padx=10, pady=5)
        
        # السماح بحذف القيود
        self.widgets['allow_delete_entries'] = ctk.CTkCheckBox(
            grid_frame,
            text="السماح بحذف القيود",
            font=("Cairo", 12)
        )
        self.widgets['allow_delete_entries'].grid(row=3, column=0, columnspan=2, sticky="e", padx=10, pady=5)
    
    def create_default_accounts_section(self):
        """قسم الحسابات الافتراضية"""
        # إطار القسم
        accounts_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        accounts_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            accounts_frame,
            text="🏦 الحسابات الافتراضية",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(accounts_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # حساب المبيعات
        sales_label = ctk.CTkLabel(
            grid_frame,
            text="حساب المبيعات:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        sales_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['sales_account'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="رقم حساب المبيعات"
        )
        self.widgets['sales_account'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # حساب المشتريات
        purchases_label = ctk.CTkLabel(
            grid_frame,
            text="حساب المشتريات:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        purchases_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['purchases_account'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="رقم حساب المشتريات"
        )
        self.widgets['purchases_account'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # حساب الضريبة
        tax_label = ctk.CTkLabel(
            grid_frame,
            text="حساب الضريبة:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        tax_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['tax_account'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="رقم حساب الضريبة"
        )
        self.widgets['tax_account'].grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        # حساب الخصم
        discount_label = ctk.CTkLabel(
            grid_frame,
            text="حساب الخصم:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        discount_label.grid(row=3, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['discount_account'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="رقم حساب الخصم"
        )
        self.widgets['discount_account'].grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        # أزرار الحفظ والإلغاء
        buttons_frame = ctk.CTkFrame(accounts_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ إعدادات المحاسبة",
            width=200,
            height=35,
            font=("Cairo", 12),
            fg_color="#28a745",
            hover_color="#218838",
            command=self.save_settings
        )
        save_btn.pack(side="left", padx=5)
        
        reset_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 إعادة تعيين",
            width=150,
            height=35,
            font=("Cairo", 12),
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.reset_settings
        )
        reset_btn.pack(side="left", padx=5)
    
    def load_settings(self):
        """تحميل الإعدادات الحالية"""
        accounting_settings = settings_manager.get_section("accounting")
        
        # تحميل القيم في الواجهة
        if DateEntry:
            # تحميل التواريخ
            start_date = accounting_settings.get("fiscal_year_start", "2025-01-01")
            end_date = accounting_settings.get("fiscal_year_end", "2025-12-31")
            
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
                self.widgets['fiscal_year_start'].set_date(start_dt)
                self.widgets['fiscal_year_end'].set_date(end_dt)
            except:
                pass
        else:
            self.widgets['fiscal_year_start'].insert(0, accounting_settings.get("fiscal_year_start", "2025-01-01"))
            self.widgets['fiscal_year_end'].insert(0, accounting_settings.get("fiscal_year_end", "2025-12-31"))
        
        # تحميل باقي الإعدادات
        if accounting_settings.get("fiscal_year_locked", False):
            self.widgets['fiscal_year_locked'].select()
        
        self.widgets['default_currency'].set(accounting_settings.get("default_currency", "SAR - ريال سعودي"))
        self.widgets['decimal_places'].set(str(accounting_settings.get("decimal_places", 2)))
        self.widgets['rounding_method'].set(accounting_settings.get("rounding_method", "تقريب عادي"))
        self.widgets['entry_method'].set(accounting_settings.get("entry_method", "قيد تلقائي"))
        self.widgets['entry_numbering'].set(accounting_settings.get("entry_numbering", "تلقائي"))
        
        if accounting_settings.get("allow_edit_entries", True):
            self.widgets['allow_edit_entries'].select()
        
        if accounting_settings.get("allow_delete_entries", False):
            self.widgets['allow_delete_entries'].select()
        
        # تحميل الحسابات الافتراضية
        self.widgets['sales_account'].insert(0, accounting_settings.get("sales_account", ""))
        self.widgets['purchases_account'].insert(0, accounting_settings.get("purchases_account", ""))
        self.widgets['tax_account'].insert(0, accounting_settings.get("tax_account", ""))
        self.widgets['discount_account'].insert(0, accounting_settings.get("discount_account", ""))
    
    def save_settings(self):
        """حفظ إعدادات المحاسبة"""
        try:
            # جمع البيانات من الواجهة
            if DateEntry:
                fiscal_year_start = self.widgets['fiscal_year_start'].get_date().strftime("%Y-%m-%d")
                fiscal_year_end = self.widgets['fiscal_year_end'].get_date().strftime("%Y-%m-%d")
            else:
                fiscal_year_start = self.widgets['fiscal_year_start'].get()
                fiscal_year_end = self.widgets['fiscal_year_end'].get()
            
            accounting_data = {
                "fiscal_year_start": fiscal_year_start,
                "fiscal_year_end": fiscal_year_end,
                "fiscal_year_locked": self.widgets['fiscal_year_locked'].get() == 1,
                "default_currency": self.widgets['default_currency'].get(),
                "decimal_places": int(self.widgets['decimal_places'].get()),
                "rounding_method": self.widgets['rounding_method'].get(),
                "entry_method": self.widgets['entry_method'].get(),
                "entry_numbering": self.widgets['entry_numbering'].get(),
                "allow_edit_entries": self.widgets['allow_edit_entries'].get() == 1,
                "allow_delete_entries": self.widgets['allow_delete_entries'].get() == 1,
                "sales_account": self.widgets['sales_account'].get(),
                "purchases_account": self.widgets['purchases_account'].get(),
                "tax_account": self.widgets['tax_account'].get(),
                "discount_account": self.widgets['discount_account'].get()
            }
            
            # حفظ الإعدادات
            settings_manager.set_section("accounting", accounting_data)
            
            if settings_manager.save_settings():
                messagebox.showinfo("نجح", "تم حفظ إعدادات المحاسبة بنجاح!")
            else:
                messagebox.showerror("خطأ", "فشل في حفظ إعدادات المحاسبة!")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ إعدادات المحاسبة: {e}")
    
    def reset_settings(self):
        """إعادة تعيين إعدادات المحاسبة للقيم الافتراضية"""
        result = messagebox.askyesno(
            "تأكيد",
            "هل أنت متأكد من إعادة تعيين إعدادات المحاسبة للقيم الافتراضية؟"
        )
        if result:
            # مسح جميع الحقول
            for widget_name, widget in self.widgets.items():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
                elif isinstance(widget, ctk.CTkComboBox):
                    widget.set("")
                elif isinstance(widget, ctk.CTkCheckBox):
                    widget.deselect()
            
            # إعادة تعيين القسم
            settings_manager.reset_section("accounting")
            self.load_settings()
            messagebox.showinfo("تم", "تم إعادة تعيين إعدادات المحاسبة!")
