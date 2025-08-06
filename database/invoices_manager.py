# -*- coding: utf-8 -*-
"""
مدير الفواتير - إدارة شاملة لفواتير المبيعات
Invoices Manager - Comprehensive Sales Invoices Management
"""

import logging
from datetime import datetime, timedelta
from database.database_manager import DatabaseManager
from database.products_manager import ProductsManager
from typing import Dict
from typing import List
from typing import Optional
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class InvoicesManager:
    """مدير الفواتير مع عمليات CRUD كاملة"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.products_manager = ProductsManager(db_manager)
        self.logger = logging.getLogger(__name__)

    def create_invoice(self, invoice_data: Dict) -> Dict:
        """إنشاء فاتورة مبيعات جديدة"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # التحقق من صحة البيانات
                validation = self._validate_invoice_data(invoice_data)
                if not validation['is_valid']:
                    return {
                        'success': False,
                        'errors': validation['errors'],
                        'message': 'بيانات الفاتورة غير صحيحة'
                    }

                # إنشاء رقم فاتورة فريد
                invoice_number = self._generate_invoice_number()

                # حساب الإجماليات
                totals = self._calculate_totals(invoice_data['items'], 
                                              invoice_data.get('discount_percent', 0),
                                              invoice_data.get('tax_percent', 0))

                # إدراج الفاتورة الرئيسية
                cursor.execute("""
                    INSERT INTO sales_invoices 
                    (invoice_number, customer_id, total_amount, discount_amount, 
                     tax_amount, net_amount, payment_status, invoice_date, notes, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_number,
                    invoice_data.get('customer_id'),
                    totals['subtotal'],
                    totals['discount_amount'],
                    totals['tax_amount'],
                    totals['net_amount'],
                    invoice_data.get('payment_status', 'pending'),
                    invoice_data.get('invoice_date', datetime.now()),
                    invoice_data.get('notes', ''),
                    invoice_data.get('created_by')
                ))

                invoice_id = cursor.lastrowid

                # إدراج تفاصيل الفاتورة وتحديث المخزون
                for item in invoice_data['items']:
                    # إدراج تفاصيل الفاتورة
                    cursor.execute("""
                        INSERT INTO sales_invoice_items
                        (invoice_id, product_id, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        invoice_id,
                        item['product_id'],
                        item['quantity'],
                        item['unit_price'],
                        item['quantity'] * item['unit_price']
                    ))

                    # تحديث المخزون (خصم الكمية المباعة)
                    if item.get('product_id'):
                        stock_result = self.products_manager.update_stock(
                            item['product_id'], 
                            -item['quantity'], 
                            'sale'
                        )

                        if not stock_result['success']:
                            # إذا فشل تحديث المخزون، إلغاء العملية
                            conn.rollback()
                            return {
                                'success': False,
                                'error': 'stock_update_failed',
                                'message': f"فشل في تحديث مخزون المنتج: {stock_result['message']}"
                            }

                conn.commit()

                self.logger.info(f"تم إنشاء الفاتورة: {invoice_number} (ID: {invoice_id})")

                return {
                    'success': True,
                    'invoice_id': invoice_id,
                    'invoice_number': invoice_number,
                    'net_amount': totals['net_amount'],
                    'message': f'تم إنشاء الفاتورة {invoice_number} بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الفاتورة: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في إنشاء الفاتورة'
            }

    def get_invoice(self, invoice_id: int) -> Optional[Dict]:
        """الحصول على فاتورة مع تفاصيلها"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # جلب بيانات الفاتورة الرئيسية
                cursor.execute("""
                    SELECT si.*, c.name as customer_name, u.full_name as created_by_name
                    FROM sales_invoices si
                    LEFT JOIN customers c ON si.customer_id = c.id
                    LEFT JOIN users u ON si.created_by = u.id
                    WHERE si.id = ?
                """, (invoice_id,))

                invoice = cursor.fetchone()
                if not invoice:
                    return None

                # جلب تفاصيل الفاتورة
                cursor.execute("""
                    SELECT sii.*, p.name as product_name, p.unit
                    FROM sales_invoice_items sii
                    JOIN products p ON sii.product_id = p.id
                    WHERE sii.invoice_id = ?
                    ORDER BY sii.id
                """, (invoice_id,))

                items = cursor.fetchall()

                return {
                    'invoice': dict(invoice),
                    'items': [dict(item) for item in items]
                }

        except Exception as e:
            self.logger.error(f"خطأ في جلب الفاتورة: {e}")
            return None

    def get_invoice_by_number(self, invoice_number: str) -> Optional[Dict]:
        """الحصول على فاتورة برقم الفاتورة"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM sales_invoices WHERE invoice_number = ?", 
                             (invoice_number,))
                result = cursor.fetchone()

                if result:
                    return self.get_invoice(result[0])
                return None

        except Exception as e:
            self.logger.error(f"خطأ في جلب الفاتورة برقم الفاتورة: {e}")
            return None

    def update_payment_status(self, invoice_id: int, payment_status: str, 
                            payment_date: datetime = None) -> Dict:
        """تحديث حالة الدفع للفاتورة"""
        try:
            valid_statuses = ['pending', 'paid', 'partial', 'cancelled']
            if payment_status not in valid_statuses:
                return {
                    'success': False,
                    'error': 'invalid_status',
                    'message': f'حالة الدفع غير صحيحة. الحالات المسموحة: {valid_statuses}'
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # التحقق من وجود الفاتورة
                cursor.execute("SELECT invoice_number FROM sales_invoices WHERE id = ?", 
                             (invoice_id,))
                result = cursor.fetchone()
                if not result:
                    return {
                        'success': False,
                        'error': 'invoice_not_found',
                        'message': 'الفاتورة غير موجودة'
                    }

                # تحديث حالة الدفع
                cursor.execute("""
                    UPDATE sales_invoices 
                    SET payment_status = ?
                    WHERE id = ?
                """, (payment_status, invoice_id))

                conn.commit()

                self.logger.info(f"تم تحديث حالة الدفع للفاتورة {result[0]} إلى {payment_status}")

                return {
                    'success': True,
                    'message': f'تم تحديث حالة الدفع إلى {payment_status}'
                }

        except Exception as e:
            self.logger.error(f"خطأ في تحديث حالة الدفع: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في تحديث حالة الدفع'
            }

    def cancel_invoice(self, invoice_id: int, reason: str = '') -> Dict:
        """إلغاء فاتورة وإرجاع المخزون"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # جلب بيانات الفاتورة
                invoice_data = self.get_invoice(invoice_id)
                if not invoice_data:
                    return {
                        'success': False,
                        'error': 'invoice_not_found',
                        'message': 'الفاتورة غير موجودة'
                    }

                # التحقق من إمكانية الإلغاء
                if invoice_data['invoice']['payment_status'] == 'cancelled':
                    return {
                        'success': False,
                        'error': 'already_cancelled',
                        'message': 'الفاتورة ملغاة مسبقاً'
                    }

                # إرجاع المخزون
                for item in invoice_data['items']:
                    if item['product_id']:
                        self.products_manager.update_stock(
                            item['product_id'], 
                            item['quantity'], 
                            'return'
                        )

                # تحديث حالة الفاتورة
                cursor.execute("""
                    UPDATE sales_invoices 
                    SET payment_status = 'cancelled',
                        notes = CASE 
                            WHEN notes IS NULL OR notes = '' THEN ?
                            ELSE notes || ' | ' || ?
                        END
                    WHERE id = ?
                """, (f"ملغاة: {reason}", f"ملغاة: {reason}", invoice_id))

                conn.commit()

                self.logger.info(f"تم إلغاء الفاتورة {invoice_data['invoice']['invoice_number']}")

                return {
                    'success': True,
                    'message': 'تم إلغاء الفاتورة وإرجاع المخزون بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في إلغاء الفاتورة: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'فشل في إلغاء الفاتورة'
            }

    def search_invoices(self, search_criteria: Dict) -> List[Dict]:
        """البحث في الفواتير"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                query = """
                    SELECT si.id, si.invoice_number, si.net_amount, si.payment_status,
                           si.invoice_date, c.name as customer_name
                    FROM sales_invoices si
                    LEFT JOIN customers c ON si.customer_id = c.id
                    WHERE 1=1
                """
                params = []

                # البحث بالنص
                if search_criteria.get('search_term'):
                    query += " AND (si.invoice_number LIKE ? OR c.name LIKE ?)"
                    term = f"%{search_criteria['search_term']}%"
                    params.extend([term, term])

                # فلترة بالتاريخ
                if search_criteria.get('start_date'):
                    query += " AND DATE(si.invoice_date) >= ?"
                    params.append(search_criteria['start_date'])

                if search_criteria.get('end_date'):
                    query += " AND DATE(si.invoice_date) <= ?"
                    params.append(search_criteria['end_date'])

                # فلترة بحالة الدفع
                if search_criteria.get('payment_status'):
                    query += " AND si.payment_status = ?"
                    params.append(search_criteria['payment_status'])

                # فلترة بالعميل
                if search_criteria.get('customer_id'):
                    query += " AND si.customer_id = ?"
                    params.append(search_criteria['customer_id'])

                query += " ORDER BY si.invoice_date DESC"

                # تحديد الحد الأقصى للنتائج
                limit = search_criteria.get('limit', 100)
                query += " LIMIT ?"
                params.append(limit)

                cursor.execute(query, params)
                invoices = cursor.fetchall()

                return [dict(invoice) for invoice in invoices]

        except Exception as e:
            self.logger.error(f"خطأ في البحث في الفواتير: {e}")
            return []

    def get_sales_summary(self, start_date: str, end_date: str) -> Dict:
        """ملخص المبيعات لفترة محددة"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # إجمالي المبيعات
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_invoices,
                        SUM(CASE WHEN payment_status != 'cancelled' THEN net_amount ELSE 0 END) as total_sales,
                        SUM(CASE WHEN payment_status = 'paid' THEN net_amount ELSE 0 END) as paid_amount,
                        SUM(CASE WHEN payment_status = 'pending' THEN net_amount ELSE 0 END) as pending_amount,
                        AVG(CASE WHEN payment_status != 'cancelled' THEN net_amount ELSE NULL END) as average_sale
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
                      AND si.payment_status != 'cancelled'
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
                        SUM(CASE WHEN payment_status != 'cancelled' THEN net_amount ELSE 0 END) as daily_sales
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
            self.logger.error(f"خطأ في ملخص المبيعات: {e}")
            return {}

    def _validate_invoice_data(self, invoice_data: Dict) -> Dict:
        """التحقق من صحة بيانات الفاتورة"""
        errors = []

        # التحقق من وجود أصناف
        if not invoice_data.get('items') or len(invoice_data['items']) == 0:
            errors.append("يجب إضافة صنف واحد على الأقل")

        # التحقق من صحة بيانات الأصناف
        for i, item in enumerate(invoice_data.get('items', [])):
            if not item.get('product_id'):
                errors.append(f"معرف المنتج مطلوب في السطر {i+1}")

            if not isinstance(item.get('quantity'), (int, float)) or item.get('quantity') <= 0:
                errors.append(f"كمية صحيحة مطلوبة في السطر {i+1}")

            if not isinstance(item.get('unit_price'), (int, float)) or item.get('unit_price') <= 0:
                errors.append(f"سعر صحيح مطلوب في السطر {i+1}")

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def _calculate_totals(self, items: List[Dict], discount_percent: float = 0, 
                         tax_percent: float = 0) -> Dict:
        """حساب إجماليات الفاتورة"""
        subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
        discount_amount = subtotal * (discount_percent / 100)
        taxable_amount = subtotal - discount_amount
        tax_amount = taxable_amount * (tax_percent / 100)
        net_amount = taxable_amount + tax_amount

        return {
            'subtotal': round(subtotal, 2),
            'discount_amount': round(discount_amount, 2),
            'tax_amount': round(tax_amount, 2),
            'net_amount': round(net_amount, 2)
        }

    def _generate_invoice_number(self) -> str:
        """إنشاء رقم فاتورة فريد"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"INV{timestamp}"
