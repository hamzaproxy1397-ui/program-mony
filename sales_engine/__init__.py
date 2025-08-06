# -*- coding: utf-8 -*-
"""
محرك المبيعات الذكي
Smart Sales Engine

يحتوي على جميع أنظمة المبيعات المتقدمة:
- نظام التسعير الذكي
- إدارة العروض والخصومات
- نظام التوصيات الذكية
- تحليل المبيعات المتقدم
"""

from .pricelist import PriceListManager
from .promotions import PromotionManager, PromotionType, PromotionCondition
from .recommendations import RecommendationEngine
from .analytics import SalesAnalytics, AnalyticsPeriod

__all__ = [
    'PriceListManager',
    'PromotionManager',
    'PromotionType',
    'PromotionCondition',
    'RecommendationEngine',
    'SalesAnalytics',
    'AnalyticsPeriod'
]


class SmartSalesEngine:
    """محرك المبيعات الذكي المتكامل"""

    def __init__(self, database_manager=None):
        self.db_manager = database_manager

        # تهيئة المكونات
        self.price_manager = PriceListManager(database_manager)
        self.promotion_manager = PromotionManager(database_manager)
        self.recommendation_engine = RecommendationEngine(database_manager)
        self.analytics = SalesAnalytics(database_manager)

    def process_sale(self, customer_id, cart_items, apply_promotions=True):
        """معالجة عملية بيع متكاملة"""

        result = {
            'success': False,
            'cart_items': cart_items,
            'pricing': {},
            'promotions_applied': [],
            'recommendations': [],
            'total_amount': 0,
            'final_amount': 0,
            'total_discount': 0
        }

        try:
            # 1. حساب الأسعار
            for item in cart_items:
                pricing = self.price_manager.get_final_price(
                    item['product_id'],
                    item['quantity'],
                    customer_id
                )
                item.update(pricing)
                result['pricing'][item['product_id']] = pricing

            # 2. تطبيق العروض والخصومات
            if apply_promotions:
                applicable_promotions = (
                    self.promotion_manager.get_applicable_promotions(
                        cart_items, customer_id
                    )
                )

                for promo in applicable_promotions:
                    promo_result = self.promotion_manager.apply_promotion(
                        promo['id'], cart_items, customer_id
                    )
                    if promo_result['success']:
                        result['promotions_applied'].append(promo_result)

            # 3. حساب المجاميع
            result['total_amount'] = sum(
                item['total_amount'] for item in cart_items
            )
            result['total_discount'] = sum(
                promo['discount_amount']
                for promo in result['promotions_applied']
            )
            result['final_amount'] = (
                result['total_amount'] - result['total_discount']
            )

            # 4. الحصول على التوصيات
            product_ids = [item['product_id'] for item in cart_items]
            result['recommendations'] = (
                self.recommendation_engine.get_product_recommendations(
                    customer_id, product_ids, limit=5
                )
            )

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)

        return result
