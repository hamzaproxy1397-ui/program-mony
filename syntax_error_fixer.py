#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة إصلاح الأخطاء النحوية السريعة
Quick Syntax Error Fixer
"""

import ast
import re
from pathlib import Path
from typing import List, Dict

class SyntaxErrorFixer:
    """مصلح الأخطاء النحوية السريع"""

    def __init__(self):
        self.project_root = Path(".")
        self.fixed_files = []
        self.errors = []

    def fix_common_syntax_errors(self, file_path: Path) -> bool:
        """إصلاح الأخطاء النحوية الشائعة"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # إصلاح الاستيرادات المكررة
            content = self.fix_duplicate_imports(content)

            # إصلاح المسافات البادئة
            content = self.fix_indentation_issues(content)

            # إصلاح try/except blocks غير المكتملة
            content = self.fix_incomplete_try_blocks(content)

            # إصلاح الأقواس غير المتطابقة
            content = self.fix_unmatched_brackets(content)

            # إصلاح الفواصل المفقودة
            content = self.fix_missing_commas(content)

            # إذا تم تغيير المحتوى، احفظه
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"✅ تم إصلاح: {file_path.name}")
                return True

            return False

        except Exception as e:
            error_msg = f"خطأ في إصلاح {file_path}: {e}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False

    def fix_duplicate_imports(self, content: str) -> str:
        """إصلاح الاستيرادات المكررة"""
        lines = content.split('\n')
        seen_imports = set()
        new_lines = []

        for line in lines:
            stripped = line.strip()

            # إذا كان السطر استيراد
            if (stripped.startswith('from ') and 'import' in stripped) or stripped.startswith('import '):
                if stripped not in seen_imports:
                    seen_imports.add(stripped)
                    new_lines.append(line)
                # تجاهل الاستيرادات المكررة
            else:
                new_lines.append(line)

        return '\n'.join(new_lines)

    def fix_indentation_issues(self, content: str) -> str:
        """إصلاح مشاكل المسافات البادئة البسيطة"""
        lines = content.split('\n')
        new_lines = []

        for i, line in enumerate(lines):
            # إصلاح المسافات المختلطة (tabs و spaces)
            if '\t' in line and '    ' in line:
                # تحويل جميع tabs إلى 4 spaces
                line = line.replace('\t', '    ')

            new_lines.append(line)

        return '\n'.join(new_lines)

    def fix_incomplete_try_blocks(self, content: str) -> str:
        """إصلاح try blocks غير المكتملة"""
        lines = content.split('\n')
        new_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            new_lines.append(line)

            # إذا وجدنا try block
            if line.strip().endswith('try:'):
                # ابحث عن except أو finally
                j = i + 1
                found_except_or_finally = False

                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line.startswith('except') or next_line.startswith('finally'):
                        found_except_or_finally = True
                        break
                    elif next_line and not next_line.startswith(' ') and not next_line.startswith('\t'):
                        # وصلنا لكود جديد بدون except/finally
                        break
                    j += 1

                # إذا لم نجد except أو finally، أضف except عام
                if not found_except_or_finally and j < len(lines):
                    # أضف except عام قبل السطر التالي
                    indent = '    ' if not line.startswith(' ') else '        '
                    new_lines.append(f"{indent}pass")
                    new_lines.append(f"except Exception as e:")
                    new_lines.append(f"{indent}print(f'خطأ: {{e}}')")

            i += 1

        return '\n'.join(new_lines)

    def fix_unmatched_brackets(self, content: str) -> str:
        """إصلاح الأقواس غير المتطابقة (إصلاح بسيط)"""
        # عد الأقواس
        open_parens = content.count('(')
        close_parens = content.count(')')
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        open_braces = content.count('{')
        close_braces = content.count('}')

        # إضافة الأقواس المفقودة في نهاية الملف (حل بسيط)
        if open_parens > close_parens:
            content += ')' * (open_parens - close_parens)
        elif close_parens > open_parens:
            content = '(' * (close_parens - open_parens) + content

        if open_brackets > close_brackets:
            content += ']' * (open_brackets - close_brackets)
        elif close_brackets > open_brackets:
            content = '[' * (close_brackets - open_brackets) + content

        if open_braces > close_braces:
            content += '}' * (open_braces - close_braces)
        elif close_braces > open_braces:
            content = '{' * (close_braces - open_braces) + content

        return content

    def fix_missing_commas(self, content: str) -> str:
        """إصلاح الفواصل المفقودة في القوائم"""
        # إصلاح بسيط للفواصل المفقودة في نهاية الأسطر
        lines = content.split('\n')
        new_lines = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            # إذا كان السطر ينتهي بقيمة وليس بفاصلة والسطر التالي يبدأ بقيمة
            if (i < len(lines) - 1 and 
                stripped and 
                not stripped.endswith(',') and 
                not stripped.endswith(':') and
                not stripped.endswith('{') and
                not stripped.endswith('[') and
                lines[i + 1].strip().startswith('"')):

                line += ','

            new_lines.append(line)

        return '\n'.join(new_lines)

    def validate_syntax(self, file_path: Path) -> bool:
        """التحقق من صحة النحو"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            ast.parse(content)
            return True

        except SyntaxError:
            return False
        except Exception:
            return False

    def fix_files_with_syntax_errors(self):
        """إصلاح الملفات التي بها أخطاء نحوية"""
        print("🔧 بدء إصلاح الأخطاء النحوية...")

        # قائمة الملفات التي بها مشاكل (من التحليل السابق)
        problematic_files = [
            "ui/backup_restore.py",
            "ui/categories_management_window.py", 
            "ui/comprehensive_income_window.py",
            "ui/daily_journal_window.py",
            # "ui/employees_window_fixed.py",  # تم تعطيله مؤقتاً
            "ui/inventory_window.py",
            "ui/pos_simple.py",
            "ui/pos_window.py",
            "ui/sales_analysis_window.py",
            "ui/stock_management_window.py",
            "ui/structured_profit_loss_window.py",
            "ui/treasury_window.py",
            "ui/units_management_window.py",
            "ui/warehouses_management_window.py",
            "ui/warehouse_management_window.py",
            "ui/welcome_window.py"
        ]

        fixed_count = 0

        for file_path_str in problematic_files:
            file_path = Path(file_path_str)

            if not file_path.exists():
                print(f"⚠️ الملف غير موجود: {file_path}")
                continue

            # فحص النحو قبل الإصلاح
            if self.validate_syntax(file_path):
                print(f"✅ {file_path.name}: لا يحتاج إصلاح")
                continue

            # محاولة الإصلاح
            if self.fix_common_syntax_errors(file_path):
                # فحص النحو بعد الإصلاح
                if self.validate_syntax(file_path):
                    print(f"✅ {file_path.name}: تم الإصلاح بنجاح")
                    fixed_count += 1
                    self.fixed_files.append(str(file_path))
                else:
                    print(f"⚠️ {file_path.name}: تم الإصلاح جزئياً")
            else:
                print(f"❌ {file_path.name}: فشل في الإصلاح")

        print(f"\n📊 النتائج:")
        print(f"   🔧 ملفات تم إصلاحها: {fixed_count}")
        print(f"   ❌ أخطاء حدثت: {len(self.errors)}")

        if self.errors:
            print(f"\n⚠️ الأخطاء:")
            for error in self.errors:
                print(f"   - {error}")

        return fixed_count

def main():
    """الدالة الرئيسية"""
    fixer = SyntaxErrorFixer()
    fixed_count = fixer.fix_files_with_syntax_errors()

    print(f"\n🎉 تم الانتهاء من إصلاح الأخطاء النحوية!")
    print(f"📊 إجمالي الملفات المصلحة: {fixed_count}")

if __name__ == "__main__":
    main()
