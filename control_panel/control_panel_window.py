# -*- coding: utf-8 -*-
"""
نافذة لوحة التحكم الرئيسية
Main Control Panel Window
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع للاستيراد
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
    from PIL import Image
except ImportError as e:
    print(f"خطأ في استيراد المكتبات: {e}")
    sys.exit(1)

from core.settings_manager import settings_manager

class ControlPanelWindow:
    """نافذة لوحة التحكم والإعدادات الشاملة"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.current_page = None
        self.pages = {}
        self.setup_window()
        self.create_interface()
        self.load_current_settings()
    
    def setup_window(self):
        """إعداد النافذة الأساسية"""
        self.window = ctk.CTkToplevel(self.parent) if self.parent else ctk.CTk()
        self.window.title("لوحة التحكم والإعدادات - برنامج ست الكل للمحاسبة")
        self.window.geometry("1200x800")
        self.window.minsize(1000, 700)
        
        # تعيين الأيقونة إذا كانت متوفرة
        try:
            if os.path.exists("assets/logo/222555.png"):
                icon_image = Image.open("assets/logo/222555.png")
                icon_photo = ctk.CTkImage(light_image=icon_image, size=(32, 32))
                self.window.iconphoto(False, icon_photo)
        except:
            pass
        
        # تعيين الثيم
        theme = settings_manager.get_setting("general", "theme", "light")
        ctk.set_appearance_mode(theme)
        
        # جعل النافذة في المقدمة
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # توسيط النافذة
        self.center_window()
    
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        # الإطار الرئيسي
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # الشريط العلوي
        self.create_header(main_frame)
        
        # المحتوى الرئيسي
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # القائمة الجانبية
        self.create_sidebar(content_frame)
        
        # منطقة المحتوى
        self.create_content_area(content_frame)
        
        # الشريط السفلي
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """إنشاء الشريط العلوي"""
        header_frame = ctk.CTkFrame(parent, height=80, fg_color="#1f538d")
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # العنوان الرئيسي
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ لوحة التحكم والإعدادات",
            font=("Cairo", 24, "bold"),
            text_color="white"
        )
        title_label.pack(side="right", padx=20, pady=20)
        
        # زر الإغلاق
        close_btn = ctk.CTkButton(
            header_frame,
            text="✕ إغلاق",
            width=100,
            height=40,
            font=("Cairo", 14),
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.close_window
        )
        close_btn.pack(side="left", padx=20, pady=20)
        
        # زر الحفظ
        save_btn = ctk.CTkButton(
            header_frame,
            text="💾 حفظ",
            width=100,
            height=40,
            font=("Cairo", 14),
            fg_color="#28a745",
            hover_color="#218838",
            command=self.save_all_settings
        )
        save_btn.pack(side="left", padx=(0, 10), pady=20)
    
    def create_sidebar(self, parent):
        """إنشاء القائمة الجانبية"""
        sidebar_frame = ctk.CTkFrame(parent, width=280, fg_color="#2b2b2b")
        sidebar_frame.pack(side="right", fill="y", padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # عنوان القائمة
        sidebar_title = ctk.CTkLabel(
            sidebar_frame,
            text="أقسام الإعدادات",
            font=("Cairo", 18, "bold"),
            text_color="white"
        )
        sidebar_title.pack(pady=(20, 10))
        
        # قائمة الأقسام
        self.menu_items = [
            ("🏠", "الإعدادات العامة", "general"),
            ("🏢", "بيانات الشركة", "company"),
            ("💼", "المحاسبة", "accounting"),
            ("📦", "إدارة المخزون", "inventory"),
            ("🧾", "إعدادات الفوترة", "invoicing"),
            ("👥", "إدارة المستخدمين", "users"),
            ("🔐", "الأمان", "security"),
            ("🌐", "الشبكة والتكامل", "network"),
            ("📊", "التقارير والطباعة", "reports")
        ]
        
        self.menu_buttons = {}
        for icon, text, key in self.menu_items:
            btn = ctk.CTkButton(
                sidebar_frame,
                text=f"{icon} {text}",
                width=250,
                height=50,
                font=("Cairo", 14),
                fg_color="transparent",
                hover_color="#404040",
                anchor="e",
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(pady=5, padx=10)
            self.menu_buttons[key] = btn
        
        # زر استعادة الإعدادات الافتراضية
        reset_btn = ctk.CTkButton(
            sidebar_frame,
            text="🔄 استعادة الافتراضية",
            width=250,
            height=40,
            font=("Cairo", 12),
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.reset_to_defaults
        )
        reset_btn.pack(side="bottom", pady=20, padx=10)
    
    def create_content_area(self, parent):
        """إنشاء منطقة المحتوى"""
        self.content_frame = ctk.CTkFrame(parent, fg_color="#f8f9fa")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # إنشاء الصفحات
        self.create_pages()
        
        # عرض الصفحة الأولى
        self.show_page("general")
    
    def create_footer(self, parent):
        """إنشاء الشريط السفلي"""
        footer_frame = ctk.CTkFrame(parent, height=50, fg_color="#6c757d")
        footer_frame.pack(fill="x", pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        # معلومات الحالة
        status_label = ctk.CTkLabel(
            footer_frame,
            text="جاهز للتحديث | آخر حفظ: لم يتم الحفظ بعد",
            font=("Cairo", 12),
            text_color="white"
        )
        status_label.pack(side="right", padx=20, pady=15)
        
        # معلومات الإصدار
        version_label = ctk.CTkLabel(
            footer_frame,
            text="الإصدار 1.0.0",
            font=("Cairo", 12),
            text_color="white"
        )
        version_label.pack(side="left", padx=20, pady=15)
    
    def create_pages(self):
        """إنشاء صفحات الإعدادات"""
        # سيتم إنشاء الصفحات ديناميكياً
        for icon, text, key in self.menu_items:
            page_frame = ctk.CTkScrollableFrame(
                self.content_frame,
                fg_color="transparent"
            )
            self.pages[key] = page_frame
            
            # عنوان الصفحة
            page_title = ctk.CTkLabel(
                page_frame,
                text=f"{icon} {text}",
                font=("Cairo", 22, "bold"),
                text_color="#1f538d"
            )
            page_title.pack(anchor="e", padx=20, pady=(20, 10))
            
            # محتوى الصفحة (سيتم إضافته لاحقاً)
            self.create_page_content(page_frame, key)
    
    def create_page_content(self, parent, page_key):
        """إنشاء محتوى الصفحة حسب النوع"""
        try:
            if page_key == "general":
                from .settings_pages.general_settings import GeneralSettingsPage
                GeneralSettingsPage(parent)
            elif page_key == "company":
                from .settings_pages.company_settings import CompanySettingsPage
                CompanySettingsPage(parent)
            elif page_key == "accounting":
                from .settings_pages.accounting_settings import AccountingSettingsPage
                AccountingSettingsPage(parent)
            else:
                # محتوى مؤقت للصفحات الأخرى
                content_label = ctk.CTkLabel(
                    parent,
                    text=f"محتوى صفحة {page_key} قيد التطوير...",
                    font=("Cairo", 16),
                    text_color="#6c757d"
                )
                content_label.pack(padx=20, pady=50)
        except Exception as e:
            error_label = ctk.CTkLabel(
                parent,
                text=f"خطأ في تحميل الصفحة: {e}",
                font=("Cairo", 14),
                text_color="#dc3545"
            )
            error_label.pack(padx=20, pady=50)
    
    def show_page(self, page_key):
        """عرض صفحة محددة"""
        # إخفاء الصفحة الحالية
        if self.current_page:
            self.pages[self.current_page].pack_forget()
        
        # عرض الصفحة الجديدة
        if page_key in self.pages:
            self.pages[page_key].pack(fill="both", expand=True)
            self.current_page = page_key
            
            # تحديث ألوان الأزرار
            self.update_menu_buttons(page_key)
    
    def update_menu_buttons(self, active_key):
        """تحديث ألوان أزرار القائمة"""
        for key, btn in self.menu_buttons.items():
            if key == active_key:
                btn.configure(fg_color="#1f538d")
            else:
                btn.configure(fg_color="transparent")
    
    def load_current_settings(self):
        """تحميل الإعدادات الحالية"""
        # سيتم تنفيذها عند إنشاء صفحات الإعدادات
        pass
    
    def save_all_settings(self):
        """حفظ جميع الإعدادات"""
        try:
            if settings_manager.save_settings():
                messagebox.showinfo("نجح", "تم حفظ الإعدادات بنجاح!")
            else:
                messagebox.showerror("خطأ", "فشل في حفظ الإعدادات!")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ الإعدادات: {e}")
    
    def reset_to_defaults(self):
        """إعادة تعيين الإعدادات للقيم الافتراضية"""
        result = messagebox.askyesno(
            "تأكيد",
            "هل أنت متأكد من إعادة تعيين جميع الإعدادات للقيم الافتراضية؟\nسيتم فقدان جميع التخصيصات الحالية."
        )
        if result:
            settings_manager.reset_to_defaults()
            messagebox.showinfo("تم", "تم إعادة تعيين الإعدادات للقيم الافتراضية!")
            self.load_current_settings()
    
    def close_window(self):
        """إغلاق النافذة"""
        self.window.destroy()
    
    def show(self):
        """عرض النافذة"""
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()

# دالة للاختبار
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = ControlPanelWindow()
    app.show()
    app.window.mainloop()
