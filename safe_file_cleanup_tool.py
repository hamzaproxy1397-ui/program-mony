#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة التنظيف الآمنة للملفات غير الضرورية
Safe File Cleanup Tool
"""

import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import argparse

class SafeFileCleanupTool:
    def __init__(self, dry_run=True):
        self.project_root = Path(".")
        self.dry_run = dry_run
        self.backup_created = False
        self.cleanup_log = []
        
        # الملفات والمجلدات المحمية (يجب عدم حذفها أبداً)
        self.protected_files = {
            "main.py", "START_HERE.py", "large_font_run.py", "requirements.txt", 
            "LICENSE", "README.md", "setup.py", "run.py", "launch_app.py"
        }
        
        self.protected_directories = {
            "ui", "database", "core", "auth", "config", "themes", "services", 
            "models", "reports", "assets"
        }
        
        # قواعد التنظيف حسب الأولوية
        self.cleanup_rules = {
            "phase1_backup_dirs": {
                "priority": "HIGH",
                "safety": "SAFE",
                "patterns": [
                    "backup_critical_files", "backup_deep", "backup_final", 
                    "backup_fixes", "backup_precise", "backup_systematic",
                    "backup_ultimate", "backup_ultimate_advanced",
                    "COMPLETE_SYSTEM_BACKUP_20250725_185838"
                ],
                "description": "حذف مجلدات النسخ الاحتياطية القديمة"
            },
            "phase2_cache_files": {
                "priority": "HIGH", 
                "safety": "SAFE",
                "patterns": ["__pycache__", "*.pyc", "*.pyo", "*.pyd"],
                "description": "حذف ملفات الكاش"
            },
            "phase3_old_reports": {
                "priority": "MEDIUM",
                "safety": "SAFE", 
                "patterns": [
                    "*_report_*.json", "*_audit_*.json", "*_analysis_*.json",
                    "comprehensive_system_report_*.json", "deep_*_report_*.json"
                ],
                "description": "حذف التقارير القديمة"
            },
            "phase4_temp_tools": {
                "priority": "MEDIUM",
                "safety": "MODERATE",
                "patterns": [
                    "*_fixer.py", "*_analyzer.py", "*_checker.py", 
                    "comprehensive_*_fixer.py", "ultimate_*_fixer.py",
                    "temp_*.py", "search_temp.py"
                ],
                "description": "حذف الأدوات المؤقتة"
            },
            "phase5_test_files": {
                "priority": "LOW",
                "safety": "MODERATE",
                "patterns": [
                    "test_*.py", "*_test.py", "comprehensive_validation_test.py"
                ],
                "description": "حذف ملفات الاختبار القديمة",
                "exclude": ["test_main_window.py", "test_database.py"]  # اختبارات مهمة
            },
            "phase6_duplicate_docs": {
                "priority": "LOW",
                "safety": "MODERATE", 
                "patterns": [
                    "*_README.md", "*_GUIDE.md", "*_REPORT.md",
                    "FINAL_*.md", "COMPREHENSIVE_*.md"
                ],
                "description": "حذف ملفات التوثيق المكررة",
                "exclude": ["README.md", "USER_GUIDE.md"]  # توثيق أساسي
            }
        }
    
    def create_safety_backup(self) -> bool:
        """إنشاء نسخة احتياطية آمنة قبل التنظيف"""
        if self.dry_run:
            print("🔍 [وضع المحاكاة] سيتم إنشاء نسخة احتياطية آمنة")
            return True
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"SAFETY_BACKUP_BEFORE_CLEANUP_{timestamp}.zip"
            
            print(f"💾 إنشاء نسخة احتياطية آمنة: {backup_name}")
            
            with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # نسخ احتياطية للملفات المهمة فقط
                important_files = []
                
                # ملفات Python الأساسية
                for py_file in self.project_root.rglob("*.py"):
                    if any(protected in str(py_file) for protected in self.protected_directories):
                        important_files.append(py_file)
                
                # ملفات التكوين
                for config_file in self.project_root.rglob("*.json"):
                    if "config" in str(config_file) or "settings" in str(config_file):
                        important_files.append(config_file)
                
                # قاعدة البيانات
                for db_file in self.project_root.rglob("*.db"):
                    important_files.append(db_file)
                
                for file_path in important_files:
                    if file_path.is_file():
                        arcname = str(file_path.relative_to(self.project_root))
                        zipf.write(file_path, arcname)
            
            self.backup_created = True
            print(f"✅ تم إنشاء النسخة الاحتياطية: {backup_name}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False
    
    def is_file_protected(self, file_path: Path) -> bool:
        """فحص ما إذا كان الملف محمياً"""
        # فحص الملفات المحمية بالاسم
        if file_path.name in self.protected_files:
            return True
        
        # فحص المجلدات المحمية
        for protected_dir in self.protected_directories:
            if protected_dir in file_path.parts:
                return True
        
        # فحص ملفات قاعدة البيانات الحية
        if file_path.suffix in ['.db', '.sqlite'] and 'backup' not in str(file_path):
            return True
        
        # فحص ملفات التكوين النشطة
        if 'config' in str(file_path) and file_path.suffix in ['.py', '.json']:
            return True
        
        return False
    
    def cleanup_phase(self, phase_name: str, rules: Dict) -> Dict:
        """تنفيذ مرحلة تنظيف محددة"""
        print(f"\n🧹 المرحلة: {phase_name}")
        print(f"📝 الوصف: {rules['description']}")
        print(f"⚡ الأولوية: {rules['priority']} | 🛡️ الأمان: {rules['safety']}")
        
        phase_results = {
            "files_processed": 0,
            "files_deleted": 0,
            "space_freed_mb": 0,
            "errors": []
        }
        
        for pattern in rules['patterns']:
            try:
                matches = list(self.project_root.rglob(pattern))
                
                for match in matches:
                    # تجاهل الملفات المحمية
                    if self.is_file_protected(match):
                        continue
                    
                    # تجاهل الملفات المستثناة
                    if 'exclude' in rules:
                        if any(exclude in str(match) for exclude in rules['exclude']):
                            continue
                    
                    phase_results["files_processed"] += 1
                    
                    try:
                        # حساب حجم الملف/المجلد
                        if match.is_file():
                            size_mb = match.stat().st_size / (1024 * 1024)
                        else:
                            size_mb = self._get_directory_size(match)
                        
                        if self.dry_run:
                            print(f"🔍 [محاكاة] سيتم حذف: {match} ({size_mb:.2f} MB)")
                        else:
                            if match.is_file():
                                match.unlink()
                                print(f"🗑️ تم حذف الملف: {match}")
                            else:
                                shutil.rmtree(match)
                                print(f"🗑️ تم حذف المجلد: {match}")
                        
                        phase_results["files_deleted"] += 1
                        phase_results["space_freed_mb"] += size_mb
                        
                        # تسجيل العملية
                        self.cleanup_log.append({
                            "timestamp": datetime.now().isoformat(),
                            "action": "DELETE",
                            "path": str(match),
                            "size_mb": size_mb,
                            "phase": phase_name
                        })
                        
                    except Exception as e:
                        error_msg = f"خطأ في حذف {match}: {e}"
                        phase_results["errors"].append(error_msg)
                        print(f"❌ {error_msg}")
                        
            except Exception as e:
                error_msg = f"خطأ في معالجة النمط {pattern}: {e}"
                phase_results["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        return phase_results
    
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
    
    def run_cleanup(self, phases: List[str] = None) -> Dict:
        """تشغيل عملية التنظيف"""
        print("🚀 بدء عملية التنظيف الآمنة للملفات")
        print(f"📁 مجلد المشروع: {self.project_root.absolute()}")
        print(f"🔧 وضع التشغيل: {'محاكاة' if self.dry_run else 'تنفيذ فعلي'}")
        
        # إنشاء نسخة احتياطية
        if not self.create_safety_backup():
            print("❌ فشل في إنشاء النسخة الاحتياطية - توقف التنظيف")
            return {"status": "failed", "reason": "backup_failed"}
        
        # تحديد المراحل المطلوبة
        if phases is None:
            phases = list(self.cleanup_rules.keys())
        
        total_results = {
            "start_time": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "phases_executed": [],
            "total_files_processed": 0,
            "total_files_deleted": 0,
            "total_space_freed_mb": 0,
            "total_errors": 0
        }
        
        # تنفيذ المراحل
        for phase_name in phases:
            if phase_name in self.cleanup_rules:
                rules = self.cleanup_rules[phase_name]
                phase_results = self.cleanup_phase(phase_name, rules)
                
                total_results["phases_executed"].append({
                    "phase": phase_name,
                    "results": phase_results
                })
                
                total_results["total_files_processed"] += phase_results["files_processed"]
                total_results["total_files_deleted"] += phase_results["files_deleted"]
                total_results["total_space_freed_mb"] += phase_results["space_freed_mb"]
                total_results["total_errors"] += len(phase_results["errors"])
        
        total_results["end_time"] = datetime.now().isoformat()
        
        # حفظ سجل التنظيف
        self._save_cleanup_log(total_results)
        
        # طباعة الملخص
        self._print_summary(total_results)
        
        return total_results
    
    def _save_cleanup_log(self, results: Dict):
        """حفظ سجل عملية التنظيف"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f"cleanup_log_{timestamp}.json"
        
        log_data = {
            "cleanup_results": results,
            "detailed_log": self.cleanup_log,
            "protected_files": list(self.protected_files),
            "protected_directories": list(self.protected_directories)
        }
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            print(f"📝 تم حفظ سجل التنظيف: {log_file}")
        except Exception as e:
            print(f"❌ خطأ في حفظ السجل: {e}")
    
    def _print_summary(self, results: Dict):
        """طباعة ملخص النتائج"""
        print("\n" + "="*60)
        print("📊 ملخص عملية التنظيف")
        print("="*60)
        print(f"📁 الملفات المعالجة: {results['total_files_processed']}")
        print(f"🗑️ الملفات المحذوفة: {results['total_files_deleted']}")
        print(f"💾 المساحة المحررة: {results['total_space_freed_mb']:.2f} ميجابايت")
        print(f"❌ الأخطاء: {results['total_errors']}")
        print(f"⏱️ وقت التنفيذ: {results['start_time']} - {results['end_time']}")
        
        if self.dry_run:
            print("\n🔍 هذا كان وضع المحاكاة - لم يتم حذف أي ملفات فعلياً")
            print("💡 لتنفيذ التنظيف الفعلي، استخدم: --execute")

def main():
    parser = argparse.ArgumentParser(description="أداة التنظيف الآمنة للملفات")
    parser.add_argument("--execute", action="store_true", 
                       help="تنفيذ التنظيف الفعلي (افتراضياً: وضع المحاكاة)")
    parser.add_argument("--phases", nargs="+", 
                       help="المراحل المطلوب تنفيذها (افتراضياً: جميع المراحل)")
    
    args = parser.parse_args()
    
    # إنشاء أداة التنظيف
    cleanup_tool = SafeFileCleanupTool(dry_run=not args.execute)
    
    # تشغيل التنظيف
    results = cleanup_tool.run_cleanup(phases=args.phases)
    
    if results.get("status") == "failed":
        exit(1)

if __name__ == "__main__":
    main()
