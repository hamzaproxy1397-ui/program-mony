#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 أداة تنظيف المشروع الشاملة
Comprehensive Project Cleanup Tool

تقوم هذه الأداة بتنظيف الملفات المكررة والنسخ الاحتياطية القديمة
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set

class ProjectCleanupTool:
    """أداة تنظيف المشروع"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.cleanup_report = {
            "timestamp": datetime.now().isoformat(),
            "files_removed": [],
            "directories_removed": [],
            "space_freed": 0,
            "duplicate_files_removed": [],
            "old_backups_removed": [],
            "temp_files_removed": []
        }
        
        # أنماط الملفات المؤقتة
        self.temp_patterns = [
            "*.pyc", "*.pyo", "*.pyd", "__pycache__",
            "*.tmp", "*.temp", "*.log~", "*.bak",
            ".DS_Store", "Thumbs.db", "*.swp", "*.swo"
        ]
        
        # أنماط النسخ الاحتياطية القديمة
        self.backup_patterns = [
            "*.backup", "*.backup_*", "*.except_backup",
            "*_backup_*", "backup_*", "*_backup"
        ]
        
        # مجلدات النسخ الاحتياطية الكبيرة
        self.large_backup_dirs = [
            "COMPLETE_SYSTEM_BACKUP_*",
            "backup_deep", "backup_final", "backup_fixes",
            "backup_precise", "backup_systematic", 
            "backup_ultimate", "backup_ultimate_advanced"
        ]

    def run_cleanup(self):
        """تشغيل عملية التنظيف الشاملة"""
        print("🧹 بدء تنظيف المشروع الشامل...")
        print("=" * 60)
        
        # 1. تنظيف الملفات المؤقتة
        self._clean_temp_files()
        
        # 2. تنظيف النسخ الاحتياطية القديمة
        self._clean_old_backups()
        
        # 3. إزالة الملفات المكررة
        self._remove_duplicate_files()
        
        # 4. تنظيف مجلدات النسخ الاحتياطية الكبيرة
        self._clean_large_backup_dirs()
        
        # 5. تنظيف ملفات السجلات القديمة
        self._clean_old_logs()
        
        # 6. حفظ التقرير
        self._save_cleanup_report()
        
        print(f"\n✅ تم الانتهاء من التنظيف!")
        print(f"📊 إجمالي الملفات المحذوفة: {len(self.cleanup_report['files_removed'])}")
        print(f"📁 إجمالي المجلدات المحذوفة: {len(self.cleanup_report['directories_removed'])}")

    def _clean_temp_files(self):
        """تنظيف الملفات المؤقتة"""
        print("\n🗑️ تنظيف الملفات المؤقتة...")
        
        for pattern in self.temp_patterns:
            for file_path in self.project_root.rglob(pattern):
                try:
                    if file_path.is_file():
                        size = file_path.stat().st_size
                        file_path.unlink()
                        self.cleanup_report["temp_files_removed"].append(str(file_path.relative_to(self.project_root)))
                        self.cleanup_report["files_removed"].append(str(file_path.relative_to(self.project_root)))
                        self.cleanup_report["space_freed"] += size
                        print(f"   🗑️ حذف: {file_path.relative_to(self.project_root)}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        self.cleanup_report["directories_removed"].append(str(file_path.relative_to(self.project_root)))
                        print(f"   🗑️ حذف مجلد: {file_path.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"   ⚠️ لا يمكن حذف {file_path}: {e}")

    def _clean_old_backups(self):
        """تنظيف النسخ الاحتياطية القديمة"""
        print("\n🗑️ تنظيف النسخ الاحتياطية القديمة...")
        
        # حذف الملفات الاحتياطية الأقدم من 30 يوم
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for pattern in self.backup_patterns:
            for backup_file in self.project_root.rglob(pattern):
                try:
                    if backup_file.is_file():
                        file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
                        if file_time < cutoff_date:
                            size = backup_file.stat().st_size
                            backup_file.unlink()
                            self.cleanup_report["old_backups_removed"].append(str(backup_file.relative_to(self.project_root)))
                            self.cleanup_report["files_removed"].append(str(backup_file.relative_to(self.project_root)))
                            self.cleanup_report["space_freed"] += size
                            print(f"   🗑️ حذف نسخة احتياطية قديمة: {backup_file.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"   ⚠️ لا يمكن حذف {backup_file}: {e}")

    def _remove_duplicate_files(self):
        """إزالة الملفات المكررة"""
        print("\n🔍 البحث عن الملفات المكررة...")
        
        file_hashes = {}
        duplicates_found = 0
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and not self._should_skip_file(file_path):
                try:
                    # حساب hash للملف
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash in file_hashes:
                        # ملف مكرر - احتفظ بالأصلي واحذف المكرر
                        original = file_hashes[file_hash]
                        
                        # اختر أي ملف نحذف (عادة الأحدث أو الذي في مجلد backup)
                        if "backup" in str(file_path).lower() or file_path.stat().st_mtime > original.stat().st_mtime:
                            duplicate_to_remove = file_path
                        else:
                            duplicate_to_remove = original
                            file_hashes[file_hash] = file_path
                        
                        try:
                            size = duplicate_to_remove.stat().st_size
                            duplicate_to_remove.unlink()
                            self.cleanup_report["duplicate_files_removed"].append({
                                "removed": str(duplicate_to_remove.relative_to(self.project_root)),
                                "kept": str(file_hashes[file_hash].relative_to(self.project_root))
                            })
                            self.cleanup_report["files_removed"].append(str(duplicate_to_remove.relative_to(self.project_root)))
                            self.cleanup_report["space_freed"] += size
                            duplicates_found += 1
                            print(f"   🔄 حذف ملف مكرر: {duplicate_to_remove.relative_to(self.project_root)}")
                        except Exception as e:
                            print(f"   ⚠️ لا يمكن حذف الملف المكرر {duplicate_to_remove}: {e}")
                    else:
                        file_hashes[file_hash] = file_path
                        
                except Exception:
                    continue
        
        print(f"   📊 تم العثور على {duplicates_found} ملف مكرر")

    def _clean_large_backup_dirs(self):
        """تنظيف مجلدات النسخ الاحتياطية الكبيرة"""
        print("\n🗑️ تنظيف مجلدات النسخ الاحتياطية الكبيرة...")
        
        for pattern in self.large_backup_dirs:
            for backup_dir in self.project_root.glob(pattern):
                if backup_dir.is_dir():
                    try:
                        # حساب حجم المجلد
                        total_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
                        
                        # إذا كان المجلد كبير (أكثر من 100 MB) واقدم من 7 أيام
                        if total_size > 100 * 1024 * 1024:  # 100 MB
                            dir_time = datetime.fromtimestamp(backup_dir.stat().st_mtime)
                            if datetime.now() - dir_time > timedelta(days=7):
                                print(f"   📁 مجلد نسخ احتياطية كبير: {backup_dir.name} ({total_size / (1024*1024):.1f} MB)")
                                
                                # اسأل المستخدم (في بيئة تفاعلية) أو احذف تلقائياً
                                # هنا سنحذف تلقائياً المجلدات الأقدم من 30 يوم
                                if datetime.now() - dir_time > timedelta(days=30):
                                    shutil.rmtree(backup_dir)
                                    self.cleanup_report["directories_removed"].append(str(backup_dir.relative_to(self.project_root)))
                                    self.cleanup_report["space_freed"] += total_size
                                    print(f"   🗑️ حذف مجلد نسخ احتياطية قديم: {backup_dir.relative_to(self.project_root)}")
                    except Exception as e:
                        print(f"   ⚠️ لا يمكن معالجة {backup_dir}: {e}")

    def _clean_old_logs(self):
        """تنظيف ملفات السجلات القديمة"""
        print("\n🗑️ تنظيف ملفات السجلات القديمة...")
        
        logs_dir = self.project_root / "logs"
        if logs_dir.exists():
            cutoff_date = datetime.now() - timedelta(days=30)
            
            for log_file in logs_dir.rglob("*.log"):
                try:
                    file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_time < cutoff_date and log_file.name != "app.log":  # احتفظ بالسجل الرئيسي
                        size = log_file.stat().st_size
                        log_file.unlink()
                        self.cleanup_report["files_removed"].append(str(log_file.relative_to(self.project_root)))
                        self.cleanup_report["space_freed"] += size
                        print(f"   🗑️ حذف سجل قديم: {log_file.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"   ⚠️ لا يمكن حذف {log_file}: {e}")

    def _should_skip_file(self, file_path: Path) -> bool:
        """تحديد ما إذا كان يجب تخطي الملف"""
        skip_patterns = [
            ".git", ".vscode", ".idea", "node_modules",
            "venv", "env", ".env"
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)

    def _save_cleanup_report(self):
        """حفظ تقرير التنظيف"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"project_cleanup_report_{timestamp}.json"
        
        # تحويل الحجم إلى وحدة مناسبة
        space_freed_mb = self.cleanup_report["space_freed"] / (1024 * 1024)
        self.cleanup_report["space_freed_mb"] = round(space_freed_mb, 2)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.cleanup_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ تقرير التنظيف في: {report_path}")
        print(f"💾 مساحة محررة: {space_freed_mb:.2f} MB")

def main():
    """الدالة الرئيسية"""
    print("🧹 أداة تنظيف المشروع الشاملة")
    print("=" * 50)
    
    # إنشاء أداة التنظيف
    cleanup_tool = ProjectCleanupTool()
    
    # تشغيل التنظيف
    cleanup_tool.run_cleanup()
    
    print("\n🎯 تم الانتهاء من تنظيف المشروع")
    print("💡 راجع تقرير التنظيف للتفاصيل")

if __name__ == "__main__":
    main()
