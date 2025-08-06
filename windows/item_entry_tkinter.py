# -*- coding: utf-8 -*-
"""
نافذة إدخال الأصناف - إصدار Tkinter
Professional Item Entry Window - Tkinter Version
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.inventory_manager import InventoryManager
from core.item_code_generator import ItemCodeGenerator
from core.validation_engine import ValidationEngine
from models.item_model import ItemModel

class ItemEntryTkinter:
    """نافذة إدخال الأصناف باستخدام Tkinter"""
    
    def __init__(self, parent=None, item_id=None):
        self.parent = parent
        self.item_id = item_id
        self.image_path = None
        
        # تهيئة المدراء
        self.inventory_manager = InventoryManager()
        self.code_generator = ItemCodeGenerator()
        self.validator = ValidationEngine()
        
        # إنشاء النافذة
        self.create_window()
        self.create_widgets()
        self.load_data()
        
        # تحميل بيانات الصنف للتعديل
        if self.item_id:
            self.load_item_data(self.item_id)
    
    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("إدخال الأصناف - نظام المحاسبة")

        # تكوين النافذة لملء الشاشة مع قابلية التحكم
        self.window.configure(bg='#f8f9fa')
        self.window.state('zoomed')  # ملء الشاشة في Windows

        # تمكين تغيير الحجم
        self.window.resizable(True, True)

        # تعيين الحد الأدنى لحجم النافذة
        self.window.minsize(800, 600)

        # جعل النافذة في المقدمة
        if self.parent:
            self.window.transient(self.parent)
            self.window.grab_set()

        # ربط مفاتيح التحكم
        self.bind_window_controls()

    def bind_window_controls(self):
        """ربط مفاتيح التحكم في النافذة"""
        # F11 أو Escape للتبديل بين ملء الشاشة والنافذة العادية
        self.window.bind('<F11>', self.toggle_fullscreen)
        self.window.bind('<Escape>', self.toggle_fullscreen)

        # Ctrl+S للحفظ السريع
        self.window.bind('<Control-s>', lambda e: self.save_item())

        # Ctrl+Q للإغلاق
        self.window.bind('<Control-q>', lambda e: self.close_window())

        # Alt+F4 للإغلاق (Windows)
        self.window.bind('<Alt-F4>', lambda e: self.close_window())

        # تركيز النافذة
        self.window.focus_set()

    def toggle_fullscreen(self, event=None):
        """التبديل بين ملء الشاشة والنافذة العادية"""
        current_state = self.window.state()

        if current_state == 'zoomed':
            # تغيير إلى نافذة عادية
            self.window.state('normal')
            self.window.geometry("1000x800")
            self.center_window()
            print("🔲 تم التبديل إلى النافذة العادية")
        else:
            # تغيير إلى ملء الشاشة
            self.window.state('zoomed')
            print("🔳 تم التبديل إلى ملء الشاشة")

    def minimize_window(self):
        """تصغير النافذة"""
        self.window.iconify()
        print("🔽 تم تصغير النافذة")

    def maximize_window(self):
        """تكبير النافذة"""
        self.window.state('zoomed')
        print("🔳 تم تكبير النافذة")

    def center_window(self):
        """تمركز النافذة في الشاشة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # إطار رئيسي مع شريط تمرير
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # شريط العنوان
        self.create_header(main_frame)
        
        # إطار المحتوى مع شريط تمرير
        canvas = tk.Canvas(main_frame, bg='#f8f9fa')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط شريط التمرير
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # إنشاء الأقسام
        self.create_basic_info_section(scrollable_frame)
        self.create_price_section(scrollable_frame)
        self.create_image_section(scrollable_frame)
        self.create_button_section(scrollable_frame)
        
        # ربط عجلة الماوس بالتمرير
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_header(self, parent):
        """إنشاء شريط العنوان"""
        header_frame = tk.Frame(parent, bg='#2980b9', height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        # العنوان الرئيسي
        title_text = "📦 إدخال صنف جديد" if not self.item_id else "✏️ تعديل الصنف"
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=("Cairo", 18, "bold"),
            bg='#2980b9',
            fg='white'
        )
        title_label.pack(pady=(15, 5))

        # إطار أزرار التحكم
        controls_frame = tk.Frame(header_frame, bg='#2980b9')
        controls_frame.pack(pady=(0, 10))

        # زر تبديل ملء الشاشة
        fullscreen_btn = tk.Button(
            controls_frame,
            text="🔳 ملء الشاشة",
            command=self.toggle_fullscreen,
            bg='#3498db',
            fg='white',
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        fullscreen_btn.pack(side=tk.LEFT, padx=5)

        # زر تصغير
        minimize_btn = tk.Button(
            controls_frame,
            text="🔽 تصغير",
            command=self.minimize_window,
            bg='#f39c12',
            fg='white',
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        minimize_btn.pack(side=tk.LEFT, padx=5)

        # معلومات التحكم
        controls_label = tk.Label(
            header_frame,
            text="F11/Escape: تبديل ملء الشاشة | Ctrl+S: حفظ | Ctrl+Q: إغلاق",
            font=("Arial", 9),
            bg='#2980b9',
            fg='#ecf0f1'
        )
        controls_label.pack(pady=(5, 5))
    
    def create_basic_info_section(self, parent):
        """إنشاء قسم المعلومات الأساسية"""
        # إطار المعلومات الأساسية
        basic_frame = ttk.LabelFrame(parent, text="المعلومات الأساسية", padding=15)
        basic_frame.pack(fill=tk.X, pady=10)
        
        # اسم الصنف
        ttk.Label(basic_frame, text="اسم الصنف *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.item_name_var = tk.StringVar()
        self.item_name_entry = ttk.Entry(basic_frame, textvariable=self.item_name_var, width=40)
        self.item_name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        # رمز الصنف
        ttk.Label(basic_frame, text="رمز الصنف *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.item_code_var = tk.StringVar()
        self.item_code_entry = ttk.Entry(basic_frame, textvariable=self.item_code_var, width=40)
        self.item_code_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        # زر توليد الرمز
        generate_btn = ttk.Button(basic_frame, text="توليد", command=self.generate_code)
        generate_btn.grid(row=1, column=2, pady=5, padx=(5, 0))
        
        # التصنيف الرئيسي
        ttk.Label(basic_frame, text="التصنيف الرئيسي *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.main_category_var = tk.StringVar()
        self.main_category_combo = ttk.Combobox(basic_frame, textvariable=self.main_category_var, width=37)
        self.main_category_combo.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        self.main_category_combo.bind('<<ComboboxSelected>>', self.on_main_category_changed)
        
        # التصنيف الفرعي
        ttk.Label(basic_frame, text="التصنيف الفرعي:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.sub_category_var = tk.StringVar()
        self.sub_category_combo = ttk.Combobox(basic_frame, textvariable=self.sub_category_var, width=37)
        self.sub_category_combo.grid(row=3, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        # وحدة القياس
        ttk.Label(basic_frame, text="وحدة القياس *:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.unit_var = tk.StringVar()
        self.unit_combo = ttk.Combobox(basic_frame, textvariable=self.unit_var, width=37)
        self.unit_combo.grid(row=4, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        # الكمية الابتدائية
        ttk.Label(basic_frame, text="الكمية الابتدائية:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.initial_quantity_var = tk.IntVar()
        self.initial_quantity_spin = ttk.Spinbox(basic_frame, from_=0, to=999999, textvariable=self.initial_quantity_var, width=37)
        self.initial_quantity_spin.grid(row=5, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        # الوصف
        ttk.Label(basic_frame, text="الوصف:").grid(row=6, column=0, sticky=tk.W+tk.N, pady=5)
        self.description_text = tk.Text(basic_frame, height=3, width=40)
        self.description_text.grid(row=6, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        # تكوين الأعمدة
        basic_frame.columnconfigure(1, weight=1)
    
    def create_price_section(self, parent):
        """إنشاء قسم الأسعار"""
        price_frame = ttk.LabelFrame(parent, text="الأسعار والتكلفة", padding=15)
        price_frame.pack(fill=tk.X, pady=10)
        
        # التكلفة
        ttk.Label(price_frame, text="التكلفة:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cost_var = tk.DoubleVar()
        self.cost_spin = ttk.Spinbox(price_frame, from_=0.0, to=999999.99, increment=0.01, textvariable=self.cost_var, width=20)
        self.cost_spin.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.cost_spin.bind('<KeyRelease>', self.calculate_profit)
        
        # سعر البيع
        ttk.Label(price_frame, text="سعر البيع *:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.selling_price_var = tk.DoubleVar()
        self.selling_price_spin = ttk.Spinbox(price_frame, from_=0.01, to=999999.99, increment=0.01, textvariable=self.selling_price_var, width=20)
        self.selling_price_spin.grid(row=0, column=3, sticky=tk.W, pady=5, padx=(10, 0))
        self.selling_price_spin.bind('<KeyRelease>', self.calculate_profit)
        
        # نسبة الربح
        ttk.Label(price_frame, text="نسبة الربح:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.profit_label = tk.Label(price_frame, text="0.00%", fg='#27ae60', font=("Arial", 10, "bold"))
        self.profit_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # نوع الضريبة
        ttk.Label(price_frame, text="نوع الضريبة:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.tax_var = tk.StringVar()
        self.tax_combo = ttk.Combobox(price_frame, textvariable=self.tax_var, width=25)
        self.tax_combo['values'] = ["معفى من الضريبة", "15% ضريبة القيمة المضافة", "5% ضريبة خاصة"]
        self.tax_combo.current(1)  # افتراضي 15%
        self.tax_combo.grid(row=1, column=3, sticky=tk.W, pady=5, padx=(10, 0))
    
    def create_image_section(self, parent):
        """إنشاء قسم الصورة"""
        image_frame = ttk.LabelFrame(parent, text="صورة الصنف", padding=15)
        image_frame.pack(fill=tk.X, pady=10)
        
        # إطار الصورة
        self.image_label = tk.Label(image_frame, text="لا توجد صورة\n📷", width=20, height=8, 
                                   bg='#f8f9fa', relief=tk.RIDGE, bd=2)
        self.image_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # أزرار الصورة
        image_buttons_frame = tk.Frame(image_frame, bg='#f8f9fa')
        image_buttons_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        upload_btn = ttk.Button(image_buttons_frame, text="📁 تحميل صورة", command=self.upload_image)
        upload_btn.pack(pady=5)
        
        clear_image_btn = ttk.Button(image_buttons_frame, text="🗑️ حذف الصورة", command=self.clear_image)
        clear_image_btn.pack(pady=5)
    
    def create_button_section(self, parent):
        """إنشاء قسم الأزرار"""
        button_frame = tk.Frame(parent, bg='#f8f9fa')
        button_frame.pack(fill=tk.X, pady=20)
        
        # إطار الأزرار
        buttons_container = tk.Frame(button_frame, bg='#f8f9fa')
        buttons_container.pack()
        
        # زر الحفظ
        save_btn = tk.Button(buttons_container, text="💾 حفظ", command=self.save_item,
                           bg='#27ae60', fg='white', font=("Arial", 10, "bold"),
                           width=12, height=2)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # زر الإلغاء
        cancel_btn = tk.Button(buttons_container, text="❌ إلغاء", command=self.close_window,
                             bg='#e74c3c', fg='white', font=("Arial", 10, "bold"),
                             width=12, height=2)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # زر المسح
        clear_btn = tk.Button(buttons_container, text="🗑️ مسح", command=self.clear_form,
                            bg='#f39c12', fg='white', font=("Arial", 10, "bold"),
                            width=12, height=2)
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def load_data(self):
        """تحميل البيانات الأساسية"""
        # تحميل التصنيفات
        categories = self.inventory_manager.get_categories()
        self.main_category_combo['values'] = categories.get('main', [])
        
        # تحميل وحدات القياس
        units = self.inventory_manager.get_units()
        self.unit_combo['values'] = units
    
    def on_main_category_changed(self, event=None):
        """عند تغيير التصنيف الرئيسي"""
        category = self.main_category_var.get()
        if category:
            sub_categories = self.inventory_manager.get_sub_categories(category)
            self.sub_category_combo['values'] = sub_categories
            self.sub_category_combo.set('')
    
    def generate_code(self):
        """توليد رمز الصنف"""
        main_cat = self.main_category_var.get()
        sub_cat = self.sub_category_var.get()
        code = self.code_generator.generate_code(main_cat, sub_cat)
        self.item_code_var.set(code)
    
    def calculate_profit(self, event=None):
        """حساب نسبة الربح"""
        try:
            cost = self.cost_var.get()
            selling_price = self.selling_price_var.get()
            
            if cost > 0:
                profit_margin = ((selling_price - cost) / cost) * 100
                self.profit_label.config(text=f"{profit_margin:.2f}%")
                
                # تغيير اللون حسب النسبة
                if profit_margin > 50:
                    self.profit_label.config(fg='#e67e22')  # برتقالي
                elif profit_margin < 10:
                    self.profit_label.config(fg='#e74c3c')  # أحمر
                else:
                    self.profit_label.config(fg='#27ae60')  # أخضر
            else:
                self.profit_label.config(text="0.00%", fg='#7f8c8d')
        except:
            self.profit_label.config(text="0.00%", fg='#7f8c8d')
    
    def upload_image(self):
        """تحميل صورة"""
        file_path = filedialog.askopenfilename(
            title="اختر صورة الصنف",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            try:
                # تحميل وعرض الصورة
                image = Image.open(file_path)
                image = image.resize((150, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo  # حفظ مرجع
                self.image_path = file_path
                
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في تحميل الصورة: {str(e)}")
    
    def clear_image(self):
        """حذف الصورة"""
        self.image_label.config(image="", text="لا توجد صورة\n📷")
        self.image_label.image = None
        self.image_path = None
    
    def validate_form(self):
        """التحقق من صحة النموذج"""
        errors = []
        
        if not self.item_name_var.get().strip():
            errors.append("اسم الصنف مطلوب")
        
        if not self.item_code_var.get().strip():
            errors.append("رمز الصنف مطلوب")
        
        if not self.main_category_var.get():
            errors.append("التصنيف الرئيسي مطلوب")
        
        if not self.unit_var.get():
            errors.append("وحدة القياس مطلوبة")
        
        if self.selling_price_var.get() <= 0:
            errors.append("سعر البيع يجب أن يكون أكبر من صفر")
        
        return errors
    
    def save_item(self):
        """حفظ الصنف"""
        # التحقق من صحة البيانات
        errors = self.validate_form()
        if errors:
            messagebox.showerror("خطأ في البيانات", "\n".join(errors))
            return
        
        try:
            # إنشاء بيانات الصنف
            item_data = {
                'name': self.item_name_var.get().strip(),
                'code': self.item_code_var.get().strip(),
                'main_category': self.main_category_var.get(),
                'sub_category': self.sub_category_var.get(),
                'unit': self.unit_var.get(),
                'initial_quantity': self.initial_quantity_var.get(),
                'cost': self.cost_var.get(),
                'selling_price': self.selling_price_var.get(),
                'tax_type': self.tax_var.get(),
                'description': self.description_text.get("1.0", tk.END).strip(),
                'image_path': self.image_path,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # حفظ الصنف
            if self.item_id:
                success = self.inventory_manager.update_item(self.item_id, item_data)
                message = "تم تحديث الصنف بنجاح"
            else:
                success = self.inventory_manager.add_item(item_data)
                message = "تم حفظ الصنف بنجاح"
            
            if success:
                messagebox.showinfo("نجح الحفظ", message)
                self.close_window()
            else:
                messagebox.showerror("خطأ", "فشل في حفظ الصنف")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {str(e)}")
    
    def clear_form(self):
        """مسح النموذج"""
        if messagebox.askyesno("تأكيد المسح", "هل أنت متأكد من مسح جميع البيانات؟"):
            self.item_name_var.set("")
            self.item_code_var.set("")
            self.main_category_var.set("")
            self.sub_category_var.set("")
            self.unit_var.set("")
            self.initial_quantity_var.set(0)
            self.cost_var.set(0.0)
            self.selling_price_var.set(0.0)
            self.tax_var.set("15% ضريبة القيمة المضافة")
            self.description_text.delete("1.0", tk.END)
            self.clear_image()
    
    def load_item_data(self, item_id):
        """تحميل بيانات صنف للتعديل"""
        item_data = self.inventory_manager.get_item(item_id)
        if item_data:
            self.item_name_var.set(item_data.get('name', ''))
            self.item_code_var.set(item_data.get('code', ''))
            self.main_category_var.set(item_data.get('main_category', ''))
            self.sub_category_var.set(item_data.get('sub_category', ''))
            self.unit_var.set(item_data.get('unit', ''))
            self.initial_quantity_var.set(item_data.get('initial_quantity', 0))
            self.cost_var.set(item_data.get('cost', 0.0))
            self.selling_price_var.set(item_data.get('selling_price', 0.0))
            self.tax_var.set(item_data.get('tax_type', ''))
            self.description_text.insert("1.0", item_data.get('description', ''))
            
            # تحميل الصورة
            image_path = item_data.get('image_path')
            if image_path and os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    image = image.resize((150, 120), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo, text="")
                    self.image_label.image = photo
                    self.image_path = image_path
                except:
                    pass
    
    def close_window(self):
        """إغلاق النافذة"""
        self.window.destroy()
    
    def show(self):
        """عرض النافذة"""
        self.window.mainloop()


if __name__ == "__main__":
    app = ItemEntryTkinter()
    app.show()
