# -*- coding: utf-8 -*-
"""
نموذج بيانات الصنف
Item Data Model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class ItemModel:
    """نموذج بيانات الصنف"""
    
    # المعرف الفريد
    id: Optional[int] = None
    
    # البيانات الأساسية
    name: str = ""
    code: str = ""
    description: str = ""
    
    # التصنيف
    main_category: str = ""
    sub_category: str = ""
    
    # وحدة القياس والكمية
    unit: str = ""
    initial_quantity: int = 0
    current_quantity: int = 0
    minimum_quantity: int = 0
    maximum_quantity: int = 0
    
    # الأسعار والتكلفة
    cost: Decimal = field(default_factory=lambda: Decimal('0.00'))
    selling_price: Decimal = field(default_factory=lambda: Decimal('0.00'))
    wholesale_price: Optional[Decimal] = None
    retail_price: Optional[Decimal] = None
    
    # الضريبة
    tax_type: str = "15% ضريبة القيمة المضافة"
    tax_rate: Decimal = field(default_factory=lambda: Decimal('15.00'))
    is_tax_exempt: bool = False
    
    # الصورة والملفات
    image_path: Optional[str] = None
    barcode: Optional[str] = None
    qr_code: Optional[str] = None
    
    # معلومات إضافية
    brand: str = ""
    model: str = ""
    color: str = ""
    size: str = ""
    weight: Optional[Decimal] = None
    dimensions: str = ""
    
    # معلومات المورد
    supplier_name: str = ""
    supplier_code: str = ""
    supplier_price: Optional[Decimal] = None
    
    # تواريخ مهمة
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    expiry_date: Optional[datetime] = None
    manufacturing_date: Optional[datetime] = None
    
    # حالة الصنف
    is_active: bool = True
    is_discontinued: bool = False
    is_seasonal: bool = False
    
    # معلومات المحاسبة
    asset_account: str = ""
    revenue_account: str = ""
    expense_account: str = ""
    
    # ملاحظات وتصنيفات إضافية
    notes: str = ""
    tags: list = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """معالجة ما بعد التهيئة"""
        # تحويل الأسعار إلى Decimal
        if isinstance(self.cost, (int, float, str)):
            self.cost = Decimal(str(self.cost))
        
        if isinstance(self.selling_price, (int, float, str)):
            self.selling_price = Decimal(str(self.selling_price))
        
        if self.wholesale_price and isinstance(self.wholesale_price, (int, float, str)):
            self.wholesale_price = Decimal(str(self.wholesale_price))
        
        if self.retail_price and isinstance(self.retail_price, (int, float, str)):
            self.retail_price = Decimal(str(self.retail_price))
        
        # تحديث الكمية الحالية إذا لم تكن محددة
        if self.current_quantity == 0 and self.initial_quantity > 0:
            self.current_quantity = self.initial_quantity
        
        # تحديد معدل الضريبة حسب النوع
        self._update_tax_rate()
    
    def _update_tax_rate(self):
        """تحديث معدل الضريبة"""
        if "معفى" in self.tax_type:
            self.tax_rate = Decimal('0.00')
            self.is_tax_exempt = True
        elif "15%" in self.tax_type:
            self.tax_rate = Decimal('15.00')
            self.is_tax_exempt = False
        elif "5%" in self.tax_type:
            self.tax_rate = Decimal('5.00')
            self.is_tax_exempt = False
    
    @property
    def profit_margin(self) -> Decimal:
        """حساب نسبة الربح"""
        if self.cost <= 0:
            return Decimal('0.00')
        
        profit = self.selling_price - self.cost
        return (profit / self.cost) * 100
    
    @property
    def profit_amount(self) -> Decimal:
        """مبلغ الربح"""
        return self.selling_price - self.cost
    
    @property
    def tax_amount(self) -> Decimal:
        """مبلغ الضريبة"""
        if self.is_tax_exempt:
            return Decimal('0.00')
        
        return (self.selling_price * self.tax_rate) / 100
    
    @property
    def total_price_with_tax(self) -> Decimal:
        """السعر الإجمالي مع الضريبة"""
        return self.selling_price + self.tax_amount
    
    @property
    def inventory_value(self) -> Decimal:
        """قيمة المخزون"""
        return self.cost * self.current_quantity
    
    @property
    def is_low_stock(self) -> bool:
        """هل المخزون منخفض"""
        return self.current_quantity <= self.minimum_quantity
    
    @property
    def is_out_of_stock(self) -> bool:
        """هل المخزون منتهي"""
        return self.current_quantity <= 0
    
    @property
    def is_overstocked(self) -> bool:
        """هل المخزون زائد"""
        return self.maximum_quantity > 0 and self.current_quantity > self.maximum_quantity
    
    @property
    def stock_status(self) -> str:
        """حالة المخزون"""
        if self.is_out_of_stock:
            return "منتهي"
        elif self.is_low_stock:
            return "منخفض"
        elif self.is_overstocked:
            return "زائد"
        else:
            return "طبيعي"
    
    def update_quantity(self, quantity_change: int, operation: str = "add"):
        """تحديث الكمية"""
        if operation == "add":
            self.current_quantity += quantity_change
        elif operation == "subtract":
            self.current_quantity = max(0, self.current_quantity - quantity_change)
        elif operation == "set":
            self.current_quantity = max(0, quantity_change)
        
        self.updated_at = datetime.now()
    
    def set_price(self, price: Decimal, price_type: str = "selling"):
        """تحديد السعر"""
        if price_type == "selling":
            self.selling_price = Decimal(str(price))
        elif price_type == "cost":
            self.cost = Decimal(str(price))
        elif price_type == "wholesale":
            self.wholesale_price = Decimal(str(price))
        elif price_type == "retail":
            self.retail_price = Decimal(str(price))
        
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str):
        """إضافة تصنيف"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str):
        """حذف تصنيف"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def set_custom_field(self, field_name: str, value: Any):
        """تحديد حقل مخصص"""
        self.custom_fields[field_name] = value
        self.updated_at = datetime.now()
    
    def get_custom_field(self, field_name: str, default: Any = None):
        """الحصول على حقل مخصص"""
        return self.custom_fields.get(field_name, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            else:
                data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ItemModel':
        """إنشاء من قاموس"""
        # تحويل التواريخ
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        if 'expiry_date' in data and isinstance(data['expiry_date'], str):
            data['expiry_date'] = datetime.fromisoformat(data['expiry_date'])
        
        if 'manufacturing_date' in data and isinstance(data['manufacturing_date'], str):
            data['manufacturing_date'] = datetime.fromisoformat(data['manufacturing_date'])
        
        # إنشاء الكائن
        return cls(**data)
    
    def validate(self) -> tuple[bool, list[str]]:
        """التحقق من صحة البيانات"""
        errors = []
        
        if not self.name.strip():
            errors.append("اسم الصنف مطلوب")
        
        if not self.code.strip():
            errors.append("رمز الصنف مطلوب")
        
        if not self.main_category.strip():
            errors.append("التصنيف الرئيسي مطلوب")
        
        if not self.unit.strip():
            errors.append("وحدة القياس مطلوبة")
        
        if self.selling_price <= 0:
            errors.append("سعر البيع يجب أن يكون أكبر من صفر")
        
        if self.cost < 0:
            errors.append("التكلفة لا يمكن أن تكون سالبة")
        
        if self.current_quantity < 0:
            errors.append("الكمية الحالية لا يمكن أن تكون سالبة")
        
        return len(errors) == 0, errors
    
    def __str__(self) -> str:
        """تمثيل نصي للصنف"""
        return f"{self.name} ({self.code})"
    
    def __repr__(self) -> str:
        """تمثيل تقني للصنف"""
        return f"ItemModel(id={self.id}, name='{self.name}', code='{self.code}')"
