# -*- coding: utf-8 -*-
"""
الخدمات
Services

يحتوي على جميع الخدمات المساعدة والمديرين:
- مدير المبيعات
- مدير المشتريات
- مدير الموظفين
- مدير الخزينة
- طابعة الفواتير
"""

from .employees_manager import EmployeesManager
from .invoice_printer import InvoicePrinter
from .purchases_manager import PurchasesManager
from .sales_manager import SalesManager
from .treasury_manager import TreasuryManager

__all__ = [
    'SalesManager',
    'PurchasesManager',
    'EmployeesManager',
    'TreasuryManager',
    'InvoicePrinter'
]
"""
Services module - الخدمات
"""
