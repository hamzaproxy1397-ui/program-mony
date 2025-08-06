#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة التحليل الشامل لتنظيف الملفات غير الضرورية
Comprehensive File Cleanup Analyzer
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import ast
import re

class ComprehensiveFileCleanupAnalyzer:
    def __init__(self):
        self.project_root = Path(".")
        self.analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "total_files_analyzed": 0,
            "total_size_mb": 0,
            "files_to_delete": {},
            "files_to_keep": {},
            "backup_analysis": {},
            "dependency_analysis": {},
            "recommendations": []
        }
        
        # الملفات الأساسية التي يجب الاحتفاظ بها
        self.core_files = {
            "main.py", "START_HERE.py", "requirements.txt", "LICENSE", "README.md",
            "setup.py", "run.py", "launch_app.py"
        }
        
        # المجلدات الأساسية
        self.core_directories = {
            "ui", "database", "core", "auth", "config", "themes", "services", 
            "models", "reports", "assets"
        }
        
        # أنماط الملفات المؤقتة والنسخ الاحتياطية
        self.temporary_patterns = {
            "backup_files": [
                "backup_*", "*.backup", "*.bak", "*_backup_*", 
                "COMPLETE_SYSTEM_BACKUP_*"
            ],
            "cache_files": [
                "__pycache__", "*.pyc", "*.pyo", "*.pyd"
            ],
            "log_files": [
                "*.log", "logs/*", "*_report_*.json", "*_report_*.md"
            ],
            "test_files": [
                "test_*.py", "*_test.py", "comprehensive_validation_test.py"
            ],
            "temp_files": [
                "temp_*.py", "*_temp.py", "search_temp.py", "temp_clean_end.py"
            ],
            "fixer_files": [
                "*_fixer.py", "*_analyzer.py", "*_checker.py", "*_diagnostic.py",
                "comprehensive_*_fixer.py", "ultimate_*_fixer.py", "deep_*_fixer.py"
            ],
            "duplicate_files": [
                "*_fixed.py", "*_enhanced.py", "*_improved.py"
            ]
        }
        
        # الملفات المستخدمة فعلياً
        self.used_files = set()
        self.imported_modules = set()
        
    def analyze_project(self) -> Dict:
        """تحليل شامل للمشروع"""
        print("🔍 بدء التحليل الشامل للمشروع...")
        
        # 1. تحليل الملفات المستخدمة
        self._analyze_used_files()
        
        # 2. تحليل النسخ الاحتياطية
        self._analyze_backup_files()
        
        # 3. تحليل الملفات المؤقتة
        self._analyze_temporary_files()
        
        # 4. تحليل الملفات المكررة
        self._analyze_duplicate_files()
        
        # 5. تحليل ملفات التوثيق
        self._analyze_documentation_files()
        
        # 6. تحليل الأصول (Assets)
        self._analyze_assets()
        
        # 7. إنشاء التوصيات
        self._generate_recommendations()
        
        return self.analysis_report
    
    def _analyze_used_files(self):
        """تحليل الملفات المستخدمة فعلياً في النظام"""
        print("📊 تحليل الملفات المستخدمة...")
        
        # البدء من الملفات الرئيسية
        entry_points = ["main.py", "START_HERE.py", "large_font_run.py"]
        
        for entry_point in entry_points:
            if Path(entry_point).exists():
                self._trace_dependencies(Path(entry_point))
        
        # تحليل ملفات UI الرئيسية
        ui_main_files = [
            "ui/main_window.py", "ui/login_window.py", "ui/pos_window.py",
            "ui/pos_simple.py"
        ]
        
        for ui_file in ui_main_files:
            if Path(ui_file).exists():
                self._trace_dependencies(Path(ui_file))
    
    def _trace_dependencies(self, file_path: Path):
        """تتبع التبعيات لملف معين"""
        if file_path in self.used_files:
            return
            
        self.used_files.add(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تحليل الاستيرادات
            imports = self._extract_imports(content)
            
            for imp in imports:
                # تحويل الاستيراد إلى مسار ملف
                file_paths = self._import_to_file_path(imp)
                for fp in file_paths:
                    if fp.exists() and fp not in self.used_files:
                        self._trace_dependencies(fp)
                        
        except Exception as e:
            print(f"⚠️ خطأ في تحليل {file_path}: {e}")
    
    def _extract_imports(self, content: str) -> List[str]:
        """استخراج الاستيرادات من محتوى الملف"""
        imports = []
        
        # استيرادات from ... import
        from_imports = re.findall(r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import', content)
        imports.extend(from_imports)
        
        # استيرادات import
        direct_imports = re.findall(r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)', content)
        imports.extend(direct_imports)
        
        return imports
    
    def _import_to_file_path(self, import_name: str) -> List[Path]:
        """تحويل اسم الاستيراد إلى مسار ملف"""
        paths = []
        
        # تجاهل المكتبات الخارجية
        external_libs = {
            'tkinter', 'customtkinter', 'sqlite3', 'json', 'os', 'sys', 
            'datetime', 'pathlib', 'logging', 'threading', 'PIL', 'numpy'
        }
        
        if import_name.split('.')[0] in external_libs:
            return paths
        
        # تحويل النقاط إلى مسارات
        parts = import_name.split('.')
        
        # محاولة العثور على الملف
        for i in range(len(parts)):
            potential_path = Path('/'.join(parts[:i+1]) + '.py')
            if potential_path.exists():
                paths.append(potential_path)
        
        # محاولة العثور على المجلد مع __init__.py
        potential_dir = Path('/'.join(parts))
        if potential_dir.exists() and (potential_dir / '__init__.py').exists():
            paths.append(potential_dir / '__init__.py')
        
        return paths
    
    def _analyze_backup_files(self):
        """تحليل ملفات النسخ الاحتياطية"""
        print("💾 تحليل ملفات النسخ الاحتياطية...")
        
        backup_info = {
            "backup_directories": [],
            "backup_files": [],
            "total_backup_size_mb": 0,
            "oldest_backup": None,
            "newest_backup": None
        }
        
        # البحث عن مجلدات النسخ الاحتياطية
        for item in self.project_root.iterdir():
            if item.is_dir() and any(pattern in item.name.lower() for pattern in ['backup', 'نسخ']):
                backup_info["backup_directories"].append({
                    "name": item.name,
                    "size_mb": self._get_directory_size(item),
                    "file_count": len(list(item.rglob("*")))
                })
        
        # البحث عن ملفات النسخ الاحتياطية
        for pattern in self.temporary_patterns["backup_files"]:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    backup_info["backup_files"].append({
                        "path": str(file_path),
                        "size_mb": file_path.stat().st_size / (1024 * 1024),
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
        
        self.analysis_report["backup_analysis"] = backup_info
    
    def _analyze_temporary_files(self):
        """تحليل الملفات المؤقتة"""
        print("🧹 تحليل الملفات المؤقتة...")
        
        temp_categories = {}
        
        for category, patterns in self.temporary_patterns.items():
            temp_categories[category] = []
            
            for pattern in patterns:
                for file_path in self.project_root.rglob(pattern):
                    if file_path.is_file():
                        temp_categories[category].append({
                            "path": str(file_path),
                            "size_mb": file_path.stat().st_size / (1024 * 1024),
                            "can_delete": self._can_delete_file(file_path)
                        })
        
        self.analysis_report["files_to_delete"] = temp_categories
    
    def _analyze_duplicate_files(self):
        """تحليل الملفات المكررة"""
        print("🔄 تحليل الملفات المكررة...")
        
        # البحث عن ملفات مشابهة
        similar_files = {}
        
        for py_file in self.project_root.rglob("*.py"):
            base_name = py_file.stem
            
            # البحث عن ملفات مشابهة
            variations = [
                f"{base_name}_fixed.py",
                f"{base_name}_enhanced.py", 
                f"{base_name}_improved.py",
                f"{base_name}_new.py",
                f"{base_name}_old.py"
            ]
            
            found_variations = []
            for var in variations:
                var_path = py_file.parent / var
                if var_path.exists():
                    found_variations.append(str(var_path))
            
            if found_variations:
                similar_files[str(py_file)] = found_variations
        
        self.analysis_report["duplicate_analysis"] = similar_files
    
    def _analyze_documentation_files(self):
        """تحليل ملفات التوثيق"""
        print("📚 تحليل ملفات التوثيق...")
        
        doc_files = {
            "essential_docs": [],
            "redundant_docs": [],
            "outdated_docs": []
        }
        
        # الملفات الأساسية للتوثيق
        essential_patterns = ["README.md", "LICENSE", "USER_GUIDE.md"]
        
        for doc_file in self.project_root.rglob("*.md"):
            if doc_file.name in essential_patterns:
                doc_files["essential_docs"].append(str(doc_file))
            elif any(word in doc_file.name.upper() for word in ["REPORT", "AUDIT", "SUMMARY", "UPDATE"]):
                doc_files["redundant_docs"].append(str(doc_file))
            else:
                doc_files["outdated_docs"].append(str(doc_file))
        
        self.analysis_report["documentation_analysis"] = doc_files
    
    def _analyze_assets(self):
        """تحليل ملفات الأصول"""
        print("🖼️ تحليل ملفات الأصول...")
        
        assets_info = {
            "used_assets": [],
            "unused_assets": [],
            "total_assets_size_mb": 0
        }
        
        assets_dir = Path("assets")
        if assets_dir.exists():
            for asset_file in assets_dir.rglob("*"):
                if asset_file.is_file():
                    size_mb = asset_file.stat().st_size / (1024 * 1024)
                    assets_info["total_assets_size_mb"] += size_mb
                    
                    # فحص ما إذا كان الأصل مستخدماً
                    if self._is_asset_used(asset_file):
                        assets_info["used_assets"].append(str(asset_file))
                    else:
                        assets_info["unused_assets"].append({
                            "path": str(asset_file),
                            "size_mb": size_mb
                        })
        
        self.analysis_report["assets_analysis"] = assets_info
    
    def _is_asset_used(self, asset_path: Path) -> bool:
        """فحص ما إذا كان الأصل مستخدماً في الكود"""
        asset_name = asset_path.name
        
        # البحث في جميع ملفات Python
        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if asset_name in content or str(asset_path) in content:
                        return True
            except:
                continue
        
        return False
    
    def _can_delete_file(self, file_path: Path) -> bool:
        """تحديد ما إذا كان يمكن حذف الملف بأمان"""
        # لا تحذف الملفات الأساسية
        if file_path.name in self.core_files:
            return False
        
        # لا تحذف الملفات المستخدمة
        if file_path in self.used_files:
            return False
        
        # لا تحذف ملفات قاعدة البيانات
        if file_path.suffix in ['.db', '.sqlite', '.sql']:
            return False
        
        return True
    
    def _get_directory_size(self, directory: Path) -> float:
        """حساب حجم المجلد بالميجابايت"""
        total_size = 0
        try:
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except:
            pass
        return total_size / (1024 * 1024)
    
    def _generate_recommendations(self):
        """إنشاء التوصيات"""
        recommendations = []
        
        # حساب المساحة المحتملة للتوفير
        total_savings_mb = 0
        
        # النسخ الاحتياطية
        backup_size = sum(dir_info["size_mb"] for dir_info in self.analysis_report["backup_analysis"]["backup_directories"])
        if backup_size > 100:  # أكثر من 100 ميجابايت
            recommendations.append({
                "priority": "HIGH",
                "category": "backup_cleanup",
                "description": f"حذف النسخ الاحتياطية القديمة - توفير {backup_size:.1f} ميجابايت",
                "action": "delete_old_backups",
                "savings_mb": backup_size
            })
            total_savings_mb += backup_size
        
        # ملفات الكاش
        cache_files = len(self.analysis_report["files_to_delete"].get("cache_files", []))
        if cache_files > 0:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "cache_cleanup", 
                "description": f"حذف ملفات الكاش ({cache_files} ملف)",
                "action": "delete_cache_files",
                "savings_mb": 5  # تقدير
            })
            total_savings_mb += 5
        
        # ملفات الاختبار
        test_files = len(self.analysis_report["files_to_delete"].get("test_files", []))
        if test_files > 5:
            recommendations.append({
                "priority": "LOW",
                "category": "test_cleanup",
                "description": f"حذف ملفات الاختبار القديمة ({test_files} ملف)",
                "action": "delete_old_tests",
                "savings_mb": 2
            })
            total_savings_mb += 2
        
        self.analysis_report["recommendations"] = recommendations
        self.analysis_report["total_potential_savings_mb"] = total_savings_mb

def main():
    """تشغيل التحليل الشامل"""
    analyzer = ComprehensiveFileCleanupAnalyzer()
    
    print("🚀 بدء التحليل الشامل لتنظيف الملفات...")
    report = analyzer.analyze_project()
    
    # حفظ التقرير
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"comprehensive_cleanup_analysis_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم حفظ تقرير التحليل في: {report_file}")
    
    # طباعة ملخص
    print("\n" + "="*60)
    print("📊 ملخص التحليل")
    print("="*60)
    print(f"📁 إجمالي الملفات المحللة: {report['total_files_analyzed']}")
    print(f"💾 المساحة المحتملة للتوفير: {report.get('total_potential_savings_mb', 0):.1f} ميجابايت")
    print(f"🗂️ عدد التوصيات: {len(report['recommendations'])}")
    
    # طباعة التوصيات
    if report['recommendations']:
        print("\n🎯 التوصيات الرئيسية:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. [{rec['priority']}] {rec['description']}")

if __name__ == "__main__":
    main()
