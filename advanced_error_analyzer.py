#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
محلل الأخطاء المتقدم والعميق
Advanced Deep Error Analyzer
"""

import ast
import re
import sys
import traceback
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
import json
from datetime import datetime
import logging
import sqlite3

class AdvancedErrorAnalyzer:
    """محلل الأخطاء المتقدم والعميق"""

    def __init__(self):
        self.project_root = Path(".")
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "syntax_errors": [],
            "import_errors": [],
            "runtime_errors": [],
            "logic_errors": [],
            "performance_issues": [],
            "ui_errors": [],
            "database_errors": [],
            "recommendations": []
        }

        # إعداد نظام السجلات
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # قائمة الملفات المهمة للفحص
        self.critical_files = [
            "main.py",
            "ui/main_window.py",
            "ui/login_window.py",
            "database/hybrid_database_manager.py",
            "services/sales_manager.py",
            "core/scheduler_manager.py",
            "themes/theme_manager.py"
        ]

    def analyze_syntax_errors(self):
        """تحليل الأخطاء النحوية"""
        print("🔍 تحليل الأخطاء النحوية...")

        python_files = list(self.project_root.rglob("*.py"))
        syntax_errors = []

        for file_path in python_files:
            if any(skip in str(file_path) for skip in ["__pycache__", ".git", "venv"]):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # محاولة تحليل الملف نحوياً
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    syntax_errors.append({
                        "file": str(file_path),
                        "line": e.lineno,
                        "column": e.offset,
                        "error": str(e),
                        "severity": "high" if str(file_path) in self.critical_files else "medium"
                    })

            except Exception as e:
                self.logger.error(f"خطأ في قراءة {file_path}: {e}")

        self.analysis_results["syntax_errors"] = syntax_errors
        print(f"   📊 تم العثور على {len(syntax_errors)} خطأ نحوي")

        return syntax_errors

    def analyze_import_errors(self):
        """تحليل أخطاء الاستيرادات"""
        print("📦 تحليل أخطاء الاستيرادات...")

        import_errors = []

        for file_path in self.critical_files:
            file_path = Path(file_path)
            if not file_path.exists():
                continue

            try:
                # محاولة استيراد الملف
                spec = None
                module_name = str(file_path).replace('/', '.').replace('\\', '.').replace('.py', '')

                try:
                    # تشغيل الملف في بيئة منفصلة للتحقق من الاستيرادات
                    result = subprocess.run([
                        sys.executable, '-c', f'import {module_name}'
                    ], capture_output=True, text=True, timeout=10)

                    if result.returncode != 0:
                        import_errors.append({
                            "file": str(file_path),
                            "error": result.stderr.strip(),
                            "severity": "high"
                        })

                except subprocess.TimeoutExpired:
                    import_errors.append({
                        "file": str(file_path),
                        "error": "Timeout during import test",
                        "severity": "medium"
                    })

            except Exception as e:
                import_errors.append({
                    "file": str(file_path),
                    "error": str(e),
                    "severity": "medium"
                })

        self.analysis_results["import_errors"] = import_errors
        print(f"   📊 تم العثور على {len(import_errors)} خطأ استيراد")

        return import_errors

    def analyze_runtime_errors(self):
        """تحليل أخطاء وقت التشغيل"""
        print("⚡ تحليل أخطاء وقت التشغيل...")

        runtime_errors = []

        # اختبار تشغيل البرنامج الرئيسي
        try:
            result = subprocess.run([
                sys.executable, '-c', 
                'from ui.main_window import MainApplication; print("SUCCESS")'
            ], capture_output=True, text=True, timeout=15)

            if result.returncode != 0:
                runtime_errors.append({
                    "component": "MainApplication",
                    "error": result.stderr.strip(),
                    "severity": "critical"
                })
            else:
                print("   ✅ MainApplication يمكن استيراده بنجاح")

        except subprocess.TimeoutExpired:
            runtime_errors.append({
                "component": "MainApplication",
                "error": "Timeout during runtime test",
                "severity": "high"
            })
        except Exception as e:
            runtime_errors.append({
                "component": "MainApplication", 
                "error": str(e),
                "severity": "high"
            })

        # اختبار مكونات أخرى مهمة
        components_to_test = [
            "database.hybrid_database_manager.HybridDatabaseManager",
            "services.sales_manager.SalesManager",
            "themes.theme_manager.ThemeManager"
        ]

        for component in components_to_test:
            try:
                result = subprocess.run([
                    sys.executable, '-c', 
                    f'from {component.rsplit(".", 1)[0]} import {component.split(".")[-1]}; print("SUCCESS")'
                ], capture_output=True, text=True, timeout=10)

                if result.returncode != 0:
                    runtime_errors.append({
                        "component": component,
                        "error": result.stderr.strip(),
                        "severity": "high"
                    })
                else:
                    print(f"   ✅ {component} يعمل بنجاح")

            except Exception as e:
                runtime_errors.append({
                    "component": component,
                    "error": str(e),
                    "severity": "medium"
                })

        self.analysis_results["runtime_errors"] = runtime_errors
        print(f"   📊 تم العثور على {len(runtime_errors)} خطأ وقت تشغيل")

        return runtime_errors

    def analyze_ui_errors(self):
        """تحليل أخطاء الواجهة الرسومية"""
        print("🖼️ تحليل أخطاء الواجهة الرسومية...")

        ui_errors = []

        # فحص مشاكل تحميل الصور
        ui_files = list(Path("ui").glob("*.py"))

        for file_path in ui_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # البحث عن استخدام Image بدون استيراد
                if re.search(r'\bImage\.(open|new|fromarray)', content):
                    if 'from PIL import Image' not in content and 'import PIL' not in content:
                        ui_errors.append({
                            "file": str(file_path),
                            "error": "استخدام Image بدون استيراد PIL",
                            "type": "missing_import",
                            "severity": "medium"
                        })

                # البحث عن مشاكل customtkinter
                if 'customtkinter' in content:
                    # فحص استخدام after بدون معالجة الأخطاء
                    if re.search(r'\.after\(\d+', content):
                        if 'try:' not in content or 'except' not in content:
                            ui_errors.append({
                                "file": str(file_path),
                                "error": "استخدام after بدون معالجة أخطاء",
                                "type": "error_handling",
                                "severity": "low"
                            })

            except Exception as e:
                ui_errors.append({
                    "file": str(file_path),
                    "error": f"خطأ في قراءة الملف: {e}",
                    "type": "file_error",
                    "severity": "medium"
                })

        self.analysis_results["ui_errors"] = ui_errors
        print(f"   📊 تم العثور على {len(ui_errors)} خطأ واجهة رسومية")

        return ui_errors

    def analyze_database_errors(self):
        """تحليل أخطاء قاعدة البيانات"""
        print("🗄️ تحليل أخطاء قاعدة البيانات...")

        database_errors = []

        # فحص ملفات قاعدة البيانات
        db_files = list(Path("database").glob("*.py"))

        for file_path in db_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # البحث عن استعلامات SQL غير آمنة
                if re.search(r'f["\'].*\{.*\}.*["\']', content):
                    database_errors.append({
                        "file": str(file_path),
                        "error": "استخدام f-strings في SQL queries (مخاطر أمنية)",
                        "type": "security",
                        "severity": "high"
                    })

                # البحث عن عدم إغلاق الاتصالات
                if 'sqlite3.connect' in content or 'psycopg2.connect' in content:
                    if '.close()' not in content and 'with' not in content:
                        database_errors.append({
                            "file": str(file_path),
                            "error": "عدم إغلاق اتصالات قاعدة البيانات",
                            "type": "resource_leak",
                            "severity": "medium"
                        })

            except Exception as e:
                database_errors.append({
                    "file": str(file_path),
                    "error": f"خطأ في قراءة الملف: {e}",
                    "type": "file_error",
                    "severity": "medium"
                })

        self.analysis_results["database_errors"] = database_errors
        print(f"   📊 تم العثور على {len(database_errors)} خطأ قاعدة بيانات")

        return database_errors

    def generate_recommendations(self):
        """إنشاء التوصيات"""
        recommendations = []

        # توصيات بناءً على الأخطاء المكتشفة
        if self.analysis_results["syntax_errors"]:
            recommendations.append("إصلاح الأخطاء النحوية فوراً - أولوية عالية")

        if self.analysis_results["import_errors"]:
            recommendations.append("مراجعة وإصلاح جميع مشاكل الاستيرادات")

        if self.analysis_results["runtime_errors"]:
            recommendations.append("إصلاح أخطاء وقت التشغيل - أولوية حرجة")

        if self.analysis_results["ui_errors"]:
            recommendations.append("تحسين معالجة أخطاء الواجهة الرسومية")

        if self.analysis_results["database_errors"]:
            recommendations.append("مراجعة أمان وكفاءة استعلامات قاعدة البيانات")

        # توصيات عامة
        recommendations.extend([
            "إضافة اختبارات وحدة شاملة",
            "تطبيق معايير الكود الآمن",
            "إنشاء نظام مراقبة الأخطاء",
            "توثيق جميع الوظائف والكلاسات",
            "إنشاء نظام نسخ احتياطي متقدم"
        ])

        self.analysis_results["recommendations"] = recommendations

    def save_detailed_report(self):
        """حفظ تقرير مفصل"""
        report_file = f"deep_error_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)

            print(f"\n📋 تم حفظ التقرير المفصل: {report_file}")
            return report_file

        except Exception as e:
            self.logger.error(f"خطأ في حفظ التقرير: {e}")
            return None

    def run_deep_analysis(self):
        """تشغيل التحليل العميق الشامل"""
        print("🔬 بدء التحليل العميق والشامل للأخطاء")
        print("=" * 60)

        # تشغيل جميع أنواع التحليل
        syntax_errors = self.analyze_syntax_errors()
        import_errors = self.analyze_import_errors()
        runtime_errors = self.analyze_runtime_errors()
        ui_errors = self.analyze_ui_errors()
        database_errors = self.analyze_database_errors()

        # إنشاء التوصيات
        self.generate_recommendations()

        # عرض الملخص
        print(f"\n📊 ملخص التحليل العميق:")
        print(f"   🔍 أخطاء نحوية: {len(syntax_errors)}")
        print(f"   📦 أخطاء استيراد: {len(import_errors)}")
        print(f"   ⚡ أخطاء وقت تشغيل: {len(runtime_errors)}")
        print(f"   🖼️ أخطاء واجهة رسومية: {len(ui_errors)}")
        print(f"   🗄️ أخطاء قاعدة بيانات: {len(database_errors)}")

        total_errors = len(syntax_errors) + len(import_errors) + len(runtime_errors) + len(ui_errors) + len(database_errors)
        print(f"   📈 إجمالي الأخطاء: {total_errors}")

        # حفظ التقرير
        report_file = self.save_detailed_report()

        # عرض التوصيات
        print(f"\n💡 التوصيات الرئيسية:")
        for i, rec in enumerate(self.analysis_results["recommendations"][:5], 1):
            print(f"   {i}. {rec}")

        print(f"\n🎯 حالة البرنامج:")
        if total_errors == 0:
            print("   ✅ ممتاز - لا توجد أخطاء مكتشفة")
        elif total_errors <= 5:
            print("   🟡 جيد - أخطاء قليلة تحتاج إصلاح")
        elif total_errors <= 15:
            print("   🟠 متوسط - عدة أخطاء تحتاج اهتمام")
        else:
            print("   🔴 يحتاج عمل - أخطاء كثيرة تحتاج إصلاح فوري")

        return self.analysis_results

def main():
    """الدالة الرئيسية"""
    analyzer = AdvancedErrorAnalyzer()
    results = analyzer.run_deep_analysis()

    print(f"\n🎉 تم الانتهاء من التحليل العميق!")

    return results

if __name__ == "__main__":
    main()
