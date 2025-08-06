#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مصلح الأخطاء النحوية الدقيق والمتخصص
Precise Syntax Error Fixer
"""

import ast
import re
from pathlib import Path
from datetime import datetime
import shutil

class PreciseSyntaxFixer:
    """مصلح الأخطاء النحوية الدقيق"""

    def __init__(self):
        self.project_root = Path(".")
        self.backup_dir = Path("backup_precise")
        self.backup_dir.mkdir(exist_ok=True)

        self.fixed_files = []
        self.failed_fixes = []

    def fix_specific_files(self):
        """إصلاح ملفات محددة بدقة"""
        print("🔧 بدء الإصلاح الدقيق للأخطاء النحوية...")
        print("=" * 60)

        # الملفات الحرجة التي تحتاج إصلاح فوري
        critical_files = [
            "ui/main_window.py",
            "ui/pos_window.py", 
            "ui/pos_simple.py",
            "ui/sales_analysis_window.py"
        ]

        for file_path in critical_files:
            self.fix_file_precisely(file_path)

        return len(self.fixed_files)

    def fix_file_precisely(self, file_path: str):
        """إصلاح ملف محدد بدقة"""
        full_path = self.project_root / file_path

        if not full_path.exists():
            print(f"⚠️  الملف غير موجود: {file_path}")
            return

        print(f"🔍 إصلاح: {file_path}")

        try:
            # قراءة المحتوى
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # محاولة تحليل الملف
            try:
                ast.parse(content)
                print(f"✅ {file_path} - لا توجد أخطاء نحوية")
                return
            except SyntaxError as e:
                print(f"❌ خطأ نحوي في {file_path}: السطر {e.lineno} - {e.msg}")

                # إنشاء نسخة احتياطية
                self.create_backup(full_path)

                # إصلاح الخطأ المحدد
                fixed_content = self.fix_syntax_error_precisely(content, e, file_path)

                if fixed_content != content:
                    # حفظ المحتوى المصلح
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)

                    # التحقق من الإصلاح
                    try:
                        ast.parse(fixed_content)
                        print(f"✅ تم إصلاح {file_path}")
                        self.fixed_files.append(file_path)
                    except SyntaxError as new_error:
                        print(f"❌ فشل في إصلاح {file_path}: {new_error.msg}")
                        self.failed_fixes.append(file_path)
                        # استعادة النسخة الأصلية
                        self.restore_backup(full_path)
                else:
                    print(f"⚠️  لم يتم العثور على إصلاح مناسب لـ {file_path}")
                    self.failed_fixes.append(file_path)

        except Exception as e:
            print(f"❌ خطأ في معالجة {file_path}: {e}")
            self.failed_fixes.append(file_path)

    def fix_syntax_error_precisely(self, content: str, error: SyntaxError, file_path: str) -> str:
        """إصلاح خطأ نحوي بدقة حسب نوع الخطأ"""
        lines = content.split('\n')

        if not error.lineno or error.lineno > len(lines):
            return content

        error_line_idx = error.lineno - 1
        error_line = lines[error_line_idx]

        print(f"   السطر المشكل: {error_line.strip()}")

        # إصلاحات محددة حسب نوع الخطأ
        if "expected an indented block" in error.msg:
            return self.fix_indentation_error(lines, error_line_idx)

        elif "invalid syntax" in error.msg:
            return self.fix_invalid_syntax(lines, error_line_idx, error)

        elif "unexpected EOF" in error.msg:
            return self.fix_unexpected_eof(lines)

        elif "unmatched" in error.msg:
            return self.fix_unmatched_brackets(lines, error_line_idx)

        return content

    def fix_indentation_error(self, lines: list, error_idx: int) -> str:
        """إصلاح أخطاء المسافات البادئة"""
        # البحث عن السطر السابق الذي يحتاج مسافة بادئة
        for i in range(error_idx - 1, -1, -1):
            line = lines[i].strip()
            if line.endswith(':'):
                # إضافة سطر pass إذا كان السطر التالي فارغ أو غير مبدوء بمسافة
                if error_idx < len(lines):
                    next_line = lines[error_idx]
                    if not next_line.strip() or not next_line.startswith('    '):
                        # حساب المسافة البادئة المطلوبة
                        indent = self.get_indent_level(lines[i]) + 4
                        lines.insert(error_idx, ' ' * indent + 'pass')
                        break

        return '\n'.join(lines)

    def fix_invalid_syntax(self, lines: list, error_idx: int, error: SyntaxError) -> str:
        """إصلاح الأخطاء النحوية العامة"""
        error_line = lines[error_idx]

        # إصلاح الأقواس غير المكتملة
        if error.offset:
            char_at_error = error_line[error.offset - 1] if error.offset <= len(error_line) else ''

            # إصلاح الأقواس المفتوحة
            if '(' in error_line and ')' not in error_line:
                lines[error_idx] = error_line + ')'
            elif '[' in error_line and ']' not in error_line:
                lines[error_idx] = error_line + ']'
            elif '{' in error_line and '}' not in error_line:
                lines[error_idx] = error_line + '}'

            # إصلاح النقطتين المفقودتين
            elif error_line.strip().startswith(('if ', 'for ', 'while ', 'def ', 'class ', 'try', 'except', 'else', 'elif')):
                if not error_line.rstrip().endswith(':'):
                    lines[error_idx] = error_line.rstrip() + ':'

        return '\n'.join(lines)

    def fix_unexpected_eof(self, lines: list) -> str:
        """إصلاح نهاية الملف غير المتوقعة"""
        # البحث عن الأقواس أو البلوكات غير المكتملة
        open_brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []

        for i, line in enumerate(lines):
            for char in line:
                if char in open_brackets:
                    stack.append((char, i))
                elif char in open_brackets.values():
                    if stack and open_brackets[stack[-1][0]] == char:
                        stack.pop()

        # إغلاق الأقواس المفتوحة
        for bracket, line_idx in reversed(stack):
            lines.append(open_brackets[bracket])

        return '\n'.join(lines)

    def fix_unmatched_brackets(self, lines: list, error_idx: int) -> str:
        """إصلاح الأقواس غير المتطابقة"""
        error_line = lines[error_idx]

        # عد الأقواس في السطر
        open_parens = error_line.count('(')
        close_parens = error_line.count(')')

        if open_parens > close_parens:
            lines[error_idx] = error_line + ')' * (open_parens - close_parens)
        elif close_parens > open_parens:
            lines[error_idx] = '(' * (close_parens - open_parens) + error_line

        return '\n'.join(lines)

    def get_indent_level(self, line: str) -> int:
        """حساب مستوى المسافة البادئة"""
        return len(line) - len(line.lstrip())

    def create_backup(self, file_path: Path):
        """إنشاء نسخة احتياطية"""
        backup_path = self.backup_dir / f"{file_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"   💾 تم إنشاء نسخة احتياطية: {backup_path.name}")

    def restore_backup(self, file_path: Path):
        """استعادة النسخة الاحتياطية"""
        backup_files = list(self.backup_dir.glob(f"{file_path.name}.backup_*"))
        if backup_files:
            latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
            shutil.copy2(latest_backup, file_path)
            print(f"   🔄 تم استعادة النسخة الاحتياطية")

def main():
    """تشغيل المصلح الدقيق"""
    fixer = PreciseSyntaxFixer()
    fixed_count = fixer.fix_specific_files()

    print("\n" + "="*60)
    print("📊 ملخص الإصلاح الدقيق:")
    print(f"   ✅ ملفات تم إصلاحها: {len(fixer.fixed_files)}")
    print(f"   ❌ ملفات فشل إصلاحها: {len(fixer.failed_fixes)}")

    if fixer.fixed_files:
        print("   📋 الملفات المصلحة:")
        for file in fixer.fixed_files:
            print(f"      • {file}")

    if fixer.failed_fixes:
        print("   ⚠️  الملفات التي تحتاج مراجعة يدوية:")
        for file in fixer.failed_fixes:
            print(f"      • {file}")

    print("="*60)

if __name__ == "__main__":
    main()
