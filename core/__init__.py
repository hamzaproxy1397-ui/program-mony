# -*- coding: utf-8 -*-
"""
النواة الأساسية للنظام
Core System Components

يحتوي على جميع المكونات الأساسية للنظام:
- المحاسبة (accounting)
- المبيعات (sales)
- المشتريات (purchases)
- المخزون (inventory)
- المستودعات (warehouse)
- الموارد البشرية (hr)
- نقاط البيع (pos)
- إدارة العملاء (crm)
- إدارة المشاريع (projects)
- التقارير (reports)
- الأمان (security)
"""

from .app_core import AppCore
from .application_manager import ApplicationManager

# استيراد المكونات الفرعية
from . import (
    accounting,
    sales,
    purchases,
    inventory,
    warehouse,
    hr,
    pos,
    crm,
    projects,
    reports,
    security
)

__all__ = [
    'AppCore',
    'ApplicationManager',
    'accounting',
    'sales',
    'purchases',
    'inventory',
    'warehouse',
    'hr',
    'pos',
    'crm',
    'projects',
    'reports',
    'security'
]
"""
Core module - المنطق العام للبرنامج
"""
