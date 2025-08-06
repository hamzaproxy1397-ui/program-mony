#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مصلح الأخطاء المتقدم والشامل
Advanced Comprehensive Error Fixer
"""

import ast
import re
import json
from pathlib import Path
from datetime import datetime
import shutil
import logging

class AdvancedErrorFixer:
    """مصلح الأخطاء المتقدم والشامل"""

    def __init__(self):
        self.project_root = Path(".")
        self.backup_dir = Path("backup_fixes")
        self.backup_dir.mkdir(exist_ok=True)

        self.fixed_files = []
        self.failed_fixes = []

        # إعداد نظام السجلات
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # قائمة الملفات التي بها أخطاء نحوية (من التقرير)
        self.problematic_files = [
            "comprehensive_income_formula_demo.py",
            "run_app.py", 
            "run_fixed_app.py",
            "safe_start.py",
            "start_with_scheduler.py",
            "config/postgresql_config.py",
            "core/app_core.py",
            "database/comprehensive_income_manager.py",
            "ui/backup_restore.py",
            "ui/daily_journal_window.py",
            "ui/pos_simple.py",
            "ui/pos_window.py",
            "ui/sales_analysis_window.py"
        ]

    def fix_all_errors(self):
        """إصلاح جميع الأخطاء المكتشفة"""
        print("🔧 بدء الإصلاح الشامل للأخطاء...")
        print("=" * 60)

        # 1. إصلاح الأخطاء النحوية
        self.fix_syntax_errors()

        # 2. إصلاح مشاكل الاستيراد
        self.fix_import_issues()

        # 3. إصلاح مشاكل واجهة المستخدم
        self.fix_ui_issues()

        # 4. إنشاء تقرير الإصلاح
        self.generate_fix_report()

        return len(self.fixed_files)

    def fix_syntax_errors(self):
        """إصلاح الأخطاء النحوية"""
        print("\n🔧 إصلاح الأخطاء النحوية...")

        for file_path in self.problematic_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                print(f"⚠️  الملف غير موجود: {file_path}")
                continue

            print(f"🔍 فحص: {file_path}")

            try:
                # إنشاء نسخة احتياطية
                self.create_backup(full_path)

                # قراءة المحتوى
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # محاولة تحليل الملف
                try:
                    ast.parse(content)
                    print(f"✅ {file_path} - لا توجد أخطاء نحوية")
                    continue
                except SyntaxError as e:
                    print(f"❌ خطأ نحوي في {file_path}: السطر {e.lineno}")

                    # محاولة إصلاح الخطأ
                    fixed_content = self.fix_specific_syntax_error(content, e)
                    if fixed_content != content:
                        # حفظ المحتوى المصلح
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)

                        # التحقق من الإصلاح
                        try:
                            ast.parse(fixed_content)
                            print(f"✅ تم إصلاح {file_path}")
                            self.fixed_files.append(str(file_path))
                        except SyntaxError:
                            print(f"❌ فشل في إصلاح {file_path}")
                            self.failed_fixes.append(str(file_path))
                            # استعادة النسخة الأصلية
                            self.restore_backup(full_path)
                    else:
                        print(f"⚠️  لم يتم العثور على إصلاح لـ {file_path}")
                        self.failed_fixes.append(str(file_path))

            except Exception as e:
                print(f"❌ خطأ في معالجة {file_path}: {e}")
                self.failed_fixes.append(str(file_path))

    def fix_specific_syntax_error(self, content: str, error: SyntaxError) -> str:
        """إصلاح خطأ نحوي محدد"""
        lines = content.split('\n')

        if error.lineno and error.lineno <= len(lines):
            error_line = lines[error.lineno - 1]

            # إصلاحات شائعة
            fixes = [
                # إصلاح except blocks غير مكتملة
                (r'^(\\s*)except\\s*:\\s*$', r'\1except Exception:\n\1    pass'),

                # إصلاح try blocks غير مكتملة
                (r'^(\\s*)try\\s*:\\s*$', r'\1try:'),

                # إصلاح الأقواس غير المتطابقة
                (r'\\(\\s*$', '()'),
                (r'\\[\\s*$', '[]'),
                (r'\\{\\s*$', '{}'),

                # إصلاح النقاط الفاصلة المفقودة
                (r'^(\\s*)(if|while|for|def|class)([^:]+)$', r'\1\2\3:'),

                # إصلاح escape sequences غير صحيحة
                (r'\\\([^\\\\nrtbfav\'"0-7xuUN])', r'\\\\\\1'),
            ]

            original_line = error_line
            for pattern, replacement in fixes:
                error_line = re.sub(pattern, replacement, error_line)

            if error_line != original_line:
                lines[error.lineno - 1] = error_line
                return '\n'.join(lines)

        return content

    def fix_import_issues(self):
        """إصلاح مشاكل الاستيراد"""
        print("\n📦 إصلاح مشاكل الاستيراد...")

        # البحث عن ملفات بها مشاكل استيراد
        ui_files = list((self.project_root / "ui").glob("*.py"))

        for file_path in ui_files:
            if ".except_backup" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # البحث عن مشاكل الاستيراد الشائعة
                fixed_content = self.fix_import_patterns(content)

                if fixed_content != content:
                    # إنشاء نسخة احتياطية
                    self.create_backup(file_path)

                    # حفظ المحتوى المصلح
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)

                    print(f"✅ تم إصلاح استيرادات {file_path.name}")
                    self.fixed_files.append(str(file_path))

            except Exception as e:
                print(f"❌ خطأ في إصلاح استيرادات {file_path}: {e}")

    def fix_import_patterns(self, content: str) -> str:
        """إصلاح أنماط الاستيراد الشائعة"""
        # إصلاح except ImportError بدون معالجة
        content = re.sub(
            r'except ImportError:\\s*pass',
            'except ImportError:\n    print("تحذير: فشل في استيراد المكتبة")',
            content
        )

        # إصلاح try/except blocks غير مكتملة للاستيرادات
        pattern = r'(try:\\s*\n\\s*from .+ import .+\\s*\n)except ImportError:\\s*$'
        replacement = r'\1except ImportError:\n    pass'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

        # إضافة استيرادات مفقودة شائعة
        if 'customtkinter' in content and 'import customtkinter as ctk' not in content:
            if 'import customtkinter' not in content:
                content = 'import customtkinter as ctk\n' + content

        if 'messagebox' in content and 'from tkinter import messagebox' not in content:
            content = 'from tkinter import messagebox\n' + content

        return content

    def fix_ui_issues(self):
        """إصلاح مشاكل واجهة المستخدم"""
        print("\n🖥️  إصلاح مشاكل واجهة المستخدم...")

        ui_files = list((self.project_root / "ui").glob("*.py"))

        for file_path in ui_files:
            if ".except_backup" in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                fixed_content = self.fix_ui_patterns(content)

                if fixed_content != content:
                    self.create_backup(file_path)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)

                    print(f"✅ تم إصلاح واجهة {file_path.name}")
                    if str(file_path) not in self.fixed_files:
                        self.fixed_files.append(str(file_path))

            except Exception as e:
                print(f"❌ خطأ في إصلاح واجهة {file_path}: {e}")

    def fix_ui_patterns(self, content: str) -> str:
        """إصلاح أنماط واجهة المستخدم الشائعة"""
        # إضافة معالجة أخطاء لـ after
        pattern = r'(\\w+\\.after\\(\\d+[^)]*\\))'
        def add_try_catch(match):
            return f'try:\n    {match.group(1)}\nexcept Exception:\n    pass'

        # إضافة فحص قبل destroy
        content = re.sub(
            r'(\\w+)\\.destroy\\(\\)',
            r'if \1 and hasattr(\1, "destroy"):\n    \1.destroy()',
            content
        )

        return content

    def create_backup(self, file_path: Path):
        """إنشاء نسخة احتياطية من الملف"""
        backup_path = self.backup_dir / f"{file_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)

    def restore_backup(self, file_path: Path):
        """استعادة النسخة الاحتياطية"""
        backup_files = list(self.backup_dir.glob(f"{file_path.name}.backup_*"))
        if backup_files:
            latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
            shutil.copy2(latest_backup, file_path)

    def generate_fix_report(self):
        """إنشاء تقرير الإصلاح"""
        print("\n📊 إنشاء تقرير الإصلاح...")

        report = {
            "timestamp": datetime.now().isoformat(),
            "fixed_files": self.fixed_files,
            "failed_fixes": self.failed_fixes,
            "total_files_processed": len(self.problematic_files),
            "success_rate": len(self.fixed_files) / len(self.problematic_files) * 100 if self.problematic_files else 0
        }

        report_file = f"error_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"📄 تم حفظ تقرير الإصلاح في: {report_file}")

        # طباعة ملخص
        print("\n" + "="*60)
        print("📊 ملخص الإصلاح:")
        print(f"   ✅ ملفات تم إصلاحها: {len(self.fixed_files)}")
        print(f"   ❌ ملفات فشل إصلاحها: {len(self.failed_fixes)}")
        print(f"   📊 معدل النجاح: {report['success_rate']:.1f}%")
        print("="*60)

def main():
    """تشغيل مصلح الأخطاء المتقدم"""
    fixer = AdvancedErrorFixer()
    fixed_count = fixer.fix_all_errors()

    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} ملف بنجاح!")
        print("💡 يُنصح بإجراء اختبار شامل للتأكد من عمل جميع الوحدات")
    else:
        print("\n⚠️  لم يتم إصلاح أي ملفات. قد تحتاج إلى مراجعة يدوية")

if __name__ == "__main__":
    main()
