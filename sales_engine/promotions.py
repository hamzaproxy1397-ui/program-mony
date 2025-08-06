# -*- coding: utf-8 -*-
"""
إدارة العروض والخصومات
Promotions and Discounts Management
"""

from typing import Dict, List, Optional, Union
from decimal import Decimal
from datetime import datetime, date
from enum import Enum
import json

class PromotionType(Enum):
    """أنواع العروض"""
    PERCENTAGE_DISCOUNT = "percentage_discount"  # خصم نسبي
    FIXED_AMOUNT_DISCOUNT = "fixed_amount_discount"  # خصم مبلغ ثابت
    BUY_X_GET_Y = "buy_x_get_y"  # اشتري X واحصل على Y
    FREE_SHIPPING = "free_shipping"  # شحن مجاني
    BUNDLE_DISCOUNT = "bundle_discount"  # خصم على المجموعة
    LOYALTY_POINTS = "loyalty_points"  # نقاط ولاء

class PromotionCondition(Enum):
    """شروط العروض"""
    MIN_QUANTITY = "min_quantity"  # حد أدنى للكمية
    MIN_AMOUNT = "min_amount"  # حد أدنى للمبلغ
    SPECIFIC_PRODUCTS = "specific_products"  # منتجات محددة
    PRODUCT_CATEGORY = "product_category"  # فئة منتجات
    CUSTOMER_GROUP = "customer_group"  # مجموعة عملاء
    FIRST_TIME_CUSTOMER = "first_time_customer"  # عميل جديد

class PromotionManager:
    """مدير العروض والخصومات"""
    
    def __init__(self, database_manager=None):
        self.db_manager = database_manager
        self.promotions = {}
        self.active_promotions = {}
        
    def create_promotion(self, name: str, description: str,
                        promotion_type: PromotionType,
                        start_date: date, end_date: date,
                        conditions: Dict, rewards: Dict) -> int:
        """إنشاء عرض جديد"""
        
        promotion_id = len(self.promotions) + 1
        
        promotion = {
            'id': promotion_id,
            'name': name,
            'description': description,
            'type': promotion_type,
            'start_date': start_date,
            'end_date': end_date,
            'conditions': conditions,
            'rewards': rewards,
            'is_active': True,
            'usage_count': 0,
            'max_usage': conditions.get('max_usage', None),
            'created_date': datetime.now(),
            'applicable_products': conditions.get('products', []),
            'applicable_categories': conditions.get('categories', []),
            'applicable_customers': conditions.get('customers', [])
        }
        
        self.promotions[promotion_id] = promotion
        self._update_active_promotions()
        
        return promotion_id
    
    def _update_active_promotions(self):
        """تحديث قائمة العروض النشطة"""
        current_date = date.today()
        self.active_promotions = {}
        
        for promo_id, promo in self.promotions.items():
            if (promo['is_active'] and 
                promo['start_date'] <= current_date <= promo['end_date']):
                
                # فحص حد الاستخدام
                if (promo['max_usage'] is None or 
                    promo['usage_count'] < promo['max_usage']):
                    self.active_promotions[promo_id] = promo
    
    def check_promotion_eligibility(self, promotion_id: int, 
                                  cart_items: List[Dict],
                                  customer_id: Optional[int] = None) -> bool:
        """فحص أهلية العرض"""
        
        if promotion_id not in self.active_promotions:
            return False
            
        promotion = self.active_promotions[promotion_id]
        conditions = promotion['conditions']
        
        # فحص الحد الأدنى للكمية
        if 'min_quantity' in conditions:
            total_quantity = sum(item['quantity'] for item in cart_items)
            if total_quantity < conditions['min_quantity']:
                return False
        
        # فحص الحد الأدنى للمبلغ
        if 'min_amount' in conditions:
            total_amount = sum(
                Decimal(str(item['price'])) * item['quantity'] 
                for item in cart_items
            )
            if total_amount < Decimal(str(conditions['min_amount'])):
                return False
        
        # فحص المنتجات المحددة
        if promotion['applicable_products']:
            cart_product_ids = [item['product_id'] for item in cart_items]
            if not any(pid in promotion['applicable_products'] 
                      for pid in cart_product_ids):
                return False
        
        # فحص فئات المنتجات
        if promotion['applicable_categories']:
            # يحتاج إلى تطبيق مع قاعدة البيانات للحصول على فئات المنتجات
            pass
        
        # فحص مجموعة العملاء
        if promotion['applicable_customers']:
            if customer_id not in promotion['applicable_customers']:
                return False
        
        return True
    
    def apply_promotion(self, promotion_id: int, cart_items: List[Dict],
                       customer_id: Optional[int] = None) -> Dict:
        """تطبيق العرض على السلة"""
        
        if not self.check_promotion_eligibility(promotion_id, cart_items, customer_id):
            return {
                'success': False,
                'message': 'العرض غير مؤهل للتطبيق',
                'discount_amount': Decimal('0')
            }
        
        promotion = self.active_promotions[promotion_id]
        promotion_type = promotion['type']
        rewards = promotion['rewards']
        
        result = {
            'success': True,
            'promotion_id': promotion_id,
            'promotion_name': promotion['name'],
            'discount_amount': Decimal('0'),
            'free_items': [],
            'loyalty_points': 0,
            'message': ''
        }
        
        if promotion_type == PromotionType.PERCENTAGE_DISCOUNT:
            result.update(self._apply_percentage_discount(cart_items, rewards))
            
        elif promotion_type == PromotionType.FIXED_AMOUNT_DISCOUNT:
            result.update(self._apply_fixed_discount(cart_items, rewards))
            
        elif promotion_type == PromotionType.BUY_X_GET_Y:
            result.update(self._apply_buy_x_get_y(cart_items, rewards))
            
        elif promotion_type == PromotionType.BUNDLE_DISCOUNT:
            result.update(self._apply_bundle_discount(cart_items, rewards))
            
        elif promotion_type == PromotionType.LOYALTY_POINTS:
            result.update(self._apply_loyalty_points(cart_items, rewards))
        
        # تحديث عداد الاستخدام
        self.promotions[promotion_id]['usage_count'] += 1
        
        return result
    
    def _apply_percentage_discount(self, cart_items: List[Dict], 
                                 rewards: Dict) -> Dict:
        """تطبيق خصم نسبي"""
        discount_percent = Decimal(str(rewards.get('discount_percent', 0)))
        max_discount = rewards.get('max_discount_amount')
        
        total_amount = sum(
            Decimal(str(item['price'])) * item['quantity'] 
            for item in cart_items
        )
        
        discount_amount = total_amount * (discount_percent / 100)
        
        if max_discount and discount_amount > Decimal(str(max_discount)):
            discount_amount = Decimal(str(max_discount))
        
        return {
            'discount_amount': discount_amount,
            'message': f'خصم {discount_percent}% على إجمالي المبلغ'
        }
    
    def _apply_fixed_discount(self, cart_items: List[Dict], 
                            rewards: Dict) -> Dict:
        """تطبيق خصم مبلغ ثابت"""
        discount_amount = Decimal(str(rewards.get('discount_amount', 0)))
        
        total_amount = sum(
            Decimal(str(item['price'])) * item['quantity'] 
            for item in cart_items
        )
        
        # التأكد من أن الخصم لا يتجاوز المبلغ الإجمالي
        if discount_amount > total_amount:
            discount_amount = total_amount
        
        return {
            'discount_amount': discount_amount,
            'message': f'خصم {discount_amount} ريال'
        }
    
    def _apply_buy_x_get_y(self, cart_items: List[Dict], 
                          rewards: Dict) -> Dict:
        """تطبيق عرض اشتري X واحصل على Y"""
        buy_quantity = rewards.get('buy_quantity', 1)
        get_quantity = rewards.get('get_quantity', 1)
        target_product_id = rewards.get('target_product_id')
        
        free_items = []
        
        for item in cart_items:
            if (target_product_id is None or 
                item['product_id'] == target_product_id):
                
                # حساب عدد العناصر المجانية
                eligible_sets = item['quantity'] // buy_quantity
                free_count = eligible_sets * get_quantity
                
                if free_count > 0:
                    free_items.append({
                        'product_id': item['product_id'],
                        'quantity': free_count,
                        'value': Decimal(str(item['price'])) * free_count
                    })
        
        total_free_value = sum(item['value'] for item in free_items)
        
        return {
            'discount_amount': total_free_value,
            'free_items': free_items,
            'message': f'اشتري {buy_quantity} واحصل على {get_quantity} مجاناً'
        }
    
    def _apply_bundle_discount(self, cart_items: List[Dict], 
                             rewards: Dict) -> Dict:
        """تطبيق خصم على مجموعة منتجات"""
        required_products = rewards.get('required_products', [])
        bundle_discount = Decimal(str(rewards.get('bundle_discount', 0)))
        
        cart_product_ids = [item['product_id'] for item in cart_items]
        
        # فحص وجود جميع المنتجات المطلوبة
        if all(pid in cart_product_ids for pid in required_products):
            return {
                'discount_amount': bundle_discount,
                'message': 'خصم على مجموعة المنتجات'
            }
        
        return {
            'discount_amount': Decimal('0'),
            'message': 'المجموعة غير مكتملة'
        }
    
    def _apply_loyalty_points(self, cart_items: List[Dict], 
                            rewards: Dict) -> Dict:
        """تطبيق نقاط الولاء"""
        points_per_riyal = rewards.get('points_per_riyal', 1)
        
        total_amount = sum(
            Decimal(str(item['price'])) * item['quantity'] 
            for item in cart_items
        )
        
        loyalty_points = int(total_amount * points_per_riyal)
        
        return {
            'loyalty_points': loyalty_points,
            'message': f'ستحصل على {loyalty_points} نقطة ولاء'
        }
    
    def get_applicable_promotions(self, cart_items: List[Dict],
                                customer_id: Optional[int] = None) -> List[Dict]:
        """الحصول على العروض المطبقة على السلة"""
        
        self._update_active_promotions()
        applicable = []
        
        for promo_id, promotion in self.active_promotions.items():
            if self.check_promotion_eligibility(promo_id, cart_items, customer_id):
                applicable.append({
                    'id': promo_id,
                    'name': promotion['name'],
                    'description': promotion['description'],
                    'type': promotion['type'].value,
                    'end_date': promotion['end_date']
                })
        
        return applicable
    
    def deactivate_promotion(self, promotion_id: int) -> bool:
        """إلغاء تفعيل عرض"""
        if promotion_id in self.promotions:
            self.promotions[promotion_id]['is_active'] = False
            self._update_active_promotions()
            return True
        return False
    
    def get_promotion_statistics(self, promotion_id: int) -> Optional[Dict]:
        """إحصائيات العرض"""
        if promotion_id not in self.promotions:
            return None
            
        promotion = self.promotions[promotion_id]
        
        return {
            'id': promotion_id,
            'name': promotion['name'],
            'usage_count': promotion['usage_count'],
            'max_usage': promotion['max_usage'],
            'start_date': promotion['start_date'],
            'end_date': promotion['end_date'],
            'is_active': promotion['is_active'],
            'days_remaining': (promotion['end_date'] - date.today()).days
        }
