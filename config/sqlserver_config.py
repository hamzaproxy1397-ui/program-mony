# -*- coding: utf-8 -*-
"""
إعدادات قاعدة بيانات SQL Server
"""

import os
from pathlib import Path
import sys

# إعدادات الاتصال بـ SQL Server
SQLSERVER_CONFIG = {
    # معلومات الخادم
    'server': os.getenv('SQLSERVER_HOST', 'localhost'),
    'port': int(os.getenv('SQLSERVER_PORT', 1433)),
    'database': os.getenv('SQLSERVER_DATABASE', 'AccountingDB'),

    # إعدادات المصادقة
    'authentication_type': 'windows',  # 'windows' أو 'sql'
    'username': os.getenv('SQLSERVER_USER', ''),
    'password': os.getenv('SQLSERVER_PASSWORD', ''),

    # إعدادات الاتصال
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'yes',
    'timeout': 30,
    'connection_timeout': 30,
    'command_timeout': 30,

    # إعدادات الأمان
    'encrypt': 'no',  # 'yes' للاتصالات المشفرة
    'trust_server_certificate': 'yes',

    # إعدادات الأداء
    'pooling': True,
    'max_pool_size': 100,
    'min_pool_size': 5,

    # إعدادات اللغة والترميز
    'charset': 'utf8',
    'collation': 'Arabic_CI_AS'
}

# إعدادات النسخ الاحتياطي
BACKUP_CONFIG = {
    'backup_directory': 'backups/sqlserver',
    'backup_filename_format': 'sqlserver_backup_{timestamp}.bak',
    'compression': True,
    'verify_backup': True,
    'auto_backup_enabled': True,
    'backup_retention_days': 30
}

# إعدادات الأداء والتحسين
PERFORMANCE_CONFIG = {
    'enable_connection_pooling': True,
    'connection_pool_size': 20,
    'query_timeout': 30,
    'bulk_insert_batch_size': 1000,
    'enable_query_logging': False,
    'log_slow_queries': True,
    'slow_query_threshold': 5.0  # بالثواني
}

# إعدادات الأمان
SECURITY_CONFIG = {
    'enable_sql_injection_protection': True,
    'use_parameterized_queries': True,
    'encrypt_connection': False,
    'certificate_validation': False,
    'enable_audit_logging': True
}

# إعدادات المراقبة
MONITORING_CONFIG = {
    'enable_performance_monitoring': True,
    'log_connection_events': True,
    'log_query_execution_time': True,
    'enable_health_checks': True,
    'health_check_interval': 300  # بالثواني
}

# رسائل النظام
MESSAGES = {
    'connection_success': 'تم الاتصال بـ SQL Server بنجاح',
    'connection_failed': 'فشل في الاتصال بـ SQL Server',
    'database_created': 'تم إنشاء قاعدة البيانات بنجاح',
    'database_exists': 'قاعدة البيانات موجودة بالفعل',
    'tables_created': 'تم إنشاء الجداول بنجاح',
    'backup_success': 'تم إنشاء النسخة الاحتياطية بنجاح',
    'backup_failed': 'فشل في إنشاء النسخة الاحتياطية',
    'query_executed': 'تم تنفيذ الاستعلام بنجاح',
    'query_failed': 'فشل في تنفيذ الاستعلام'
}

# دوال مساعدة
def get_connection_string(auth_type='windows'):
    """بناء نص الاتصال حسب نوع المصادقة"""
    config = SQLSERVER_CONFIG.copy()

    if auth_type == 'windows':
        return (
            f"DRIVER={config['driver']};"
            f"SERVER={config['server']};"
            f"DATABASE={config['database']};"
            f"Trusted_Connection={config['trusted_connection']};"
            f"TIMEOUT={config['timeout']};"
        )
    else:  # SQL Server Authentication
        return (
            f"DRIVER={config['driver']};"
            f"SERVER={config['server']};"
            f"DATABASE={config['database']};"
            f"UID={config['username']};"
            f"PWD={config['password']};"
            f"TIMEOUT={config['timeout']};"
        )

def get_master_connection_string(auth_type='windows'):
    """بناء نص الاتصال بقاعدة البيانات الرئيسية"""
    config = SQLSERVER_CONFIG.copy()

    if auth_type == 'windows':
        return (
            f"DRIVER={config['driver']};"
            f"SERVER={config['server']};"
            f"DATABASE=master;"
            f"Trusted_Connection={config['trusted_connection']};"
            f"TIMEOUT={config['timeout']};"
        )
    else:
        return (
            f"DRIVER={config['driver']};"
            f"SERVER={config['server']};"
            f"DATABASE=master;"
            f"UID={config['username']};"
            f"PWD={config['password']};"
            f"TIMEOUT={config['timeout']};"
        )

def validate_config():
    """التحقق من صحة الإعدادات"""
    errors = []

    if not SQLSERVER_CONFIG['server']:
        errors.append("عنوان الخادم مطلوب")

    if SQLSERVER_CONFIG['authentication_type'] == 'sql':
        if not SQLSERVER_CONFIG['username']:
            errors.append("اسم المستخدم مطلوب لمصادقة SQL Server")
        if not SQLSERVER_CONFIG['password']:
            errors.append("كلمة المرور مطلوبة لمصادقة SQL Server")

    if not SQLSERVER_CONFIG['database']:
        errors.append("اسم قاعدة البيانات مطلوب")

    return errors

def get_backup_path():
    """الحصول على مسار النسخ الاحتياطية"""
    backup_dir = Path(BACKUP_CONFIG['backup_directory'])
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir

def is_windows_auth():
    """التحقق من استخدام مصادقة Windows"""
    return SQLSERVER_CONFIG['authentication_type'] == 'windows'

def get_database_name():
    """الحصول على اسم قاعدة البيانات"""
    return SQLSERVER_CONFIG['database']

def get_server_name():
    """الحصول على اسم الخادم"""
    return SQLSERVER_CONFIG['server']

# إعدادات متقدمة للاستعلامات
QUERY_TEMPLATES = {
    'check_database_exists': """
        SELECT database_id FROM sys.databases WHERE name = ?
    """,

    'create_database': """
        CREATE DATABASE [{}] COLLATE Arabic_CI_AS
    """,

    'check_table_exists': """
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = ? AND TABLE_TYPE = 'BASE TABLE'
    """,

    'get_table_info': """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
    """,

    'get_database_size': """
        SELECT 
            DB_NAME() as database_name,
            SUM(size * 8.0 / 1024) as size_mb
        FROM sys.database_files
    """,

    'backup_database': """
        BACKUP DATABASE [{}] TO DISK = '{}'
        WITH FORMAT, INIT, COMPRESSION
    """
}

# إعدادات الفهارس والتحسين
INDEX_CONFIG = {
    'auto_create_indexes': True,
    'indexes': [
        {
            'table': 'products',
            'columns': ['barcode'],
            'unique': True,
            'name': 'IX_products_barcode'
        },
        {
            'table': 'sales_invoices',
            'columns': ['invoice_number'],
            'unique': True,
            'name': 'IX_sales_invoices_number'
        },
        {
            'table': 'sales_invoices',
            'columns': ['created_at'],
            'unique': False,
            'name': 'IX_sales_invoices_date'
        },
        {
            'table': 'customers',
            'columns': ['name'],
            'unique': False,
            'name': 'IX_customers_name'
        }
    ]
}
