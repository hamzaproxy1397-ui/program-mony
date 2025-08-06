# -*- coding: utf-8 -*-
"""
نموذج العميل
"""

from datetime import datetime
from database.database_manager import DatabaseManager

class Customer:
    """نموذج العميل"""

    def __init__(self, customer_id=None, name=None, phone=None, email=None, 
                 address=None, tax_number=None, credit_limit=0, current_balance=0,
                 customer_type='regular', created_at=None, is_active=True):
        self.id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.tax_number = tax_number
        self.credit_limit = credit_limit
        self.current_balance = current_balance
        self.customer_type = customer_type
        self.created_at = created_at or datetime.now()
        self.is_active = is_active
        self.db = DatabaseManager()

    def save(self):
        """حفظ العميل"""
        try:
            if self.id:
                # تحديث عميل موجود
                query = '''
                    UPDATE customers 
                    SET name=?, phone=?, email=?, address=?, tax_number=?, 
                        credit_limit=?, current_balance=?, customer_type=?, is_active=?
                    WHERE id=?
                '''
                params = (self.name, self.phone, self.email, self.address, 
                         self.tax_number, self.credit_limit, self.current_balance,
                         self.customer_type, self.is_active, self.id)
            else:
                # إنشاء عميل جديد
                query = '''
                    INSERT INTO customers (name, phone, email, address, tax_number, 
                                         credit_limit, current_balance, customer_type, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (self.name, self.phone, self.email, self.address,
                         self.tax_number, self.credit_limit, self.current_balance,
                         self.customer_type, self.is_active)

            self.db.execute_query(query, params)

            if not self.id:
                # الحصول على ID العميل الجديد
                result = self.db.fetch_one("SELECT last_insert_rowid()")
                self.id = result[0]

            return True
        except Exception as e:
            print(f"خطأ في حفظ العميل: {e}")
            return False

    def delete(self):
        """حذف العميل (حذف منطقي)"""
        try:
            if self.id:
                self.db.execute_query(
                    "UPDATE customers SET is_active = 0 WHERE id = ?",
                    (self.id,)
                )
                self.is_active = False
                return True
            return False
        except Exception as e:
            print(f"خطأ في حذف العميل: {e}")
            return False

    @classmethod
    def get_by_id(cls, customer_id):
        """الحصول على عميل بالمعرف"""
        try:
            db = DatabaseManager()
            result = db.fetch_one(
                "SELECT * FROM customers WHERE id = ? AND is_active = 1",
                (customer_id,)
            )

            if result:
                return cls(
                    customer_id=result['id'],
                    name=result['name'],
                    phone=result['phone'],
                    email=result['email'],
                    address=result['address'],
                    tax_number=result['tax_number'],
                    credit_limit=result['credit_limit'],
                    current_balance=result['current_balance'],
                    customer_type=result['customer_type'],
                    created_at=result['created_at'],
                    is_active=result['is_active']
                )
            return None
        except Exception as e:
            print(f"خطأ في جلب العميل: {e}")
            return None

    @classmethod
    def get_all(cls, active_only=True):
        """الحصول على جميع العملاء"""
        try:
            db = DatabaseManager()
            query = "SELECT * FROM customers"
            if active_only:
                query += " WHERE is_active = 1"
            query += " ORDER BY name"

            results = db.fetch_all(query)
            customers = []

            for result in results:
                customer = cls(
                    customer_id=result['id'],
                    name=result['name'],
                    phone=result['phone'],
                    email=result['email'],
                    address=result['address'],
                    tax_number=result['tax_number'],
                    credit_limit=result['credit_limit'],
                    current_balance=result['current_balance'],
                    customer_type=result['customer_type'],
                    created_at=result['created_at'],
                    is_active=result['is_active']
                )
                customers.append(customer)

            return customers
        except Exception as e:
            print(f"خطأ في جلب العملاء: {e}")
            return []

    @classmethod
    def search(cls, search_term):
        """البحث في العملاء"""
        try:
            db = DatabaseManager()
            query = '''
                SELECT * FROM customers 
                WHERE (name LIKE ? OR phone LIKE ? OR email LIKE ?) 
                AND is_active = 1
                ORDER BY name
            '''
            search_pattern = f"%{search_term}%"
            results = db.fetch_all(query, (search_pattern, search_pattern, search_pattern))

            customers = []
            for result in results:
                customer = cls(
                    customer_id=result['id'],
                    name=result['name'],
                    phone=result['phone'],
                    email=result['email'],
                    address=result['address'],
                    tax_number=result['tax_number'],
                    credit_limit=result['credit_limit'],
                    current_balance=result['current_balance'],
                    customer_type=result['customer_type'],
                    created_at=result['created_at'],
                    is_active=result['is_active']
                )
                customers.append(customer)

            return customers
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return []

    def update_balance(self, amount):
        """تحديث رصيد العميل"""
        try:
            self.current_balance += amount
            self.db.execute_query(
                "UPDATE customers SET current_balance = ? WHERE id = ?",
                (self.current_balance, self.id)
            )
            return True
        except Exception as e:
            print(f"خطأ في تحديث الرصيد: {e}")
            return False

    def get_transactions(self):
        """الحصول على معاملات العميل"""
        try:
            query = '''
                SELECT si.*, 'sale' as transaction_type
                FROM sales_invoices si
                WHERE si.customer_id = ?
                ORDER BY si.invoice_date DESC
            '''
            results = self.db.fetch_all(query, (self.id,))
            return results
        except Exception as e:
            print(f"خطأ في جلب المعاملات: {e}")
            return []

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'tax_number': self.tax_number,
            'credit_limit': self.credit_limit,
            'current_balance': self.current_balance,
            'customer_type': self.customer_type,
            'created_at': self.created_at,
            'is_active': self.is_active
        }

    def __str__(self):
        return f"العميل: {self.name} - الهاتف: {self.phone}"
