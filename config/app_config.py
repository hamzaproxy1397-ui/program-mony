# -*- coding: utf-8 -*-
"""
إعدادات التطبيق
Application Configuration
"""

import os
from pathlib import Path
from typing import Dict, Any
import json

# مسارات المشروع
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
STATIC_DIR = PROJECT_ROOT / "static"
FONTS_DIR = STATIC_DIR / "fonts"
TRANSLATIONS_DIR = PROJECT_ROOT / "translations"

# إعدادات قاعدة البيانات
DATABASE_CONFIG = {
    'sqlite': {
        'path': DATA_DIR / "accounting.db",
        'enabled': True
    },
    'postgresql': {
        'host': 'localhost',
        'port': 5432,
        'database': 'accounting_db',
        'username': 'postgres',
        'password': '',
        'enabled': False
    },
    'sqlserver': {
        'server': 'localhost',
        'database': 'accounting_db',
        'username': 'sa',
        'password': '',
        'enabled': False
    }
}

# إعدادات التطبيق الافتراضية
DEFAULT_APP_SETTINGS = {
    'theme': 'light',
    'language': 'ar',
    'font_family': 'Cairo',
    'font_size': 12,
    'window_state': 'maximized',
    'auto_backup': True,
    'backup_interval': 24,  # ساعات
    'backup_location': str(DATA_DIR / "backups"),
    'currency': 'ريال سعودي',
    'currency_symbol': 'ر.س',
    'currency_code': 'SAR',
    'tax_rate': 15.0,
    'decimal_places': 2,
    'date_format': '%Y-%m-%d',
    'time_format': '%H:%M:%S',
    'rtl_support': True,
    'auto_save': True,
    'auto_save_interval': 5,  # دقائق
    'session_timeout': 480,  # دقائق (8 ساعات)
    'max_login_attempts': 3,
    'password_min_length': 6,
    'enable_audit_log': True,
    'enable_notifications': True,
    'print_preview': True,
    'default_printer': '',
    'invoice_template': 'default',
    'report_template': 'default'
}

# معلومات الشركة الافتراضية
DEFAULT_COMPANY_INFO = {
    'name': 'شركة ست الكل للمحاسبة',
    'name_en': 'Sit Al-Kol Accounting Company',
    'address': '',
    'address_en': '',
    'city': '',
    'country': 'المملكة العربية السعودية',
    'country_en': 'Saudi Arabia',
    'phone': '',
    'fax': '',
    'email': '',
    'website': '',
    'tax_number': '',
    'commercial_register': '',
    'logo_path': '',
    'established_date': '',
    'fiscal_year_start': '01-01',  # شهر-يوم
    'fiscal_year_end': '12-31'
}

# إعدادات الأمان
SECURITY_CONFIG = {
    'encryption_key': None,  # سيتم توليدها تلقائياً
    'session_secret': None,  # سيتم توليدها تلقائياً
    'password_hash_rounds': 12,
    'enable_two_factor': False,
    'backup_encryption': True,
    'audit_log_retention': 365,  # أيام
    'failed_login_lockout': 30,  # دقائق
    'password_expiry': 90,  # أيام
    'force_password_change': False
}

# إعدادات التقارير
REPORTS_CONFIG = {
    'default_format': 'pdf',
    'supported_formats': ['pdf', 'excel', 'csv', 'html'],
    'max_records_per_page': 50,
    'enable_charts': True,
    'chart_library': 'matplotlib',
    'watermark': True,
    'watermark_text': 'شركة ست الكل للمحاسبة',
    'header_logo': True,
    'footer_info': True,
    'page_numbers': True,
    'generation_timestamp': True
}

# إعدادات الطباعة
PRINTING_CONFIG = {
    'default_paper_size': 'A4',
    'default_orientation': 'portrait',
    'margins': {
        'top': 20,
        'bottom': 20,
        'left': 20,
        'right': 20
    },
    'dpi': 300,
    'color_mode': 'color',
    'duplex': False,
    'collate': True,
    'copies': 1
}

# إعدادات التصدير والاستيراد
IMPORT_EXPORT_CONFIG = {
    'supported_formats': ['excel', 'csv', 'json', 'xml'],
    'max_file_size': 50,  # ميجابايت
    'chunk_size': 1000,  # عدد السجلات في كل دفعة
    'validate_data': True,
    'create_backup_before_import': True,
    'log_import_errors': True,
    'export_with_headers': True,
    'export_encoding': 'utf-8'
}

class AppConfig:
    """مدير إعدادات التطبيق"""
    
    def __init__(self):
        self.config_file = CONFIG_DIR / "app_settings.json"
        self.company_file = CONFIG_DIR / "company_info.json"
        self.settings = {}
        self.company_info = {}
        self._ensure_directories()
        self.load_settings()
    
    def _ensure_directories(self):
        """التأكد من وجود المجلدات المطلوبة"""
        directories = [CONFIG_DIR, DATA_DIR, LOGS_DIR, STATIC_DIR, 
                      FONTS_DIR, TRANSLATIONS_DIR]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_settings(self):
        """تحميل الإعدادات"""
        # تحميل إعدادات التطبيق
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.settings = DEFAULT_APP_SETTINGS.copy()
        else:
            self.settings = DEFAULT_APP_SETTINGS.copy()
        
        # تحميل معلومات الشركة
        if self.company_file.exists():
            try:
                with open(self.company_file, 'r', encoding='utf-8') as f:
                    self.company_info = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.company_info = DEFAULT_COMPANY_INFO.copy()
        else:
            self.company_info = DEFAULT_COMPANY_INFO.copy()
    
    def save_settings(self):
        """حفظ الإعدادات"""
        try:
            # حفظ إعدادات التطبيق
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            
            # حفظ معلومات الشركة
            with open(self.company_file, 'w', encoding='utf-8') as f:
                json.dump(self.company_info, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"خطأ في حفظ الإعدادات: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """الحصول على قيمة إعداد"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """تعيين قيمة إعداد"""
        self.settings[key] = value
    
    def get_company_info(self, key: str, default: Any = None) -> Any:
        """الحصول على معلومات الشركة"""
        return self.company_info.get(key, default)
    
    def set_company_info(self, key: str, value: Any):
        """تعيين معلومات الشركة"""
        self.company_info[key] = value
    
    def reset_to_defaults(self):
        """إعادة تعيين الإعدادات للقيم الافتراضية"""
        self.settings = DEFAULT_APP_SETTINGS.copy()
        self.company_info = DEFAULT_COMPANY_INFO.copy()
    
    def export_settings(self, file_path: str) -> bool:
        """تصدير الإعدادات"""
        try:
            export_data = {
                'app_settings': self.settings,
                'company_info': self.company_info,
                'export_date': str(Path().cwd()),
                'version': '1.0'
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"خطأ في تصدير الإعدادات: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """استيراد الإعدادات"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'app_settings' in import_data:
                self.settings.update(import_data['app_settings'])
            
            if 'company_info' in import_data:
                self.company_info.update(import_data['company_info'])
            
            return True
        except Exception as e:
            print(f"خطأ في استيراد الإعدادات: {e}")
            return False

# إنشاء مثيل عام للإعدادات
app_config = AppConfig()

# دوال مساعدة للوصول السريع للإعدادات
def get_setting(key: str, default: Any = None) -> Any:
    """الحصول على إعداد"""
    return app_config.get(key, default)

def set_setting(key: str, value: Any):
    """تعيين إعداد"""
    app_config.set(key, value)

def get_company_info(key: str, default: Any = None) -> Any:
    """الحصول على معلومات الشركة"""
    return app_config.get_company_info(key, default)

def set_company_info(key: str, value: Any):
    """تعيين معلومات الشركة"""
    app_config.set_company_info(key, value)

def save_config():
    """حفظ الإعدادات"""
    return app_config.save_settings()
