# -*- coding: utf-8 -*-
# cSpell:disable
"""
نافذة المبيعات
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from themes.modern_theme import MODERN_COLORS, FONTS
from database.hybrid_database_manager import HybridDatabaseManager
from ui.window_utils import configure_window_fullscreen

class SalesWindow:
    def __init__(self, parent, sales_manager=None):
        self.parent = parent
        self.window = None

        # استخدام مدير المبيعات الممرر أو إنشاء واحد جديد
        if sales_manager:
            self.sales_manager = sales_manager
            self.db_manager = None
        else:
            try:
                self.db_manager = HybridDatabaseManager()
                self.sales_manager = self.db_manager.sales_manager
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في تهيئة مدير المبيعات: {e}")
                self.db_manager = None
                self.sales_manager = None

        # جلب المنتجات من قاعدة البيانات
        self.products = self.load_products()

        self.create_window()

    def load_products(self):
        """جلب المنتجات من قاعدة البيانات"""
        try:
            if self.db_manager:
                products = self.db_manager.get_all_products()
                return {product['id']: product for product in products}
            elif self.sales_manager and hasattr(self.sales_manager, 'get_all_products'):
                products = self.sales_manager.get_all_products()
                return {product['id']: product for product in products}
            else:
                # الطريقة القديمة للتوافق
                from database.products_manager import ProductsManager
                from database.database_manager import DatabaseManager

                db_manager = DatabaseManager()
                products_manager = ProductsManager(db_manager)
                products = products_manager.get_all_products()

                return {product['id']: product for product in products}
        except Exception as e:
            print(f"خطأ في جلب المنتجات: {e}")
            return {}

    def create_window(self):
        """إنشاء نافذة المبيعات"""
        self.window = ctk.CTkToplevel(self.parent)

        # إعداد النافذة لتملأ الشاشة
        configure_window_fullscreen(self.window, "نظام المبيعات - برنامج ست الكل للمحاسبة")
        self.window.configure(fg_color=MODERN_COLORS['background'])

        # جعل النافذة في المقدمة
        self.window.transient(self.parent)
        self.window.grab_set()

        # إنشاء المحتوى
        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """إنشاء رأس النافذة"""
        header_frame = ctk.CTkFrame(self.window, height=80, fg_color=MODERN_COLORS['primary'])
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)

        # عنوان النافذة
        title_label = ctk.CTkLabel(
            header_frame,
            text="🛒 نظام المبيعات",
            font=(FONTS['arabic'], 24, "bold"),
            text_color="white"
        )
        title_label.pack(side="right", padx=20, pady=20)

        # أيقونة نقطة البيع المحسنة في الوسط
        pos_button = ctk.CTkButton(
            header_frame,
            text="🏪 نقطة البيع المحسنة",
            font=(FONTS['arabic'], 16, "bold"),
            fg_color=MODERN_COLORS['success'],
            hover_color=MODERN_COLORS['success_hover'],
            text_color="white",
            width=200,
            height=40,
            command=self.open_enhanced_pos
        )
        pos_button.pack(side="top", pady=20)

        # تاريخ اليوم
        date_label = ctk.CTkLabel(
            header_frame,
            text=f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}",
            font=(FONTS['arabic'], 14),
            text_color="white"
        )
        date_label.pack(side="left", padx=20, pady=20)

    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # إطار معلومات الفاتورة
        self.create_invoice_info(main_frame)

        # إطار الأصناف
        self.create_items_section(main_frame)

        # إطار الإجماليات
        self.create_totals_section(main_frame)

    def create_invoice_info(self, parent):
        """إنشاء قسم معلومات الفاتورة"""
        info_frame = ctk.CTkFrame(parent, height=120)
        info_frame.pack(fill="x", pady=(0, 10))
        info_frame.pack_propagate(False)

        # العنوان
        title = ctk.CTkLabel(
            info_frame,
            text="معلومات الفاتورة",
            font=(FONTS['arabic'], 16, "bold"),
            text_color=MODERN_COLORS['text_primary']
        )
        title.pack(pady=(10, 5))

        # إطار الحقول
        fields_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=5)

        # الصف الأول
        row1 = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)

        # رقم الفاتورة
        ctk.CTkLabel(row1, text="رقم الفاتورة:", font=(FONTS['arabic'], 12)).pack(side="right", padx=10)
        self.invoice_number = ctk.CTkEntry(row1, width=150, placeholder_text="تلقائي")
        self.invoice_number.pack(side="right", padx=10)

        # اسم العميل
        ctk.CTkLabel(row1, text="اسم العميل:", font=(FONTS['arabic'], 12)).pack(side="right", padx=10)
        self.customer_name = ctk.CTkEntry(row1, width=200, placeholder_text="أدخل اسم العميل")
        self.customer_name.pack(side="right", padx=10)

    def create_items_section(self, parent):
        """إنشاء قسم الأصناف"""
        items_frame = ctk.CTkFrame(parent)
        items_frame.pack(fill="both", expand=True, pady=(0, 10))

        # العنوان
        title = ctk.CTkLabel(
            items_frame,
            text="أصناف الفاتورة",
            font=(FONTS['arabic'], 16, "bold"),
            text_color=MODERN_COLORS['text_primary']
        )
        title.pack(pady=(10, 5))

        # إطار إدخال الصنف
        input_frame = ctk.CTkFrame(items_frame, height=60)
        input_frame.pack(fill="x", padx=20, pady=5)
        input_frame.pack_propagate(False)

        # حقول الإدخال
        ctk.CTkLabel(input_frame, text="اسم الصنف:", font=(FONTS['arabic'], 12)).pack(side="right", padx=10, pady=15)
        self.item_name = ctk.CTkEntry(input_frame, width=150, placeholder_text="اسم الصنف")
        self.item_name.pack(side="right", padx=5, pady=15)

        # ربط دالة الاقتراح مع حقل اسم المنتج
        self.item_name.bind('<KeyRelease>', self.suggest_products)

        ctk.CTkLabel(input_frame, text="الكمية:", font=(FONTS['arabic'], 12)).pack(side="right", padx=10, pady=15)
        self.item_quantity = ctk.CTkEntry(input_frame, width=80, placeholder_text="الكمية")
        self.item_quantity.pack(side="right", padx=5, pady=15)

        ctk.CTkLabel(input_frame, text="السعر:", font=(FONTS['arabic'], 12)).pack(side="right", padx=10, pady=15)
        self.item_price = ctk.CTkEntry(input_frame, width=100, placeholder_text="السعر")
        self.item_price.pack(side="right", padx=5, pady=15)

        # زر الإضافة
        add_btn = ctk.CTkButton(
            input_frame,
            text="إضافة",
            width=80,
            command=self.add_item,
            fg_color=MODERN_COLORS['success']
        )
        add_btn.pack(side="right", padx=10, pady=15)

        # زر نقطة البيع
        pos_btn = ctk.CTkButton(
            input_frame,
            text="🛒 نقطة البيع",
            width=120,
            command=self.open_pos,
            fg_color=MODERN_COLORS['info']
        )
        pos_btn.pack(side="left", padx=10, pady=15)

        # جدول الأصناف
        self.create_items_table(items_frame)

    def create_items_table(self, parent):
        """إنشاء جدول الأصناف"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # إنشاء Treeview
        columns = ("item", "quantity", "price", "total")
        self.items_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        # تعريف الأعمدة
        self.items_tree.heading("item", text="اسم الصنف")
        self.items_tree.heading("quantity", text="الكمية")
        self.items_tree.heading("price", text="السعر")
        self.items_tree.heading("total", text="الإجمالي")

        # تحديد عرض الأعمدة
        self.items_tree.column("item", width=200)
        self.items_tree.column("quantity", width=100)
        self.items_tree.column("price", width=100)
        self.items_tree.column("total", width=100)

        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)

        # تخطيط الجدول
        self.items_tree.pack(side="right", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

    def create_totals_section(self, parent):
        """إنشاء قسم الإجماليات"""
        totals_frame = ctk.CTkFrame(parent, height=100)
        totals_frame.pack(fill="x", pady=(0, 10))
        totals_frame.pack_propagate(False)

        # العنوان
        title = ctk.CTkLabel(
            totals_frame,
            text="الإجماليات",
            font=(FONTS['arabic'], 16, "bold"),
            text_color=MODERN_COLORS['text_primary']
        )
        title.pack(pady=(10, 5))

        # إطار الإجماليات
        totals_content = ctk.CTkFrame(totals_frame, fg_color="transparent")
        totals_content.pack(fill="x", padx=20, pady=5)

        # الإجمالي الفرعي
        subtotal_frame = ctk.CTkFrame(totals_content, fg_color="transparent")
        subtotal_frame.pack(side="right", padx=20)

        ctk.CTkLabel(subtotal_frame, text="الإجمالي:", font=(FONTS['arabic'], 14, "bold")).pack(side="right", padx=10)
        self.total_label = ctk.CTkLabel(subtotal_frame, text="0.00 ريال", font=(FONTS['arabic'], 14, "bold"))
        self.total_label.pack(side="right", padx=10)

    def create_footer(self):
        """إنشاء تذييل النافذة"""
        footer_frame = ctk.CTkFrame(self.window, height=60, fg_color="transparent")
        footer_frame.pack(fill="x", padx=10, pady=(0, 10))
        footer_frame.pack_propagate(False)

        # أزرار العمليات
        save_btn = ctk.CTkButton(
            footer_frame,
            text="💾 حفظ الفاتورة",
            width=120,
            command=self.save_invoice,
            fg_color=MODERN_COLORS['success']
        )
        save_btn.pack(side="right", padx=10, pady=15)

        print_btn = ctk.CTkButton(
            footer_frame,
            text="🖨️ طباعة",
            width=100,
            command=self.print_invoice,
            fg_color=MODERN_COLORS['info']
        )
        print_btn.pack(side="right", padx=10, pady=15)

        close_btn = ctk.CTkButton(
            footer_frame,
            text="❌ إغلاق",
            width=100,
            command=self.close_window,
            fg_color=MODERN_COLORS['error']
        )
        close_btn.pack(side="left", padx=10, pady=15)

    def add_item(self):
        """إضافة صنف جديد"""
        try:
            name = self.item_name.get().strip()
            quantity = float(self.item_quantity.get())
            price = float(self.item_price.get())

            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم الصنف")
                return

            # البحث عن المنتج في قاعدة البيانات
            product_id = None
            for pid, product in self.products.items():
                if product['name'].lower() == name.lower():
                    product_id = pid
                    # استخدام سعر البيع من قاعدة البيانات إذا لم يتم تعديل السعر
                    if price == 0:
                        price = product['selling_price']
                    break

            total = quantity * price

            # إضافة إلى الجدول مع معرف المنتج
            item_id = self.items_tree.insert("", "end", values=(name, quantity, price, f"{total:.2f}"))

            # حفظ معرف المنتج مع العنصر
            if product_id:
                self.items_tree.set(item_id, "product_id", product_id)

            # مسح الحقول
            self.item_name.delete(0, "end")
            self.item_quantity.delete(0, "end")
            self.item_price.delete(0, "end")

            # تحديث الإجمالي
            self.update_total()

        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للكمية والسعر")

    def update_total(self):
        """تحديث الإجمالي"""
        total = 0
        for item in self.items_tree.get_children():
            values = self.items_tree.item(item)['values']
            total += float(values[3])

        self.total_label.configure(text=f"{total:.2f} ريال")

    def save_invoice(self):
        """حفظ الفاتورة باستخدام SalesManager"""
        try:
            # التحقق من وجود مدير المبيعات
            if not self.sales_manager:
                messagebox.showerror("خطأ", "مدير المبيعات غير متاح")
                return

            # التحقق من البيانات الأساسية
            customer = self.customer_name.get().strip()
            if not customer:
                messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
                return

            if not self.items_tree.get_children():
                messagebox.showerror("خطأ", "يرجى إضافة أصناف للفاتورة")
                return

            # جمع بيانات الأصناف
            items = []
            total_amount = 0

            for item_id in self.items_tree.get_children():
                values = self.items_tree.item(item_id)['values']
                item_name = values[0]
                quantity = float(values[1])
                price = float(values[2])
                item_total = float(values[3])

                # محاولة الحصول على معرف المنتج
                product_id = None
                try:
                    product_id = self.items_tree.set(item_id, "product_id")
                    if product_id:
                        product_id = int(product_id)
                except:
                    # البحث عن المنتج بالاسم
                    for pid, product in self.products.items():
                        if product['name'].lower() == item_name.lower():
                            product_id = pid
                            break

                items.append({
                    'product_id': product_id,
                    'name': item_name,
                    'quantity': quantity,
                    'price': price
                })

                total_amount += item_total

            # التحقق من إمكانية تحديث المخزون
            can_update_stock = all(item.get('product_id') for item in items)

            # معالجة البيع باستخدام SalesManager
            result = self.sales_manager.process_sale(
                customer_name=customer,
                items=items,
                total_amount=total_amount,
                payment_status='pending',
                notes=f'فاتورة من نافذة المبيعات - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                update_stock=can_update_stock  # تحديث المخزون إذا كانت جميع المنتجات لها معرف
            )

            if result['success']:
                # إعداد رسالة النجاح
                success_message = f"تم حفظ الفاتورة بنجاح!\n"
                success_message += f"رقم الفاتورة: {result['invoice_number']}\n"
                success_message += f"المبلغ الإجمالي: {result['net_amount']:.2f} ل.س"

                # إضافة معلومات تحديث المخزون
                if result.get('inventory_updated'):
                    success_message += f"\nتم تحديث مخزون {len(result['updated_products'])} منتج"
                elif can_update_stock:
                    success_message += "\nتم تحديث المخزون تلقائياً"
                else:
                    success_message += "\nتنبيه: لم يتم تحديث المخزون (منتجات غير مسجلة)"

                messagebox.showinfo("نجح", success_message)

                # مسح البيانات بعد الحفظ الناجح
                self.clear_form()

            else:
                messagebox.showerror("خطأ", f"فشل في حفظ الفاتورة:\n{result['message']}")

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ الفاتورة:\n{str(e)}")

    def clear_form(self):
        """مسح النموذج بعد الحفظ"""
        try:
            # مسح حقول الإدخال
            self.customer_name.delete(0, "end")
            self.item_name.delete(0, "end")
            self.item_quantity.delete(0, "end")
            self.item_price.delete(0, "end")

            # مسح جدول الأصناف
            for item in self.items_tree.get_children():
                self.items_tree.delete(item)

            # إعادة تعيين الإجمالي
            self.total_label.configure(text="0.00 ل.س")

        except Exception as e:
            print(f"خطأ في مسح النموذج: {e}")

    def suggest_products(self, event=None):
        """اقتراح المنتجات أثناء الكتابة"""
        try:
            current_text = self.item_name.get().lower()
            if len(current_text) < 2:  # البدء في الاقتراح بعد حرفين
                return

            # البحث عن المنتجات المطابقة
            suggestions = []
            for product in self.products.values():
                if current_text in product['name'].lower():
                    suggestions.append(product)

            # عرض أول اقتراح إذا وجد
            if suggestions:
                first_suggestion = suggestions[0]
                # ملء السعر تلقائياً
                if not self.item_price.get():
                    self.item_price.delete(0, "end")
                    self.item_price.insert(0, str(first_suggestion['selling_price']))

        except Exception as e:
            print(f"خطأ في اقتراح المنتجات: {e}")

    def print_invoice(self):
        """طباعة الفاتورة"""
        messagebox.showinfo("طباعة", "سيتم إرسال الفاتورة للطابعة")

    def open_pos(self):
        """فتح نقطة البيع"""
        try:
            from ui.pos_simple import SimplePOSWindow
            pos_window = SimplePOSWindow(self.window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نقطة البيع: {str(e)}")

    def open_enhanced_pos(self):
        """فتح نقطة البيع المحسنة"""
        try:
            from ui.enhanced_pos_window import EnhancedPOSWindow
            enhanced_pos = EnhancedPOSWindow(self.window)
        except Exception as e:
            try:
                # في حالة عدم وجود النافذة المحسنة، استخدم النافذة البسيطة
                pos_window = SimplePOSWindow(self.window)
                messagebox.showinfo("نقطة البيع", "تم فتح نقطة البيع البسيطة")
            except Exception as e2:
                messagebox.showerror("خطأ", f"حدث خطأ في فتح نقطة البيع المحسنة: {str(e)}")

    def close_window(self):
        """إغلاق النافذة"""
        if hasattr(self, 'window') and self.window:
            self.window.destroy()
