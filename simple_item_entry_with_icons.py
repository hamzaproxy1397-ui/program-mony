#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدخال الأصناف المبسط مع الأيقونات المحسنة
نسخة مبسطة لعرض الأيقونات الجميلة
"""

import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from datetime import datetime


class SimpleItemEntryWithIcons:
    """نافذة إدخال الأصناف المبسطة مع الأيقونات"""
    
    def __init__(self):
        # إعداد الأيقونات أولاً
        self.setup_icons()
        
        # إنشاء النافذة الرئيسية
        self.create_main_window()
        
        # إنشاء الواجهة
        self.create_interface()
        
        # بيانات مؤقتة
        self.items = []
        
    def setup_icons(self):
        """إعداد الأيقونات"""
        self.icons = {
            'new': '📄',
            'save': '💾',
            'delete': '🗑️',
            'search': '🔍',
            'edit': '✏️',
            'copy': '📋',
            'paste': '📌',
            'import': '📥',
            'export': '📤',
            'settings': '⚙️',
            'help': '❓',
            'refresh': '🔄',
            'add': '➕',
            'category': '📁',
            'unit': '📏',
            'barcode': '🏷️',
            'analytics': '📊',
            'ai': '🤖'
        }

    def get_icon(self, icon_name):
        """الحصول على أيقونة"""
        return self.icons.get(icon_name, '●')

    def create_main_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Tk()
        self.window.title("🎨 نظام إدخال الأصناف مع الأيقونات المحسنة")
        self.window.geometry("1200x800")
        self.window.configure(bg='#F5F5F5')
        
        # تعيين الخط
        self.window.option_add('*Font', 'Arial 11')

    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        # شريط الأدوات
        self.create_toolbar()
        
        # المحتوى الرئيسي
        self.create_main_content()
        
        # شريط الحالة
        self.create_status_bar()

    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        self.toolbar_frame = ttk.Frame(self.window)
        self.toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # أزرار شريط الأدوات
        self.create_toolbar_button("جديد", "new", self.new_item)
        self.create_toolbar_button("حفظ", "save", self.save_item)
        self.create_toolbar_button("حذف", "delete", self.delete_item)
        
        # فاصل
        ttk.Separator(self.toolbar_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.create_toolbar_button("بحث", "search", self.search_items)
        self.create_toolbar_button("تحديث", "refresh", self.refresh_list)
        
        # فاصل
        ttk.Separator(self.toolbar_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.create_toolbar_button("استيراد", "import", self.import_data)
        self.create_toolbar_button("تصدير", "export", self.export_data)
        
        # فاصل
        ttk.Separator(self.toolbar_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.create_toolbar_button("ذكاء اصطناعي", "ai", self.ai_features)
        self.create_toolbar_button("تحليلات", "analytics", self.analytics)

    def create_toolbar_button(self, text, icon_name, command):
        """إنشاء زر في شريط الأدوات مع أيقونة"""
        emoji_icon = self.get_icon(icon_name)
        button_text = f"{emoji_icon} {text}"
        
        button = ttk.Button(self.toolbar_frame, text=button_text, command=command)
        button.pack(side=tk.LEFT, padx=2)
        return button

    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        # إطار رئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # تبويبات
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # تبويب المعلومات الأساسية
        self.create_basic_info_tab()
        
        # تبويب الذكاء الاصطناعي
        self.create_ai_tab()
        
        # تبويب التحليلات
        self.create_analytics_tab()

    def create_basic_info_tab(self):
        """إنشاء تبويب المعلومات الأساسية"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text=f"{self.get_icon('edit')} المعلومات الأساسية")
        
        # نموذج الإدخال
        form_frame = ttk.LabelFrame(basic_frame, text="بيانات الصنف")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # حقول الإدخال
        ttk.Label(form_frame, text="اسم الصنف:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="الوصف:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # أزرار إضافية
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text=f"{self.get_icon('category')} إضافة فئة", 
                  command=self.add_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text=f"{self.get_icon('unit')} إضافة وحدة", 
                  command=self.add_unit).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text=f"{self.get_icon('barcode')} توليد باركود", 
                  command=self.generate_barcode).pack(side=tk.LEFT, padx=5)

    def create_ai_tab(self):
        """إنشاء تبويب الذكاء الاصطناعي"""
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text=f"{self.get_icon('ai')} الذكاء الاصطناعي")
        
        # أزرار الذكاء الاصطناعي
        ai_buttons_frame = ttk.LabelFrame(ai_frame, text="ميزات الذكاء الاصطناعي")
        ai_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(ai_buttons_frame, text=f"{self.get_icon('ai')} اقتراح التصنيف", 
                  command=self.suggest_category).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(ai_buttons_frame, text="💰 توقع السعر", 
                  command=self.predict_price).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(ai_buttons_frame, text=f"{self.get_icon('search')} كشف التكرار", 
                  command=self.detect_duplicates).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(ai_buttons_frame, text="⭐ تقييم الجودة", 
                  command=self.evaluate_quality).pack(fill=tk.X, padx=5, pady=5)

    def create_analytics_tab(self):
        """إنشاء تبويب التحليلات"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text=f"{self.get_icon('analytics')} التحليلات")
        
        # أزرار التحليلات
        analytics_buttons_frame = ttk.LabelFrame(analytics_frame, text="التحليلات والإحصائيات")
        analytics_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(analytics_buttons_frame, text="📈 اتجاه المبيعات", 
                  command=self.sales_trend).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(analytics_buttons_frame, text="🥧 توزيع الفئات", 
                  command=self.category_distribution).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(analytics_buttons_frame, text="💹 تحليل الربحية", 
                  command=self.profitability_analysis).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(analytics_buttons_frame, text="📦 حالة المخزون", 
                  command=self.inventory_status).pack(fill=tk.X, padx=5, pady=5)

    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_frame = ttk.Frame(self.window)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🎨 جاهز - واجهة محسنة بالأيقونات")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)

    # وظائف الأزرار
    def new_item(self):
        messagebox.showinfo("جديد", f"{self.get_icon('new')} إنشاء صنف جديد")
        
    def save_item(self):
        messagebox.showinfo("حفظ", f"{self.get_icon('save')} تم حفظ البيانات")
        
    def delete_item(self):
        messagebox.showinfo("حذف", f"{self.get_icon('delete')} تم حذف الصنف")
        
    def search_items(self):
        messagebox.showinfo("بحث", f"{self.get_icon('search')} البحث في الأصناف")
        
    def refresh_list(self):
        messagebox.showinfo("تحديث", f"{self.get_icon('refresh')} تم تحديث القائمة")
        
    def import_data(self):
        messagebox.showinfo("استيراد", f"{self.get_icon('import')} استيراد البيانات")
        
    def export_data(self):
        messagebox.showinfo("تصدير", f"{self.get_icon('export')} تصدير البيانات")
        
    def ai_features(self):
        messagebox.showinfo("ذكاء اصطناعي", f"{self.get_icon('ai')} ميزات الذكاء الاصطناعي")
        
    def analytics(self):
        messagebox.showinfo("تحليلات", f"{self.get_icon('analytics')} التحليلات والإحصائيات")
        
    def add_category(self):
        messagebox.showinfo("فئة", f"{self.get_icon('category')} إضافة فئة جديدة")
        
    def add_unit(self):
        messagebox.showinfo("وحدة", f"{self.get_icon('unit')} إضافة وحدة جديدة")
        
    def generate_barcode(self):
        messagebox.showinfo("باركود", f"{self.get_icon('barcode')} توليد باركود")
        
    def suggest_category(self):
        messagebox.showinfo("اقتراح", f"{self.get_icon('ai')} اقتراح التصنيف")
        
    def predict_price(self):
        messagebox.showinfo("توقع", "💰 توقع السعر")
        
    def detect_duplicates(self):
        messagebox.showinfo("كشف", f"{self.get_icon('search')} كشف التكرار")
        
    def evaluate_quality(self):
        messagebox.showinfo("تقييم", "⭐ تقييم الجودة")
        
    def sales_trend(self):
        messagebox.showinfo("اتجاه", "📈 اتجاه المبيعات")
        
    def category_distribution(self):
        messagebox.showinfo("توزيع", "🥧 توزيع الفئات")
        
    def profitability_analysis(self):
        messagebox.showinfo("ربحية", "💹 تحليل الربحية")
        
    def inventory_status(self):
        messagebox.showinfo("مخزون", "📦 حالة المخزون")

    def run(self):
        """تشغيل التطبيق"""
        self.window.mainloop()


def main():
    """تشغيل النافذة"""
    print("🎨 تشغيل نظام إدخال الأصناف المبسط مع الأيقونات...")
    
    try:
        app = SimpleItemEntryWithIcons()
        app.run()
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {e}")
        messagebox.showerror("خطأ", f"فشل في تشغيل النظام: {e}")


if __name__ == "__main__":
    main()
