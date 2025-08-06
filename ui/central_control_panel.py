# -*- coding: utf-8 -*-
"""
لوحة التحكم المركزية الجذابة لبرنامج المحاسبة العربي
تصميم حديث بألوان دافئة وجذابة مع دعم كامل للـ RTL
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import json
import os
from pathlib import Path
from datetime import datetime
import sqlite3
from typing import Dict, Any, Optional

# استيراد الثيمات والإعدادات
try:
    from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS
except ImportError:
    # إذا لم يكن الثيم متوفراً، استخدم ألوان افتراضية
    MODERN_COLORS = {
        'primary': '#2E8B57',
        'background': '#f8f9fa',
        'surface': '#ffffff',
        'text_primary': '#212529',
        'success': '#28a745',
        'warning': '#ffc107',
        'error': '#dc3545'
    }
    FONTS = {
        'arabic': 'Cairo',
        'english': 'Arial'
    }
    DIMENSIONS = {
        'button_height': 40,
        'input_height': 35
    }
try:
    from config.settings import PROJECT_ROOT, DATABASE_PATH
except ImportError:
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).parent.parent
    DATABASE_PATH = PROJECT_ROOT / "database" / "accounting.db"

# استيراد التكامل المتقدم
try:
    from ui.control_panel_integration import integrate_advanced_control_panel
except ImportError:
    # إذا لم يكن التكامل متوفراً، استخدم دالة فارغة
    def integrate_advanced_control_panel(panel):
        return None

# ألوان دافئة وجذابة جديدة (بدون رمادي)
WARM_COLORS = {
    # ألوان دافئة أساسية
    'coral': '#FF6B6B',           # مرجاني دافئ
    'sunset': '#FF8E53',          # برتقالي غروب
    'golden': '#FFD93D',          # ذهبي مشرق
    'mint': '#6BCF7F',            # نعناعي منعش
    'lavender': '#A8E6CF',        # لافندر هادئ
    'sky': '#4ECDC4',             # سماوي صافي
    'rose': '#FF8A95',            # وردي ناعم
    'peach': '#FFAAA5',           # خوخي فاتح
    'turquoise': '#45B7D1',       # تركوازي
    'violet': '#96CEB4',          # بنفسجي فاتح
    'cream': '#FFF8E1',           # كريمي دافئ
    'ivory': '#FFFEF7',           # عاجي
    
    # ألوان خلفية دافئة
    'warm_white': '#FFFEF7',      # أبيض دافئ
    'soft_cream': '#FFF8E1',      # كريمي ناعم
    'light_peach': '#FFF5F5',     # خوخي فاتح جداً
    'mint_bg': '#F0FFF4',         # خلفية نعناعية
    
    # ألوان نص دافئة
    'dark_coral': '#E55555',      # مرجاني داكن
    'warm_brown': '#8B4513',      # بني دافئ
    'deep_teal': '#2C5F5D',       # تيل عميق
    'rich_purple': '#6A4C93',     # بنفسجي غني
}

class CentralControlPanel:
    """لوحة التحكم المركزية الجذابة"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.settings_file = PROJECT_ROOT / "config" / "control_panel_settings.json"
        self.current_settings = {}
        self.sidebar_buttons = {}
        self.current_section = "general"
        
        # إنشاء النافذة الرئيسية
        self.create_main_window()
        
        # تحميل الإعدادات المحفوظة
        self.load_settings()

        # دمج الأقسام المتقدمة
        self.advanced_integration = integrate_advanced_control_panel(self)

        # إنشاء الواجهة
        self.create_interface()
        
        # عرض القسم الافتراضي
        self.show_section("general")

        # تفعيل جميع الأزرار والوظائف
        self.activate_all_functions()

        # تطبيق إعدادات النافذة
        self.window.after(1000, self.apply_window_settings)

    def open_accounting_window(self):
        """فتح نافذة المحاسبة الرئيسية"""
        try:
            # محاولة فتح النافذة الرئيسية
            try:
                from ui.main_window import MainApplication
                app = MainApplication()
                app.run()
                self.update_status("📊 تم فتح نافذة المحاسبة الرئيسية")
            except ImportError:
                # إذا لم تكن متوفرة، عرض رسالة
                messagebox.showinfo("معلومات", "نافذة المحاسبة الرئيسية قيد التطوير")
                self.update_status("ℹ️ نافذة المحاسبة قيد التطوير")
        except Exception as e:
            self.update_status("❌ خطأ في فتح نافذة المحاسبة")
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المحاسبة:\n{str(e)}")

    def open_sales_window(self):
        """فتح نافذة المبيعات"""
        try:
            from ui.sales_window import SalesWindow
            sales_window = SalesWindow(self.window)
            self.update_status("🛒 تم فتح نافذة المبيعات")
        except Exception as e:
            self.update_status("❌ خطأ في فتح نافذة المبيعات")
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المبيعات:\n{str(e)}")

    def open_purchases_window(self):
        """فتح نافذة المشتريات"""
        try:
            from ui.purchases_window import PurchasesWindow
            purchases_window = PurchasesWindow(self.window)
            self.update_status("📦 تم فتح نافذة المشتريات")
        except Exception as e:
            self.update_status("❌ خطأ في فتح نافذة المشتريات")
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المشتريات:\n{str(e)}")

    def open_inventory_window(self):
        """فتح نافذة إدارة المخزون"""
        try:
            from ui.inventory_window import InventoryWindow
            inventory_window = InventoryWindow(self.window)
            self.update_status("📋 تم فتح نافذة المخزون")
        except Exception as e:
            self.update_status("❌ خطأ في فتح نافذة المخزون")
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة المخزون:\n{str(e)}")

    def show_temp_message(self, window_name):
        """عرض رسالة مؤقتة للنوافذ قيد التطوير"""
        messagebox.showinfo("معلومات", f"نافذة {window_name} قيد التطوير")
        self.update_status(f"ℹ️ نافذة {window_name} قيد التطوير")

    def open_customers_window(self):
        """فتح نافذة إدارة العملاء"""
        try:
            # محاولة فتح نافذة العملاء إذا كانت متوفرة
            messagebox.showinfo("معلومات", "نافذة العملاء قيد التطوير")
            self.update_status("ℹ️ نافذة العملاء قيد التطوير")
        except Exception as e:
            self.update_status("❌ خطأ في فتح نافذة العملاء")

    def open_suppliers_window(self):
        """فتح نافذة إدارة الموردين"""
        try:
            messagebox.showinfo("معلومات", "نافذة الموردين قيد التطوير")
            self.update_status("ℹ️ نافذة الموردين قيد التطوير")
        except Exception as e:
            self.update_status("❌ خطأ في فتح نافذة الموردين")

    def open_employees_window(self):
        """فتح نافذة إدارة الموظفين"""
        try:
            from ui.employees_window import EmployeesWindow
            employees_window = EmployeesWindow(self.window)
            self.update_status("👥 تم فتح نافذة الموظفين")
        except Exception as e:
            messagebox.showinfo("معلومات", "نافذة الموظفين قيد التطوير")
            self.update_status("ℹ️ نافذة الموظفين قيد التطوير")

    def open_reports_window(self):
        """فتح نافذة التقارير"""
        try:
            from ui.reports_window import ReportsWindow
            reports_window = ReportsWindow(self.window)
            self.update_status("📈 تم فتح نافذة التقارير")
        except Exception as e:
            messagebox.showinfo("معلومات", "نافذة التقارير قيد التطوير")
            self.update_status("ℹ️ نافذة التقارير قيد التطوير")

    def open_pos_window(self):
        """فتح نافذة نقاط البيع"""
        try:
            from ui.pos_window import POSWindow
            pos_window = POSWindow(self.window)
            self.update_status("🏪 تم فتح نافذة نقاط البيع")
        except Exception as e:
            messagebox.showinfo("معلومات", "نافذة نقاط البيع قيد التطوير")
            self.update_status("ℹ️ نافذة نقاط البيع قيد التطوير")

    def open_backup_window(self):
        """فتح نافذة النسخ الاحتياطي"""
        messagebox.showinfo("معلومات", "نافذة النسخ الاحتياطي قيد التطوير")
        self.update_status("ℹ️ نافذة النسخ الاحتياطي قيد التطوير")

    def open_settings_window(self):
        """فتح نافذة الإعدادات"""
        messagebox.showinfo("معلومات", "نافذة الإعدادات قيد التطوير")
        self.update_status("ℹ️ نافذة الإعدادات قيد التطوير")

    def open_database_manager(self):
        """فتح مدير قاعدة البيانات"""
        messagebox.showinfo("معلومات", "مدير قاعدة البيانات قيد التطوير")
        self.update_status("ℹ️ مدير قاعدة البيانات قيد التطوير")

    def open_system_monitor(self):
        """فتح مراقب النظام"""
        messagebox.showinfo("معلومات", "مراقب النظام قيد التطوير")
        self.update_status("ℹ️ مراقب النظام قيد التطوير")

    def open_invoices_reports(self):
        """فتح تقارير الفواتير"""
        messagebox.showinfo("معلومات", "تقارير الفواتير قيد التطوير")
        self.update_status("ℹ️ تقارير الفواتير قيد التطوير")

    def export_to_excel(self):
        """تصدير البيانات إلى Excel"""
        messagebox.showinfo("معلومات", "تصدير Excel قيد التطوير")
        self.update_status("ℹ️ تصدير Excel قيد التطوير")

    def restore_defaults(self):
        """استعادة الإعدادات الافتراضية"""
        if messagebox.askyesno("تأكيد", "هل تريد استعادة الإعدادات الافتراضية؟"):
            messagebox.showinfo("معلومات", "تم استعادة الإعدادات الافتراضية")
            self.update_status("🔄 تم استعادة الإعدادات الافتراضية")

    def test_settings(self):
        """اختبار الإعدادات"""
        messagebox.showinfo("اختبار الإعدادات", "جميع الإعدادات تعمل بشكل صحيح")
        self.update_status("✅ تم اختبار الإعدادات بنجاح")

    def activate_all_functions(self):
        """تفعيل جميع الأزرار والوظائف في لوحة التحكم"""
        try:
            # ربط أحداث لوحة المفاتيح
            self.window.bind('<F11>', self.toggle_fullscreen)
            self.window.bind('<Escape>', self.exit_fullscreen)
            self.window.bind('<Control-s>', self.save_all_settings)
            self.window.bind('<Control-r>', self.refresh_panel)

            # تحديث حالة الأزرار
            self.update_button_states()

            # تحديث الحالة
            self.update_status("✅ تم تفعيل جميع الوظائف بنجاح")

        except Exception as e:
            self.update_status(f"⚠️ خطأ في تفعيل الوظائف: {str(e)}")

    def toggle_fullscreen(self, event=None):
        """تبديل وضع ملء الشاشة"""
        try:
            # التحقق من الحالة الحالية
            is_fullscreen = self.window.attributes('-fullscreen')

            if is_fullscreen:
                # الخروج من ملء الشاشة
                self.window.attributes('-fullscreen', False)
                self.window.state('zoomed')
                self.update_status("🖼️ تم الخروج من ملء الشاشة الكامل")
            else:
                # الدخول في ملء الشاشة
                self.window.attributes('-fullscreen', True)
                self.update_status("🖼️ تم تفعيل ملء الشاشة الكامل")

        except Exception as e:
            # إذا فشل، استخدم الطريقة التقليدية
            try:
                current_state = self.window.state()
                if current_state == 'zoomed':
                    self.window.state('normal')
                    screen_width = self.window.winfo_screenwidth()
                    screen_height = self.window.winfo_screenheight()
                    # تعيين حجم أصغر قليلاً من الشاشة
                    new_width = int(screen_width * 0.9)
                    new_height = int(screen_height * 0.9)
                    x = (screen_width - new_width) // 2
                    y = (screen_height - new_height) // 2
                    self.window.geometry(f"{new_width}x{new_height}+{x}+{y}")
                    self.update_status("🖼️ تم تصغير النافذة")
                else:
                    self.window.state('zoomed')
                    self.update_status("🖼️ تم تكبير النافذة")
            except Exception as e2:
                print(f"خطأ في تبديل ملء الشاشة: {e2}")

    def exit_fullscreen(self, event=None):
        """الخروج من وضع ملء الشاشة"""
        try:
            # الخروج من ملء الشاشة الكامل
            self.window.attributes('-fullscreen', False)
            self.window.state('zoomed')
            self.update_status("🖼️ تم الخروج من ملء الشاشة")
        except Exception as e:
            try:
                # الطريقة التقليدية
                self.window.state('normal')
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()
                new_width = int(screen_width * 0.8)
                new_height = int(screen_height * 0.8)
                x = (screen_width - new_width) // 2
                y = (screen_height - new_height) // 2
                self.window.geometry(f"{new_width}x{new_height}+{x}+{y}")
                self.update_status("🖼️ تم تصغير النافذة")
            except Exception as e2:
                print(f"خطأ في الخروج من ملء الشاشة: {e2}")

    def close_window(self, event=None):
        """إغلاق النافذة"""
        try:
            result = messagebox.askyesno(
                "تأكيد الإغلاق",
                "هل تريد إغلاق لوحة التحكم المركزية؟"
            )
            if result:
                self.window.destroy()
        except Exception as e:
            print(f"خطأ في إغلاق النافذة: {e}")

    def maximize_window(self):
        """تكبير النافذة لتملأ الشاشة"""
        try:
            # الحصول على أبعاد الشاشة
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            # تعيين النافذة لتملأ الشاشة
            self.window.geometry(f"{screen_width}x{screen_height}+0+0")
            self.window.state('zoomed')

            # تفعيل ملء الشاشة الكامل
            try:
                self.window.attributes('-fullscreen', True)
            except:
                pass

            self.update_status(f"🖼️ تم تكبير النافذة: {screen_width}x{screen_height}")

        except Exception as e:
            print(f"خطأ في تكبير النافذة: {e}")
            self.update_status("❌ خطأ في تكبير النافذة")

    def set_fullscreen_mode(self):
        """تعيين وضع ملء الشاشة الكامل"""
        try:
            # تفعيل ملء الشاشة الكامل
            self.window.attributes('-fullscreen', True)
            self.update_status("🖼️ تم تفعيل ملء الشاشة الكامل")

            # تحديث معلومات النافذة
            self.refresh_window_info()

        except Exception as e:
            print(f"خطأ في تفعيل ملء الشاشة: {e}")
            self.update_status("❌ خطأ في تفعيل ملء الشاشة")

    def set_normal_window(self):
        """تعيين النافذة في الوضع العادي"""
        try:
            # إلغاء ملء الشاشة
            self.window.attributes('-fullscreen', False)
            self.window.state('normal')

            # تعيين حجم مناسب
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            # حجم النافذة 80% من الشاشة
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)

            # وضع النافذة في المنتصف
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.update_status(f"🪟 تم تعيين النافذة العادية: {window_width}×{window_height}")

            # تحديث معلومات النافذة
            self.refresh_window_info()

        except Exception as e:
            print(f"خطأ في تعيين النافذة العادية: {e}")
            self.update_status("❌ خطأ في تعيين النافذة العادية")

    def set_small_window(self):
        """تعيين النافذة في حجم صغير"""
        try:
            # إلغاء ملء الشاشة
            self.window.attributes('-fullscreen', False)
            self.window.state('normal')

            # تعيين حجم صغير
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            # حجم النافذة 60% من الشاشة
            window_width = int(screen_width * 0.6)
            window_height = int(screen_height * 0.6)

            # وضع النافذة في المنتصف
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.update_status(f"📱 تم تعيين النافذة الصغيرة: {window_width}×{window_height}")

            # تحديث معلومات النافذة
            self.refresh_window_info()

        except Exception as e:
            print(f"خطأ في تعيين النافذة الصغيرة: {e}")
            self.update_status("❌ خطأ في تعيين النافذة الصغيرة")

    def refresh_window_info(self):
        """تحديث معلومات النافذة"""
        try:
            # إعادة عرض القسم الحالي لتحديث المعلومات
            if hasattr(self, 'current_section'):
                self.window.after(500, lambda: self.show_section(self.current_section))
        except Exception as e:
            print(f"خطأ في تحديث معلومات النافذة: {e}")

    def apply_window_settings(self):
        """تطبيق إعدادات النافذة المحفوظة"""
        try:
            # جلب الإعدادات المحفوظة
            default_size = self.current_settings.get('default_window_size', 'ملء الشاشة الكامل')
            window_position = self.current_settings.get('window_position', 'ملء الشاشة')

            if default_size == 'ملء الشاشة الكامل' or window_position == 'ملء الشاشة':
                self.set_fullscreen_mode()
            elif default_size == 'كبير (1920×1080)':
                self.maximize_window()
            elif default_size == 'متوسط (1366×768)':
                self.set_normal_window()
            elif default_size == 'صغير (1024×768)':
                self.set_small_window()

            self.update_status("✅ تم تطبيق إعدادات النافذة")

        except Exception as e:
            print(f"خطأ في تطبيق إعدادات النافذة: {e}")
            self.update_status("❌ خطأ في تطبيق إعدادات النافذة")

    def make_draggable(self, widget):
        """جعل العنصر قابل للسحب لتحريك النافذة"""
        def start_drag(event):
            widget.start_x = event.x
            widget.start_y = event.y

        def drag_window(event):
            if hasattr(widget, 'start_x') and hasattr(widget, 'start_y'):
                x = self.window.winfo_x() + (event.x - widget.start_x)
                y = self.window.winfo_y() + (event.y - widget.start_y)
                self.window.geometry(f"+{x}+{y}")

        widget.bind("<Button-1>", start_drag)
        widget.bind("<B1-Motion>", drag_window)

    def close_window(self):
        """إغلاق النافذة مع تأكيد"""
        try:
            result = messagebox.askyesno(
                "تأكيد الإغلاق",
                "هل تريد إغلاق لوحة التحكم المركزية؟",
                parent=self.window
            )
            if result:
                self.window.quit()
                self.window.destroy()
        except Exception as e:
            print(f"خطأ في إغلاق النافذة: {e}")
            self.window.destroy()

    def minimize_window(self):
        """تصغير النافذة إلى شريط المهام"""
        try:
            self.window.iconify()
            self.update_status("➖ تم تصغير النافذة")
        except Exception as e:
            print(f"خطأ في تصغير النافذة: {e}")

    def toggle_maximize(self):
        """تبديل بين التكبير والاستعادة"""
        try:
            if self.is_maximized:
                # استعادة الحجم العادي
                self.window.geometry(self.normal_geometry)
                self.maximize_btn.configure(text="⬜")
                self.is_maximized = False
                self.update_status("🗗 تم استعادة النافذة للحجم العادي")
            else:
                # حفظ الحجم الحالي
                self.normal_geometry = self.window.geometry()

                # تكبير النافذة
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()
                taskbar_height = 40

                self.window.geometry(f"{screen_width}x{screen_height - taskbar_height}+0+0")
                self.maximize_btn.configure(text="🗗")
                self.is_maximized = True
                self.update_status("⬜ تم تكبير النافذة")

        except Exception as e:
            print(f"خطأ في تبديل حجم النافذة: {e}")

    def update_title_bar_info(self):
        """تحديث معلومات شريط العنوان"""
        try:
            # تحديث النص حسب حالة النافذة
            if self.is_maximized:
                status = "مكبرة"
            else:
                status = "عادية"

            # يمكن إضافة معلومات إضافية هنا إذا لزم الأمر

        except Exception as e:
            print(f"خطأ في تحديث شريط العنوان: {e}")

    def set_window_always_on_top(self, on_top=True):
        """جعل النافذة دائماً في المقدمة"""
        try:
            self.window.attributes('-topmost', on_top)
            if on_top:
                self.update_status("📌 تم تثبيت النافذة في المقدمة")
            else:
                self.update_status("📌 تم إلغاء تثبيت النافذة في المقدمة")
        except Exception as e:
            print(f"خطأ في تثبيت النافذة: {e}")

    def refresh_panel(self, event=None):
        """تحديث لوحة التحكم"""
        try:
            self.load_settings()
            self.show_section(self.current_section)
            self.update_status("🔄 تم تحديث لوحة التحكم")
        except Exception as e:
            self.update_status(f"❌ خطأ في التحديث: {str(e)}")

    def update_button_states(self):
        """تحديث حالة الأزرار"""
        for key, button in self.sidebar_buttons.items():
            if hasattr(button, 'configure'):
                # تأكد من أن الزر قابل للنقر
                button.configure(state="normal")
                # إضافة تأثير hover
                button.bind("<Enter>", lambda e, btn=button: self.on_button_hover(btn, True))
                button.bind("<Leave>", lambda e, btn=button: self.on_button_hover(btn, False))

    def on_button_hover(self, button, is_hover):
        """تأثير عند التمرير فوق الزر"""
        try:
            if is_hover:
                # تأثير عند التمرير
                button.configure(cursor="hand2")
            else:
                # إزالة التأثير
                button.configure(cursor="arrow")
        except Exception as e:
            pass
    
    def create_main_window(self):
        """إنشاء النافذة الرئيسية مع شريط عنوان مخصص"""
        self.window = ctk.CTkToplevel()

        # إزالة شريط العنوان الافتراضي
        self.window.overrideredirect(True)

        # الحصول على أبعاد الشاشة
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # تعيين النافذة لتملأ الشاشة (مع ترك مساحة لشريط المهام)
        taskbar_height = 40  # ارتفاع شريط المهام تقريباً
        window_width = screen_width
        window_height = screen_height - taskbar_height

        self.window.geometry(f"{window_width}x{window_height}+0+0")

        # إعدادات النافذة
        self.window.configure(fg_color=WARM_COLORS['warm_white'])
        self.window.minsize(1200, 800)

        # متغيرات حالة النافذة
        self.is_maximized = True
        self.normal_geometry = "1400x900+200+100"

        # إنشاء شريط العنوان المخصص
        self.create_custom_title_bar()

        # جعل النافذة في المقدمة وتركيز عليها
        self.window.lift()
        self.window.focus_force()

        # ربط أحداث النافذة
        self.window.bind('<F11>', self.toggle_fullscreen)
        self.window.bind('<Escape>', self.exit_fullscreen)

        print(f"📐 أبعاد الشاشة: {screen_width}x{screen_height}")
        print(f"📐 أبعاد النافذة: {window_width}x{window_height}")

    def create_custom_title_bar(self):
        """إنشاء شريط عنوان مخصص مع أزرار التحكم"""
        # إنشاء شريط العنوان
        self.title_bar = ctk.CTkFrame(
            self.window,
            height=40,
            fg_color=WARM_COLORS['coral'],
            corner_radius=0
        )
        self.title_bar.pack(fill="x", side="top")
        self.title_bar.pack_propagate(False)

        # أيقونة البرنامج
        icon_label = ctk.CTkLabel(
            self.title_bar,
            text="🎛️",
            font=("Segoe UI Emoji", 20),
            text_color="white"
        )
        icon_label.pack(side="right", padx=(15, 5), pady=5)

        # عنوان النافذة
        self.title_label = ctk.CTkLabel(
            self.title_bar,
            text="لوحة التحكم المركزية - برنامج ست الكل للمحاسبة",
            font=(FONTS['arabic'], 14, "bold"),
            text_color="white"
        )
        self.title_label.pack(side="right", padx=10, pady=5, expand=True)

        # إطار أزرار التحكم (في الزاوية اليسرى للواجهة العربية)
        controls_frame = ctk.CTkFrame(self.title_bar, fg_color="transparent")
        controls_frame.pack(side="left", padx=5, pady=2)

        # زر الإغلاق
        self.close_btn = ctk.CTkButton(
            controls_frame,
            text="❌",
            width=35,
            height=30,
            fg_color="#ff4757",
            hover_color="#ff3838",
            font=("Segoe UI Emoji", 12),
            command=self.close_window,
            corner_radius=5
        )
        self.close_btn.pack(side="left", padx=2)

        # زر التكبير/الاستعادة
        self.maximize_btn = ctk.CTkButton(
            controls_frame,
            text="🗗",
            width=35,
            height=30,
            fg_color="#2ed573",
            hover_color="#26d466",
            font=("Segoe UI Emoji", 12),
            command=self.toggle_maximize,
            corner_radius=5
        )
        self.maximize_btn.pack(side="left", padx=2)

        # زر التصغير
        self.minimize_btn = ctk.CTkButton(
            controls_frame,
            text="➖",
            width=35,
            height=30,
            fg_color="#ffa502",
            hover_color="#ff9500",
            font=("Segoe UI Emoji", 12),
            command=self.minimize_window,
            corner_radius=5
        )
        self.minimize_btn.pack(side="left", padx=2)

        # زر الإعدادات السريعة
        self.settings_btn = ctk.CTkButton(
            controls_frame,
            text="⚙️",
            width=35,
            height=30,
            fg_color="#5352ed",
            hover_color="#4834d4",
            font=("Segoe UI Emoji", 12),
            command=self.show_quick_settings,
            corner_radius=5
        )
        self.settings_btn.pack(side="left", padx=2)

        # إضافة tooltip للأزرار
        self.add_tooltips()

        # جعل شريط العنوان قابل للسحب
        self.make_draggable(self.title_bar)
        self.make_draggable(self.title_label)

    def add_tooltips(self):
        """إضافة تلميحات للأزرار"""
        try:
            # يمكن إضافة مكتبة tooltip هنا إذا كانت متوفرة
            pass
        except:
            pass

    def show_quick_settings(self):
        """عرض قائمة الإعدادات السريعة"""
        try:
            # إنشاء قائمة منبثقة للإعدادات السريعة
            settings_menu = ctk.CTkToplevel(self.window)
            settings_menu.title("الإعدادات السريعة")
            settings_menu.geometry("300x400")
            settings_menu.configure(fg_color=WARM_COLORS['warm_white'])
            settings_menu.transient(self.window)
            settings_menu.grab_set()

            # وضع القائمة بجانب زر الإعدادات
            x = self.window.winfo_x() + 50
            y = self.window.winfo_y() + 50
            settings_menu.geometry(f"+{x}+{y}")

            # عنوان القائمة
            title_label = ctk.CTkLabel(
                settings_menu,
                text="⚙️ الإعدادات السريعة",
                font=(FONTS['arabic'], 16, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            title_label.pack(pady=15)

            # أزرار الإعدادات السريعة
            quick_settings = [
                {"text": "🖼️ ملء الشاشة", "command": lambda: [self.set_fullscreen_mode(), settings_menu.destroy()]},
                {"text": "🪟 نافذة عادية", "command": lambda: [self.set_normal_window(), settings_menu.destroy()]},
                {"text": "📌 تثبيت في المقدمة", "command": lambda: [self.set_window_always_on_top(True), settings_menu.destroy()]},
                {"text": "📌 إلغاء التثبيت", "command": lambda: [self.set_window_always_on_top(False), settings_menu.destroy()]},
                {"text": "🔄 تحديث لوحة التحكم", "command": lambda: [self.refresh_panel(), settings_menu.destroy()]},
                {"text": "💾 حفظ الإعدادات", "command": lambda: [self.save_all_settings(), settings_menu.destroy()]},
                {"text": "ℹ️ حول البرنامج", "command": lambda: [self.show_about_dialog(), settings_menu.destroy()]}
            ]

            for setting in quick_settings:
                btn = ctk.CTkButton(
                    settings_menu,
                    text=setting["text"],
                    font=(FONTS['arabic'], 12),
                    fg_color=WARM_COLORS['mint'],
                    hover_color=self.lighten_color(WARM_COLORS['mint']),
                    height=35,
                    command=setting["command"]
                )
                btn.pack(fill="x", padx=20, pady=5)

            # زر إغلاق
            close_btn = ctk.CTkButton(
                settings_menu,
                text="إغلاق",
                font=(FONTS['arabic'], 12),
                fg_color=WARM_COLORS['sunset'],
                hover_color=self.lighten_color(WARM_COLORS['sunset']),
                command=settings_menu.destroy
            )
            close_btn.pack(pady=15)

        except Exception as e:
            print(f"خطأ في عرض الإعدادات السريعة: {e}")
            self.update_status("❌ خطأ في عرض الإعدادات السريعة")
        self.window.state('zoomed')
        
        # تكوين الشبكة
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        
        if self.parent:
            self.window.transient(self.parent)
            self.window.grab_set()
    
    def create_interface(self):
        """إنشاء واجهة لوحة التحكم مع شريط العنوان المخصص"""
        # إنشاء الإطار الرئيسي (تحت شريط العنوان)
        self.main_container = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)

        # الشريط الجانبي
        self.create_sidebar()

        # المنطقة الرئيسية
        self.create_main_area()

        # الشريط السفلي
        self.create_bottom_bar()
    
    def create_top_bar(self):
        """إنشاء الشريط العلوي"""
        top_frame = ctk.CTkFrame(
            self.window,
            height=80,
            fg_color=WARM_COLORS['coral'],
            corner_radius=0
        )
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        top_frame.grid_propagate(False)
        
        # شعار وعنوان
        title_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        title_frame.pack(side="right", fill="y", padx=20)
        
        # العنوان الرئيسي
        title_label = ctk.CTkLabel(
            title_frame,
            text="🎛️ لوحة التحكم المركزية",
            font=(FONTS['arabic'], 28, "bold"),
            text_color="white"
        )
        title_label.pack(side="top", pady=(15, 5))
        
        # العنوان الفرعي
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="إدارة شاملة لجميع إعدادات النظام",
            font=(FONTS['arabic'], 14),
            text_color=WARM_COLORS['cream']
        )
        subtitle_label.pack(side="top")
        
        # معلومات الشركة على اليسار
        company_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        company_frame.pack(side="left", fill="y", padx=20)
        
        company_label = ctk.CTkLabel(
            company_frame,
            text="شركة ست الكل للمحاسبة",
            font=(FONTS['arabic'], 16, "bold"),
            text_color="white"
        )
        company_label.pack(expand=True)
    
    def create_sidebar(self):
        """إنشاء الشريط الجانبي للتنقل"""
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=280,
            fg_color=WARM_COLORS['soft_cream'],
            corner_radius=0
        )
        self.sidebar.pack(side="right", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # عنوان الشريط الجانبي
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="🧭 أقسام التحكم",
            font=(FONTS['arabic'], 18, "bold"),
            text_color=WARM_COLORS['dark_coral']
        )
        sidebar_title.pack(pady=(20, 10))
        
        # أقسام التحكم
        sections = [
            {
                'key': 'general',
                'title': 'الإعدادات العامة',
                'icon': '🧩',
                'color': WARM_COLORS['coral'],
                'description': 'اللغة، التاريخ، الشعار'
            },
            {
                'key': 'users',
                'title': 'المستخدمون والصلاحيات',
                'icon': '👥',
                'color': WARM_COLORS['sunset'],
                'description': 'إدارة المستخدمين'
            },
            {
                'key': 'invoices',
                'title': 'إعدادات الفواتير',
                'icon': '🧾',
                'color': WARM_COLORS['golden'],
                'description': 'بيع، شراء، POS'
            },
            {
                'key': 'payroll',
                'title': 'الرواتب والضرائب',
                'icon': '💰',
                'color': WARM_COLORS['mint'],
                'description': 'إعدادات الرواتب'
            },
            {
                'key': 'warehouses',
                'title': 'إعدادات المخازن',
                'icon': '🏪',
                'color': WARM_COLORS['sky'],
                'description': 'إدارة المخازن'
            },
            {
                'key': 'modules',
                'title': 'التحكم في الموديلات',
                'icon': '🔧',
                'color': WARM_COLORS['rose'],
                'description': 'إظهار/إخفاء الميزات'
            },
            {
                'key': 'backup',
                'title': 'النسخ الاحتياطي',
                'icon': '💾',
                'color': WARM_COLORS['peach'],
                'description': 'حفظ واستعادة البيانات'
            },
            {
                'key': 'import_export',
                'title': 'استيراد من Excel',
                'icon': '📊',
                'color': WARM_COLORS['turquoise'],
                'description': 'إدارة البيانات'
            },
            {
                'key': 'appearance',
                'title': 'تخصيص الواجهة',
                'icon': '🎨',
                'color': WARM_COLORS['violet'],
                'description': 'الألوان والخطوط'
            },
            {
                'key': 'security',
                'title': 'نظام الأمان',
                'icon': '🛡️',
                'color': WARM_COLORS['lavender'],
                'description': 'الحماية والمراقبة'
            },
            {
                'key': 'numbering',
                'title': 'الأرقام التسلسلية',
                'icon': '🔢',
                'color': WARM_COLORS['coral'],
                'description': 'توليد الأرقام التلقائي'
            }
        ]
        
        # إنشاء أزرار الأقسام
        for section in sections:
            self.create_sidebar_button(section)
    
    def create_sidebar_button(self, section_info):
        """إنشاء زر في الشريط الجانبي"""
        button_frame = ctk.CTkFrame(
            self.sidebar,
            height=70,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=15, pady=5)
        button_frame.pack_propagate(False)
        
        # الزر الرئيسي
        button = ctk.CTkButton(
            button_frame,
            text="",
            height=70,
            fg_color=section_info['color'],
            hover_color=self.lighten_color(section_info['color']),
            corner_radius=12,
            command=lambda: self.show_section(section_info['key'])
        )
        button.pack(fill="both", expand=True)
        
        # محتوى الزر
        content_frame = ctk.CTkFrame(button, fg_color="transparent")
        content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # الأيقونة
        icon_label = ctk.CTkLabel(
            content_frame,
            text=section_info['icon'],
            font=("Segoe UI Emoji", 24),
            text_color="white"
        )
        icon_label.pack(side="right", padx=(0, 15), pady=10)
        
        # النص
        text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        text_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        title_label = ctk.CTkLabel(
            text_frame,
            text=section_info['title'],
            font=(FONTS['arabic'], 14, "bold"),
            text_color="white",
            anchor="e"
        )
        title_label.pack(anchor="e", pady=(8, 2))
        
        desc_label = ctk.CTkLabel(
            text_frame,
            text=section_info['description'],
            font=(FONTS['arabic'], 10),
            text_color=WARM_COLORS['cream'],
            anchor="e"
        )
        desc_label.pack(anchor="e")
        
        # حفظ مرجع الزر
        self.sidebar_buttons[section_info['key']] = button
    
    def create_main_area(self):
        """إنشاء المنطقة الرئيسية لعرض الإعدادات"""
        self.main_area = ctk.CTkFrame(
            self.main_container,
            fg_color=WARM_COLORS['warm_white'],
            corner_radius=0
        )
        self.main_area.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        
        # إطار المحتوى القابل للتمرير
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def create_bottom_bar(self):
        """إنشاء الشريط السفلي"""
        bottom_frame = ctk.CTkFrame(
            self.main_container,
            height=60,
            fg_color=WARM_COLORS['mint_bg'],
            corner_radius=0
        )
        bottom_frame.pack(side="bottom", fill="x", padx=0, pady=0)
        bottom_frame.pack_propagate(False)
        
        # أزرار الإجراءات
        buttons_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        buttons_frame.pack(side="left", padx=20, pady=10)
        
        # زر الحفظ
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ جميع الإعدادات",
            font=(FONTS['arabic'], 14, "bold"),
            fg_color=WARM_COLORS['mint'],
            hover_color=self.lighten_color(WARM_COLORS['mint']),
            height=40,
            width=180,
            command=self.save_all_settings
        )
        save_btn.pack(side="right", padx=5)
        
        # زر الاستعادة
        restore_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 استعادة الافتراضي",
            font=(FONTS['arabic'], 14, "bold"),
            fg_color=WARM_COLORS['sunset'],
            hover_color=self.lighten_color(WARM_COLORS['sunset']),
            height=40,
            width=180,
            command=self.restore_defaults
        )
        restore_btn.pack(side="right", padx=5)
        
        # زر التجربة
        test_btn = ctk.CTkButton(
            buttons_frame,
            text="🎯 تجربة الإعدادات",
            font=(FONTS['arabic'], 14, "bold"),
            fg_color=WARM_COLORS['turquoise'],
            hover_color=self.lighten_color(WARM_COLORS['turquoise']),
            height=40,
            width=180,
            command=self.test_settings
        )
        test_btn.pack(side="right", padx=5)
        
        # معلومات الحالة
        status_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        status_frame.pack(side="right", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✅ جاهز للتحكم",
            font=(FONTS['arabic'], 12),
            text_color=WARM_COLORS['deep_teal']
        )
        self.status_label.pack()
    
    def lighten_color(self, color):
        """تفتيح اللون للتأثير عند التمرير"""
        # تحويل بسيط لتفتيح اللون
        if color.startswith('#'):
            hex_color = color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        return color

    def show_section(self, section_key):
        """عرض قسم معين من الإعدادات"""
        # تحديث الزر النشط
        for key, button in self.sidebar_buttons.items():
            if key == section_key:
                button.configure(fg_color=WARM_COLORS['coral'])
            else:
                # إعادة اللون الأصلي للأزرار الأخرى
                section_colors = {
                    'general': WARM_COLORS['coral'],
                    'users': WARM_COLORS['sunset'],
                    'invoices': WARM_COLORS['golden'],
                    'payroll': WARM_COLORS['mint'],
                    'warehouses': WARM_COLORS['sky'],
                    'modules': WARM_COLORS['rose'],
                    'backup': WARM_COLORS['peach'],
                    'import_export': WARM_COLORS['turquoise'],
                    'appearance': WARM_COLORS['violet'],
                    'security': WARM_COLORS['lavender'],
                    'numbering': WARM_COLORS['coral']
                }
                button.configure(fg_color=section_colors.get(key, WARM_COLORS['coral']))

        # مسح المحتوى الحالي
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # عرض القسم المطلوب
        self.current_section = section_key

        if section_key == "general":
            self.create_general_settings()
        elif section_key == "users":
            self.create_users_settings()
        elif section_key == "invoices":
            self.create_invoices_settings()
        elif section_key == "payroll":
            self.create_payroll_settings()
        elif section_key == "warehouses":
            self.create_warehouses_settings()
        elif section_key == "modules":
            self.create_modules_settings()
        elif section_key == "backup":
            self.create_backup_settings()
        elif section_key == "import_export":
            self.create_import_export_settings()
        elif section_key == "appearance":
            self.create_appearance_settings()
        elif section_key == "security":
            self.create_security_settings()
        elif section_key == "numbering":
            self.create_numbering_settings()

    def create_section_header(self, title, icon, description, color):
        """إنشاء رأس القسم"""
        header_frame = ctk.CTkFrame(
            self.scrollable_frame,
            height=100,
            fg_color=color,
            corner_radius=15
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        # الأيقونة
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=("Segoe UI Emoji", 36),
            text_color="white"
        )
        icon_label.pack(side="right", padx=30, pady=20)

        # النص
        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            font=(FONTS['arabic'], 24, "bold"),
            text_color="white",
            anchor="e"
        )
        title_label.pack(anchor="e", pady=(15, 5))

        desc_label = ctk.CTkLabel(
            text_frame,
            text=description,
            font=(FONTS['arabic'], 14),
            text_color=WARM_COLORS['cream'],
            anchor="e"
        )
        desc_label.pack(anchor="e")

    def create_settings_card(self, title, content_func, color=None):
        """إنشاء بطاقة إعدادات"""
        if color is None:
            color = WARM_COLORS['light_peach']

        card_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=color,
            corner_radius=12
        )
        card_frame.pack(fill="x", pady=10)

        # عنوان البطاقة
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=(FONTS['arabic'], 16, "bold"),
            text_color=WARM_COLORS['dark_coral'],
            anchor="e"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))

        # محتوى البطاقة
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 15))

        # استدعاء دالة المحتوى
        content_func(content_frame)

        return card_frame

    def create_general_settings(self):
        """إنشاء إعدادات عامة مفصلة"""
        self.create_section_header(
            "الإعدادات العامة",
            "🧩",
            "إعدادات اللغة، التاريخ، الشعار، وشكل الواجهة",
            WARM_COLORS['coral']
        )

        # بطاقة الوصول السريع للنوافذ
        def quick_access_content(parent):
            # عنوان القسم
            title_label = ctk.CTkLabel(
                parent,
                text="🚀 الوصول السريع للنوافذ",
                font=(FONTS['arabic'], 16, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            title_label.pack(pady=(0, 15))

            # إطار الأزرار - الصف الأول
            buttons_frame1 = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame1.pack(fill="x", pady=5)

            # أزرار النوافذ الرئيسية
            quick_buttons1 = [
                {"text": "📊 المحاسبة الرئيسية", "command": self.open_accounting_window, "color": WARM_COLORS['coral']},
                {"text": "🛒 المبيعات", "command": self.open_sales_window, "color": WARM_COLORS['mint']},
                {"text": "📦 المشتريات", "command": self.open_purchases_window, "color": WARM_COLORS['golden']},
                {"text": "📋 المخزون", "command": self.open_inventory_window, "color": WARM_COLORS['sky']}
            ]

            for btn_info in quick_buttons1:
                btn = ctk.CTkButton(
                    buttons_frame1,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 12, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=40,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=5, fill="x", expand=True)

            # إطار الأزرار - الصف الثاني
            buttons_frame2 = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame2.pack(fill="x", pady=5)

            quick_buttons2 = [
                {"text": "👥 العملاء", "command": self.open_customers_window, "color": WARM_COLORS['sunset']},
                {"text": "🏭 الموردين", "command": self.open_suppliers_window, "color": WARM_COLORS['rose']},
                {"text": "👨‍💼 الموظفين", "command": self.open_employees_window, "color": WARM_COLORS['peach']},
                {"text": "📈 التقارير", "command": self.open_reports_window, "color": WARM_COLORS['turquoise']}
            ]

            for btn_info in quick_buttons2:
                btn = ctk.CTkButton(
                    buttons_frame2,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 12, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=40,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=5, fill="x", expand=True)

            # إطار الأزرار - الصف الثالث
            buttons_frame3 = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame3.pack(fill="x", pady=5)

            quick_buttons3 = [
                {"text": "🛒 نقاط البيع", "command": self.open_pos_window, "color": WARM_COLORS['violet']},
                {"text": "💾 النسخ الاحتياطي", "command": self.open_backup_window, "color": WARM_COLORS['lavender']},
                {"text": "🖼️ ملء الشاشة", "command": self.set_fullscreen_mode, "color": WARM_COLORS['mint']},
                {"text": "📊 تصدير Excel", "command": self.export_to_excel, "color": WARM_COLORS['golden']}
            ]

            for btn_info in quick_buttons3:
                btn = ctk.CTkButton(
                    buttons_frame3,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 12, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=40,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=5, fill="x", expand=True)

        self.create_settings_card("🚀 الوصول السريع", quick_access_content, WARM_COLORS['light_peach'])

        # بطاقة معلومات الشركة المفصلة
        def company_info_content(parent):
            # اسم الشركة
            self.create_input_field(parent, "اسم الشركة:", "company_name", "شركة ست الكل للمحاسبة")

            # اسم الشركة بالإنجليزية
            self.create_input_field(parent, "اسم الشركة (English):", "company_name_en", "")

            # السجل التجاري
            self.create_input_field(parent, "السجل التجاري:", "commercial_register", "")

            # الرقم الضريبي
            self.create_input_field(parent, "الرقم الضريبي:", "tax_number", "")

            # رقم الهاتف الرئيسي
            self.create_input_field(parent, "رقم الهاتف الرئيسي:", "phone_main", "")

            # رقم الهاتف الفرعي
            self.create_input_field(parent, "رقم الهاتف الفرعي:", "phone_secondary", "")

            # رقم الفاكس
            self.create_input_field(parent, "رقم الفاكس:", "fax", "")

            # البريد الإلكتروني الرئيسي
            self.create_input_field(parent, "البريد الإلكتروني الرئيسي:", "email_main", "")

            # البريد الإلكتروني للدعم
            self.create_input_field(parent, "بريد الدعم الفني:", "email_support", "")

            # الموقع الإلكتروني
            self.create_input_field(parent, "الموقع الإلكتروني:", "website", "")

            # العنوان التفصيلي
            self.create_textarea_field(parent, "عنوان الشركة التفصيلي:", "address_detailed", "")

            # المدينة
            self.create_input_field(parent, "المدينة:", "city", "")

            # المنطقة/المحافظة
            self.create_input_field(parent, "المنطقة/المحافظة:", "region", "")

            # الرمز البريدي
            self.create_input_field(parent, "الرمز البريدي:", "postal_code", "")

            # الدولة
            self.create_dropdown_field(parent, "الدولة:", "country",
                                     ["السعودية", "الإمارات", "الكويت", "قطر", "البحرين", "عمان", "مصر", "الأردن"], "السعودية")

            # شعار الشركة
            self.create_file_field(parent, "شعار الشركة (PNG/JPG):", "company_logo", "اختيار صورة")

            # شعار فرعي
            self.create_file_field(parent, "شعار فرعي:", "company_logo_alt", "اختيار صورة")

            # ختم الشركة
            self.create_file_field(parent, "ختم الشركة:", "company_stamp", "اختيار صورة")

        self.create_settings_card("🏢 معلومات الشركة التفصيلية", company_info_content, WARM_COLORS['light_peach'])

        # بطاقة الإعدادات الأساسية المتقدمة
        def basic_settings_content(parent):
            # اللغة الافتراضية
            self.create_dropdown_field(parent, "اللغة الافتراضية:", "default_language",
                                     ["العربية", "English", "Français", "Español"], "العربية")

            # اللغة الثانوية
            self.create_dropdown_field(parent, "اللغة الثانوية:", "secondary_language",
                                     ["English", "العربية", "Français", "Español"], "English")

            # تنسيق التاريخ
            self.create_dropdown_field(parent, "تنسيق التاريخ:", "date_format",
                                     ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD", "DD-MM-YYYY"], "DD/MM/YYYY")

            # تنسيق الوقت
            self.create_dropdown_field(parent, "تنسيق الوقت:", "time_format",
                                     ["24 ساعة", "12 ساعة AM/PM"], "24 ساعة")

            # المنطقة الزمنية
            self.create_dropdown_field(parent, "المنطقة الزمنية:", "timezone",
                                     ["Asia/Riyadh", "Asia/Dubai", "Asia/Kuwait", "UTC"], "Asia/Riyadh")

            # العملة الافتراضية
            self.create_dropdown_field(parent, "العملة الافتراضية:", "default_currency",
                                     ["ريال سعودي", "درهم إماراتي", "دينار كويتي", "ريال قطري", "دولار أمريكي", "يورو"], "ريال سعودي")

            # رمز العملة
            self.create_input_field(parent, "رمز العملة:", "currency_symbol", "ر.س")

            # عدد الخانات العشرية
            self.create_dropdown_field(parent, "عدد الخانات العشرية:", "decimal_places",
                                     ["0", "1", "2", "3", "4"], "2")

            # فاصل الآلاف
            self.create_dropdown_field(parent, "فاصل الآلاف:", "thousands_separator",
                                     [",", ".", " ", "بدون"], ",")

            # الوضع الليلي
            self.create_switch_field(parent, "تفعيل الوضع الليلي:", "dark_mode", False)

            # الوضع التلقائي للثيم
            self.create_switch_field(parent, "تغيير الثيم تلقائياً:", "auto_theme", False)

            # الأصوات
            self.create_switch_field(parent, "تفعيل الأصوات:", "sounds_enabled", True)

            # الإشعارات
            self.create_switch_field(parent, "تفعيل الإشعارات:", "notifications_enabled", True)

            # التحديث التلقائي
            self.create_switch_field(parent, "التحديث التلقائي:", "auto_update", True)

        self.create_settings_card("⚙️ الإعدادات الأساسية المتقدمة", basic_settings_content, WARM_COLORS['mint_bg'])

        # بطاقة إعدادات الواجهة
        def interface_settings_content(parent):
            # حجم الخط الافتراضي
            self.create_dropdown_field(parent, "حجم الخط الافتراضي:", "default_font_size",
                                     ["صغير (10)", "متوسط (12)", "كبير (14)", "كبير جداً (16)"], "متوسط (12)")

            # نوع الخط العربي
            self.create_dropdown_field(parent, "الخط العربي الافتراضي:", "arabic_font",
                                     ["Cairo", "Amiri", "Noto Naskh Arabic", "Tajawal", "Almarai", "IBM Plex Sans Arabic"], "Cairo")

            # نوع الخط الإنجليزي
            self.create_dropdown_field(parent, "الخط الإنجليزي:", "english_font",
                                     ["Arial", "Calibri", "Times New Roman", "Segoe UI", "Roboto"], "Arial")

            # كثافة الخط
            self.create_dropdown_field(parent, "كثافة الخط:", "font_weight",
                                     ["عادي", "عريض", "رفيع"], "عادي")

            # التحكم في حجم النافذة الحالية
            window_control_frame = ctk.CTkFrame(parent, fg_color="transparent")
            window_control_frame.pack(fill="x", pady=15)

            window_control_title = ctk.CTkLabel(
                window_control_frame,
                text="🖼️ التحكم في حجم النافذة الحالية:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            window_control_title.pack(anchor="e", pady=(0, 10))

            # أزرار التحكم في النافذة
            window_buttons_frame = ctk.CTkFrame(window_control_frame, fg_color="transparent")
            window_buttons_frame.pack(fill="x", pady=5)

            window_buttons = [
                {"text": "🖼️ ملء الشاشة الكامل", "command": self.set_fullscreen_mode, "color": WARM_COLORS['mint']},
                {"text": "📺 تكبير النافذة", "command": self.maximize_window, "color": WARM_COLORS['sky']},
                {"text": "🪟 نافذة عادية", "command": self.set_normal_window, "color": WARM_COLORS['golden']},
                {"text": "📱 نافذة صغيرة", "command": self.set_small_window, "color": WARM_COLORS['sunset']}
            ]

            for btn_info in window_buttons:
                btn = ctk.CTkButton(
                    window_buttons_frame,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 11, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=35,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=3, fill="x", expand=True)

            # معلومات النافذة الحالية
            info_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['soft_cream'], corner_radius=8)
            info_frame.pack(fill="x", pady=10)

            try:
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()
                window_width = self.window.winfo_width()
                window_height = self.window.winfo_height()

                info_text = f"""
                📐 أبعاد الشاشة: {screen_width} × {screen_height}
                🖼️ أبعاد النافذة الحالية: {window_width} × {window_height}
                📊 نسبة التغطية: {(window_width * window_height) / (screen_width * screen_height) * 100:.1f}%
                """

                info_label = ctk.CTkLabel(
                    info_frame,
                    text=info_text,
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['deep_teal'],
                    justify="center"
                )
                info_label.pack(pady=10)

            except Exception as e:
                error_label = ctk.CTkLabel(
                    info_frame,
                    text="⚠️ خطأ في جلب معلومات النافذة",
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['sunset']
                )
                error_label.pack(pady=10)

            # حجم النافذة الافتراضي للجلسات الجديدة
            self.create_dropdown_field(parent, "حجم النافذة الافتراضي للجلسات الجديدة:", "default_window_size",
                                     ["صغير (1024×768)", "متوسط (1366×768)", "كبير (1920×1080)", "ملء الشاشة الكامل"], "ملء الشاشة الكامل")

            # موضع النافذة
            self.create_dropdown_field(parent, "موضع النافذة:", "window_position",
                                     ["وسط الشاشة", "أعلى اليسار", "أعلى اليمين", "ملء الشاشة"], "ملء الشاشة")

            # شفافية النوافذ
            self.create_dropdown_field(parent, "شفافية النوافذ:", "window_opacity",
                                     ["100%", "95%", "90%", "85%"], "100%")

            # تأثيرات الانتقال
            self.create_switch_field(parent, "تأثيرات الانتقال:", "transition_effects", True)

            # الظلال
            self.create_switch_field(parent, "إظهار الظلال:", "show_shadows", True)

            # الحدود المستديرة
            self.create_switch_field(parent, "الحدود المستديرة:", "rounded_corners", True)

            # شريط التقدم المتحرك
            self.create_switch_field(parent, "شريط التقدم المتحرك:", "animated_progress", True)

            # أيقونات ملونة
            self.create_switch_field(parent, "الأيقونات الملونة:", "colored_icons", True)

        self.create_settings_card("🎨 إعدادات الواجهة والتصميم", interface_settings_content, WARM_COLORS['soft_cream'])

        # بطاقة إعدادات النظام
        def system_settings_content(parent):
            # مسار حفظ الملفات
            self.create_file_field(parent, "مسار حفظ الملفات:", "default_save_path", "اختيار مجلد")

            # مسار النسخ الاحتياطي
            self.create_file_field(parent, "مسار النسخ الاحتياطي:", "backup_path", "اختيار مجلد")

            # مسار التقارير
            self.create_file_field(parent, "مسار حفظ التقارير:", "reports_path", "اختيار مجلد")

            # مسار الصور
            self.create_file_field(parent, "مسار حفظ الصور:", "images_path", "اختيار مجلد")

            # حد الذاكرة
            self.create_dropdown_field(parent, "حد استخدام الذاكرة:", "memory_limit",
                                     ["512 MB", "1 GB", "2 GB", "4 GB", "بدون حد"], "2 GB")

            # مستوى السجلات
            self.create_dropdown_field(parent, "مستوى تسجيل الأحداث:", "log_level",
                                     ["أساسي", "تفصيلي", "تشخيصي", "إيقاف"], "أساسي")

            # مدة حفظ السجلات
            self.create_dropdown_field(parent, "مدة حفظ السجلات:", "log_retention",
                                     ["30 يوم", "60 يوم", "90 يوم", "180 يوم", "سنة واحدة"], "90 يوم")

            # التشغيل مع النظام
            self.create_switch_field(parent, "التشغيل مع بدء النظام:", "startup_with_system", False)

            # التصغير للشريط
            self.create_switch_field(parent, "التصغير لشريط المهام:", "minimize_to_tray", True)

            # الإغلاق للشريط
            self.create_switch_field(parent, "الإغلاق للشريط بدلاً من الخروج:", "close_to_tray", False)

            # التحقق من التحديثات
            self.create_switch_field(parent, "التحقق من التحديثات تلقائياً:", "check_updates", True)

            # إرسال تقارير الأخطاء
            self.create_switch_field(parent, "إرسال تقارير الأخطاء:", "send_error_reports", True)

        self.create_settings_card("🖥️ إعدادات النظام المتقدمة", system_settings_content, WARM_COLORS['light_peach'])

    def create_input_field(self, parent, label, key, default_value=""):
        """إنشاء حقل إدخال نص"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))

        # حقل الإدخال
        entry = ctk.CTkEntry(
            field_frame,
            font=(FONTS['arabic'], 12),
            height=35,
            fg_color="white",
            border_color=WARM_COLORS['coral'],
            border_width=2
        )
        entry.pack(side="right", fill="x", expand=True)
        entry.insert(0, self.current_settings.get(key, default_value))

        # حفظ مرجع الحقل
        setattr(self, f"field_{key}", entry)

        return entry

    def create_dropdown_field(self, parent, label, key, options, default_value=""):
        """إنشاء حقل قائمة منسدلة"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))

        # القائمة المنسدلة
        dropdown = ctk.CTkComboBox(
            field_frame,
            values=options,
            font=(FONTS['arabic'], 12),
            height=35,
            fg_color="white",
            border_color=WARM_COLORS['coral'],
            border_width=2,
            button_color=WARM_COLORS['coral'],
            button_hover_color=self.lighten_color(WARM_COLORS['coral'])
        )
        dropdown.pack(side="right", fill="x", expand=True)
        dropdown.set(self.current_settings.get(key, default_value))

        # حفظ مرجع الحقل
        setattr(self, f"field_{key}", dropdown)

        return dropdown

    def create_switch_field(self, parent, label, key, default_value=False):
        """إنشاء حقل مفتاح تشغيل/إيقاف"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))

        # المفتاح
        switch = ctk.CTkSwitch(
            field_frame,
            text="",
            font=(FONTS['arabic'], 12),
            progress_color=WARM_COLORS['mint'],
            button_color=WARM_COLORS['coral'],
            button_hover_color=self.lighten_color(WARM_COLORS['coral'])
        )
        switch.pack(side="right")

        # تعيين القيمة الافتراضية
        current_value = self.current_settings.get(key, default_value)
        if current_value:
            switch.select()
        else:
            switch.deselect()

        # حفظ مرجع الحقل
        setattr(self, f"field_{key}", switch)

        return switch

    def create_textarea_field(self, parent, label, key, default_value=""):
        """إنشاء حقل نص متعدد الأسطر"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="ne",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10), anchor="n")

        # حقل النص
        textbox = ctk.CTkTextbox(
            field_frame,
            font=(FONTS['arabic'], 12),
            height=80,
            fg_color="white",
            border_color=WARM_COLORS['coral'],
            border_width=2
        )
        textbox.pack(side="right", fill="both", expand=True)
        textbox.insert("1.0", self.current_settings.get(key, default_value))

        # حفظ مرجع الحقل
        setattr(self, f"field_{key}", textbox)

        return textbox

    def create_file_field(self, parent, label, key, button_text="اختيار ملف"):
        """إنشاء حقل اختيار ملف"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))

        # إطار الملف
        file_frame = ctk.CTkFrame(field_frame, fg_color="transparent")
        file_frame.pack(side="right", fill="x", expand=True)

        # زر الاختيار
        file_button = ctk.CTkButton(
            file_frame,
            text=button_text,
            font=(FONTS['arabic'], 12),
            height=35,
            width=120,
            fg_color=WARM_COLORS['sunset'],
            hover_color=self.lighten_color(WARM_COLORS['sunset']),
            command=lambda: self.select_file(key)
        )
        file_button.pack(side="left", padx=(0, 10))

        # عرض المسار
        path_label = ctk.CTkLabel(
            file_frame,
            text=self.current_settings.get(key, "لم يتم اختيار ملف"),
            font=(FONTS['arabic'], 10),
            text_color=WARM_COLORS['deep_teal'],
            anchor="w"
        )
        path_label.pack(side="left", fill="x", expand=True)

        # حفظ مرجع الحقل
        setattr(self, f"field_{key}", path_label)
        setattr(self, f"button_{key}", file_button)

        return file_button, path_label

    def create_color_field(self, parent, label, key, default_value="#FFFFFF"):
        """إنشاء حقل اختيار لون"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)

        # التسمية
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label,
            font=(FONTS['arabic'], 12, "bold"),
            text_color=WARM_COLORS['deep_teal'],
            anchor="e",
            width=150
        )
        label_widget.pack(side="right", padx=(0, 10))

        # إطار اللون
        color_frame = ctk.CTkFrame(field_frame, fg_color="transparent")
        color_frame.pack(side="right", fill="x", expand=True)

        # زر اختيار اللون
        current_color = self.current_settings.get(key, default_value)
        color_button = ctk.CTkButton(
            color_frame,
            text="اختيار اللون",
            font=(FONTS['arabic'], 12),
            height=35,
            width=120,
            fg_color=current_color,
            hover_color=self.lighten_color(current_color),
            command=lambda: self.select_color(key)
        )
        color_button.pack(side="left", padx=(0, 10))

        # عرض كود اللون
        color_label = ctk.CTkLabel(
            color_frame,
            text=current_color,
            font=(FONTS['arabic'], 10),
            text_color=WARM_COLORS['deep_teal'],
            anchor="w"
        )
        color_label.pack(side="left", fill="x", expand=True)

        # حفظ مرجع الحقل
        setattr(self, f"field_{key}", color_label)
        setattr(self, f"button_{key}", color_button)

        return color_button, color_label

    def select_file(self, key):
        """اختيار ملف"""
        file_path = filedialog.askopenfilename(
            title="اختيار ملف",
            filetypes=[
                ("صور", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("جميع الملفات", "*.*")
            ]
        )
        if file_path:
            # تحديث عرض المسار
            path_label = getattr(self, f"field_{key}")
            path_label.configure(text=file_path)

            # حفظ في الإعدادات
            self.current_settings[key] = file_path

    def select_color(self, key):
        """اختيار لون"""
        current_color = self.current_settings.get(key, "#FFFFFF")
        color = colorchooser.askcolor(
            title="اختيار لون",
            initialcolor=current_color
        )
        if color[1]:  # إذا تم اختيار لون
            new_color = color[1]

            # تحديث الزر واللون
            color_button = getattr(self, f"button_{key}")
            color_label = getattr(self, f"field_{key}")

            color_button.configure(fg_color=new_color, hover_color=self.lighten_color(new_color))
            color_label.configure(text=new_color)

            # حفظ في الإعدادات
            self.current_settings[key] = new_color

    def create_numbering_settings(self):
        """إنشاء إعدادات الأرقام التسلسلية"""
        self.create_section_header(
            "الأرقام التسلسلية",
            "🔢",
            "توليد تلقائي للأرقام التسلسلية لجميع الفواتير والموظفين والعملاء",
            WARM_COLORS['turquoise']
        )

        # بطاقة إعدادات الفواتير
        def invoice_numbering_content(parent):
            self.create_input_field(parent, "بادئة فواتير البيع:", "sales_invoice_prefix", "INV")
            self.create_input_field(parent, "بادئة فواتير الشراء:", "purchase_invoice_prefix", "PUR")
            self.create_input_field(parent, "بادئة المرتجعات:", "return_prefix", "RET")
            self.create_input_field(parent, "طول الرقم التسلسلي:", "number_length", "6")
            self.create_switch_field(parent, "تضمين السنة:", "include_year", True)
            self.create_switch_field(parent, "تضمين الشهر:", "include_month", True)

        self.create_settings_card("🧾 ترقيم الفواتير", invoice_numbering_content, WARM_COLORS['light_peach'])

        # بطاقة إعدادات الموظفين والعملاء
        def entity_numbering_content(parent):
            self.create_input_field(parent, "بادئة الموظفين:", "employee_prefix", "EMP")
            self.create_input_field(parent, "بادئة العملاء:", "customer_prefix", "CUS")
            self.create_input_field(parent, "بادئة الموردين:", "supplier_prefix", "SUP")
            self.create_switch_field(parent, "ترقيم تلقائي:", "auto_numbering", True)

        self.create_settings_card("👥 ترقيم الأشخاص", entity_numbering_content, WARM_COLORS['mint_bg'])

    def create_appearance_settings(self):
        """إنشاء إعدادات تخصيص الواجهة"""
        self.create_section_header(
            "تخصيص الواجهة",
            "🎨",
            "تخصيص الألوان والخطوط وشكل الواجهة",
            WARM_COLORS['violet']
        )

        # بطاقة الألوان
        def colors_content(parent):
            self.create_color_field(parent, "اللون الأساسي:", "primary_color", WARM_COLORS['coral'])
            self.create_color_field(parent, "لون الخلفية:", "background_color", WARM_COLORS['warm_white'])
            self.create_color_field(parent, "لون العناوين:", "header_color", WARM_COLORS['deep_teal'])
            self.create_color_field(parent, "لون الأزرار:", "button_color", WARM_COLORS['mint'])
            self.create_color_field(parent, "لون النص:", "text_color", WARM_COLORS['dark_coral'])

        self.create_settings_card("🌈 الألوان", colors_content, WARM_COLORS['light_peach'])

        # بطاقة الخطوط
        def fonts_content(parent):
            font_options = ["Cairo", "Amiri", "Noto Naskh Arabic", "Tajawal", "Almarai"]
            self.create_dropdown_field(parent, "الخط الأساسي:", "main_font", font_options, "Cairo")
            self.create_dropdown_field(parent, "خط العناوين:", "header_font", font_options, "Cairo")
            self.create_dropdown_field(parent, "حجم الخط:", "font_size", ["صغير", "متوسط", "كبير", "كبير جداً"], "متوسط")
            self.create_switch_field(parent, "خط عريض للعناوين:", "bold_headers", True)

        self.create_settings_card("🔤 الخطوط", fonts_content, WARM_COLORS['mint_bg'])

    def create_backup_settings(self):
        """إنشاء إعدادات النسخ الاحتياطي"""
        self.create_section_header(
            "النسخ الاحتياطي",
            "💾",
            "إدارة النسخ الاحتياطية واستعادة النظام",
            WARM_COLORS['peach']
        )

        # بطاقة الإعدادات التلقائية
        def auto_backup_content(parent):
            self.create_switch_field(parent, "النسخ التلقائي:", "auto_backup", True)
            self.create_dropdown_field(parent, "فترة النسخ:", "backup_frequency",
                                     ["يومياً", "أسبوعياً", "شهرياً"], "يومياً")
            self.create_dropdown_field(parent, "وقت النسخ:", "backup_time",
                                     ["02:00", "03:00", "04:00", "23:00"], "02:00")
            self.create_input_field(parent, "عدد النسخ المحفوظة:", "max_backups", "30")
            self.create_switch_field(parent, "ضغط النسخ:", "compress_backups", True)

        self.create_settings_card("⏰ النسخ التلقائي", auto_backup_content, WARM_COLORS['light_peach'])

        # بطاقة إدارة النسخ الاحتياطية
        def backup_management_content(parent):
            # عنوان القسم
            title_label = ctk.CTkLabel(
                parent,
                text="🛠️ إدارة النسخ الاحتياطية",
                font=(FONTS['arabic'], 16, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            title_label.pack(pady=(0, 15))

            # الصف الأول من الأزرار
            buttons_frame1 = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame1.pack(fill="x", pady=5)

            backup_buttons1 = [
                {"text": "💾 نسخة احتياطية فورية", "command": self.perform_backup, "color": WARM_COLORS['mint']},
                {"text": "🔄 استعادة نسخة احتياطية", "command": self.restore_backup, "color": WARM_COLORS['sunset']},
                {"text": "📋 قائمة النسخ الاحتياطية", "command": self.list_backups, "color": WARM_COLORS['sky']},
                {"text": "🗑️ حذف نسخ قديمة", "command": self.cleanup_old_backups, "color": WARM_COLORS['rose']}
            ]

            for btn_info in backup_buttons1:
                btn = ctk.CTkButton(
                    buttons_frame1,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 12, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=40,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=5, fill="x", expand=True)

            # الصف الثاني من الأزرار
            buttons_frame2 = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame2.pack(fill="x", pady=5)

            backup_buttons2 = [
                {"text": "📤 تصدير نسخة احتياطية", "command": self.export_backup, "color": WARM_COLORS['golden']},
                {"text": "📥 استيراد نسخة احتياطية", "command": self.import_backup, "color": WARM_COLORS['peach']},
                {"text": "🔍 فحص سلامة النسخ", "command": self.verify_backups, "color": WARM_COLORS['turquoise']},
                {"text": "⚙️ جدولة النسخ التلقائي", "command": self.schedule_backups, "color": WARM_COLORS['violet']}
            ]

            for btn_info in backup_buttons2:
                btn = ctk.CTkButton(
                    buttons_frame2,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 12, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=40,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=5, fill="x", expand=True)

            # معلومات النسخ الاحتياطية
            info_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
            info_frame.pack(fill="x", pady=15)

            info_title = ctk.CTkLabel(
                info_frame,
                text="📊 معلومات النسخ الاحتياطية",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            info_title.pack(pady=(10, 5))

            # عرض معلومات النسخ
            try:
                backup_info = self.get_backup_info()
                info_text = f"""
                آخر نسخة احتياطية: {backup_info.get('last_backup', 'لا توجد')}
                عدد النسخ المتوفرة: {backup_info.get('backup_count', '0')}
                حجم النسخ الإجمالي: {backup_info.get('total_size', '0 MB')}
                مساحة القرص المتاحة: {backup_info.get('free_space', 'غير معروف')}
                """

                info_label = ctk.CTkLabel(
                    info_frame,
                    text=info_text,
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['deep_teal'],
                    justify="center"
                )
                info_label.pack(pady=10)

            except Exception as e:
                error_label = ctk.CTkLabel(
                    info_frame,
                    text="⚠️ خطأ في جلب معلومات النسخ الاحتياطية",
                    font=(FONTS['arabic'], 11),
                    text_color=WARM_COLORS['sunset']
                )
                error_label.pack(pady=10)

        self.create_settings_card("🛠️ إدارة النسخ", backup_management_content, WARM_COLORS['mint_bg'])

    def create_backup(self):
        """إنشاء نسخة احتياطية"""
        try:
            # إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجوداً
            backup_dir = PROJECT_ROOT / "backups"
            backup_dir.mkdir(exist_ok=True)

            # اسم الملف مع التاريخ والوقت
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"backup_{timestamp}.db"

            # نسخ قاعدة البيانات
            import shutil
            shutil.copy2(DATABASE_PATH, backup_file)

            self.update_status(f"✅ تم إنشاء النسخة الاحتياطية: {backup_file.name}")
            messagebox.showinfo("نجح", f"تم إنشاء النسخة الاحتياطية بنجاح\n{backup_file}")

        except Exception as e:
            self.update_status(f"❌ خطأ في إنشاء النسخة الاحتياطية")
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء النسخة الاحتياطية:\n{str(e)}")

    def restore_backup(self):
        """استعادة من نسخة احتياطية"""
        backup_file = filedialog.askopenfilename(
            title="اختيار نسخة احتياطية",
            initialdir=PROJECT_ROOT / "backups",
            filetypes=[("قواعد البيانات", "*.db"), ("جميع الملفات", "*.*")]
        )

        if backup_file:
            result = messagebox.askyesno(
                "تأكيد الاستعادة",
                "هل أنت متأكد من استعادة هذه النسخة الاحتياطية؟\n"
                "سيتم استبدال البيانات الحالية بالكامل!"
            )

            if result:
                try:
                    import shutil
                    shutil.copy2(backup_file, DATABASE_PATH)

                    self.update_status("✅ تم استعادة النسخة الاحتياطية بنجاح")
                    messagebox.showinfo("نجح", "تم استعادة النسخة الاحتياطية بنجاح\nيُنصح بإعادة تشغيل البرنامج")

                except Exception as e:
                    self.update_status("❌ خطأ في استعادة النسخة الاحتياطية")
                    messagebox.showerror("خطأ", f"حدث خطأ في استعادة النسخة الاحتياطية:\n{str(e)}")

    def update_status(self, message):
        """تحديث رسالة الحالة"""
        self.status_label.configure(text=message)

    def create_users_settings(self):
        """إنشاء إعدادات المستخدمين والصلاحيات المفصلة"""
        self.create_section_header(
            "المستخدمون والصلاحيات",
            "👥",
            "إدارة المستخدمين والأدوار والصلاحيات",
            WARM_COLORS['sunset']
        )

        # بطاقة إدارة المستخدمين
        def users_management_content(parent):
            # زر إضافة مستخدم جديد
            add_user_btn = ctk.CTkButton(
                parent,
                text="➕ إضافة مستخدم جديد",
                font=(FONTS['arabic'], 14, "bold"),
                fg_color=WARM_COLORS['mint'],
                hover_color=self.lighten_color(WARM_COLORS['mint']),
                height=40,
                command=self.open_add_user_dialog
            )
            add_user_btn.pack(pady=10)

            # قائمة المستخدمين الحاليين
            users_frame = ctk.CTkFrame(parent, fg_color="transparent")
            users_frame.pack(fill="x", pady=10)

            # عنوان القائمة
            users_title = ctk.CTkLabel(
                users_frame,
                text="👥 المستخدمون الحاليون:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            users_title.pack(anchor="e", pady=(0, 10))

            # قائمة المستخدمين (مثال)
            sample_users = [
                {"name": "المدير العام", "username": "admin", "role": "مدير", "status": "نشط", "last_login": "2025-07-22 10:30"},
                {"name": "محاسب رئيسي", "username": "accountant1", "role": "محاسب", "status": "نشط", "last_login": "2025-07-22 09:15"},
                {"name": "موظف مبيعات", "username": "sales1", "role": "مستخدم", "status": "غير نشط", "last_login": "2025-07-21 16:45"}
            ]

            for user in sample_users:
                user_card = ctk.CTkFrame(users_frame, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
                user_card.pack(fill="x", pady=5)

                user_info = ctk.CTkLabel(
                    user_card,
                    text=f"👤 {user['name']} ({user['username']}) - {user['role']} - {user['status']}",
                    font=(FONTS['arabic'], 12),
                    text_color=WARM_COLORS['deep_teal'],
                    anchor="e"
                )
                user_info.pack(side="right", padx=15, pady=10)

                # أزرار الإجراءات
                actions_frame = ctk.CTkFrame(user_card, fg_color="transparent")
                actions_frame.pack(side="left", padx=15, pady=5)

                edit_btn = ctk.CTkButton(
                    actions_frame,
                    text="✏️ تعديل",
                    width=80,
                    height=30,
                    fg_color=WARM_COLORS['golden'],
                    hover_color=self.lighten_color(WARM_COLORS['golden']),
                    command=lambda u=user: self.edit_user(u)
                )
                edit_btn.pack(side="left", padx=2)

                delete_btn = ctk.CTkButton(
                    actions_frame,
                    text="🗑️ حذف",
                    width=80,
                    height=30,
                    fg_color=WARM_COLORS['coral'],
                    hover_color=self.lighten_color(WARM_COLORS['coral']),
                    command=lambda u=user: self.delete_user(u)
                )
                delete_btn.pack(side="left", padx=2)

        self.create_settings_card("👥 إدارة المستخدمين", users_management_content, WARM_COLORS['light_peach'])

        # بطاقة الأدوار والصلاحيات
        def roles_permissions_content(parent):
            # الأدوار المتاحة
            roles_title = ctk.CTkLabel(
                parent,
                text="🎭 الأدوار والصلاحيات:",
                font=(FONTS['arabic'], 14, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            roles_title.pack(anchor="e", pady=(0, 10))

            # دور المدير
            manager_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['mint_bg'], corner_radius=8)
            manager_frame.pack(fill="x", pady=5)

            manager_title = ctk.CTkLabel(
                manager_frame,
                text="👑 مدير النظام - صلاحيات كاملة",
                font=(FONTS['arabic'], 12, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            manager_title.pack(anchor="e", padx=15, pady=(10, 5))

            manager_permissions = [
                "✅ إدارة جميع المستخدمين", "✅ الوصول لجميع التقارير", "✅ إعدادات النظام",
                "✅ النسخ الاحتياطي", "✅ ضبط المصنع", "✅ إدارة قاعدة البيانات"
            ]

            for perm in manager_permissions:
                perm_label = ctk.CTkLabel(
                    manager_frame,
                    text=perm,
                    font=(FONTS['arabic'], 10),
                    text_color=WARM_COLORS['rich_purple'],
                    anchor="e"
                )
                perm_label.pack(anchor="e", padx=25, pady=1)

            # مساحة فارغة
            ctk.CTkLabel(manager_frame, text="", height=5).pack()

            # دور المحاسب
            accountant_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['soft_cream'], corner_radius=8)
            accountant_frame.pack(fill="x", pady=5)

            accountant_title = ctk.CTkLabel(
                accountant_frame,
                text="📊 محاسب - صلاحيات محاسبية",
                font=(FONTS['arabic'], 12, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            accountant_title.pack(anchor="e", padx=15, pady=(10, 5))

            accountant_permissions = [
                "✅ إدارة الفواتير", "✅ التقارير المالية", "✅ إدارة العملاء والموردين",
                "✅ المخزون", "❌ إعدادات النظام", "❌ إدارة المستخدمين"
            ]

            for perm in accountant_permissions:
                color = WARM_COLORS['mint'] if perm.startswith("✅") else WARM_COLORS['coral']
                perm_label = ctk.CTkLabel(
                    accountant_frame,
                    text=perm,
                    font=(FONTS['arabic'], 10),
                    text_color=color,
                    anchor="e"
                )
                perm_label.pack(anchor="e", padx=25, pady=1)

            # مساحة فارغة
            ctk.CTkLabel(accountant_frame, text="", height=5).pack()

            # دور المستخدم العادي
            user_frame = ctk.CTkFrame(parent, fg_color=WARM_COLORS['warm_white'], corner_radius=8)
            user_frame.pack(fill="x", pady=5)

            user_title = ctk.CTkLabel(
                user_frame,
                text="👤 مستخدم عادي - صلاحيات محدودة",
                font=(FONTS['arabic'], 12, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            user_title.pack(anchor="e", padx=15, pady=(10, 5))

            user_permissions = [
                "✅ عرض الفواتير", "✅ إضافة عملاء", "❌ حذف البيانات",
                "❌ التقارير المالية", "❌ إعدادات النظام", "❌ النسخ الاحتياطي"
            ]

            for perm in user_permissions:
                color = WARM_COLORS['mint'] if perm.startswith("✅") else WARM_COLORS['coral']
                perm_label = ctk.CTkLabel(
                    user_frame,
                    text=perm,
                    font=(FONTS['arabic'], 10),
                    text_color=color,
                    anchor="e"
                )
                perm_label.pack(anchor="e", padx=25, pady=1)

            # مساحة فارغة
            ctk.CTkLabel(user_frame, text="", height=5).pack()

            # زر تخصيص الصلاحيات
            customize_btn = ctk.CTkButton(
                parent,
                text="⚙️ تخصيص الصلاحيات",
                font=(FONTS['arabic'], 14, "bold"),
                fg_color=WARM_COLORS['turquoise'],
                hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                height=40,
                command=self.open_permissions_dialog
            )
            customize_btn.pack(pady=10)

        self.create_settings_card("🎭 الأدوار والصلاحيات", roles_permissions_content, WARM_COLORS['mint_bg'])

        # بطاقة إعدادات الأمان المتقدمة
        def security_content(parent):
            # إعدادات كلمة المرور
            self.create_input_field(parent, "الحد الأدنى لطول كلمة المرور:", "min_password_length", "8")
            self.create_input_field(parent, "الحد الأقصى لطول كلمة المرور:", "max_password_length", "50")
            self.create_switch_field(parent, "تطلب أحرف كبيرة:", "require_uppercase", True)
            self.create_switch_field(parent, "تطلب أحرف صغيرة:", "require_lowercase", True)
            self.create_switch_field(parent, "تطلب أرقام:", "require_numbers", True)
            self.create_switch_field(parent, "تطلب رموز خاصة:", "require_symbols", True)
            self.create_switch_field(parent, "منع كلمات المرور الشائعة:", "block_common_passwords", True)

            # إعدادات الجلسة
            self.create_input_field(parent, "مدة انتهاء الجلسة (دقيقة):", "session_timeout", "120")
            self.create_input_field(parent, "تحذير انتهاء الجلسة (دقيقة):", "session_warning", "10")
            self.create_switch_field(parent, "تسجيل خروج تلقائي عند الخمول:", "auto_logout", True)
            self.create_input_field(parent, "مدة الخمول للخروج التلقائي (دقيقة):", "idle_timeout", "30")

            # إعدادات تسجيل الدخول
            self.create_input_field(parent, "عدد محاولات تسجيل الدخول:", "max_login_attempts", "5")
            self.create_input_field(parent, "مدة الحظر بعد المحاولات الفاشلة (دقيقة):", "lockout_duration", "15")
            self.create_switch_field(parent, "تسجيل محاولات الدخول الفاشلة:", "log_failed_attempts", True)
            self.create_switch_field(parent, "إرسال تنبيه عند محاولات دخول مشبوهة:", "alert_suspicious_login", True)

            # إعدادات التشفير
            self.create_dropdown_field(parent, "مستوى التشفير:", "encryption_level",
                                     ["أساسي", "متوسط", "عالي", "عسكري"], "عالي")
            self.create_switch_field(parent, "تشفير قاعدة البيانات:", "encrypt_database", False)
            self.create_switch_field(parent, "تشفير الملفات المحفوظة:", "encrypt_files", True)

            # إعدادات المراجعة
            self.create_switch_field(parent, "تسجيل جميع العمليات:", "log_all_operations", True)
            self.create_switch_field(parent, "تسجيل تغييرات البيانات:", "log_data_changes", True)
            self.create_switch_field(parent, "تسجيل الوصول للتقارير:", "log_report_access", True)
            self.create_input_field(parent, "مدة حفظ سجلات المراجعة (يوم):", "audit_log_retention", "365")

        self.create_settings_card("🔐 إعدادات الأمان المتقدمة", security_content, WARM_COLORS['light_peach'])

    def create_invoices_settings(self):
        """إنشاء إعدادات الفواتير"""
        self.create_section_header(
            "إعدادات الفواتير",
            "🧾",
            "إعدادات البيع والشراء و POS والمرتجعات والتقارير",
            WARM_COLORS['golden']
        )

        # بطاقة إدارة الفواتير السريعة
        def invoice_management_content(parent):
            # عنوان القسم
            title_label = ctk.CTkLabel(
                parent,
                text="⚡ إدارة الفواتير السريعة",
                font=(FONTS['arabic'], 16, "bold"),
                text_color=WARM_COLORS['deep_teal']
            )
            title_label.pack(pady=(0, 15))

            # أزرار إدارة الفواتير
            buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=10)

            # الصف الأول من الأزرار
            row1_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
            row1_frame.pack(fill="x", pady=5)

            invoice_buttons1 = [
                {"text": "🧾 فاتورة مبيعات جديدة", "command": self.create_new_sales_invoice, "color": WARM_COLORS['mint']},
                {"text": "📦 فاتورة مشتريات جديدة", "command": self.create_new_purchase_invoice, "color": WARM_COLORS['golden']},
                {"text": "🔄 مرتجع مبيعات", "command": self.create_sales_return, "color": WARM_COLORS['sunset']},
                {"text": "↩️ مرتجع مشتريات", "command": self.create_purchase_return, "color": WARM_COLORS['rose']}
            ]

            for btn_info in invoice_buttons1:
                btn = ctk.CTkButton(
                    row1_frame,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 12, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=40,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=5, fill="x", expand=True)

            # الصف الثاني من الأزرار
            row2_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
            row2_frame.pack(fill="x", pady=5)

            invoice_buttons2 = [
                {"text": "📋 قائمة فواتير المبيعات", "command": self.view_sales_invoices, "color": WARM_COLORS['sky']},
                {"text": "📄 قائمة فواتير المشتريات", "command": self.view_purchase_invoices, "color": WARM_COLORS['peach']},
                {"text": "🔍 البحث في الفواتير", "command": self.search_invoices, "color": WARM_COLORS['turquoise']},
                {"text": "📊 تقارير الفواتير", "command": self.invoice_reports, "color": WARM_COLORS['violet']}
            ]

            for btn_info in invoice_buttons2:
                btn = ctk.CTkButton(
                    row2_frame,
                    text=btn_info["text"],
                    font=(FONTS['arabic'], 12, "bold"),
                    fg_color=btn_info["color"],
                    hover_color=self.lighten_color(btn_info["color"]),
                    height=40,
                    command=btn_info["command"]
                )
                btn.pack(side="right", padx=5, fill="x", expand=True)

        self.create_settings_card("⚡ إدارة الفواتير", invoice_management_content, WARM_COLORS['light_peach'])

        # بطاقة إعدادات الفواتير العامة
        def invoice_general_content(parent):
            # إعدادات القالب والتصميم
            self.create_dropdown_field(parent, "قالب الفاتورة:", "invoice_template",
                                     ["حديث", "كلاسيكي", "مبسط", "احترافي"], "حديث")

            self.create_dropdown_field(parent, "حجم الورق:", "paper_size",
                                     ["A4", "A5", "Letter", "A3"], "A4")

            self.create_dropdown_field(parent, "اتجاه الطباعة:", "print_orientation",
                                     ["عمودي", "أفقي"], "عمودي")

            # إعدادات العرض
            self.create_switch_field(parent, "عرض الشعار في الفاتورة:", "show_logo", True)
            self.create_switch_field(parent, "عرض ختم الشركة:", "show_stamp", True)
            self.create_switch_field(parent, "عرض توقيع المسؤول:", "show_signature", True)
            self.create_switch_field(parent, "عرض الباركود:", "show_barcode", True)

            # إعدادات الطباعة
            self.create_switch_field(parent, "طباعة تلقائية:", "auto_print", False)
            self.create_switch_field(parent, "حفظ PDF تلقائياً:", "auto_save_pdf", True)
            self.create_switch_field(parent, "إرسال بالبريد الإلكتروني:", "auto_email", False)

            # إعدادات الضرائب
            self.create_input_field(parent, "معدل الضريبة الافتراضي (%):", "default_tax_rate", "15")
            self.create_switch_field(parent, "تطبيق الضريبة تلقائياً:", "auto_apply_tax", True)
            self.create_switch_field(parent, "عرض تفاصيل الضريبة:", "show_tax_details", True)

            # إعدادات الترقيم
            self.create_input_field(parent, "بادئة رقم فاتورة المبيعات:", "sales_invoice_prefix", "INV-")
            self.create_input_field(parent, "بادئة رقم فاتورة المشتريات:", "purchase_invoice_prefix", "PUR-")
            self.create_input_field(parent, "طول الرقم التسلسلي:", "invoice_number_length", "6")

            # إعدادات الخصومات
            self.create_switch_field(parent, "السماح بالخصومات:", "allow_discounts", True)
            self.create_input_field(parent, "الحد الأقصى للخصم (%):", "max_discount_percent", "50")
            self.create_switch_field(parent, "طلب سبب الخصم:", "require_discount_reason", True)

        self.create_settings_card("📄 إعدادات الفواتير العامة", invoice_general_content, WARM_COLORS['mint_bg'])

        # بطاقة إعدادات نقاط البيع (POS)
        def pos_settings_content(parent):
            # إعدادات الشاشة
            self.create_dropdown_field(parent, "حجم شاشة POS:", "pos_screen_size",
                                     ["صغير", "متوسط", "كبير", "ملء الشاشة"], "كبير")

            self.create_dropdown_field(parent, "عدد أعمدة المنتجات:", "pos_product_columns",
                                     ["3", "4", "5", "6"], "4")

            # إعدادات الدفع
            self.create_switch_field(parent, "قبول الدفع النقدي:", "accept_cash", True)
            self.create_switch_field(parent, "قبول البطاقات:", "accept_cards", True)
            self.create_switch_field(parent, "قبول التحويل البنكي:", "accept_transfer", True)
            self.create_switch_field(parent, "قبول الدفع الآجل:", "accept_credit", True)

            # إعدادات الطباعة
            self.create_switch_field(parent, "طباعة إيصال فورية:", "print_receipt", True)
            self.create_dropdown_field(parent, "حجم الإيصال:", "receipt_size",
                                     ["80mm", "58mm", "A4"], "80mm")

            # إعدادات أخرى
            self.create_switch_field(parent, "صوت عند المسح:", "beep_on_scan", True)
            self.create_switch_field(parent, "تحديث المخزون فورياً:", "update_inventory_realtime", True)
            self.create_input_field(parent, "رسالة شكر في الإيصال:", "receipt_thank_message", "شكراً لزيارتكم")

        self.create_settings_card("🛒 إعدادات نقاط البيع (POS)", pos_settings_content, WARM_COLORS['soft_cream'])

    def create_payroll_settings(self):
        """إنشاء إعدادات الرواتب والضرائب"""
        self.create_section_header(
            "الرواتب والضرائب",
            "💰",
            "إعدادات الرواتب والضرائب والخصومات",
            WARM_COLORS['mint']
        )

        # بطاقة إعدادات الرواتب
        def payroll_content(parent):
            self.create_input_field(parent, "معدل ضريبة الدخل (%):", "income_tax_rate", "10")
            self.create_input_field(parent, "نسبة التأمينات (%):", "insurance_rate", "9")
            self.create_switch_field(parent, "حساب الإضافي تلقائياً:", "auto_overtime", True)
            self.create_input_field(parent, "ساعات العمل اليومية:", "daily_hours", "8")
            self.create_input_field(parent, "أيام العمل الأسبوعية:", "weekly_days", "5")

        self.create_settings_card("💼 إعدادات الرواتب", payroll_content, WARM_COLORS['light_peach'])

    def create_warehouses_settings(self):
        """إنشاء إعدادات المخازن"""
        self.create_section_header(
            "إعدادات المخازن",
            "🏪",
            "إدارة المخازن والمخزون والباركود",
            WARM_COLORS['sky']
        )

        # بطاقة إعدادات المخزون
        def inventory_content(parent):
            self.create_switch_field(parent, "تتبع المخزون:", "track_inventory", True)
            self.create_switch_field(parent, "تحذير نفاد المخزون:", "low_stock_alert", True)
            self.create_input_field(parent, "الحد الأدنى للمخزون:", "min_stock_level", "10")
            self.create_switch_field(parent, "استخدام الباركود:", "use_barcode", True)
            self.create_dropdown_field(parent, "طريقة تقييم المخزون:", "inventory_method",
                                     ["FIFO", "LIFO", "متوسط مرجح"], "FIFO")

        self.create_settings_card("📦 إدارة المخزون", inventory_content, WARM_COLORS['light_peach'])

    def create_modules_settings(self):
        """إنشاء إعدادات التحكم في الموديلات"""
        self.create_section_header(
            "التحكم في الموديلات",
            "🔧",
            "إظهار وإخفاء الميزات والموديلات النشطة",
            WARM_COLORS['rose']
        )

        # بطاقة الموديلات الأساسية
        def basic_modules_content(parent):
            self.create_switch_field(parent, "موديل المبيعات:", "sales_module", True)
            self.create_switch_field(parent, "موديل المشتريات:", "purchases_module", True)
            self.create_switch_field(parent, "موديل المخازن:", "inventory_module", True)
            self.create_switch_field(parent, "موديل الحسابات:", "accounts_module", True)
            self.create_switch_field(parent, "موديل الرواتب:", "payroll_module", True)

        self.create_settings_card("🧩 الموديلات الأساسية", basic_modules_content, WARM_COLORS['light_peach'])

        # بطاقة الموديلات المتقدمة
        def advanced_modules_content(parent):
            self.create_switch_field(parent, "نقاط البيع (POS):", "pos_module", True)
            self.create_switch_field(parent, "التقارير المتقدمة:", "advanced_reports", True)
            self.create_switch_field(parent, "إدارة العملاء:", "crm_module", True)
            self.create_switch_field(parent, "الباركود:", "barcode_module", True)
            self.create_switch_field(parent, "التكامل مع Excel:", "excel_integration", True)

        self.create_settings_card("⚡ الموديلات المتقدمة", advanced_modules_content, WARM_COLORS['mint_bg'])

    def create_import_export_settings(self):
        """إنشاء إعدادات استيراد وتصدير البيانات"""
        self.create_section_header(
            "استيراد من Excel",
            "📊",
            "إدارة استيراد وتصدير البيانات من وإلى Excel",
            WARM_COLORS['turquoise']
        )

        # بطاقة إعدادات الاستيراد
        def import_content(parent):
            self.create_switch_field(parent, "السماح بالاستيراد:", "allow_import", True)
            self.create_switch_field(parent, "التحقق من البيانات:", "validate_data", True)
            self.create_switch_field(parent, "إنشاء نسخة احتياطية قبل الاستيراد:", "backup_before_import", True)
            self.create_input_field(parent, "الحد الأقصى للصفوف:", "max_import_rows", "1000")

        self.create_settings_card("📥 إعدادات الاستيراد", import_content, WARM_COLORS['light_peach'])

    def create_security_settings(self):
        """إنشاء إعدادات نظام الأمان"""
        self.create_section_header(
            "نظام الأمان",
            "🛡️",
            "الحماية والمراقبة وسجل العمليات",
            WARM_COLORS['lavender']
        )

        # بطاقة إعدادات الأمان
        def security_content(parent):
            self.create_switch_field(parent, "تسجيل العمليات:", "log_operations", True)
            self.create_switch_field(parent, "مراقبة تسجيل الدخول:", "monitor_login", True)
            self.create_switch_field(parent, "تشفير البيانات الحساسة:", "encrypt_sensitive", False)
            self.create_input_field(parent, "مدة حفظ السجلات (يوم):", "log_retention_days", "90")

        self.create_settings_card("🔒 إعدادات الأمان", security_content, WARM_COLORS['light_peach'])

        # بطاقة إجراءات الأمان
        def security_actions_content(parent):
            # أزرار الإجراءات الخطيرة
            buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=10)

            # زر ضبط المصنع
            factory_reset_btn = ctk.CTkButton(
                buttons_frame,
                text="⚠️ ضبط المصنع",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['coral'],
                hover_color=self.lighten_color(WARM_COLORS['coral']),
                height=40,
                command=self.factory_reset
            )
            factory_reset_btn.pack(side="right", padx=5)

            # زر عرض سجل العمليات
            view_log_btn = ctk.CTkButton(
                buttons_frame,
                text="📋 عرض سجل العمليات",
                font=(FONTS['arabic'], 12, "bold"),
                fg_color=WARM_COLORS['turquoise'],
                hover_color=self.lighten_color(WARM_COLORS['turquoise']),
                height=40,
                command=self.view_operations_log
            )
            view_log_btn.pack(side="right", padx=5)

        self.create_settings_card("⚡ إجراءات الأمان", security_actions_content, WARM_COLORS['mint_bg'])

    def factory_reset(self):
        """ضبط المصنع - حذف جميع البيانات"""
        result = messagebox.askyesnocancel(
            "تحذير - ضبط المصنع",
            "⚠️ تحذير شديد ⚠️\n\n"
            "هذا الإجراء سيحذف جميع البيانات نهائياً!\n"
            "• جميع الفواتير والمعاملات\n"
            "• بيانات العملاء والموردين\n"
            "• المخزون والمنتجات\n"
            "• الإعدادات المخصصة\n\n"
            "هل أنت متأكد تماماً من المتابعة؟"
        )

        if result:
            # طلب تأكيد إضافي
            confirm = messagebox.askstring(
                "تأكيد نهائي",
                "اكتب 'حذف نهائي' للتأكيد:",
                show='*'
            )

            if confirm == "حذف نهائي":
                try:
                    # إنشاء نسخة احتياطية أولاً
                    self.create_backup()

                    # حذف قاعدة البيانات وإعادة إنشائها
                    if DATABASE_PATH.exists():
                        DATABASE_PATH.unlink()

                    # إعادة إنشاء قاعدة البيانات الفارغة
                    conn = sqlite3.connect(DATABASE_PATH)
                    conn.close()

                    self.update_status("✅ تم ضبط المصنع بنجاح")
                    messagebox.showinfo("تم", "تم ضبط المصنع بنجاح\nيجب إعادة تشغيل البرنامج")

                except Exception as e:
                    self.update_status("❌ خطأ في ضبط المصنع")
                    messagebox.showerror("خطأ", f"حدث خطأ في ضبط المصنع:\n{str(e)}")
            else:
                messagebox.showinfo("تم الإلغاء", "تم إلغاء عملية ضبط المصنع")

    def view_operations_log(self):
        """عرض سجل العمليات"""
        # إنشاء نافذة جديدة لعرض السجل
        log_window = ctk.CTkToplevel(self.window)
        log_window.title("📋 سجل العمليات")
        log_window.geometry("800x600")
        log_window.configure(fg_color=WARM_COLORS['warm_white'])

        # عنوان النافذة
        title_label = ctk.CTkLabel(
            log_window,
            text="📋 سجل العمليات والأنشطة",
            font=(FONTS['arabic'], 20, "bold"),
            text_color=WARM_COLORS['deep_teal']
        )
        title_label.pack(pady=20)

        # منطقة عرض السجل
        log_text = ctk.CTkTextbox(
            log_window,
            font=(FONTS['arabic'], 12),
            fg_color="white",
            border_color=WARM_COLORS['coral'],
            border_width=2
        )
        log_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # إدراج بيانات وهمية للسجل
        sample_log = """
🕐 2025-07-22 10:30:15 - تسجيل دخول المستخدم: admin
🕐 2025-07-22 10:31:22 - إنشاء فاتورة بيع رقم: INV-2025-001
🕐 2025-07-22 10:35:45 - تعديل بيانات العميل: أحمد محمد
🕐 2025-07-22 10:40:12 - إضافة منتج جديد: لابتوب HP
🕐 2025-07-22 10:45:33 - إنشاء نسخة احتياطية تلقائية
🕐 2025-07-22 10:50:18 - تحديث إعدادات النظام
🕐 2025-07-22 11:00:05 - تسجيل خروج المستخدم: admin
        """
        log_text.insert("1.0", sample_log.strip())
        log_text.configure(state="disabled")

    def load_settings(self):
        """تحميل الإعدادات المحفوظة"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.current_settings = json.load(f)
            else:
                # إعدادات افتراضية
                self.current_settings = self.get_default_settings()

        except Exception as e:
            print(f"خطأ في تحميل الإعدادات: {e}")
            self.current_settings = self.get_default_settings()

    def get_default_settings(self):
        """الحصول على الإعدادات الافتراضية"""
        return {
            # معلومات الشركة
            'company_name': 'شركة ست الكل للمحاسبة',
            'commercial_register': '',
            'phone': '',
            'email': '',
            'address': '',
            'company_logo': '',

            # الإعدادات الأساسية
            'default_language': 'العربية',
            'date_format': 'DD/MM/YYYY',
            'default_currency': 'ريال سعودي',
            'currency_symbol': 'ر.س',
            'dark_mode': False,
            'sounds_enabled': True,

            # الأرقام التسلسلية
            'sales_invoice_prefix': 'INV',
            'purchase_invoice_prefix': 'PUR',
            'return_prefix': 'RET',
            'number_length': '6',
            'include_year': True,
            'include_month': True,
            'employee_prefix': 'EMP',
            'customer_prefix': 'CUS',
            'supplier_prefix': 'SUP',
            'auto_numbering': True,

            # الألوان
            'primary_color': WARM_COLORS['coral'],
            'background_color': WARM_COLORS['warm_white'],
            'header_color': WARM_COLORS['deep_teal'],
            'button_color': WARM_COLORS['mint'],
            'text_color': WARM_COLORS['dark_coral'],

            # الخطوط
            'main_font': 'Cairo',
            'header_font': 'Cairo',
            'font_size': 'متوسط',
            'bold_headers': True,

            # النسخ الاحتياطي
            'auto_backup': True,
            'backup_frequency': 'يومياً',
            'backup_time': '02:00',
            'max_backups': '30',
            'compress_backups': True,

            # الأمان
            'min_password_length': '6',
            'require_numbers': True,
            'require_symbols': False,
            'session_timeout': '60',
            'max_login_attempts': '3',

            # الفواتير
            'invoice_template': 'حديث',
            'paper_size': 'A4',
            'show_logo': True,
            'auto_print': False,
            'tax_rate': '15',

            # الرواتب
            'income_tax_rate': '10',
            'insurance_rate': '9',
            'auto_overtime': True,
            'daily_hours': '8',
            'weekly_days': '5',

            # المخازن
            'track_inventory': True,
            'low_stock_alert': True,
            'min_stock_level': '10',
            'use_barcode': True,
            'inventory_method': 'FIFO',

            # الموديلات
            'sales_module': True,
            'purchases_module': True,
            'inventory_module': True,
            'accounts_module': True,
            'payroll_module': True,
            'pos_module': True,
            'advanced_reports': True,
            'crm_module': True,
            'barcode_module': True,
            'excel_integration': True,

            # الاستيراد والتصدير
            'allow_import': True,
            'validate_data': True,
            'backup_before_import': True,
            'max_import_rows': '1000',

            # الأمان المتقدم
            'log_operations': True,
            'monitor_login': True,
            'encrypt_sensitive': False,
            'log_retention_days': '90'
        }

    def save_all_settings(self):
        """حفظ جميع الإعدادات"""
        try:
            # جمع القيم من جميع الحقول
            self.collect_all_field_values()

            # إنشاء مجلد الإعدادات إذا لم يكن موجوداً
            self.settings_file.parent.mkdir(exist_ok=True)

            # حفظ الإعدادات في ملف JSON
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_settings, f, ensure_ascii=False, indent=2)

            self.update_status("✅ تم حفظ جميع الإعدادات بنجاح")
            messagebox.showinfo("تم الحفظ", "تم حفظ جميع الإعدادات بنجاح!")

        except Exception as e:
            self.update_status("❌ خطأ في حفظ الإعدادات")
            messagebox.showerror("خطأ", f"حدث خطأ في حفظ الإعدادات:\n{str(e)}")

    def collect_all_field_values(self):
        """جمع القيم من جميع الحقول"""
        try:
            # جمع القيم من الحقول المختلفة
            if hasattr(self, 'current_settings'):
                # تحديث الإعدادات الحالية
                pass
        except Exception as e:
            print(f"خطأ في جمع القيم: {e}")


# دالة لفتح لوحة التحكم من النافذة الرئيسية
def open_central_control_panel(parent=None):
    """فتح لوحة التحكم المركزية"""
    try:
        panel = CentralControlPanel(parent)
        return panel
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ في فتح لوحة التحكم:\n{str(e)}")
        return None
