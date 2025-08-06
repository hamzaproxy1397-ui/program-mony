#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شامل وعميق للنظام المحاسبي
Deep Comprehensive System Audit for Accounting Software
"""

import sys
import os
import ast
import sqlite3
import json
import logging
import traceback
import importlib
import inspect
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import subprocess
import re

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class DeepSystemAuditor:
    """مدقق النظام الشامل والعميق"""
    
    def __init__(self):
        self.audit_results = {
            'code_quality': {},
            'security_analysis': {},
            'performance_analysis': {},
            'database_integrity': {},
            'ui_consistency': {},
            'business_logic_validation': {},
            'dependency_analysis': {},
            'architecture_review': {},
            'rtl_compliance': {},
            'error_handling': {}
        }
        self.setup_logging()
        self.critical_issues = []
        self.warnings = []
        self.recommendations = []
    
    def setup_logging(self):
        """إعداد نظام السجلات المتقدم"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/deep_audit_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def analyze_code_quality(self):
        """تحليل جودة الكود"""
        print("🔍 تحليل جودة الكود...")
        
        python_files = list(Path(".").rglob("*.py"))
        python_files = [f for f in python_files if not any(part.startswith('.') for part in f.parts)]
        
        quality_metrics = {
            'total_files': len(python_files),
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'complexity_issues': [],
            'documentation_coverage': 0,
            'syntax_errors': [],
            'import_issues': [],
            'unused_imports': [],
            'code_duplications': []
        }
        
        documented_functions = 0
        total_functions = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # عد الأسطر
                lines = content.split('\n')
                quality_metrics['total_lines'] += len(lines)
                
                # تحليل AST
                try:
                    tree = ast.parse(content)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            total_functions += 1
                            quality_metrics['total_functions'] += 1
                            
                            # فحص التوثيق
                            if ast.get_docstring(node):
                                documented_functions += 1
                            
                            # فحص التعقيد (عدد العقد الشرطية)
                            complexity = self._calculate_complexity(node)
                            if complexity > 10:
                                quality_metrics['complexity_issues'].append({
                                    'file': str(file_path),
                                    'function': node.name,
                                    'complexity': complexity
                                })
                        
                        elif isinstance(node, ast.ClassDef):
                            quality_metrics['total_classes'] += 1
                
                except SyntaxError as e:
                    quality_metrics['syntax_errors'].append({
                        'file': str(file_path),
                        'error': str(e),
                        'line': e.lineno
                    })
                
                # فحص الاستيرادات
                import_analysis = self._analyze_imports(content, file_path)
                quality_metrics['import_issues'].extend(import_analysis['issues'])
                quality_metrics['unused_imports'].extend(import_analysis['unused'])
                
            except Exception as e:
                self.logger.error(f"خطأ في تحليل الملف {file_path}: {e}")
        
        # حساب تغطية التوثيق
        if total_functions > 0:
            quality_metrics['documentation_coverage'] = (documented_functions / total_functions) * 100
        
        self.audit_results['code_quality'] = quality_metrics
        
        # تقييم الجودة
        quality_score = self._calculate_quality_score(quality_metrics)
        print(f"  📊 نقاط الجودة: {quality_score:.1f}/100")
        print(f"  📁 إجمالي الملفات: {quality_metrics['total_files']}")
        print(f"  📝 إجمالي الأسطر: {quality_metrics['total_lines']:,}")
        print(f"  🔧 إجمالي الدوال: {quality_metrics['total_functions']}")
        print(f"  🏗️ إجمالي الفئات: {quality_metrics['total_classes']}")
        print(f"  📚 تغطية التوثيق: {quality_metrics['documentation_coverage']:.1f}%")
        
        if quality_metrics['syntax_errors']:
            print(f"  ❌ أخطاء نحوية: {len(quality_metrics['syntax_errors'])}")
            for error in quality_metrics['syntax_errors'][:3]:  # أول 3 أخطاء
                print(f"    - {error['file']}:{error['line']} - {error['error']}")
        
        if quality_metrics['complexity_issues']:
            print(f"  ⚠️ مشاكل التعقيد: {len(quality_metrics['complexity_issues'])}")
    
    def _calculate_complexity(self, node):
        """حساب تعقيد الدالة (Cyclomatic Complexity)"""
        complexity = 1  # البداية
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _analyze_imports(self, content: str, file_path: Path) -> Dict:
        """تحليل الاستيرادات"""
        issues = []
        unused = []
        
        try:
            tree = ast.parse(content)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            imports.append(f"{node.module}.{alias.name}")
            
            # فحص الاستيرادات غير المستخدمة (تحليل بسيط)
            for imp in imports:
                module_name = imp.split('.')[0]
                if module_name not in content:
                    unused.append({
                        'file': str(file_path),
                        'import': imp
                    })
        
        except Exception as e:
            issues.append({
                'file': str(file_path),
                'error': f"خطأ في تحليل الاستيرادات: {e}"
            })
        
        return {'issues': issues, 'unused': unused}
    
    def _calculate_quality_score(self, metrics: Dict) -> float:
        """حساب نقاط الجودة الإجمالية"""
        score = 100.0
        
        # خصم نقاط للأخطاء النحوية
        score -= len(metrics['syntax_errors']) * 10
        
        # خصم نقاط لمشاكل التعقيد
        score -= len(metrics['complexity_issues']) * 5
        
        # خصم نقاط لضعف التوثيق
        if metrics['documentation_coverage'] < 50:
            score -= (50 - metrics['documentation_coverage']) * 0.5
        
        # خصم نقاط للاستيرادات غير المستخدمة
        score -= len(metrics['unused_imports']) * 1
        
        return max(0, score)
    
    def analyze_security(self):
        """تحليل الأمان"""
        print("🔒 تحليل الأمان...")
        
        security_issues = {
            'sql_injection_risks': [],
            'password_security': [],
            'file_access_risks': [],
            'input_validation': [],
            'authentication_issues': [],
            'authorization_issues': [],
            'data_exposure_risks': []
        }
        
        python_files = list(Path(".").rglob("*.py"))
        python_files = [f for f in python_files if not any(part.startswith('.') for part in f.parts)]
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # فحص مخاطر SQL Injection
                sql_patterns = [
                    r'execute\s*\(\s*["\'].*%.*["\']',
                    r'execute\s*\(\s*f["\'].*{.*}.*["\']',
                    r'query\s*=.*\+.*',
                ]
                
                for pattern in sql_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        security_issues['sql_injection_risks'].append({
                            'file': str(file_path),
                            'line': line_num,
                            'pattern': pattern,
                            'code': match.group()
                        })
                
                # فحص أمان كلمات المرور
                password_patterns = [
                    r'password\s*=\s*["\'][^"\']*["\']',
                    r'pwd\s*=\s*["\'][^"\']*["\']',
                    r'hashlib\.md5\(',
                ]
                
                for pattern in password_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        security_issues['password_security'].append({
                            'file': str(file_path),
                            'line': line_num,
                            'issue': 'استخدام تشفير ضعيف أو كلمة مرور مكشوفة',
                            'code': match.group()
                        })
                
                # فحص مخاطر الوصول للملفات
                file_access_patterns = [
                    r'open\s*\([^)]*["\']\.\./',
                    r'os\.system\s*\(',
                    r'subprocess\.call\s*\(',
                ]
                
                for pattern in file_access_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        security_issues['file_access_risks'].append({
                            'file': str(file_path),
                            'line': line_num,
                            'risk': 'وصول غير آمن للملفات أو تنفيذ أوامر',
                            'code': match.group()
                        })
            
            except Exception as e:
                self.logger.error(f"خطأ في تحليل أمان الملف {file_path}: {e}")
        
        self.audit_results['security_analysis'] = security_issues
        
        # عرض النتائج
        total_issues = sum(len(issues) for issues in security_issues.values())
        print(f"  🚨 إجمالي مشاكل الأمان: {total_issues}")
        
        for category, issues in security_issues.items():
            if issues:
                category_name = {
                    'sql_injection_risks': 'مخاطر SQL Injection',
                    'password_security': 'أمان كلمات المرور',
                    'file_access_risks': 'مخاطر الوصول للملفات',
                    'input_validation': 'التحقق من المدخلات',
                    'authentication_issues': 'مشاكل المصادقة',
                    'authorization_issues': 'مشاكل التخويل',
                    'data_exposure_risks': 'مخاطر كشف البيانات'
                }.get(category, category)
                
                print(f"  ⚠️ {category_name}: {len(issues)}")
                
                # عرض أول 2 مشاكل من كل فئة
                for issue in issues[:2]:
                    print(f"    - {issue['file']}:{issue.get('line', '?')}")
    
    def analyze_database_integrity(self):
        """تحليل سلامة قاعدة البيانات"""
        print("🗄️ تحليل سلامة قاعدة البيانات...")
        
        db_analysis = {
            'connection_test': False,
            'table_structure': {},
            'data_integrity': {},
            'index_analysis': {},
            'foreign_key_constraints': [],
            'orphaned_records': [],
            'data_consistency': {},
            'backup_status': {}
        }
        
        try:
            # اختبار الاتصال
            from database.database_manager import DatabaseManager
            db = DatabaseManager()
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # اختبار الاتصال
                cursor.execute("SELECT 1")
                db_analysis['connection_test'] = True
                print("  ✅ اتصال قاعدة البيانات")
                
                # تحليل هيكل الجداول
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    
                    # معلومات الجدول
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    # عدد السجلات
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    record_count = cursor.fetchone()[0]
                    
                    db_analysis['table_structure'][table_name] = {
                        'columns': len(columns),
                        'records': record_count,
                        'column_details': [
                            {
                                'name': col[1],
                                'type': col[2],
                                'not_null': bool(col[3]),
                                'primary_key': bool(col[5])
                            } for col in columns
                        ]
                    }
                
                # تحليل الفهارس
                cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index'")
                indexes = cursor.fetchall()
                
                for index in indexes:
                    if not index[0].startswith('sqlite_'):  # تجاهل الفهارس التلقائية
                        db_analysis['index_analysis'][index[0]] = {
                            'table': index[1]
                        }
                
                print(f"  📊 عدد الجداول: {len(tables)}")
                print(f"  📈 عدد الفهارس: {len(db_analysis['index_analysis'])}")
                
                # فحص سلامة البيانات
                integrity_issues = self._check_data_integrity(cursor, db_analysis['table_structure'])
                db_analysis['data_integrity'] = integrity_issues
                
                if integrity_issues['issues']:
                    print(f"  ⚠️ مشاكل سلامة البيانات: {len(integrity_issues['issues'])}")
                else:
                    print("  ✅ سلامة البيانات")
        
        except Exception as e:
            print(f"  ❌ خطأ في تحليل قاعدة البيانات: {e}")
            db_analysis['error'] = str(e)
        
        self.audit_results['database_integrity'] = db_analysis
    
    def _check_data_integrity(self, cursor, table_structure):
        """فحص سلامة البيانات"""
        issues = []
        
        for table_name, info in table_structure.items():
            try:
                # فحص القيم الفارغة في الأعمدة المطلوبة
                for col in info['column_details']:
                    if col['not_null'] and not col['primary_key']:
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {col['name']} IS NULL")
                        null_count = cursor.fetchone()[0]
                        
                        if null_count > 0:
                            issues.append({
                                'table': table_name,
                                'column': col['name'],
                                'issue': f'{null_count} سجل يحتوي على قيم فارغة في عمود مطلوب'
                            })
                
                # فحص التكرار في المفاتيح الفريدة
                primary_keys = [col['name'] for col in info['column_details'] if col['primary_key']]
                if primary_keys:
                    pk_col = primary_keys[0]
                    cursor.execute(f"SELECT {pk_col}, COUNT(*) FROM {table_name} GROUP BY {pk_col} HAVING COUNT(*) > 1")
                    duplicates = cursor.fetchall()
                    
                    if duplicates:
                        issues.append({
                            'table': table_name,
                            'issue': f'{len(duplicates)} مفتاح أساسي مكرر'
                        })
            
            except Exception as e:
                issues.append({
                    'table': table_name,
                    'issue': f'خطأ في فحص السلامة: {e}'
                })
        
        return {'issues': issues}

    def analyze_performance(self):
        """تحليل الأداء"""
        print("⚡ تحليل الأداء...")

        performance_metrics = {
            'startup_time': 0,
            'memory_usage': {},
            'database_performance': {},
            'ui_responsiveness': {},
            'bottlenecks': [],
            'optimization_suggestions': []
        }

        try:
            import psutil
            import time

            # قياس استخدام الذاكرة
            process = psutil.Process()
            memory_info = process.memory_info()

            performance_metrics['memory_usage'] = {
                'rss': memory_info.rss / 1024 / 1024,  # MB
                'vms': memory_info.vms / 1024 / 1024,  # MB
                'percent': process.memory_percent()
            }

            print(f"  💾 استخدام الذاكرة: {performance_metrics['memory_usage']['rss']:.1f} MB")

            # اختبار أداء قاعدة البيانات
            db_perf = self._test_database_performance()
            performance_metrics['database_performance'] = db_perf

            if db_perf.get('avg_query_time', 0) > 100:  # أكثر من 100ms
                performance_metrics['bottlenecks'].append({
                    'component': 'database',
                    'issue': 'استعلامات قاعدة البيانات بطيئة',
                    'avg_time': db_perf['avg_query_time']
                })

            # اختبار أداء الاستيراد
            import_perf = self._test_import_performance()
            performance_metrics['import_performance'] = import_perf

        except ImportError:
            print("  ⚠️ psutil غير متوفر - تخطي تحليل الأداء المتقدم")
        except Exception as e:
            print(f"  ❌ خطأ في تحليل الأداء: {e}")

        self.audit_results['performance_analysis'] = performance_metrics

    def _test_database_performance(self):
        """اختبار أداء قاعدة البيانات"""
        try:
            from database.database_manager import DatabaseManager
            import time

            db = DatabaseManager()
            query_times = []

            # اختبار عدة استعلامات
            test_queries = [
                "SELECT COUNT(*) FROM users",
                "SELECT COUNT(*) FROM accounts",
                "SELECT COUNT(*) FROM journal_entries",
                "SELECT * FROM users LIMIT 10",
                "SELECT * FROM accounts LIMIT 10"
            ]

            for query in test_queries:
                try:
                    start_time = time.time()
                    with db.get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(query)
                        cursor.fetchall()
                    end_time = time.time()

                    query_time = (end_time - start_time) * 1000  # ms
                    query_times.append(query_time)
                except Exception:
                    continue

            if query_times:
                return {
                    'avg_query_time': sum(query_times) / len(query_times),
                    'max_query_time': max(query_times),
                    'min_query_time': min(query_times),
                    'total_queries': len(query_times)
                }
        except Exception as e:
            return {'error': str(e)}

        return {}

    def _test_import_performance(self):
        """اختبار أداء الاستيراد"""
        import time

        modules_to_test = [
            'ui.main_window',
            'database.database_manager',
            'auth.auth_manager',
            'themes.theme_manager'
        ]

        import_times = {}

        for module in modules_to_test:
            try:
                start_time = time.time()
                importlib.import_module(module)
                end_time = time.time()

                import_time = (end_time - start_time) * 1000  # ms
                import_times[module] = import_time
            except Exception as e:
                import_times[module] = f"خطأ: {e}"

        return import_times

    def analyze_ui_consistency(self):
        """تحليل اتساق الواجهة"""
        print("🎨 تحليل اتساق الواجهة...")

        ui_analysis = {
            'rtl_compliance': {},
            'font_consistency': {},
            'color_scheme': {},
            'layout_patterns': {},
            'accessibility': {},
            'responsive_design': {}
        }

        # فحص ملفات الواجهة
        ui_files = list(Path("ui").rglob("*.py")) if Path("ui").exists() else []

        rtl_patterns = []
        font_usage = []
        color_usage = []

        for ui_file in ui_files:
            try:
                with open(ui_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # فحص دعم RTL
                rtl_indicators = [
                    'anchor="e"',
                    'justify="right"',
                    'RTL',
                    'arabic',
                    'عربي'
                ]

                for indicator in rtl_indicators:
                    if indicator in content:
                        rtl_patterns.append({
                            'file': str(ui_file),
                            'indicator': indicator
                        })

                # فحص استخدام الخطوط
                font_patterns = re.findall(r'font.*=.*["\']([^"\']+)["\']', content, re.IGNORECASE)
                for font in font_patterns:
                    font_usage.append({
                        'file': str(ui_file),
                        'font': font
                    })

                # فحص استخدام الألوان
                color_patterns = re.findall(r'color.*=.*["\']([^"\']+)["\']', content, re.IGNORECASE)
                for color in color_patterns:
                    color_usage.append({
                        'file': str(ui_file),
                        'color': color
                    })

            except Exception as e:
                self.logger.error(f"خطأ في تحليل ملف الواجهة {ui_file}: {e}")

        ui_analysis['rtl_compliance'] = {
            'files_with_rtl': len(set(p['file'] for p in rtl_patterns)),
            'total_ui_files': len(ui_files),
            'rtl_patterns': rtl_patterns[:10]  # أول 10 أنماط
        }

        ui_analysis['font_consistency'] = {
            'unique_fonts': len(set(f['font'] for f in font_usage)),
            'font_usage': font_usage[:10]
        }

        ui_analysis['color_scheme'] = {
            'unique_colors': len(set(c['color'] for c in color_usage)),
            'color_usage': color_usage[:10]
        }

        self.audit_results['ui_consistency'] = ui_analysis

        # عرض النتائج
        rtl_coverage = (ui_analysis['rtl_compliance']['files_with_rtl'] /
                       max(ui_analysis['rtl_compliance']['total_ui_files'], 1)) * 100

        print(f"  🔄 تغطية RTL: {rtl_coverage:.1f}%")
        print(f"  🎨 خطوط مختلفة: {ui_analysis['font_consistency']['unique_fonts']}")
        print(f"  🌈 ألوان مختلفة: {ui_analysis['color_scheme']['unique_colors']}")

    def analyze_business_logic(self):
        """تحليل المنطق التجاري"""
        print("💼 تحليل المنطق التجاري...")

        business_analysis = {
            'accounting_rules': {},
            'data_validation': {},
            'workflow_integrity': {},
            'calculation_accuracy': {},
            'audit_trail': {}
        }

        try:
            # اختبار نظام القيد المزدوج
            from database.journal_entries_manager import JournalEntriesManager
        except Exception as e:
            pass
from typing import List, Dict, Optional, Tuple, Any, Union, Callable
            journal_manager = JournalEntriesManager()

            # اختبار التوازن
            test_cases = [
                # حالة متوازنة
                [
                    {'debit_amount': 1000, 'credit_amount': 0},
                    {'debit_amount': 0, 'credit_amount': 1000}
                ],
                # حالة غير متوازنة
                [
                    {'debit_amount': 1000, 'credit_amount': 0},
                    {'debit_amount': 0, 'credit_amount': 900}
                ],
                # حالة معقدة
                [
                    {'debit_amount': 500, 'credit_amount': 0},
                    {'debit_amount': 300, 'credit_amount': 0},
                    {'debit_amount': 0, 'credit_amount': 800}
                ]
            ]

            balance_tests = []
            for i, test_case in enumerate(test_cases):
                result = journal_manager._check_balance(test_case)
                balance_tests.append({
                    'test_case': i + 1,
                    'is_balanced': result['is_balanced'],
                    'total_debit': result['total_debit'],
                    'total_credit': result['total_credit'],
                    'difference': result['difference']
                })

            business_analysis['accounting_rules']['balance_tests'] = balance_tests

            # فحص دقة الحسابات
            passed_tests = sum(1 for test in balance_tests if
                             (test['is_balanced'] and abs(test['difference']) < 0.01) or
                             (not test['is_balanced'] and abs(test['difference']) >= 0.01))

            accuracy = (passed_tests / len(balance_tests)) * 100
            business_analysis['calculation_accuracy']['balance_accuracy'] = accuracy

            print(f"  ⚖️ دقة التوازن المحاسبي: {accuracy:.1f}%")

        except Exception as e:
            print(f"  ❌ خطأ في تحليل المنطق التجاري: {e}")
            business_analysis['error'] = str(e)

        self.audit_results['business_logic_validation'] = business_analysis

    def generate_comprehensive_report(self):
        """إنشاء تقرير شامل"""
        print("\n" + "="*80)
        print("📋 تقرير الفحص الشامل والعميق")
        print("="*80)

        # حساب النقاط الإجمالية
        total_score = 0
        max_score = 0

        # نقاط جودة الكود
        if 'code_quality' in self.audit_results:
            code_score = self._calculate_quality_score(self.audit_results['code_quality'])
            total_score += code_score
            max_score += 100
            print(f"\n🔍 جودة الكود: {code_score:.1f}/100")

        # نقاط الأمان
        if 'security_analysis' in self.audit_results:
            security_issues = sum(len(issues) for issues in self.audit_results['security_analysis'].values())
            security_score = max(0, 100 - security_issues * 10)
            total_score += security_score
            max_score += 100
            print(f"🔒 الأمان: {security_score:.1f}/100")

        # نقاط قاعدة البيانات
        if 'database_integrity' in self.audit_results:
            db_issues = len(self.audit_results['database_integrity'].get('data_integrity', {}).get('issues', []))
            db_score = max(0, 100 - db_issues * 15)
            total_score += db_score
            max_score += 100
            print(f"🗄️ قاعدة البيانات: {db_score:.1f}/100")

        # نقاط الواجهة
        if 'ui_consistency' in self.audit_results:
            ui_data = self.audit_results['ui_consistency']
            rtl_coverage = 0
            if ui_data['rtl_compliance']['total_ui_files'] > 0:
                rtl_coverage = (ui_data['rtl_compliance']['files_with_rtl'] /
                               ui_data['rtl_compliance']['total_ui_files']) * 100
            ui_score = rtl_coverage
            total_score += ui_score
            max_score += 100
            print(f"🎨 الواجهة: {ui_score:.1f}/100")

        # نقاط المنطق التجاري
        if 'business_logic_validation' in self.audit_results:
            business_data = self.audit_results['business_logic_validation']
            business_score = business_data.get('calculation_accuracy', {}).get('balance_accuracy', 0)
            total_score += business_score
            max_score += 100
            print(f"💼 المنطق التجاري: {business_score:.1f}/100")

        # النقاط الإجمالية
        overall_score = (total_score / max_score * 100) if max_score > 0 else 0

        print(f"\n🏆 النقاط الإجمالية: {overall_score:.1f}/100")

        # تقييم الحالة العامة
        if overall_score >= 90:
            status = "ممتاز ✨"
            status_color = "🟢"
        elif overall_score >= 80:
            status = "جيد جداً ✅"
            status_color = "🟡"
        elif overall_score >= 70:
            status = "جيد ⚠️"
            status_color = "🟠"
        else:
            status = "يحتاج تحسين ❌"
            status_color = "🔴"

        print(f"\n{status_color} حالة النظام: {status}")

        # حفظ التقرير
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': overall_score,
            'status': status,
            'detailed_results': self.audit_results,
            'critical_issues': self.critical_issues,
            'warnings': self.warnings,
            'recommendations': self.recommendations
        }

        report_file = f"deep_comprehensive_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 تم حفظ التقرير المفصل في: {report_file}")

        return overall_score >= 70

    def run_deep_audit(self):
        """تشغيل الفحص الشامل والعميق"""
        print("🚀 بدء الفحص الشامل والعميق للنظام")
        print("="*80)

        try:
            self.analyze_code_quality()
            self.analyze_security()
            self.analyze_database_integrity()
            self.analyze_performance()
            self.analyze_ui_consistency()
            self.analyze_business_logic()

            return self.generate_comprehensive_report()

        except Exception as e:
            print(f"❌ خطأ في تشغيل الفحص: {e}")
            traceback.print_exc()
            return False

def main():
    """الدالة الرئيسية"""
    auditor = DeepSystemAuditor()
    success = auditor.run_deep_audit()

    if success:
        print("\n🎉 تم إكمال الفحص الشامل بنجاح!")
        return 0
    else:
        print("\n⚠️ تم اكتشاف مشاكل تحتاج إلى معالجة")
        return 1

if __name__ == "__main__":
    sys.exit(main())
