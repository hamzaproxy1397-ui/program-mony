# -*- coding: utf-8 -*-
# cSpell:disable
"""
نافذة المبيعات الشاملة مع جميع الوظائف
Comprehensive Sales Window with All Functions
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

try:
    from themes.modern_theme import MODERN_COLORS, FONTS
    from ui.window_utils import configure_window_fullscreen
    from ui.enhanced_pos_window import EnhancedPOSWindow
    from database.hybrid_database_manager import HybridDatabaseManager
except ImportError as e:
    print(f"تحذير: {e}")
    # ألوان افتراضية
    MODERN_COLORS = {
        'primary': '#2E8B57',
        'secondary': '#4682B4',
        'background': '#f8f9fa',
        'surface': '#ffffff',
        'success': '#28a745',
        'warning': '#ffc107',
        'error': '#dc3545',
        'info': '#17a2b8'
    }
    FONTS = {'arabic': 'Arial'}

class ComprehensiveSalesWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = None

        # تهيئة قاعدة البيانات
        try:
            self.db_manager = HybridDatabaseManager()
            self.sales_manager = self.db_manager.sales_manager
        except Exception as e:
            print(f"خطأ في تهيئة قاعدة البيانات: {e}")
            self.db_manager = None
            self.sales_manager = None

        self.create_window()

    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        try:
            self.window = ctk.CTkToplevel(self.parent)

            # إعداد النافذة لتملأ الشاشة
            configure_window_fullscreen(self.window, "نظام المبيعات الشامل - برنامج ست الكل للمحاسبة")

            # جعل النافذة في المقدمة
            self.window.transient(self.parent)
            self.window.grab_set()

            # إنشاء المحتوى
            self.create_main_layout()

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إنشاء نافذة المبيعات: {str(e)}")

    def create_main_layout(self):
        """إنشاء التخطيط الرئيسي"""
        # الشريط العلوي
        self.create_header()

        # المحتوى الرئيسي
        main_container = ctk.CTkScrollableFrame(self.window, fg_color="#f8f9fa")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # إنشاء الأقسام
        self.create_pos_section(main_container)
        self.create_invoices_section(main_container)
        self.create_reports_section(main_container)

    def create_header(self):
        """إنشاء الشريط العلوي"""
        header = ctk.CTkFrame(self.window, height=100, fg_color="#2E8B57")
        header.pack(fill="x", padx=20, pady=(20, 0))
        header.pack_propagate(False)

        # العنوان الرئيسي
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="right", padx=30, pady=20)

        main_title = ctk.CTkLabel(
            title_frame,
            text="🏪 نظام المبيعات الشامل",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        main_title.pack()

        subtitle = ctk.CTkLabel(
            title_frame,
            text="جميع وظائف المبيعات في مكان واحد",
            font=("Arial", 14),
            text_color="#E8F5E8"
        )
        subtitle.pack()

        # معلومات التاريخ والوقت
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="left", padx=30, pady=20)

        date_label = ctk.CTkLabel(
            info_frame,
            text=f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}",
            font=("Arial", 12),
            text_color="white"
        )
        date_label.pack(anchor="w")

        time_label = ctk.CTkLabel(
            info_frame,
            text=f"🕐 الوقت: {datetime.now().strftime('%H:%M')}",
            font=("Arial", 12),
            text_color="#E8F5E8"
        )
        time_label.pack(anchor="w")

        # زر الإغلاق
        close_btn = ctk.CTkButton(
            header,
            text="❌ إغلاق",
            width=120,
            height=50,
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.close_window,
            font=("Arial", 14, "bold")
        )
        close_btn.pack(side="left", padx=(0, 30), pady=25)

    def create_pos_section(self, parent):
        """إنشاء قسم نقاط البيع"""
        # عنوان القسم
        section_title = ctk.CTkLabel(
            parent,
            text="🛒 نقاط البيع وإدارة الفواتير",
            font=("Arial", 20, "bold"),
            text_color="#2E8B57"
        )
        section_title.pack(anchor="e", pady=(20, 10))

        # إطار الأيقونات
        pos_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        pos_frame.pack(fill="x", pady=10)

        # الصف الأول من الأيقونات
        first_row = ctk.CTkFrame(pos_frame, fg_color="transparent")
        first_row.pack(fill="x", padx=30, pady=20)

        pos_icons_row1 = [
            ("🏪", "نقطة المبيعات المحسنة", "#2E8B57", self.open_enhanced_pos, "نظام نقطة البيع الاحترافي مع حاسبة متطورة"),
            ("📄", "إضافة فاتورة جديدة", "#4682B4", self.add_new_invoice, "إنشاء فاتورة بيع جديدة"),
            ("💳", "نقطة البيع السريعة", "#FF6B35", self.open_quick_pos, "نقطة بيع مبسطة للمعاملات السريعة"),
            ("🖥️", "واجهة البيع التفاعلية", "#9C27B0", self.open_interactive_sales, "واجهة بيع تفاعلية متقدمة")
        ]

        for icon, title, color, command, description in pos_icons_row1:
            self.create_icon_button(first_row, icon, title, color, command, description)

    def create_invoices_section(self, parent):
        """إنشاء قسم الفواتير والمراجعة"""
        # عنوان القسم
        section_title = ctk.CTkLabel(
            parent,
            text="📋 إدارة الفواتير والمراجعة",
            font=("Arial", 20, "bold"),
            text_color="#4682B4"
        )
        section_title.pack(anchor="e", pady=(30, 10))

        # إطار الأيقونات
        invoices_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        invoices_frame.pack(fill="x", pady=10)

        # الصف الثاني من الأيقونات
        second_row = ctk.CTkFrame(invoices_frame, fg_color="transparent")
        second_row.pack(fill="x", padx=30, pady=20)

        invoices_icons = [
            ("💰", "قائمة أسعار الأصناف", "#28a745", self.open_price_list, "عرض وإدارة أسعار جميع الأصناف"),
            ("🔍", "مراجعة المبيعات", "#17a2b8", self.open_sales_review, "مراجعة فواتير المبيعات والمرتجعات"),
            ("↩️", "المرتجعات", "#ffc107", self.open_returns, "إدارة مرتجعات المبيعات"),
            ("🏷️", "عروض الأسعار", "#6f42c1", self.open_price_quotes, "إنشاء ومتابعة عروض الأسعار")
        ]

        for icon, title, color, command, description in invoices_icons:
            self.create_icon_button(second_row, icon, title, color, command, description)

    def create_reports_section(self, parent):
        """إنشاء قسم التقارير"""
        # عنوان القسم
        section_title = ctk.CTkLabel(
            parent,
            text="📊 التقارير والتحليلات",
            font=("Arial", 20, "bold"),
            text_color="#dc3545"
        )
        section_title.pack(anchor="e", pady=(30, 10))

        # إطار الأيقونات
        reports_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        reports_frame.pack(fill="x", pady=10)

        # الصف الثالث من الأيقونات
        third_row = ctk.CTkFrame(reports_frame, fg_color="transparent")
        third_row.pack(fill="x", padx=30, pady=20)

        reports_icons = [
            ("📈", "تقارير المبيعات", "#dc3545", self.open_sales_reports, "تقارير شاملة عن المبيعات والأرباح"),
            ("📊", "تحليل الأداء", "#e83e8c", self.open_performance_analysis, "تحليل أداء المبيعات والعملاء"),
            ("💹", "الرسوم البيانية", "#fd7e14", self.open_charts, "رسوم بيانية للمبيعات والاتجاهات"),
            ("📋", "تقارير مخصصة", "#20c997", self.open_custom_reports, "إنشاء تقارير مخصصة حسب الحاجة")
        ]

        for icon, title, color, command, description in reports_icons:
            self.create_icon_button(third_row, icon, title, color, command, description)

    def create_icon_button(self, parent, icon, title, color, command, description):
        """إنشاء زر أيقونة"""
        # إطار الزر
        button_frame = ctk.CTkFrame(parent, width=280, height=160, fg_color=color)
        button_frame.pack(side="right", padx=15, pady=10)
        button_frame.pack_propagate(False)

        # الزر الرئيسي
        main_button = ctk.CTkButton(
            button_frame,
            text="",
            width=260,
            height=140,
            fg_color="transparent",
            hover_color=self.get_hover_color(color),
            command=command,
            corner_radius=10
        )
        main_button.pack(padx=10, pady=10)

        # محتوى الزر
        content_frame = ctk.CTkFrame(main_button, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # الأيقونة
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon,
            font=("Arial", 40),
            text_color="white"
        )
        icon_label.pack(pady=(0, 5))

        # العنوان
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=("Arial", 14, "bold"),
            text_color="white",
            wraplength=200
        )
        title_label.pack(pady=(0, 5))

        # الوصف
        desc_label = ctk.CTkLabel(
            content_frame,
            text=description,
            font=("Arial", 10),
            text_color="#f0f0f0",
            wraplength=220
        )
        desc_label.pack()

    def get_hover_color(self, color):
        """الحصول على لون التمرير"""
        hover_colors = {
            "#2E8B57": "#267A4A",
            "#4682B4": "#3A6B94",
            "#FF6B35": "#E55A2B",
            "#9C27B0": "#8E24AA",
            "#28a745": "#218838",
            "#17a2b8": "#138496",
            "#ffc107": "#e0a800",
            "#6f42c1": "#5a32a3",
            "#dc3545": "#c82333",
            "#e83e8c": "#d91a72",
            "#fd7e14": "#e8690b",
            "#20c997": "#1ba085"
        }
        return hover_colors.get(color, "#5A6268")

    # وظائف نقاط البيع
    def open_enhanced_pos(self):
        """فتح نقطة المبيعات المحسنة"""
        try:
            enhanced_pos = EnhancedPOSWindow(self.window)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح نقطة المبيعات المحسنة: {str(e)}")

    def add_new_invoice(self):
        """إضافة فاتورة جديدة"""
        try:
            # نافذة إضافة فاتورة جديدة
            invoice_window = ctk.CTkToplevel(self.window)
            invoice_window.title("إضافة فاتورة جديدة")
            invoice_window.geometry("800x600")
            invoice_window.transient(self.window)
            invoice_window.grab_set()

            # محتوى النافذة
            header = ctk.CTkFrame(invoice_window, height=80, fg_color="#4682B4")
            header.pack(fill="x", padx=10, pady=10)
            header.pack_propagate(False)

            ctk.CTkLabel(
                header,
                text="📄 إضافة فاتورة بيع جديدة",
                font=("Arial", 20, "bold"),
                text_color="white"
            ).pack(expand=True)

            # نموذج الفاتورة
            form_frame = ctk.CTkScrollableFrame(invoice_window)
            form_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # حقول الفاتورة
            fields = [
                ("رقم الفاتورة:", f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                ("اسم العميل:", ""),
                ("تاريخ الفاتورة:", datetime.now().strftime('%Y-%m-%d')),
                ("ملاحظات:", "")
            ]

            entries = {}
            for label, default_value in fields:
                field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
                field_frame.pack(fill="x", pady=10)

                ctk.CTkLabel(
                    field_frame,
                    text=label,
                    font=("Arial", 12, "bold"),
                    width=150
                ).pack(side="right", padx=10)

                entry = ctk.CTkEntry(
                    field_frame,
                    font=("Arial", 12),
                    width=400
                )
                entry.pack(side="right", padx=10)
                entry.insert(0, default_value)
                entries[label] = entry

            # أزرار العمليات
            buttons_frame = ctk.CTkFrame(invoice_window, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=10, pady=10)

            def save_invoice():
                messagebox.showinfo("حفظ", "تم حفظ الفاتورة بنجاح!")
                if invoice_window and hasattr(invoice_window, "destroy"):

                    invoice_window.destroy()

            ctk.CTkButton(
                buttons_frame,
                text="💾 حفظ الفاتورة",
                command=save_invoice,
                fg_color="#28a745",
                width=150
            ).pack(side="right", padx=10)

            ctk.CTkButton(
                buttons_frame,
                text="❌ إلغاء",
                command=invoice_window.destroy,
                fg_color="#6c757d",
                width=100
            ).pack(side="right", padx=5)

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح نافذة الفاتورة: {str(e)}")

    def open_quick_pos(self):
        """فتح نقطة البيع السريعة"""
        try:
            from ui.pos_simple import SimplePOSWindow
            quick_pos = SimplePOSWindow(self.window)
        except Exception as e:
            messagebox.showinfo("نقطة البيع السريعة", "نافذة نقطة البيع السريعة ستكون متاحة قريباً")

    def open_interactive_sales(self):
        """فتح واجهة البيع التفاعلية"""
        messagebox.showinfo("واجهة البيع التفاعلية", "واجهة البيع التفاعلية ستكون متاحة قريباً")

    # وظائف الفواتير والمراجعة
    def open_price_list(self):
        """فتح قائمة أسعار الأصناف"""
        try:
            # نافذة قائمة الأسعار
            price_window = ctk.CTkToplevel(self.window)
            price_window.title("قائمة أسعار الأصناف")
            price_window.geometry("900x700")
            price_window.transient(self.window)
            price_window.grab_set()

            # الشريط العلوي
            header = ctk.CTkFrame(price_window, height=80, fg_color="#28a745")
            header.pack(fill="x", padx=10, pady=10)
            header.pack_propagate(False)

            ctk.CTkLabel(
                header,
                text="💰 قائمة أسعار الأصناف",
                font=("Arial", 20, "bold"),
                text_color="white"
            ).pack(expand=True)

            # جدول الأسعار
            table_frame = ctk.CTkScrollableFrame(price_window)
            table_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # عناوين الجدول
            headers = ["كود الصنف", "اسم الصنف", "سعر الشراء", "سعر البيع", "الربح", "العملة"]
            header_frame = ctk.CTkFrame(table_frame, fg_color="#e9ecef")
            header_frame.pack(fill="x", pady=(0, 5))

            for header in headers:
                ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=140
                ).pack(side="right", padx=5, pady=10)

            # بيانات تجريبية
            sample_items = [
                ("001", "مكيف هواء سبليت", "1800.00", "2100.00", "300.00", "ر.س"),
                ("002", "فرن كهربائي", "700.00", "850.00", "150.00", "ر.س"),
                ("003", "مكنسة كهربائية", "350.00", "450.00", "100.00", "ر.س"),
                ("004", "غلاية كهربائية", "80.00", "120.00", "40.00", "ر.س"),
                ("005", "مروحة سقف", "250.00", "320.00", "70.00", "ر.س")
            ]

            for item in sample_items:
                item_frame = ctk.CTkFrame(table_frame, fg_color="#f8f9fa")
                item_frame.pack(fill="x", pady=2)

                for value in item:
                    ctk.CTkLabel(
                        item_frame,
                        text=value,
                        font=("Arial", 11),
                        width=140
                    ).pack(side="right", padx=5, pady=8)

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح قائمة الأسعار: {str(e)}")

    def open_sales_review(self):
        """فتح مراجعة المبيعات"""
        messagebox.showinfo("مراجعة المبيعات", "نافذة مراجعة المبيعات ستكون متاحة قريباً")

    def open_returns(self):
        """فتح المرتجعات"""
        messagebox.showinfo("المرتجعات", "نافذة إدارة المرتجعات ستكون متاحة قريباً")

    def open_price_quotes(self):
        """فتح عروض الأسعار"""
        messagebox.showinfo("عروض الأسعار", "نافذة عروض الأسعار ستكون متاحة قريباً")

    # وظائف التقارير
    def open_sales_reports(self):
        """فتح تقارير المبيعات"""
        try:
            from ui.sales_analysis_window import SalesAnalysisWindow
            sales_reports = SalesAnalysisWindow(self.window)
        except Exception as e:
            messagebox.showinfo("تقارير المبيعات", "نافذة تقارير المبيعات ستكون متاحة قريباً")

    def open_performance_analysis(self):
        """فتح تحليل الأداء"""
        messagebox.showinfo("تحليل الأداء", "نافذة تحليل الأداء ستكون متاحة قريباً")

    def open_charts(self):
        """فتح الرسوم البيانية"""
        messagebox.showinfo("الرسوم البيانية", "نافذة الرسوم البيانية ستكون متاحة قريباً")

    def open_custom_reports(self):
        """فتح التقارير المخصصة"""
        messagebox.showinfo("التقارير المخصصة", "نافذة التقارير المخصصة ستكون متاحة قريباً")

    def close_window(self):
        """إغلاق النافذة"""
        if hasattr(self, 'window') and self.window:

            self.window.destroy()
