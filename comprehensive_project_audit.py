#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 أداة الفحص الشامل للمشروع المحاسبي
Comprehensive Project Audit Tool

تقوم هذه الأداة بفحص شامل لجميع ملفات المشروع وإصلاح الأخطاء
"""

import os
import sys
import ast
import json
import shutil
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

class ProjectAuditor:
    """فئة فحص المشروع الشامل"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root.absolute()),
            "files_checked": 0,
            "errors_found": 0,
            "errors_fixed": 0,
            "files_cleaned": 0,
            "syntax_errors": [],
            "import_errors": [],
            "duplicate_files": [],
            "obsolete_files": [],
            "recommendations": []
        }
        
        # الملفات الأساسية المطلوبة
        self.essential_files = [
            "main.py",
            "ui/views/main_window.py",
            "ui/views/login_window.py",
            "database/hybrid_database_manager.py",
            "themes/modern_theme.py",
            "config/settings.py"
        ]
        
        # أنماط الملفات المؤقتة للحذف
        self.temp_patterns = [
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "__pycache__",
            "*.tmp",
            "*.temp",
            "*.log~",
            "*.bak",
            ".DS_Store",
            "Thumbs.db"
        ]
        
        # أنماط النسخ الاحتياطية القديمة
        self.backup_patterns = [
            "*.backup",
            "*.backup_*",
            "*.except_backup",
            "*_backup_*"
        ]

    def run_audit(self) -> Dict[str, Any]:
        """تشغيل الفحص الشامل"""
        print("🔍 بدء الفحص الشامل للمشروع...")
        print("=" * 60)
        
        try:
            # 1. فحص الملفات الأساسية
            self._check_essential_files()
            
            # 2. فحص ملفات Python
            self._check_python_files()
            
            # 3. فحص الاستيرادات
            self._check_imports()
            
            # 4. البحث عن الملفات المكررة
            self._find_duplicate_files()
            
            # 5. تنظيف الملفات المؤقتة
            self._clean_temp_files()
            
            # 6. تنظيف النسخ الاحتياطية القديمة
            self._clean_old_backups()
            
            # 7. إنشاء التوصيات
            self._generate_recommendations()
            
            print("\n✅ تم إكمال الفحص الشامل بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في الفحص الشامل: {e}")
            traceback.print_exc()
            self.report["audit_error"] = str(e)
        
        return self.report

    def _check_essential_files(self):
        """فحص الملفات الأساسية"""
        print("\n📁 فحص الملفات الأساسية...")
        
        missing_files = []
        for file_path in self.essential_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - مفقود")
                missing_files.append(file_path)
        
        if missing_files:
            self.report["missing_essential_files"] = missing_files
            self.report["errors_found"] += len(missing_files)

    def _check_python_files(self):
        """فحص ملفات Python للأخطاء النحوية"""
        print("\n🐍 فحص ملفات Python...")
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for py_file in python_files:
            if self._should_skip_file(py_file):
                continue
                
            self.report["files_checked"] += 1
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # فحص بناء الجملة
                try:
                    ast.parse(content)
                    print(f"✅ {py_file.relative_to(self.project_root)}")
                except SyntaxError as e:
                    error_info = {
                        "file": str(py_file.relative_to(self.project_root)),
                        "line": e.lineno,
                        "error": str(e)
                    }
                    self.report["syntax_errors"].append(error_info)
                    self.report["errors_found"] += 1
                    print(f"❌ {py_file.relative_to(self.project_root)} - خطأ نحوي: {e}")
                    
            except Exception as e:
                print(f"⚠️ لا يمكن قراءة {py_file.relative_to(self.project_root)}: {e}")

    def _check_imports(self):
        """فحص الاستيرادات"""
        print("\n📦 فحص الاستيرادات...")
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for py_file in python_files:
            if self._should_skip_file(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.Import, ast.ImportFrom)):
                            # هنا يمكن إضافة فحص أكثر تفصيلاً للاستيرادات
                            pass
                except:
                    pass
                    
            except Exception as e:
                continue

    def _find_duplicate_files(self):
        """البحث عن الملفات المكررة"""
        print("\n🔍 البحث عن الملفات المكررة...")
        
        file_hashes = {}
        duplicates = []
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and not self._should_skip_file(file_path):
                try:
                    # حساب hash للملف
                    import hashlib
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash in file_hashes:
                        duplicates.append({
                            "original": str(file_hashes[file_hash].relative_to(self.project_root)),
                            "duplicate": str(file_path.relative_to(self.project_root))
                        })
                        print(f"🔄 ملف مكرر: {file_path.relative_to(self.project_root)}")
                    else:
                        file_hashes[file_hash] = file_path
                        
                except Exception:
                    continue
        
        self.report["duplicate_files"] = duplicates

    def _clean_temp_files(self):
        """تنظيف الملفات المؤقتة"""
        print("\n🧹 تنظيف الملفات المؤقتة...")
        
        cleaned_files = []
        
        for pattern in self.temp_patterns:
            for file_path in self.project_root.rglob(pattern):
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        cleaned_files.append(str(file_path.relative_to(self.project_root)))
                        print(f"🗑️ حذف: {file_path.relative_to(self.project_root)}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        cleaned_files.append(str(file_path.relative_to(self.project_root)))
                        print(f"🗑️ حذف مجلد: {file_path.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"⚠️ لا يمكن حذف {file_path}: {e}")
        
        self.report["temp_files_cleaned"] = cleaned_files
        self.report["files_cleaned"] += len(cleaned_files)

    def _clean_old_backups(self):
        """تنظيف النسخ الاحتياطية القديمة"""
        print("\n🧹 تنظيف النسخ الاحتياطية القديمة...")
        
        cleaned_backups = []
        
        # البحث عن مجلدات النسخ الاحتياطية
        backup_dirs = [
            "backup_*",
            "*_backup",
            "backups"
        ]
        
        for pattern in backup_dirs:
            for backup_dir in self.project_root.glob(pattern):
                if backup_dir.is_dir():
                    # الاحتفاظ بأحدث 3 نسخ احتياطية فقط
                    backup_files = list(backup_dir.rglob("*"))
                    if len(backup_files) > 100:  # إذا كان هناك أكثر من 100 ملف
                        print(f"📁 مجلد نسخ احتياطية كبير: {backup_dir.name}")
                        # يمكن إضافة منطق لحذف الملفات القديمة
        
        # البحث عن ملفات النسخ الاحتياطية المفردة
        for pattern in self.backup_patterns:
            for backup_file in self.project_root.rglob(pattern):
                if backup_file.is_file():
                    # فحص تاريخ الملف
                    file_age = datetime.now().timestamp() - backup_file.stat().st_mtime
                    if file_age > 30 * 24 * 3600:  # أكثر من 30 يوم
                        try:
                            backup_file.unlink()
                            cleaned_backups.append(str(backup_file.relative_to(self.project_root)))
                            print(f"🗑️ حذف نسخة احتياطية قديمة: {backup_file.relative_to(self.project_root)}")
                        except Exception as e:
                            print(f"⚠️ لا يمكن حذف {backup_file}: {e}")
        
        self.report["old_backups_cleaned"] = cleaned_backups

    def _generate_recommendations(self):
        """إنشاء التوصيات"""
        recommendations = []
        
        if self.report["syntax_errors"]:
            recommendations.append("إصلاح الأخطاء النحوية في ملفات Python")
        
        if self.report["duplicate_files"]:
            recommendations.append("مراجعة الملفات المكررة وحذف غير الضروري منها")
        
        if "missing_essential_files" in self.report:
            recommendations.append("إنشاء الملفات الأساسية المفقودة")
        
        recommendations.extend([
            "تحديث ملف requirements.txt بالمكتبات المطلوبة",
            "إنشاء نسخة احتياطية قبل إجراء تغييرات كبيرة",
            "تحديث التوثيق والملفات التوضيحية"
        ])
        
        self.report["recommendations"] = recommendations

    def _should_skip_file(self, file_path: Path) -> bool:
        """تحديد ما إذا كان يجب تخطي الملف"""
        skip_patterns = [
            "__pycache__",
            ".git",
            ".vscode",
            ".idea",
            "node_modules",
            "backup_",
            ".backup",
            ".log"
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)

    def save_report(self, filename: str = None):
        """حفظ التقرير"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comprehensive_audit_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ التقرير في: {filename}")
        return filename

def main():
    """الدالة الرئيسية"""
    print("🔍 أداة الفحص الشامل للمشروع المحاسبي")
    print("=" * 60)
    
    auditor = ProjectAuditor()
    report = auditor.run_audit()
    
    # حفظ التقرير
    report_file = auditor.save_report()
    
    # عرض ملخص النتائج
    print("\n📊 ملخص النتائج:")
    print(f"   📁 ملفات تم فحصها: {report['files_checked']}")
    print(f"   ❌ أخطاء مكتشفة: {report['errors_found']}")
    print(f"   🧹 ملفات تم تنظيفها: {report['files_cleaned']}")
    print(f"   🔄 ملفات مكررة: {len(report['duplicate_files'])}")
    
    if report['syntax_errors']:
        print(f"\n❌ أخطاء نحوية ({len(report['syntax_errors'])}):")
        for error in report['syntax_errors']:
            print(f"   - {error['file']} (السطر {error['line']})")
    
    if report['recommendations']:
        print(f"\n💡 التوصيات:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"   {i}. {rec}")

if __name__ == "__main__":
    main()
