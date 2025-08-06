# -*- coding: utf-8 -*-
"""
إعدادات SQL Server المحلية
"""

# إعدادات الاتصال بـ SQL Server المحلي
LOCAL_SQLSERVER_CONFIG = {
    'server': 'localhost\SQLEXPRESS',  # أو localhost
    'database': 'AccountingDB',
    'authentication_type': 'windows',
    'trusted_connection': 'yes',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'timeout': 30
}

# إعدادات بديلة للاختبار
TEST_CONFIG = {
    'server': '(localdb)\MSSQLLocalDB',  # LocalDB
    'database': 'AccountingDB',
    'authentication_type': 'windows',
    'trusted_connection': 'yes',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'timeout': 30
}
