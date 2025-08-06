# -*- coding: utf-8 -*-
"""
إعدادات خاصة بلوحة التحكم المركزية
"""

from pathlib import Path

# مسارات المشروع
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
UI_DIR = PROJECT_ROOT / "ui"
ASSETS_DIR = PROJECT_ROOT / "assets"
DATABASE_DIR = PROJECT_ROOT / "database"
BACKUPS_DIR = PROJECT_ROOT / "backups"

# ملفات الإعدادات
CONTROL_PANEL_SETTINGS_FILE = CONFIG_DIR / "control_panel_settings.json"
APP_SETTINGS_FILE = CONFIG_DIR / "app_settings.json"
USER_PREFERENCES_FILE = CONFIG_DIR / "user_preferences.json"

# إعدادات لوحة التحكم
CONTROL_PANEL_CONFIG = {
    # إعدادات النافذة
    'window': {
        'title': '🎛️ لوحة التحكم المركزية - برنامج المحاسبة',
        'geometry': '1400x900',
        'state': 'zoomed',  # ملء الشاشة
        'resizable': True,
        'topmost': False
    },
    
    # إعدادات الشريط الجانبي
    'sidebar': {
        'width': 280,
        'sections_count': 11,
        'button_height': 70,
        'padding': 15,
        'spacing': 5
    },
    
    # إعدادات المحتوى
    'content': {
        'padding': 20,
        'card_spacing': 10,
        'header_height': 100,
        'field_height': 35,
        'field_spacing': 5
    },
    
    # إعدادات الشريط السفلي
    'bottom_bar': {
        'height': 60,
        'button_width': 180,
        'button_height': 40,
        'buttons_spacing': 5
    }
}

# قائمة الأقسام مع تفاصيلها
CONTROL_SECTIONS = [
    {
        'key': 'general',
        'title': 'الإعدادات العامة',
        'icon': '🧩',
        'color_key': 'coral',
        'description': 'اللغة، التاريخ، الشعار',
        'priority': 1
    },
    {
        'key': 'users',
        'title': 'المستخدمون والصلاحيات',
        'icon': '👥',
        'color_key': 'sunset',
        'description': 'إدارة المستخدمين',
        'priority': 2
    },
    {
        'key': 'invoices',
        'title': 'إعدادات الفواتير',
        'icon': '🧾',
        'color_key': 'golden',
        'description': 'بيع، شراء، POS',
        'priority': 3
    },
    {
        'key': 'payroll',
        'title': 'الرواتب والضرائب',
        'icon': '💰',
        'color_key': 'mint',
        'description': 'إعدادات الرواتب',
        'priority': 4
    },
    {
        'key': 'warehouses',
        'title': 'إعدادات المخازن',
        'icon': '🏪',
        'color_key': 'sky',
        'description': 'إدارة المخازن',
        'priority': 5
    },
    {
        'key': 'modules',
        'title': 'التحكم في الموديلات',
        'icon': '🔧',
        'color_key': 'rose',
        'description': 'إظهار/إخفاء الميزات',
        'priority': 6
    },
    {
        'key': 'backup',
        'title': 'النسخ الاحتياطي',
        'icon': '💾',
        'color_key': 'peach',
        'description': 'حفظ واستعادة البيانات',
        'priority': 7
    },
    {
        'key': 'import_export',
        'title': 'استيراد من Excel',
        'icon': '📊',
        'color_key': 'turquoise',
        'description': 'إدارة البيانات',
        'priority': 8
    },
    {
        'key': 'appearance',
        'title': 'تخصيص الواجهة',
        'icon': '🎨',
        'color_key': 'violet',
        'description': 'الألوان والخطوط',
        'priority': 9
    },
    {
        'key': 'security',
        'title': 'نظام الأمان',
        'icon': '🛡️',
        'color_key': 'lavender',
        'description': 'الحماية والمراقبة',
        'priority': 10
    },
    {
        'key': 'numbering',
        'title': 'الأرقام التسلسلية',
        'icon': '🔢',
        'color_key': 'coral',
        'description': 'توليد الأرقام التلقائي',
        'priority': 11
    }
]

# إعدادات الحقول
FIELD_TYPES = {
    'text': 'نص',
    'number': 'رقم',
    'email': 'بريد إلكتروني',
    'phone': 'هاتف',
    'dropdown': 'قائمة منسدلة',
    'switch': 'مفتاح تشغيل',
    'textarea': 'نص متعدد الأسطر',
    'file': 'ملف',
    'color': 'لون',
    'date': 'تاريخ',
    'time': 'وقت'
}

# خيارات القوائم المنسدلة
DROPDOWN_OPTIONS = {
    'languages': ['العربية', 'English'],
    'date_formats': ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD'],
    'currencies': ['ريال سعودي', 'درهم إماراتي', 'دينار كويتي', 'دولار أمريكي'],
    'fonts': ['Cairo', 'Amiri', 'Noto Naskh Arabic', 'Tajawal', 'Almarai'],
    'font_sizes': ['صغير', 'متوسط', 'كبير', 'كبير جداً'],
    'invoice_templates': ['حديث', 'كلاسيكي', 'مبسط'],
    'paper_sizes': ['A4', 'A5', 'Letter'],
    'backup_frequencies': ['يومياً', 'أسبوعياً', 'شهرياً'],
    'backup_times': ['02:00', '03:00', '04:00', '23:00'],
    'inventory_methods': ['FIFO', 'LIFO', 'متوسط مرجح']
}

# رسائل التأكيد
CONFIRMATION_MESSAGES = {
    'factory_reset': {
        'title': 'تحذير - ضبط المصنع',
        'message': '⚠️ تحذير شديد ⚠️\n\n'
                  'هذا الإجراء سيحذف جميع البيانات نهائياً!\n'
                  '• جميع الفواتير والمعاملات\n'
                  '• بيانات العملاء والموردين\n'
                  '• المخزون والمنتجات\n'
                  '• الإعدادات المخصصة\n\n'
                  'هل أنت متأكد تماماً من المتابعة؟'
    },
    'restore_defaults': {
        'title': 'استعادة الافتراضي',
        'message': 'هل أنت متأكد من استعادة جميع الإعدادات إلى القيم الافتراضية؟\n'
                  'سيتم فقدان جميع التخصيصات الحالية!'
    },
    'restore_backup': {
        'title': 'تأكيد الاستعادة',
        'message': 'هل أنت متأكد من استعادة هذه النسخة الاحتياطية؟\n'
                  'سيتم استبدال البيانات الحالية بالكامل!'
    }
}

# رسائل الحالة
STATUS_MESSAGES = {
    'ready': '✅ جاهز للتحكم',
    'saving': '💾 جاري الحفظ...',
    'saved': '✅ تم حفظ جميع الإعدادات بنجاح',
    'loading': '📂 جاري التحميل...',
    'loaded': '✅ تم تحميل الإعدادات بنجاح',
    'error_save': '❌ خطأ في حفظ الإعدادات',
    'error_load': '❌ خطأ في تحميل الإعدادات',
    'backup_created': '✅ تم إنشاء النسخة الاحتياطية بنجاح',
    'backup_restored': '✅ تم استعادة النسخة الاحتياطية بنجاح',
    'factory_reset_done': '✅ تم ضبط المصنع بنجاح',
    'defaults_restored': '✅ تم استعادة الإعدادات الافتراضية',
    'preview_opened': '🎯 تم فتح معاينة الإعدادات'
}

# إعدادات الأمان
SECURITY_SETTINGS = {
    'min_password_length': 6,
    'max_login_attempts': 3,
    'session_timeout_minutes': 60,
    'require_confirmation_for_dangerous_actions': True,
    'log_all_operations': True,
    'encrypt_sensitive_data': False
}

def get_section_by_key(key):
    """الحصول على قسم بالمفتاح"""
    for section in CONTROL_SECTIONS:
        if section['key'] == key:
            return section
    return None

def get_dropdown_options(option_key):
    """الحصول على خيارات القائمة المنسدلة"""
    return DROPDOWN_OPTIONS.get(option_key, [])

def get_confirmation_message(message_key):
    """الحصول على رسالة التأكيد"""
    return CONFIRMATION_MESSAGES.get(message_key, {})

def get_status_message(status_key):
    """الحصول على رسالة الحالة"""
    return STATUS_MESSAGES.get(status_key, status_key)
