#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
الفحص التشخيصي الشامل والعميق لبرنامج المحاسبة العربي
Ultimate Comprehensive Diagnostic for Arabic Accounting System
"""

import ast
import sys
import json
import traceback
from pathlib import Path
from datetime import datetime
import importlib.util
import sqlite3
import logging

class UltimateComprehensiveDiagnostic:
    """الفحص التشخيصي الشامل والعميق"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "critical_files": {},
            "syntax_errors": [],
            "import_errors": [],
            "database_status": {},
            "library_status": {},
            "overall_health": "unknown"
        }
        
        # الملفات الحرجة للنظام
        self.critical_files = [
            "main.py",
            "ui/main_window.py",
            "ui/login_window.py", 
            "ui/pos_window.py",
            "ui/pos_simple.py",
            "ui/advanced_settings_window.py",
            "database/hybrid_database_manager.py",
            "database/database_manager.py",
            "core/scheduler_manager.py",
            "auth/auth_manager.py",
            "themes/theme_manager.py",
            "services/sales_manager.py"
        ]
        
        # المكتبات المطلوبة
        self.required_libraries = [
            "customtkinter",
            "tkinter", 
            "sqlite3",
            "pathlib",
            "datetime",
            "json",
            "logging",
            "PIL",
            "apscheduler"
        ]
    
    def run_ultimate_diagnostic(self):
        """تشغيل الفحص التشخيصي الشامل"""
        print("🔍 بدء الفحص التشخيصي الشامل والعميق...")
        print("=" * 80)
        
        # المرحلة 1: فحص الملفات الحرجة
        print("\n🎯 المرحلة 1: فحص الملفات الحرجة للنظام...")
        self.diagnose_critical_files()
        
        # المرحلة 2: فحص المكتبات المطلوبة
        print("\n📦 المرحلة 2: فحص المكتبات والوحدات...")
        self.diagnose_libraries()
        
        # المرحلة 3: فحص قاعدة البيانات
        print("\n🗄️  المرحلة 3: فحص سلامة قاعدة البيانات...")
        self.diagnose_database()
        
        # المرحلة 4: فحص شامل للأخطاء النحوية
        print("\n🔧 المرحلة 4: فحص شامل للأخطاء النحوية...")
        self.diagnose_all_syntax_errors()
        
        # المرحلة 5: تحليل الحالة العامة
        print("\n📊 المرحلة 5: تحليل الحالة العامة للنظام...")
        self.analyze_overall_health()
        
        # إنشاء التقرير التشخيصي
        self.generate_diagnostic_report()
        
        return self.results
    
    def diagnose_critical_files(self):
        """فحص الملفات الحرجة للنظام"""
        for file_path in self.critical_files:
            full_path = self.project_root / file_path
            
            file_status = {
                "exists": False,
                "syntax_valid": False,
                "importable": False,
                "size": 0,
                "errors": []
            }
            
            if full_path.exists():
                file_status["exists"] = True
                file_status["size"] = full_path.stat().st_size
                
                # فحص النحو
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                    file_status["syntax_valid"] = True
                    print(f"   ✅ {file_path} - نحو سليم")
                except SyntaxError as e:
                    file_status["errors"].append(f"خطأ نحوي: {e.msg} (السطر {e.lineno})")
                    print(f"   ❌ {file_path} - خطأ نحوي: {e.msg} (السطر {e.lineno})")
                except Exception as e:
                    file_status["errors"].append(f"خطأ في القراءة: {str(e)}")
                    print(f"   ❌ {file_path} - خطأ في القراءة: {str(e)}")
                
                # فحص إمكانية الاستيراد (للملفات Python)
                if file_path.endswith('.py') and file_status["syntax_valid"]:
                    try:
                        module_name = file_path.replace('/', '.').replace('.py', '')
                        spec = importlib.util.spec_from_file_location(module_name, full_path)
                        if spec and spec.loader:
                            file_status["importable"] = True
                            print(f"   ✅ {file_path} - قابل للاستيراد")
                    except Exception as e:
                        file_status["errors"].append(f"خطأ في الاستيراد: {str(e)}")
                        print(f"   ⚠️  {file_path} - مشكلة في الاستيراد: {str(e)}")
            else:
                file_status["errors"].append("الملف غير موجود")
                print(f"   ❌ {file_path} - الملف غير موجود")
            
            self.results["critical_files"][file_path] = file_status
    
    def diagnose_libraries(self):
        """فحص المكتبات والوحدات المطلوبة"""
        for library in self.required_libraries:
            lib_status = {
                "available": False,
                "version": None,
                "error": None
            }
            
            try:
                if library == "tkinter":
                    import tkinter as tk
                    lib_status["available"] = True
                    lib_status["version"] = tk.TkVersion
                elif library == "customtkinter":
                    import customtkinter as ctk
                    lib_status["available"] = True
                    lib_status["version"] = ctk.__version__
                elif library == "PIL":
                    from PIL import Image
                    lib_status["available"] = True
                    lib_status["version"] = Image.__version__ if hasattr(Image, '__version__') else "unknown"
                elif library == "apscheduler":
                    import apscheduler
                    lib_status["available"] = True
                    lib_status["version"] = apscheduler.__version__
                else:
                    module = __import__(library)
                    lib_status["available"] = True
                    lib_status["version"] = getattr(module, '__version__', 'unknown')
                
                print(f"   ✅ {library} - متوفر (الإصدار: {lib_status['version']})")
                
            except ImportError as e:
                lib_status["error"] = f"غير متوفر: {str(e)}"
                print(f"   ❌ {library} - غير متوفر: {str(e)}")
            except Exception as e:
                lib_status["error"] = f"خطأ: {str(e)}"
                print(f"   ⚠️  {library} - خطأ: {str(e)}")
            
            self.results["library_status"][library] = lib_status
    
    def diagnose_database(self):
        """فحص سلامة قاعدة البيانات"""
        db_status = {
            "sqlite_available": False,
            "database_file_exists": False,
            "database_accessible": False,
            "tables_count": 0,
            "errors": []
        }
        
        # فحص توفر SQLite
        try:
            import sqlite3
            db_status["sqlite_available"] = True
            print("   ✅ SQLite متوفر")
        except ImportError:
            db_status["errors"].append("SQLite غير متوفر")
            print("   ❌ SQLite غير متوفر")
        
        # فحص ملف قاعدة البيانات
        db_file = self.project_root / "accounting.db"
        if db_file.exists():
            db_status["database_file_exists"] = True
            print("   ✅ ملف قاعدة البيانات موجود")
            
            # فحص إمكانية الوصول
            try:
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                db_status["tables_count"] = len(tables)
                db_status["database_accessible"] = True
                conn.close()
                print(f"   ✅ قاعدة البيانات قابلة للوصول ({len(tables)} جدول)")
            except Exception as e:
                db_status["errors"].append(f"خطأ في الوصول: {str(e)}")
                print(f"   ❌ خطأ في الوصول لقاعدة البيانات: {str(e)}")
        else:
            print("   ⚠️  ملف قاعدة البيانات غير موجود (سيتم إنشاؤه عند التشغيل)")
        
        self.results["database_status"] = db_status
    
    def diagnose_all_syntax_errors(self):
        """فحص شامل للأخطاء النحوية في جميع الملفات"""
        syntax_errors = []
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError as e:
                error_info = {
                    "file": str(py_file.relative_to(self.project_root)),
                    "line": e.lineno,
                    "message": e.msg,
                    "text": e.text.strip() if e.text else ""
                }
                syntax_errors.append(error_info)
                print(f"   ❌ {error_info['file']} - السطر {error_info['line']}: {error_info['message']}")
            except Exception as e:
                error_info = {
                    "file": str(py_file.relative_to(self.project_root)),
                    "line": "unknown",
                    "message": f"خطأ في القراءة: {str(e)}",
                    "text": ""
                }
                syntax_errors.append(error_info)
        
        self.results["syntax_errors"] = syntax_errors
        print(f"   📊 إجمالي الأخطاء النحوية: {len(syntax_errors)}")
    
    def analyze_overall_health(self):
        """تحليل الحالة العامة للنظام"""
        # تحليل الملفات الحرجة
        critical_healthy = sum(1 for f in self.results["critical_files"].values() 
                              if f["exists"] and f["syntax_valid"])
        critical_total = len(self.critical_files)
        
        # تحليل المكتبات
        libs_available = sum(1 for lib in self.results["library_status"].values() 
                            if lib["available"])
        libs_total = len(self.required_libraries)
        
        # تحليل قاعدة البيانات
        db_healthy = (self.results["database_status"]["sqlite_available"] and 
                     self.results["database_status"]["database_accessible"])
        
        # تحليل الأخطاء النحوية
        syntax_errors_count = len(self.results["syntax_errors"])
        
        # حساب النتيجة الإجمالية
        critical_score = (critical_healthy / critical_total) * 100
        libs_score = (libs_available / libs_total) * 100
        db_score = 100 if db_healthy else 50  # 50 إذا كان SQLite متوفر لكن قاعدة البيانات غير موجودة
        syntax_score = max(0, 100 - (syntax_errors_count * 2))  # خصم نقطتين لكل خطأ نحوي
        
        overall_score = (critical_score * 0.4 + libs_score * 0.3 + db_score * 0.2 + syntax_score * 0.1)
        
        if overall_score >= 90:
            health_status = "excellent"
            health_desc = "ممتاز - النظام جاهز للإنتاج"
        elif overall_score >= 75:
            health_status = "good"
            health_desc = "جيد - يحتاج تحسينات طفيفة"
        elif overall_score >= 50:
            health_status = "fair"
            health_desc = "مقبول - يحتاج إصلاحات"
        else:
            health_status = "poor"
            health_desc = "ضعيف - يحتاج إصلاحات شاملة"
        
        self.results["overall_health"] = {
            "status": health_status,
            "score": round(overall_score, 1),
            "description": health_desc,
            "breakdown": {
                "critical_files": f"{critical_healthy}/{critical_total} ({critical_score:.1f}%)",
                "libraries": f"{libs_available}/{libs_total} ({libs_score:.1f}%)",
                "database": f"{'صحي' if db_healthy else 'يحتاج إعداد'} ({db_score}%)",
                "syntax_errors": f"{syntax_errors_count} خطأ ({syntax_score:.1f}%)"
            }
        }
        
        print(f"   📊 النتيجة الإجمالية: {overall_score:.1f}% - {health_desc}")
        print(f"   🎯 الملفات الحرجة: {critical_healthy}/{critical_total}")
        print(f"   📦 المكتبات: {libs_available}/{libs_total}")
        print(f"   🗄️  قاعدة البيانات: {'✅' if db_healthy else '⚠️'}")
        print(f"   🔧 الأخطاء النحوية: {syntax_errors_count}")
    
    def generate_diagnostic_report(self):
        """إنشاء التقرير التشخيصي الشامل"""
        report_file = f"ultimate_diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ التقرير التشخيصي الشامل في: {report_file}")
        
        # طباعة ملخص التقرير
        print("\n" + "="*80)
        print("📊 ملخص التقرير التشخيصي الشامل:")
        print(f"   🎯 الحالة العامة: {self.results['overall_health']['description']}")
        print(f"   📊 النتيجة: {self.results['overall_health']['score']}%")
        print(f"   🎯 الملفات الحرجة: {self.results['overall_health']['breakdown']['critical_files']}")
        print(f"   📦 المكتبات: {self.results['overall_health']['breakdown']['libraries']}")
        print(f"   🗄️  قاعدة البيانات: {self.results['overall_health']['breakdown']['database']}")
        print(f"   🔧 الأخطاء النحوية: {self.results['overall_health']['breakdown']['syntax_errors']}")
        print("="*80)

def main():
    """تشغيل الفحص التشخيصي الشامل"""
    diagnostic = UltimateComprehensiveDiagnostic()
    results = diagnostic.run_ultimate_diagnostic()
    
    return results

if __name__ == "__main__":
    main()
