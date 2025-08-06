#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مصلح الملفات الحرجة - إصلاح يدوي متقدم
Critical File Fixer - Advanced Manual Repair
"""

import ast
from pathlib import Path
from typing import List, Dict
import re

class CriticalFileFixer:
    """مصلح الملفات الحرجة"""

    def __init__(self):
        self.project_root = Path(".")
        self.fixed_files = []

        # الملفات الحرجة التي يجب إصلاحها أولاً
        self.critical_files = [
            "ui/comprehensive_income_window.py",
            "ui/daily_journal_window.py", 
            "ui/stock_management_window.py",
            "ui/inventory_window.py",
            "ui/categories_management_window.py",
            "ui/treasury_window.py",
            "ui/sales_analysis_window.py",
            "ui/backup_restore.py"
        ]

    def fix_comprehensive_income_window(self):
        """إصلاح ملف comprehensive_income_window.py"""
        file_path = Path("ui/comprehensive_income_window.py")
        if not file_path.exists():
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # إصلاح الأخطاء الشائعة
            lines = content.split('\n')
            new_lines = []

            for i, line in enumerate(lines):
                # إصلاح السطر 18 - مشكلة في النحو
                if i == 17:  # السطر 18 (index 17)
                    if 'invalid syntax' in line or line.strip().startswith('"""'):
                        # إصلاح docstring غير مكتمل
                        if '"""' in line and line.count('"""') == 1:
                            line = line + '"""'

                new_lines.append(line)

            # كتابة الملف المصلح
            fixed_content = '\n'.join(new_lines)

            # التحقق من صحة النحو
            try:
                ast.parse(fixed_content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ تم إصلاح: {file_path.name}")
                return True
            except SyntaxError:
                print(f"⚠️ {file_path.name}: يحتاج إصلاح يدوي")
                return False

        except Exception as e:
            print(f"❌ خطأ في إصلاح {file_path.name}: {e}")
            return False

    def fix_except_blocks(self, file_path: Path):
        """إصلاح except blocks غير المكتملة"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            new_lines = []
            i = 0

            while i < len(lines):
                line = lines[i]
                stripped = line.strip()

                # إذا وجدنا except: بدون محتوى
                if stripped.startswith('except') and stripped.endswith(':'):
                    new_lines.append(line)

                    # التحقق من السطر التالي
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        next_stripped = next_line.strip()

                        # إذا كان السطر التالي فارغ أو بدء كود جديد
                        if not next_stripped or not next_line.startswith('    '):
                            # إضافة pass
                            indent = len(line) - len(line.lstrip()) + 4
                            new_lines.append(' ' * indent + 'pass')
                else:
                    new_lines.append(line)

                i += 1

            # كتابة الملف المصلح
            fixed_content = '\n'.join(new_lines)

            # التحقق من صحة النحو
            try:
                ast.parse(fixed_content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ تم إصلاح: {file_path.name}")
                return True
            except SyntaxError as e:
                print(f"⚠️ {file_path.name}: خطأ نحوي متبقي - {e}")
                return False

        except Exception as e:
            print(f"❌ خطأ في إصلاح {file_path.name}: {e}")
            return False

    def fix_indentation_issues(self, file_path: Path):
        """إصلاح مشاكل المسافات البادئة المعقدة"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            new_lines = []

            for line in lines:
                # تحويل tabs إلى spaces
                if '\t' in line:
                    line = line.replace('\t', '    ')

                # إصلاح المسافات البادئة غير المتسقة
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    # التأكد من أن المسافة البادئة مضاعف 4
                    if indent % 4 != 0:
                        correct_indent = ((indent + 3) // 4) * 4
                        line = ' ' * correct_indent + line.lstrip()

                new_lines.append(line)

            # كتابة الملف المصلح
            fixed_content = '\n'.join(new_lines)

            # التحقق من صحة النحو
            try:
                ast.parse(fixed_content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ تم إصلاح: {file_path.name}")
                return True
            except SyntaxError as e:
                print(f"⚠️ {file_path.name}: خطأ نحوي متبقي - {e}")
                return False

        except Exception as e:
            print(f"❌ خطأ في إصلاح {file_path.name}: {e}")
            return False

    def fix_invalid_syntax(self, file_path: Path):
        """إصلاح أخطاء النحو العامة"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # إصلاحات عامة
            lines = content.split('\n')
            new_lines = []

            for line in lines:
                # إصلاح docstrings غير مكتملة
                if '"""' in line and line.count('"""') == 1:
                    if line.strip().startswith('"""'):
                        line = line + '"""'

                # إصلاح أقواس غير متطابقة
                open_parens = line.count('(')
                close_parens = line.count(')')
                if open_parens > close_parens:
                    line = line + ')' * (open_parens - close_parens)

                new_lines.append(line)

            # كتابة الملف المصلح
            fixed_content = '\n'.join(new_lines)

            # التحقق من صحة النحو
            try:
                ast.parse(fixed_content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ تم إصلاح: {file_path.name}")
                return True
            except SyntaxError as e:
                print(f"⚠️ {file_path.name}: خطأ نحوي متبقي - {e}")
                return False

        except Exception as e:
            print(f"❌ خطأ في إصلاح {file_path.name}: {e}")
            return False

    def fix_critical_files(self):
        """إصلاح الملفات الحرجة"""
        print("🔧 بدء إصلاح الملفات الحرجة...")

        fixed_count = 0

        for file_path_str in self.critical_files:
            file_path = Path(file_path_str)

            if not file_path.exists():
                print(f"⚠️ الملف غير موجود: {file_path}")
                continue

            print(f"\n🔍 إصلاح: {file_path.name}")

            # تطبيق إصلاحات متعددة
            success = False

            # إصلاح except blocks
            if self.fix_except_blocks(file_path):
                success = True

            # إصلاح مشاكل المسافات البادئة
            if not success and self.fix_indentation_issues(file_path):
                success = True

            # إصلاح أخطاء النحو العامة
            if not success and self.fix_invalid_syntax(file_path):
                success = True

            if success:
                fixed_count += 1
                self.fixed_files.append(str(file_path))

        print(f"\n📊 النتائج:")
        print(f"   🔧 ملفات تم إصلاحها: {fixed_count}")
        print(f"   ⚠️ ملفات تحتاج مراجعة يدوية: {len(self.critical_files) - fixed_count}")

        return fixed_count

    def create_backup_files(self):
        """إنشاء نسخ احتياطية من الملفات الحرجة"""
        print("💾 إنشاء نسخ احتياطية...")

        backup_dir = Path("backup_critical_files")
        backup_dir.mkdir(exist_ok=True)

        for file_path_str in self.critical_files:
            file_path = Path(file_path_str)

            if file_path.exists():
                backup_path = backup_dir / f"{file_path.name}.backup"

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print(f"   💾 {file_path.name} -> {backup_path.name}")

                except Exception as e:
                    print(f"   ❌ خطأ في نسخ {file_path.name}: {e}")

def main():
    """الدالة الرئيسية"""
    fixer = CriticalFileFixer()

    # إنشاء نسخ احتياطية
    fixer.create_backup_files()

    # إصلاح الملفات الحرجة
    fixed_count = fixer.fix_critical_files()

    print(f"\n🎉 تم الانتهاء من إصلاح الملفات الحرجة!")
    print(f"📊 إجمالي الملفات المصلحة: {fixed_count}")

    if fixed_count > 0:
        print(f"\n💡 يُنصح بإعادة تشغيل التحليل العميق للتأكد من الإصلاحات")

if __name__ == "__main__":
    main()
