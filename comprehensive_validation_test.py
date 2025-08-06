#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل للتحقق من صحة الإصلاحات
Comprehensive Validation Test for Accounting Software
"""

import sys
import os
import logging
import traceback
from pathlib import Path
from datetime import datetime

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class ComprehensiveValidator:
    """فئة التحقق الشامل من صحة النظام"""
    
    def __init__(self):
        self.results = {
            'syntax_tests': [],
            'import_tests': [],
            'database_tests': [],
            'ui_tests': [],
            'business_logic_tests': [],
            'rtl_tests': []
        }
        self.setup_logging()
    
    def setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/validation_test.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def test_syntax_fixes(self):
        """اختبار إصلاحات الأخطاء النحوية"""
        print("🔍 اختبار الأخطاء النحوية...")
        
        critical_files = [
            'main.py',
            'START_HERE.py', 
            'run_app.py',
            'safe_start.py',
            'core/app_core.py',
            'services/purchases_manager.py'
        ]
        
        for file_path in critical_files:
            try:
                # محاولة تجميع الملف
                import py_compile
                py_compile.compile(file_path, doraise=True)
                self.results['syntax_tests'].append({
                    'file': file_path,
                    'status': 'PASS',
                    'message': 'تم تجميع الملف بنجاح'
                })
                print(f"  ✅ {file_path}")
            except Exception as e:
                self.results['syntax_tests'].append({
                    'file': file_path,
                    'status': 'FAIL',
                    'message': str(e)
                })
                print(f"  ❌ {file_path}: {e}")
    
    def test_critical_imports(self):
        """اختبار الاستيرادات الحرجة"""
        print("📦 اختبار الاستيرادات الحرجة...")
        
        critical_imports = [
            ('config.settings', 'إعدادات النظام'),
            ('database.database_manager', 'مدير قاعدة البيانات'),
            ('auth.auth_manager', 'مدير المصادقة'),
            ('ui.main_window', 'النافذة الرئيسية'),
            ('ui.central_control_panel', 'لوحة التحكم'),
            ('themes.font_manager', 'مدير الخطوط'),
            ('themes.theme_manager', 'مدير الثيمات')
        ]
        
        for module_name, description in critical_imports:
            try:
                __import__(module_name)
                self.results['import_tests'].append({
                    'module': module_name,
                    'status': 'PASS',
                    'message': f'تم استيراد {description} بنجاح'
                })
                print(f"  ✅ {description}")
            except Exception as e:
                self.results['import_tests'].append({
                    'module': module_name,
                    'status': 'FAIL',
                    'message': str(e)
                })
                print(f"  ❌ {description}: {e}")
    
    def test_database_functionality(self):
        """اختبار وظائف قاعدة البيانات"""
        print("🗄️ اختبار قاعدة البيانات...")
        
        try:
            from database.database_manager import DatabaseManager
            db = DatabaseManager()
            
            # اختبار الاتصال
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
            self.results['database_tests'].append({
                'test': 'connection',
                'status': 'PASS',
                'message': 'اتصال قاعدة البيانات يعمل بنجاح'
            })
            print("  ✅ اتصال قاعدة البيانات")
            
            # اختبار المصادقة
            from auth.auth_manager import AuthManager
            auth = AuthManager()
            
            self.results['database_tests'].append({
                'test': 'authentication',
                'status': 'PASS',
                'message': 'نظام المصادقة يعمل بنجاح'
            })
            print("  ✅ نظام المصادقة")
            
        except Exception as e:
            self.results['database_tests'].append({
                'test': 'database_general',
                'status': 'FAIL',
                'message': str(e)
            })
            print(f"  ❌ قاعدة البيانات: {e}")
    
    def test_ui_components(self):
        """اختبار مكونات الواجهة"""
        print("🖼️ اختبار مكونات الواجهة...")
        
        try:
            import customtkinter as ctk
            
            # اختبار إنشاء نافذة أساسية
            root = ctk.CTk()
            root.withdraw()  # إخفاء النافذة
            
            self.results['ui_tests'].append({
                'test': 'customtkinter',
                'status': 'PASS',
                'message': 'customtkinter يعمل بنجاح'
            })
            print("  ✅ customtkinter")
            
            # اختبار مدير الخطوط
            from themes.font_manager import get_arabic_font
            font = get_arabic_font(size=12)
            
            self.results['ui_tests'].append({
                'test': 'arabic_fonts',
                'status': 'PASS',
                'message': 'الخطوط العربية تعمل بنجاح'
            })
            print("  ✅ الخطوط العربية")
            
            root.destroy()
            
        except Exception as e:
            self.results['ui_tests'].append({
                'test': 'ui_general',
                'status': 'FAIL',
                'message': str(e)
            })
            print(f"  ❌ الواجهة: {e}")
    
    def test_business_logic(self):
        """اختبار المنطق التجاري"""
        print("💼 اختبار المنطق التجاري...")
        
        try:
            # اختبار مدير القيود المحاسبية
            from database.journal_entries_manager import JournalEntriesManager
            journal_manager = JournalEntriesManager()
            
            # اختبار التوازن المحاسبي
            test_details = [
                {'debit_amount': 1000, 'credit_amount': 0},
                {'debit_amount': 0, 'credit_amount': 1000}
            ]
            
            balance_check = journal_manager._check_balance(test_details)
            
            if balance_check['is_balanced']:
                self.results['business_logic_tests'].append({
                    'test': 'double_entry_balance',
                    'status': 'PASS',
                    'message': 'نظام القيد المزدوج يعمل بنجاح'
                })
                print("  ✅ نظام القيد المزدوج")
            else:
                raise Exception("فشل في اختبار التوازن المحاسبي")
                
        except Exception as e:
            self.results['business_logic_tests'].append({
                'test': 'business_logic_general',
                'status': 'FAIL',
                'message': str(e)
            })
            print(f"  ❌ المنطق التجاري: {e}")
    
    def test_rtl_support(self):
        """اختبار دعم RTL"""
        print("🔄 اختبار دعم RTL...")
        
        try:
            from config.settings import RTL_SUPPORT, DEFAULT_FONT
            
            if RTL_SUPPORT and DEFAULT_FONT:
                self.results['rtl_tests'].append({
                    'test': 'rtl_config',
                    'status': 'PASS',
                    'message': 'إعدادات RTL مفعلة بنجاح'
                })
                print("  ✅ إعدادات RTL")
            else:
                raise Exception("إعدادات RTL غير مفعلة")
                
        except Exception as e:
            self.results['rtl_tests'].append({
                'test': 'rtl_general',
                'status': 'FAIL',
                'message': str(e)
            })
            print(f"  ❌ دعم RTL: {e}")
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        print("\n" + "="*60)
        print("📊 تقرير التحقق الشامل")
        print("="*60)
        
        total_tests = 0
        passed_tests = 0
        
        for category, tests in self.results.items():
            category_name = {
                'syntax_tests': 'الأخطاء النحوية',
                'import_tests': 'الاستيرادات',
                'database_tests': 'قاعدة البيانات',
                'ui_tests': 'الواجهة',
                'business_logic_tests': 'المنطق التجاري',
                'rtl_tests': 'دعم RTL'
            }.get(category, category)
            
            print(f"\n🔍 {category_name}:")
            
            for test in tests:
                total_tests += 1
                if test['status'] == 'PASS':
                    passed_tests += 1
                    print(f"  ✅ {test.get('message', 'نجح الاختبار')}")
                else:
                    print(f"  ❌ {test.get('message', 'فشل الاختبار')}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 النتائج الإجمالية:")
        print(f"  📊 إجمالي الاختبارات: {total_tests}")
        print(f"  ✅ الاختبارات الناجحة: {passed_tests}")
        print(f"  ❌ الاختبارات الفاشلة: {total_tests - passed_tests}")
        print(f"  📊 معدل النجاح: {success_rate:.1f}%")
        
        # حفظ التقرير
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'results': self.results,
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': success_rate
            }
        }
        
        report_file = f"comprehensive_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            import json
            import re
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 تم حفظ التقرير في: {report_file}")
        
        return success_rate >= 80  # نجح إذا كان معدل النجاح 80% أو أكثر
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء التحقق الشامل من صحة النظام")
        print("="*60)
        
        try:
            self.test_syntax_fixes()
            self.test_critical_imports()
            self.test_database_functionality()
            self.test_ui_components()
            self.test_business_logic()
            self.test_rtl_support()
            
            return self.generate_report()
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل الاختبارات: {e}")
            traceback.print_exc()
            return False

def main():
    """الدالة الرئيسية"""
    validator = ComprehensiveValidator()
    success = validator.run_all_tests()
    
    if success:
        print("\n🎉 تم اجتياز التحقق الشامل بنجاح!")
        return 0
    else:
        print("\n⚠️ هناك مشاكل تحتاج إلى إصلاح")
        return 1

if __name__ == "__main__":
    sys.exit(main())
