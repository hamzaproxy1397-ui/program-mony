# -*- coding: utf-8 -*-
"""
مدير الأصناف الذكي - نظام الذكاء الاصطناعي المتكامل
Intelligent Item Manager - Integrated AI System
"""

import re
import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from decimal import Decimal
import sqlite3
from pathlib import Path

# محاولة استيراد مكتبات الذكاء الاصطناعي
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class IntelligentItemManager:
    """مدير الأصناف الذكي مع قدرات الذكاء الاصطناعي"""
    
    def __init__(self, db_connection=None):
        self.db_connection = db_connection
        self.project_root = Path(__file__).parent.parent
        
        # قواعد التصنيف الذكي
        self.category_rules = {
            'إلكترونيات': [
                'هاتف', 'جوال', 'كمبيوتر', 'لابتوب', 'تلفزيون', 'راديو', 'كاميرا',
                'سماعة', 'شاحن', 'بطارية', 'كابل', 'فلاش', 'ذاكرة', 'قرص'
            ],
            'ملابس': [
                'قميص', 'بنطلون', 'فستان', 'جاكيت', 'حذاء', 'جزمة', 'قبعة',
                'جوارب', 'ملابس', 'تيشيرت', 'بلوزة', 'تنورة', 'معطف'
            ],
            'أغذية': [
                'أرز', 'خبز', 'لحم', 'دجاج', 'سمك', 'خضار', 'فواكه', 'حليب',
                'جبن', 'زيت', 'سكر', 'ملح', 'توابل', 'عصير', 'ماء', 'شاي', 'قهوة'
            ],
            'كتب': [
                'كتاب', 'مجلة', 'جريدة', 'رواية', 'قاموس', 'موسوعة', 'دليل',
                'مرجع', 'دراسة', 'بحث', 'مذكرة', 'كراسة'
            ],
            'أدوات': [
                'مفك', 'مطرقة', 'منشار', 'مفتاح', 'أداة', 'معدة', 'جهاز',
                'آلة', 'قطعة غيار', 'برغي', 'مسمار', 'صامولة'
            ]
        }
        
        # نماذج التسعير الذكي
        self.pricing_models = {
            'cost_plus': {'markup_min': 0.15, 'markup_max': 0.50},
            'market_based': {'variance_threshold': 0.20},
            'value_based': {'quality_multiplier': 1.2}
        }
        
        # خوارزميات كشف التكرار
        self.similarity_threshold = 0.85
        
    def suggest_category(self, item_name: str, item_description: str = "") -> Dict[str, Any]:
        """اقتراح تصنيف الصنف بناءً على الاسم والوصف"""
        text = f"{item_name} {item_description}".lower()
        
        # تنظيف النص
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        
        # حساب النقاط لكل فئة
        category_scores = {}
        
        for category, keywords in self.category_rules.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword in text:
                    score += 1
                    matched_keywords.append(keyword)
                    
                # البحث عن كلمات مشابهة
                for word in words:
                    if self._calculate_similarity(word, keyword) > 0.8:
                        score += 0.5
                        if keyword not in matched_keywords:
                            matched_keywords.append(keyword)
            
            if score > 0:
                category_scores[category] = {
                    'score': score,
                    'confidence': min(score / len(keywords), 1.0),
                    'matched_keywords': matched_keywords
                }
        
        # ترتيب النتائج
        if category_scores:
            best_category = max(category_scores.keys(), 
                              key=lambda x: category_scores[x]['score'])
            
            return {
                'suggested_category': best_category,
                'confidence': category_scores[best_category]['confidence'],
                'all_suggestions': dict(sorted(category_scores.items(), 
                                             key=lambda x: x[1]['score'], reverse=True)),
                'matched_keywords': category_scores[best_category]['matched_keywords']
            }
        else:
            return {
                'suggested_category': 'عام',
                'confidence': 0.1,
                'all_suggestions': {},
                'matched_keywords': []
            }
    
    def predict_price(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """توقع سعر الصنف بناءً على البيانات المتاحة"""
        try:
            category = item_data.get('category', 'عام')
            cost_price = float(item_data.get('cost_price', 0))
            
            # الحصول على أسعار مشابهة من قاعدة البيانات
            similar_prices = self._get_similar_item_prices(item_data)
            
            predictions = {}
            
            # نموذج Cost-Plus
            if cost_price > 0:
                markup_range = self.pricing_models['cost_plus']
                min_price = cost_price * (1 + markup_range['markup_min'])
                max_price = cost_price * (1 + markup_range['markup_max'])
                avg_price = (min_price + max_price) / 2
                
                predictions['cost_plus'] = {
                    'price': round(avg_price, 2),
                    'min_price': round(min_price, 2),
                    'max_price': round(max_price, 2),
                    'confidence': 0.8
                }
            
            # نموذج Market-Based
            if similar_prices:
                market_avg = statistics.mean(similar_prices)
                market_median = statistics.median(similar_prices)
                market_std = statistics.stdev(similar_prices) if len(similar_prices) > 1 else 0
                
                predictions['market_based'] = {
                    'price': round(market_median, 2),
                    'avg_price': round(market_avg, 2),
                    'price_range': {
                        'min': round(min(similar_prices), 2),
                        'max': round(max(similar_prices), 2)
                    },
                    'std_deviation': round(market_std, 2),
                    'confidence': min(len(similar_prices) / 10, 0.9)
                }
            
            # التوصية النهائية
            if predictions:
                # اختيار أفضل نموذج بناءً على الثقة
                best_model = max(predictions.keys(), 
                               key=lambda x: predictions[x]['confidence'])
                
                recommended_price = predictions[best_model]['price']
                
                return {
                    'recommended_price': recommended_price,
                    'best_model': best_model,
                    'all_predictions': predictions,
                    'confidence': predictions[best_model]['confidence'],
                    'similar_items_count': len(similar_prices)
                }
            else:
                # سعر افتراضي بناءً على الفئة
                default_price = self._get_category_default_price(category)
                return {
                    'recommended_price': default_price,
                    'best_model': 'default',
                    'all_predictions': {},
                    'confidence': 0.3,
                    'similar_items_count': 0
                }
                
        except Exception as e:
            return {
                'recommended_price': 0.0,
                'best_model': 'error',
                'all_predictions': {},
                'confidence': 0.0,
                'error': str(e)
            }
    
    def detect_duplicates(self, item_name: str, item_code: str = "", 
                         barcode: str = "") -> List[Dict[str, Any]]:
        """كشف الأصناف المكررة أو المشابهة"""
        duplicates = []
        
        if not self.db_connection:
            return duplicates
        
        try:
            cursor = self.db_connection.cursor()
            
            # البحث عن تطابق دقيق في الرمز أو الباركود
            if item_code:
                cursor.execute("SELECT * FROM items WHERE code = ? AND is_active = 1", (item_code,))
                exact_matches = cursor.fetchall()
                for match in exact_matches:
                    duplicates.append({
                        'item': dict(match),
                        'match_type': 'exact_code',
                        'similarity': 1.0,
                        'confidence': 1.0
                    })
            
            if barcode:
                cursor.execute("SELECT * FROM items WHERE barcode = ? AND is_active = 1", (barcode,))
                barcode_matches = cursor.fetchall()
                for match in barcode_matches:
                    duplicates.append({
                        'item': dict(match),
                        'match_type': 'exact_barcode',
                        'similarity': 1.0,
                        'confidence': 1.0
                    })
            
            # البحث عن تشابه في الأسماء
            cursor.execute("SELECT id, name, code, barcode FROM items WHERE is_active = 1")
            all_items = cursor.fetchall()
            
            for item in all_items:
                similarity = self._calculate_similarity(item_name.lower(), item['name'].lower())
                
                if similarity >= self.similarity_threshold:
                    duplicates.append({
                        'item': dict(item),
                        'match_type': 'name_similarity',
                        'similarity': similarity,
                        'confidence': similarity
                    })
            
            # ترتيب النتائج حسب درجة التشابه
            duplicates.sort(key=lambda x: x['similarity'], reverse=True)
            
            return duplicates[:10]  # أفضل 10 نتائج
            
        except Exception as e:
            print(f"خطأ في كشف التكرار: {e}")
            return []
    
    def analyze_demand_forecast(self, item_id: int, days: int = 30) -> Dict[str, Any]:
        """تحليل وتوقع الطلب على الصنف"""
        if not self.db_connection:
            return {'error': 'لا يوجد اتصال بقاعدة البيانات'}
        
        try:
            cursor = self.db_connection.cursor()
            
            # الحصول على بيانات المبيعات التاريخية
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days * 3)  # 3 أضعاف الفترة للتحليل
            
            cursor.execute('''
                SELECT DATE(created_at) as sale_date, 
                       SUM(quantity) as total_quantity,
                       COUNT(*) as transaction_count
                FROM inventory_movements 
                WHERE item_id = ? AND movement_type = 'out' 
                      AND created_at BETWEEN ? AND ?
                GROUP BY DATE(created_at)
                ORDER BY sale_date
            ''', (item_id, start_date.isoformat(), end_date.isoformat()))
            
            sales_data = cursor.fetchall()
            
            if not sales_data:
                return {
                    'forecast': 0,
                    'trend': 'no_data',
                    'confidence': 0,
                    'recommendations': ['لا توجد بيانات مبيعات كافية للتحليل']
                }
            
            # تحليل الاتجاه
            quantities = [float(row['total_quantity']) for row in sales_data]
            
            if len(quantities) >= 7:  # نحتاج على الأقل أسبوع من البيانات
                # حساب المتوسط المتحرك
                moving_avg = self._calculate_moving_average(quantities, window=7)
                
                # تحديد الاتجاه
                trend = self._determine_trend(quantities)
                
                # توقع الطلب
                forecast = self._simple_forecast(quantities, days)
                
                # حساب الثقة
                confidence = min(len(quantities) / 30, 0.9)
                
                # التوصيات
                recommendations = self._generate_demand_recommendations(
                    forecast, trend, quantities
                )
                
                return {
                    'forecast': round(forecast, 2),
                    'trend': trend,
                    'confidence': confidence,
                    'historical_avg': round(statistics.mean(quantities), 2),
                    'recent_avg': round(statistics.mean(quantities[-7:]), 2),
                    'recommendations': recommendations,
                    'data_points': len(quantities)
                }
            else:
                avg_demand = statistics.mean(quantities)
                return {
                    'forecast': round(avg_demand, 2),
                    'trend': 'insufficient_data',
                    'confidence': 0.3,
                    'recommendations': ['بيانات غير كافية - استخدم المتوسط الحالي']
                }
                
        except Exception as e:
            return {
                'error': f'خطأ في تحليل الطلب: {e}',
                'forecast': 0,
                'confidence': 0
            }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """حساب درجة التشابه بين نصين"""
        if not text1 or not text2:
            return 0.0
        
        # تحويل إلى مجموعات من الكلمات
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # حساب Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _get_similar_item_prices(self, item_data: Dict[str, Any]) -> List[float]:
        """الحصول على أسعار الأصناف المشابهة"""
        if not self.db_connection:
            return []
        
        try:
            cursor = self.db_connection.cursor()
            category = item_data.get('category', '')
            
            # البحث عن أصناف في نفس الفئة
            cursor.execute('''
                SELECT selling_price FROM items i
                JOIN categories c ON i.category_id = c.id
                WHERE c.name = ? AND i.selling_price > 0 AND i.is_active = 1
                ORDER BY i.created_at DESC
                LIMIT 20
            ''', (category,))
            
            results = cursor.fetchall()
            return [float(row['selling_price']) for row in results]
            
        except Exception:
            return []
    
    def _get_category_default_price(self, category: str) -> float:
        """الحصول على السعر الافتراضي للفئة"""
        default_prices = {
            'إلكترونيات': 500.0,
            'ملابس': 100.0,
            'أغذية': 20.0,
            'كتب': 50.0,
            'أدوات': 150.0,
            'عام': 100.0
        }
        return default_prices.get(category, 100.0)
    
    def _calculate_moving_average(self, data: List[float], window: int) -> List[float]:
        """حساب المتوسط المتحرك"""
        if len(data) < window:
            return data
        
        moving_avg = []
        for i in range(len(data) - window + 1):
            avg = sum(data[i:i + window]) / window
            moving_avg.append(avg)
        
        return moving_avg
    
    def _determine_trend(self, data: List[float]) -> str:
        """تحديد اتجاه البيانات"""
        if len(data) < 3:
            return 'insufficient_data'
        
        # مقارنة النصف الأول بالنصف الثاني
        mid = len(data) // 2
        first_half_avg = statistics.mean(data[:mid])
        second_half_avg = statistics.mean(data[mid:])
        
        change_percent = (second_half_avg - first_half_avg) / first_half_avg * 100
        
        if change_percent > 10:
            return 'increasing'
        elif change_percent < -10:
            return 'decreasing'
        else:
            return 'stable'
    
    def _simple_forecast(self, data: List[float], days: int) -> float:
        """توقع بسيط بناءً على الاتجاه"""
        if len(data) < 2:
            return data[0] if data else 0
        
        # حساب متوسط الأيام الأخيرة
        recent_avg = statistics.mean(data[-min(7, len(data)):])
        
        # تطبيق عامل الاتجاه
        trend = self._determine_trend(data)
        
        if trend == 'increasing':
            return recent_avg * 1.1
        elif trend == 'decreasing':
            return recent_avg * 0.9
        else:
            return recent_avg
    
    def _generate_demand_recommendations(self, forecast: float, trend: str, 
                                       historical_data: List[float]) -> List[str]:
        """إنشاء توصيات بناءً على تحليل الطلب"""
        recommendations = []
        
        avg_demand = statistics.mean(historical_data)
        
        if trend == 'increasing':
            recommendations.append("الطلب في ازدياد - فكر في زيادة المخزون")
            if forecast > avg_demand * 1.5:
                recommendations.append("نمو سريع في الطلب - راجع استراتيجية التسعير")
        
        elif trend == 'decreasing':
            recommendations.append("الطلب في تراجع - قلل من الطلبيات الجديدة")
            recommendations.append("فكر في عروض ترويجية لتحفيز المبيعات")
        
        else:
            recommendations.append("الطلب مستقر - حافظ على مستوى المخزون الحالي")
        
        # توصيات إضافية
        if forecast < avg_demand * 0.5:
            recommendations.append("طلب منخفض - راجع جودة المنتج أو التسويق")
        
        return recommendations

    def generate_quality_score(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """تقييم جودة بيانات الصنف"""
        score = 0
        max_score = 100
        issues = []
        suggestions = []

        # فحص الحقول الأساسية (40 نقطة)
        if item_data.get('name'):
            score += 15
        else:
            issues.append("اسم الصنف مفقود")
            suggestions.append("أضف اسم واضح ومميز للصنف")

        if item_data.get('code'):
            score += 10
        else:
            issues.append("رمز الصنف مفقود")
            suggestions.append("أضف رمز فريد للصنف")

        if item_data.get('category_id'):
            score += 10
        else:
            issues.append("فئة الصنف غير محددة")
            suggestions.append("حدد فئة مناسبة للصنف")

        if item_data.get('unit_id'):
            score += 5
        else:
            issues.append("وحدة القياس غير محددة")
            suggestions.append("حدد وحدة قياس مناسبة")

        # فحص معلومات التسعير (30 نقطة)
        cost_price = float(item_data.get('cost_price', 0))
        selling_price = float(item_data.get('selling_price', 0))

        if cost_price > 0:
            score += 15
        else:
            issues.append("سعر التكلفة غير محدد")
            suggestions.append("أدخل سعر التكلفة الفعلي")

        if selling_price > 0:
            score += 10
            if cost_price > 0 and selling_price > cost_price:
                score += 5
            else:
                issues.append("سعر البيع أقل من سعر التكلفة")
                suggestions.append("راجع أسعار البيع والتكلفة")
        else:
            issues.append("سعر البيع غير محدد")
            suggestions.append("حدد سعر بيع مناسب")

        # فحص معلومات المخزون (20 نقطة)
        if item_data.get('min_stock_level'):
            score += 10
        else:
            suggestions.append("حدد الحد الأدنى للمخزون")

        if item_data.get('reorder_point'):
            score += 10
        else:
            suggestions.append("حدد نقطة إعادة الطلب")

        # فحص المعلومات الإضافية (10 نقاط)
        if item_data.get('description'):
            score += 5
        else:
            suggestions.append("أضف وصف تفصيلي للصنف")

        if item_data.get('barcode'):
            score += 5
        else:
            suggestions.append("أضف باركود للصنف")

        # تحديد مستوى الجودة
        if score >= 90:
            quality_level = "ممتاز"
            quality_color = "#4CAF50"
        elif score >= 75:
            quality_level = "جيد جداً"
            quality_color = "#8BC34A"
        elif score >= 60:
            quality_level = "جيد"
            quality_color = "#FFC107"
        elif score >= 40:
            quality_level = "مقبول"
            quality_color = "#FF9800"
        else:
            quality_level = "ضعيف"
            quality_color = "#F44336"

        return {
            'score': score,
            'max_score': max_score,
            'percentage': round((score / max_score) * 100, 1),
            'quality_level': quality_level,
            'quality_color': quality_color,
            'issues': issues,
            'suggestions': suggestions,
            'completeness': {
                'basic_info': len([x for x in ['name', 'code', 'category_id']
                                 if item_data.get(x)]) / 3,
                'pricing': len([x for x in ['cost_price', 'selling_price']
                              if float(item_data.get(x, 0)) > 0]) / 2,
                'inventory': len([x for x in ['min_stock_level', 'reorder_point']
                                if item_data.get(x)]) / 2,
                'additional': len([x for x in ['description', 'barcode']
                                 if item_data.get(x)]) / 2
            }
        }

def main():
    """اختبار نظام الذكاء الاصطناعي"""
    print("🤖 اختبار نظام الذكاء الاصطناعي للأصناف...")

    ai_manager = IntelligentItemManager()

    # اختبار اقتراح التصنيف
    test_items = [
        "هاتف ذكي سامسونج",
        "قميص قطني أزرق",
        "أرز بسمتي 5 كيلو",
        "كتاب البرمجة بالبايثون"
    ]

    print("\n📋 اختبار اقتراح التصنيف:")
    for item in test_items:
        result = ai_manager.suggest_category(item)
        print(f"  📦 {item}")
        print(f"     ➜ الفئة المقترحة: {result['suggested_category']}")
        print(f"     ➜ الثقة: {result['confidence']:.2%}")
        print()

    # اختبار توقع الأسعار
    print("💰 اختبار توقع الأسعار:")
    test_item_data = {
        'name': 'هاتف ذكي',
        'category': 'إلكترونيات',
        'cost_price': 800
    }

    price_prediction = ai_manager.predict_price(test_item_data)
    print(f"  📱 {test_item_data['name']}")
    print(f"     ➜ السعر المقترح: {price_prediction['recommended_price']} ريال")
    print(f"     ➜ النموذج المستخدم: {price_prediction['best_model']}")
    print(f"     ➜ الثقة: {price_prediction['confidence']:.2%}")

    # اختبار تقييم الجودة
    print("\n⭐ اختبار تقييم جودة البيانات:")
    quality_result = ai_manager.generate_quality_score(test_item_data)
    print(f"  📊 النتيجة: {quality_result['score']}/{quality_result['max_score']}")
    print(f"  📈 النسبة: {quality_result['percentage']}%")
    print(f"  🏆 المستوى: {quality_result['quality_level']}")

    print("\n🎉 تم اختبار نظام الذكاء الاصطناعي بنجاح!")

if __name__ == "__main__":
    main()
