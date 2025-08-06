# -*- coding: utf-8 -*-
"""
مدير قاعدة البيانات للفواتير - إدارة شاملة لجداول الفواتير والعمليات
"""

import sqlite3
import os
from datetime import datetime, date
from pathlib import Path
import logging


class InvoicesDatabaseManager:
    """مدير قاعدة البيانات للفواتير"""

    def __init__(self, db_path=None):
        if db_path is None:
            # استخدام مسار افتراضي
            project_root = Path(__file__).parent.parent
            db_path = project_root / "database" / "invoices.db"

        self.db_path = db_path
        self.ensure_database_directory()
        self.init_database()

        # إعداد نظام السجلات
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def ensure_database_directory(self):
        """التأكد من وجود مجلد قاعدة البيانات"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
        return conn

    def init_database(self):
        """إنشاء جداول قاعدة البيانات للفواتير"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # جدول العملاء
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_code TEXT UNIQUE NOT NULL,
                        name_ar TEXT NOT NULL,
                        name_en TEXT,
                        phone TEXT,
                        email TEXT,
                        address TEXT,
                        customer_type TEXT DEFAULT 'cash' CHECK (customer_type IN ('cash', 'credit', 'vip')),
                        credit_limit DECIMAL(15,2) DEFAULT 0,
                        current_balance DECIMAL(15,2) DEFAULT 0,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # جدول الموردين
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS suppliers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        supplier_code TEXT UNIQUE NOT NULL,
                        name_ar TEXT NOT NULL,
                        name_en TEXT,
                        phone TEXT,
                        email TEXT,
                        address TEXT,
                        contact_person TEXT,
                        payment_terms TEXT,
                        current_balance DECIMAL(15,2) DEFAULT 0,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # جدول الأصناف/المنتجات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_code TEXT UNIQUE NOT NULL,
                        barcode TEXT UNIQUE,
                        name_ar TEXT NOT NULL,
                        name_en TEXT,
                        category_id INTEGER,
                        unit_id INTEGER,
                        cost_price DECIMAL(10,2) DEFAULT 0,
                        sale_price DECIMAL(10,2) DEFAULT 0,
                        wholesale_price DECIMAL(10,2) DEFAULT 0,
                        min_quantity INTEGER DEFAULT 0,
                        max_quantity INTEGER DEFAULT 0,
                        current_stock INTEGER DEFAULT 0,
                        vat_rate DECIMAL(5,2) DEFAULT 0,
                        is_service BOOLEAN DEFAULT 0,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # جدول الفواتير الرئيسي
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_number TEXT UNIQUE NOT NULL,
                        invoice_type TEXT NOT NULL CHECK (invoice_type IN ('sale', 'purchase', 'sale_return', 'purchase_return', 'pos', 'quick')),
                        invoice_date DATE NOT NULL,
                        customer_id INTEGER,
                        supplier_id INTEGER,
                        warehouse_id INTEGER DEFAULT 1,
                        subtotal DECIMAL(15,2) DEFAULT 0,
                        discount_amount DECIMAL(15,2) DEFAULT 0,
                        discount_percentage DECIMAL(5,2) DEFAULT 0,
                        tax_amount DECIMAL(15,2) DEFAULT 0,
                        tax_percentage DECIMAL(5,2) DEFAULT 0,
                        total_amount DECIMAL(15,2) NOT NULL,
                        paid_amount DECIMAL(15,2) DEFAULT 0,
                        remaining_amount DECIMAL(15,2) DEFAULT 0,
                        payment_method TEXT DEFAULT 'cash' CHECK (payment_method IN ('cash', 'credit', 'card', 'transfer', 'mixed')),
                        payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'partial', 'paid', 'overdue')),
                        invoice_status TEXT DEFAULT 'active' CHECK (invoice_status IN ('active', 'cancelled', 'returned', 'deleted')),
                        notes TEXT,
                        created_by INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        deleted_at TIMESTAMP NULL,
                        deleted_by INTEGER NULL,
                        delete_reason TEXT NULL,
                        FOREIGN KEY (customer_id) REFERENCES customers (id),
                        FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
                        FOREIGN KEY (created_by) REFERENCES users (id),
                        FOREIGN KEY (deleted_by) REFERENCES users (id)
                    )
                ''')

                # جدول تفاصيل الفواتير
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoice_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity DECIMAL(10,3) NOT NULL,
                        unit_price DECIMAL(10,2) NOT NULL,
                        discount_amount DECIMAL(10,2) DEFAULT 0,
                        discount_percentage DECIMAL(5,2) DEFAULT 0,
                        tax_amount DECIMAL(10,2) DEFAULT 0,
                        tax_percentage DECIMAL(5,2) DEFAULT 0,
                        line_total DECIMAL(15,2) NOT NULL,
                        cost_price DECIMAL(10,2) DEFAULT 0,
                        profit_amount DECIMAL(15,2) DEFAULT 0,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products (id)
                    )
                ''')

                # جدول المدفوعات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoice_payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER NOT NULL,
                        payment_date DATE NOT NULL,
                        payment_amount DECIMAL(15,2) NOT NULL,
                        payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'card', 'transfer', 'check')),
                        reference_number TEXT,
                        notes TEXT,
                        created_by INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                ''')

                # جدول حركات المخزون
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stock_movements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER NOT NULL,
                        warehouse_id INTEGER DEFAULT 1,
                        movement_type TEXT NOT NULL CHECK (movement_type IN ('in', 'out', 'adjustment', 'transfer')),
                        quantity DECIMAL(10,3) NOT NULL,
                        unit_cost DECIMAL(10,2) DEFAULT 0,
                        reference_type TEXT NOT NULL CHECK (reference_type IN ('invoice', 'adjustment', 'transfer', 'opening')),
                        reference_id INTEGER,
                        movement_date DATE NOT NULL,
                        notes TEXT,
                        created_by INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products (id),
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                ''')

                # جدول أرقام الفواتير التسلسلية
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoice_sequences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_type TEXT UNIQUE NOT NULL,
                        prefix TEXT NOT NULL,
                        current_number INTEGER DEFAULT 0,
                        format_pattern TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # إدراج البيانات الافتراضية لأرقام الفواتير
                cursor.execute('''
                    INSERT OR IGNORE INTO invoice_sequences (invoice_type, prefix, current_number, format_pattern)
                    VALUES 
                    ('sale', 'SAL', 0, 'SAL-{year}-{month}-{number:05d}'),
                    ('purchase', 'PUR', 0, 'PUR-{year}-{month}-{number:05d}'),
                    ('sale_return', 'RET-SAL', 0, 'RET-SAL-{year}-{month}-{number:05d}'),
                    ('purchase_return', 'RET-PUR', 0, 'RET-PUR-{year}-{month}-{number:05d}'),
                    ('pos', 'POS', 0, 'POS-{year}{month}{day}-{number:04d}'),
                    ('quick', 'QCK', 0, 'QCK-{year}{month}{day}-{number:04d}')
                ''')

                # إنشاء الفهارس لتحسين الأداء
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(invoice_date)",
                    "CREATE INDEX IF NOT EXISTS idx_invoices_customer ON invoices(customer_id)",
                    "CREATE INDEX IF NOT EXISTS idx_invoices_type ON invoices(invoice_type)",
                    "CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(invoice_status)",
                    "CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice ON invoice_items(invoice_id)",
                    "CREATE INDEX IF NOT EXISTS idx_invoice_items_product ON invoice_items(product_id)",
                    "CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id)",
                    "CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(movement_date)",
                    "CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode)",
                    "CREATE INDEX IF NOT EXISTS idx_products_code ON products(product_code)"
                ]

                for index_sql in indexes:
                    cursor.execute(index_sql)

                conn.commit()
                self.logger.info("تم إنشاء جداول قاعدة البيانات للفواتير بنجاح")

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء قاعدة البيانات: {str(e)}")
            raise

    def generate_invoice_number(self, invoice_type):
        """توليد رقم فاتورة تلقائي"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # الحصول على معلومات التسلسل
                cursor.execute(
                    "SELECT prefix, current_number, format_pattern FROM invoice_sequences WHERE invoice_type = ?",
                    (invoice_type,)
                )
                sequence = cursor.fetchone()

                if not sequence:
                    raise ValueError(f"نوع الفاتورة غير مدعوم: {invoice_type}")

                # زيادة الرقم
                new_number = sequence['current_number'] + 1

                # تحديث التسلسل
                cursor.execute(
                    "UPDATE invoice_sequences SET current_number = ?, updated_at = CURRENT_TIMESTAMP WHERE invoice_type = ?",
                    (new_number, invoice_type)
                )

                # تكوين رقم الفاتورة
                now = datetime.now()
                invoice_number = sequence['format_pattern'].format(
                    year=now.year,
                    month=f"{now.month:02d}",
                    day=f"{now.day:02d}",
                    number=new_number
                )

                conn.commit()
                return invoice_number

        except Exception as e:
            self.logger.error(f"خطأ في توليد رقم الفاتورة: {str(e)}")
            raise

    def save_invoice(self, invoice_data, items_data):
        """حفظ فاتورة جديدة"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # إدراج الفاتورة الرئيسية
                cursor.execute('''
                    INSERT INTO invoices (
                        invoice_number, invoice_type, invoice_date, customer_id, supplier_id,
                        warehouse_id, subtotal, discount_amount, discount_percentage,
                        tax_amount, tax_percentage, total_amount, paid_amount, remaining_amount,
                        payment_method, payment_status, notes, created_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    invoice_data['invoice_number'], invoice_data['invoice_type'],
                    invoice_data['invoice_date'], invoice_data.get('customer_id'),
                    invoice_data.get('supplier_id'), invoice_data.get('warehouse_id', 1),
                    invoice_data['subtotal'], invoice_data.get('discount_amount', 0),
                    invoice_data.get('discount_percentage', 0), invoice_data.get('tax_amount', 0),
                    invoice_data.get('tax_percentage', 0), invoice_data['total_amount'],
                    invoice_data.get('paid_amount', 0), invoice_data.get('remaining_amount', 0),
                    invoice_data.get('payment_method', 'cash'),
                    invoice_data.get('payment_status', 'pending'),
                    invoice_data.get('notes'), invoice_data['created_by']
                ))

                invoice_id = cursor.lastrowid

                # إدراج تفاصيل الفاتورة
                for item in items_data:
                    cursor.execute('''
                        INSERT INTO invoice_items (
                            invoice_id, product_id, quantity, unit_price, discount_amount,
                            discount_percentage, tax_amount, tax_percentage, line_total,
                            cost_price, profit_amount, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        invoice_id, item['product_id'], item['quantity'], item['unit_price'],
                        item.get('discount_amount', 0), item.get('discount_percentage', 0),
                        item.get('tax_amount', 0), item.get('tax_percentage', 0),
                        item['line_total'], item.get('cost_price', 0),
                        item.get('profit_amount', 0), item.get('notes')
                    ))

                    # تحديث المخزون (للمبيعات والمشتريات)
                    if invoice_data['invoice_type'] in ['sale', 'pos', 'quick']:
                        # خصم من المخزون
                        self.update_stock(item['product_id'], -item['quantity'], 
                                        'out', 'invoice', invoice_id, invoice_data['created_by'])
                    elif invoice_data['invoice_type'] == 'purchase':
                        # إضافة للمخزون
                        self.update_stock(item['product_id'], item['quantity'], 
                                        'in', 'invoice', invoice_id, invoice_data['created_by'])

                conn.commit()
                self.logger.info(f"تم حفظ الفاتورة بنجاح: {invoice_data['invoice_number']}")
                return {'success': True, 'invoice_id': invoice_id, 'invoice_number': invoice_data['invoice_number']}

        except Exception as e:
            self.logger.error(f"خطأ في حفظ الفاتورة: {str(e)}")
            return {'success': False, 'error': str(e)}

    def update_stock(self, product_id, quantity, movement_type, reference_type, reference_id, created_by):
        """تحديث المخزون"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # إدراج حركة المخزون
                cursor.execute('''
                    INSERT INTO stock_movements (
                        product_id, movement_type, quantity, reference_type, reference_id,
                        movement_date, created_by
                    ) VALUES (?, ?, ?, ?, ?, DATE('now'), ?)
                ''', (product_id, movement_type, quantity, reference_type, reference_id, created_by))

                # تحديث الكمية الحالية في جدول المنتجات
                cursor.execute('''
                    UPDATE products 
                    SET current_stock = current_stock + ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (quantity, product_id))

                conn.commit()

        except Exception as e:
            self.logger.error(f"خطأ في تحديث المخزون: {str(e)}")
            raise

    def get_invoices_report(self, filters=None):
        """الحصول على تقرير الفواتير"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                query = '''
                    SELECT 
                        i.invoice_number,
                        i.invoice_type,
                        i.invoice_date,
                        COALESCE(c.name_ar, s.name_ar, 'غير محدد') as client_name,
                        i.total_amount,
                        i.payment_status,
                        i.invoice_status,
                        u.username as created_by_name
                    FROM invoices i
                    LEFT JOIN customers c ON i.customer_id = c.id
                    LEFT JOIN suppliers s ON i.supplier_id = s.id
                    LEFT JOIN users u ON i.created_by = u.id
                    WHERE i.invoice_status != 'deleted'
                '''

                params = []

                if filters:
                    if filters.get('from_date'):
                        query += " AND i.invoice_date >= ?"
                        params.append(filters['from_date'])
                    if filters.get('to_date'):
                        query += " AND i.invoice_date <= ?"
                        params.append(filters['to_date'])
                    if filters.get('invoice_type'):
                        query += " AND i.invoice_type = ?"
                        params.append(filters['invoice_type'])
                    if filters.get('customer_id'):
                        query += " AND i.customer_id = ?"
                        params.append(filters['customer_id'])

                query += " ORDER BY i.invoice_date DESC, i.created_at DESC"

                cursor.execute(query, params)
                return cursor.fetchall()

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على تقرير الفواتير: {str(e)}")
            return []


def main():
    """اختبار مدير قاعدة البيانات"""
    db_manager = InvoicesDatabaseManager()
    print("تم إنشاء قاعدة البيانات بنجاح")

    # اختبار توليد رقم فاتورة
    invoice_number = db_manager.generate_invoice_number('sale')
    print(f"رقم الفاتورة المولد: {invoice_number}")


if __name__ == "__main__":
    main()
