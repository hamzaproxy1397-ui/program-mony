# -*- coding: utf-8 -*-
"""
نماذج البيانات
Data Models

يحتوي على جميع نماذج البيانات للنظام:
- العملاء (Customers)
- المنتجات (Products)
- الفواتير (Invoices)
"""

from .customer import Customer
from .invoice import SalesInvoice
from .product import Product

__all__ = [
    'Customer',
    'Product',
    'SalesInvoice'
]
"""
Models module - الكائنات والبيانات
"""
