# -*- coding: utf-8 -*-
# cSpell:disable
"""
مدير المبيعات المحسن
Enhanced Sales Manager with Database Integration
"""

from datetime import datetime
import logging
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class SalesManager:
    """مدير المبيعات مع تكامل قاعدة البيانات"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def create_invoice(self, customer_id: Optional[int], items: List[Dict], 
                      discount: float = 0, tax_rate: float = 0) -> Dict:
        """إنشاء فاتورة مبيعات جديدة"""
        try:
            # حساب الإجماليات
            subtotal = sum(item['quantity'] * item['price'] for item in items)
            discount_amount = subtotal * (discount / 100)
            tax_amount = (subtotal - discount_amount) * (tax_rate / 100)
            net_amount = subtotal - discount_amount + tax_amount

            # إنشاء رقم فاتورة فريد
            invoice_number = self._generate_invoice_number()

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # حفظ الفاتورة الرئيسية
                cursor.execute("""
                    INSERT INTO sales_invoices 
                    (invoice_number, customer_id, total_amount, discount_amount, 
                     tax_amount, net_amount, payment_status, invoice_date)
                    VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
                """, (invoice_number, customer_id, subtotal, discount_amount,
                      tax_amount, net_amount, datetime.now()))

                invoice_id = cursor.lastrowid

                # حفظ تفاصيل الفاتورة
                for item in items:
                    cursor.execute("""
                        INSERT INTO sales_invoice_items
                        (invoice_id, product_id, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (invoice_id, item.get('product_id'), item['quantity'],
                          item['price'], item['quantity'] * item['price']))

                    # تحديث المخزون
                    self._update_inventory(cursor, item.get('product_id'), 
                                         -item['quantity'])

                conn.commit()

                return {
                    'success': True,
                    'invoice_id': invoice_id,
                    'invoice_number': invoice_number,
                    'total_amount': net_amount,
                    'message': f'تم إنشاء الفاتورة رقم {invoice_number} بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الفاتورة: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في إنشاء الفاتورة'
            }

    def get_invoice(self, invoice_id: int) -> Optional[Dict]:
        """استرجاع فاتورة بالتفاصيل"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # استرجاع بيانات الفاتورة الرئيسية
                cursor.execute("""
                    SELECT si.*, c.name as customer_name
                    FROM sales_invoices si
                    LEFT JOIN customers c ON si.customer_id = c.id
                    WHERE si.id = ?
                """, (invoice_id,))

                invoice = cursor.fetchone()
                if not invoice:
                    return None

                # استرجاع تفاصيل الفاتورة
                cursor.execute("""
                    SELECT sii.*, p.name as product_name
                    FROM sales_invoice_items sii
                    JOIN products p ON sii.product_id = p.id
                    WHERE sii.invoice_id = ?
                """, (invoice_id,))

                items = cursor.fetchall()

                return {
                    'invoice': dict(invoice),
                    'items': [dict(item) for item in items]
                }

        except Exception as e:
            self.logger.error(f"خطأ في استرجاع الفاتورة: {e}")
            return None

    def update_payment_status(self, invoice_id: int, status: str) -> bool:
        """تحديث حالة الدفع للفاتورة"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE sales_invoices 
                    SET payment_status = ?
                    WHERE id = ?
                """, (status, invoice_id))

                return cursor.rowcount > 0

        except Exception as e:
            self.logger.error(f"خطأ في تحديث حالة الدفع: {e}")
            return False

    def get_sales_report(self, start_date: str, end_date: str) -> Dict:
        """تقرير المبيعات لفترة محددة"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # إجمالي المبيعات
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_invoices,
                        SUM(net_amount) as total_sales,
                        AVG(net_amount) as average_sale
                    FROM sales_invoices
                    WHERE DATE(invoice_date) BETWEEN ? AND ?
                """, (start_date, end_date))

                summary = cursor.fetchone()

                # أفضل المنتجات مبيعاً
                cursor.execute("""
                    SELECT 
                        p.name,
                        SUM(sii.quantity) as total_quantity,
                        SUM(sii.total_price) as total_revenue
                    FROM sales_invoice_items sii
                    JOIN products p ON sii.product_id = p.id
                    JOIN sales_invoices si ON sii.invoice_id = si.id
                    WHERE DATE(si.invoice_date) BETWEEN ? AND ?
                    GROUP BY p.id, p.name
                    ORDER BY total_revenue DESC
                    LIMIT 10
                """, (start_date, end_date))

                top_products = cursor.fetchall()

                # المبيعات اليومية
                cursor.execute("""
                    SELECT 
                        DATE(invoice_date) as sale_date,
                        COUNT(*) as daily_invoices,
                        SUM(net_amount) as daily_sales
                    FROM sales_invoices
                    WHERE DATE(invoice_date) BETWEEN ? AND ?
                    GROUP BY DATE(invoice_date)
                    ORDER BY sale_date
                """, (start_date, end_date))

                daily_sales = cursor.fetchall()

                return {
                    'summary': dict(summary) if summary else {},
                    'top_products': [dict(row) for row in top_products],
                    'daily_sales': [dict(row) for row in daily_sales]
                }

        except Exception as e:
            self.logger.error(f"خطأ في تقرير المبيعات: {e}")
            return {}

    def search_invoices(self, search_term: str, limit: int = 50) -> List[Dict]:
        """البحث في الفواتير"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT 
                        si.id,
                        si.invoice_number,
                        si.net_amount,
                        si.payment_status,
                        si.invoice_date,
                        c.name as customer_name
                    FROM sales_invoices si
                    LEFT JOIN customers c ON si.customer_id = c.id
                    WHERE si.invoice_number LIKE ? 
                       OR c.name LIKE ?
                    ORDER BY si.invoice_date DESC
                    LIMIT ?
                """, (f'%{search_term}%', f'%{search_term}%', limit))

                return [dict(row) for row in cursor.fetchall()]

        except Exception as e:
            self.logger.error(f"خطأ في البحث: {e}")
            return []

    def _generate_invoice_number(self) -> str:
        """إنشاء رقم فاتورة فريد"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"INV{timestamp}"

    def _update_inventory(self, cursor, product_id: int, quantity_change: float):
        """تحديث المخزون"""
        if product_id:
            cursor.execute("""
                UPDATE products 
                SET current_stock = current_stock + ?
                WHERE id = ?
            """, (quantity_change, product_id))

class OptimizedCart:
    """سلة مشتريات محسنة للأداء"""

    def __init__(self):
        self.items = {}  # استخدام dictionary للوصول السريع O(1)
        self.total_amount = 0.0

    def add_item(self, product_id: int, product_data: Dict, quantity: float = 1):
        """إضافة منتج للسلة"""
        if product_id in self.items:
            # تحديث الكمية للمنتج الموجود
            self.items[product_id]['quantity'] += quantity
        else:
            # إضافة منتج جديد
            self.items[product_id] = {
                'name': product_data['name'],
                'price': product_data['price'],
                'quantity': quantity,
                'product_id': product_id
            }

        # تحديث الإجمالي
        self.items[product_id]['total'] = (
            self.items[product_id]['quantity'] * 
            self.items[product_id]['price']
        )

        self._update_total()

    def remove_item(self, product_id: int):
        """حذف منتج من السلة"""
        if product_id in self.items:
            del self.items[product_id]
            self._update_total()

    def update_quantity(self, product_id: int, new_quantity: float):
        """تحديث كمية منتج"""
        if product_id in self.items:
            if new_quantity <= 0:
                self.remove_item(product_id)
            else:
                self.items[product_id]['quantity'] = new_quantity
                self.items[product_id]['total'] = (
                    new_quantity * self.items[product_id]['price']
                )
                self._update_total()

    def clear(self):
        """مسح السلة"""
        self.items.clear()
        self.total_amount = 0.0

    def get_items_list(self) -> List[Dict]:
        """الحصول على قائمة العناصر"""
        return list(self.items.values())

    def get_item_count(self) -> int:
        """عدد الأصناف في السلة"""
        return len(self.items)

    def get_total_quantity(self) -> float:
        """إجمالي الكميات"""
        return sum(item['quantity'] for item in self.items.values())

    def _update_total(self):
        """تحديث الإجمالي الكلي"""
        self.total_amount = sum(item['total'] for item in self.items.values())

class SalesValidator:
    """مدقق بيانات المبيعات"""

    @staticmethod
    def validate_invoice_data(customer_id: Optional[int], items: List[Dict]) -> Dict:
        """التحقق من صحة بيانات الفاتورة"""
        errors = []

        # التحقق من وجود أصناف
        if not items:
            errors.append("يجب إضافة صنف واحد على الأقل")

        # التحقق من صحة بيانات الأصناف
        for i, item in enumerate(items):
            if not item.get('name'):
                errors.append(f"اسم الصنف مطلوب في السطر {i+1}")

            if not isinstance(item.get('quantity'), (int, float)) or item.get('quantity') <= 0:
                errors.append(f"كمية صحيحة مطلوبة في السطر {i+1}")

            if not isinstance(item.get('price'), (int, float)) or item.get('price') <= 0:
                errors.append(f"سعر صحيح مطلوب في السطر {i+1}")

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    @staticmethod
    def validate_payment_status(status: str) -> bool:
        """التحقق من صحة حالة الدفع"""
        valid_statuses = ['pending', 'paid', 'partial', 'cancelled']
        return status in valid_statuses
