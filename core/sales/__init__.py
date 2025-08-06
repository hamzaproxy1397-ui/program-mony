# -*- coding: utf-8 -*-
"""
نظام المبيعات
Sales System

يحتوي على:
- إدارة فواتير المبيعات
- متابعة المدفوعات
- تحليل المبيعات
"""

from .sales_manager import (
    SalesManager,
    SalesInvoice,
    InvoiceStatus,
    PaymentMethod
)

__all__ = [
    'SalesManager',
    'SalesInvoice',
    'InvoiceStatus',
    'PaymentMethod'
]
