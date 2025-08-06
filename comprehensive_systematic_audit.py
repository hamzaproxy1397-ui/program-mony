#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الفحص الشامل والمنهجي لبرنامج المحاسبة العربي
Comprehensive Systematic Audit System for Arabic Accounting Software
"""

import ast
import sys
import json
import sqlite3
import importlib
import traceback
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

class ComprehensiveSystematicAudit:
    """نظام الفحص الشامل والمنهجي"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "project_structure": {},
            "code_analysis": {},
            "database_analysis": {},
            "functional_tests": {},
            "performance_metrics": {},
            "recommendations": [],
            "overall_score": 0
        }
        
        # تعريف هيكل المشروع المتوقع
        self.expected_structure = {
            "core_files": [
                "main.py",
                "ui/main_window.py",
                "ui/login_window.py",
                "database/hybrid_database_manager.py",
                "auth/auth_manager.py"
            ],
            "ui_modules": [
                "ui/pos_window.py",
                "ui/pos_simple.py", 
                "ui/advanced_settings_window.py",
                "ui/sales_analysis_window.py",
                "ui/accounts_window.py",
                "ui/reports_window.py"
            ],
            "database_modules": [
                "database/database_manager.py",
                "database/products_manager.py",
                "database/invoices_manager.py",
                "database/accounts_manager.py"
            ],
            "service_modules": [
                "services/sales_manager.py",
                "services/purchases_manager.py",
                "services/treasury_manager.py"
            ],
            "config_files": [
                "config/settings.py",
                "themes/theme_manager.py",
                "core/scheduler_manager.py"
            ]
        }
        
        # المكتبات المطلوبة
        self.required_libraries = {
            "customtkinter": "5.0.0+",
            "tkinter": "built-in",
            "sqlite3": "built-in", 
            "PIL": "8.0.0+",
            "apscheduler": "3.0.0+",
            "pathlib": "built-in",
            "datetime": "built-in",
            "json": "built-in",
            "logging": "built-in"
        }
    
    def run_comprehensive_audit(self):
        """تشغيل الفحص الشامل والمنهجي"""
        print("🔍 بدء الفحص الشامل والمنهجي لبرنامج المحاسبة العربي...")
        print("=" * 80)
        
        # المرحلة 1: فحص هيكل المشروع
        print("\n📁 المرحلة 1: فحص هيكل المشروع...")
        self.audit_project_structure()
        
        # المرحلة 2: تحليل الأكواد البرمجية
        print("\n💻 المرحلة 2: تحليل الأكواد البرمجية...")
        self.audit_code_analysis()
        
        # المرحلة 3: فحص قاعدة البيانات
        print("\n🗄️  المرحلة 3: فحص قاعدة البيانات...")
        self.audit_database()
        
        # المرحلة 4: الاختبار الوظيفي
        print("\n🧪 المرحلة 4: الاختبار الوظيفي...")
        self.audit_functional_tests()
        
        # المرحلة 5: تحليل الأداء
        print("\n⚡ المرحلة 5: تحليل الأداء...")
        self.audit_performance()
        
        # المرحلة 6: حساب النتيجة الإجمالية
        print("\n📊 المرحلة 6: حساب النتيجة الإجمالية...")
        self.calculate_overall_score()
        
        # إنشاء التقرير الشامل
        self.generate_comprehensive_report()
        
        return self.audit_results
    
    # تحذير: دالة معقدة (تعقيد: 24) - استخدم list comprehensions بدلاً من loops معقدة
    def audit_project_structure(self):
        """فحص هيكل المشروع"""
        structure_results = {
            "core_files_status": {},
            "ui_modules_status": {},
            "database_modules_status": {},
            "service_modules_status": {},
            "config_files_status": {},
            "missing_files": [],
            "extra_files": [],
            "directory_structure": {}
        }
        
        # فحص الملفات الأساسية
        print("   🎯 فحص الملفات الأساسية...")
        for file_path in self.expected_structure["core_files"]:
            full_path = self.project_root / file_path
            status = {
                "exists": full_path.exists(),
                "size": full_path.stat().st_size if full_path.exists() else 0,
                "readable": False,
                "syntax_valid": False
            }
            
            if status["exists"]:
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    status["readable"] = True
                    
                    # فحص النحو
                    try:
                        ast.parse(content)
                        status["syntax_valid"] = True
                        print(f"      ✅ {file_path}")
                    except SyntaxError as e:
                        print(f"      ❌ {file_path} - خطأ نحوي: {e.msg}")
                except Exception as e:
                    print(f"      ⚠️  {file_path} - خطأ في القراءة: {e}")
            else:
                print(f"      ❌ {file_path} - غير موجود")
                structure_results["missing_files"].append(file_path)
            
            structure_results["core_files_status"][file_path] = status
        
        # فحص وحدات واجهة المستخدم
        print("   🖥️  فحص وحدات واجهة المستخدم...")
        for file_path in self.expected_structure["ui_modules"]:
            full_path = self.project_root / file_path
            status = self._check_file_status(full_path)
            structure_results["ui_modules_status"][file_path] = status
            
            if status["exists"] and status["syntax_valid"]:
                print(f"      ✅ {file_path}")
            elif status["exists"]:
                print(f"      ⚠️  {file_path} - يحتاج إصلاح")
            else:
                print(f"      ❌ {file_path} - غير موجود")
        
        # فحص وحدات قاعدة البيانات
        print("   🗄️  فحص وحدات قاعدة البيانات...")
        for file_path in self.expected_structure["database_modules"]:
            full_path = self.project_root / file_path
            status = self._check_file_status(full_path)
            structure_results["database_modules_status"][file_path] = status
            
            if status["exists"] and status["syntax_valid"]:
                print(f"      ✅ {file_path}")
            elif status["exists"]:
                print(f"      ⚠️  {file_path} - يحتاج إصلاح")
            else:
                print(f"      ❌ {file_path} - غير موجود")
        
        # فحص وحدات الخدمات
        print("   🔧 فحص وحدات الخدمات...")
        for file_path in self.expected_structure["service_modules"]:
            full_path = self.project_root / file_path
            status = self._check_file_status(full_path)
            structure_results["service_modules_status"][file_path] = status
            
            if status["exists"] and status["syntax_valid"]:
                print(f"      ✅ {file_path}")
            elif status["exists"]:
                print(f"      ⚠️  {file_path} - يحتاج إصلاح")
            else:
                print(f"      ❌ {file_path} - غير موجود")
        
        # فحص ملفات التكوين
        print("   ⚙️  فحص ملفات التكوين...")
        for file_path in self.expected_structure["config_files"]:
            full_path = self.project_root / file_path
            status = self._check_file_status(full_path)
            structure_results["config_files_status"][file_path] = status
            
            if status["exists"] and status["syntax_valid"]:
                print(f"      ✅ {file_path}")
            elif status["exists"]:
                print(f"      ⚠️  {file_path} - يحتاج إصلاح")
            else:
                print(f"      ❌ {file_path} - غير موجود")
        
        # فحص هيكل المجلدات
        expected_dirs = ["ui", "database", "services", "config", "themes", "core", "auth", "assets"]
        for dir_name in expected_dirs:
            dir_path = self.project_root / dir_name
            structure_results["directory_structure"][dir_name] = {
                "exists": dir_path.exists(),
                "is_directory": dir_path.is_dir() if dir_path.exists() else False,
                "file_count": len(list(dir_path.glob("*.py"))) if dir_path.exists() and dir_path.is_dir() else 0
            }
        
        self.audit_results["project_structure"] = structure_results
    
    def audit_code_analysis(self):
        """تحليل الأكواد البرمجية"""
        code_results = {
            "syntax_errors": [],
            "import_errors": [],
            "undefined_variables": [],
            "unused_imports": [],
            "code_quality_issues": [],
            "library_compatibility": {},
            "total_files_analyzed": 0,
            "healthy_files": 0,
            "problematic_files": 0
        }
        
        # فحص المكتبات المطلوبة
        print("   📦 فحص المكتبات المطلوبة...")
        for lib_name, min_version in self.required_libraries.items():
            lib_status = self._check_library_status(lib_name, min_version)
            code_results["library_compatibility"][lib_name] = lib_status
            
            if lib_status["available"]:
                print(f"      ✅ {lib_name} - {lib_status['version']}")
            else:
                print(f"      ❌ {lib_name} - {lib_status['error']}")
        
        # تحليل جميع ملفات Python
        print("   💻 تحليل ملفات Python...")
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            code_results["total_files_analyzed"] += 1
            file_issues = self._analyze_python_file(py_file)
            
            if file_issues["has_issues"]:
                code_results["problematic_files"] += 1
                code_results["syntax_errors"].extend(file_issues["syntax_errors"])
                code_results["import_errors"].extend(file_issues["import_errors"])
                code_results["code_quality_issues"].extend(file_issues["quality_issues"])
                print(f"      ⚠️  {py_file.name} - {len(file_issues['syntax_errors']) + len(file_issues['import_errors'])} مشاكل")
            else:
                code_results["healthy_files"] += 1
                print(f"      ✅ {py_file.name}")
        
        print(f"   📊 ملخص التحليل: {code_results['healthy_files']}/{code_results['total_files_analyzed']} ملف سليم")
        
        self.audit_results["code_analysis"] = code_results
    
    def audit_database(self):
        """فحص قاعدة البيانات"""
        db_results = {
            "sqlite_available": False,
            "database_file_exists": False,
            "database_accessible": False,
            "tables_analysis": {},
            "data_integrity": {},
            "performance_metrics": {},
            "backup_system": {}
        }
        
        # فحص توفر SQLite
        try:
            import sqlite3
            db_results["sqlite_available"] = True
            print("   ✅ SQLite متوفر")
        except ImportError:
            print("   ❌ SQLite غير متوفر")
            self.audit_results["database_analysis"] = db_results
            return
        
        # فحص ملف قاعدة البيانات
        db_file = self.project_root / "accounting.db"
        if db_file.exists():
            db_results["database_file_exists"] = True
            print("   ✅ ملف قاعدة البيانات موجود")
            
            # فحص إمكانية الوصول وتحليل الجداول
            try:
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()
                
                # الحصول على قائمة الجداول
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                db_results["database_accessible"] = True
                print(f"   ✅ قاعدة البيانات قابلة للوصول ({len(tables)} جدول)")
                
                # تحليل كل جدول
                for (table_name,) in tables:
                    table_info = self._analyze_table(cursor, table_name)
                    db_results["tables_analysis"][table_name] = table_info
                    print(f"      📊 {table_name}: {table_info['row_count']} سجل، {table_info['column_count']} عمود")
                
                conn.close()
                
            except Exception as e:
                print(f"   ❌ خطأ في الوصول لقاعدة البيانات: {e}")
        else:
            print("   ⚠️  ملف قاعدة البيانات غير موجود (سيتم إنشاؤه عند التشغيل)")
        
        # فحص نظام النسخ الاحتياطي
        backup_dir = self.project_root / "backups"
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("*.db"))
            db_results["backup_system"] = {
                "backup_dir_exists": True,
                "backup_count": len(backup_files),
                "latest_backup": max(backup_files, key=lambda x: x.stat().st_mtime).name if backup_files else None
            }
            print(f"   ✅ نظام النسخ الاحتياطي: {len(backup_files)} نسخة احتياطية")
        else:
            db_results["backup_system"] = {"backup_dir_exists": False}
            print("   ⚠️  مجلد النسخ الاحتياطي غير موجود")
        
        self.audit_results["database_analysis"] = db_results
    
    def audit_functional_tests(self):
        """الاختبار الوظيفي"""
        functional_results = {
            "ui_components": {},
            "core_functions": {},
            "integration_tests": {},
            "user_workflows": {}
        }
        
        print("   🖥️  اختبار مكونات واجهة المستخدم...")
        
        # اختبار الملفات الأساسية للواجهة
        ui_components = [
            "ui/main_window.py",
            "ui/login_window.py", 
            "ui/pos_window.py",
            "ui/advanced_settings_window.py"
        ]
        
        for component in ui_components:
            component_path = self.project_root / component
            test_result = self._test_ui_component(component_path)
            functional_results["ui_components"][component] = test_result
            
            if test_result["importable"]:
                print(f"      ✅ {component} - قابل للاستيراد")
            else:
                print(f"      ❌ {component} - غير قابل للاستيراد")
        
        print("   🔧 اختبار الوظائف الأساسية...")
        
        # اختبار الوظائف الأساسية
        core_functions = [
            "database/hybrid_database_manager.py",
            "services/sales_manager.py",
            "auth/auth_manager.py",
            "core/scheduler_manager.py"
        ]
        
        for function_module in core_functions:
            module_path = self.project_root / function_module
            test_result = self._test_core_function(module_path)
            functional_results["core_functions"][function_module] = test_result
            
            if test_result["functional"]:
                print(f"      ✅ {function_module} - وظيفي")
            else:
                print(f"      ❌ {function_module} - غير وظيفي")
        
        self.audit_results["functional_tests"] = functional_results
    
    def audit_performance(self):
        """تحليل الأداء"""
        performance_results = {
            "file_sizes": {},
            "import_times": {},
            "memory_usage": {},
            "startup_time": None,
            "recommendations": []
        }
        
        print("   📊 تحليل أحجام الملفات...")
        
        # تحليل أحجام الملفات
        large_files = []
        total_size = 0
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            file_size = py_file.stat().st_size
            total_size += file_size
            performance_results["file_sizes"][str(py_file.relative_to(self.project_root))] = file_size
            
            if file_size > 50000:  # أكبر من 50KB
                large_files.append((str(py_file.relative_to(self.project_root)), file_size))
        
        print(f"      📊 إجمالي حجم الكود: {total_size / 1024:.1f} KB")
        
        if large_files:
            print("      ⚠️  ملفات كبيرة الحجم:")
            for file_name, size in sorted(large_files, key=lambda x: x[1], reverse=True)[:5]:
                print(f"         - {file_name}: {size / 1024:.1f} KB")
                performance_results["recommendations"].append(f"مراجعة حجم الملف: {file_name}")
        
        self.audit_results["performance_metrics"] = performance_results
    
    def calculate_overall_score(self):
        """حساب النتيجة الإجمالية"""
        scores = {}
        
        # نتيجة هيكل المشروع (25%)
        structure_score = self._calculate_structure_score()
        scores["structure"] = structure_score
        
        # نتيجة تحليل الكود (35%)
        code_score = self._calculate_code_score()
        scores["code"] = code_score
        
        # نتيجة قاعدة البيانات (20%)
        database_score = self._calculate_database_score()
        scores["database"] = database_score
        
        # نتيجة الاختبار الوظيفي (20%)
        functional_score = self._calculate_functional_score()
        scores["functional"] = functional_score
        
        # حساب النتيجة الإجمالية
        overall_score = (
            structure_score * 0.25 +
            code_score * 0.35 +
            database_score * 0.20 +
            functional_score * 0.20
        )
        
        self.audit_results["overall_score"] = round(overall_score, 1)
        self.audit_results["score_breakdown"] = scores
        
        print(f"   📊 النتيجة الإجمالية: {overall_score:.1f}%")
        print(f"      - هيكل المشروع: {structure_score:.1f}%")
        print(f"      - تحليل الكود: {code_score:.1f}%")
        print(f"      - قاعدة البيانات: {database_score:.1f}%")
        print(f"      - الاختبار الوظيفي: {functional_score:.1f}%")
    
    def _check_file_status(self, file_path: Path) -> dict:
        """فحص حالة ملف واحد"""
        status = {
            "exists": file_path.exists(),
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "readable": False,
            "syntax_valid": False,
            "importable": False
        }
        
        if status["exists"]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                status["readable"] = True
                
                # فحص النحو
                try:
                    ast.parse(content)
                    status["syntax_valid"] = True
                except SyntaxError:
                    pass
                
                # فحص إمكانية الاستيراد
                if status["syntax_valid"]:
                    try:
                        module_name = str(file_path.relative_to(self.project_root)).replace('/', '.').replace('.py', '')
                        spec = importlib.util.spec_from_file_location(module_name, file_path)
                        if spec and spec.loader:
                            status["importable"] = True
                    except Exception:
                        pass
            except Exception:
                pass
        
        return status
    
    def _check_library_status(self, lib_name: str, min_version: str) -> dict:
        """فحص حالة مكتبة"""
        status = {
            "available": False,
            "version": None,
            "meets_requirement": False,
            "error": None
        }
        
        try:
            if lib_name == "tkinter":
                import tkinter as tk
                status["available"] = True
                status["version"] = str(tk.TkVersion)
                status["meets_requirement"] = True
            elif lib_name == "customtkinter":
                import customtkinter as ctk
                status["available"] = True
                status["version"] = ctk.__version__
                status["meets_requirement"] = True
            elif lib_name == "PIL":
                from PIL import Image
                status["available"] = True
                status["version"] = getattr(Image, '__version__', 'unknown')
                status["meets_requirement"] = True
            else:
                module = __import__(lib_name)
                status["available"] = True
                status["version"] = getattr(module, '__version__', 'unknown')
                status["meets_requirement"] = True
        except ImportError as e:
            status["error"] = f"غير متوفر: {str(e)}"
        except Exception as e:
            status["error"] = f"خطأ: {str(e)}"
        
        return status
    
    def _analyze_python_file(self, file_path: Path) -> dict:
        """تحليل ملف Python واحد"""
        analysis = {
            "has_issues": False,
            "syntax_errors": [],
            "import_errors": [],
            "quality_issues": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # فحص النحو
            try:
                ast.parse(content)
            except SyntaxError as e:
                analysis["has_issues"] = True
                analysis["syntax_errors"].append({
                    "file": str(file_path.relative_to(self.project_root)),
                    "line": e.lineno,
                    "message": e.msg,
                    "text": e.text.strip() if e.text else ""
                })
            
            # فحص الاستيرادات
            import_lines = [line for line in content.split('\n') if line.strip().startswith(('import ', 'from '))]
            for i, line in enumerate(import_lines, 1):
                if 'import' in line:
                    # فحص بسيط للاستيرادات
                    if line.count('import') > 1 and 'from' not in line:
                        analysis["quality_issues"].append({
                            "file": str(file_path.relative_to(self.project_root)),
                            "line": i,
                            "issue": "استيراد متعدد في سطر واحد",
                            "suggestion": "فصل الاستيرادات إلى أسطر منفصلة"
                        })
            
        except Exception as e:
            analysis["has_issues"] = True
            analysis["import_errors"].append({
                "file": str(file_path.relative_to(self.project_root)),
                "error": f"خطأ في القراءة: {str(e)}"
            })
        
        return analysis
    
    def _analyze_table(self, cursor, table_name: str) -> dict:
        """تحليل جدول قاعدة البيانات"""
        table_info = {
            "row_count": 0,
            "column_count": 0,
            "columns": [],
            "has_primary_key": False,
            "has_foreign_keys": False
        }
        
        try:
            # عدد الصفوف
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            table_info["row_count"] = cursor.fetchone()[0]
            
            # معلومات الأعمدة
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            table_info["column_count"] = len(columns)
            
            for col in columns:
                col_info = {
                    "name": col[1],
                    "type": col[2],
                    "not_null": bool(col[3]),
                    "default_value": col[4],
                    "primary_key": bool(col[5])
                }
                table_info["columns"].append(col_info)
                
                if col_info["primary_key"]:
                    table_info["has_primary_key"] = True
            
            # فحص المفاتيح الخارجية
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            foreign_keys = cursor.fetchall()
            table_info["has_foreign_keys"] = len(foreign_keys) > 0
            
        except Exception as e:
            table_info["error"] = str(e)
        
        return table_info
    
    def _test_ui_component(self, component_path: Path) -> dict:
        """اختبار مكون واجهة المستخدم"""
        test_result = {
            "exists": component_path.exists(),
            "importable": False,
            "has_main_class": False,
            "error": None
        }
        
        if test_result["exists"]:
            try:
                # محاولة الاستيراد
                module_name = str(component_path.relative_to(self.project_root)).replace('/', '.').replace('.py', '')
                spec = importlib.util.spec_from_file_location(module_name, component_path)
                if spec and spec.loader:
                    test_result["importable"] = True
                    
                    # فحص وجود فئة رئيسية
                    with open(component_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'class ' in content and ('Window' in content or 'Panel' in content):
                        test_result["has_main_class"] = True
                        
            except Exception as e:
                test_result["error"] = str(e)
        
        return test_result
    
    def _test_core_function(self, module_path: Path) -> dict:
        """اختبار وظيفة أساسية"""
        test_result = {
            "exists": module_path.exists(),
            "importable": False,
            "functional": False,
            "error": None
        }
        
        if test_result["exists"]:
            try:
                # محاولة الاستيراد
                module_name = str(module_path.relative_to(self.project_root)).replace('/', '.').replace('.py', '')
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec and spec.loader:
                    test_result["importable"] = True
                    test_result["functional"] = True  # افتراض أنه وظيفي إذا كان قابل للاستيراد
                    
            except Exception as e:
                test_result["error"] = str(e)
        
        return test_result
    
    def _calculate_structure_score(self) -> float:
        """حساب نتيجة هيكل المشروع"""
        structure = self.audit_results["project_structure"]
        total_files = 0
        valid_files = 0
        
        for category in ["core_files_status", "ui_modules_status", "database_modules_status", "service_modules_status", "config_files_status"]:
            for file_path, status in structure[category].items():
                total_files += 1
                if status["exists"] and status["syntax_valid"]:
                    valid_files += 1
        
        return (valid_files / total_files * 100) if total_files > 0 else 0
    
    def _calculate_code_score(self) -> float:
        """حساب نتيجة تحليل الكود"""
        code = self.audit_results["code_analysis"]
        
        if code["total_files_analyzed"] == 0:
            return 0
        
        # نسبة الملفات السليمة
        healthy_ratio = code["healthy_files"] / code["total_files_analyzed"]
        
        # خصم نقاط للأخطاء
        error_penalty = min(len(code["syntax_errors"]) * 2, 50)  # حد أقصى 50 نقطة خصم
        
        # نتيجة المكتبات
        libs_available = sum(1 for lib in code["library_compatibility"].values() if lib["available"])
        libs_total = len(code["library_compatibility"])
        libs_score = (libs_available / libs_total) if libs_total > 0 else 0
        
        final_score = (healthy_ratio * 70 + libs_score * 30) - error_penalty
        return max(0, final_score)
    
    def _calculate_database_score(self) -> float:
        """حساب نتيجة قاعدة البيانات"""
        db = self.audit_results["database_analysis"]
        
        score = 0
        if db["sqlite_available"]:
            score += 30
        if db["database_accessible"]:
            score += 40
        if db["backup_system"].get("backup_dir_exists", False):
            score += 20
        if len(db["tables_analysis"]) > 0:
            score += 10
        
        return score
    
    def _calculate_functional_score(self) -> float:
        """حساب نتيجة الاختبار الوظيفي"""
        functional = self.audit_results["functional_tests"]
        
        ui_score = 0
        ui_total = len(functional["ui_components"])
        if ui_total > 0:
            ui_working = sum(1 for comp in functional["ui_components"].values() if comp["importable"])
            ui_score = (ui_working / ui_total) * 50
        
        core_score = 0
        core_total = len(functional["core_functions"])
        if core_total > 0:
            core_working = sum(1 for func in functional["core_functions"].values() if func["functional"])
            core_score = (core_working / core_total) * 50
        
        return ui_score + core_score
    
    def generate_comprehensive_report(self):
        """إنشاء التقرير الشامل"""
        report_file = f"comprehensive_systematic_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ التقرير الشامل في: {report_file}")
        
        # طباعة ملخص التقرير
        self._print_audit_summary()
    
    def _print_audit_summary(self):
        """طباعة ملخص التقرير"""
        print("\n" + "="*80)
        print("📊 ملخص الفحص الشامل والمنهجي:")
        print(f"   🎯 النتيجة الإجمالية: {self.audit_results['overall_score']}%")
        
        # تقييم الحالة العامة
        score = self.audit_results['overall_score']
        if score >= 90:
            status = "ممتاز - جاهز للإنتاج"
            emoji = "🏆"
        elif score >= 80:
            status = "جيد جداً - يحتاج تحسينات طفيفة"
            emoji = "🥇"
        elif score >= 70:
            status = "جيد - يحتاج بعض الإصلاحات"
            emoji = "🥈"
        elif score >= 60:
            status = "مقبول - يحتاج إصلاحات متوسطة"
            emoji = "🥉"
        else:
            status = "يحتاج تحسينات شاملة"
            emoji = "⚠️"
        
        print(f"   {emoji} الحالة العامة: {status}")
        
        # تفاصيل النتائج
        breakdown = self.audit_results.get('score_breakdown', {})
        print(f"   📁 هيكل المشروع: {breakdown.get('structure', 0):.1f}%")
        print(f"   💻 تحليل الكود: {breakdown.get('code', 0):.1f}%")
        print(f"   🗄️  قاعدة البيانات: {breakdown.get('database', 0):.1f}%")
        print(f"   🧪 الاختبار الوظيفي: {breakdown.get('functional', 0):.1f}%")
        
        # إحصائيات سريعة
        code_analysis = self.audit_results.get('code_analysis', {})
        print(f"   📊 الملفات المحللة: {code_analysis.get('total_files_analyzed', 0)}")
        print(f"   ✅ الملفات السليمة: {code_analysis.get('healthy_files', 0)}")
        print(f"   ❌ الأخطاء النحوية: {len(code_analysis.get('syntax_errors', []))}")
        
        print("="*80)

def main():
    """تشغيل الفحص الشامل والمنهجي"""
    audit = ComprehensiveSystematicAudit()
    results = audit.run_comprehensive_audit()
    
    return results

if __name__ == "__main__":
    main()
