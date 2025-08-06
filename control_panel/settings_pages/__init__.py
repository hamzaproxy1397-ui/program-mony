# -*- coding: utf-8 -*-
"""
صفحات الإعدادات المختلفة
Settings Pages Module
"""

from .general_settings import GeneralSettingsPage
from .company_settings import CompanySettingsPage
from .accounting_settings import AccountingSettingsPage

__all__ = [
    'GeneralSettingsPage',
    'CompanySettingsPage',
    'AccountingSettingsPage'
]
