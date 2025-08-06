# -*- coding: utf-8 -*-
"""
مولد رموز الأصناف الذكي
Smart Item Code Generator
"""

import re
from datetime import datetime
from typing import Optional

class ItemCodeGenerator:
    """مولد رموز الأصناف الذكي"""
    
    def __init__(self):
        self.category_prefixes = {
            # التصنيفات الرئيسية
            "إلكترونيات": "ELC",
            "ملابس": "CLT",
            "مواد غذائية": "FD",
            "أدوية": "MED",
            "خدمات": "SRV",
            "مواد بناء": "CNS",
            
            # التصنيفات الفرعية
            "هواتف ذكية": "PHN",
            "حاسوب": "CMP",
            "أجهزة منزلية": "HOM",
            "ملابس رجالية": "MEN",
            "ملابس نسائية": "WMN",
            "ملابس أطفال": "KID",
            "خضروات": "VEG",
            "فواكه": "FRT",
            "لحوم": "MEA",
            "أدوية عامة": "GEN",
            "مكملات غذائية": "SUP",
            "استشارات": "CON",
            "صيانة": "MNT",
            "أسمنت": "CMT",
            "حديد": "STL",
            "دهانات": "PNT"
        }
        
        self.sequence_counter = {}
    
    def generate_code(self, main_category: str = "", sub_category: str = "") -> str:
        """توليد رمز صنف ذكي"""
        # تحديد البادئة
        prefix = self._get_prefix(main_category, sub_category)
        
        # تحديد التاريخ
        date_part = datetime.now().strftime("%Y%m")
        
        # تحديد التسلسل
        sequence_key = f"{prefix}-{date_part}"
        if sequence_key not in self.sequence_counter:
            self.sequence_counter[sequence_key] = 1
        else:
            self.sequence_counter[sequence_key] += 1
        
        sequence = str(self.sequence_counter[sequence_key]).zfill(4)
        
        # تكوين الرمز النهائي
        code = f"{prefix}-{date_part}-{sequence}"
        
        return code
    
    def _get_prefix(self, main_category: str, sub_category: str) -> str:
        """الحصول على البادئة المناسبة"""
        # أولوية للتصنيف الفرعي
        if sub_category and sub_category in self.category_prefixes:
            return self.category_prefixes[sub_category]
        
        # ثم التصنيف الرئيسي
        if main_category and main_category in self.category_prefixes:
            return self.category_prefixes[main_category]
        
        # افتراضي
        return "PRD"
    
    def validate_code_format(self, code: str) -> bool:
        """التحقق من صيغة الرمز"""
        # نمط الرمز: XXX-YYYYMM-NNNN
        pattern = r'^[A-Z]{3}-\d{6}-\d{4}$'
        return bool(re.match(pattern, code))
    
    def extract_code_info(self, code: str) -> dict:
        """استخراج معلومات من الرمز"""
        if not self.validate_code_format(code):
            return {}
        
        parts = code.split('-')
        prefix = parts[0]
        date_part = parts[1]
        sequence = parts[2]
        
        # استخراج السنة والشهر
        year = date_part[:4]
        month = date_part[4:6]
        
        # البحث عن التصنيف
        category = None
        for cat, pre in self.category_prefixes.items():
            if pre == prefix:
                category = cat
                break
        
        return {
            'prefix': prefix,
            'category': category,
            'year': year,
            'month': month,
            'sequence': int(sequence),
            'full_code': code
        }
    
    def suggest_similar_codes(self, partial_code: str, limit: int = 5) -> list:
        """اقتراح رموز مشابهة"""
        suggestions = []
        
        # إذا كان الرمز جزئي، اقترح إكماله
        if len(partial_code) < 3:
            # اقترح بادئات مشابهة
            for category, prefix in self.category_prefixes.items():
                if prefix.startswith(partial_code.upper()):
                    suggestions.append({
                        'code': self.generate_code_with_prefix(prefix),
                        'category': category,
                        'prefix': prefix
                    })
                    if len(suggestions) >= limit:
                        break
        
        return suggestions
    
    def generate_code_with_prefix(self, prefix: str) -> str:
        """توليد رمز بادئة محددة"""
        date_part = datetime.now().strftime("%Y%m")
        sequence_key = f"{prefix}-{date_part}"
        
        if sequence_key not in self.sequence_counter:
            self.sequence_counter[sequence_key] = 1
        else:
            self.sequence_counter[sequence_key] += 1
        
        sequence = str(self.sequence_counter[sequence_key]).zfill(4)
        return f"{prefix}-{date_part}-{sequence}"
    
    def reset_sequence(self, prefix: str = None):
        """إعادة تعيين التسلسل"""
        if prefix:
            # إعادة تعيين تسلسل بادئة محددة
            keys_to_reset = [k for k in self.sequence_counter.keys() if k.startswith(prefix)]
            for key in keys_to_reset:
                self.sequence_counter[key] = 0
        else:
            # إعادة تعيين جميع التسلسلات
            self.sequence_counter.clear()
    
    def get_next_sequence(self, prefix: str) -> int:
        """الحصول على التسلسل التالي"""
        date_part = datetime.now().strftime("%Y%m")
        sequence_key = f"{prefix}-{date_part}"
        
        return self.sequence_counter.get(sequence_key, 0) + 1
    
    def add_custom_prefix(self, category: str, prefix: str):
        """إضافة بادئة مخصصة"""
        if len(prefix) == 3 and prefix.isalpha():
            self.category_prefixes[category] = prefix.upper()
            return True
        return False
    
    def remove_prefix(self, category: str):
        """حذف بادئة"""
        if category in self.category_prefixes:
            del self.category_prefixes[category]
            return True
        return False
    
    def get_all_prefixes(self) -> dict:
        """الحصول على جميع البادئات"""
        return self.category_prefixes.copy()
    
    def generate_batch_codes(self, count: int, main_category: str = "", sub_category: str = "") -> list:
        """توليد مجموعة من الرموز"""
        codes = []
        for _ in range(count):
            code = self.generate_code(main_category, sub_category)
            codes.append(code)
        return codes
    
    def is_code_expired(self, code: str, months: int = 12) -> bool:
        """التحقق من انتهاء صلاحية الرمز"""
        code_info = self.extract_code_info(code)
        if not code_info:
            return False
        
        code_date = datetime(int(code_info['year']), int(code_info['month']), 1)
        current_date = datetime.now()
        
        # حساب الفرق بالأشهر
        months_diff = (current_date.year - code_date.year) * 12 + (current_date.month - code_date.month)
        
        return months_diff > months
    
    def get_statistics(self) -> dict:
        """إحصائيات الرموز المولدة"""
        stats = {
            'total_sequences': len(self.sequence_counter),
            'total_codes_generated': sum(self.sequence_counter.values()),
            'prefixes_used': len(set(k.split('-')[0] for k in self.sequence_counter.keys())),
            'current_month_codes': 0,
            'sequences_by_prefix': {}
        }
        
        current_month = datetime.now().strftime("%Y%m")
        
        for key, count in self.sequence_counter.items():
            prefix, date_part = key.split('-')
            
            if date_part == current_month:
                stats['current_month_codes'] += count
            
            if prefix not in stats['sequences_by_prefix']:
                stats['sequences_by_prefix'][prefix] = 0
            stats['sequences_by_prefix'][prefix] += count
        
        return stats
