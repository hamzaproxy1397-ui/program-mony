# -*- coding: utf-8 -*-
# cSpell:disable
"""
نافذة التطبيق الرئيسية للبرنامج المحاسبي
Main Application Window for Arabic Accounting Software

هذا الملف يحتوي على الواجهة الرئيسية للبرنامج المحاسبي باللغة العربية
ويدعم جميع الوظائف الأساسية مثل المبيعات والمشتريات والتقارير
"""

# Standard library imports
import os
import traceback
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Callable

# Third-party imports
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog

# Optional third-party imports with fallbacks
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    print("تحذير: فشل في استيراد مكتبة PIL للصور")
    Image = None
    ImageTk = None
    PIL_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    print("تحذير: فشل في استيراد مكتبة numpy")
    np = None
    NUMPY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("تحذير: فشل في استيراد مكتبة matplotlib")
    plt = None
    MATPLOTLIB_AVAILABLE = False

# Local application imports - Core modules
from ui.login_window import LoginWindow
from ui.window_utils import configure_window_fullscreen
from themes.theme_manager import ThemeManager
from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS, get_hover_color
from config.settings import (
    WINDOW_TITLE, WINDOW_MIN_SIZE, GRID_SPACING, BUTTON_SIZE
)
from database.hybrid_database_manager import HybridDatabaseManager

# Error handling system
try:
    from core.error_handler import (
        error_handler, db_error_handler, setup_global_exception_handler,
        handle_ui_error, handle_db_operation, log_error, log_info, log_warning
    )
    ERROR_HANDLING_AVAILABLE = True
except ImportError:
    ERROR_HANDLING_AVAILABLE = False
    print("تحذير: نظام معالجة الأخطاء المحسن غير متاح")

# UI Window imports with safe fallbacks
def safe_import(module_path: str, class_name: str, fallback_name: str = None) -> Optional[Any]:
    """
    استيراد آمن للوحدات مع معالجة الأخطاء
    Safe import of modules with error handling
    """
    try:
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)
    except ImportError as e:
        fallback_display = fallback_name or class_name
        print(f"تحذير: فشل في استيراد {fallback_display} من {module_path}: {e}")
        return None

# Import UI windows safely
SimpleWelcomeWindow = safe_import('ui.simple_welcome_window', 'SimpleWelcomeWindow', 'نافذة الترحيب')
WarehousesWindow = safe_import('ui.warehouses_management_window', 'WarehousesManagementWindow', 'إدارة المخازن')
PurchasesWindow = safe_import('ui.purchases_window', 'PurchasesWindow', 'المشتريات')
SalesWindow = safe_import('ui.sales_window', 'SalesWindow', 'المبيعات')
ReportsWindow = safe_import('ui.reports_window', 'ReportsWindow', 'التقارير')
AdvancedFinancialReportsWindow = safe_import('ui.advanced_financial_reports_window', 'AdvancedFinancialReportsWindow', 'التقارير المالية المتقدمة')
AccountsWindow = safe_import('ui.accounts_window', 'AccountsWindow', 'الحسابات')
JournalEntriesWindow = safe_import('ui.journal_entries_window', 'JournalEntriesWindow', 'قيود اليومية')
AddItemsWindow = safe_import('ui.add_items_window', 'AddItemsWindow', 'إضافة الأصناف')
CategoriesManagementWindow = safe_import('ui.categories_management_window', 'CategoriesManagementWindow', 'إدارة الفئات')
UnitsManagementWindow = safe_import('ui.units_management_window', 'UnitsManagementWindow', 'إدارة الوحدات')
WarehousesManagementWindow = safe_import('ui.warehouses_management_window', 'WarehousesManagementWindow', 'إدارة المخازن')
StockManagementWindow = safe_import('ui.stock_management_window', 'StockManagementWindow', 'إدارة المخزون')
UserManagementWindow = safe_import('ui.user_management', 'UserManagementWindow', 'إدارة المستخدمين')
HRManagementWindow = safe_import('ui.hr_management_window', 'HRManagementWindow', 'إدارة الموارد البشرية')
InvoicesMainWindow = safe_import('ui.invoices_main_window', 'InvoicesMainWindow', 'الفواتير')
BarcodeScanner = safe_import('core.barcode_scanner', 'BarcodeScanner', 'ماسح الباركود')

# Import control panel function
try:
    from ui.central_control_panel import open_central_control_panel
except ImportError:
    print("تحذير: فشل في استيراد لوحة التحكم المركزية")
    open_central_control_panel = None

# Temporarily disabled modules (will be implemented later)
TreasuryWindow = None  # معطل مؤقتاً - سيتم تنفيذه لاحقاً
SalesAnalysisWindow = None  # معطل مؤقتاً - سيتم تنفيذه لاحقاً
EmployeeDataWindowFixed = None  # معطل مؤقتاً - سيتم تنفيذه لاحقاً

class MainApplication:
    """
    التطبيق الرئيسي للبرنامج المحاسبي
    Main Application class for the Arabic Accounting Software

    يدير جميع جوانب التطبيق بما في ذلك:
    - إدارة النوافذ والواجهات
    - الاتصال بقاعدة البيانات
    - إدارة المستخدمين والصلاحيات
    - معالجة الأخطاء والاستثناءات
    """

    def __init__(self):
        """تهيئة التطبيق الرئيسي مع معالجة شاملة للأخطاء"""

        # Initialize instance variables first
        self.auth_manager: Optional[Any] = None
        self.current_user: Optional[Dict[str, Any]] = None
        self.main_window: Optional[ctk.CTk] = None
        self.loaded_images: Dict[str, Any] = {}  # تخزين الصور المحملة
        self.scheduler_manager: Optional[Any] = None  # مدير المهام المجدولة
        self.theme_manager: Optional[ThemeManager] = None
        self.db_manager: Optional[HybridDatabaseManager] = None
        self.sales_manager: Optional[Any] = None

        # إعداد معالج الاستثناءات العام إذا كان متاحاً
        self._setup_error_handling()

        # إنشاء مدير الثيم مع معالجة الأخطاء
        self._initialize_theme_manager()

        # تهيئة مدير قاعدة البيانات المدمج
        self._initialize_database_manager()

        # إعداد customtkinter
        self._setup_customtkinter()

    def _setup_error_handling(self) -> None:
        """إعداد نظام معالجة الأخطاء"""
        try:
            if ERROR_HANDLING_AVAILABLE:
                setup_global_exception_handler()
                log_info("بدء تشغيل البرنامج المحاسبي")
        except Exception as e:
            print(f"تحذير: فشل في إعداد معالج الأخطاء: {e}")

    def _initialize_theme_manager(self) -> None:
        """تهيئة مدير الثيم مع معالجة الأخطاء"""
        try:
            self.theme_manager = ThemeManager()
            if ERROR_HANDLING_AVAILABLE:
                log_info("تم تحميل مدير الثيم بنجاح")
        except Exception as e:
            error_msg = f"تحذير: لم يتم تحميل مدير الثيم: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_warning(error_msg)
            self.theme_manager = None

    def _initialize_database_manager(self) -> None:
        """تهيئة مدير قاعدة البيانات مع معالجة شاملة للأخطاء"""
        try:
            self.db_manager = HybridDatabaseManager()

            # التحقق من صحة الاتصال
            if self.db_manager and hasattr(self.db_manager, 'sales_manager'):
                self.sales_manager = self.db_manager.sales_manager

                # التحقق من نوع قاعدة البيانات
                if hasattr(self.db_manager, 'db_type') and self.db_manager.db_type:
                    db_type_value = self.db_manager.db_type.value
                    success_msg = f"تم تهيئة قاعدة البيانات: {db_type_value}"
                    print(success_msg)
                    if ERROR_HANDLING_AVAILABLE:
                        log_info(success_msg)
                else:
                    print("تحذير: لم يتم تحديد نوع قاعدة البيانات")
            else:
                raise Exception("فشل في تهيئة مدير المبيعات")

        except Exception as e:
            error_msg = f"خطأ في تهيئة مدير قاعدة البيانات: {e}"
            print(error_msg)

            if ERROR_HANDLING_AVAILABLE:
                try:
                    db_error_handler.handle_db_error("تهيئة قاعدة البيانات", e, critical=True)
                except Exception as handler_error:
                    print(f"خطأ في معالج الأخطاء: {handler_error}")
            else:
                try:
                    messagebox.showerror("خطأ قاعدة البيانات", error_msg)
                except Exception as msg_error:
                    print(f"خطأ في عرض رسالة الخطأ: {msg_error}")

            self.db_manager = None
            self.sales_manager = None

    def _setup_customtkinter(self) -> None:
        """إعداد customtkinter مع معالجة الأخطاء"""
        try:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
        except Exception as e:
            print(f"تحذير: فشل في إعداد customtkinter: {e}")
            # Continue without customtkinter settings

    def run(self) -> None:
        """تشغيل التطبيق مع معالجة شاملة للأخطاء"""
        try:
            if ERROR_HANDLING_AVAILABLE:
                log_info("بدء تشغيل التطبيق")

            # عرض نافذة الترحيب أولاً
            self.show_welcome_window()

        except Exception as e:
            error_msg = f"خطأ حرج في تشغيل التطبيق: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)

            # محاولة عرض نافذة تسجيل الدخول مباشرة
            try:
                self.show_login_window()
            except Exception as login_error:
                print(f"خطأ حرج: فشل في عرض نافذة تسجيل الدخول: {login_error}")
                messagebox.showerror("خطأ حرج", "فشل في تشغيل التطبيق. يرجى إعادة المحاولة.")

    def show_welcome_window(self) -> None:
        """عرض نافذة الترحيب مع معالجة محسنة للأخطاء"""
        try:
            # التحقق من توفر نافذة الترحيب
            if SimpleWelcomeWindow is None:
                print("تحذير: نافذة الترحيب غير متاحة، الانتقال مباشرة لتسجيل الدخول")
                self.show_login_window()
                return

            # إنشاء نافذة الترحيب المبسطة
            welcome = SimpleWelcomeWindow()

            # التحقق من نجاح إنشاء النافذة
            if welcome is None:
                print("خطأ: فشل في إنشاء نافذة الترحيب")
                self.show_login_window()
                return

            # بعد انتهاء التحميل، انتقل لتسجيل الدخول
            def delayed_transition() -> None:
                try:
                    # إغلاق نافذة الترحيب أولاً
                    if welcome and hasattr(welcome, 'window') and welcome.window:
                        try:
                            welcome.close_welcome()
                        except Exception as close_error:
                            print(f"تحذير: فشل في إغلاق نافذة الترحيب: {close_error}")

                    # ثم عرض نافذة تسجيل الدخول
                    self.show_login_window()

                except Exception as e:
                    print(f"خطأ في الانتقال: {e}")
                    if ERROR_HANDLING_AVAILABLE:
                        log_error(f"خطأ في الانتقال من نافذة الترحيب: {e}")

                    # محاولة عرض نافذة تسجيل الدخول رغم الخطأ
                    try:
                        self.show_login_window()
                    except Exception as login_error:
                        print(f"خطأ حرج في عرض نافذة تسجيل الدخول: {login_error}")

            # تأخير الانتقال لمدة 8 ثواني
            if welcome and hasattr(welcome, 'window') and welcome.window:
                try:
                    welcome.window.after(8000, delayed_transition)
                    welcome.show()
                except Exception as show_error:
                    print(f"خطأ في عرض نافذة الترحيب: {show_error}")
                    self.show_login_window()
            else:
                print("تحذير: نافذة الترحيب غير صالحة، الانتقال مباشرة لتسجيل الدخول")
                self.show_login_window()

        except Exception as e:
            error_msg = f"خطأ في نافذة الترحيب: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)

            # في حالة الخطأ، انتقل مباشرة لتسجيل الدخول
            try:
                self.show_login_window()
            except Exception as login_error:
                print(f"خطأ حرج: فشل في عرض نافذة تسجيل الدخول: {login_error}")
                messagebox.showerror("خطأ", "فشل في تشغيل التطبيق")



    def show_login_window(self):
        """عرض نافذة تسجيل الدخول"""
        # عرض نافذة تسجيل الدخول
        login_window = LoginWindow()
        login_window.create_window(self.on_login_success)
        login_window.show()

        # الحصول على مدير المصادقة
        self.auth_manager = login_window.get_auth_manager()

    def on_login_success(self, user):
        """استدعاء عند نجاح تسجيل الدخول"""
        self.current_user = user
        self.create_main_window()

    def create_main_window(self) -> None:
        """
        إنشاء النافذة الرئيسية للتطبيق
        Create the main application window

        تقوم هذه الدالة بـ:
        - إنشاء النافذة الرئيسية باستخدام customtkinter
        - ضبط النافذة لملء الشاشة مع دعم متعدد المنصات
        - إنشاء المحتوى الرئيسي للواجهة
        - بدء حلقة الأحداث الرئيسية

        This function:
        - Creates the main window using customtkinter
        - Sets up fullscreen mode with cross-platform support
        - Creates the main UI content
        - Starts the main event loop
        """
        self.main_window = ctk.CTk()
        self.main_window.title(WINDOW_TITLE)

        # ضبط النافذة لملء الشاشة
        try:
            self.main_window.state('zoomed')  # ملء الشاشة في Windows
        except Exception:
            # للأنظمة الأخرى كبديل
            try:
                self.main_window.attributes('-zoomed', True)  # Linux
            except Exception:
                pass

        # كبديل احتياطي - استخدام حجم الشاشة
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        self.main_window.geometry(f"{screen_width}x{screen_height}+0+0")

        self.main_window.minsize(*WINDOW_MIN_SIZE)

        # إنشاء المحتوى - Create main content
        self.create_main_content()

        # عرض النافذة - Show window
        self.main_window.mainloop()

    def center_window(self):
        """توسيط النافذة على الشاشة"""  # noqa: spell-check
        self.main_window.update_idletasks()
        width = self.main_window.winfo_width()
        height = self.main_window.winfo_height()
        x = (self.main_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.main_window.winfo_screenheight() // 2) - (height // 2)
        self.main_window.geometry(f"{width}x{height}+{x}+{y}")

    def create_main_content(self):
        """إنشاء محتوى النافذة الرئيسية"""
        # الإطار الرئيسي
        main_frame = ctk.CTkFrame(self.main_window, fg_color=MODERN_COLORS['background'])
        main_frame.pack(fill="both", expand=True)

        # إنشاء الشريط العلوي
        self.create_top_menu_bar(main_frame)

        # إنشاء منطقة المحتوى الرئيسي
        content_frame = ctk.CTkFrame(main_frame, fg_color=MODERN_COLORS['background'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # إنشاء الشريط العلوي الأخضر مع الأيقونات والشعار
        self.create_green_top_bar(content_frame)

        # إنشاء منطقة الأيقونات الرئيسية
        self.create_main_grid_area(content_frame)

        # إنشاء معلومات المستخدم في الأسفل
        self.create_user_info_bottom(content_frame)

        # إنشاء الشريط السفلي
        self.create_bottom_taskbar(main_frame)



    def create_top_menu_bar(self, parent):
        """إنشاء شريط القائمة العلوي"""
        menu_bar = ctk.CTkFrame(parent, height=DIMENSIONS['top_bar_height'], fg_color="#FF8C00")
        menu_bar.pack(fill="x", padx=0, pady=0)
        menu_bar.pack_propagate(False)

        # قائمة الروابط العلوية المحدثة مع الأوامر
        menu_items = [
            ("الرئيسية", self.show_main_page),
            ("المخازن", self.show_warehouses),
            ("العملاء", self.show_clients),
            ("المشتريات", self.show_purchases),
            ("المبيعات", self.show_sales),
            ("الموظفين", self.show_employees),
            ("الحسابات", self.show_accounts),
            ("مساعدة", self.show_help),
            ("اشتراكي", self.show_subscription)
        ]

        # إنشاء الأزرار
        for i, (item_text, item_command) in enumerate(menu_items):
            btn = ctk.CTkButton(
                menu_bar,
                text=item_text,
                command=item_command,
                width=80,
                height=30,
                fg_color="transparent",
                text_color="#FFFFFF",
                hover_color="#FF7F00",
                font=("Cairo", 14),
                corner_radius=0
            )
            btn.pack(side="right", padx=2, pady=5)

        # شريط البحث
        search_frame = ctk.CTkFrame(menu_bar, fg_color="transparent")
        search_frame.pack(side="left", padx=10, pady=5)

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="أدخل ما تريد البحث عنه ست الكل",
            width=300,
            height=30,
            font=(FONTS['arabic'], FONTS['sizes']['normal'])
        )
        search_entry.pack(side="left")

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=30,
            height=30,
            fg_color="#4CAF50",
            font=(FONTS['icon'], FONTS['sizes']['normal'])
        )
        search_btn.pack(side="left", padx=(5, 0))

    def create_green_top_bar(self, parent):
        """إنشاء الشريط الأخضر العلوي مع الأيقونات"""
        green_bar = ctk.CTkFrame(parent, height=180, fg_color=MODERN_COLORS['primary'])
        green_bar.pack(fill="x", pady=(10, 0))
        green_bar.pack_propagate(False)

        # شعار البرنامج في الجانب الأيسر من الشريط الأخضر
        logo_frame = ctk.CTkFrame(green_bar, width=300, height=120, fg_color="transparent")
        logo_frame.pack(side="left", padx=15, pady=10)
        logo_frame.pack_propagate(False)

        # تحميل صورة الشعار مع معالجة مسارات متعددة المنصات
        logo_image_path = self._get_asset_path("logo", "222555.png")
        print(f"محاولة تحميل الشعار من: {logo_image_path}")

        if os.path.exists(logo_image_path):
            logo_image = self.load_icon_image(logo_image_path, (280, 100))
            if logo_image:
                logo_label = ctk.CTkLabel(
                    logo_frame,
                    image=logo_image,
                    text="",
                    fg_color="transparent"
                )
                logo_label.pack(expand=True, fill="both")
                print("تم عرض الشعار في الشريط الأخضر")
            else:
                # في حالة فشل تحميل الصورة، استخدم النص
                logo_label = ctk.CTkLabel(
                    logo_frame,
                    text="برنامج ست الكل\nللمحاسبة",
                    font=(FONTS['arabic'], FONTS['sizes']['large'], "bold"),
                    text_color=MODERN_COLORS['text_primary'],
                    justify="center"
                )
                logo_label.pack(expand=True)
        else:
            print(f"الملف غير موجود: {logo_image_path}")
            # في حالة عدم وجود الصورة، استخدم النص
            logo_label = ctk.CTkLabel(
                logo_frame,
                text="برنامج ست الكل\nللمحاسبة",
                font=(FONTS['arabic'], FONTS['sizes']['large'], "bold"),
                text_color=MODERN_COLORS['text_primary'],
                justify="center"
            )
            logo_label.pack(expand=True)

        # الأيقونات الست في الشريط الأخضر - إطار شفاف تماماً
        icons_frame = ctk.CTkFrame(green_bar, fg_color="transparent", corner_radius=0)
        icons_frame.pack(expand=True, fill="both", padx=20, pady=10)

        green_icons = [
            ("assets/icons/4.png", "التقارير المالية", self.open_advanced_financial_reports),
            ("assets/icons/5.png", "الفواتير", self.open_invoices),
            ("assets/icons/40.png", "الخزينة", self.open_treasury),
            ("assets/icons/43.png", "الحسابات", self.open_accounts),
            ("assets/icons/48.jpg", "المحاسبة", self.open_accounting),
            ("assets/icons/employees.png", "الموظفين", self.open_employees)
        ]

        for i, (icon_path, text, command) in enumerate(green_icons):
            # إطار شفاف تماماً للأيقونة مع ارتفاع أكبر
            icon_frame = ctk.CTkFrame(icons_frame, fg_color="transparent", corner_radius=0,
                                    width=130, height=180, border_width=0)
            icon_frame.pack(side="right", padx=8, pady=5)
            icon_frame.pack_propagate(False)

            # تحميل الأيقونة من الملف
            if os.path.exists(icon_path):
                icon_image = self.load_icon_image_no_bg(icon_path, (70, 70))
                if icon_image:
                    icon_label = ctk.CTkLabel(
                        icon_frame,
                        image=icon_image,
                        text="",
                        fg_color="transparent"
                    )
                else:
                    # في حالة فشل تحميل الصورة، استخدم النص
                    icon_label = ctk.CTkLabel(
                        icon_frame,
                        text="📊",
                        font=(FONTS['icon'], DIMENSIONS['icon_size']),
                        text_color=MODERN_COLORS['text_primary']
                    )
            else:
                # في حالة عدم وجود الصورة، استخدم رمز افتراضي
                icon_label = ctk.CTkLabel(
                    icon_frame,
                    text="📊",
                    font=(FONTS['icon'], DIMENSIONS['icon_size']),
                    text_color=MODERN_COLORS['text_primary']
                )

            icon_label.pack(pady=(30, 5))

            # النص أسفل الأيقونة مباشرة مع خط أكبر
            text_label = ctk.CTkLabel(
                icon_frame,
                text=text,
                font=(FONTS['arabic'], FONTS['sizes']['medium'], "bold"),
                text_color=MODERN_COLORS['text_primary'],
                wraplength=120,
                justify="center",
                anchor="center"
            )
            text_label.pack(pady=(0, 30), fill="x")

            # جعل الإطار قابل للنقر
            icon_frame.bind("<Button-1>", lambda e, cmd=command: cmd())
            icon_label.bind("<Button-1>", lambda e, cmd=command: cmd())
            text_label.bind("<Button-1>", lambda e, cmd=command: cmd())

            # تأثير التمرير مع خلفية شفافة
            def on_enter(e, frame=icon_frame):
                frame.configure(fg_color=MODERN_COLORS['primary_dark'], corner_radius=10)

            def on_leave(e, frame=icon_frame):
                frame.configure(fg_color="transparent", corner_radius=0)

            # ربط تأثيرات التمرير
            icon_frame.bind("<Enter>", on_enter)
            icon_frame.bind("<Leave>", on_leave)
            icon_label.bind("<Enter>", on_enter)
            icon_label.bind("<Leave>", on_leave)
            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)



    def create_old_top_bar(self, parent):
        """إنشاء الشريط العلوي"""
        top_frame = self.theme_manager.create_styled_frame(
            parent,
            height=80,
            corner_radius=10
        )
        top_frame.pack(fill="x", pady=(0, 10))
        top_frame.pack_propagate(False)

        # الجانب الأيمن - الشعار واسم البرنامج
        right_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20)

        # شعار البرنامج (مؤقت - نص)
        logo_label = self.theme_manager.create_styled_label(
            right_frame,
            text="🏪",
            font_size=32
        )
        logo_label.pack(side="right", padx=(0, 10))

        # اسم البرنامج
        title_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        title_frame.pack(side="right", fill="y")

        program_title = self.theme_manager.create_styled_label(
            title_frame,
            text="برنامج ست الكل للمحاسبة",
            font_size=20
        )
        program_title.pack(anchor="e", pady=(10, 0))

        subtitle = self.theme_manager.create_styled_label(
            title_frame,
            text="نظام إدارة المبيعات والمحاسبة المتكامل",
            font_size=12
        )
        subtitle.configure(text_color=self.theme_manager.get_color("text_secondary"))
        subtitle.pack(anchor="e")

        # الوسط - القائمة العلوية
        self.create_top_menu(top_frame)

        # الجانب الأيسر - أدوات المستخدم
        self.create_user_tools(top_frame)

    def create_top_menu(self, parent):
        """إنشاء القائمة العلوية"""
        menu_frame = ctk.CTkFrame(parent, fg_color="transparent")
        menu_frame.pack(expand=True, fill="both", padx=20)

        # قائمة الروابط المحدثة
        menu_items = [
            ("الرئيسية", self.show_main_page),
            ("المخازن", self.show_warehouses),
            ("العملاء", self.show_clients),
            ("المشتريات", self.show_purchases),
            ("المبيعات", self.show_sales),
            ("الموظفين", self.show_employees),
            ("الحسابات", self.show_accounts),
            ("مساعدة", self.show_help),
            ("اشتراكي", self.show_subscription)
        ]

        # إنشاء الأزرار
        buttons_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)

        for i, (text, command) in enumerate(menu_items):
            # التحقق من وجود theme_manager وإنشاء الزر المناسب
            if hasattr(self, 'theme_manager') and self.theme_manager:
                try:
                    btn = self.theme_manager.create_styled_button(
                        buttons_frame,
                        text=text,
                        command=command,
                        button_type="secondary",
                        width=80,
                        height=30,
                        font_size=11
                    )
                except Exception as e:
                    # في حالة فشل theme_manager، استخدم الزر العادي
                    btn = ctk.CTkButton(
                        buttons_frame,
                        text=text,
                        command=command,
                        width=80,
                        height=30,
                        font=(FONTS.get('arabic', 'Arial'), 11),
                        fg_color=MODERN_COLORS.get('primary', '#2E8B57'),
                        hover_color=get_hover_color(MODERN_COLORS.get('primary', '#2E8B57')),
                        corner_radius=8
                    )
            else:
                # إنشاء زر عادي بدون theme_manager
                btn = ctk.CTkButton(
                    buttons_frame,
                    text=text,
                    command=command,
                    width=80,
                    height=30,
                    font=(FONTS.get('arabic', 'Arial'), 11),
                    fg_color=MODERN_COLORS.get('primary', '#2E8B57'),
                    hover_color=get_hover_color(MODERN_COLORS.get('primary', '#2E8B57')),
                    corner_radius=8
                )
            btn.pack(side="right", padx=5, pady=20)

    def create_user_tools(self, parent):
        """إنشاء أدوات المستخدم"""
        tools_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tools_frame.pack(side="left", fill="y", padx=20)

        # زر تغيير الثيم
        if hasattr(self, 'theme_manager') and self.theme_manager:
            try:
                theme_btn = self.theme_manager.create_styled_button(
                    tools_frame,
                    text="🌙" if self.theme_manager.current_theme == "light" else "☀️",
                    command=self.toggle_theme,
                    button_type="settings",
                    width=40,
                    height=40,
                    font_size=16
                )
            except Exception as e:
                theme_btn = ctk.CTkButton(
                    tools_frame,
                    text="🌙",
                    command=self.toggle_theme,
                    width=40,
                    height=40,
                    fg_color=MODERN_COLORS.get('secondary', '#4682B4'),
                    corner_radius=8
                )
        else:
            theme_btn = ctk.CTkButton(
                tools_frame,
                text="🌙",
                command=self.toggle_theme,
                width=40,
                height=40,
                fg_color=MODERN_COLORS.get('secondary', '#4682B4'),
                corner_radius=8
            )
        theme_btn.pack(side="top", pady=5)

        # زر تسجيل الخروج
        if hasattr(self, 'theme_manager') and self.theme_manager:
            try:
                logout_btn = self.theme_manager.create_styled_button(
                    tools_frame,
                    text="خروج",
                    command=self.logout,
                    button_type="secondary",
                    width=60,
                    height=30,
                    font_size=10
                )
            except Exception as e:
                logout_btn = ctk.CTkButton(
                    tools_frame,
                    text="خروج",
                    command=self.logout,
                    width=60,
                    height=30,
                    font=(FONTS.get('arabic', 'Arial'), 10),
                    fg_color=MODERN_COLORS.get('danger', '#dc3545'),
                    corner_radius=8
                )
        else:
            logout_btn = ctk.CTkButton(
                tools_frame,
                text="خروج",
                command=self.logout,
                width=60,
                height=30,
                font=(FONTS.get('arabic', 'Arial'), 10),
                fg_color=MODERN_COLORS.get('danger', '#dc3545'),
                corner_radius=8
            )
        logout_btn.pack(side="top", pady=5)

    def create_user_info_bottom(self, parent):
        """إنشاء معلومات المستخدم في الأسفل"""
        user_frame = ctk.CTkFrame(parent, height=120, fg_color="transparent")
        user_frame.pack(side="bottom", fill="x", pady=10)
        user_frame.pack_propagate(False)

        # إطار معلومات المستخدم في الجانب الأيسر
        user_info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
        user_info_frame.pack(side="left", padx=20)

        # الصورة الشخصية (دائرية)
        profile_frame = ctk.CTkFrame(user_info_frame, width=70, height=70, fg_color=MODERN_COLORS['card'], corner_radius=35)
        profile_frame.pack(side="left", padx=(0, 15))
        profile_frame.pack_propagate(False)

        # صورة افتراضية (يمكن استبدالها بصورة حقيقية)
        profile_label = ctk.CTkLabel(
            profile_frame,
            text="👤",
            font=(FONTS['icon'], FONTS['sizes']['xlarge']),
            text_color="white"
        )
        profile_label.pack(expand=True)

        # معلومات المستخدم
        info_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="y")

        # الاسم
        name_label = ctk.CTkLabel(
            info_frame,
            text="رئيس مجلس الإدارة",
            font=(FONTS['arabic'], FONTS['sizes']['medium'], "bold"),
            text_color=MODERN_COLORS['text_primary'],
            anchor="w"
        )
        name_label.pack(anchor="w", pady=(10, 2))

        # المسمى الوظيفي
        title_label = ctk.CTkLabel(
            info_frame,
            text="محمود عبد الحميد",
            font=(FONTS['arabic'], FONTS['sizes']['normal']),
            text_color=MODERN_COLORS['text_secondary'],
            anchor="w"
        )
        title_label.pack(anchor="w")

        # نوع المستخدم
        user_type_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
        user_type_frame.pack(side="right", padx=20)

        user_type_label = ctk.CTkLabel(
            user_type_frame,
            text="حدد نوع المستخدم",
            font=(FONTS['arabic'], FONTS['sizes']['normal']),
            text_color=MODERN_COLORS['text_primary']
        )
        user_type_label.pack(pady=10)

    def create_old_sidebar(self, parent):
        """إنشاء الشريط الجانبي الأيمن"""
        sidebar_frame = self.theme_manager.create_styled_frame(
            parent,
            width=250,
            corner_radius=10
        )
        sidebar_frame.pack(side="right", fill="y", padx=(0, 10))
        sidebar_frame.pack_propagate(False)

        # معلومات المستخدم
        user_frame = self.theme_manager.create_styled_frame(
            sidebar_frame,
            corner_radius=8
        )
        user_frame.pack(fill="x", padx=10, pady=10)

        # صورة المستخدم (مؤقت - رمز)
        user_icon = self.theme_manager.create_styled_label(
            user_frame,
            text="👤",
            font_size=48
        )
        user_icon.pack(pady=(15, 5))

        # اسم المستخدم
        user_name = self.theme_manager.create_styled_label(
            user_frame,
            text=self.current_user['full_name'],
            font_size=16
        )
        user_name.pack(pady=2)

        # المسمى الوظيفي
        role_names = {
            'admin': 'مدير النظام',
            'accountant': 'محاسب',
            'user': 'مستخدم'
        }
        user_role = self.theme_manager.create_styled_label(
            user_frame,
            text=role_names.get(self.current_user['role'], 'مستخدم'),
            font_size=12
        )
        user_role.configure(text_color=self.theme_manager.get_color("text_secondary"))
        user_role.pack(pady=(0, 15))

        # إحصائيات سريعة
        stats_frame = self.theme_manager.create_styled_frame(
            sidebar_frame,
            corner_radius=8
        )
        stats_frame.pack(fill="x", padx=10, pady=10)

        stats_title = self.theme_manager.create_styled_label(
            stats_frame,
            text="إحصائيات اليوم",
            font_size=14
        )
        stats_title.pack(pady=(10, 5))

        # إحصائيات وهمية (ستكون حقيقية لاحقاً)
        stats_data = [
            ("المبيعات", "15,250 ر.س"),
            ("الفواتير", "23 فاتورة"),
            ("العملاء الجدد", "5 عملاء")
        ]

        for label, value in stats_data:
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.pack(fill="x", padx=10, pady=2)

            stat_label = self.theme_manager.create_styled_label(
                stat_frame,
                text=f"{label}:",
                font_size=10
            )
            stat_label.pack(side="right")

            stat_value = self.theme_manager.create_styled_label(
                stat_frame,
                text=value,
                font_size=10
            )
            stat_value.configure(text_color=self.theme_manager.get_color("primary"))
            stat_value.pack(side="left")

        # مساحة فارغة
        ctk.CTkLabel(stats_frame, text="", height=10).pack()

    def create_main_grid_area(self, parent):
        """إنشاء منطقة الشبكة الرئيسية للأيقونات"""
        # إطار التقارير
        reports_frame = ctk.CTkFrame(parent, fg_color="transparent")
        reports_frame.pack(fill="both", expand=True, pady=20)

        # عنوان التقارير
        reports_title = ctk.CTkLabel(
            reports_frame,
            text="تقارير",
            font=(FONTS['arabic'], FONTS['sizes']['large'], "bold"),
            text_color=MODERN_COLORS['text_primary'],
            anchor="e"
        )
        reports_title.pack(anchor="ne", padx=20, pady=(0, 10))

        # الصف الأول من الأيقونات
        first_row = ctk.CTkFrame(reports_frame, fg_color="transparent")
        first_row.pack(fill="x", padx=20, pady=5)

        first_row_icons = [
            ("assets/icons/6.png", "تحليل المبيعات", MODERN_COLORS['icon_blue'], self.open_sales_analysis, "assets/icons/6.png"),
            ("assets/icons/3.png", "الحركة اليومية", MODERN_COLORS['icon_purple'], self.open_daily_movement, "assets/icons/3.png"),
            ("assets/icons/23.png", "إدخال الحسابات", MODERN_COLORS['icon_yellow'], self.open_account_entry, "assets/icons/23.png"),
            ("assets/icons/26.png", "إدارة الأصناف", MODERN_COLORS['icon_cyan'], self.show_warehouses, "assets/icons/26.png"),
            ("⚙️", "الإعدادات", MODERN_COLORS['icon_purple'], self.open_settings, "assets/icons/53.ico"),
            ("assets/icons/12.png", "أهلاً بكم", MODERN_COLORS['icon_sky_blue'], self.open_welcome, "assets/icons/12.png")
        ]

        for icon, text, color, command, icon_path in first_row_icons:
            self.create_grid_button(first_row, icon, text, color, command, icon_path)

        # الصف الثاني من الأيقونات
        second_row = ctk.CTkFrame(reports_frame, fg_color="transparent")
        second_row.pack(fill="x", padx=20, pady=5)

        second_row_icons = [
            ("assets/icons/24.png", "مؤشرات", MODERN_COLORS['icon_teal'], self.open_indicators, "assets/icons/24.png"),
            ("assets/icons/18.png", "صرف", MODERN_COLORS['icon_red'], self.open_expenses, "assets/icons/18.png"),
            ("assets/icons/54.ico", "شراء", MODERN_COLORS['icon_dark_red'], self.open_purchases, "assets/icons/54.ico"),
            ("assets/icons/50.jpg", "بيع", MODERN_COLORS['icon_green'], self.open_sales, "assets/icons/50.jpg"),
            ("assets/icons/21.png", "إدارة المخزون", MODERN_COLORS['warning'], self.open_warehouse, "assets/icons/21.png")
        ]

        for icon, text, color, command, icon_path in second_row_icons:
            self.create_grid_button(second_row, icon, text, color, command, icon_path)

        # الصف الثالث من الأيقونات
        third_row = ctk.CTkFrame(reports_frame, fg_color="transparent")
        third_row.pack(fill="x", padx=20, pady=5)

        third_row_icons = [
            ("assets/icons/46.jpg", "تسوية مخزن", MODERN_COLORS['icon_dark_teal'], self.open_inventory_adjustment, "assets/icons/46.jpg"),
            ("assets/icons/47.jpg", "تحويل لمخزن", MODERN_COLORS['icon_blue_2'], self.open_inventory_transfer, "assets/icons/47.jpg"),
            ("assets/icons/25.png", "قيمة", MODERN_COLORS['icon_violet'], self.open_value, "assets/icons/25.png"),
            ("assets/icons/38.ico", "مرتجع شراء", MODERN_COLORS['icon_dark_violet'], self.open_purchase_returns, "assets/icons/38.ico"),
            ("assets/icons/44.jpg", "عرض أسعار", MODERN_COLORS['icon_teal'], self.open_price_list, "assets/icons/44.jpg"),
            ("assets/icons/21.png", "مرتجع بيع", MODERN_COLORS['icon_light_green'], self.open_sales_returns, "assets/icons/21.png")
        ]

        for icon, text, color, command, icon_path in third_row_icons:
            self.create_grid_button(third_row, icon, text, color, command, icon_path, 'medium', 10)

    def create_grid_button(self, parent, icon, text, color, command, icon_path=None, font_size='large', top_padding=15):
        """إنشاء زر في الشبكة"""
        button_frame = ctk.CTkFrame(parent, width=DIMENSIONS['button_width'], height=DIMENSIONS['button_height'], fg_color=color, corner_radius=DIMENSIONS['border_radius'])
        button_frame.pack(side="right", padx=DIMENSIONS['margin'], pady=DIMENSIONS['margin'])
        button_frame.pack_propagate(False)

        # إطار للأيقونة في الأعلى
        icon_frame = ctk.CTkFrame(button_frame, fg_color="transparent", height=90)
        icon_frame.pack(fill="x", pady=(top_padding, 5))
        icon_frame.pack_propagate(False)

        # الأيقونة
        if icon_path and os.path.exists(icon_path):
            # استخدام صورة من ملف - تكبير 4 أضعاف
            icon_image = self.load_icon_image(icon_path, (80, 80))  # تصغير الأيقونات
            if icon_image:
                icon_label = ctk.CTkLabel(
                    icon_frame,
                    image=icon_image,
                    text=""
                )
            else:
                # في حالة فشل تحميل الصورة، استخدم النص
                icon_label = ctk.CTkLabel(
                    icon_frame,
                    text=icon,
                    font=(FONTS['icon'], DIMENSIONS['icon_size']),
                    text_color=MODERN_COLORS['text_primary']
                )
        else:
            # استخدام رمز تعبيري
            icon_label = ctk.CTkLabel(
                icon_frame,
                text=icon,
                font=(FONTS['icon'], DIMENSIONS['icon_size']),
                text_color=MODERN_COLORS['text_primary']
            )
        icon_label.pack(expand=True, anchor="center")

        # إطار للنص في الأسفل
        text_frame = ctk.CTkFrame(button_frame, fg_color="transparent", height=40)
        text_frame.pack(fill="x", pady=(0, 10))
        text_frame.pack_propagate(False)

        # النص في المنتصف أسفل الأيقونة
        text_label = ctk.CTkLabel(
            text_frame,
            text=text,
            font=(FONTS['arabic'], FONTS['sizes'][font_size], "bold"),
            text_color=MODERN_COLORS['text_primary'],
            wraplength=120,
            justify="center",
            anchor="center"
        )
        text_label.pack(expand=True, fill="both")

        # جعل الزر قابل للنقر
        button_frame.bind("<Button-1>", lambda e: command())
        icon_frame.bind("<Button-1>", lambda e: command())
        icon_label.bind("<Button-1>", lambda e: command())
        text_frame.bind("<Button-1>", lambda e: command())
        text_label.bind("<Button-1>", lambda e: command())

        # تأثير التمرير
        def on_enter(e):
            button_frame.configure(fg_color=self.lighten_color(color))

        def on_leave(e):
            button_frame.configure(fg_color=color)

        button_frame.bind("<Enter>", on_enter)
        button_frame.bind("<Leave>", on_leave)
        icon_frame.bind("<Enter>", on_enter)
        icon_frame.bind("<Leave>", on_leave)
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
        text_frame.bind("<Enter>", on_enter)
        text_frame.bind("<Leave>", on_leave)
        text_label.bind("<Enter>", on_enter)
        text_label.bind("<Leave>", on_leave)

    def lighten_color(self, color):
        """تفتيح اللون للتأثير عند التمرير"""
        return get_hover_color(color)

    def load_icon_image(self, icon_path: str, size: tuple = (160, 160)) -> Optional[Any]:
        """
        تحميل أيقونة من ملف صورة مع معالجة شاملة للأخطاء
        Load icon image from file with comprehensive error handling

        Args:
            icon_path: مسار ملف الصورة
            size: حجم الصورة المطلوب (العرض، الارتفاع)

        Returns:
            CTkImage object أو None في حالة الفشل
        """
        try:
            # التحقق من توفر PIL
            if not PIL_AVAILABLE or Image is None:
                if ERROR_HANDLING_AVAILABLE:
                    log_warning("PIL غير متوفر، لا يمكن تحميل الصور")
                return None

            # التحقق من صحة وأمان المعاملات
            if not self._validate_file_path(icon_path):
                print("خطأ: مسار الصورة غير صحيح أو غير آمن")
                return None

            if not isinstance(size, tuple) or len(size) != 2:
                print("خطأ: حجم الصورة غير صحيح")
                size = (160, 160)

            # التحقق من وجود الملف
            if not os.path.exists(icon_path):
                print(f"تحذير: ملف الصورة غير موجود: {icon_path}")
                return None

            # إنشاء مفتاح التخزين المؤقت
            cache_key = f"{icon_path}_{size[0]}x{size[1]}"

            # التحقق من التخزين المؤقت
            if cache_key in self.loaded_images:
                return self.loaded_images[cache_key]

            print(f"تحميل الصورة: {icon_path} بحجم {size}")

            # تحميل الصورة وتغيير حجمها
            with Image.open(icon_path) as image:
                print(f"حجم الصورة الأصلي: {image.size}")

                # الحفاظ على الشفافية وإزالة الخلفية البيضاء
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')

                # إزالة الخلفية البيضاء
                image = self._remove_white_background(image)

                # تغيير حجم الصورة
                image = image.resize(size, Image.Resampling.LANCZOS)
                print(f"حجم الصورة بعد التغيير: {image.size}")

                # تحويل إلى CTkImage
                ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=size)
                self.loaded_images[cache_key] = ctk_image
                print("تم إنشاء CTkImage بنجاح")

                return ctk_image

        except FileNotFoundError:
            print(f"خطأ: ملف الصورة غير موجود: {icon_path}")
        except PermissionError:
            print(f"خطأ: لا توجد صلاحية لقراءة الملف: {icon_path}")
        except Exception as e:
            error_msg = f"خطأ في تحميل الأيقونة {icon_path}: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            traceback.print_exc()

        return None

    def _remove_white_background(self, image: Any) -> Any:
        """
        إزالة الخلفية البيضاء من الصورة
        Remove white background from image
        """
        try:
            if NUMPY_AVAILABLE and np is not None:
                # استخدام numpy للسرعة
                data = np.array(image)

                # تحديد البكسلات البيضاء (RGB > 240)
                white_mask = (data[:, :, 0] > 240) & (data[:, :, 1] > 240) & (data[:, :, 2] > 240)

                # جعل البكسلات البيضاء شفافة
                data[white_mask] = [255, 255, 255, 0]

                # تحويل العودة إلى صورة
                return Image.fromarray(data, 'RGBA')
            else:
                # طريقة بديلة بدون numpy
                print("numpy غير متوفر، استخدام طريقة بديلة لإزالة الخلفية")
                datas = image.getdata()
                new_data = []
                for item in datas:
                    if len(item) >= 3 and item[0] > 240 and item[1] > 240 and item[2] > 240:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                image.putdata(new_data)
                return image

        except Exception as e:
            print(f"خطأ في معالجة الصورة: {e}")
            return image  # إرجاع الصورة الأصلية في حالة الخطأ

    def load_icon_image_no_bg(self, icon_path: str, size: tuple = (50, 50)) -> Optional[Any]:
        """
        تحميل أيقونة من ملف صورة مع إزالة الخلفية البيضاء المحسنة
        Load icon image with enhanced white background removal

        Args:
            icon_path: مسار ملف الصورة
            size: حجم الصورة المطلوب

        Returns:
            CTkImage object أو None في حالة الفشل
        """
        try:
            # التحقق من توفر PIL
            if not PIL_AVAILABLE or Image is None:
                if ERROR_HANDLING_AVAILABLE:
                    log_warning("PIL غير متوفر، لا يمكن تحميل الصور")
                return None

            # التحقق من صحة المعاملات
            if not icon_path or not isinstance(icon_path, str):
                print("خطأ: مسار الصورة غير صحيح")
                return None

            if not os.path.exists(icon_path):
                print(f"تحذير: ملف الصورة غير موجود: {icon_path}")
                return None

            cache_key = f"{icon_path}_nobg_{size[0]}x{size[1]}"

            # التحقق من التخزين المؤقت
            if cache_key in self.loaded_images:
                return self.loaded_images[cache_key]

            print(f"تحميل الصورة مع إزالة الخلفية: {icon_path} بحجم {size}")

            # تحميل الصورة
            with Image.open(icon_path) as image:
                print(f"حجم الصورة الأصلي: {image.size}")

                # تحويل إلى RGBA للشفافية
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')

                # إزالة الخلفية البيضاء بطريقة محسنة
                image = self._remove_white_background_enhanced(image)

                # تغيير الحجم
                image = image.resize(size, Image.Resampling.LANCZOS)
                print(f"حجم الصورة بعد التغيير: {image.size}")

                # تحويل إلى CTkImage
                ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=size)
                self.loaded_images[cache_key] = ctk_image
                print("تم إنشاء CTkImage مع إزالة الخلفية بنجاح")

                return ctk_image

        except Exception as e:
            error_msg = f"خطأ في تحميل الأيقونة مع إزالة الخلفية {icon_path}: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            traceback.print_exc()

        return None

    def _remove_white_background_enhanced(self, image: Any) -> Any:
        """
        إزالة محسنة للخلفية البيضاء مع معالجة الألوان الرمادية
        Enhanced white background removal with gray color handling
        """
        try:
            data = image.getdata()
            new_data = []

            for item in data:
                if len(item) < 3:
                    new_data.append(item)
                    continue

                # إذا كان البكسل أبيض أو قريب من الأبيض، اجعله شفاف
                if item[0] > 230 and item[1] > 230 and item[2] > 230:
                    new_data.append((255, 255, 255, 0))  # شفاف تمام
                elif item[0] > 200 and item[1] > 200 and item[2] > 200:
                    # للألوان الرمادية الفاتحة، قلل الشفافية
                    alpha = max(0, 255 - (item[0] + item[1] + item[2]) // 3)
                    new_data.append((item[0], item[1], item[2], alpha))
                else:
                    new_data.append(item)

            image.putdata(new_data)
            return image

        except Exception as e:
            print(f"خطأ في معالجة إزالة الخلفية: {e}")
            return image  # إرجاع الصورة الأصلية في حالة الخطأ

    def clear_image_cache(self) -> None:
        """
        مسح ذاكرة التخزين المؤقت للصور لتحرير الذاكرة
        Clear image cache to free memory
        """
        try:
            cache_size = len(self.loaded_images)
            self.loaded_images.clear()
            print(f"تم مسح {cache_size} صورة من ذاكرة التخزين المؤقت")
            if ERROR_HANDLING_AVAILABLE:
                log_info(f"تم مسح ذاكرة التخزين المؤقت للصور: {cache_size} صورة")
        except Exception as e:
            print(f"خطأ في مسح ذاكرة التخزين المؤقت: {e}")

    def get_cache_info(self) -> Dict[str, Any]:
        """
        الحصول على معلومات ذاكرة التخزين المؤقت
        Get cache information
        """
        try:
            return {
                'cached_images': len(self.loaded_images),
                'cache_keys': list(self.loaded_images.keys())
            }
        except Exception as e:
            print(f"خطأ في الحصول على معلومات ذاكرة التخزين المؤقت: {e}")
            return {'cached_images': 0, 'cache_keys': []}

    def _get_asset_path(self, *path_parts: str) -> str:
        """
        الحصول على مسار الأصول مع دعم متعدد المنصات
        Get asset path with cross-platform support
        """
        try:
            # استخدام pathlib للتعامل مع المسارات بطريقة متوافقة مع جميع المنصات
            base_path = Path("assets")
            asset_path = base_path.joinpath(*path_parts)
            return str(asset_path)
        except Exception as e:
            print(f"خطأ في تكوين مسار الأصول: {e}")
            # fallback إلى os.path.join
            return os.path.join("assets", *path_parts)

    def check_database_health(self) -> bool:
        """
        فحص صحة الاتصال بقاعدة البيانات
        Check database connection health
        """
        try:
            if self.db_manager is None:
                return False

            # محاولة تنفيذ استعلام بسيط للتحقق من الاتصال
            if hasattr(self.db_manager, 'test_connection'):
                return self.db_manager.test_connection()
            else:
                # fallback: التحقق من وجود المدير فقط
                return True

        except Exception as e:
            error_msg = f"خطأ في فحص صحة قاعدة البيانات: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            return False

    def reconnect_database(self) -> bool:
        """
        إعادة الاتصال بقاعدة البيانات
        Reconnect to database
        """
        try:
            print("محاولة إعادة الاتصال بقاعدة البيانات...")

            # إعادة تهيئة مدير قاعدة البيانات
            self._initialize_database_manager()

            # التحقق من نجاح الاتصال
            if self.check_database_health():
                print("تم إعادة الاتصال بقاعدة البيانات بنجاح")
                if ERROR_HANDLING_AVAILABLE:
                    log_info("تم إعادة الاتصال بقاعدة البيانات بنجاح")
                return True
            else:
                print("فشل في إعادة الاتصال بقاعدة البيانات")
                return False

        except Exception as e:
            error_msg = f"خطأ في إعادة الاتصال بقاعدة البيانات: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            return False

    def cleanup_resources(self) -> None:
        """
        تنظيف الموارد عند إغلاق التطبيق
        Cleanup resources on application shutdown
        """
        try:
            print("بدء تنظيف موارد التطبيق...")

            # مسح ذاكرة التخزين المؤقت للصور
            self.clear_image_cache()

            # إغلاق اتصال قاعدة البيانات
            if self.db_manager and hasattr(self.db_manager, 'close'):
                try:
                    self.db_manager.close()
                    print("تم إغلاق اتصال قاعدة البيانات")
                except Exception as db_error:
                    print(f"خطأ في إغلاق قاعدة البيانات: {db_error}")

            # تنظيف المتغيرات
            self.auth_manager = None
            self.current_user = None
            self.sales_manager = None

            print("تم تنظيف موارد التطبيق بنجاح")
            if ERROR_HANDLING_AVAILABLE:
                log_info("تم تنظيف موارد التطبيق بنجاح")

        except Exception as e:
            error_msg = f"خطأ في تنظيف الموارد: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)

    def _validate_file_path(self, file_path: str) -> bool:
        """
        التحقق من صحة وأمان مسار الملف
        Validate file path for security
        """
        try:
            if not file_path or not isinstance(file_path, str):
                return False

            # تحويل إلى مسار مطلق للتحقق من الأمان
            abs_path = os.path.abspath(file_path)

            # التحقق من أن المسار داخل مجلد المشروع
            project_root = os.path.abspath(".")
            if not abs_path.startswith(project_root):
                print(f"تحذير أمني: محاولة الوصول لملف خارج المشروع: {file_path}")
                return False

            # التحقق من امتدادات الملفات المسموحة للصور
            allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico'}
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in allowed_extensions:
                print(f"تحذير: امتداد ملف غير مسموح: {file_ext}")
                return False

            return True

        except Exception as e:
            print(f"خطأ في التحقق من مسار الملف: {e}")
            return False

    def _sanitize_input(self, user_input: str) -> str:
        """
        تنظيف المدخلات من المستخدم
        Sanitize user input
        """
        try:
            if not isinstance(user_input, str):
                return ""

            # إزالة المحارف الخطيرة
            dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
            sanitized = user_input

            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')

            # تحديد الطول الأقصى
            max_length = 1000
            if len(sanitized) > max_length:
                sanitized = sanitized[:max_length]

            return sanitized.strip()

        except Exception as e:
            print(f"خطأ في تنظيف المدخلات: {e}")
            return ""

    def create_old_main_icons_area(self, parent):
        """إنشاء منطقة الأيقونات الرئيسية"""
        icons_frame = self.theme_manager.create_styled_frame(
            parent,
            corner_radius=10
        )
        icons_frame.pack(fill="both", expand=True, padx=(10, 0))

        # عنوان المنطقة
        title_frame = ctk.CTkFrame(icons_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))

        main_title = self.theme_manager.create_styled_label(
            title_frame,
            text="الوظائف الرئيسية",
            font_size=18
        )
        main_title.pack(anchor="e")

        # منطقة الأيقونات
        grid_frame = ctk.CTkFrame(icons_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # تعريف الأيقونات والوظائف
        icons_data = [
            # الصف الأول
            [
                ("📊", "تقارير", "reports", self.open_reports),
                ("📋", "الحركة اليومية", "sales", self.open_daily_movement),
                ("📝", "إدخال الحسابات", "accounts", self.open_accounts_entry),
                ("📄", "إدخال الأصناف", "inventory", self.show_warehouses),
                ("👥", "أعداد رقم", "customers", self.open_number_setup)
            ],
            # الصف الثاني
            [
                ("✅", "موافقين", "success", self.open_approvals),
                ("💰", "صرف", "treasury", self.open_expense),
                ("🛒", "شراء", "purchase", self.open_purchase),
                ("💳", "بيع", "sales", self.open_sales),
                ("👥", "قائمة العملاء", "sales", self.open_client_list)
            ],
            # الصف الثالث
            [
                ("🏬", "إدارة المخازن", "inventory", self.open_warehouses_management),
                ("📊", "تسوية مخزن", "inventory", self.open_inventory_adjustment),
                ("🚚", "تحويل لمخزن", "inventory", self.open_inventory_transfer),
                ("💎", "قيمة", "treasury", self.open_value_management),
                ("📋", "مرتجع شراء", "purchase", self.open_purchase_return),
                ("➕", "عرض أسعار", "sales", self.open_price_quote)
            ],
            # الصف الرابع
            [
                ("🛒", "مرتجع بيع", "sales", self.open_sales_return)
            ]
        ]

        # إنشاء الشبكة
        for row_idx, row_data in enumerate(icons_data):
            row_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=GRID_SPACING//2)

            for col_idx, (icon, text, btn_type, command) in enumerate(row_data):
                # التحقق من الصلاحيات
                if not self.has_permission_for_function(btn_type):
                    continue

                # إنشاء الزر
                btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=GRID_SPACING//2)

                icon_btn = self.theme_manager.create_styled_button(
                    btn_frame,
                    text=f"{icon}\n{text}",
                    command=command,
                    button_type=btn_type,
                    width=BUTTON_SIZE[0],
                    height=BUTTON_SIZE[1],
                    font_size=12
                )
                icon_btn.pack()

    def create_bottom_taskbar(self, parent):
        """إنشاء شريط المهام السفلي"""
        taskbar = ctk.CTkFrame(parent, height=DIMENSIONS['bottom_bar_height'], fg_color="#1E1E1E")
        taskbar.pack(side="bottom", fill="x")
        taskbar.pack_propagate(False)

        # زر البداية
        start_btn = ctk.CTkButton(
            taskbar,
            text="⊞",
            width=40,
            height=40,
            fg_color="#0078D4",
            font=("Arial", 16),
            corner_radius=0
        )
        start_btn.pack(side="left", padx=5, pady=5)

        # أيقونات التطبيقات
        app_icons = [
            ("📁", "#FFB347"),  # مجلد
            ("🌐", "#4285F4"),  # متصفح
            ("📧", "#EA4335"),  # بريد
            ("📊", "#34A853"),  # إكسل
            ("💬", "#00BCD4"),  # محادثة
            ("🔧", "#FF9800"),  # أدوات
            ("📱", "#9C27B0"),  # تطبيق
            ("🎵", "#E91E63")   # موسيقى
        ]

        for icon, color in app_icons:
            app_btn = ctk.CTkButton(
                taskbar,
                text=icon,
                width=40,
                height=40,
                fg_color=color,
                font=("Arial", 16),
                corner_radius=5
            )
            app_btn.pack(side="left", padx=2, pady=5)

        # الوقت والتاريخ
        time_frame = ctk.CTkFrame(taskbar, fg_color="transparent")
        time_frame.pack(side="right", padx=10, pady=5)

        now = datetime.now()

        time_label = ctk.CTkLabel(
            time_frame,
            text=now.strftime("%H:%M"),
            font=("Arial", 12, "bold"),
            text_color="white"
        )
        time_label.pack()

        date_label = ctk.CTkLabel(
            time_frame,
            text=now.strftime("%Y/%m/%d"),
            font=("Arial", 10),
            text_color="#CCCCCC"
        )
        date_label.pack()

    def create_old_bottom_bar(self, parent):
        """إنشاء الشريط السفلي"""
        bottom_frame = self.theme_manager.create_styled_frame(
            parent,
            height=60,
            corner_radius=10
        )
        bottom_frame.pack(fill="x", pady=(10, 0))
        bottom_frame.pack_propagate(False)

        # روابط وسائل التواصل الاجتماعي
        social_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        social_frame.pack(side="right", fill="y", padx=20)

        social_links = [
            ("📘", "فيسبوك", self.open_facebook),
            ("📺", "يوتيوب", self.open_youtube),
            ("🌐", "الموقع", self.open_website),
            ("📧", "البريد", self.open_email)
        ]

        for icon, text, command in social_links:
            social_btn = self.theme_manager.create_styled_button(
                social_frame,
                text=icon,
                command=command,
                button_type="secondary",
                width=40,
                height=40,
                font_size=16
            )
            social_btn.pack(side="right", padx=5, pady=10)

        # معلومات النظام
        info_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="y", padx=20)

        # الوقت والتاريخ
        now = datetime.now()
        time_label = self.theme_manager.create_styled_label(
            info_frame,
            text=f"التاريخ: {now.strftime('%Y-%m-%d')} | الوقت: {now.strftime('%H:%M')}",
            font_size=10
        )
        time_label.configure(text_color=self.theme_manager.get_color("text_secondary"))
        time_label.pack(pady=20)

    # وظائف الصلاحيات
    def has_permission_for_function(self, function_type):
        """التحقق من صلاحية الوصول لوظيفة معينة"""
        if not self.auth_manager or not self.auth_manager.current_user:
            return False

        permission_map = {
            'sales': 'view_sales',
            'purchase': 'view_purchases',
            'treasury': 'view_treasury',
            'inventory': 'view_inventory',
            'reports': 'view_reports',
            'accounts': 'view_customers',
            'customers': 'view_customers',
            'success': True  # الموافقات متاحة للجميع
        }

        permission = permission_map.get(function_type, True)
        if permission:
            return True

        return self.auth_manager.has_permission(permission)

    # وظائف القائمة العلوية
    def show_program_info(self):
        """عرض معلومات البرنامج"""
        messagebox.showinfo("معلومات البرنامج",
                            f"{WINDOW_TITLE}\nالإصدار 1.0\nتطوير: فريق التطوير")

    def show_print_options(self):
        """عرض خيارات الطباعة"""
        messagebox.showinfo("الطباعة", "خيارات الطباعة ستكون متاحة قريباً")

    def show_accounts(self) -> None:
        """عرض نافذة إدارة الحسابات"""
        try:
            if AccountsWindow is not None:
                accounts_window = AccountsWindow(self.main_window, self.db_manager)
                if ERROR_HANDLING_AVAILABLE:
                    log_info("تم فتح نافذة الحسابات")
            else:
                messagebox.showinfo("الحسابات", "نافذة الحسابات غير متاحة حال")
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة الحسابات: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            messagebox.showerror("خطأ", "فشل في فتح نافذة الحسابات")

    def show_invoices(self) -> None:
        """عرض نافذة إدارة الفواتير"""
        try:
            if InvoicesMainWindow is not None:
                invoices_window = InvoicesMainWindow(self.main_window, self.db_manager)
                if ERROR_HANDLING_AVAILABLE:
                    log_info("تم فتح نافذة الفواتير")
            else:
                messagebox.showinfo("الفواتير", "نافذة الفواتير غير متاحة حال")
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة الفواتير: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            messagebox.showerror("خطأ", "فشل في فتح نافذة الفواتير")

    def show_treasury(self) -> None:
        """عرض نافذة إدارة الخزينة"""
        try:
            if TreasuryWindow is not None:
                treasury_window = TreasuryWindow(self.main_window, self.db_manager)
                if ERROR_HANDLING_AVAILABLE:
                    log_info("تم فتح نافذة الخزينة")
            else:
                messagebox.showinfo("الخزينة", "نافذة الخزينة قيد التطوير وستكون متاحة قريباً")
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة الخزينة: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            messagebox.showerror("خطأ", "فشل في فتح نافذة الخزينة")

    def show_reports(self) -> None:
        """عرض نافذة التقارير"""
        try:
            if ReportsWindow is not None:
                reports_window = ReportsWindow(self.main_window, self.db_manager)
                if ERROR_HANDLING_AVAILABLE:
                    log_info("تم فتح نافذة التقارير")
            else:
                messagebox.showinfo("التقارير", "نافذة التقارير غير متاحة حال")
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة التقارير: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            messagebox.showerror("خطأ", "فشل في فتح نافذة التقارير")

    def show_help(self):
        """عرض المساعدة"""
        help_text = """
        مرحباً بك في برنامج ست الكل للمحاسبة

        للمساعدة:
        - اتصل بنا: 123-456-7890
        - البريد الإلكتروني: support@example.com
        - الموقع الإلكتروني: www.example.com
        """
        messagebox.showinfo("المساعدة", help_text)

    def show_subscription(self):
        """عرض معلومات الاشتراك"""
        messagebox.showinfo("الاشتراك", "معلومات الاشتراك ستكون متاحة قريباً")

    def show_main_page(self):
        """عرض قائمة منسدلة للصفحة الرئيسية"""
        try:
            self.show_main_dropdown_menu()
        except Exception as e:
            print(f"خطأ في القائمة المنسدلة: {e}")
            # في حالة فشل القائمة المنسدلة، عرض قائمة بسيطة
            try:
                self.show_simple_main_menu()
            except Exception as e2:
                print(f"خطأ في القائمة البسيطة: {e2}")
                messagebox.showinfo("قائمة الرئيسية", "قائمة الرئيسية ستكون متاحة قريباً")

    # تحذير: دالة معقدة (تعقيد: 24) - استخدم list comprehensions بدلاً من loops معقدة
    def show_main_dropdown_menu(self):
        """عرض القائمة المنسدلة الاحترافية المدمجة مع الشريط العلوي"""
        try:
            # التحقق من وجود النافذة الرئيسية
            if not hasattr(self, 'main_window') or not self.main_window:
                print("خطأ: النافذة الرئيسية غير متاحة")
                self.show_simple_main_menu()
                return

            # التحقق من وجود النافذة وأنها لا تزال موجودة
            try:
                if not self.main_window.winfo_exists():
                    print("خطأ: النافذة الرئيسية غير موجودة")
                    self.show_simple_main_menu()
                    return
            except Exception:
                print("خطأ: فشل في التحقق من النافذة الرئيسية")
                self.show_simple_main_menu()
                return

            # إنشاء نافذة القائمة المنسدلة الاحترافية
            dropdown_window = ctk.CTkToplevel(self.main_window)
            dropdown_window.title("")
            dropdown_window.resizable(False, False)

            # إزالة شريط العنوان لمظهر احترافي
            try:
                dropdown_window.overrideredirect(True)
            except Exception:
                pass

            # تطبيق الألوان الحديثة
            try:
                dropdown_window.configure(fg_color='#ffffff')
            except Exception as e:
                print(f"تحذير: فشل في تطبيق الألوان: {e}")

            # جعل النافذة في المقدمة
            try:
                dropdown_window.transient(self.main_window)
                dropdown_window.grab_set()
                dropdown_window.focus_set()
            except Exception as e:
                print(f"تحذير: فشل في إعداد النافذة: {e}")

            # محاولة إضافة إطار حدود وظل حول النافذة المنسدلة لتحسين المظهر البصري
            try:
                border_frame = ctk.CTkFrame(
                    dropdown_window,               # النافذة التي سيتم إضافة الإطار حولها
                    fg_color='#ffffff',            # لون خلفية الإطار أبيض لتعزيز التباين
                    border_width=2,                # سمك الحد الخارجي للإطار 2 بكسل
                    border_color='#e0e0e0',       # لون الحد الخارجي رمادي فاتح لتعزيز المظهر
                    corner_radius=8               # نصف قطر الزوايا لتكون مستديرة (نعومة الزوايا)
                )
                # تعبئة الإطار ليملأ كامل النافذة المنسدلة مع توسعة ديناميكية وحواف داخلية
                border_frame.pack(fill="both", expand=True, padx=2, pady=2)
            except Exception as e:
                # في حالة حدوث خطأ، طباعة تحذير والاستخدام المباشر للنافذة بدلاً من الإطار
                print(f"تحذير: فشل في إضافة الحدود: {e}")
                border_frame = dropdown_window

            # إنشاء شريط عنوان احترافي في أعلى الإطار الحاوي
            header_frame = ctk.CTkFrame(
                border_frame,                     # الإطار الحاوي الذي يحتوي على شريط العنوان
                height=45,                       # ارتفاع الشريط 45 بكسل
                fg_color='#FF8C00',              # لون البرتقالي الداكن المستخدم في الشريط العلوي (نفس لون الشريط العلوي)
                corner_radius=(6, 6, 0, 0)       # زوايا علوية مستديرة فقط (الزاويتين العلوية اليمنى واليسرى)
            )
            header_frame.pack(fill="x", padx=0, pady=0)    # تعبئة العرض أفقيًا فقط، بدون حواف
            header_frame.pack_propagate(False)              # منع تغيير حجم الحاوية وفقًا لمحتوياتها للحفاظ على الارتفاع ثابتًا

            # إنشاء عنوان القائمة داخل شريط العنوان
            title_label = ctk.CTkLabel(
                header_frame,                      # الإطار الحاوي لشريط العنوان
                text="🏠  القائمة الرئيسية",      # نص العنوان مع رمز منزل للتمثيل المرئي للقائمة الرئيسية
                font=("Cairo", 14, "bold"),       # خط "Cairo" بحجم 14 وبوزن عريض لإظهار النص بشكل واضح وجذاب
                text_color='#ffffff'               # لون نص أبيض يتناسب مع خلفية البرتقالي الداكن
            )
            # وضع العنوان على يمين شريط العنوان مع مسافات داخلية مناسبة من الجانبين
            title_label.pack(side="right", padx=15, pady=12)

            # إنشاء زر إغلاق صغير في شريط العنوان
            close_btn = ctk.CTkButton(
                header_frame,                     # الإطار الحاوي لشريط العنوان
                text="✕",                        # رمز "✕" للإشارة إلى زر الإغلاق
                width=25,                        # عرض ثابت 25 بكسل لتناسب التصميم العام
                height=25,                       # ارتفاع ثابت 25 بكسل
                fg_color="transparent",          # خلفية شفافة لتندمج مع لون شريط العنوان
                hover_color='#FF7F00',           # لون برتقالي أفتح يظهر عند مرور مؤشر الفأرة على الزر
                text_color='#ffffff',            # لون نص أبيض للرمز
                font=("Arial", 12, "bold"),      # خط "Arial" بحجم 12 وبوزن عريض للزر
                command=dropdown_window.destroy  # وظيفة الزر: إغلاق النافذة المنسدلة عند النقر
            )
            # وضع الزر على يسار شريط العنوان مع padding داخلية
            close_btn.pack(side="left", padx=10, pady=10)

            # إنشاء الإطار الأساسي للمحتوى داخل إطار الحدود السفلي
            # هذا الإطار سيحوي أزرار خيارات القائمة المختلفة مع خلفية فاتحة وزوايا مستديرة في الأسفل فقط
            content_frame = ctk.CTkFrame(
                border_frame,                    # الإطار الحاوي لإطار الحدود
                fg_color='#f8f9fa',             # لون خلفية رمادي فاتح لتوفير تباين لطيف مع الشريط العلوي
                corner_radius=(0, 0, 6, 6)      # زوايا مستديرة فقط في أسفل اليسار واليمين لإعطاء مظهر ناعم
            )
            # تعبئة الإطار ليشغل كامل المساحة الفارغة مع التوسعة الأفقية والعمودية بدون padding
            content_frame.pack(fill="both", expand=True, padx=0, pady=0)

            # تعريف قائمة الخيارات المهنية لقائمة التطبيق المنسدلة
            # كل عنصر في القائمة عبارة عن صف Tuple يحوي:
            # - icon: رمز تعبيري (إيموجي) يمثل الخيار بصريًا
            # - title: اسم الخيار (نص عربي) يتم عرضه على الزر
            # - description: وصف موجز (نص عربي) يشرح وظيفة الخيار للمستخدم
            # - command_function: دالة/وظيفة يتم استدعاؤها عند اختيار المستخدم لهذا الخيار
            # - color_hex: رمز اللون السداسي لتصميم الزر والتمييز البصري للخيار
            menu_options = [
                ("🏢", "بيانات الشركة", "إدارة معلومات الشركة والإعدادات", self.show_company_data, "#3498db"),
                ("🎛️", "لوحة التحكم الشاملة", "لوحة التحكم المتطورة مع جميع الإعدادات", self.open_comprehensive_admin_panel, "#FF8C00"),
                ("⚙️", "الخيارات", "إعدادات البرنامج والتخصيصات", self.show_options, "#9b59b6"),
                ("🏪", "الفروع", "إدارة فروع الشركة والمواقع", self.show_branches, "#f39c12"),
                ("📹", "غرفة المراقبة", "مراقبة العمليات والأنشطة", self.show_monitoring_room, "#1abc9c"),
                ("🤖", "تحليل ونمو مبيعاتك بالذكاء الاصطناعي", "تحليل البيانات والذكاء الاصطناعي", self.show_ai_analytics, "#3498db"),
                ("🗄️", "قواعد البيانات", "إدارة قواعد البيانات والنسخ الاحتياطي", self.show_databases, "#27ae60"),
                ("🌐", "الشبكات والشركات", "إدارة الشبكات والاتصالات", self.show_networks, "#e74c3c"),
                ("🔧", "ضبط الملحقات", "إعداد الملحقات والإضافات", self.show_accessories_settings, "#34495e"),
                ("📧", "الرسائل الخارجية", "إدارة الرسائل والاتصالات الخارجية", self.show_external_messages, "#e67e22"),
                ("📊", "تصميم التقارير", "تصميم وإنشاء التقارير المخصصة", self.show_report_design, "#8e44ad"),
                ("💾", "تفريغ قواعد البيانات", "تصدير ونسخ احتياطي لقواعد البيانات", self.show_database_export, "#2c3e50")
            ]
            # Loop through each menu option to create buttons dynamically
            for icon, title, description, command, color in menu_options:
                # Container frame for each button to control size and layout
                btn_container = ctk.CTkFrame(
                    content_frame,
                    height=55,                      # Fixed height to maintain consistent button size
                    fg_color='transparent'          # No background color, lets button background show through
                )
                btn_container.pack(fill="x", pady=2, padx=8)  # Horizontal fill with vertical padding between buttons
                btn_container.pack_propagate(False)            # Prevent container from shrinking to fit child widgets

                # Interactive button widget inside the container
                btn = ctk.CTkButton(
                    btn_container,
                    text="",                       # Empty text, content added separately in custom layout
                    command=lambda cmd=command, win=dropdown_window: self.execute_menu_command(cmd, win),
                                                    # On click, call a method to execute the command with the current dropdown window
                    width=350,                    # Button width
                    height=50,                    # Button height
                    fg_color='#ffffff',           # White background for the button
                    hover_color='#f1f3f4',        # Light gray background on hover to indicate interactivity
                    border_width=1,               # Thin border around button
                    border_color='#e0e0e0',       # Light gray border color
                    corner_radius=6               # Rounded corners for the button
                )
                btn.pack(fill="both", expand=True)             # Fill the container frame fully

                # Inner content frame inside the button to hold icon and text separately
                content_inner = ctk.CTkFrame(btn, fg_color='transparent')
                content_inner.place(relx=0, rely=0, relwidth=1, relheight=1)
                # Positioned absolutely to fill entire button area

                # Icon label placed on the right side representing the menu option visually
                icon_label = ctk.CTkLabel(
                    content_inner,
                    text=icon,                      # Emoji icon for the menu option
                    font=("Segoe UI Emoji", 20),   # Emoji-compatible font with size 20
                    text_color=color,               # Specific color associated with the menu item
                    width=40                       # Width to reserve space for the icon area
                )
                icon_label.pack(side="right", padx=(15, 10), pady=10)  # Padding to the right and inside the button

                # Frame to hold the text elements (title and description) on the left side of the icon
                text_frame = ctk.CTkFrame(content_inner, fg_color='transparent')
                text_frame.pack(side="right", fill="both", expand=True, padx=(0, 10))  # Expand to use available space on the left of icon

                # Label for the menu option main title (e.g. "بيانات الشركة")
                title_label = ctk.CTkLabel(
                    text_frame,
                    text=title,
                    font=("Cairo", 12, "bold"),
                    text_color='#2c3e50',
                    anchor="e"
                )
                title_label.pack(anchor="e", pady=(8, 2))

                # الوصف
                desc_label = ctk.CTkLabel(
                    text_frame,
                    text=description,
                    font=("Cairo", 9),
                    text_color='#6c757d',
                    anchor="e",
                    wraplength=200
                )
                desc_label.pack(anchor="e", pady=(0, 8))



            # تحديد موضع النافذة تحت زر "الرئيسية" مباشرة
            try:
                dropdown_window.update_idletasks()

                # الحصول على موضع النافذة الرئيسية
                main_x = self.main_window.winfo_x()
                main_y = self.main_window.winfo_y()

                # حساب موضع زر "الرئيسية" في الشريط العلوي
                # زر الرئيسية هو الأول من اليمين في الشريط العلوي
                dropdown_x = main_x + self.main_window.winfo_width() - 450  # من اليمين
                dropdown_y = main_y + 65  # تحت الشريط العلوي مباشرة

                # التأكد من أن النافذة لا تخرج من حدود الشاشة
                screen_width = dropdown_window.winfo_screenwidth()
                screen_height = dropdown_window.winfo_screenheight()

                if dropdown_x + 380 > screen_width:
                    dropdown_x = screen_width - 400
                if dropdown_x < 0:
                    dropdown_x = 20

                if dropdown_y + 480 > screen_height:
                    dropdown_y = screen_height - 500
                if dropdown_y < 0:
                    dropdown_y = 20

                dropdown_window.geometry(f"380x480+{dropdown_x}+{dropdown_y}")

            except Exception as e:
                print(f"تحذير: فشل في تحديد موضع النافذة: {e}")
                # موضع افتراضي في وسط الشاشة
                dropdown_window.geometry("380x480+100+100")

            # إضافة تأثير الظهور
            try:
                dropdown_window.attributes('-alpha', 0.95)
            except Exception:
                pass

            # إضافة وظيفة إغلاق النافذة عند النقر خارجها
            def close_on_focus_out(event=None):
                try:
                    if dropdown_window.winfo_exists():
                        if dropdown_window and hasattr(dropdown_window, "destroy"):
                            dropdown_window.destroy()
                except Exception:
                    pass

            # ربط الأحداث لإغلاق النافذة
            try:
                dropdown_window.bind('<FocusOut>', close_on_focus_out)
                self.main_window.bind('<Button-1>', close_on_focus_out)

                # إزالة الربط بعد إغلاق النافذة
                def cleanup():
                    try:
                        self.main_window.unbind('<Button-1>')
                    except Exception:
                        pass

                dropdown_window.protocol("WM_DELETE_WINDOW", cleanup)
            except Exception as e:
                print(f"تحذير: فشل في ربط أحداث الإغلاق: {e}")

        except Exception as e:
            print(f"خطأ في عرض قائمة الرئيسية: {str(e)}")
            # في حالة فشل القائمة المنسدلة، عرض قائمة بسيطة
            try:
                self.show_simple_main_menu()
            except Exception as e2:
                print(f"خطأ في القائمة البسيطة: {e2}")
                messagebox.showinfo("قائمة الرئيسية", "قائمة الرئيسية ستكون متاحة قريباً")

    def execute_menu_command(self, command, window):
        """تنفيذ أمر من القائمة المنسدلة"""
        try:
            if window and hasattr(window, "destroy"):
                window.destroy()  # إغلاق النافذة المنسدلة
            command()  # تنفيذ الأمر
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تنفيذ الأمر: {str(e)}")

    def show_simple_main_menu(self):
        """عرض قائمة رئيسية مبسطة كبديل"""
        try:
            # إنشاء نافذة بسيطة
            simple_window = ctk.CTkToplevel()
            simple_window.title("قائمة الرئيسية")
            simple_window
            simple_window.configure(fg_color='#ffffff')

            # عنوان
            title = ctk.CTkLabel(
                simple_window,
                text="🏠 قائمة الرئيسية",
                font=("Arial", 20, "bold"),
                text_color='#2E8B57'
            )
            title.pack(pady=20)

            # قائمة الخيارات البسيطة
            options = [
                "🏢 بيانات الشركة", "🎛️ لوحة التحكم الشاملة", "⚙️ الخيارات", "🏪 الفروع", "📹 غرفة المراقبة",
                "🤖 تحليل ونمو مبيعاتك بالذكاء الاصطناعي", "🗄️ قواعد البيانات",
                "🌐 الشبكات والشركات", "🔧 ضبط الملحقات", "📧 الرسائل الخارجية",
                "📊 تصميم التقارير", "💾 تفريغ قواعد البيانات"
            ]

            #إطار للأزرار
            frame = ctk.CTkScrollableFrame(simple_window, width=350, height=450)
            frame.pack(pady=10, padx=20, fill="both", expand=True)

            # إنشاء الأزرار
            for option in options:
                btn = ctk.CTkButton(
                    frame,
                    text=option,
                    command=lambda opt=option: self.show_simple_option(opt, simple_window),
                    width=320,
                    height=45,
                    font=("Arial", 12, "bold"),
                    fg_color='#2E8B57',
                    hover_color='#1B5E20',
                    corner_radius=8
                )
                btn.pack(pady=5, padx=10, fill="x")

            # زر إغلاق
            close_btn = ctk.CTkButton(
                simple_window,
                text="❌ إغلاق",
                command=simple_window.destroy,
                width=150,
                height=35,
                font=("Arial", 12, "bold"),
                fg_color='#dc3545',
                corner_radius=8
            )
            close_btn.pack(pady=15)

            # توسيط النافذة
            simple_window.update_idletasks()
            x = (simple_window.winfo_screenwidth() // 2) - (200)
            y = (simple_window.winfo_screenheight() // 2) - (300)
            simple_window.geometry(f"400x600+{x}+{y}")

        except Exception as e:
            messagebox.showinfo("قائمة الرئيسية", "قائمة الرئيسية ستكون متاحة قريباً")

    def show_simple_option(self, option, window):
        """عرض خيار بسيط"""
        try:
            if window and hasattr(window, "destroy"):
                window.destroy()

            # معالجة خاصة للوحة التحكم الشاملة
            if "لوحة التحكم الشاملة" in option:
                self.open_comprehensive_admin_panel()
                return

            option_name = option.split(" ", 1)[1] if " " in option else option
            messagebox.showinfo("تم الاختيار", f"تم اختيار: {option_name}\nهذا الخيار سيكون متاح قريباً")
        except Exception as e:
            messagebox.showinfo("خيار", "الخيار سيكون متاح قريباً")

    def show_warehouses(self):
        """عرض المخازن"""
        try:
            warehouses_window = WarehousesManagementWindow(self.main_window, self.db_manager)
        except ImportError:
            messagebox.showinfo("تطوير", "نافذة المخازن قيد التطوير وستكون متاحة قريباً")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المخازن: {str(e)}")

    def show_clients(self):
        """عرض العملاء"""
        try:
            clients_window = ClientsWindow(self.main_window)
        except ImportError:
            messagebox.showinfo("تطوير", "نافذة العملاء قيد التطوير وستكون متاحة قريباً")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة العملاء: {str(e)}")

    def show_purchases(self) -> None:
        """عرض نافذة إدارة المشتريات"""
        try:
            if PurchasesWindow is not None:
                if self.db_manager is not None:
                    purchases_window = PurchasesWindow(self.main_window, self.db_manager)
                    if ERROR_HANDLING_AVAILABLE:
                        log_info("تم فتح نافذة المشتريات")
                else:
                    messagebox.showerror("خطأ", "قاعدة البيانات غير متاحة")
            else:
                messagebox.showinfo("المشتريات", "نافذة المشتريات غير متاحة حال")
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة المشتريات: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            messagebox.showerror("خطأ", "فشل في فتح نافذة المشتريات")

    def show_sales(self) -> None:
        """عرض نافذة إدارة المبيعات"""
        try:
            if SalesWindow is not None:
                if self.sales_manager is not None:
                    sales_window = SalesWindow(self.main_window, self.sales_manager)
                    if ERROR_HANDLING_AVAILABLE:
                        log_info("تم فتح نافذة المبيعات")
                else:
                    messagebox.showerror("خطأ", "مدير المبيعات غير متاح")
            else:
                messagebox.showinfo("المبيعات", "نافذة المبيعات غير متاحة حال")
        except Exception as e:
            error_msg = f"خطأ في فتح نافذة المبيعات: {e}"
            print(error_msg)
            if ERROR_HANDLING_AVAILABLE:
                log_error(error_msg)
            messagebox.showerror("خطأ", "فشل في فتح نافذة المبيعات")

    def show_employees(self):
        """عرض الموظفين"""
        try:
            hr_window = HRManagementWindow(self.main_window, self.db_manager)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة الموظفين: {str(e)}")

    # دوال قائمة الرئيسية المنسدلة
    def show_company_data(self):
        """عرض بيانات الشركة"""
        try:
            company_window = CompanyDataWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("بيانات الشركة", "نافذة بيانات الشركة ستكون متاحة قريباً")

    def show_options(self):
        """عرض الخيارات"""
        try:
            options_window = OptionsWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("الخيارات", "نافذة الخيارات ستكون متاحة قريباً")

    def show_branches(self):
        """عرض الفروع"""
        try:
            branches_window = BranchesWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("الفروع", "نافذة الفروع ستكون متاحة قريباً")

    def show_monitoring_room(self):
        """عرض غرفة المراقبة"""
        try:
            monitoring_window = MonitoringWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("غرفة المراقبة", "نافذة غرفة المراقبة ستكون متاحة قريباً")

    def show_ai_analytics(self):
        """عرض تحليل المبيعات بالذكاء الاصطناعي"""
        try:
            ai_window = AIAnalyticsWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("الذكاء الاصطناعي", "نافذة تحليل المبيعات بالذكاء الاصطناعي ستكون متاحة قريباً")

    def show_databases(self):
        """عرض قواعد البيانات"""
        try:
            databases_window = DatabasesWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("قواعد البيانات", "نافذة قواعد البيانات ستكون متاحة قريباً")

    def show_networks(self):
        """عرض الشبكات والشركات"""
        try:
            networks_window = NetworksWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("الشبكات والشركات", "نافذة الشبكات والشركات ستكون متاحة قريباً")

    def show_accessories_settings(self):
        """عرض ضبط الملحقات"""
        try:
            accessories_window = AccessoriesWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("ضبط الملحقات", "نافذة ضبط الملحقات ستكون متاحة قريباً")

    def show_external_messages(self):
        """عرض الرسائل الخارجية"""
        try:
            messages_window = MessagesWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("الرسائل الخارجية", "نافذة الرسائل الخارجية ستكون متاحة قريباً")

    def show_report_design(self):
        """عرض تصميم التقارير"""
        try:
            report_window = ReportDesignWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("تصميم التقارير", "نافذة تصميم التقارير ستكون متاحة قريباً")

    def show_database_export(self):
        """عرض تفريغ قواعد البيانات"""
        try:
            export_window = DatabaseExportWindow(self.main_window)
        except Exception as e:
            messagebox.showinfo("تفريغ قواعد البيانات", "نافذة تفريغ قواعد البيانات ستكون متاحة قريباً")

    # وظائف الأيقونات الرئيسية الجديدة
    def open_reports(self):
        """فتح التقارير"""
        try:
            reports_window = ReportsWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة التقارير: {str(e)}")

    def open_advanced_financial_reports(self):
        """فتح التقارير المالية المتقدمة"""
        try:
            advanced_reports = AdvancedFinancialReportsWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة التقارير المالية المتقدمة: {str(e)}")

    def open_invoices(self):
        """فتح وحدة الفواتير المتكاملة"""
        try:
            invoices_window = InvoicesMainWindow(self)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح وحدة الفواتير: {str(e)}")

    def open_treasury(self):
        """فتح الخزينة"""
        try:
            treasury_window = TreasuryWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة الخزينة: {str(e)}")

    def open_accounts(self):
        """فتح الحسابات"""
        try:
            accounts_window = AccountsWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة الحسابات: {str(e)}")

    def open_accounting(self):
        """فتح المحاسبة"""
        try:
            journal_window = JournalEntriesWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المحاسبة: {str(e)}")

    def open_employees(self):
        """فتح الموظفين"""
        try:
            hr_window = HRManagementWindow(self.main_window, self.db_manager)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة الموظفين: {str(e)}")

    def open_sales_analysis(self):
        """فتح تحليل المبيعات"""
        try:
            sales_analysis_window = SalesAnalysisWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح نافذة تحليل المبيعات: {e}")

    def open_account_entry(self):
        """فتح إدخال الحسابات"""
        messagebox.showinfo("إدخال الحسابات", "تم فتح نافذة إدخال الحسابات")

    def open_welcome(self):
        """فتح أهلاً بكم"""
        messagebox.showinfo("أهلاً بكم", "مرحباً بكم في نظام المحاسبة")



    def open_indicators(self):
        """فتح المؤشرات"""
        messagebox.showinfo("المؤشرات", "تم فتح نافذة المؤشرات")

    def open_warehouse(self):
        """فتح إدارة المخازن مباشرة"""
        self.open_warehouses_management()

    def open_expenses(self):
        """فتح الصرف"""
        messagebox.showinfo("الصرف", "تم فتح نافذة الصرف")

    def open_purchases(self):
        """فتح الشراء"""
        try:
            purchases_window = PurchasesWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المشتريات: {str(e)}")

    def open_value(self):
        """فتح القيمة"""
        messagebox.showinfo("القيمة", "تم فتح نافذة القيمة")

    def open_purchase_returns(self):
        """فتح مرتجع الشراء"""
        messagebox.showinfo("مرتجع الشراء", "تم فتح نافذة مرتجع الشراء")

    def open_price_list(self):
        """فتح عرض الأسعار"""
        messagebox.showinfo("عرض الأسعار", "تم فتح نافذة عرض الأسعار")

    def open_sales_returns(self):
        """فتح مرتجع البيع"""
        messagebox.showinfo("مرتجع البيع", "تم فتح نافذة مرتجع البيع")

    # وظائف الأيقونات الرئيسية القديمة
    def old_open_reports(self):
        """فتح التقارير"""
        messagebox.showinfo("التقارير", "تم فتح نافذة التقارير")

    def open_daily_movement(self):
        """فتح الحركة اليومية"""
        messagebox.showinfo("الحركة اليومية", "تم فتح نافذة الحركة اليومية")

    def open_accounts_entry(self):
        """فتح إدخال الحسابات"""
        messagebox.showinfo("إدخال الحسابات", "تم فتح نافذة إدخال الحسابات")



    def open_number_setup(self):
        """فتح إعداد الأرقام"""
        messagebox.showinfo("إعداد الأرقام", "تم فتح نافذة إعداد الأرقام")

    def open_approvals(self):
        """فتح الموافقات"""
        messagebox.showinfo("الموافقات", "تم فتح نافذة الموافقات")

    def open_expense(self):
        """فتح الصرف"""
        messagebox.showinfo("الصرف", "تم فتح نافذة الصرف")

    def open_purchase(self):
        """فتح المشتريات"""
        messagebox.showinfo("المشتريات", "تم فتح نافذة المشتريات")

    def open_sales(self):
        """فتح نافذة المبيعات"""
        try:
            sales_window = SalesWindow(self.main_window, self.sales_manager)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المبيعات: {str(e)}")



    def open_client_list(self):
        """فتح قائمة العملاء"""
        try:
            clients_window = ClientsWindow(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح قائمة العملاء: {str(e)}")



    def open_inventory_adjustment(self):
        """فتح تسوية المخزن"""
        messagebox.showinfo("تسوية المخزن", "تم فتح نافذة تسوية المخزن")

    def open_inventory_transfer(self):
        """فتح تحويل المخزن"""
        messagebox.showinfo("تحويل المخزن", "تم فتح نافذة تحويل المخزن")

    def open_value_management(self):
        """فتح إدارة القيم"""
        messagebox.showinfo("إدارة القيم", "تم فتح نافذة إدارة القيم")

    def open_purchase_return(self):
        """فتح مرتجع الشراء"""
        messagebox.showinfo("مرتجع الشراء", "تم فتح نافذة مرتجع الشراء")

    def open_price_quote(self):
        """فتح عرض الأسعار"""
        messagebox.showinfo("عرض الأسعار", "تم فتح نافذة عرض الأسعار")

    def open_sales_return(self):
        """فتح مرتجع البيع"""
        messagebox.showinfo("مرتجع البيع", "تم فتح نافذة مرتجع البيع")

    # وظائف وسائل التواصل
    def open_facebook(self):
        """فتح صفحة فيسبوك"""
        webbrowser.open("https://facebook.com")

    def open_youtube(self):
        """فتح قناة يوتيوب"""
        webbrowser.open("https://youtube.com")

    def open_website(self):
        """فتح الموقع الإلكتروني"""
        webbrowser.open("https://example.com")

    def open_email(self):
        """فتح البريد الإلكتروني"""
        webbrowser.open("mailto:support@example.com")

    # وظائف النظام
    def toggle_theme(self):
        """تبديل الثيم"""
        try:
            if hasattr(self, 'theme_manager') and self.theme_manager:
                self.theme_manager.toggle_theme()
                # إعادة إنشاء النافذة بالثيم الجديد
                if hasattr(self, 'main_window') and self.main_window:
                    self.main_window.destroy()
                self.create_main_window()
            else:
                # تبديل بسيط بدون theme_manager
                current_mode = ctk.get_appearance_mode()
                new_mode = "dark" if current_mode == "Light" else "light"
                ctk.set_appearance_mode(new_mode)
                messagebox.showinfo("تبديل الثيم", f"تم تبديل الثيم إلى: {new_mode}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تبديل الثيم: {str(e)}")

    def show_settings_menu(self):
        """عرض قائمة الإعدادات"""
        settings_window = ctk.CTkToplevel(self.main_window)
        settings_window.title("⚙️ الإعدادات والتكوين")
        settings_window
        settings_window.configure(fg_color=MODERN_COLORS['background'])

        # جعل النافذة في المقدمة
        settings_window.transient(self.main_window)
        settings_window.grab_set()

        # عنوان النافذة
        title_label = ctk.CTkLabel(
            settings_window,
            text="⚙️ الإعدادات والتكوين",
            font=(FONTS['arabic'], 24, "bold"),
            text_color=MODERN_COLORS['primary']
        )
        title_label.pack(pady=20)

        #إطار الأزرار
        buttons_frame = ctk.CTkFrame(settings_window, fg_color=MODERN_COLORS['surface'])
        buttons_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # أزرار الإعدادات
        settings_buttons = [
            ("⚙️ الإعدادات المتقدمة", "إعدادات شاملة ومتقدمة للنظام", self.open_system_settings, MODERN_COLORS['primary']),
            ("📂 إدارة التصنيفات", "إدارة التصنيفات الهرمية للأصناف", self.open_categories_management, MODERN_COLORS['success']),
            ("📏 إدارة وحدات القياس", "إدارة وحدات القياس المختلفة", self.open_units_management, MODERN_COLORS['info']),
            ("🏪 إدارة المخازن", "إدارة المخازن والفروع", self.open_warehouses_management, MODERN_COLORS['warning']),
            ("📷 قارئ الباركود", "إعداد واختبار قارئ الباركود", self.open_barcode_scanner, MODERN_COLORS['error']),
            ("👥 إدارة المستخدمين", "إدارة حسابات المستخدمين", self.open_user_management, MODERN_COLORS['secondary'])
        ]

        for i, (text, description, command, color) in enumerate(settings_buttons):
            btn_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=20, pady=10)

            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                command=lambda cmd=command, win=settings_window: self.execute_and_close(cmd, win),
                fg_color=color,
                width=200,
                height=50,
                font=(FONTS['arabic'], 14, "bold")
            )
            btn.pack(side="right", padx=10)

            desc_label = ctk.CTkLabel(
                btn_frame,
                text=description,
                font=(FONTS['arabic'], 11),
                text_color=MODERN_COLORS['text_secondary']
            )
            desc_label.pack(side="right", padx=20)



    # وظائف النوافذ المتقدمة الجديدة
    def open_categories_management(self):
        """فتح إدارة التصنيفات"""
        try:
            categories_window = CategoriesManagementWindow(self.main_window, self.db_manager)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح نافذة إدارة التصنيفات: {e}")

    def open_units_management(self):
        """فتح إدارة وحدات القياس"""
        try:
            units_window = UnitsManagementWindow(self.main_window, self.db_manager)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح نافذة إدارة وحدات القياس: {e}")

    def open_warehouses_management(self):
        """فتح إدارة المخازن"""
        try:
            warehouses_window = WarehousesManagementWindow(self.main_window, self.db_manager)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح نافذة إدارة المخازن: {e}")



    def open_barcode_scanner(self):
        """فتح قارئ الباركود"""
        try:
            barcode_scanner = BarcodeScanner()
            barcode_scanner.test_scanner()
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تشغيل قارئ الباركود: {e}")

    def open_system_settings(self):
        """فتح إعدادات النظام المتقدمة"""
        try:
            settings_window = AdvancedSettingsWindow(self)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة الإعدادات: {str(e)}")

    def open_user_management(self):
        """فتح إدارة المستخدمين"""
        try:
            user_mgmt = UserManagement(self.main_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح إدارة المستخدمين: {e}")



    def open_settings(self):
        """فتح لوحة التحكم المركزية الجذابة"""
        try:
            panel = open_central_control_panel(self.main_window)
            if panel:
                print("تم فتح لوحة التحكم المركزية بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح لوحة التحكم:\n{str(e)}")
            print(f"خطأ في فتح لوحة التحكم: {e}")

    def logout(self):
        """تسجيل الخروج"""
        result = messagebox.askyesno("تسجيل الخروج", "هل تريد تسجيل الخروج؟")
        if result:
            if self.auth_manager:
                self.auth_manager.logout()
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.destroy()
            # إعادة تشغيل نافذة تسجيل الدخول
            self.run()

if __name__ == "__main__":
    app = MainApplication()
    app.run()
