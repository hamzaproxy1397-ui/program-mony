# -*- coding: utf-8 -*-
# cSpell:disable
"""
نافذة إدارة تصنيفات المنتجات
Categories Management Window
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk

try:
    from themes.modern_theme import MODERN_COLORS, FONTS
    from ui.window_utils import configure_window_fullscreen
except ImportError:
    MODERN_COLORS = {
        'primary': '#1f538d',
        'secondary': '#2c3e50',
        'success': '#27ae60',
        'danger': '#e74c3c',
        'error': '#e74c3c',
        'warning': '#f39c12',
        'info': '#3498db',
        'background': '#ecf0f1',
        'surface': '#ffffff',
        'text_primary': '#2c3e50',
        'text_secondary': '#7f8c8d',
        'border': '#bdc3c7'
    }
    FONTS = {'arabic': 'Arial', 'english': 'Arial'}

class CategoriesManagementWindow:
    """نافذة إدارة تصنيفات المنتجات"""

    def __init__(self, parent, db_manager=None):
        self.parent = parent
        self.db_manager = db_manager
        self.window = None
        self.current_category_id = None
        self.categories_data = []

        # إعداد النافذة
        self.create_window()
        self.load_categories_data()

    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = ctk.CTkToplevel(self.parent)

        # إعداد النافذة لتملأ الشاشة
        configure_window_fullscreen(self.window, "📂 إدارة تصنيفات المنتجات - برنامج ست الكل للمحاسبة")

        # ضبط النافذة لملء الشاشة
        self.window  # ملء الشاشة في Windows

        # للأنظمة الأخرى كبديل
        try:
            self.window  # Linux
        except:
            pass

        # كبديل احتياطي - استخدام أبعاد الشاشة الكاملة
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")

        self.window.configure(fg_color=MODERN_COLORS['background'])

        # جعل النافذة في المقدمة
        self.window.transient(self.parent)
        self.window.grab_set()

        # إنشاء المحتوى
        self.create_header()
        self.create_main_layout()

    def create_header(self):
        """إنشاء رأس النافذة"""
        header_frame = ctk.CTkFrame(self.window, height=80, fg_color=MODERN_COLORS['primary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        # الأيقونة والعنوان
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="right", padx=20, pady=15)

        title_label = ctk.CTkLabel(
            title_frame,
            text="📂 إدارة تصنيفات المنتجات",
            font=(FONTS['arabic'], 24, "bold"),
            text_color="white"
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="تنظيم وإدارة تصنيفات المنتجات بشكل هرمي",
            font=(FONTS['arabic'], 12),
            text_color="white"
        )
        subtitle_label.pack()

        # معلومات سريعة
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", padx=20, pady=15)

        self.categories_count_label = ctk.CTkLabel(
            info_frame,
            text="إجمالي التصنيفات: 0",
            font=(FONTS['arabic'], 12),
            text_color="white"
        )
        self.categories_count_label.pack()

        self.main_categories_label = ctk.CTkLabel(
            info_frame,
            text="التصنيفات الرئيسية: 0",
            font=(FONTS['arabic'], 12),
            text_color="white"
        )
        self.main_categories_label.pack()

    def create_main_layout(self):
        """إنشاء التخطيط الرئيسي"""
        # إطار المحتوى الرئيسي
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # الجانب الأيمن - نموذج إضافة/تعديل التصنيف
        self.create_category_form(main_container)

        # الجانب الأيسر - شجرة التصنيفات
        self.create_categories_tree(main_container)

    def create_category_form(self, parent):
        """إنشاء نموذج إضافة/تعديل التصنيف"""
        # إطار النموذج
        form_frame = ctk.CTkFrame(parent, width=400, fg_color=MODERN_COLORS['surface'])
        form_frame.pack(side="right", fill="y", padx=(0, 10))
        form_frame.pack_propagate(False)

        # عنوان النموذج
        form_title = ctk.CTkLabel(
            form_frame,
            text="📝 بيانات التصنيف",
            font=(FONTS['arabic'], 18, "bold"),
            text_color=MODERN_COLORS['primary']
        )
        form_title.pack(pady=(20, 10))

        # إطار الحقول
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # اسم التصنيف بالعربية
        self.create_form_field(fields_frame, "اسم التصنيف (عربي):", "name_ar", required=True)

        # اسم التصنيف بالإنجليزية
        self.create_form_field(fields_frame, "اسم التصنيف (English):", "name_en")

        # التصنيف الأب
        self.create_parent_category_field(fields_frame)

        # أزرار الإجراءات
        self.create_form_buttons(form_frame)

    def create_form_field(self, parent, label_text, field_name, required=False):
        """إنشاء حقل في النموذج"""
        # إطار الحقل
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=10)

        # التسمية
        label_text_with_required = f"{label_text} *" if required else label_text
        label = ctk.CTkLabel(
            field_frame,
            text=label_text_with_required,
            font=(FONTS['arabic'], 12, "bold" if required else "normal"),
            text_color=MODERN_COLORS['error'] if required else MODERN_COLORS['text_primary']
        )
        label.pack(anchor="e", pady=(0, 5))

        # الحقل
        entry = ctk.CTkEntry(
            field_frame,
            placeholder_text=f"أدخل {label_text}",
            font=(FONTS['arabic'], 12),
            height=35
        )
        entry.pack(fill="x", pady=(0, 5))

        # حفظ مرجع الحقل
        setattr(self, f"{field_name}_entry", entry)

        return entry

    def create_parent_category_field(self, parent):
        """إنشاء حقل التصنيف الأب"""
        # إطار الحقل
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=10)

        # التسمية
        label = ctk.CTkLabel(
            field_frame,
            text="التصنيف الأب:",
            font=(FONTS['arabic'], 12),
            text_color=MODERN_COLORS['text_primary']
        )
        label.pack(anchor="e", pady=(0, 5))

        # القائمة المنسدلة
        self.parent_category_combo = ctk.CTkComboBox(
            field_frame,
            values=["لا يوجد (تصنيف رئيسي)"],
            font=(FONTS['arabic'], 12),
            height=35
        )
        self.parent_category_combo.pack(fill="x", pady=(0, 5))
        self.parent_category_combo.set("لا يوجد (تصنيف رئيسي)")

        return self.parent_category_combo

    def create_form_buttons(self, parent):
        """إنشاء أزرار النموذج"""
        buttons_frame = ctk.CTkFrame(parent, height=80, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)
        buttons_frame.pack_propagate(False)

        # زر حفظ
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ التصنيف",
            command=self.save_category,
            fg_color=MODERN_COLORS['success'],
            width=120,
            height=40,
            font=(FONTS['arabic'], 12, "bold")
        )
        save_btn.pack(side="right", padx=5, pady=10)

        # زر تعديل
        self.edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ تعديل",
            command=self.update_category,
            fg_color=MODERN_COLORS['info'],
            width=100,
            height=40,
            font=(FONTS['arabic'], 12, "bold"),
            state="disabled"
        )
        self.edit_btn.pack(side="right", padx=5, pady=10)

        # زر جديد
        new_btn = ctk.CTkButton(
            buttons_frame,
            text="📄 جديد",
            command=self.clear_form,
            fg_color=MODERN_COLORS['primary'],
            width=100,
            height=40,
            font=(FONTS['arabic'], 12, "bold")
        )
        new_btn.pack(side="right", padx=5, pady=10)

        # زر حذف
        self.delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ حذف",
            command=self.delete_category,
            fg_color=MODERN_COLORS['error'],
            width=100,
            height=40,
            font=(FONTS['arabic'], 12, "bold"),
            state="disabled"
        )
        self.delete_btn.pack(side="left", padx=5, pady=10)

    def create_categories_tree(self, parent):
        """إنشاء شجرة التصنيفات"""
        # إطار الشجرة
        tree_frame = ctk.CTkFrame(parent, fg_color=MODERN_COLORS['surface'])
        tree_frame.pack(side="left", fill="both", expand=True)

        # عنوان الشجرة
        tree_header = ctk.CTkFrame(tree_frame, height=60, fg_color=MODERN_COLORS['primary'])
        tree_header.pack(fill="x", padx=10, pady=(10, 0))
        tree_header.pack_propagate(False)

        # عنوان
        tree_title = ctk.CTkLabel(
            tree_header,
            text="🌳 شجرة التصنيفات",
            font=(FONTS['arabic'], 16, "bold"),
            text_color="white"
        )
        tree_title.pack(side="right", padx=20, pady=15)

        # أزرار التحكم
        controls_frame = ctk.CTkFrame(tree_header, fg_color="transparent")
        controls_frame.pack(side="left", padx=20, pady=10)

        # زر توسيع الكل
        expand_btn = ctk.CTkButton(
            controls_frame,
            text="📖 توسيع الكل",
            command=self.expand_all,
            fg_color=MODERN_COLORS['info'],
            width=100,
            height=30,
            font=(FONTS['arabic'], 10)
        )
        expand_btn.pack(side="left", padx=5)

        # زر طي الكل
        collapse_btn = ctk.CTkButton(
            controls_frame,
            text="📕 طي الكل",
            command=self.collapse_all,
            fg_color=MODERN_COLORS['warning'],
            width=100,
            height=30,
            font=(FONTS['arabic'], 10)
        )
        collapse_btn.pack(side="left", padx=5)

        # زر تحديث
        refresh_btn = ctk.CTkButton(
            controls_frame,
            text="🔄 تحديث",
            command=self.refresh_tree,
            fg_color=MODERN_COLORS['success'],
            width=80,
            height=30,
            font=(FONTS['arabic'], 10)
        )
        refresh_btn.pack(side="left", padx=5)

        # إطار الشجرة الفعلي
        tree_container = ctk.CTkFrame(tree_frame, fg_color="white")
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        # إنشاء Treeview
        columns = ("id", "name_ar", "name_en", "level")

        self.categories_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="tree headings",
            height=20
        )

        # تعريف رؤوس الأعمدة
        self.categories_tree.heading("#0", text="التصنيف", anchor="e")
        self.categories_tree.heading("id", text="الرقم", anchor="center")
        self.categories_tree.heading("name_ar", text="الاسم (عربي)", anchor="center")
        self.categories_tree.heading("name_en", text="الاسم (English)", anchor="center")
        self.categories_tree.heading("level", text="المستوى", anchor="center")

        # تحديد عرض الأعمدة
        self.categories_tree.column("#0", width=200, anchor="e")
        self.categories_tree.column("id", width=80, anchor="center")
        self.categories_tree.column("name_ar", width=150, anchor="center")
        self.categories_tree.column("name_en", width=150, anchor="center")
        self.categories_tree.column("level", width=80, anchor="center")

        # شريط التمرير
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.categories_tree.yview)
        self.categories_tree.configure(yscrollcommand=scrollbar.set)

        # تخطيط الشجرة
        self.categories_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ربط الأحداث
        self.categories_tree.bind("<ButtonRelease-1>", self.on_category_select)
        self.categories_tree.bind("<Double-1>", self.on_category_double_click)
        self.categories_tree.bind("<Button-3>", self.show_context_menu)

    def load_categories_data(self):
        """تحميل بيانات التصنيفات"""
        try:
            if self.db_manager:
                # استعلام قاعدة البيانات الحقيقية
                query = """
                SELECT id, name_ar, name_en, parent_id
                FROM item_categories
                ORDER BY parent_id NULLS FIRST, name_ar
                """
                self.categories_data = self.db_manager.fetch_all(query)
            else:
                # بيانات وهمية للاختبار
                self.categories_data = self.get_sample_categories_data()

            # تحديث الشجرة والقوائم
            self.populate_categories_tree()
            self.update_parent_categories_list()
            self.update_categories_count()

        except Exception as e:
            pass
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحميل بيانات التصنيفات: {e}")

    def get_sample_categories_data(self):
        """بيانات وهمية للاختبار"""
        return [
            (1, "إلكترونيات", "Electronics", None),
            (2, "أجهزة كمبيوتر", "Computers", 1),
            (3, "لابتوب", "Laptops", 2),
            (4, "أجهزة مكتبية", "Desktop", 2),
            (5, "هواتف ذكية", "Smartphones", 1),
            (6, "ملابس", "Clothing", None),
            (7, "ملابس رجالية", "Men's Clothing", 6),
            (8, "ملابس نسائية", "Women's Clothing", 6),
            (9, "أحذية", "Shoes", 6),
            (10, "طعام ومشروبات", "Food & Beverages", None),
            (11, "مشروبات ساخنة", "Hot Beverages", 10),
            (12, "مشروبات باردة", "Cold Beverages", 10),
        ]

    def populate_categories_tree(self):
        """ملء شجرة التصنيفات"""
        # مسح الشجرة
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)

        # إنشاء خريطة للتصنيفات
        categories_map = {}
        for category in self.categories_data:
            categories_map[category[0]] = category

        # إضافة التصنيفات الرئيسية أولاً
        for category in self.categories_data:
            if category[3] is None:  # parent_id is None:
                self.add_category_to_tree("", category, categories_map, 0)

    def add_category_to_tree(self, parent_item, category, categories_map, level):
        """إضافة تصنيف للشجرة مع أطفاله"""
        # إضافة التصنيف الحالي
        item_id = self.categories_tree.insert(
            parent_item, "end",
            text=f"{'  ' * level}📁 {category[1]}",
            values=(category[0], category[1], category[2], level),
            open=True if level < 2 else False
        )

        # البحث عن التصنيفات الفرعية
        for child_category in self.categories_data:
            if child_category[3] == category[0]:  # parent_id == current category id:
                self.add_category_to_tree(item_id, child_category, categories_map, level + 1)

    def update_parent_categories_list(self):
        """تحديث قائمة التصنيفات الأب"""
        # مسح القائمة الحالية
        parent_options = ["لا يوجد (تصنيف رئيسي)"]

        # إضافة التصنيفات
        for category in self.categories_data:
            if category[0] != self.current_category_id:  # تجنب التصنيف الحالي:
                parent_options.append(f"{category[1]} ({category[0]})")

        # تحديث القائمة المنسدلة
        self.parent_category_combo.configure(values=parent_options)

    def update_categories_count(self):
        """تحديث عداد التصنيفات"""
        total_categories = len(self.categories_data)
        main_categories = sum(1 for cat in self.categories_data if cat[3] is None)

        self.categories_count_label.configure(text=f"إجمالي التصنيفات: {total_categories}")
        self.main_categories_label.configure(text=f"التصنيفات الرئيسية: {main_categories}")

    def on_category_select(self, event):
        """عند تحديد تصنيف"""
        selected_item = self.categories_tree.selection()
        if selected_item:
            item_values = self.categories_tree.item(selected_item[0])['values']
            if item_values:
                self.current_category_id = item_values[0]
                self.fill_form_with_category_data(item_values)

                # تفعيل أزرار التعديل والحذف
                self.edit_btn.configure(state="normal")
                self.delete_btn.configure(state="normal")

    def fill_form_with_category_data(self, category_values):
        """ملء النموذج ببيانات التصنيف"""
        # مسح النموذج
        self.clear_form()

        # ملء البيانات
        self.name_ar_entry.insert(0, category_values[1])
        self.name_en_entry.insert(0, category_values[2])

        # تحديد التصنيف الأب
        category_id = category_values[0]
        parent_category = None
        for cat in self.categories_data:
            if cat[0] == category_id:
                parent_category = cat[3]
                break

        if parent_category:
            for cat in self.categories_data:
                if cat[0] == parent_category:
                    self.parent_category_combo.set(f"{cat[1]} ({cat[0]})")
                    break
        else:
            self.parent_category_combo.set("لا يوجد (تصنيف رئيسي)")

    def clear_form(self):
        """مسح النموذج"""
        self.name_ar_entry.delete(0, "end")
        self.name_en_entry.delete(0, "end")
        self.parent_category_combo.set("لا يوجد (تصنيف رئيسي)")

        self.current_category_id = None
        self.edit_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")

    def save_category(self):
        """حفظ تصنيف جديد"""
        # التحقق من البيانات
        if not self.validate_form():
            return

        try:
            # جمع البيانات
            name_ar = self.name_ar_entry.get().strip()
            name_en = self.name_en_entry.get().strip()
            parent_id = self.get_parent_id_from_combo()

            if self.db_manager:
                # حفظ في قاعدة البيانات
                query = """
                INSERT INTO item_categories (name_ar, name_en, parent_id)
                VALUES (?, ?, ?)
                """
                self.db_manager.execute_query(query, (name_ar, name_en, parent_id))
                messagebox.showinfo("نجح", "تم حفظ التصنيف بنجاح")
            else:
                # محاكاة الحفظ
                messagebox.showinfo("نجح", "تم حفظ التصنيف بنجاح (وضع الاختبار)")

            # تحديث البيانات
            self.load_categories_data()
            self.clear_form()

        except Exception as e:
            pass
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ التصنيف: {e}")

    def update_category(self):
        """تعديل التصنيف المحدد"""
        if not self.current_category_id:
            messagebox.showwarning("تحذير", "يرجى تحديد تصنيف للتعديل")
            return

        # التحقق من البيانات
        if not self.validate_form():
            return

        try:
            # جمع البيانات
            name_ar = self.name_ar_entry.get().strip()
            name_en = self.name_en_entry.get().strip()
            parent_id = self.get_parent_id_from_combo()

            # التحقق من عدم جعل التصنيف أب لنفسه
            if parent_id == self.current_category_id:
                messagebox.showerror("خطأ", "لا يمكن جعل التصنيف أب لنفسه")
                return

            if self.db_manager:
                # تحديث في قاعدة البيانات
                query = """
                UPDATE item_categories
                SET name_ar = ?, name_en = ?, parent_id = ?
                WHERE id = ?
                """
                self.db_manager.execute_query(query, (name_ar, name_en, parent_id, self.current_category_id))
                messagebox.showinfo("نجح", "تم تعديل التصنيف بنجاح")
            else:
                # محاكاة التعديل
                messagebox.showinfo("نجح", "تم تعديل التصنيف بنجاح (وضع الاختبار)")

            # تحديث البيانات
            self.load_categories_data()
            self.clear_form()

        except Exception as e:
            pass
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تعديل التصنيف: {e}")

    def delete_category(self):
        """حذف التصنيف المحدد"""
        if not self.current_category_id:
            messagebox.showwarning("تحذير", "يرجى تحديد تصنيف للحذف")
            return

        # التحقق من وجود تصنيفات فرعية
        has_children = any(cat[3] == self.current_category_id for cat in self.categories_data)
        if has_children:
            messagebox.showerror("خطأ", "لا يمكن حذف تصنيف يحتوي على تصنيفات فرعية")
            return

        # تأكيد الحذف
        result = messagebox.askyesno(
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف التصنيف؟\n\nهذا الإجراء لا يمكن التراجع عنه."
        )

        if result:
            try:
                if self.db_manager:
                    # حذف من قاعدة البيانات
                    query = "DELETE FROM item_categories WHERE id = ?"
                    self.db_manager.execute_query(query, (self.current_category_id,))
                    messagebox.showinfo("نجح", "تم حذف التصنيف بنجاح")
                else:
                    # محاكاة الحذف
                    messagebox.showinfo("نجح", "تم حذف التصنيف بنجاح (وضع الاختبار)")

                # تحديث البيانات
                self.load_categories_data()
                self.clear_form()

            except Exception as e:
                pass
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في حذف التصنيف: {e}")

    def validate_form(self):
        """التحقق من صحة البيانات"""
        if not self.name_ar_entry.get().strip():
            messagebox.showerror("خطأ", "اسم التصنيف بالعربية مطلوب")
            return False
        return True

    def get_parent_id_from_combo(self):
        """الحصول على معرف التصنيف الأب من القائمة المنسدلة"""
        selected = self.parent_category_combo.get()
        if selected == "لا يوجد (تصنيف رئيسي)":
            return None

        # استخراج المعرف من النص
        try:
            parent_id = int(selected.split("(")[-1].split(")")[0])
            return parent_id
        except:
            return None

    def expand_all(self):
        """توسيع جميع العقد"""
        def expand_item(item):
            self.categories_tree.item(item, open=True)
            for child in self.categories_tree.get_children(item):
                expand_item(child)

        for item in self.categories_tree.get_children():
            expand_item(item)

    def collapse_all(self):
        """طي جميع العقد"""
        def collapse_item(item):
            self.categories_tree.item(item, open=False)
            for child in self.categories_tree.get_children(item):
                collapse_item(child)

        for item in self.categories_tree.get_children():
            collapse_item(item)

    def refresh_tree(self):
        """تحديث الشجرة"""
        self.load_categories_data()
        messagebox.showinfo("تحديث", "تم تحديث شجرة التصنيفات بنجاح")

    def on_category_double_click(self, event):
        """عند النقر المزدوج على تصنيف"""
        self.on_category_select(event)

    def show_context_menu(self, event):
        """عرض القائمة السياقية"""
        # إنشاء قائمة سياقية
        context_menu = tk.Menu(self.window, tearoff=0)
        context_menu.add_command(label="إضافة تصنيف فرعي", command=self.add_subcategory)
        context_menu.add_command(label="تعديل التصنيف", command=self.update_category)
        context_menu.add_command(label="حذف التصنيف", command=self.delete_category)
        context_menu.add_separator()
        context_menu.add_command(label="توسيع الفرع", command=self.expand_selected)
        context_menu.add_command(label="طي الفرع", command=self.collapse_selected)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def add_subcategory(self):
        """إضافة تصنيف فرعي للتصنيف المحدد"""
        selected_item = self.categories_tree.selection()
        if selected_item:
            item_values = self.categories_tree.item(selected_item[0])['values']
            if item_values:
                # مسح النموذج وتحديد التصنيف الأب
                self.clear_form()
                category_name = item_values[1]
                category_id = item_values[0]
                self.parent_category_combo.set(f"{category_name} ({category_id})")
                self.name_ar_entry.focus()

    def expand_selected(self):
        """توسيع التصنيف المحدد"""
        selected_item = self.categories_tree.selection()
        if selected_item:
            self.categories_tree.item(selected_item[0], open=True)

    def collapse_selected(self):
        """طي التصنيف المحدد"""
        selected_item = self.categories_tree.selection()
        if selected_item:
            self.categories_tree.item(selected_item[0], open=False)

    def close_window(self):
        """إغلاق النافذة"""
        if hasattr(self, 'window') and self.window:

            self.window.destroy()
