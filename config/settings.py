# -*- coding: utf-8 -*-
"""
إعدادات البرنامج الأساسية
"""

import os
from pathlib import Path

# مسارات المشروع
PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "database" / "accounting.db"
ASSETS_PATH = PROJECT_ROOT / "assets"
LOGS_PATH = PROJECT_ROOT / "logs"
REPORTS_PATH = PROJECT_ROOT / "reports" / "generated"

# إعدادات الواجهة المحسنة والموسعة
WINDOW_TITLE = "برنامج ست الكل للمحاسبة"
WINDOW_SIZE = "1920x1080"
WINDOW_MIN_SIZE = (1500, 950)  # زيادة إضافية للحد الأدنى (+100px عرض، +50px ارتفاع)
WINDOW_DEFAULT_SIZE = (1900, 1050)  # الحجم الافتراضي المحسن (+100px عرض، +50px ارتفاع)
WINDOW_EMPLOYEES_SIZE = (1850, 1000)  # حجم نافذة الموظفين المحسن (+50px عرض، +50px ارتفاع)
WINDOW_MAIN_SIZE = (1920, 1080)  # حجم النافذة الرئيسية المحسن (شاشة كاملة محسنة)

# إعدادات RTL
RTL_SUPPORT = True
DEFAULT_FONT = "Cairo"
FALLBACK_FONT = "Arial"

# ألوان الثيم الافتراضي
COLORS = {
    "primary": "#2E8B57",      # أخضر البرنامج الرئيسي
    "secondary": "#4682B4",    # أزرق ثانوي
    "success": "#28a745",      # أخضر النجاح
    "warning": "#ffc107",      # أصفر التحذير
    "danger": "#dc3545",       # أحمر الخطر
    "info": "#17a2b8",         # أزرق المعلومات
    "light": "#f8f9fa",        # رمادي فاتح
    "dark": "#343a40",         # رمادي داكن
    "white": "#ffffff",        # أبيض
    "black": "#000000"         # أسود
}

# إعدادات الشبكة (Grid)
GRID_COLUMNS = 5
GRID_SPACING = 15
BUTTON_SIZE = (150, 150)

# إعدادات قاعدة البيانات
DB_SETTINGS = {
    "timeout": 30,
    "check_same_thread": False,
    "isolation_level": None
}

# إعدادات الأمان
SECURITY = {
    "password_min_length": 6,
    "session_timeout": 3600,  # ساعة واحدة
    "max_login_attempts": 3
}

# إعدادات التقارير
REPORTS = {
    "default_format": "PDF",
    "date_format": "%Y-%m-%d",
    "currency": "ريال سعودي",
    "currency_symbol": "ر.س"
}

# إنشاء المجلدات المطلوبة
def create_directories():
    """إنشاء المجلدات المطلوبة إذا لم تكن موجودة"""
    directories = [
        DATABASE_PATH.parent,
        LOGS_PATH,
        REPORTS_PATH,
        ASSETS_PATH / "icons",
        ASSETS_PATH / "fonts",
        ASSETS_PATH / "images"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# تشغيل إنشاء المجلدات عند استيراد الملف
create_directories()
