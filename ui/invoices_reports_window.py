# -*- coding: utf-8 -*-
"""
نافذة تقارير وتحليل الفواتير - نظام شامل للتقارير والإحصائيات
"""

import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime, date, timedelta
import customtkinter as ctk

from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS
from ui.window_utils import configure_window_fullscreen


class InvoicesReportsWindow:
    """نافذة تقارير وتحليل الفواتير"""

    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.current_user = getattr(parent, 'current_user', {'role': 'admin', 'username': 'admin'})

        # متغيرات التقارير
        self.reports_tree = None
        self.filter_vars = {}
        self.current_report_type = "daily_sales"

        self.create_window()

    def create_window(self):
        """إنشاء نافذة التقارير"""
        self.window = ctk.CTkToplevel()
        self.window.title("📊 تقارير وتحليل الفواتير - برنامج ست الكل للمحاسبة")

        # تكوين النافذة
        configure_window_fullscreen(self.window)
        self.window.configure(fg_color=MODERN_COLORS['background'])

        # إنشاء الإطار الرئيسي
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # إنشاء الهيدر
        self.create_header(main_frame)

        # إنشاء المحتوى
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(10, 0))

        # إنشاء الأقسام
        self.create_reports_layout(content_frame)

    def create_header(self, parent):
        """إنشاء هيدر النافذة"""
        header_frame = ctk.CTkFrame(parent, height=80, fg_color=MODERN_COLORS['info'])
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)

        # العنوان
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="right", fill="y", padx=20, pady=10)

        title = ctk.CTkLabel(
            title_frame,
            text="📊 تقارير وتحليل الفواتير",
            font=("Cairo", 20, "bold"),
            text_color="white"
        )
        title.pack(anchor="e")

        subtitle = ctk.CTkLabel(
            title_frame,
            text="تقارير شاملة ومفصلة لجميع العمليات والمبيعات",
            font=("Cairo", 14),
            text_color="white"
        )
        subtitle.pack(anchor="e")

        # أزرار التصدير
        self.create_export_buttons(header_frame)

    def create_export_buttons(self, parent):
        """إنشاء أزرار التصدير"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(side="left", fill="y", padx=20, pady=10)

        export_buttons = [
            ("📄", "تصدير PDF", self.export_pdf, MODERN_COLORS['error']),
            ("📊", "تصدير Excel", self.export_excel, MODERN_COLORS['success']),
            ("🖨️", "طباعة", self.print_report, MODERN_COLORS['warning']),
            ("🔄", "تحديث", self.refresh_report, MODERN_COLORS['secondary'])
        ]

        for icon, text, command, color in export_buttons:
            btn = ctk.CTkButton(
                buttons_frame,
                text=f"{icon} {text}",
                font=("Cairo", 11),
                fg_color=color,
                width=100,
                height=35,
                command=command
            )
            btn.pack(side="left", padx=5)

    def create_reports_layout(self, parent):
        """إنشاء تخطيط التقارير"""
        # الشريط الجانبي - أنواع التقارير
        sidebar = ctk.CTkFrame(parent, width=280, fg_color=MODERN_COLORS['surface'])
        sidebar.pack(side="right", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        self.create_reports_sidebar(sidebar)

        # المنطقة الرئيسية - الفلاتر والنتائج
        main_area = ctk.CTkFrame(parent, fg_color="transparent")
        main_area.pack(side="left", fill="both", expand=True)

        # قسم الفلاتر
        filters_frame = ctk.CTkFrame(main_area, height=120, fg_color=MODERN_COLORS['surface'])
        filters_frame.pack(fill="x", pady=(0, 10))
        filters_frame.pack_propagate(False)

        self.create_filters_section(filters_frame)

        # قسم النتائج
        results_frame = ctk.CTkFrame(main_area, fg_color=MODERN_COLORS['surface'])
        results_frame.pack(fill="both", expand=True)

        self.create_results_section(results_frame)

    def create_reports_sidebar(self, parent):
        """إنشاء الشريط الجانبي لأنواع التقارير"""
        # عنوان الشريط الجانبي
        title = ctk.CTkLabel(
            parent,
            text="📋 أنواع التقارير",
            font=("Cairo", 16, "bold"),
            text_color=MODERN_COLORS['text_primary']
        )
        title.pack(pady=20)

        # أزرار أنواع التقارير
        reports_data = [
            ("📊", "المبيعات اليومية", "daily_sales", MODERN_COLORS['success']),
            ("📈", "حركة الفواتير", "invoices_movement", MODERN_COLORS['info']),
            ("🛍️", "مبيعات الأصناف", "items_sales", MODERN_COLORS['warning']),
            ("👥", "مبيعات المستخدمين", "users_sales", MODERN_COLORS['secondary']),
            ("🔝", "الأصناف الأكثر مبيعاً", "top_items", MODERN_COLORS['primary']),
            ("💰", "تحليل الأرباح", "profit_analysis", "#9C27B0"),
            ("📅", "التقرير الشهري", "monthly_report", "#FF5722"),
            ("🗑️", "الفواتير المحذوفة", "deleted_invoices", "#795548"),
            ("📋", "تقرير مخصص", "custom_report", "#607D8B")
        ]

        for icon, text, report_type, color in reports_data:
            btn = ctk.CTkButton(
                parent,
                text=f"{icon} {text}",
                font=("Cairo", 12),
                fg_color=color,
                hover_color=self.get_hover_color(color),
                height=45,
                anchor="e",
                command=lambda rt=report_type: self.select_report_type(rt)
            )
            btn.pack(fill="x", padx=15, pady=3)

    def create_filters_section(self, parent):
        """إنشاء قسم الفلاتر"""
        # عنوان القسم
        title = ctk.CTkLabel(
            parent,
            text="🔍 فلاتر التقرير",
            font=("Cairo", 14, "bold"),
            text_color=MODERN_COLORS['text_primary']
        )
        title.pack(anchor="e", padx=20, pady=(10, 5))

        # إطار الفلاتر
        filters_container = ctk.CTkFrame(parent, fg_color="transparent")
        filters_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # الصف الأول - التواريخ
        date_row = ctk.CTkFrame(filters_container, fg_color="transparent")
        date_row.pack(fill="x", pady=5)

        # من تاريخ
        from_date_label = ctk.CTkLabel(date_row, text="من تاريخ:", font=("Cairo", 12))
        from_date_label.pack(side="right", padx=(0, 10))

        self.filter_vars['from_date'] = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        from_date_entry = ctk.CTkEntry(
            date_row,
            textvariable=self.filter_vars['from_date'],
            font=("Cairo", 12),
            width=120
        )
        from_date_entry.pack(side="right", padx=5)

        # إلى تاريخ
        to_date_label = ctk.CTkLabel(date_row, text="إلى تاريخ:", font=("Cairo", 12))
        to_date_label.pack(side="right", padx=(20, 10))

        self.filter_vars['to_date'] = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        to_date_entry = ctk.CTkEntry(
            date_row,
            textvariable=self.filter_vars['to_date'],
            font=("Cairo", 12),
            width=120
        )
        to_date_entry.pack(side="right", padx=5)

        # الصف الثاني - فلاتر إضافية
        extra_row = ctk.CTkFrame(filters_container, fg_color="transparent")
        extra_row.pack(fill="x", pady=5)

        # العميل
        customer_label = ctk.CTkLabel(extra_row, text="العميل:", font=("Cairo", 12))
        customer_label.pack(side="right", padx=(0, 10))

        self.filter_vars['customer'] = ctk.StringVar()
        customer_combo = ctk.CTkComboBox(
            extra_row,
            variable=self.filter_vars['customer'],
            values=["جميع العملاء", "عميل نقدي", "عميل آجل", "عميل مميز"],
            font=("Cairo", 12),
            width=150
        )
        customer_combo.pack(side="right", padx=5)
        customer_combo.set("جميع العملاء")

        # المستخدم
        user_label = ctk.CTkLabel(extra_row, text="المستخدم:", font=("Cairo", 12))
        user_label.pack(side="right", padx=(20, 10))

        self.filter_vars['user'] = ctk.StringVar()
        user_combo = ctk.CTkComboBox(
            extra_row,
            variable=self.filter_vars['user'],
            values=["جميع المستخدمين", "admin", "cashier1", "cashier2"],
            font=("Cairo", 12),
            width=150
        )
        user_combo.pack(side="right", padx=5)
        user_combo.set("جميع المستخدمين")

        # زر التطبيق
        apply_btn = ctk.CTkButton(
            extra_row,
            text="🔍 تطبيق الفلاتر",
            font=("Cairo", 12),
            fg_color=MODERN_COLORS['primary'],
            width=120,
            command=self.apply_filters
        )
        apply_btn.pack(side="left", padx=20)

    def create_results_section(self, parent):
        """إنشاء قسم النتائج"""
        # عنوان القسم
        results_header = ctk.CTkFrame(parent, height=50, fg_color="transparent")
        results_header.pack(fill="x", padx=20, pady=10)
        results_header.pack_propagate(False)

        results_title = ctk.CTkLabel(
            results_header,
            text="📋 نتائج التقرير",
            font=("Cairo", 16, "bold"),
            text_color=MODERN_COLORS['text_primary']
        )
        results_title.pack(side="right", pady=10)

        # معلومات التقرير
        info_label = ctk.CTkLabel(
            results_header,
            text="المبيعات اليومية - اليوم",
            font=("Cairo", 12),
            text_color=MODERN_COLORS['text_secondary']
        )
        info_label.pack(side="left", pady=10)

        # جدول النتائج
        table_frame = ctk.CTkFrame(parent, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # إنشاء Treeview للنتائج
        columns = ("date", "invoice_no", "customer", "amount", "user", "status")
        column_names = ("التاريخ", "رقم الفاتورة", "العميل", "المبلغ", "المستخدم", "الحالة")

        self.reports_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # تكوين الأعمدة
        for col, name in zip(columns, column_names):
            self.reports_tree.heading(col, text=name)
            if col == "amount":
                self.reports_tree.column(col, width=100, anchor="center")
            elif col in ["date", "invoice_no"]:
                self.reports_tree.column(col, width=120, anchor="center")
            else:
                self.reports_tree.column(col, width=150, anchor="e")

        # شريط التمرير
        reports_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.reports_tree.yview)
        self.reports_tree.configure(yscrollcommand=reports_scrollbar.set)

        # تخطيط الجدول
        self.reports_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        reports_scrollbar.pack(side="right", fill="y", pady=10)

        # تحميل بيانات تجريبية
        self.load_sample_data()

    def load_sample_data(self):
        """تحميل بيانات تجريبية للتقرير"""
        sample_data = [
            ("2024-07-19", "SAL-2024-07-001", "عميل نقدي", "150.00", "admin", "مكتملة"),
            ("2024-07-19", "SAL-2024-07-002", "شركة الأمل", "2500.00", "cashier1", "مكتملة"),
            ("2024-07-19", "SAL-2024-07-003", "عميل آجل", "750.00", "cashier2", "معلقة"),
            ("2024-07-19", "SAL-2024-07-004", "عميل نقدي", "320.00", "admin", "مكتملة"),
            ("2024-07-19", "SAL-2024-07-005", "مؤسسة النور", "1200.00", "cashier1", "مكتملة"),
        ]

        for data in sample_data:
            self.reports_tree.insert("", "end", values=data)

    def select_report_type(self, report_type):
        """اختيار نوع التقرير"""
        self.current_report_type = report_type

        # تحديث عنوان التقرير
        report_names = {
            "daily_sales": "المبيعات اليومية",
            "invoices_movement": "حركة الفواتير",
            "items_sales": "مبيعات الأصناف",
            "users_sales": "مبيعات المستخدمين",
            "top_items": "الأصناف الأكثر مبيعاً",
            "profit_analysis": "تحليل الأرباح",
            "monthly_report": "التقرير الشهري",
            "deleted_invoices": "الفواتير المحذوفة",
            "custom_report": "تقرير مخصص"
        }

        messagebox.showinfo("تم التحديد", f"تم اختيار تقرير: {report_names.get(report_type, 'غير محدد')}")

    def apply_filters(self):
        """تطبيق الفلاتر"""
        from_date = self.filter_vars['from_date'].get()
        to_date = self.filter_vars['to_date'].get()
        customer = self.filter_vars['customer'].get()
        user = self.filter_vars['user'].get()

        messagebox.showinfo("تطبيق الفلاتر", 
                          f"تم تطبيق الفلاتر:\nمن: {from_date}\nإلى: {to_date}\nالعميل: {customer}\nالمستخدم: {user}")

    def get_hover_color(self, color):
        """الحصول على لون التمرير"""
        hover_colors = {
            MODERN_COLORS['success']: '#45a049',
            MODERN_COLORS['info']: '#1976D2',
            MODERN_COLORS['warning']: '#F57C00',
            MODERN_COLORS['secondary']: '#303F9F',
            MODERN_COLORS['primary']: MODERN_COLORS.get('primary_dark', '#1B5E20'),
            '#9C27B0': '#7B1FA2',
            '#FF5722': '#E64A19',
            '#795548': '#5D4037',
            '#607D8B': '#455A64'
        }
        return hover_colors.get(color, color)

    def export_pdf(self):
        """تصدير التقرير إلى PDF"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="حفظ التقرير كـ PDF"
        )
        if filename:
            messagebox.showinfo("قريباً", f"سيتم تصدير التقرير إلى:\n{filename}")

    def export_excel(self):
        """تصدير التقرير إلى Excel"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="حفظ التقرير كـ Excel"
        )
        if filename:
            messagebox.showinfo("قريباً", f"سيتم تصدير التقرير إلى:\n{filename}")

    def print_report(self):
        """طباعة التقرير"""
        messagebox.showinfo("قريباً", "طباعة التقرير قيد التطوير")

    def refresh_report(self):
        """تحديث التقرير"""
        # مسح البيانات الحالية
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)

        # إعادة تحميل البيانات
        self.load_sample_data()
        messagebox.showinfo("تم التحديث", "تم تحديث التقرير بنجاح")


def main():
    """تشغيل النافذة للاختبار"""
    root = ctk.CTk()
    root.withdraw()

    app = InvoicesReportsWindow()
    root.mainloop()


if __name__ == "__main__":
    main()
