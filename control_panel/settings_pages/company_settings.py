# -*- coding: utf-8 -*-
"""
صفحة إعدادات الشركة
Company Settings Page
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع للاستيراد
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
    from PIL import Image
except ImportError as e:
    print(f"خطأ في استيراد المكتبات: {e}")
    sys.exit(1)

from core.settings_manager import settings_manager

class CompanySettingsPage:
    """صفحة إعدادات الشركة"""
    
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.widgets = {}
        self.logo_image = None
        self.create_content()
        self.load_settings()
    
    def create_content(self):
        """إنشاء محتوى الصفحة"""
        # قسم المعلومات الأساسية
        self.create_basic_info_section()
        
        # قسم الشعار
        self.create_logo_section()
        
        # قسم معلومات الاتصال
        self.create_contact_section()
        
        # قسم المعلومات القانونية
        self.create_legal_section()
    
    def create_basic_info_section(self):
        """قسم المعلومات الأساسية"""
        # إطار القسم
        basic_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        basic_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            basic_frame,
            text="🏢 المعلومات الأساسية",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(basic_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # اسم الشركة
        name_label = ctk.CTkLabel(
            grid_frame,
            text="اسم الشركة:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        name_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['company_name'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل اسم الشركة"
        )
        self.widgets['company_name'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # العنوان
        address_label = ctk.CTkLabel(
            grid_frame,
            text="العنوان:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        address_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['address'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل عنوان الشركة"
        )
        self.widgets['address'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # المدينة
        city_label = ctk.CTkLabel(
            grid_frame,
            text="المدينة:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        city_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['city'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل المدينة"
        )
        self.widgets['city'].grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        # الدولة
        country_label = ctk.CTkLabel(
            grid_frame,
            text="الدولة:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        country_label.grid(row=3, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['country'] = ctk.CTkComboBox(
            grid_frame,
            values=[
                "المملكة العربية السعودية", "الإمارات العربية المتحدة", "الكويت",
                "قطر", "البحرين", "عمان", "الأردن", "لبنان", "مصر", "العراق"
            ],
            width=300,
            font=("Cairo", 12)
        )
        self.widgets['country'].grid(row=3, column=0, sticky="w", padx=10, pady=5)
    
    def create_logo_section(self):
        """قسم الشعار"""
        # إطار القسم
        logo_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        logo_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            logo_frame,
            text="🎨 شعار الشركة",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # محتوى القسم
        content_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # عرض الشعار الحالي
        self.logo_display_frame = ctk.CTkFrame(
            content_frame,
            width=200,
            height=150,
            fg_color="#f8f9fa",
            corner_radius=10
        )
        self.logo_display_frame.pack(side="right", padx=10)
        self.logo_display_frame.pack_propagate(False)
        
        self.logo_display_label = ctk.CTkLabel(
            self.logo_display_frame,
            text="لا يوجد شعار",
            font=("Cairo", 12),
            text_color="#6c757d"
        )
        self.logo_display_label.pack(expand=True)
        
        # أزرار إدارة الشعار
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(side="right", fill="y", padx=10)
        
        browse_btn = ctk.CTkButton(
            buttons_frame,
            text="📁 تصفح الشعار",
            width=150,
            height=35,
            font=("Cairo", 12),
            fg_color="#007bff",
            hover_color="#0056b3",
            command=self.browse_logo
        )
        browse_btn.pack(pady=5)
        
        remove_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ إزالة الشعار",
            width=150,
            height=35,
            font=("Cairo", 12),
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.remove_logo
        )
        remove_btn.pack(pady=5)
        
        # مسار الشعار
        path_label = ctk.CTkLabel(
            content_frame,
            text="مسار الشعار:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        path_label.pack(anchor="e", pady=(10, 5))
        
        self.widgets['logo_path'] = ctk.CTkEntry(
            content_frame,
            width=400,
            height=35,
            font=("Cairo", 12),
            placeholder_text="مسار ملف الشعار",
            state="readonly"
        )
        self.widgets['logo_path'].pack(anchor="e", pady=(0, 10))
    
    def create_contact_section(self):
        """قسم معلومات الاتصال"""
        # إطار القسم
        contact_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        contact_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            contact_frame,
            text="📞 معلومات الاتصال",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(contact_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # رقم الهاتف
        phone_label = ctk.CTkLabel(
            grid_frame,
            text="رقم الهاتف:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        phone_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['phone'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل رقم الهاتف"
        )
        self.widgets['phone'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # البريد الإلكتروني
        email_label = ctk.CTkLabel(
            grid_frame,
            text="البريد الإلكتروني:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        email_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['email'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل البريد الإلكتروني"
        )
        self.widgets['email'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # الموقع الإلكتروني
        website_label = ctk.CTkLabel(
            grid_frame,
            text="الموقع الإلكتروني:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        website_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['website'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل الموقع الإلكتروني"
        )
        self.widgets['website'].grid(row=2, column=0, sticky="w", padx=10, pady=5)
    
    def create_legal_section(self):
        """قسم المعلومات القانونية"""
        # إطار القسم
        legal_frame = ctk.CTkFrame(self.parent, fg_color="#ffffff", corner_radius=10)
        legal_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        title_label = ctk.CTkLabel(
            legal_frame,
            text="⚖️ المعلومات القانونية",
            font=("Cairo", 18, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(anchor="e", padx=20, pady=(15, 10))
        
        # شبكة الإعدادات
        grid_frame = ctk.CTkFrame(legal_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # الرقم الضريبي
        tax_label = ctk.CTkLabel(
            grid_frame,
            text="الرقم الضريبي:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        tax_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['tax_number'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل الرقم الضريبي"
        )
        self.widgets['tax_number'].grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # السجل التجاري
        cr_label = ctk.CTkLabel(
            grid_frame,
            text="السجل التجاري:",
            font=("Cairo", 14),
            text_color="#333333"
        )
        cr_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        self.widgets['commercial_register'] = ctk.CTkEntry(
            grid_frame,
            width=300,
            height=35,
            font=("Cairo", 12),
            placeholder_text="أدخل رقم السجل التجاري"
        )
        self.widgets['commercial_register'].grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # أزرار الحفظ والإلغاء
        buttons_frame = ctk.CTkFrame(legal_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ بيانات الشركة",
            width=180,
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
        company_settings = settings_manager.get_section("company")
        
        # تحميل القيم في الواجهة
        self.widgets['company_name'].insert(0, company_settings.get("name", ""))
        self.widgets['address'].insert(0, company_settings.get("address", ""))
        self.widgets['city'].insert(0, company_settings.get("city", ""))
        self.widgets['country'].set(company_settings.get("country", "المملكة العربية السعودية"))
        self.widgets['phone'].insert(0, company_settings.get("phone", ""))
        self.widgets['email'].insert(0, company_settings.get("email", ""))
        self.widgets['website'].insert(0, company_settings.get("website", ""))
        self.widgets['tax_number'].insert(0, company_settings.get("tax_number", ""))
        self.widgets['commercial_register'].insert(0, company_settings.get("commercial_register", ""))
        
        # تحميل الشعار
        logo_path = company_settings.get("logo_path", "")
        if logo_path:
            self.widgets['logo_path'].configure(state="normal")
            self.widgets['logo_path'].delete(0, "end")
            self.widgets['logo_path'].insert(0, logo_path)
            self.widgets['logo_path'].configure(state="readonly")
            self.load_logo_preview(logo_path)
    
    def browse_logo(self):
        """تصفح واختيار شعار جديد"""
        file_path = filedialog.askopenfilename(
            title="اختر شعار الشركة",
            filetypes=[
                ("ملفات الصور", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("جميع الملفات", "*.*")
            ]
        )
        
        if file_path:
            self.widgets['logo_path'].configure(state="normal")
            self.widgets['logo_path'].delete(0, "end")
            self.widgets['logo_path'].insert(0, file_path)
            self.widgets['logo_path'].configure(state="readonly")
            self.load_logo_preview(file_path)
    
    def remove_logo(self):
        """إزالة الشعار"""
        self.widgets['logo_path'].configure(state="normal")
        self.widgets['logo_path'].delete(0, "end")
        self.widgets['logo_path'].configure(state="readonly")
        
        # إزالة معاينة الشعار
        self.logo_display_label.configure(image=None, text="لا يوجد شعار")
        self.logo_image = None
    
    def load_logo_preview(self, logo_path):
        """تحميل معاينة الشعار"""
        try:
            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                # تغيير حجم الصورة للمعاينة
                image.thumbnail((180, 130), Image.Resampling.LANCZOS)
                self.logo_image = ctk.CTkImage(light_image=image, size=image.size)
                self.logo_display_label.configure(image=self.logo_image, text="")
            else:
                self.logo_display_label.configure(image=None, text="الملف غير موجود")
        except Exception as e:
            self.logo_display_label.configure(image=None, text="خطأ في تحميل الصورة")
            print(f"خطأ في تحميل الشعار: {e}")
    
    def save_settings(self):
        """حفظ إعدادات الشركة"""
        try:
            # جمع البيانات من الواجهة
            company_data = {
                "name": self.widgets['company_name'].get(),
                "address": self.widgets['address'].get(),
                "city": self.widgets['city'].get(),
                "country": self.widgets['country'].get(),
                "phone": self.widgets['phone'].get(),
                "email": self.widgets['email'].get(),
                "website": self.widgets['website'].get(),
                "tax_number": self.widgets['tax_number'].get(),
                "commercial_register": self.widgets['commercial_register'].get(),
                "logo_path": self.widgets['logo_path'].get()
            }
            
            # حفظ الإعدادات
            settings_manager.set_section("company", company_data)
            
            if settings_manager.save_settings():
                messagebox.showinfo("نجح", "تم حفظ بيانات الشركة بنجاح!")
            else:
                messagebox.showerror("خطأ", "فشل في حفظ بيانات الشركة!")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ بيانات الشركة: {e}")
    
    def reset_settings(self):
        """إعادة تعيين إعدادات الشركة للقيم الافتراضية"""
        result = messagebox.askyesno(
            "تأكيد",
            "هل أنت متأكد من إعادة تعيين بيانات الشركة للقيم الافتراضية؟"
        )
        if result:
            # مسح جميع الحقول
            for widget_name, widget in self.widgets.items():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
                elif isinstance(widget, ctk.CTkComboBox):
                    widget.set("")
            
            # إعادة تعيين القسم
            settings_manager.reset_section("company")
            self.load_settings()
            messagebox.showinfo("تم", "تم إعادة تعيين بيانات الشركة!")
