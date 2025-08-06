# -*- coding: utf-8 -*-
"""
محرك التحقق والتصديق
Validation Engine
"""

import re
from typing import List, Dict, Any, Tuple
from decimal import Decimal

class ValidationEngine:
    """محرك التحقق الذكي للأصناف"""
    
    def __init__(self):
        self.validation_rules = {
            'item_name': {
                'min_length': 2,
                'max_length': 100,
                'required': True,
                'pattern': r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s\w\-\.]+$'
            },
            'item_code': {
                'min_length': 3,
                'max_length': 20,
                'required': True,
                'pattern': r'^[A-Z0-9\-]+$'
            },
            'selling_price': {
                'min_value': 0.01,
                'max_value': 999999.99,
                'required': True
            },
            'cost': {
                'min_value': 0.0,
                'max_value': 999999.99,
                'required': False
            },
            'initial_quantity': {
                'min_value': 0,
                'max_value': 999999,
                'required': False
            }
        }
        
        self.error_messages = {
            'ar': {
                'required': 'هذا الحقل مطلوب',
                'min_length': 'يجب أن يكون النص أطول من {min} أحرف',
                'max_length': 'يجب أن يكون النص أقصر من {max} حرف',
                'min_value': 'القيمة يجب أن تكون أكبر من {min}',
                'max_value': 'القيمة يجب أن تكون أقل من {max}',
                'pattern': 'تنسيق البيانات غير صحيح',
                'duplicate': 'هذه القيمة موجودة مسبقاً',
                'invalid_profit_margin': 'نسبة الربح غير منطقية ({margin}%)',
                'price_cost_mismatch': 'سعر البيع أقل من التكلفة',
                'category_required': 'يجب اختيار التصنيف',
                'unit_required': 'يجب اختيار وحدة القياس',
                'invalid_tax_combination': 'نوع الضريبة غير متوافق مع التصنيف'
            }
        }
    
    def validate_item_data(self, item_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """التحقق الشامل من بيانات الصنف"""
        errors = []
        
        # التحقق من الحقول الأساسية
        errors.extend(self._validate_field('item_name', item_data.get('name', '')))
        errors.extend(self._validate_field('item_code', item_data.get('code', '')))
        errors.extend(self._validate_field('selling_price', item_data.get('selling_price', 0)))
        errors.extend(self._validate_field('cost', item_data.get('cost', 0)))
        errors.extend(self._validate_field('initial_quantity', item_data.get('initial_quantity', 0)))
        
        # التحقق من التصنيف
        if not item_data.get('main_category'):
            errors.append(self.error_messages['ar']['category_required'])
        
        # التحقق من وحدة القياس
        if not item_data.get('unit'):
            errors.append(self.error_messages['ar']['unit_required'])
        
        # التحقق من العلاقة بين السعر والتكلفة
        cost = float(item_data.get('cost', 0))
        selling_price = float(item_data.get('selling_price', 0))
        
        if cost > 0 and selling_price > 0:
            if selling_price < cost:
                errors.append(self.error_messages['ar']['price_cost_mismatch'])
            else:
                profit_margin = ((selling_price - cost) / cost) * 100
                if profit_margin > 200:  # أكثر من 200%
                    errors.append(self.error_messages['ar']['invalid_profit_margin'].format(margin=f"{profit_margin:.1f}"))
        
        # التحقق من توافق الضريبة مع التصنيف
        tax_validation_error = self._validate_tax_category_compatibility(
            item_data.get('main_category', ''),
            item_data.get('tax_type', '')
        )
        if tax_validation_error:
            errors.append(tax_validation_error)
        
        return len(errors) == 0, errors
    
    def _validate_field(self, field_name: str, value: Any) -> List[str]:
        """التحقق من حقل واحد"""
        errors = []
        rules = self.validation_rules.get(field_name, {})
        
        # التحقق من الإجبارية
        if rules.get('required', False):
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(self.error_messages['ar']['required'])
                return errors
        
        # إذا كان الحقل فارغ وغير مطلوب، تجاهل باقي القواعد
        if not value and not rules.get('required', False):
            return errors
        
        # التحقق من طول النص
        if isinstance(value, str):
            if 'min_length' in rules and len(value) < rules['min_length']:
                errors.append(self.error_messages['ar']['min_length'].format(min=rules['min_length']))
            
            if 'max_length' in rules and len(value) > rules['max_length']:
                errors.append(self.error_messages['ar']['max_length'].format(max=rules['max_length']))
            
            # التحقق من النمط
            if 'pattern' in rules and not re.match(rules['pattern'], value):
                errors.append(self.error_messages['ar']['pattern'])
        
        # التحقق من القيم الرقمية
        if isinstance(value, (int, float, Decimal)):
            if 'min_value' in rules and value < rules['min_value']:
                errors.append(self.error_messages['ar']['min_value'].format(min=rules['min_value']))
            
            if 'max_value' in rules and value > rules['max_value']:
                errors.append(self.error_messages['ar']['max_value'].format(max=rules['max_value']))
        
        return errors
    
    def _validate_tax_category_compatibility(self, category: str, tax_type: str) -> str:
        """التحقق من توافق الضريبة مع التصنيف"""
        tax_exempt_categories = ['أدوية', 'مواد غذائية أساسية']
        taxable_categories = ['إلكترونيات', 'ملابس', 'خدمات']
        
        if category in tax_exempt_categories and '15%' in tax_type:
            return self.error_messages['ar']['invalid_tax_combination']
        
        if category in taxable_categories and 'معفى' in tax_type:
            return self.error_messages['ar']['invalid_tax_combination']
        
        return ""
    
    def validate_item_name(self, name: str) -> Tuple[bool, str]:
        """التحقق من اسم الصنف"""
        errors = self._validate_field('item_name', name)
        return len(errors) == 0, errors[0] if errors else ""
    
    def validate_item_code(self, code: str) -> Tuple[bool, str]:
        """التحقق من رمز الصنف"""
        errors = self._validate_field('item_code', code)
        return len(errors) == 0, errors[0] if errors else ""
    
    def validate_price(self, price: float) -> Tuple[bool, str]:
        """التحقق من السعر"""
        errors = self._validate_field('selling_price', price)
        return len(errors) == 0, errors[0] if errors else ""
    
    def validate_cost(self, cost: float) -> Tuple[bool, str]:
        """التحقق من التكلفة"""
        errors = self._validate_field('cost', cost)
        return len(errors) == 0, errors[0] if errors else ""
    
    def validate_quantity(self, quantity: int) -> Tuple[bool, str]:
        """التحقق من الكمية"""
        errors = self._validate_field('initial_quantity', quantity)
        return len(errors) == 0, errors[0] if errors else ""
    
    def calculate_profit_margin(self, cost: float, selling_price: float) -> float:
        """حساب نسبة الربح"""
        if cost <= 0:
            return 0.0
        return ((selling_price - cost) / cost) * 100
    
    def suggest_selling_price(self, cost: float, target_margin: float = 25.0) -> float:
        """اقتراح سعر البيع بناءً على نسبة ربح مستهدفة"""
        if cost <= 0:
            return 0.0
        return cost * (1 + target_margin / 100)
    
    def validate_profit_margin(self, margin: float) -> Tuple[bool, str]:
        """التحقق من نسبة الربح"""
        if margin < 0:
            return False, "نسبة الربح لا يمكن أن تكون سالبة"
        elif margin > 200:
            return False, f"نسبة الربح عالية جداً ({margin:.1f}%)"
        elif margin < 5:
            return False, f"نسبة الربح منخفضة جداً ({margin:.1f}%)"
        else:
            return True, ""
    
    def sanitize_input(self, text: str) -> str:
        """تنظيف النص المدخل"""
        if not isinstance(text, str):
            return str(text)
        
        # إزالة المسافات الزائدة
        text = text.strip()
        
        # إزالة الأحرف الخاصة الضارة
        text = re.sub(r'[<>"\']', '', text)
        
        # تنظيف المسافات المتعددة
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def validate_image_file(self, file_path: str) -> Tuple[bool, str]:
        """التحقق من ملف الصورة"""
        import os
        from pathlib import Path
        
        if not file_path:
            return True, ""  # الصورة اختيارية
        
        if not os.path.exists(file_path):
            return False, "ملف الصورة غير موجود"
        
        # التحقق من امتداد الملف
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension not in valid_extensions:
            return False, f"نوع الملف غير مدعوم. الأنواع المدعومة: {', '.join(valid_extensions)}"
        
        # التحقق من حجم الملف (أقل من 5 ميجا)
        file_size = os.path.getsize(file_path)
        max_size = 5 * 1024 * 1024  # 5 MB
        
        if file_size > max_size:
            return False, f"حجم الملف كبير جداً ({file_size / 1024 / 1024:.1f} MB). الحد الأقصى 5 MB"
        
        return True, ""
    
    def get_validation_summary(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """ملخص شامل للتحقق"""
        is_valid, errors = self.validate_item_data(item_data)
        
        # حساب نسبة الربح
        cost = float(item_data.get('cost', 0))
        selling_price = float(item_data.get('selling_price', 0))
        profit_margin = self.calculate_profit_margin(cost, selling_price)
        
        # تقييم نسبة الربح
        margin_status = "جيد"
        if profit_margin > 50:
            margin_status = "عالي"
        elif profit_margin < 10:
            margin_status = "منخفض"
        
        return {
            'is_valid': is_valid,
            'errors': errors,
            'warnings': [],
            'profit_margin': profit_margin,
            'margin_status': margin_status,
            'suggested_price': self.suggest_selling_price(cost) if cost > 0 else 0,
            'validation_score': max(0, 100 - len(errors) * 10)  # نقاط من 100
        }
    
    def add_custom_validation_rule(self, field_name: str, rule_name: str, rule_value: Any):
        """إضافة قاعدة تحقق مخصصة"""
        if field_name not in self.validation_rules:
            self.validation_rules[field_name] = {}
        
        self.validation_rules[field_name][rule_name] = rule_value
    
    def remove_validation_rule(self, field_name: str, rule_name: str):
        """حذف قاعدة تحقق"""
        if field_name in self.validation_rules and rule_name in self.validation_rules[field_name]:
            del self.validation_rules[field_name][rule_name]
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """الحصول على جميع قواعد التحقق"""
        return self.validation_rules.copy()
