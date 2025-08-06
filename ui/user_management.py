# -*- coding: utf-8 -*-
# cSpell:disable
"""
واجهة إدارة المستخدمين
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from auth.auth_manager import AuthManager
from themes.theme_manager import ThemeManager
from ui.window_utils import configure_window_fullscreen

class UserManagementWindow:
    """نافذة إدارة المستخدمين"""

    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.theme_manager = ThemeManager()
        self.window = None
        self.users_tree = None
        self.selected_user = None

        # متغيرات النموذج
        self.username_var = tk.StringVar()
        self.fullname_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.role_var = tk.StringVar()
        self.active_var = tk.BooleanVar()

    def show(self):
        """عرض نافذة إدارة المستخدمين"""
        if not self.auth_manager.has_permission('manage_users'):
            messagebox.showerror("خطأ", "ليس لديك صلاحية لإدارة المستخدمين")
            return

        self.create_window()
        self.load_users()

    def create_window(self):
        """إنشاء النافذة"""
        self.window = ctk.CTkToplevel(self.parent)

        # إعداد النافذة لتملأ الشاشة
        configure_window_fullscreen(self.window, "إدارة المستخدمين - برنامج ست الكل للمحاسبة")
        self.window.transient(self.parent)
        self.window.grab_set()

        # توسيط النافذة
        self.center_window()

        # إنشاء المحتوى
        self.create_content()

    def center_window(self):
        """توسيط النافذة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def create_content(self):
        """إنشاء محتوى النافذة"""
        # الإطار الرئيسي
        main_frame = self.theme_manager.create_styled_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # العنوان
        title_label = self.theme_manager.create_styled_label(
            main_frame,
            text="إدارة المستخدمين",
            font_size=18
        )
        title_label.pack(pady=(0, 20))

        # إطار المحتوى
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # الجانب الأيمن - قائمة المستخدمين
        self.create_users_list(content_frame)

        # الجانب الأيسر - نموذج المستخدم
        self.create_user_form(content_frame)

        # الأزرار السفلية
        self.create_buttons(main_frame)

    def create_users_list(self, parent):
        """إنشاء قائمة المستخدمين"""
        # إطار القائمة
        list_frame = self.theme_manager.create_styled_frame(parent, width=500)
        list_frame.pack(side="right", fill="both", expand=True, padx=(0, 10))
        list_frame.pack_propagate(False)

        # عنوان القائمة
        list_title = self.theme_manager.create_styled_label(
            list_frame,
            text="قائمة المستخدمين",
            font_size=14
        )
        list_title.pack(pady=(10, 5))

        # إطار البحث
        search_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = self.theme_manager.create_styled_entry(
            search_frame,
            placeholder_text="البحث في المستخدمين...",
            width=300
        )
        self.search_entry.pack(side="right", padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search)

        search_btn = self.theme_manager.create_styled_button(
            search_frame,
            text="بحث",
            command=self.search_users,
            button_type="secondary",
            width=80,
            height=30
        )
        search_btn.pack(side="right")

        # جدول المستخدمين
        tree_frame = ctk.CTkFrame(list_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # إنشاء Treeview
        columns = ('اسم المستخدم', 'الاسم الكامل', 'الدور', 'البريد الإلكتروني', 'الحالة')
        self.users_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        # تعيين عناوين الأعمدة
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100, anchor='center')

        # شريط التمرير
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)

        # تخطيط الجدول
        self.users_tree.pack(side="right", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # ربط الأحداث
        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        self.users_tree.bind('<Double-1>', self.on_user_double_click)

    def create_user_form(self, parent):
        """إنشاء نموذج المستخدم"""
        # إطار النموذج
        form_frame = self.theme_manager.create_styled_frame(parent, width=400)
        form_frame.pack(side="left", fill="y", padx=(10, 0))
        form_frame.pack_propagate(False)

        # عنوان النموذج
        form_title = self.theme_manager.create_styled_label(
            form_frame,
            text="بيانات المستخدم",
            font_size=14
        )
        form_title.pack(pady=(10, 20))

        # حقول النموذج
        fields = [
            ("اسم المستخدم:", self.username_var),
            ("الاسم الكامل:", self.fullname_var),
            ("البريد الإلكتروني:", self.email_var),
            ("رقم الهاتف:", self.phone_var)
        ]

        for label_text, var in fields:
            # التسمية
            label = self.theme_manager.create_styled_label(
                form_frame,
                text=label_text,
                font_size=12
            )
            label.pack(anchor="e", padx=20, pady=(10, 5))

            # حقل الإدخال
            entry = self.theme_manager.create_styled_entry(
                form_frame,
                textvariable=var,
                width=300,
                justify="right"
            )
            entry.pack(padx=20, pady=(0, 5))

        # حقل الدور
        role_label = self.theme_manager.create_styled_label(
            form_frame,
            text="الدور:",
            font_size=12
        )
        role_label.pack(anchor="e", padx=20, pady=(10, 5))

        self.role_combo = ctk.CTkComboBox(
            form_frame,
            values=["admin", "accountant", "user"],
            variable=self.role_var,
            width=300,
            state="readonly"
        )
        self.role_combo.pack(padx=20, pady=(0, 5))

        # حقل كلمة المرور
        password_label = self.theme_manager.create_styled_label(
            form_frame,
            text="كلمة المرور:",
            font_size=12
        )
        password_label.pack(anchor="e", padx=20, pady=(10, 5))

        self.password_entry = self.theme_manager.create_styled_entry(
            form_frame,
            placeholder_text="اتركه فارغاً للاحتفاظ بكلمة المرور الحالية",
            width=300,
            show="*",
            justify="right"
        )
        self.password_entry.pack(padx=20, pady=(0, 5))

        # خانة الاختيار للحالة
        self.active_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="المستخدم نشط",
            variable=self.active_var
        )
        self.active_checkbox.pack(pady=20)

        # أزرار النموذج
        form_buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_buttons_frame.pack(fill="x", padx=20, pady=10)

        # زر حفظ
        save_btn = self.theme_manager.create_styled_button(
            form_buttons_frame,
            text="حفظ",
            command=self.save_user,
            button_type="primary",
            width=120,
            height=35
        )
        save_btn.pack(side="right", padx=5)

        # زر جديد
        new_btn = self.theme_manager.create_styled_button(
            form_buttons_frame,
            text="جديد",
            command=self.new_user,
            button_type="secondary",
            width=120,
            height=35
        )
        new_btn.pack(side="right", padx=5)

        # زر حذف
        delete_btn = self.theme_manager.create_styled_button(
            form_buttons_frame,
            text="حذف",
            command=self.delete_user,
            button_type="secondary",
            width=120,
            height=35
        )
        delete_btn.pack(side="right", padx=5)

    def create_buttons(self, parent):
        """إنشاء الأزرار السفلية"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))

        # زر إغلاق
        close_btn = self.theme_manager.create_styled_button(
            buttons_frame,
            text="إغلاق",
            command=self.close_window,
            button_type="secondary",
            width=100,
            height=35
        )
        close_btn.pack(side="left")

        # زر تحديث
        refresh_btn = self.theme_manager.create_styled_button(
            buttons_frame,
            text="تحديث",
            command=self.load_users,
            button_type="secondary",
            width=100,
            height=35
        )
        refresh_btn.pack(side="left", padx=10)

    def load_users(self):
        """تحميل قائمة المستخدمين"""
        try:
            # مسح البيانات الحالية
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            # جلب المستخدمين من قاعدة البيانات
            users = self.auth_manager.db.fetch_all(
                "SELECT * FROM users ORDER BY username"
            )

            # إضافة المستخدمين للجدول
            for user in users:
                role_names = {
                    'admin': 'مدير النظام',
                    'accountant': 'محاسب',
                    'user': 'مستخدم'
                }

                status = 'نشط' if user['is_active'] else 'غير نشط'

                self.users_tree.insert('', 'end', values=(
                    user['username'],
                    user['full_name'],
                    role_names.get(user['role'], user['role']),
                    user['email'] or '',
                    status
                ), tags=(user['id'],))

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحميل المستخدمين: {e}")

    def on_user_select(self, event):
        """عند اختيار مستخدم"""
        selection = self.users_tree.selection()
        if selection:
            item = self.users_tree.item(selection[0])
            user_id = item['tags'][0]
            self.load_user_data(user_id)

    def on_user_double_click(self, event):
        """عند النقر المزدوج على مستخدم"""
        self.on_user_select(event)

    def load_user_data(self, user_id):
        """تحميل بيانات المستخدم"""
        try:
            user = self.auth_manager.db.fetch_one(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            )

            if user:
                self.selected_user = user
                self.username_var.set(user['username'])
                self.fullname_var.set(user['full_name'])
                self.email_var.set(user['email'] or '')
                self.phone_var.set(user['phone'] or '')
                self.role_var.set(user['role'])
                self.active_var.set(user['is_active'])
                self.password_entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحميل بيانات المستخدم: {e}")

    def new_user(self):
        """مستخدم جديد"""
        self.selected_user = None
        self.username_var.set('')
        self.fullname_var.set('')
        self.email_var.set('')
        self.phone_var.set('')
        self.role_var.set('user')
        self.active_var.set(True)
        self.password_entry.delete(0, 'end')

    def save_user(self):
        """حفظ المستخدم"""
        try:
            # التحقق من البيانات
            if not self.username_var.get().strip():
                messagebox.showerror("خطأ", "يرجى إدخال اسم المستخدم")
                return

            if not self.fullname_var.get().strip():
                messagebox.showerror("خطأ", "يرجى إدخال الاسم الكامل")
                return

            if not self.role_var.get():
                messagebox.showerror("خطأ", "يرجى اختيار الدور")
                return

            # كلمة المرور مطلوبة للمستخدم الجديد
            password = self.password_entry.get().strip()
            if not self.selected_user and not password:
                messagebox.showerror("خطأ", "يرجى إدخال كلمة المرور للمستخدم الجديد")
                return

            if self.selected_user:
                # تحديث مستخدم موجود
                result = self.update_existing_user(password)
            else:
                # إنشاء مستخدم جديد
                result = self.create_new_user(password)

            if result['success']:
                messagebox.showinfo("نجح", result['message'])
                self.load_users()
                self.new_user()
            else:
                messagebox.showerror("خطأ", result['message'])

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ المستخدم: {e}")

    def create_new_user(self, password):
        """إنشاء مستخدم جديد"""
        return self.auth_manager.create_user(
            username=self.username_var.get().strip(),
            password=password,
            full_name=self.fullname_var.get().strip(),
            role=self.role_var.get(),
            email=self.email_var.get().strip() or None,
            phone=self.phone_var.get().strip() or None
        )

    def update_existing_user(self, password):
        """تحديث مستخدم موجود"""
        try:
            # تحديث البيانات الأساسية
            query = '''
                UPDATE users 
                SET username=?, full_name=?, role=?, email=?, phone=?, is_active=?
                WHERE id=?
            '''
            params = (
                self.username_var.get().strip(),
                self.fullname_var.get().strip(),
                self.role_var.get(),
                self.email_var.get().strip() or None,
                self.phone_var.get().strip() or None,
                self.active_var.get(),
                self.selected_user['id']
            )

            self.auth_manager.db.execute_query(query, params)

            # تحديث كلمة المرور إذا تم إدخالها
            if password:
                password_hash = self.auth_manager.hash_password(password)
                self.auth_manager.db.execute_query(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (password_hash, self.selected_user['id'])
                )

            return {'success': True, 'message': 'تم تحديث المستخدم بنجاح'}

        except Exception as e:
            return {'success': False, 'message': f'خطأ في تحديث المستخدم: {e}'}

    def delete_user(self):
        """حذف المستخدم"""
        if not self.selected_user:
            messagebox.showwarning("تحذير", "يرجى اختيار مستخدم للحذف")
            return

        # التأكيد
        result = messagebox.askyesno(
            "تأكيد الحذف",
            f"هل تريد حذف المستخدم '{self.selected_user['full_name']}'؟"
        )

        if result:
            try:
                # حذف منطقي
                self.auth_manager.db.execute_query(
                    "UPDATE users SET is_active = 0 WHERE id = ?",
                    (self.selected_user['id'],)
                )

                messagebox.showinfo("نجح", "تم حذف المستخدم بنجاح")
                self.load_users()
                self.new_user()

            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في حذف المستخدم: {e}")

    def search_users(self):
        """البحث في المستخدمين"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_users()
            return

        try:
            # مسح البيانات الحالية
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            # البحث في المستخدمين
            users = self.auth_manager.db.fetch_all('''
                SELECT * FROM users 
                WHERE username LIKE ? OR full_name LIKE ? OR email LIKE ?
                ORDER BY username
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

            # إضافة النتائج للجدول
            for user in users:
                role_names = {
                    'admin': 'مدير النظام',
                    'accountant': 'محاسب',
                    'user': 'مستخدم'
                }

                status = 'نشط' if user['is_active'] else 'غير نشط'

                self.users_tree.insert('', 'end', values=(
                    user['username'],
                    user['full_name'],
                    role_names.get(user['role'], user['role']),
                    user['email'] or '',
                    status
                ), tags=(user['id'],))

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في البحث: {e}")

    def on_search(self, event):
        """عند الكتابة في حقل البحث"""
        # البحث التلقائي بعد توقف الكتابة
        self.window.after(500, self.search_users)

    def close_window(self):
        """إغلاق النافذة"""
        if hasattr(self, 'window') and self.window:

            self.window.destroy()
