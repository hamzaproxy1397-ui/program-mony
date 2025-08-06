# -*- coding: utf-8 -*-
"""
مدير قاعدة بيانات SQL Server
"""

import pyodbc
import logging
import hashlib
from datetime import datetime
from config.settings import PROJECT_ROOT
from typing import Dict
from typing import List
from typing import Optional
from typing import List, Dict, Optional, Tuple, Any, Union, Callable
import sys


class SQLServerManager:
    """مدير قاعدة بيانات SQL Server"""

    def __init__(self, config: Dict = None):
        """
        تهيئة مدير SQL Server

        Args:
            config: إعدادات الاتصال بقاعدة البيانات
        """
        self.logger = logging.getLogger(__name__)

        # إعدادات الاتصال الافتراضية
        self.config = config or {
            'server': 'localhost',
            'database': 'AccountingDB',
            'driver': '{ODBC Driver 17 for SQL Server}',
            'trusted_connection': 'yes',  # استخدام Windows Authentication
            'timeout': 30
        }

        self.connection_string = self._build_connection_string()
        self.logger.info("تم تهيئة مدير SQL Server")

        # إنشاء قاعدة البيانات والجداول
        self.init_database()

    def _build_connection_string(self) -> str:
        """بناء نص الاتصال بقاعدة البيانات"""
        try:
            if self.config.get('username') and self.config.get('password'):
                # SQL Server Authentication
                conn_str = (
                    f"DRIVER={self.config['driver']};"
                    f"SERVER={self.config['server']};"
                    f"DATABASE={self.config['database']};"
                    f"UID={self.config['username']};"
                    f"PWD={self.config['password']};"
                    f"TIMEOUT={self.config.get('timeout', 30)};"
                )
            else:
                # Windows Authentication
                conn_str = (
                    f"DRIVER={self.config['driver']};"
                    f"SERVER={self.config['server']};"
                    f"DATABASE={self.config['database']};"
                    f"Trusted_Connection={self.config.get('trusted_connection', 'yes')};"
                    f"TIMEOUT={self.config.get('timeout', 30)};"
                )

            return conn_str

        except Exception as e:
            self.logger.error(f"خطأ في بناء نص الاتصال: {e}")
            raise

    def get_connection(self):
        """إنشاء اتصال جديد بقاعدة البيانات"""
        try:
            conn = pyodbc.connect(self.connection_string)
            conn.timeout = self.config.get('timeout', 30)
            return conn
        except Exception as e:
            self.logger.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
            raise

    def test_connection(self) -> bool:
        """اختبار الاتصال بقاعدة البيانات"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.logger.info("تم اختبار الاتصال بنجاح")
                return result[0] == 1
        except Exception as e:
            self.logger.error(f"فشل في اختبار الاتصال: {e}")
            return False

    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        try:
            # أولاً، محاولة إنشاء قاعدة البيانات
            self._create_database_if_not_exists()

            # ثم إنشاء الجداول
            self._create_tables()

            self.logger.info("تم إنشاء قاعدة البيانات والجداول بنجاح")

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء قاعدة البيانات: {e}")
            raise

    def _create_database_if_not_exists(self):
        """إنشاء قاعدة البيانات إذا لم تكن موجودة"""
        try:
            # الاتصال بقاعدة البيانات الرئيسية لإنشاء قاعدة البيانات الجديدة
            master_config = self.config.copy()
            master_config['database'] = 'master'

            if master_config.get('username') and master_config.get('password'):
                master_conn_str = (
                    f"DRIVER={master_config['driver']};"
                    f"SERVER={master_config['server']};"
                    f"DATABASE=master;"
                    f"UID={master_config['username']};"
                    f"PWD={master_config['password']};"
                )
            else:
                master_conn_str = (
                    f"DRIVER={master_config['driver']};"
                    f"SERVER={master_config['server']};"
                    f"DATABASE=master;"
                    f"Trusted_Connection=yes;"
                )

            with pyodbc.connect(master_conn_str) as conn:
                cursor = conn.cursor()

                # التحقق من وجود قاعدة البيانات
                cursor.execute("""
                    SELECT database_id FROM sys.databases 
                    WHERE name = ?
                """, (self.config['database'],))

                if not cursor.fetchone():
                    # إنشاء قاعدة البيانات
                    cursor.execute(f"""
                        CREATE DATABASE [{self.config['database']}]
                        COLLATE Arabic_CI_AS
                    """)
                    conn.commit()
                    self.logger.info(f"تم إنشاء قاعدة البيانات: {self.config['database']}")

        except Exception as e:
            self.logger.warning(f"تحذير في إنشاء قاعدة البيانات: {e}")
            # المتابعة حتى لو فشل إنشاء قاعدة البيانات (قد تكون موجودة بالفعل)

    def _create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # جدول المستخدمين
                cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
                    CREATE TABLE users (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        username NVARCHAR(50) UNIQUE NOT NULL,
                        password_hash NVARCHAR(255) NOT NULL,
                        full_name NVARCHAR(100) NOT NULL,
                        email NVARCHAR(100),
                        role NVARCHAR(20) DEFAULT 'user',
                        is_active BIT DEFAULT 1,
                        created_at DATETIME2 DEFAULT GETDATE(),
                        last_login DATETIME2
                    )
                ''')

                # جدول العملاء
                cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='customers' AND xtype='U')
                    CREATE TABLE customers (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        name NVARCHAR(100) NOT NULL,
                        phone NVARCHAR(20),
                        email NVARCHAR(100),
                        address NVARCHAR(255),
                        tax_number NVARCHAR(50),
                        is_active BIT DEFAULT 1,
                        created_at DATETIME2 DEFAULT GETDATE(),
                        updated_at DATETIME2 DEFAULT GETDATE()
                    )
                ''')

                # جدول المنتجات
                cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='products' AND xtype='U')
                    CREATE TABLE products (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        name NVARCHAR(100) NOT NULL,
                        description NVARCHAR(255),
                        barcode NVARCHAR(50) UNIQUE,
                        category NVARCHAR(50),
                        unit NVARCHAR(20) DEFAULT N'قطعة',
                        cost_price DECIMAL(10,2) DEFAULT 0,
                        selling_price DECIMAL(10,2) NOT NULL,
                        stock_quantity INT DEFAULT 0,
                        min_stock_level INT DEFAULT 0,
                        is_active BIT DEFAULT 1,
                        created_at DATETIME2 DEFAULT GETDATE(),
                        updated_at DATETIME2 DEFAULT GETDATE()
                    )
                ''')

                # جدول فواتير المبيعات
                cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sales_invoices' AND xtype='U')
                    CREATE TABLE sales_invoices (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        invoice_number NVARCHAR(50) UNIQUE NOT NULL,
                        customer_id INT,
                        customer_name NVARCHAR(100),
                        total_amount DECIMAL(10,2) NOT NULL,
                        tax_amount DECIMAL(10,2) DEFAULT 0,
                        discount_amount DECIMAL(10,2) DEFAULT 0,
                        net_amount DECIMAL(10,2) NOT NULL,
                        payment_method NVARCHAR(20) DEFAULT N'نقدي',
                        status NVARCHAR(20) DEFAULT N'مكتملة',
                        notes NVARCHAR(255),
                        created_by INT,
                        created_at DATETIME2 DEFAULT GETDATE(),
                        FOREIGN KEY (customer_id) REFERENCES customers(id),
                        FOREIGN KEY (created_by) REFERENCES users(id)
                    )
                ''')

                # جدول عناصر الفواتير
                cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='invoice_items' AND xtype='U')
                    CREATE TABLE invoice_items (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        invoice_id INT NOT NULL,
                        product_id INT NOT NULL,
                        product_name NVARCHAR(100) NOT NULL,
                        quantity INT NOT NULL,
                        unit_price DECIMAL(10,2) NOT NULL,
                        total_price DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (invoice_id) REFERENCES sales_invoices(id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(id)
                    )
                ''')

                # جدول حركات المخزون
                cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='inventory_movements' AND xtype='U')
                    CREATE TABLE inventory_movements (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        product_id INT NOT NULL,
                        movement_type NVARCHAR(20) NOT NULL,
                        quantity INT NOT NULL,
                        reference_type NVARCHAR(20),
                        reference_id INT,
                        notes NVARCHAR(255),
                        created_by INT,
                        created_at DATETIME2 DEFAULT GETDATE(),
                        FOREIGN KEY (product_id) REFERENCES products(id),
                        FOREIGN KEY (created_by) REFERENCES users(id)
                    )
                ''')

                conn.commit()
                self.logger.info("تم إنشاء جميع الجداول بنجاح")

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الجداول: {e}")
            raise

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """تنفيذ استعلام وإرجاع النتائج"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # الحصول على أسماء الأعمدة
                columns = [column[0] for column in cursor.description] if cursor.description else []

                # تحويل النتائج إلى قائمة من القواميس
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))

                return results

        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ الاستعلام: {e}")
            raise

    def execute_non_query(self, query: str, params: tuple = None) -> int:
        """تنفيذ استعلام بدون إرجاع نتائج (INSERT, UPDATE, DELETE)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                conn.commit()
                return cursor.rowcount

        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ الاستعلام: {e}")
            raise

    def backup_database(self, backup_path: str = None) -> Optional[str]:
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_dir = PROJECT_ROOT / "backups"
                backup_dir.mkdir(exist_ok=True)
                backup_path = backup_dir / f"sqlserver_backup_{timestamp}.bak"

            with self.get_connection() as conn:
                cursor = conn.cursor()

                backup_query = f"""
                    BACKUP DATABASE [{self.config['database']}] 
                    TO DISK = '{backup_path}'
                    WITH FORMAT, INIT, COMPRESSION
                """

                cursor.execute(backup_query)
                conn.commit()

                self.logger.info(f"تم إنشاء النسخة الاحتياطية: {backup_path}")
                return str(backup_path)

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
            return None

    def create_default_admin(self):
        """إنشاء مستخدم المدير الافتراضي"""
        try:
            # التحقق من وجود مستخدم admin
            existing_admin = self.execute_query(
                "SELECT id FROM users WHERE username = ?", 
                ('admin',)
            )

            if not existing_admin:
                # إنشاء كلمة مرور مشفرة
                password_hash = hashlib.sha256('123'.encode()).hexdigest()

                self.execute_non_query("""
                    INSERT INTO users (username, password_hash, full_name, role, is_active)
                    VALUES (?, ?, ?, ?, ?)
                """, ('123', password_hash, 'مدير النظام', 'admin', 1))

                self.logger.info("تم إنشاء مستخدم المدير الافتراضي")

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء المستخدم الافتراضي: {e}")

    def get_database_info(self) -> Dict:
        """الحصول على معلومات قاعدة البيانات"""
        try:
            info = {}

            # معلومات قاعدة البيانات
            db_info = self.execute_query("""
                SELECT 
                    name,
                    database_id,
                    create_date,
                    collation_name
                FROM sys.databases 
                WHERE name = ?
            """, (self.config['database'],))

            if db_info:
                info['database'] = db_info[0]

            # معلومات الجداول
            tables_info = self.execute_query("""
                SELECT 
                    TABLE_NAME,
                    TABLE_TYPE
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """)

            info['tables'] = tables_info
            info['table_count'] = len(tables_info)

            return info

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على معلومات قاعدة البيانات: {e}")
            return {}
