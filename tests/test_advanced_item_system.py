#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبارات شاملة لنظام إدخال الأصناف المتقدم
Comprehensive tests for the advanced item entry system
"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import sqlite3
from unittest.mock import Mock, patch

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.advanced_dependency_manager import AdvancedDependencyManager
    from database.advanced_items_database import AdvancedItemsDatabase
    from ai.intelligent_item_manager import IntelligentItemManager
    from analytics.advanced_analytics_engine import AdvancedAnalyticsEngine
except ImportError as e:
    print(f"⚠️ تحذير: فشل في استيراد بعض الوحدات: {e}")


class TestAdvancedDependencyManager(unittest.TestCase):
    """اختبارات مدير التبعيات المتقدم"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.dependency_manager = AdvancedDependencyManager()
    
    def test_check_core_dependencies(self):
        """اختبار فحص التبعيات الأساسية"""
        # فحص tkinter (يجب أن يكون متوفر)
        is_available, version = self.dependency_manager.check_dependency('tkinter')
        self.assertTrue(is_available, "tkinter يجب أن يكون متوفراً")
        
        # فحص sqlite3 (يجب أن يكون متوفر)
        is_available, version = self.dependency_manager.check_dependency('sqlite3')
        self.assertTrue(is_available, "sqlite3 يجب أن يكون متوفراً")
    
    def test_check_optional_dependencies(self):
        """اختبار فحص التبعيات الاختيارية"""
        # فحص matplotlib
        is_available, version = self.dependency_manager.check_dependency('matplotlib')
        # لا نتطلب أن يكون متوفراً، لكن نتحقق من عمل الفحص
        self.assertIsInstance(is_available, bool)
        
        # فحص numpy
        is_available, version = self.dependency_manager.check_dependency('numpy')
        self.assertIsInstance(is_available, bool)
    
    def test_dependency_status_report(self):
        """اختبار تقرير حالة التبعيات"""
        status = self.dependency_manager.check_all_dependencies()
        self.assertIsInstance(status, dict)
        self.assertIn('tkinter', status)
        self.assertIn('sqlite3', status)


class TestAdvancedItemsDatabase(unittest.TestCase):
    """اختبارات قاعدة البيانات المتقدمة"""
    
    def setUp(self):
        """إعداد الاختبار"""
        # إنشاء قاعدة بيانات مؤقتة للاختبار
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.database = AdvancedItemsDatabase(db_path=self.temp_db.name)
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_database_initialization(self):
        """اختبار تهيئة قاعدة البيانات"""
        # التحقق من إنشاء الجداول
        conn = self.database.get_connection()
        cursor = conn.cursor()
        
        # فحص وجود جدول الأصناف
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        result = cursor.fetchone()
        self.assertIsNotNone(result, "جدول الأصناف يجب أن يكون موجوداً")
        
        # فحص وجود جدول الفئات
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
        result = cursor.fetchone()
        self.assertIsNotNone(result, "جدول الفئات يجب أن يكون موجوداً")
        
        conn.close()
    
    def test_add_item(self):
        """اختبار إضافة صنف جديد"""
        item_data = {
            'code': 'TEST001',
            'name': 'صنف تجريبي',
            'category_id': 1,
            'unit_id': 1,
            'cost_price': 100.0,
            'selling_price': 150.0,
            'current_stock': 50.0
        }
        
        result = self.database.add_item(item_data)
        self.assertTrue(result['success'], f"فشل في إضافة الصنف: {result.get('error', '')}")
        self.assertIsNotNone(result.get('item_id'), "يجب إرجاع معرف الصنف")
    
    def test_get_item(self):
        """اختبار استرجاع صنف"""
        # إضافة صنف أولاً
        item_data = {
            'code': 'TEST002',
            'name': 'صنف تجريبي 2',
            'category_id': 1,
            'unit_id': 1,
            'cost_price': 200.0,
            'selling_price': 300.0
        }
        
        add_result = self.database.add_item(item_data)
        self.assertTrue(add_result['success'])
        
        # استرجاع الصنف
        item_id = add_result['item_id']
        retrieved_item = self.database.get_item(item_id)
        
        self.assertIsNotNone(retrieved_item, "يجب استرجاع الصنف بنجاح")
        self.assertEqual(retrieved_item['code'], 'TEST002')
        self.assertEqual(retrieved_item['name'], 'صنف تجريبي 2')


class TestIntelligentItemManager(unittest.TestCase):
    """اختبارات مدير الأصناف الذكي"""
    
    def setUp(self):
        """إعداد الاختبار"""
        # إنشاء قاعدة بيانات مؤقتة
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # إنشاء اتصال قاعدة البيانات
        self.conn = sqlite3.connect(self.temp_db.name)
        self.ai_manager = IntelligentItemManager(self.conn)
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        self.conn.close()
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_suggest_category(self):
        """اختبار اقتراح التصنيف"""
        # اختبار تصنيف الإلكترونيات
        result = self.ai_manager.suggest_category("لابتوب ديل", "جهاز كمبيوتر محمول")
        self.assertIsInstance(result, dict)
        self.assertIn('suggested_category', result)
        self.assertIn('confidence', result)
        
        # اختبار تصنيف الأطعمة
        result = self.ai_manager.suggest_category("أرز بسمتي", "أرز طويل الحبة")
        self.assertIsInstance(result, dict)
    
    def test_predict_price(self):
        """اختبار توقع السعر"""
        result = self.ai_manager.predict_price(
            cost_price=100.0,
            category="إلكترونيات",
            item_name="لابتوب"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('predicted_price', result)
        self.assertIn('confidence', result)
        self.assertGreater(result['predicted_price'], 100.0, "السعر المتوقع يجب أن يكون أكبر من سعر التكلفة")
    
    def test_detect_duplicates(self):
        """اختبار كشف التكرار"""
        result = self.ai_manager.detect_duplicates("لابتوب ديل", "جهاز كمبيوتر محمول ديل")
        
        self.assertIsInstance(result, dict)
        self.assertIn('duplicates', result)
        self.assertIn('similarity_threshold', result)
    
    def test_quality_score(self):
        """اختبار تقييم جودة البيانات"""
        item_data = {
            'name': 'لابتوب ديل',
            'description': 'جهاز كمبيوتر محمول عالي الأداء',
            'category': 'إلكترونيات',
            'cost_price': 1000.0,
            'selling_price': 1500.0,
            'barcode': '1234567890123'
        }
        
        result = self.ai_manager.calculate_quality_score(item_data)
        
        self.assertIsInstance(result, dict)
        self.assertIn('overall_score', result)
        self.assertIn('details', result)
        self.assertGreaterEqual(result['overall_score'], 0)
        self.assertLessEqual(result['overall_score'], 100)


class TestAdvancedAnalyticsEngine(unittest.TestCase):
    """اختبارات محرك التحليلات المتقدم"""
    
    def setUp(self):
        """إعداد الاختبار"""
        # إنشاء قاعدة بيانات مؤقتة
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # إنشاء اتصال قاعدة البيانات
        self.conn = sqlite3.connect(self.temp_db.name)
        
        # إنشاء جداول أساسية للاختبار
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_movements (
                id INTEGER PRIMARY KEY,
                item_id INTEGER,
                movement_type TEXT,
                quantity DECIMAL(15,4),
                unit_cost DECIMAL(15,4),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
        self.analytics_engine = AdvancedAnalyticsEngine(self.conn)
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        self.conn.close()
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    @patch('matplotlib.pyplot.show')
    def test_generate_sales_trend_chart(self, mock_show):
        """اختبار إنشاء رسم اتجاه المبيعات"""
        # إدراج بيانات تجريبية
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO inventory_movements (item_id, movement_type, quantity, unit_cost)
            VALUES (1, 'out', 10, 100.0)
        ''')
        self.conn.commit()
        
        result = self.analytics_engine.generate_sales_trend_chart(days=30)
        
        self.assertIsInstance(result, dict)
        self.assertIn('chart_data', result)
        self.assertIn('summary', result)
    
    def test_calculate_profit_margins(self):
        """اختبار حساب هوامش الربح"""
        # إدراج بيانات تجريبية
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO inventory_movements (item_id, movement_type, quantity, unit_cost)
            VALUES (1, 'out', 5, 150.0)
        ''')
        self.conn.commit()
        
        result = self.analytics_engine.calculate_profit_margins()
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_revenue', result)
        self.assertIn('total_cost', result)
        self.assertIn('profit_margin', result)


class TestSystemIntegration(unittest.TestCase):
    """اختبارات التكامل بين أجزاء النظام"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.database = AdvancedItemsDatabase(db_path=self.temp_db.name)
        self.conn = self.database.get_connection()
        self.ai_manager = IntelligentItemManager(self.conn)
        self.analytics_engine = AdvancedAnalyticsEngine(self.conn)
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        self.conn.close()
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_full_item_workflow(self):
        """اختبار سير العمل الكامل للصنف"""
        # 1. اقتراح التصنيف
        category_suggestion = self.ai_manager.suggest_category("لابتوب ديل", "جهاز كمبيوتر")
        self.assertIsInstance(category_suggestion, dict)
        
        # 2. توقع السعر
        price_prediction = self.ai_manager.predict_price(1000.0, "إلكترونيات", "لابتوب")
        self.assertIsInstance(price_prediction, dict)
        
        # 3. إضافة الصنف إلى قاعدة البيانات
        item_data = {
            'code': 'LAPTOP001',
            'name': 'لابتوب ديل',
            'category_id': 1,
            'unit_id': 1,
            'cost_price': 1000.0,
            'selling_price': price_prediction.get('predicted_price', 1500.0),
            'current_stock': 10.0
        }
        
        add_result = self.database.add_item(item_data)
        self.assertTrue(add_result['success'])
        
        # 4. تقييم جودة البيانات
        quality_score = self.ai_manager.calculate_quality_score(item_data)
        self.assertIsInstance(quality_score, dict)
        self.assertIn('overall_score', quality_score)


def run_tests():
    """تشغيل جميع الاختبارات"""
    print("🧪 بدء تشغيل الاختبارات الشاملة لنظام إدخال الأصناف المتقدم")
    print("=" * 60)
    
    # إنشاء مجموعة الاختبارات
    test_suite = unittest.TestSuite()
    
    # إضافة اختبارات مدير التبعيات
    test_suite.addTest(unittest.makeSuite(TestAdvancedDependencyManager))
    
    # إضافة اختبارات قاعدة البيانات
    test_suite.addTest(unittest.makeSuite(TestAdvancedItemsDatabase))
    
    # إضافة اختبارات الذكاء الاصطناعي
    test_suite.addTest(unittest.makeSuite(TestIntelligentItemManager))
    
    # إضافة اختبارات التحليلات
    test_suite.addTest(unittest.makeSuite(TestAdvancedAnalyticsEngine))
    
    # إضافة اختبارات التكامل
    test_suite.addTest(unittest.makeSuite(TestSystemIntegration))
    
    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # طباعة النتائج
    print("\n" + "=" * 60)
    print("📊 نتائج الاختبارات:")
    print(f"✅ اختبارات نجحت: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ اختبارات فشلت: {len(result.failures)}")
    print(f"⚠️ أخطاء: {len(result.errors)}")
    
    if result.failures:
        print("\n🔴 الاختبارات الفاشلة:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️ الأخطاء:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # إرجاع النتيجة
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
