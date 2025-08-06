#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة التنظيف النهائية للنظام
Final System Cleanup Tool
"""

import re
import ast
from pathlib import Path
from datetime import datetime
import shutil

class FinalCleanupTool:
    """أداة التنظيف النهائية للنظام"""

    def __init__(self):
        self.project_root = Path(".")
        self.backup_dir = Path("backup_final")
        self.backup_dir.mkdir(exist_ok=True)

        self.fixed_files = []
        self.patterns_fixed = []

    def run_final_cleanup(self):
        """تشغيل التنظيف النهائي"""
        print("🧹 بدء التنظيف النهائي للنظام...")
        print("=" * 60)

        # البحث عن الأنماط المشكلة وإصلاحها
        self.fix_duplicate_if_patterns()
        self.fix_indentation_issues()
        self.fix_incomplete_blocks()

        # التحقق النهائي
        self.final_verification()

        return len(self.fixed_files)

    def fix_duplicate_if_patterns(self):
        """إصلاح الأنماط المكررة للـ if statements"""
        print("\n🔧 إصلاح الأنماط المكررة...")

        # البحث في جميع ملفات Python
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # إصلاح النمط المكرر الشائع
                pattern1 = r'(\s+)if window and hasattr\(window, "destroy"\):\s*\n\s+if window and hasattr\(window, "destroy"\):\s*\n\s+window\.destroy\(\)'
                replacement1 = r'\1if window and hasattr(window, "destroy"):\n\1    window.destroy()'
                content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE)

                # إصلاح النمط المكرر الآخر
                pattern2 = r'(\s+)if (\w+) and hasattr\(\2, "destroy"\):\s*\n\s+if \2 and hasattr\(\2, "destroy"\):\s*\n\s+\2\.destroy\(\)'
                replacement2 = r'\1if \2 and hasattr(\2, "destroy"):\n\1    \2.destroy()'
                content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)

                # إصلاح الأسطر المكررة العامة
                pattern3 = r'(\s+)(if .+:\s*\n)\s+\2'
                replacement3 = r'\1\2'
                content = re.sub(pattern3, replacement3, content, flags=re.MULTILINE)

                if content != original_content:
                    self.create_backup(py_file)

                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print(f"   ✅ تم إصلاح الأنماط المكررة في {py_file.name}")
                    self.fixed_files.append(str(py_file))
                    self.patterns_fixed.append("duplicate_if_patterns")

            except Exception as e:
                print(f"   ❌ خطأ في معالجة {py_file}: {e}")

    def fix_indentation_issues(self):
        """إصلاح مشاكل المسافات البادئة"""
        print("\n🔧 إصلاح مشاكل المسافات البادئة...")

        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                original_lines = lines.copy()
                fixed = False

                for i, line in enumerate(lines):
                    # إصلاح الأسطر التي تبدأ بمسافات خاطئة
                    if re.match(r'^    \w+$', line.rstrip()):
                        # سطر يحتوي على كلمة واحدة فقط مع مسافة بادئة - قد يكون خطأ
                        if i > 0 and not lines[i-1].strip().endswith(':'):
                            lines[i] = line.lstrip() + '\n'
                            fixed = True

                    # إصلاح الأسطر الفارغة مع مسافات
                    elif re.match(r'^\s+$', line):
                        lines[i] = '\n'
                        fixed = True

                if fixed:
                    self.create_backup(py_file)

                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    print(f"   ✅ تم إصلاح المسافات البادئة في {py_file.name}")
                    if str(py_file) not in self.fixed_files:
                        self.fixed_files.append(str(py_file))
                    self.patterns_fixed.append("indentation_issues")

            except Exception as e:
                print(f"   ❌ خطأ في معالجة {py_file}: {e}")

    def fix_incomplete_blocks(self):
        """إصلاح البلوكات غير المكتملة"""
        print("\n🔧 إصلاح البلوكات غير المكتملة...")

        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # محاولة تحليل الملف
                try:
                    ast.parse(content)
                    continue  # الملف سليم
                except SyntaxError as e:
                    if "expected an indented block" in str(e):
                        lines = content.split('\n')

                        if e.lineno and e.lineno <= len(lines):
                            # البحث عن السطر الذي يحتاج مسافة بادئة
                            for i in range(e.lineno - 2, max(0, e.lineno - 6), -1):
                                if lines[i].strip().endswith(':'):
                                    # حساب المسافة البادئة المطلوبة
                                    base_indent = len(lines[i]) - len(lines[i].lstrip())
                                    required_indent = base_indent + 4

                                    # إضافة pass
                                    lines.insert(e.lineno - 1, ' ' * required_indent + 'pass')

                                    # حفظ الملف
                                    self.create_backup(py_file)

                                    with open(py_file, 'w', encoding='utf-8') as f:
                                        f.write('\n'.join(lines))

                                    print(f"   ✅ تم إصلاح البلوك غير المكتمل في {py_file.name}")
                                    if str(py_file) not in self.fixed_files:
                                        self.fixed_files.append(str(py_file))
                                    self.patterns_fixed.append("incomplete_blocks")
                                    break

            except Exception as e:
                print(f"   ❌ خطأ في معالجة {py_file}: {e}")

    def final_verification(self):
        """التحقق النهائي من جميع الملفات"""
        print("\n✅ التحقق النهائي...")

        passed = 0
        failed = 0
        critical_files = ["main.py", "ui/main_window.py", "ui/pos_window.py", "ui/pos_simple.py"]

        for file_path in critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                    print(f"   ✅ {file_path} - سليم")
                    passed += 1
                except SyntaxError as e:
                    print(f"   ❌ {file_path} - خطأ: {e.msg} (السطر {e.lineno})")
                    failed += 1
                except Exception as e:
                    print(f"   ❌ {file_path} - خطأ: {e}")
                    failed += 1

        print(f"\n📊 نتائج التحقق النهائي:")
        print(f"   ✅ ملفات سليمة: {passed}")
        print(f"   ❌ ملفات بها أخطاء: {failed}")

        return passed, failed

    def create_backup(self, file_path: Path):
        """إنشاء نسخة احتياطية"""
        backup_path = self.backup_dir / f"{file_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)

    def generate_report(self):
        """إنشاء تقرير التنظيف"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "files_fixed": len(self.fixed_files),
            "patterns_fixed": list(set(self.patterns_fixed)),
            "fixed_files_list": self.fixed_files
        }

        report_file = f"final_cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            import json
import json
json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n📄 تم حفظ تقرير التنظيف في: {report_file}")

        print("\n" + "="*60)
        print("🎯 ملخص التنظيف النهائي:")
        print(f"   📁 ملفات تم إصلاحها: {len(self.fixed_files)}")
        print(f"   🔧 أنماط تم إصلاحها: {len(set(self.patterns_fixed))}")
        print("="*60)

def main():
    """تشغيل أداة التنظيف النهائية"""
    tool = FinalCleanupTool()
    fixed_count = tool.run_final_cleanup()
    tool.generate_report()

    if fixed_count > 0:
        print(f"\n🎉 تم تنظيف وإصلاح {fixed_count} ملف!")
        print("🔍 يُنصح بإجراء اختبار شامل الآن")
    else:
        print("\n✅ النظام نظيف ولا يحتاج إصلاحات إضافية")

if __name__ == "__main__":
    main()
