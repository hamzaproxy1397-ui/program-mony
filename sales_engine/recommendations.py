# -*- coding: utf-8 -*-
"""
نظام التوصيات الذكية
Smart Recommendations System
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math

class RecommendationEngine:
    """محرك التوصيات الذكية"""
    
    def __init__(self, database_manager=None):
        self.db_manager = database_manager
        self.purchase_history = defaultdict(list)  # customer_id -> [product_ids]
        self.product_associations = defaultdict(Counter)  # product_id -> {related_product_id: count}
        self.customer_preferences = defaultdict(dict)  # customer_id -> preferences
        self.product_popularity = Counter()  # product_id -> popularity_score
        
    def record_purchase(self, customer_id: int, product_ids: List[int], 
                       purchase_date: datetime = None):
        """تسجيل عملية شراء لتحليل التوصيات"""
        if purchase_date is None:
            purchase_date = datetime.now()
            
        # تسجيل تاريخ الشراء
        purchase_record = {
            'products': product_ids,
            'date': purchase_date,
            'quantity': len(product_ids)
        }
        
        self.purchase_history[customer_id].append(purchase_record)
        
        # تحديث شعبية المنتجات
        for product_id in product_ids:
            self.product_popularity[product_id] += 1
        
        # تحديث الارتباطات بين المنتجات
        self._update_product_associations(product_ids)
        
        # تحديث تفضيلات العميل
        self._update_customer_preferences(customer_id, product_ids)
    
    def _update_product_associations(self, product_ids: List[int]):
        """تحديث الارتباطات بين المنتجات"""
        for i, product1 in enumerate(product_ids):
            for j, product2 in enumerate(product_ids):
                if i != j:  # تجنب ربط المنتج بنفسه
                    self.product_associations[product1][product2] += 1
    
    def _update_customer_preferences(self, customer_id: int, product_ids: List[int]):
        """تحديث تفضيلات العميل"""
        if customer_id not in self.customer_preferences:
            self.customer_preferences[customer_id] = {
                'favorite_products': Counter(),
                'purchase_frequency': 0,
                'avg_order_size': 0,
                'last_purchase': datetime.now(),
                'preferred_categories': Counter()
            }
        
        prefs = self.customer_preferences[customer_id]
        
        # تحديث المنتجات المفضلة
        for product_id in product_ids:
            prefs['favorite_products'][product_id] += 1
        
        # تحديث تكرار الشراء
        prefs['purchase_frequency'] += 1
        
        # تحديث متوسط حجم الطلب
        total_items = sum(len(record['products']) for record in self.purchase_history[customer_id])
        prefs['avg_order_size'] = total_items / prefs['purchase_frequency']
        
        # تحديث تاريخ آخر شراء
        prefs['last_purchase'] = datetime.now()
    
    def get_product_recommendations(self, customer_id: Optional[int] = None,
                                  current_cart: List[int] = None,
                                  limit: int = 5) -> List[Dict]:
        """الحصول على توصيات المنتجات"""
        
        recommendations = []
        
        if customer_id:
            # توصيات مخصصة للعميل
            recommendations.extend(self._get_personalized_recommendations(customer_id, limit))
        
        if current_cart:
            # توصيات بناءً على السلة الحالية
            cart_recommendations = self._get_cart_based_recommendations(current_cart, limit)
            recommendations.extend(cart_recommendations)
        
        # توصيات عامة (المنتجات الأكثر شعبية)
        if len(recommendations) < limit:
            popular_recommendations = self._get_popular_recommendations(
                limit - len(recommendations),
                exclude_products=[r['product_id'] for r in recommendations]
            )
            recommendations.extend(popular_recommendations)
        
        # إزالة التكرارات وترتيب حسب النقاط
        unique_recommendations = {}
        for rec in recommendations:
            product_id = rec['product_id']
            if product_id not in unique_recommendations:
                unique_recommendations[product_id] = rec
            else:
                # دمج النقاط
                unique_recommendations[product_id]['score'] += rec['score']
        
        # ترتيب وإرجاع أفضل التوصيات
        sorted_recommendations = sorted(
            unique_recommendations.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_recommendations[:limit]
    
    def _get_personalized_recommendations(self, customer_id: int, limit: int) -> List[Dict]:
        """توصيات مخصصة للعميل"""
        recommendations = []
        
        if customer_id not in self.customer_preferences:
            return recommendations
        
        prefs = self.customer_preferences[customer_id]
        
        # المنتجات المفضلة للعميل
        favorite_products = prefs['favorite_products'].most_common(10)
        
        for product_id, frequency in favorite_products:
            # البحث عن منتجات مرتبطة
            related_products = self.product_associations[product_id].most_common(3)
            
            for related_id, association_count in related_products:
                # حساب نقاط التوصية
                score = self._calculate_recommendation_score(
                    customer_id, related_id, frequency, association_count
                )
                
                recommendations.append({
                    'product_id': related_id,
                    'score': score,
                    'reason': f'مرتبط بمنتج مفضل ({product_id})',
                    'type': 'personalized'
                })
        
        return recommendations
    
    def _get_cart_based_recommendations(self, cart_products: List[int], limit: int) -> List[Dict]:
        """توصيات بناءً على السلة الحالية"""
        recommendations = []
        
        for product_id in cart_products:
            # البحث عن منتجات مرتبطة
            related_products = self.product_associations[product_id].most_common(5)
            
            for related_id, association_count in related_products:
                if related_id not in cart_products:  # تجنب اقتراح منتجات موجودة في السلة
                    score = association_count * 0.8  # وزن أقل للتوصيات المبنية على السلة
                    
                    recommendations.append({
                        'product_id': related_id,
                        'score': score,
                        'reason': f'يُشترى عادة مع المنتج {product_id}',
                        'type': 'cart_based'
                    })
        
        return recommendations
    
    def _get_popular_recommendations(self, limit: int, exclude_products: List[int] = None) -> List[Dict]:
        """توصيات المنتجات الأكثر شعبية"""
        if exclude_products is None:
            exclude_products = []
        
        recommendations = []
        popular_products = self.product_popularity.most_common(limit * 2)
        
        for product_id, popularity in popular_products:
            if product_id not in exclude_products:
                recommendations.append({
                    'product_id': product_id,
                    'score': popularity * 0.5,  # وزن أقل للشعبية العامة
                    'reason': 'منتج شائع',
                    'type': 'popular'
                })
                
                if len(recommendations) >= limit:
                    break
        
        return recommendations
    
    def _calculate_recommendation_score(self, customer_id: int, product_id: int,
                                      customer_frequency: int, association_count: int) -> float:
        """حساب نقاط التوصية"""
        
        # العوامل المختلفة للنقاط
        base_score = association_count * 2  # قوة الارتباط
        customer_factor = customer_frequency * 1.5  # تفضيل العميل
        popularity_factor = self.product_popularity.get(product_id, 0) * 0.3  # الشعبية العامة
        
        # عامل الحداثة (المنتجات المشتراة مؤخراً تحصل على نقاط أعلى)
        if customer_id in self.customer_preferences:
            days_since_last_purchase = (
                datetime.now() - self.customer_preferences[customer_id]['last_purchase']
            ).days
            recency_factor = max(0, 30 - days_since_last_purchase) / 30  # تقل النقاط مع الوقت
        else:
            recency_factor = 0.5
        
        total_score = (base_score + customer_factor + popularity_factor) * (1 + recency_factor)
        
        return round(total_score, 2)
    
    def get_cross_sell_recommendations(self, product_id: int, limit: int = 3) -> List[Dict]:
        """توصيات البيع المتقاطع لمنتج محدد"""
        recommendations = []
        
        related_products = self.product_associations[product_id].most_common(limit)
        
        for related_id, count in related_products:
            # حساب قوة الارتباط
            total_purchases_product = self.product_popularity[product_id]
            association_strength = count / total_purchases_product if total_purchases_product > 0 else 0
            
            recommendations.append({
                'product_id': related_id,
                'association_strength': round(association_strength, 3),
                'co_purchase_count': count,
                'confidence': round(association_strength * 100, 1)  # نسبة مئوية
            })
        
        return recommendations
    
    def get_customer_insights(self, customer_id: int) -> Optional[Dict]:
        """تحليل سلوك العميل"""
        if customer_id not in self.customer_preferences:
            return None
        
        prefs = self.customer_preferences[customer_id]
        purchase_history = self.purchase_history[customer_id]
        
        # حساب متوسط الفترة بين المشتريات
        if len(purchase_history) > 1:
            purchase_dates = [record['date'] for record in purchase_history]
            purchase_dates.sort()
            intervals = []
            for i in range(1, len(purchase_dates)):
                interval = (purchase_dates[i] - purchase_dates[i-1]).days
                intervals.append(interval)
            avg_purchase_interval = sum(intervals) / len(intervals)
        else:
            avg_purchase_interval = None
        
        # تحديد نوع العميل
        customer_type = self._classify_customer(prefs, purchase_history)
        
        return {
            'customer_id': customer_id,
            'total_purchases': prefs['purchase_frequency'],
            'avg_order_size': round(prefs['avg_order_size'], 1),
            'favorite_products': dict(prefs['favorite_products'].most_common(5)),
            'last_purchase': prefs['last_purchase'],
            'avg_purchase_interval_days': round(avg_purchase_interval, 1) if avg_purchase_interval else None,
            'customer_type': customer_type,
            'loyalty_score': self._calculate_loyalty_score(prefs, purchase_history)
        }
    
    def _classify_customer(self, prefs: Dict, purchase_history: List[Dict]) -> str:
        """تصنيف العميل"""
        frequency = prefs['purchase_frequency']
        avg_order_size = prefs['avg_order_size']
        
        if frequency >= 10 and avg_order_size >= 5:
            return "عميل مميز"
        elif frequency >= 5:
            return "عميل منتظم"
        elif frequency >= 2:
            return "عميل متكرر"
        else:
            return "عميل جديد"
    
    def _calculate_loyalty_score(self, prefs: Dict, purchase_history: List[Dict]) -> float:
        """حساب نقاط الولاء"""
        frequency_score = min(prefs['purchase_frequency'] * 10, 50)  # حد أقصى 50
        order_size_score = min(prefs['avg_order_size'] * 5, 30)  # حد أقصى 30
        
        # عامل الحداثة
        days_since_last = (datetime.now() - prefs['last_purchase']).days
        recency_score = max(0, 20 - days_since_last * 0.5)  # حد أقصى 20
        
        total_score = frequency_score + order_size_score + recency_score
        return round(min(total_score, 100), 1)  # حد أقصى 100
    
    def export_recommendations_data(self, file_path: str) -> bool:
        """تصدير بيانات التوصيات"""
        try:
            data = {
                'product_associations': dict(self.product_associations),
                'product_popularity': dict(self.product_popularity),
                'customer_count': len(self.customer_preferences),
                'total_purchases': sum(prefs['purchase_frequency'] 
                                     for prefs in self.customer_preferences.values()),
                'export_date': datetime.now().isoformat()
            }
            
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"خطأ في تصدير بيانات التوصيات: {e}")
            return False
