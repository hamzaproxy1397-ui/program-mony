import time
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# تحذير أمني: هذا الملف يحتوي على عمليات حساسة
# يجب مراجعة جميع المدخلات والتأكد من التحقق منها
# Security Warning: This file contains sensitive operations
# All inputs must be validated and sanitized


"""
مدير المبيعات المحسن - SalesManager
Enhanced Sales Manager with Database Integration
"""

import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class SalesManager:
    """مدير المبيعات مع تكامل قاعدة البيانات المحسن"""

    def __init__(self, db_path='database/accounting.db'):
        """
        تهيئة مدير المبيعات

        Args:
            db_path (str): مسار قاعدة البيانات
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)

        # التأكد من وجود قاعدة البيانات
        if not Path(db_path).exists():
            self.logger.error(f"قاعدة البيانات غير موجودة: {db_path}")
            raise FileNotFoundError(f"Database not found: {db_path}")

    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30)
            conn.row_factory = sqlite3.Row  # للحصول على النتائج كـ dictionary
            return conn
        except Exception as e:
            self.logger.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
            raise

    def save_invoice(self, customer_name: str, items: List[Dict], total_amount: float,
                    discount_amount: float = 0, tax_amount: float = 0,
                    payment_status: str = 'pending', notes: str = '',
                    customer_id: Optional[int] = None) -> Dict:
        """
        حفظ فاتورة جديدة في قاعدة البيانات

        Args:
            customer_name (str): اسم العميل
            items (List[Dict]): قائمة الأصناف
            total_amount (float): المبلغ الإجمالي
            discount_amount (float): مبلغ الخصم
            tax_amount (float): مبلغ الضريبة
            payment_status (str): حالة الدفع
            notes (str): ملاحظات
            customer_id (Optional[int]): معرف العميل (اختياري)

        Returns:
            Dict: نتيجة العملية مع معرف الفاتورة
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # إنشاء رقم فاتورة فريد
                invoice_number = self._generate_invoice_number()
                invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                net_amount = total_amount - discount_amount + tax_amount

                # العثور على العميل أو إنشاؤه
                if not customer_id:
                    customer_id = self._get_or_create_customer(customer_name)

                # إدراج الفاتورة الرئيسية
                cursor.execute("""
                    INSERT INTO sales_invoices
                    (invoice_number, customer_id, total_amount, discount_amount,
                        tax_amount, net_amount, payment_status, invoice_date, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_number, customer_id, total_amount, discount_amount,
                    tax_amount, net_amount, payment_status, invoice_date, notes
                ))

                invoice_id = cursor.lastrowid

                # إدراج تفاصيل الفاتورة
                for item in items:
                    cursor.execute("""
                        INSERT INTO sales_invoice_items 
                        (invoice_id, product_id, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        invoice_id,
                        item.get('product_id'),
                        item['quantity'],
                        item['price'],
                        item['quantity'] * item['price']
                    ))

                conn.commit()

                self.logger.info(f"تم حفظ الفاتورة {invoice_number} بنجاح (ID: {invoice_id})")

                return {
                    'success': True,
                    'invoice_id': invoice_id,
                    'invoice_number': invoice_number,
                    'net_amount': net_amount,
                    'message': f'تم حفظ الفاتورة {invoice_number} بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ أثناء حفظ الفاتورة: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في حفظ الفاتورة'
            }

    def update_inventory(self, items: List[Dict]) -> Dict:
        """
        تحديث المخزون بعد البيع

        Args:
            items (List[Dict]): قائمة الأصناف المباعة

        Returns:
            Dict: نتيجة العملية
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                updated_products = []

                for item in items:
                    product_id = item.get('product_id')
                    quantity = item['quantity']

                    if not product_id:
                        continue

                    # التحقق من المخزون المتاح
                    cursor.execute(
                        "SELECT name, current_stock FROM products WHERE id = ?",
                        (product_id,)
                    )
                    product = cursor.fetchone()

                    if not product:
                        self.logger.warning(f"المنتج غير موجود: ID {product_id}")
                        continue

                    if product['current_stock'] < quantity:
                        return {
                            'success': False,
                            'error': 'insufficient_stock',
                            'message': f'المخزون غير كافي للمنتج: {product["name"]}'
                        }

                    # تحديث المخزون
                    cursor.execute("""
                        UPDATE products 
                        SET current_stock = current_stock - ? 
                        WHERE id = ?
                    """, (quantity, product_id))

                    updated_products.append({
                        'product_id': product_id,
                        'name': product['name'],
                        'old_stock': product['current_stock'],
                        'new_stock': product['current_stock'] - quantity,
                        'quantity_sold': quantity
                    })

                conn.commit()

                self.logger.info(f"تم تحديث مخزون {len(updated_products)} منتج")

                return {
                    'success': True,
                    'updated_products': updated_products,
                    'message': f'تم تحديث مخزون {len(updated_products)} منتج'
                }

        except Exception as e:
            self.logger.error(f"خطأ أثناء تحديث المخزون: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في تحديث المخزون'
            }

    def process_sale(self, customer_name: str, items: List[Dict], total_amount: float,
                    discount_amount: float = 0, tax_amount: float = 0,
                    payment_status: str = 'pending', notes: str = '',
                    update_stock: bool = True) -> Dict:
        """
        معالجة عملية بيع كاملة (حفظ الفاتورة + تحديث المخزون)

        Args:
            customer_name (str): اسم العميل
            items (List[Dict]): قائمة الأصناف
            total_amount (float): المبلغ الإجمالي
            discount_amount (float): مبلغ الخصم
            tax_amount (float): مبلغ الضريبة
            payment_status (str): حالة الدفع
            notes (str): ملاحظات
            update_stock (bool): تحديث المخزون أم لا

        Returns:
            Dict: نتيجة العملية الكاملة
        """
        try:
            # التحقق من صحة البيانات
            validation = self._validate_sale_data(customer_name, items, total_amount)
            if not validation['is_valid']:
                return {
                    'success': False,
                    'errors': validation['errors'],
                    'message': 'بيانات البيع غير صحيحة'
                }

            # التحقق من المخزون قبل البيع (إذا كان التحديث مطلوب)
            if update_stock:
                stock_check = self._check_stock_availability(items)
                if not stock_check['available']:
                    return {
                        'success': False,
                        'error': 'insufficient_stock',
                        'message': stock_check['message']
                    }

            # حفظ الفاتورة
            invoice_result = self.save_invoice(
                customer_name, items, total_amount, discount_amount,
                tax_amount, payment_status, notes
            )

            if not invoice_result['success']:
                return invoice_result

            # تحديث المخزون
            if update_stock:
                inventory_result = self.update_inventory(items)
                if not inventory_result['success']:
                    # في حالة فشل تحديث المخزون، يمكن إلغاء الفاتورة
                    self.logger.error("فشل في تحديث المخزون بعد حفظ الفاتورة")
                    return {
                        'success': False,
                        'invoice_saved': True,
                        'invoice_id': invoice_result['invoice_id'],
                        'error': inventory_result['error'],
                        'message': 'تم حفظ الفاتورة لكن فشل تحديث المخزون'
                    }

            # نجحت العملية كاملة
            result = {
                'success': True,
                'invoice_id': invoice_result['invoice_id'],
                'invoice_number': invoice_result['invoice_number'],
                'net_amount': invoice_result['net_amount'],
                'message': f'تمت عملية البيع بنجاح - فاتورة رقم {invoice_result["invoice_number"]}'
            }

            if update_stock:
                result['inventory_updated'] = True
                result['updated_products'] = inventory_result.get('updated_products', [])

            self.logger.info(f"تمت عملية البيع بنجاح: {invoice_result['invoice_number']}")

            return result

        except Exception as e:
            self.logger.error(f"خطأ في معالجة البيع: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في معالجة عملية البيع'
            }

    def get_invoice(self, invoice_id: int) -> Optional[Dict]:
        """
        الحصول على فاتورة مع تفاصيلها

        Args:
            invoice_id (int): معرف الفاتورة

        Returns:
            Optional[Dict]: بيانات الفاتورة أو None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # جلب بيانات الفاتورة الرئيسية
                cursor.execute("""
                    SELECT * FROM sales_invoices WHERE id = ?
                """, (invoice_id,))

                invoice = cursor.fetchone()
                if not invoice:
                    return None

                # جلب تفاصيل الفاتورة
                cursor.execute("""
                    SELECT sii.*, p.name as product_name
                    FROM sales_invoice_items sii
                    LEFT JOIN products p ON sii.product_id = p.id
                    WHERE sii.invoice_id = ?
                """, (invoice_id,))

                items = cursor.fetchall()

                return {
                    'invoice': dict(invoice),
                    'items': [dict(item) for item in items]
                }

        except Exception as e:
            self.logger.error(f"خطأ في جلب الفاتورة: {e}")
            return None

    def _generate_invoice_number(self) -> str:
        """إنشاء رقم فاتورة فريد"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        microseconds = str(int(time.time() * 1000000))[-6:]  # آخر 6 أرقام من الميكروثانية
        return f"INV{timestamp}{microseconds}"

    def _validate_sale_data(self, customer_name: str, items: List[Dict], 
                            total_amount: float) -> Dict:
        """التحقق من صحة بيانات البيع"""
        errors = []

        # التحقق من اسم العميل
        if not customer_name or not customer_name.strip():
            errors.append("اسم العميل مطلوب")

        # التحقق من وجود أصناف
        if not items or len(items) == 0:
            errors.append("يجب إضافة صنف واحد على الأقل")

        # التحقق من صحة بيانات الأصناف
        for i, item in enumerate(items):
            if not isinstance(item.get('quantity'), (int, float)) or item.get('quantity') <= 0:
                errors.append(f"كمية صحيحة مطلوبة في السطر {i+1}")

            if not isinstance(item.get('price'), (int, float)) or item.get('price') <= 0:
                errors.append(f"سعر صحيح مطلوب في السطر {i+1}")

        # التحقق من المبلغ الإجمالي
        if not isinstance(total_amount, (int, float)) or total_amount <= 0:
            errors.append("المبلغ الإجمالي يجب أن يكون أكبر من صفر")

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def _check_stock_availability(self, items: List[Dict]) -> Dict:
        """التحقق من توفر المخزون"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                for item in items:
                    product_id = item.get('product_id')
                    quantity = item['quantity']

                    if not product_id:
                        continue

                    cursor.execute(
                        "SELECT name, current_stock FROM products WHERE id = ?",
                        (product_id,)
                    )
                    product = cursor.fetchone()

                    if not product:
                        return {
                            'available': False,
                            'message': f'المنتج غير موجود: ID {product_id}'
                        }

                    if product['current_stock'] < quantity:
                        return {
                            'available': False,
                            'message': f'المخزون غير كافي للمنتج: {product["name"]} (متاح: {product["current_stock"]}, مطلوب: {quantity})'
                        }

                return {
                    'available': True,
                    'message': 'المخزون متاح لجميع الأصناف'
                }

        except Exception as e:
            self.logger.error(f"خطأ في فحص المخزون: {e}")
            return {
                'available': False,
                'message': f'خطأ في فحص المخزون: {str(e)}'
            }

    def _get_or_create_customer(self, customer_name: str) -> Optional[int]:
        """العثور على العميل أو إنشاؤه"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # البحث عن العميل
                cursor.execute("SELECT id FROM customers WHERE name = ?", (customer_name,))
                customer = cursor.fetchone()

                if customer:
                    return customer[0]

                # إنشاء عميل جديد
                cursor.execute("""
                    INSERT INTO customers (name, is_active)
                    VALUES (?, 1)
                """, (customer_name,))

                return cursor.lastrowid

        except Exception as e:
            self.logger.error(f"خطأ في العثور على العميل أو إنشاؤه: {e}")
            return None



    def save_invoice_simple(self, customer_name: str, items: List[Dict], total_amount: float) -> Dict:
        """حفظ فاتورة مبسطة للتوافق مع الجداول البسيطة"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # إنشاء رقم فاتورة فريد
                invoice_number = self._generate_invoice_number()
                invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # إدراج في جدول invoices البسيط
                cursor.execute("""
                    INSERT INTO invoices (customer_name, total, date)
                    VALUES (?, ?, ?)
                """, (customer_name, total_amount, invoice_date))

                invoice_id = cursor.lastrowid

                # إدراج تفاصيل الفاتورة
                for item in items:
                    cursor.execute("""
                        INSERT INTO invoice_items (invoice_id, product_id, quantity, price)
                        VALUES (?, ?, ?, ?)
                    """, (
                        invoice_id,
                        item.get('product_id'),
                        item['quantity'],
                        item['price']
                    ))

                conn.commit()

                return {
                    'success': True,
                    'invoice_id': invoice_id,
                    'invoice_number': invoice_number,
                    'net_amount': total_amount,
                    'message': f'تم حفظ الفاتورة {invoice_number} بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في حفظ الفاتورة المبسطة: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في حفظ الفاتورة'
            }

    def update_inventory_simple(self, items: List[Dict]) -> Dict:
        """تحديث المخزون المبسط"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                updated_products = []

                for item in items:
                    product_id = item.get('product_id')
                    quantity = item['quantity']

                    if not product_id:
                        continue

                    # تحديث المخزون في العمود stock
                    cursor.execute("""
                        UPDATE products 
                        SET stock = stock - ?,
                            current_stock = current_stock - ?
                        WHERE id = ?
                    """, (quantity, quantity, product_id))

                    if cursor.rowcount > 0:
                        updated_products.append({
                            'product_id': product_id,
                            'quantity_sold': quantity
                        })

                conn.commit()

                return {
                    'success': True,
                    'updated_products': updated_products,
                    'message': f'تم تحديث مخزون {len(updated_products)} منتج'
                }

        except Exception as e:
            self.logger.error(f"خطأ في تحديث المخزون المبسط: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في تحديث المخزون'
            }
    def close_connection(self):
        """إغلاق الاتصال (للتوافق مع الكود القديم)"""
        # لا حاجة لإغلاق الاتصال لأننا نستخدم context manager
        pass
