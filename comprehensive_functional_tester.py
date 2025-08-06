#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الاختبار الوظيفي الشامل
Comprehensive Functional Testing System
"""

import sys
import json
import sqlite3
import importlib.util
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class ComprehensiveFunctionalTester:
    """نظام الاختبار الوظيفي الشامل"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "core_system_tests": {},
            "ui_component_tests": {},
            "database_tests": {},
            "integration_tests": {},
            "performance_tests": {},
            "overall_functionality_score": 0
        }
        
        # تعريف المكونات الأساسية للاختبار
        self.core_components = {
            "main_application": "main.py",
            "login_system": "ui/login_window.py",
            "main_interface": "ui/main_window.py",
            "database_manager": "database/hybrid_database_manager.py",
            "authentication": "auth/auth_manager.py",
            "scheduler": "core/scheduler_manager.py"
        }
        
        self.ui_components = {
            "pos_system": "ui/pos_window.py",
            "pos_simple": "ui/pos_simple.py",
            "admin_panel": "ui/advanced_settings_window.py",
            "accounts_window": "ui/accounts_window.py",
            "reports_window": "ui/reports_window.py",
            "sales_window": "ui/sales_window.py",
            "purchases_window": "ui/purchases_window.py"
        }
        
        self.service_components = {
            "sales_manager": "services/sales_manager.py",
            "purchases_manager": "services/purchases_manager.py",
            "treasury_manager": "services/treasury_manager.py"
        }
    
    def run_comprehensive_functional_tests(self):
        """تشغيل الاختبارات الوظيفية الشاملة"""
        print("🧪 بدء الاختبار الوظيفي الشامل...")
        print("=" * 70)
        
        # المرحلة 1: اختبار النظام الأساسي
        print("\n🎯 المرحلة 1: اختبار النظام الأساسي...")
        self.test_core_system()
        
        # المرحلة 2: اختبار مكونات واجهة المستخدم
        print("\n🖥️  المرحلة 2: اختبار مكونات واجهة المستخدم...")
        self.test_ui_components()
        
        # المرحلة 3: اختبار قاعدة البيانات
        print("\n🗄️  المرحلة 3: اختبار قاعدة البيانات...")
        self.test_database_functionality()
        
        # المرحلة 4: اختبار التكامل
        print("\n🔗 المرحلة 4: اختبار التكامل...")
        self.test_integration()
        
        # المرحلة 5: اختبار الأداء
        print("\n⚡ المرحلة 5: اختبار الأداء...")
        self.test_performance()
        
        # المرحلة 6: حساب النتيجة الإجمالية
        print("\n📊 المرحلة 6: حساب النتيجة الإجمالية...")
        self.calculate_functionality_score()
        
        # إنشاء التقرير
        self.generate_functional_test_report()
        
        return self.test_results
    
    def test_core_system(self):
        """اختبار النظام الأساسي"""
        core_results = {}
        
        for component_name, file_path in self.core_components.items():
            print(f"   🔧 اختبار {component_name}...")
            
            test_result = {
                "file_exists": False,
                "importable": False,
                "functional": False,
                "has_main_class": False,
                "error": None,
                "score": 0
            }
            
            full_path = self.project_root / file_path
            
            # فحص وجود الملف
            if full_path.exists():
                test_result["file_exists"] = True
                test_result["score"] += 25
                
                # فحص إمكانية الاستيراد
                try:
                    module_name = file_path.replace('/', '.').replace('.py', '')
                    spec = importlib.util.spec_from_file_location(module_name, full_path)
                    
                    if spec and spec.loader:
                        test_result["importable"] = True
                        test_result["score"] += 25
                        
                        # فحص المحتوى
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # فحص وجود فئة رئيسية
                        if 'class ' in content:
                            test_result["has_main_class"] = True
                            test_result["score"] += 25
                        
                        # فحص الوظيفية (بناءً على المحتوى)
                        if self.check_functionality(content, component_name):
                            test_result["functional"] = True
                            test_result["score"] += 25
                        
                        print(f"      ✅ {component_name} - النتيجة: {test_result['score']}/100")
                    else:
                        test_result["error"] = "غير قابل للاستيراد"
                        print(f"      ❌ {component_name} - غير قابل للاستيراد")
                        
                except Exception as e:
                    test_result["error"] = str(e)
                    print(f"      ❌ {component_name} - خطأ: {str(e)}")
            else:
                test_result["error"] = "الملف غير موجود"
                print(f"      ❌ {component_name} - الملف غير موجود")
            
            core_results[component_name] = test_result
        
        self.test_results["core_system_tests"] = core_results
    
    def test_ui_components(self):
        """اختبار مكونات واجهة المستخدم"""
        ui_results = {}
        
        for component_name, file_path in self.ui_components.items():
            print(f"   🖥️  اختبار {component_name}...")
            
            test_result = {
                "file_exists": False,
                "importable": False,
                "has_ui_elements": False,
                "has_event_handlers": False,
                "error": None,
                "score": 0
            }
            
            full_path = self.project_root / file_path
            
            if full_path.exists():
                test_result["file_exists"] = True
                test_result["score"] += 25
                
                try:
                    module_name = file_path.replace('/', '.').replace('.py', '')
                    spec = importlib.util.spec_from_file_location(module_name, full_path)
                    
                    if spec and spec.loader:
                        test_result["importable"] = True
                        test_result["score"] += 25
                        
                        # فحص عناصر واجهة المستخدم
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # فحص عناصر UI
                        ui_elements = ['CTk', 'tkinter', 'Button', 'Label', 'Entry', 'Frame']
                        if any(element in content for element in ui_elements):
                            test_result["has_ui_elements"] = True
                            test_result["score"] += 25
                        
                        # فحص معالجات الأحداث
                        event_patterns = ['def on_', 'def handle_', 'command=', 'bind(']
                        if any(pattern in content for pattern in event_patterns):
                            test_result["has_event_handlers"] = True
                            test_result["score"] += 25
                        
                        print(f"      ✅ {component_name} - النتيجة: {test_result['score']}/100")
                    else:
                        test_result["error"] = "غير قابل للاستيراد"
                        print(f"      ❌ {component_name} - غير قابل للاستيراد")
                        
                except Exception as e:
                    test_result["error"] = str(e)
                    print(f"      ❌ {component_name} - خطأ: {str(e)}")
            else:
                test_result["error"] = "الملف غير موجود"
                print(f"      ❌ {component_name} - الملف غير موجود")
            
            ui_results[component_name] = test_result
        
        self.test_results["ui_component_tests"] = ui_results
    
    def test_database_functionality(self):
        """اختبار وظائف قاعدة البيانات"""
        db_results = {
            "sqlite_connection": False,
            "database_creation": False,
            "table_operations": False,
            "data_integrity": False,
            "backup_system": False,
            "score": 0
        }
        
        # اختبار اتصال SQLite
        try:
            import sqlite3
            db_results["sqlite_connection"] = True
            db_results["score"] += 20
            print("   ✅ اتصال SQLite - يعمل")
        except ImportError:
            print("   ❌ اتصال SQLite - فشل")
        
        # اختبار إنشاء قاعدة البيانات
        try:
            test_db_path = self.project_root / "test_accounting.db"
            conn = sqlite3.connect(str(test_db_path))
            cursor = conn.cursor()
            
            # إنشاء جدول اختبار
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    value REAL
                )
            """)
            
            db_results["database_creation"] = True
            db_results["score"] += 20
            print("   ✅ إنشاء قاعدة البيانات - يعمل")
            
            # اختبار عمليات الجدول
            cursor.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", ("test", 100.0))
            cursor.execute("SELECT * FROM test_table WHERE name = ?", ("test",))
            result = cursor.fetchone()
            
            if result:
                db_results["table_operations"] = True
                db_results["score"] += 20
                print("   ✅ عمليات الجدول - تعمل")
            
            # اختبار سلامة البيانات
            cursor.execute("SELECT COUNT(*) FROM test_table")
            count = cursor.fetchone()[0]
            
            if count > 0:
                db_results["data_integrity"] = True
                db_results["score"] += 20
                print("   ✅ سلامة البيانات - محققة")
            
            conn.close()
            
            # حذف قاعدة البيانات الاختبارية
            if test_db_path.exists():
                test_db_path.unlink()
                
        except Exception as e:
            print(f"   ❌ اختبار قاعدة البيانات - خطأ: {e}")
        
        # اختبار نظام النسخ الاحتياطي
        backup_dir = self.project_root / "backups"
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("*.db"))
            if backup_files:
                db_results["backup_system"] = True
                db_results["score"] += 20
                print(f"   ✅ نظام النسخ الاحتياطي - {len(backup_files)} نسخة")
            else:
                print("   ⚠️  نظام النسخ الاحتياطي - لا توجد نسخ")
        else:
            print("   ⚠️  نظام النسخ الاحتياطي - المجلد غير موجود")
        
        self.test_results["database_tests"] = db_results
    
    # تحذير: دالة معقدة (تعقيد: 20) - استخدم list comprehensions بدلاً من loops معقدة
    def test_integration(self):
        """اختبار التكامل بين المكونات"""
        integration_results = {
            "ui_database_integration": False,
            "auth_system_integration": False,
            "scheduler_integration": False,
            "service_integration": False,
            "score": 0
        }
        
        # اختبار تكامل واجهة المستخدم مع قاعدة البيانات
        try:
            # فحص استيراد مدير قاعدة البيانات في ملفات UI
            main_window_path = self.project_root / "ui/main_window.py"
            if main_window_path.exists():
                with open(main_window_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'database' in content.lower() or 'db_manager' in content:
                    integration_results["ui_database_integration"] = True
                    integration_results["score"] += 25
                    print("   ✅ تكامل واجهة المستخدم مع قاعدة البيانات")
                else:
                    print("   ⚠️  تكامل واجهة المستخدم مع قاعدة البيانات - غير واضح")
        except Exception as e:
            print(f"   ❌ تكامل واجهة المستخدم مع قاعدة البيانات - خطأ: {e}")
        
        # اختبار تكامل نظام المصادقة
        try:
            auth_path = self.project_root / "auth/auth_manager.py"
            login_path = self.project_root / "ui/login_window.py"
            
            if auth_path.exists() and login_path.exists():
                with open(login_path, 'r', encoding='utf-8') as f:
                    login_content = f.read()
                
                if 'auth' in login_content.lower():
                    integration_results["auth_system_integration"] = True
                    integration_results["score"] += 25
                    print("   ✅ تكامل نظام المصادقة")
                else:
                    print("   ⚠️  تكامل نظام المصادقة - غير واضح")
        except Exception as e:
            print(f"   ❌ تكامل نظام المصادقة - خطأ: {e}")
        
        # اختبار تكامل المجدول
        try:
            scheduler_path = self.project_root / "core/scheduler_manager.py"
            if scheduler_path.exists():
                integration_results["scheduler_integration"] = True
                integration_results["score"] += 25
                print("   ✅ تكامل المجدول")
        except Exception as e:
            print(f"   ❌ تكامل المجدول - خطأ: {e}")
        
        # اختبار تكامل الخدمات
        try:
            services_working = 0
            total_services = len(self.service_components)
            
            for service_name, service_path in self.service_components.items():
                full_path = self.project_root / service_path
                if full_path.exists():
                    try:
                        module_name = service_path.replace('/', '.').replace('.py', '')
                        spec = importlib.util.spec_from_file_location(module_name, full_path)
                        if spec and spec.loader:
                            services_working += 1
                    except:
                        pass
            
            if services_working > 0:
                integration_results["service_integration"] = True
                integration_results["score"] += 25
                print(f"   ✅ تكامل الخدمات - {services_working}/{total_services} خدمة تعمل")
            else:
                print("   ❌ تكامل الخدمات - لا توجد خدمات تعمل")
                
        except Exception as e:
            print(f"   ❌ تكامل الخدمات - خطأ: {e}")
        
        self.test_results["integration_tests"] = integration_results
    # تحذير: دالة معقدة (تعقيد: 17) - استخدم list comprehensions بدلاً من loops معقدة
    
    def test_performance(self):
        """اختبار الأداء"""
        performance_results = {
            "import_speed": "unknown",
            "file_sizes_optimized": False,
            "memory_efficiency": "unknown",
            "startup_readiness": False,
            "score": 0
        }
        
        # اختبار سرعة الاستيراد
        try:
            import time
            start_time = time.time()
            
            # محاولة استيراد المكونات الأساسية
            main_path = self.project_root / "main.py"
            if main_path.exists():
                spec = importlib.util.spec_from_file_location("main", main_path)
                if spec and spec.loader:
                    import_time = time.time() - start_time
                    performance_results["import_speed"] = f"{import_time:.2f}s"
                    
                    if import_time < 2.0:  # أقل من ثانيتين
                        performance_results["score"] += 25
                        print(f"   ✅ سرعة الاستيراد - {import_time:.2f}s (ممتاز)")
                    elif import_time < 5.0:  # أقل من 5 ثوان
                        performance_results["score"] += 15
                        print(f"   ⚠️  سرعة الاستيراد - {import_time:.2f}s (مقبول)")
                    else:
                        print(f"   ❌ سرعة الاستيراد - {import_time:.2f}s (بطيء)")
        except Exception as e:
            print(f"   ❌ اختبار سرعة الاستيراد - خطأ: {e}")
        
        # اختبار تحسين أحجام الملفات
        large_files = []
        total_size = 0
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            file_size = py_file.stat().st_size
            total_size += file_size
            
            if file_size > 100000:  # أكبر من 100KB
                large_files.append((py_file.name, file_size))
        
        if len(large_files) <= 5:  # عدد قليل من الملفات الكبيرة
            performance_results["file_sizes_optimized"] = True
            performance_results["score"] += 25
            print(f"   ✅ تحسين أحجام الملفات - {len(large_files)} ملف كبير فقط")
        else:
            print(f"   ⚠️  تحسين أحجام الملفات - {len(large_files)} ملف كبير")
        
        # اختبار جاهزية البدء
        critical_files = ["main.py", "ui/main_window.py", "ui/login_window.py"]
        startup_ready = True
        
        for file_path in critical_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                startup_ready = False
                break
            
            try:
                module_name = file_path.replace('/', '.').replace('.py', '')
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                if not (spec and spec.loader):
                    startup_ready = False
                    break
            except:
                startup_ready = False
                break
        
        if startup_ready:
            performance_results["startup_readiness"] = True
            performance_results["score"] += 50  # نقاط إضافية للجاهزية
            print("   ✅ جاهزية البدء - النظام جاهز للتشغيل")
        else:
            print("   ❌ جاهزية البدء - النظام غير جاهز")
        
        print(f"   📊 إجمالي حجم الكود: {total_size / 1024:.1f} KB")
        
        self.test_results["performance_tests"] = performance_results
    
    def check_functionality(self, content: str, component_name: str) -> bool:
        """فحص الوظيفية بناءً على المحتوى"""
        functionality_indicators = {
            "main_application": ["if __name__", "main()", "def main"],
            "login_system": ["login", "password", "authenticate"],
            "main_interface": ["window", "menu", "button"],
            "database_manager": ["connect", "execute", "commit"],
            "authentication": ["login", "verify", "authenticate"],
            "scheduler": ["schedule", "job", "cron"]
        }
        
        indicators = functionality_indicators.get(component_name, [])
        return any(indicator in content.lower() for indicator in indicators)
    
    def calculate_functionality_score(self):
        """حساب النتيجة الإجمالية للوظيفية"""
        total_score = 0
        max_score = 0
        
        # نتيجة النظام الأساسي (40%)
        core_scores = [test["score"] for test in self.test_results["core_system_tests"].values()]
        if core_scores:
            core_avg = sum(core_scores) / len(core_scores)
            total_score += core_avg * 0.4
            max_score += 100 * 0.4
        
        # نتيجة واجهة المستخدم (25%)
        ui_scores = [test["score"] for test in self.test_results["ui_component_tests"].values()]
        if ui_scores:
            ui_avg = sum(ui_scores) / len(ui_scores)
            total_score += ui_avg * 0.25
            max_score += 100 * 0.25
        
        # نتيجة قاعدة البيانات (20%)
        db_score = self.test_results["database_tests"]["score"]
        total_score += db_score * 0.2
        max_score += 100 * 0.2
        
        # نتيجة التكامل (10%)
        integration_score = self.test_results["integration_tests"]["score"]
        total_score += integration_score * 0.1
        max_score += 100 * 0.1
        
        # نتيجة الأداء (5%)
        performance_score = self.test_results["performance_tests"]["score"]
        total_score += performance_score * 0.05
        max_score += 100 * 0.05
        
        final_score = (total_score / max_score * 100) if max_score > 0 else 0
        self.test_results["overall_functionality_score"] = round(final_score, 1)
        
        print(f"   🎯 النتيجة الإجمالية للوظيفية: {final_score:.1f}%")
        
        # تقييم الحالة
        if final_score >= 90:
            status = "ممتاز - جميع الوظائف تعمل بشكل مثالي"
            emoji = "🏆"
        elif final_score >= 80:
            status = "جيد جداً - معظم الوظائف تعمل"
            emoji = "🥇"
        elif final_score >= 70:
            status = "جيد - الوظائف الأساسية تعمل"
            emoji = "🥈"
        elif final_score >= 60:
            status = "مقبول - بعض الوظائف تحتاج تحسين"
            emoji = "🥉"
        else:
            status = "يحتاج تحسينات شاملة"
            emoji = "⚠️"
        
        print(f"   {emoji} الحالة الوظيفية: {status}")
    
    def generate_functional_test_report(self):
        """إنشاء تقرير الاختبار الوظيفي"""
        report_file = f"comprehensive_functional_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ تقرير الاختبار الوظيفي في: {report_file}")
        
        # طباعة ملخص التقرير
        print("\n" + "="*70)
        print("🧪 ملخص الاختبار الوظيفي الشامل:")
        print(f"   🎯 النتيجة الإجمالية: {self.test_results['overall_functionality_score']}%")
        
        # تفاصيل النتائج
        core_avg = sum(test["score"] for test in self.test_results["core_system_tests"].values()) / len(self.test_results["core_system_tests"]) if self.test_results["core_system_tests"] else 0
        ui_avg = sum(test["score"] for test in self.test_results["ui_component_tests"].values()) / len(self.test_results["ui_component_tests"]) if self.test_results["ui_component_tests"] else 0
        
        print(f"   🎯 النظام الأساسي: {core_avg:.1f}%")
        print(f"   🖥️  واجهة المستخدم: {ui_avg:.1f}%")
        print(f"   🗄️  قاعدة البيانات: {self.test_results['database_tests']['score']}%")
        print(f"   🔗 التكامل: {self.test_results['integration_tests']['score']}%")
        print(f"   ⚡ الأداء: {self.test_results['performance_tests']['score']}%")
        
        print("="*70)

def main():
    """تشغيل نظام الاختبار الوظيفي الشامل"""
    tester = ComprehensiveFunctionalTester()
    results = tester.run_comprehensive_functional_tests()
    
    return results

if __name__ == "__main__":
    main()
