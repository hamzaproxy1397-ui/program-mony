# -*- coding: utf-8 -*-
"""
مدير المشتريات
"""

import logging
import time
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
from database.database_manager import DatabaseManager
from database.journal_entries_manager import JournalEntriesManager
from database.accounts_manager import AccountsManager

class PurchasesManager:
    """مدير المشتريات مع تكامل النظام المحاسبي"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db_manager = db_manager or DatabaseManager()
        self.journal_manager = JournalEntriesManager(self.db_manager)
        self.accounts_manager = AccountsManager(self.db_manager)
        self.logger = logging.getLogger(__name__)

    def save_purchase_invoice(self, supplier_data: Dict, items: List[Dict],
                            invoice_data: Dict) -> Dict:
        """حفظ فاتورة شراء"""
        try:
            # التحقق من صحة البيانات
            validation = self._validate_purchase_data(supplier_data, items, invoice_data)
            if not validation['is_valid']:
                return {
                    'success': False,
                    'errors': validation['errors']
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # التحقق من وجود المورد أو إنشاؤه
                supplier_id = self._get_or_create_supplier(cursor, supplier_data)

                # إنشاء فاتورة الشراء
                cursor.execute('''
                    INSERT INTO purchase_invoices 
                    (invoice_number, supplier_id, invoice_date, total_amount, 
                    discount_amount, tax_amount, net_amount, payment_status, notes, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    invoice_data.get('invoice_number', self._generate_invoice_number()),
                    supplier_id,
                    invoice_data.get('invoice_date', date.today()),
                    invoice_data['total_amount'],
                    invoice_data.get('discount_amount', 0),
                    invoice_data.get('tax_amount', 0),
                    invoice_data['net_amount'],
                    invoice_data.get('payment_status', 'pending'),
                    invoice_data.get('notes', ''),
                    invoice_data.get('created_by', 1)
                ))

                invoice_id = cursor.lastrowid

                # إضافة تفاصيل الفاتورة
                for item in items:
                    # التحقق من وجود المنتج أو إنشاؤه
                    product_id = self._get_or_create_product(cursor, item)

                    cursor.execute('''
                        INSERT INTO purchase_invoice_items 
                        (invoice_id, product_id, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        invoice_id,
                        product_id,
                        item['quantity'],
                        item['unit_price'],
                        item['total_price']
                    ))

                conn.commit()

                # تحديث المخزون
                inventory_result = self._update_inventory(items, 'purchase')
                if not inventory_result['success']:
                    self.logger.warning(f"فشل في تحديث المخزون: {inventory_result['errors']}")

                # إنشاء القيد المحاسبي
                journal_result = self._create_purchase_journal_entry(
                    invoice_id, supplier_data, invoice_data, items
                )

                self.logger.info(f"تم حفظ فاتورة الشراء: {invoice_data.get('invoice_number')}")

                return {
                    'success': True,
                    'invoice_id': invoice_id,
                    'invoice_number': invoice_data.get('invoice_number'),
                    'journal_entry': journal_result,
                    'message': 'تم حفظ فاتورة الشراء بنجاح'
                }

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في حفظ فاتورة الشراء: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في حفظ فاتورة الشراء: {str(e)}']
            }

    def get_purchase_invoice(self, invoice_id: int) -> Optional[Dict]:
        """جلب فاتورة شراء"""
        try:
            query = """
                SELECT pi.*, s.name as supplier_name, s.phone as supplier_phone
                FROM purchase_invoices pi
                LEFT JOIN suppliers s ON pi.supplier_id = s.id
                WHERE pi.id = ?
            """
            invoice = self.db_manager.fetch_one(query, (invoice_id,))

            if not invoice:
                return None

            invoice_dict = dict(invoice)

            # جلب تفاصيل الفاتورة
            items_query = """
                SELECT pii.*, p.name as product_name, p.barcode
                FROM purchase_invoice_items pii
                JOIN products p ON pii.product_id = p.id
                WHERE pii.invoice_id = ?
            """
            items = self.db_manager.fetch_all(items_query, (invoice_id,))
            invoice_dict['items'] = [dict(item) for item in items]

            return invoice_dict

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في جلب فاتورة الشراء: {e}")
            return None

    def get_all_purchase_invoices(self, start_date: date = None, end_date: date = None,
                                supplier_id: int = None) -> List[Dict]:
        """جلب جميع فواتير الشراء"""
        try:
            query = """
                SELECT pi.*, s.name as supplier_name
                FROM purchase_invoices pi
                LEFT JOIN suppliers s ON pi.supplier_id = s.id
                WHERE 1=1
            """
            params = []

            if start_date:
                query += " AND pi.invoice_date >= ?"
                params.append(start_date)

            if end_date:
                query += " AND pi.invoice_date <= ?"
                params.append(end_date)

            if supplier_id:
                query += " AND pi.supplier_id = ?"
                params.append(supplier_id)

            query += " ORDER BY pi.invoice_date DESC, pi.id DESC"

            invoices = self.db_manager.fetch_all(query, params)
            return [dict(invoice) for invoice in invoices]

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في جلب فواتير الشراء: {e}")
            return []

    def _validate_purchase_data(self, supplier_data: Dict, items: List[Dict],
                                invoice_data: Dict) -> Dict:
        """التحقق من صحة بيانات الشراء"""
        errors = []

        # التحقق من بيانات المورد
        if not supplier_data.get('name', '').strip():
            errors.append('اسم المورد مطلوب')

        # التحقق من الأصناف
        if not items:
            errors.append('يجب إضافة صنف واحد على الأقل')

        for i, item in enumerate(items, 1):
            if not item.get('name', '').strip():
                errors.append(f'اسم الصنف مطلوب في السطر {i}')

            if item.get('quantity', 0) <= 0:
                errors.append(f'الكمية يجب أن تكون أكبر من صفر في السطر {i}')

            if item.get('unit_price', 0) <= 0:
                errors.append(f'سعر الوحدة يجب أن يكون أكبر من صفر في السطر {i}')

        # التحقق من بيانات الفاتورة
        if invoice_data.get('total_amount', 0) <= 0:
            errors.append('إجمالي الفاتورة يجب أن يكون أكبر من صفر')

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def _get_or_create_supplier(self, cursor, supplier_data: Dict) -> int:
        """الحصول على معرف المورد أو إنشاؤه"""
        # البحث عن المورد
        cursor.execute("SELECT id FROM suppliers WHERE name = ?", (supplier_data['name'],))
        supplier = cursor.fetchone()

        if supplier:
            return supplier['id']

        # إنشاء مورد جديد
        cursor.execute('''
            INSERT INTO suppliers (name, phone, email, address, is_active)
            VALUES (?, ?, ?, ?, 1)
        ''', (
            supplier_data['name'],
            supplier_data.get('phone', ''),
            supplier_data.get('email', ''),
            supplier_data.get('address', '')
        ))

        return cursor.lastrowid

    def _get_or_create_product(self, cursor, item: Dict) -> int:
        """الحصول على معرف المنتج أو إنشاؤه"""
        # البحث عن المنتج
        cursor.execute("SELECT id FROM products WHERE name = ?", (item['name'],))
        product = cursor.fetchone()

        if product:
            return product['id']

        # إنشاء منتج جديد
        barcode = item.get('barcode', '')
        if not barcode:
            # توليد باركود فريد إذا لم يكن موجود
            import time
            barcode = f"PRD{int(time.time())}{cursor.lastrowid or 0}"

        cursor.execute('''
            INSERT INTO products (name, barcode, cost_price, selling_price, current_stock, is_active)
            VALUES (?, ?, ?, ?, 0, 1)
        ''', (
            item['name'],
            barcode,
            item['unit_price'],
            item.get('selling_price', item['unit_price'] * 1.2)  # هامش ربح افتراضي 20%
        ))

        return cursor.lastrowid

    def _update_inventory(self, items: List[Dict], operation_type: str) -> Dict:
        """تحديث المخزون"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                for item in items:
                    # البحث عن المنتج
                    cursor.execute("SELECT id, current_stock FROM products WHERE name = ?", 
                                (item['name'],))
                    product = cursor.fetchone()

                    if product:
                        if operation_type == 'purchase':
                            # زيادة المخزون عند الشراء
                            new_stock = product['current_stock'] + item['quantity']
                        else:
                            # تقليل المخزون عند البيع أو الإرجاع
                            new_stock = product['current_stock'] - item['quantity']

                        cursor.execute('''
                            UPDATE products
                            SET current_stock = ?, cost_price = ?
                            WHERE id = ?
                        ''', (new_stock, item['unit_price'], product['id']))

                        # تسجيل حركة المخزون
                        cursor.execute('''
                            INSERT INTO inventory_movements 
                            (product_id, movement_type, quantity, reference_type, notes)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            product['id'],
                            'in' if operation_type == 'purchase' else 'out',
                            item['quantity'],
                            'purchase_invoice',
                            f"شراء من فاتورة رقم {item.get('invoice_number', '')}"
                        ))

                conn.commit()

                return {
                    'success': True,
                    'message': 'تم تحديث المخزون بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في تحديث المخزون: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في تحديث المخزون: {str(e)}']
            }

    def _create_purchase_journal_entry(self, invoice_id: int, supplier_data: Dict,
                                    invoice_data: Dict, items: List[Dict]) -> Dict:
        """إنشاء القيد المحاسبي لفاتورة الشراء"""
        try:
            # البحث عن الحسابات المطلوبة
            inventory_account = self.accounts_manager.get_account_by_code('1130')  # المخزون
            suppliers_account = self.accounts_manager.get_account_by_code('2110')  # الموردون

            if not inventory_account or not suppliers_account:
                return {
                    'success': False,
                    'errors': ['لم يتم العثور على الحسابات المطلوبة']
                }

            # إعداد تفاصيل القيد
            entry_details = [
                {
                    'account_id': inventory_account['id'],
                    'description': f'شراء بضاعة من {supplier_data["name"]}',
                    'debit_amount': invoice_data['net_amount'],
                    'credit_amount': 0
                },
                {
                    'account_id': suppliers_account['id'],
                    'description': f'مديونية للمورد {supplier_data["name"]}',
                    'debit_amount': 0,
                    'credit_amount': invoice_data['net_amount']
                }
            ]

            # إنشاء القيد
            entry_data = {
                'entry_date': invoice_data.get('invoice_date', date.today()),
                'description': f'قيد شراء - فاتورة رقم {invoice_data.get("invoice_number")}',
                'reference_type': 'purchase_invoice',
                'reference_id': invoice_id,
                'details': entry_details,
                'created_by': invoice_data.get('created_by', 1)
            }

            return self.journal_manager.create_journal_entry(entry_data)

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء القيد المحاسبي: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في إنشاء القيد المحاسبي: {str(e)}']
            }

    def _generate_invoice_number(self) -> str:
        """توليد رقم فاتورة"""
        try:
            query = "SELECT MAX(CAST(SUBSTR(invoice_number, 3) AS INTEGER)) FROM purchase_invoices WHERE invoice_number LIKE 'PI%'"
            result = self.db_manager.fetch_one(query)

            last_number = result[0] if result and result[0] else 0
            new_number = last_number + 1

            return f"PI{new_number:06d}"

        except Exception as e:
            pass
        except Exception as e:
            self.logger.error(f"خطأ في توليد رقم الفاتورة: {e}")
            return f"PI{int(datetime.now().timestamp())}"
