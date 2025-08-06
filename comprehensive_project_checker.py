# -*- coding: utf-8 -*-
"""
فحص شامل ومتعمق لجميع ملفات المشروع
Comprehensive Project Checker
"""

import os
import ast
import sys
import json
from pathlib import Path
from datetime import datetime

class ComprehensiveProjectChecker:
    def __init__(self):
        self.project_root = Path('.')
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "syntax_errors": [],
            "import_errors": [],
            "missing_files": [],
            "pep8_violations": [],
            "logical_errors": [],
            "integration_issues": [],
            "recommendations": []
        }
        
    def check_syntax_errors(self):
        """فحص الأخطاء النحوية"""
        print("🔍 فحص الأخطاء النحوية...")
        
        python_files = list(self.project_root.rglob("*.py"))
        total_files = 0
        
        for py_file in python_files:
            # تجاهل المجلدات المؤقتة والنسخ الاحتياطية
            if any(skip in str(py_file) for skip in ['__pycache__', '.git', 'venv', 'backup', 'BACKUP']):
                continue
                
            total_files += 1
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # فحص الأخطاء النحوية
                try:
                    ast.parse(content)
                    print(f"✅ {py_file.name}")
                except SyntaxError as e:
                    error_info = {
                        "file": str(py_file),
                        "line": e.lineno,
                        "column": e.offset,
                        "error": str(e),
                        "severity": "high"
                    }
                    self.report["syntax_errors"].append(error_info)
                    print(f"❌ {py_file.name}: خطأ نحوي في السطر {e.lineno}")
                    
            except Exception as e:
                print(f"⚠️ {py_file.name}: خطأ في القراءة - {e}")
        
        print(f"📊 تم فحص {total_files} ملف")
        print(f"❌ أخطاء نحوية: {len(self.report['syntax_errors'])}")
        
    def check_import_errors(self):
        """فحص أخطاء الاستيراد"""
        print("\n🔍 فحص أخطاء الاستيراد...")
        
        # الملفات الأساسية المطلوبة
        critical_files = [
            "large_font_run.py",
            "control_panel/control_panel_window.py",
            "control_panel/settings_pages/general_settings.py",
            "control_panel/settings_pages/company_settings.py", 
            "control_panel/settings_pages/accounting_settings.py",
            "core/settings_manager.py"
        ]
        
        for file_path in critical_files:
            if not (self.project_root / file_path).exists():
                self.report["missing_files"].append(file_path)
                print(f"❌ ملف مفقود: {file_path}")
            else:
                print(f"✅ {file_path}")
                
    def check_integration_issues(self):
        """فحص مشاكل التكامل"""
        print("\n🔍 فحص مشاكل التكامل...")
        
        # فحص تكامل نافذة الإعدادات
        try:
            # فحص large_font_run.py
            large_font_file = self.project_root / "large_font_run.py"
            if large_font_file.exists():
                with open(large_font_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "def open_settings_window" in content:
                    print("✅ دالة فتح الإعدادات موجودة في large_font_run.py")
                else:
                    self.report["integration_issues"].append("دالة فتح الإعدادات مفقودة في large_font_run.py")
                    print("❌ دالة فتح الإعدادات مفقودة في large_font_run.py")
                    
                if "from control_panel.control_panel_window import ControlPanelWindow" in content:
                    print("✅ استيراد نافذة الإعدادات موجود")
                else:
                    print("⚠️ استيراد نافذة الإعدادات قد يكون داخل الدالة")
                    
        except Exception as e:
            print(f"❌ خطأ في فحص التكامل: {e}")
            
    def check_settings_system(self):
        """فحص نظام الإعدادات"""
        print("\n🔍 فحص نظام الإعدادات...")
        
        # فحص ملف إدارة الإعدادات
        settings_manager = self.project_root / "core/settings_manager.py"
        if settings_manager.exists():
            print("✅ ملف إدارة الإعدادات موجود")
            
            # فحص مجلد config
            config_dir = self.project_root / "config"
            if config_dir.exists():
                print("✅ مجلد config موجود")
            else:
                self.report["missing_files"].append("config/")
                print("❌ مجلد config مفقود")
        else:
            self.report["missing_files"].append("core/settings_manager.py")
            print("❌ ملف إدارة الإعدادات مفقود")
            
    def test_basic_functionality(self):
        """اختبار الوظائف الأساسية"""
        print("\n🧪 اختبار الوظائف الأساسية...")
        
        try:
            # اختبار استيراد المكتبات الأساسية
            import customtkinter as ctk
            print("✅ customtkinter متوفر")
        except ImportError:
            self.report["import_errors"].append("customtkinter مفقود")
            print("❌ customtkinter مفقود")
            
        try:
            from PIL import Image
            print("✅ PIL/Pillow متوفر")
        except ImportError:
            self.report["import_errors"].append("PIL/Pillow مفقود")
            print("❌ PIL/Pillow مفقود")
            
        # اختبار استيراد نظام الإعدادات
        try:
            sys.path.insert(0, str(self.project_root))
            from core.settings_manager import SettingsManager
            print("✅ نظام الإعدادات قابل للاستيراد")
        except ImportError as e:
            self.report["import_errors"].append(f"نظام الإعدادات: {e}")
            print(f"❌ نظام الإعدادات: {e}")
            
    def generate_report(self):
        """إنشاء تقرير شامل"""
        print("\n📋 إنشاء التقرير الشامل...")
        
        # حساب الإحصائيات
        total_issues = (len(self.report["syntax_errors"]) + 
                       len(self.report["import_errors"]) + 
                       len(self.report["missing_files"]) + 
                       len(self.report["integration_issues"]))
        
        # إضافة التوصيات
        if self.report["syntax_errors"]:
            self.report["recommendations"].append("إصلاح الأخطاء النحوية أولاً")
            
        if self.report["missing_files"]:
            self.report["recommendations"].append("إنشاء الملفات المفقودة")
            
        if self.report["import_errors"]:
            self.report["recommendations"].append("تثبيت المكتبات المفقودة")
            
        if self.report["integration_issues"]:
            self.report["recommendations"].append("إصلاح مشاكل التكامل")
            
        # حفظ التقرير
        report_file = f"comprehensive_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
            
        print(f"📄 تم حفظ التقرير في: {report_file}")
        
        # طباعة الملخص
        print(f"\n📊 ملخص الفحص:")
        print(f"   ❌ إجمالي المشاكل: {total_issues}")
        print(f"   🔧 أخطاء نحوية: {len(self.report['syntax_errors'])}")
        print(f"   📦 أخطاء استيراد: {len(self.report['import_errors'])}")
        print(f"   📁 ملفات مفقودة: {len(self.report['missing_files'])}")
        print(f"   🔗 مشاكل تكامل: {len(self.report['integration_issues'])}")
        
        if total_issues == 0:
            print("🎉 لا توجد مشاكل! المشروع في حالة جيدة.")
        else:
            print("⚠️ يحتاج المشروع إلى إصلاحات.")
            
        return self.report
        
    def run_comprehensive_check(self):
        """تشغيل الفحص الشامل"""
        print("🔧 بدء الفحص الشامل والمتعمق للمشروع...")
        print("=" * 60)
        
        self.check_syntax_errors()
        self.check_import_errors()
        self.check_integration_issues()
        self.check_settings_system()
        self.test_basic_functionality()
        
        return self.generate_report()

if __name__ == "__main__":
    checker = ComprehensiveProjectChecker()
    report = checker.run_comprehensive_check()
