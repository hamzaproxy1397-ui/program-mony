# -*- coding: utf-8 -*-
"""
مدير الترجمة
Translation Manager
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class TranslationManager:
    """مدير الترجمة والتعريب"""
    
    def __init__(self, default_language: str = 'ar'):
        self.translations_dir = Path(__file__).parent
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """تحميل ملفات الترجمة"""
        translation_files = {
            'ar': self.translations_dir / 'ar.json',
            'en': self.translations_dir / 'en.json'
        }
        
        for lang, file_path in translation_files.items():
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"خطأ في تحميل ملف الترجمة {lang}: {e}")
                    self.translations[lang] = {}
            else:
                self.translations[lang] = {}
    
    def set_language(self, language: str):
        """تعيين اللغة الحالية"""
        if language in self.translations:
            self.current_language = language
        else:
            print(f"اللغة {language} غير مدعومة")
    
    def get_text(self, key: str, language: Optional[str] = None, **kwargs) -> str:
        """الحصول على النص المترجم"""
        lang = language or self.current_language
        
        # تقسيم المفتاح إلى أجزاء (مثل: "menu.file")
        keys = key.split('.')
        
        # البحث في ترجمات اللغة المحددة
        current_dict = self.translations.get(lang, {})
        
        for k in keys:
            if isinstance(current_dict, dict) and k in current_dict:
                current_dict = current_dict[k]
            else:
                # إذا لم يوجد في اللغة الحالية، جرب اللغة الافتراضية
                if lang != self.default_language:
                    return self.get_text(key, self.default_language, **kwargs)
                else:
                    # إذا لم يوجد في اللغة الافتراضية، أرجع المفتاح نفسه
                    return key
        
        # إذا كان النص يحتوي على متغيرات، استبدلها
        if isinstance(current_dict, str) and kwargs:
            try:
                return current_dict.format(**kwargs)
            except KeyError:
                return current_dict
        
        return str(current_dict) if current_dict is not None else key
    
    def get_available_languages(self) -> list:
        """الحصول على قائمة اللغات المتاحة"""
        return list(self.translations.keys())
    
    def is_rtl(self, language: Optional[str] = None) -> bool:
        """فحص ما إذا كانت اللغة تكتب من اليمين لليسار"""
        lang = language or self.current_language
        rtl_languages = ['ar', 'he', 'fa', 'ur']
        return lang in rtl_languages
    
    def get_language_name(self, language: str) -> str:
        """الحصول على اسم اللغة"""
        language_names = {
            'ar': 'العربية',
            'en': 'English'
        }
        return language_names.get(language, language)
    
    def add_translation(self, language: str, key: str, value: str):
        """إضافة ترجمة جديدة"""
        if language not in self.translations:
            self.translations[language] = {}
        
        # تقسيم المفتاح وإنشاء البنية المتداخلة
        keys = key.split('.')
        current_dict = self.translations[language]
        
        for k in keys[:-1]:
            if k not in current_dict:
                current_dict[k] = {}
            current_dict = current_dict[k]
        
        current_dict[keys[-1]] = value
    
    def save_translations(self, language: str) -> bool:
        """حفظ ترجمات لغة معينة"""
        if language not in self.translations:
            return False
        
        file_path = self.translations_dir / f'{language}.json'
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.translations[language], f, 
                         ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في حفظ ترجمات {language}: {e}")
            return False
    
    def export_translations(self, language: str, file_path: str) -> bool:
        """تصدير ترجمات لغة معينة"""
        if language not in self.translations:
            return False
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.translations[language], f, 
                         ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في تصدير ترجمات {language}: {e}")
            return False
    
    def import_translations(self, language: str, file_path: str) -> bool:
        """استيراد ترجمات لغة معينة"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_translations = json.load(f)
            
            if language not in self.translations:
                self.translations[language] = {}
            
            # دمج الترجمات المستوردة مع الموجودة
            self._merge_translations(self.translations[language], imported_translations)
            
            return True
        except Exception as e:
            print(f"خطأ في استيراد ترجمات {language}: {e}")
            return False
    
    def _merge_translations(self, target: dict, source: dict):
        """دمج قواميس الترجمة"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_translations(target[key], value)
            else:
                target[key] = value
    
    def get_missing_translations(self, source_language: str, target_language: str) -> list:
        """الحصول على قائمة الترجمات المفقودة"""
        if source_language not in self.translations or target_language not in self.translations:
            return []
        
        missing = []
        self._find_missing_keys(
            self.translations[source_language],
            self.translations[target_language],
            missing,
            ""
        )
        
        return missing
    
    def _find_missing_keys(self, source: dict, target: dict, missing: list, prefix: str):
        """البحث عن المفاتيح المفقودة بشكل تكراري"""
        for key, value in source.items():
            current_key = f"{prefix}.{key}" if prefix else key
            
            if key not in target:
                missing.append(current_key)
            elif isinstance(value, dict) and isinstance(target[key], dict):
                self._find_missing_keys(value, target[key], missing, current_key)
    
    def validate_translations(self, language: str) -> list:
        """التحقق من صحة الترجمات"""
        errors = []
        
        if language not in self.translations:
            errors.append(f"اللغة {language} غير موجودة")
            return errors
        
        # فحص الترجمات المطلوبة
        required_keys = [
            'app.name',
            'menu.file',
            'buttons.save',
            'buttons.cancel',
            'messages.success',
            'messages.error'
        ]
        
        for key in required_keys:
            if not self.get_text(key, language):
                errors.append(f"الترجمة مفقودة: {key}")
        
        return errors

# إنشاء مثيل عام لمدير الترجمة
translation_manager = TranslationManager()

# دوال مساعدة للوصول السريع
def _(key: str, **kwargs) -> str:
    """دالة مختصرة للحصول على النص المترجم"""
    return translation_manager.get_text(key, **kwargs)

def set_language(language: str):
    """تعيين اللغة الحالية"""
    translation_manager.set_language(language)

def get_current_language() -> str:
    """الحصول على اللغة الحالية"""
    return translation_manager.current_language

def is_rtl() -> bool:
    """فحص ما إذا كانت اللغة الحالية تكتب من اليمين لليسار"""
    return translation_manager.is_rtl()

def get_available_languages() -> list:
    """الحصول على قائمة اللغات المتاحة"""
    return translation_manager.get_available_languages()

def get_language_name(language: str) -> str:
    """الحصول على اسم اللغة"""
    return translation_manager.get_language_name(language)
