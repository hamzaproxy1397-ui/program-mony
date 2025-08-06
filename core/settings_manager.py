# -*- coding: utf-8 -*-
"""
مدير الإعدادات المركزي
Central Settings Manager
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

class SettingsManager:
    """مدير الإعدادات المركزي للبرنامج"""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = Path(settings_file)
        self.settings = {}
        self.default_settings = self._get_default_settings()
        self.load_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """الإعدادات الافتراضية للبرنامج"""
        return {
            "general": {
                "language": "ar",
                "font_family": "Cairo",
                "font_size": 12,
                "theme": "light",
                "rtl_direction": True,
                "auto_save": True,
                "startup_window": "main"
            },
            "company": {
                "name": "شركة ست الكل للمحاسبة",
                "logo_path": "assets/logo/222555.png",
                "address": "",
                "city": "",
                "country": "المملكة العربية السعودية",
                "tax_number": "",
                "commercial_register": "",
                "phone": "",
                "email": "",
                "website": ""
            },
            "accounting": {
                "fiscal_year_start": "2025-01-01",
                "fiscal_year_end": "2025-12-31",
                "fiscal_year_locked": False,
                "default_currency": "SAR - ريال سعودي",
                "decimal_places": 2,
                "rounding_method": "تقريب عادي",
                "entry_method": "قيد تلقائي",
                "entry_numbering": "تلقائي",
                "allow_edit_entries": True,
                "allow_delete_entries": False,
                "sales_account": "4001",
                "purchases_account": "5001",
                "tax_account": "2301",
                "discount_account": "4002",
                "auto_posting": True,
                "accounts": {
                    "sales": "4001",
                    "purchases": "5001",
                    "cash": "1001",
                    "bank": "1002",
                    "customers": "1201",
                    "suppliers": "2001",
                    "vat_input": "1301",
                    "vat_output": "2301"
                }
            },
            "inventory": {
                "valuation_method": "FIFO",
                "low_stock_alert": True,
                "low_stock_threshold": 10,
                "expiry_alert": True,
                "expiry_days_before": 30,
                "auto_reorder": False,
                "barcode_generation": True
            },
            "invoicing": {
                "template": "default",
                "auto_numbering": True,
                "number_prefix": "INV-",
                "number_format": "YYYY-NNNN",
                "default_payment_terms": "نقدي",
                "show_tax": True,
                "tax_rate": 15.0,
                "printer_name": "",
                "print_copies": 1
            },
            "users": {
                "session_timeout": 60,
                "password_policy": {
                    "min_length": 8,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_symbols": False
                },
                "two_factor_auth": False,
                "login_attempts": 3
            },
            "security": {
                "auto_backup": True,
                "backup_interval": "daily",
                "backup_path": "backups/",
                "backup_retention": 30,
                "encryption": False,
                "audit_log": True
            },
            "network": {
                "database_type": "sqlite",
                "server_host": "localhost",
                "server_port": 5432,
                "database_name": "accounting",
                "connection_timeout": 30,
                "auto_sync": False,
                "api_integration": False
            },
            "reports": {
                "default_format": "PDF",
                "auto_open": True,
                "save_path": "reports/",
                "email_reports": False,
                "report_font": "Cairo",
                "report_font_size": 10,
                "include_logo": True,
                "watermark": False
            }
        }
    
    def load_settings(self) -> None:
        """تحميل الإعدادات من الملف"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # دمج الإعدادات المحملة مع الافتراضية
                    self.settings = self._merge_settings(self.default_settings, loaded_settings)
            else:
                self.settings = self.default_settings.copy()
                self.save_settings()
        except Exception as e:
            print(f"خطأ في تحميل الإعدادات: {e}")
            self.settings = self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """حفظ الإعدادات في الملف"""
        try:
            # إضافة معلومات التحديث
            self.settings["_metadata"] = {
                "last_updated": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"خطأ في حفظ الإعدادات: {e}")
            return False
    
    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """الحصول على قيمة إعداد محدد"""
        try:
            return self.settings.get(section, {}).get(key, default)
        except Exception:
            return default
    
    def set_setting(self, section: str, key: str, value: Any) -> None:
        """تعيين قيمة إعداد محدد"""
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """الحصول على قسم كامل من الإعدادات"""
        return self.settings.get(section, {})
    
    def set_section(self, section: str, values: Dict[str, Any]) -> None:
        """تعيين قسم كامل من الإعدادات"""
        self.settings[section] = values
    
    def reset_to_defaults(self) -> None:
        """إعادة تعيين الإعدادات للقيم الافتراضية"""
        self.settings = self.default_settings.copy()
        self.save_settings()
    
    def reset_section(self, section: str) -> None:
        """إعادة تعيين قسم محدد للقيم الافتراضية"""
        if section in self.default_settings:
            self.settings[section] = self.default_settings[section].copy()
    
    def _merge_settings(self, default: Dict, loaded: Dict) -> Dict:
        """دمج الإعدادات المحملة مع الافتراضية"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        return result
    
    def export_settings(self, file_path: str) -> bool:
        """تصدير الإعدادات لملف خارجي"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"خطأ في تصدير الإعدادات: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """استيراد الإعدادات من ملف خارجي"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
                self.settings = self._merge_settings(self.default_settings, imported_settings)
                self.save_settings()
            return True
        except Exception as e:
            print(f"خطأ في استيراد الإعدادات: {e}")
            return False

# إنشاء مثيل مشترك من مدير الإعدادات
settings_manager = SettingsManager()
