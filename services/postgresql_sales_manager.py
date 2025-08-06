# -*- coding: utf-8 -*-
"""
مدير المبيعات مع PostgreSQL
PostgreSQL Sales Manager
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
from database.postgresql_manager import PostgreSQLManager

class PostgreSQLSalesManager:
    """مدير المبيعات مع دعم PostgreSQL"""

    def __init__(self, pg_manager: PostgreSQLManager = None):
        """
        تهيئة مدير المبيعات

        Args:
            pg_manager (PostgreSQLManager): مدير PostgreSQL
        """
        self.pg_manager = pg_manager or PostgreSQLManager()
        self.logger = logging.getLogger(__name__)

    def save_invoice(self, customer_name: str, items: List[Dict], total_amount: float,
                    discount_amount: float = 0, tax_amount: float = 0,
                    payment_status: str = 'pending', notes: str = '',
                    customer_id: Optional[int] = None) -> Dict:
        """
        حفظ فاتورة جديدة في PostgreSQL

        Args:
            customer_name (str): اسم العميل
            items (List[Dict]): قائمة الأصناف
            total_amount (float): المبلغ الإجمالي
            discount_amount (float): مبلغ الخصم
            tax_amount (float): مبلغ الضريبة
            payment_status (str): حالة الدفع
            notes (str): ملاحظات
            customer_id (Optional[int]): معرف العميل

        Returns:
            Dict: نتيجة العملية مع معرف الفاتورة
        """
        try:
            with self.pg_manager.get_connection() as conn:
                cursor = conn.cursor()

                # إنشاء رقم فاتورة فريد
                invoice_number = self._generate_invoice_number()
                invoice_date = datetime.now()
                net_amount = total_amount - discount_amount + tax_amount

                # العثور على العميل أو إنشاؤه
                if not customer_id:
                    customer_id = self._get_or_create_customer(customer_name, cursor)

                # إدراج الفاتورة الرئيسية
                cursor.execute("""
                    INSERT INTO sales_invoices 
                    (invoice_number, customer_id, total_amount, discount_amount, 
                    tax_amount, net_amount, payment_status, invoice_date, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    invoice_number, customer_id, total_amount, discount_amount,
                    tax_amount, net_amount, payment_status, invoice_date, notes
                ))

                invoice_id = cursor.fetchone()[0]

                # إدراج تفاصيل الفاتورة
                for item in items:
                    cursor.execute("""
                        INSERT INTO sales_invoice_items 
                        (invoice_id, product_id, quantity, unit_price, total_price)
                        VALUES (%s, %s, %s, %s, %s)
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
            pass
        except Exception as e:
            self.logger.error(f"خطأ أثناء حفظ الفاتورة: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في حفظ الفاتورة'
            }

    def save_invoice_simple(self, customer_name: str, items: List[Dict], total_amount: float) -> Dict:
        """حفظ فاتورة مبسطة للتوافق"""
        try:
            with self.pg_manager.get_connection() as conn:
                cursor = conn.cursor()

                # إدراج في جدول invoices البسيط
                cursor.execute("""
                    INSERT INTO invoices (customer_name, total, date)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (customer_name, total_amount, datetime.now()))

                invoice_id = cursor.fetchone()[0]

                # إدراج تفاصيل الفاتورة
                for item in items:
                    cursor.execute("""
                        INSERT INTO invoice_items (invoice_id, product_id, quantity, price)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        invoice_id,
                        item.get('product_id'),
                        item['quantity'],
                        item['price']
                    ))

                conn.commit()

                invoice_number = f"INV{invoice_id:06d}"

                return {
                    'success': True,
                    'invoice_id': invoice_id,
                    'invoice_number': invoice_number,
                    'net_amount': total_amount,
                    'message': f'تم حفظ الفاتورة {invoice_number} بنجاح'
                }

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في حفظ الفاتورة المبسطة: {e}")
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
            with self.pg_manager.get_connection() as conn:
                cursor = conn.cursor()

                updated_products = []

                for item in items:
                    product_id = item.get('product_id')
                    quantity = item['quantity']

                    if not product_id:
                        continue

                    # التحقق من المخزون المتاح
                    cursor.execute(
                        "SELECT name, current_stock FROM products WHERE id = %s",
                        (product_id,)
                    )
                    product = cursor.fetchone()

                    if not product:
                        self.logger.warning(f"المنتج غير موجود: ID {product_id}")
                        continue

                    if product[1] < quantity:
                        return {
                            'success': False,
                            'error': 'insufficient_stock',
                            'message': f'المخزون غير كافي للمنتج: {product[0]}'
                        }

                    # تحديث المخزون
                    cursor.execute("""
                        UPDATE products 
                        SET current_stock = current_stock - %s,
                            stock = stock - %s
                        WHERE id = %s
                    """, (quantity, quantity, product_id))

                    # تسجيل حركة المخزون
                    cursor.execute("""
                        INSERT INTO inventory_movements 
                        (product_id, movement_type, quantity, reference_type, notes)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (product_id, 'sale', -quantity, 'sales_invoice', f'بيع {quantity} وحدة'))

                    updated_products.append({
                        'product_id': product_id,
                        'name': product[0],
                        'old_stock': product[1],
                        'new_stock': product[1] - quantity,
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
            pass
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
        معالجة عملية بيع كاملة

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
            pass
        except Exception as e:
            self.logger.error(f"خطأ في معالجة البيع: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في معالجة عملية البيع'
            }

    def get_invoice(self, invoice_id: int) -> Optional[Dict]:
        """الحصول على فاتورة مع تفاصيلها"""
        try:
            with self.pg_manager.get_connection() as conn:
                cursor = conn.cursor()

                # جلب بيانات الفاتورة الرئيسية
                cursor.execute("""
                    SELECT si.*, c.name as customer_name
                    FROM sales_invoices si
                    LEFT JOIN customers c ON si.customer_id = c.id
                    WHERE si.id = %s
                """, (invoice_id,))

                invoice = cursor.fetchone()
                if not invoice:
                    return None

                # تحويل النتيجة إلى dictionary
                columns = [desc[0] for desc in cursor.description]
                invoice_dict = dict(zip(columns, invoice))

                # جلب تفاصيل الفاتورة
                cursor.execute("""
                    SELECT sii.*, p.name as product_name, p.unit
                    FROM sales_invoice_items sii
                    JOIN products p ON sii.product_id = p.id
                    WHERE sii.invoice_id = %s
                    ORDER BY sii.id
                """, (invoice_id,))

                items = cursor.fetchall()
                items_columns = [desc[0] for desc in cursor.description]
                items_list = [dict(zip(items_columns, item)) for item in items]

                return {
                    'invoice': invoice_dict,
                    'items': items_list
                }

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في جلب الفاتورة: {e}")
            return None

    def get_all_products(self) -> List[Dict]:
        """جلب جميع المنتجات النشطة"""
        try:
            with self.pg_manager.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, name, barcode, category, unit, cost_price, selling_price,
                            min_stock, current_stock, stock, price, description
                    FROM products 
                    WHERE is_active = TRUE
                    ORDER BY name
                """)

                products = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                return [dict(zip(columns, product)) for product in products]

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في جلب المنتجات: {e}")
            return []

    def _get_or_create_customer(self, customer_name: str, cursor) -> Optional[int]:
        """العثور على العميل أو إنشاؤه"""
        try:
            # البحث عن العميل
            cursor.execute("SELECT id FROM customers WHERE name = %s", (customer_name,))
            customer = cursor.fetchone()

            if customer:
                return customer[0]

            # إنشاء عميل جديد
            cursor.execute("""
                INSERT INTO customers (name, is_active) 
                VALUES (%s, %s)
                RETURNING id
            """, (customer_name, True))

            return cursor.fetchone()[0]

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في العثور على العميل أو إنشاؤه: {e}")
            return None

    def _generate_invoice_number(self) -> str:
        """إنشاء رقم فاتورة فريد"""
        import time
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        microseconds = str(int(time.time() * 1000000))[-6:]
        return f"PG{timestamp}{microseconds}"

    def _validate_sale_data(self, customer_name: str, items: List[Dict],
                            total_amount: float) -> Dict:
        """التحقق من صحة بيانات البيع"""
        errors = []

        if not customer_name or not customer_name.strip():
            errors.append("اسم العميل مطلوب")

        if not items or len(items) == 0:
            errors.append("يجب إضافة صنف واحد على الأقل")

        for i, item in enumerate(items):
            if not isinstance(item.get('quantity'), (int, float)) or item.get('quantity') <= 0:
                errors.append(f"كمية صحيحة مطلوبة في السطر {i+1}")

            if not isinstance(item.get('price'), (int, float)) or item.get('price') <= 0:
                errors.append(f"سعر صحيح مطلوب في السطر {i+1}")

        if not isinstance(total_amount, (int, float)) or total_amount <= 0:
            errors.append("المبلغ الإجمالي يجب أن يكون أكبر من صفر")

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def _check_stock_availability(self, items: List[Dict]) -> Dict:
        """التحقق من توفر المخزون"""
        try:
            with self.pg_manager.get_connection() as conn:
                cursor = conn.cursor()

                for item in items:
                    product_id = item.get('product_id')
                    quantity = item['quantity']

                    if not product_id:
                        continue

                    cursor.execute(
                        "SELECT name, current_stock FROM products WHERE id = %s",
                        (product_id,)
                    )
                    product = cursor.fetchone()

                    if not product:
                        return {
                            'available': False,
                            'message': f'المنتج غير موجود: ID {product_id}'
                        }

                    if product[1] < quantity:
                        return {
                            'available': False,
                            'message': f'المخزون غير كافي للمنتج: {product[0]} (متاح: {product[1]}, مطلوب: {quantity})'
                        }

                return {
                    'available': True,
                    'message': 'المخزون متاح لجميع الأصناف'
                }

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في فحص المخزون: {e}")
            return {
                'available': False,
                'message': f'خطأ في فحص المخزون: {str(e)}'
            }
