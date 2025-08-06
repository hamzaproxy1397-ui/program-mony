# -*- coding: utf-8 -*-
"""
نظام التسعير الذكي
Smart Pricing System
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, date
import json
from pathlib import Path

class PriceListManager:
    """مدير قوائم الأسعار الذكي"""
    
    def __init__(self, database_manager=None):
        self.db_manager = database_manager
        self.price_lists = {}
        self.customer_price_groups = {}
        self.quantity_discounts = {}
        
    def create_price_list(self, name: str, description: str = "", 
                         currency: str = "SAR", is_default: bool = False) -> int:
        """إنشاء قائمة أسعار جديدة"""
        price_list = {
            'id': len(self.price_lists) + 1,
            'name': name,
            'description': description,
            'currency': currency,
            'is_default': is_default,
            'created_date': datetime.now(),
            'is_active': True,
            'items': {}
        }
        
        self.price_lists[price_list['id']] = price_list
        return price_list['id']
    
    def add_item_price(self, price_list_id: int, product_id: int, 
                      price: Decimal, min_quantity: int = 1) -> bool:
        """إضافة سعر منتج لقائمة أسعار"""
        if price_list_id not in self.price_lists:
            return False
            
        if product_id not in self.price_lists[price_list_id]['items']:
            self.price_lists[price_list_id]['items'][product_id] = []
            
        price_item = {
            'price': price,
            'min_quantity': min_quantity,
            'effective_date': datetime.now(),
            'is_active': True
        }
        
        self.price_lists[price_list_id]['items'][product_id].append(price_item)
        return True
    
    def get_product_price(self, product_id: int, quantity: int = 1, 
                         customer_id: Optional[int] = None, 
                         price_list_id: Optional[int] = None) -> Decimal:
        """الحصول على سعر المنتج حسب الكمية والعميل"""
        
        # تحديد قائمة الأسعار المناسبة
        if price_list_id is None:
            if customer_id and customer_id in self.customer_price_groups:
                price_list_id = self.customer_price_groups[customer_id]
            else:
                # البحث عن القائمة الافتراضية
                for pl_id, pl in self.price_lists.items():
                    if pl.get('is_default', False):
                        price_list_id = pl_id
                        break
        
        if price_list_id not in self.price_lists:
            return Decimal('0')
            
        price_list = self.price_lists[price_list_id]
        
        if product_id not in price_list['items']:
            return Decimal('0')
            
        # البحث عن أفضل سعر حسب الكمية
        best_price = Decimal('0')
        for price_item in price_list['items'][product_id]:
            if (price_item['is_active'] and 
                quantity >= price_item['min_quantity']):
                if best_price == 0 or price_item['price'] < best_price:
                    best_price = price_item['price']
        
        return best_price
    
    def set_customer_price_group(self, customer_id: int, price_list_id: int):
        """تعيين مجموعة أسعار للعميل"""
        self.customer_price_groups[customer_id] = price_list_id
    
    def add_quantity_discount(self, product_id: int, min_quantity: int, 
                            discount_percent: Decimal):
        """إضافة خصم كمية للمنتج"""
        if product_id not in self.quantity_discounts:
            self.quantity_discounts[product_id] = []
            
        discount = {
            'min_quantity': min_quantity,
            'discount_percent': discount_percent,
            'is_active': True
        }
        
        self.quantity_discounts[product_id].append(discount)
        # ترتيب حسب الكمية الأدنى
        self.quantity_discounts[product_id].sort(
            key=lambda x: x['min_quantity'], reverse=True
        )
    
    def calculate_quantity_discount(self, product_id: int, 
                                  quantity: int, base_price: Decimal) -> Tuple[Decimal, Decimal]:
        """حساب خصم الكمية"""
        if product_id not in self.quantity_discounts:
            return base_price, Decimal('0')
            
        applicable_discount = Decimal('0')
        
        for discount in self.quantity_discounts[product_id]:
            if (discount['is_active'] and 
                quantity >= discount['min_quantity']):
                applicable_discount = discount['discount_percent']
                break
        
        discount_amount = base_price * (applicable_discount / 100)
        final_price = base_price - discount_amount
        
        return final_price, discount_amount
    
    def get_final_price(self, product_id: int, quantity: int = 1,
                       customer_id: Optional[int] = None) -> Dict:
        """الحصول على السعر النهائي مع جميع الحسابات"""
        
        # السعر الأساسي
        base_price = self.get_product_price(product_id, quantity, customer_id)
        
        if base_price == 0:
            return {
                'base_price': Decimal('0'),
                'quantity_discount': Decimal('0'),
                'final_price': Decimal('0'),
                'total_amount': Decimal('0'),
                'discount_percent': Decimal('0')
            }
        
        # حساب خصم الكمية
        discounted_price, discount_amount = self.calculate_quantity_discount(
            product_id, quantity, base_price
        )
        
        # حساب المبلغ الإجمالي
        total_amount = discounted_price * quantity
        
        # حساب نسبة الخصم
        discount_percent = Decimal('0')
        if base_price > 0:
            discount_percent = (discount_amount / base_price) * 100
        
        return {
            'base_price': base_price,
            'quantity_discount': discount_amount,
            'final_price': discounted_price,
            'total_amount': total_amount,
            'discount_percent': discount_percent,
            'quantity': quantity
        }
    
    def export_price_list(self, price_list_id: int, file_path: str) -> bool:
        """تصدير قائمة أسعار إلى ملف"""
        if price_list_id not in self.price_lists:
            return False
            
        try:
            price_list = self.price_lists[price_list_id].copy()
            # تحويل التواريخ والأرقام العشرية للتصدير
            price_list['created_date'] = price_list['created_date'].isoformat()
            
            for product_id, items in price_list['items'].items():
                for item in items:
                    item['price'] = str(item['price'])
                    item['effective_date'] = item['effective_date'].isoformat()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(price_list, f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            print(f"خطأ في تصدير قائمة الأسعار: {e}")
            return False
    
    def import_price_list(self, file_path: str) -> Optional[int]:
        """استيراد قائمة أسعار من ملف"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # إنشاء قائمة أسعار جديدة
            price_list_id = self.create_price_list(
                data['name'], 
                data.get('description', ''),
                data.get('currency', 'SAR'),
                data.get('is_default', False)
            )
            
            # إضافة العناصر
            for product_id, items in data['items'].items():
                for item in items:
                    self.add_item_price(
                        price_list_id,
                        int(product_id),
                        Decimal(item['price']),
                        item.get('min_quantity', 1)
                    )
            
            return price_list_id
            
        except Exception as e:
            print(f"خطأ في استيراد قائمة الأسعار: {e}")
            return None
    
    def get_price_lists_summary(self) -> List[Dict]:
        """الحصول على ملخص قوائم الأسعار"""
        summary = []
        
        for pl_id, pl in self.price_lists.items():
            summary.append({
                'id': pl_id,
                'name': pl['name'],
                'description': pl['description'],
                'currency': pl['currency'],
                'is_default': pl.get('is_default', False),
                'is_active': pl.get('is_active', True),
                'items_count': len(pl['items']),
                'created_date': pl['created_date']
            })
        
        return summary
