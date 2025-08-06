#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مصلح الأخطاء النحوية المتقدم
Advanced Syntax Error Fixer
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Tuple
import json

class AdvancedSyntaxFixer:
    """مصلح الأخطاء النحوية المتقدم"""

    def __init__(self):
        self.project_root = Path(".")
        self.fixed_files = []
        self.errors = []

        # قراءة تقرير الأخطاء
        self.error_report = self.load_error_report()

    def load_error_report(self):
        """تحميل تقرير الأخطاء"""
        try:
            report_files = list(self.project_root.glob("deep_error_analysis_report_*.json"))
            if report_files:
                latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
                with open(latest_report, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ لا يمكن تحميل تقرير الأخطاء: {e}")

        return {"syntax_errors": []}

    def fix_incomplete_try_blocks(self, file_path: Path, content: str) -> str:
        """إصلاح try blocks غير المكتملة"""
        lines = content.split('\n')
        new_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # إذا وجدنا try:
            if stripped == 'try:':
                new_lines.append(line)
                indent = len(line) - len(line.lstrip())

                # البحث عن المحتوى والـ except/finally
                j = i + 1
                has_content = False
                has_except_or_finally = False

                while j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.strip()

                    if not next_stripped:  # سطر فارغ
                        new_lines.append(next_line)
                        j += 1
                        continue

                    next_indent = len(next_line) - len(next_line.lstrip())

                    # إذا كان المحتوى داخل try
                    if next_indent > indent:
                        has_content = True
                        new_lines.append(next_line)
                    # إذا وجدنا except أو finally
                    elif next_stripped.startswith(('except', 'finally')) and next_indent == indent:
                        has_except_or_finally = True
                        new_lines.append(next_line)
                        break
                    # إذا وصلنا لكود جديد بنفس المستوى أو أقل
                    elif next_indent <= indent:
                        break
                    else:
                        new_lines.append(next_line)

                    j += 1

                # إذا لم يكن هناك محتوى، أضف pass
                if not has_content:
                    new_lines.append(' ' * (indent + 4) + 'pass')

                # إذا لم يكن هناك except أو finally، أضف except عام
                if not has_except_or_finally:
                    new_lines.append(' ' * indent + 'except Exception as e:')
                    new_lines.append(' ' * (indent + 4) + 'print(f"خطأ: {e}")')

                i = j - 1
            else:
                new_lines.append(line)

            i += 1

        return '\n'.join(new_lines)

    def fix_indentation_errors(self, file_path: Path, content: str) -> str:
        """إصلاح أخطاء المسافات البادئة"""
        lines = content.split('\n')
        new_lines = []

        for i, line in enumerate(lines):
            # تحويل tabs إلى spaces
            if '\t' in line:
                line = line.replace('\t', '    ')

            # إصلاح المسافات البادئة غير المتسقة
            if line.strip():
                # حساب المسافة البادئة الحالية
                indent = len(line) - len(line.lstrip())

                # التأكد من أن المسافة البادئة مضاعف 4
                if indent % 4 != 0:
                    correct_indent = (indent // 4) * 4
                    if indent % 4 >= 2:
                        correct_indent += 4

                    line = ' ' * correct_indent + line.lstrip()

            new_lines.append(line)

        return '\n'.join(new_lines)

    def fix_missing_colons(self, file_path: Path, content: str) -> str:
        """إصلاح النقطتين المفقودة"""
        lines = content.split('\n')
        new_lines = []

        for line in lines:
            stripped = line.strip()

            # إضافة : للكلمات المفتاحية التي تحتاجها
            keywords_need_colon = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'def', 'class', 'with']

            for keyword in keywords_need_colon:
                pattern = rf'\b{keyword}\b.*[^:]$'
                if re.match(pattern, stripped) and not stripped.endswith(':'):
                    # تأكد أنه ليس تعليق أو string
                    if not stripped.startswith('#') and not stripped.startswith(('"""', "'''")):
                        line = line.rstrip() + ':'
                        break

            new_lines.append(line)

        return '\n'.join(new_lines)

    def fix_escape_sequences(self, file_path: Path, content: str) -> str:
        """إصلاح escape sequences غير صحيحة"""
        # إصلاح \\S و \\M وغيرها من escape sequences غير صحيحة
        content = re.sub(r'\\\([SM])', r'\\\\\\1', content)

        # إصلاح مسارات Windows
        content = re.sub(r'\\\(?![nrtbfav\\\'"0-7xuUN])', r'\\\\', content)

        return content

    def fix_file_syntax_errors(self, file_path: Path) -> bool:
        """إصلاح أخطاء ملف واحد"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # تطبيق الإصلاحات
            content = self.fix_incomplete_try_blocks(file_path, content)
            content = self.fix_indentation_errors(file_path, content)
            content = self.fix_missing_colons(file_path, content)
            content = self.fix_escape_sequences(file_path, content)

            # التحقق من صحة النحو بعد الإصلاح
            try:
                ast.parse(content)
                syntax_valid = True
            except SyntaxError:
                syntax_valid = False

            # إذا تم تحسين الكود أو إصلاح النحو، احفظه
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                status = "✅ تم الإصلاح" if syntax_valid else "⚠️ تم التحسين جزئياً"
                print(f"{status}: {file_path.name}")
                return True

            return False

        except Exception as e:
            error_msg = f"خطأ في إصلاح {file_path}: {e}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False

    def fix_all_syntax_errors(self):
        """إصلاح جميع الأخطاء النحوية"""
        print("🔧 بدء إصلاح الأخطاء النحوية المتقدم...")

        syntax_errors = self.error_report.get("syntax_errors", [])

        if not syntax_errors:
            print("✅ لا توجد أخطاء نحوية للإصلاح")
            return 0

        print(f"📊 تم العثور على {len(syntax_errors)} خطأ نحوي")

        # تجميع الملفات التي تحتاج إصلاح
        files_to_fix = set()
        for error in syntax_errors:
            file_path = Path(error["file"])
            if file_path.exists():
                files_to_fix.add(file_path)

        print(f"📁 ملفات تحتاج إصلاح: {len(files_to_fix)}")

        # إصلاح كل ملف
        fixed_count = 0
        for file_path in files_to_fix:
            if self.fix_file_syntax_errors(file_path):
                fixed_count += 1
                self.fixed_files.append(str(file_path))

        print(f"\n📊 النتائج:")
        print(f"   🔧 ملفات تم إصلاحها: {fixed_count}")
        print(f"   ❌ أخطاء حدثت: {len(self.errors)}")

        if self.errors:
            print(f"\n⚠️ الأخطاء:")
            for error in self.errors:
                print(f"   - {error}")

        return fixed_count

    def validate_fixes(self):
        """التحقق من صحة الإصلاحات"""
        print(f"\n🔍 التحقق من صحة الإصلاحات...")

        valid_count = 0
        for file_path_str in self.fixed_files:
            file_path = Path(file_path_str)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                ast.parse(content)
                valid_count += 1
                print(f"   ✅ {file_path.name}: صحيح نحوياً")

            except SyntaxError as e:
                print(f"   ⚠️ {file_path.name}: لا يزال به خطأ نحوي - {e}")
            except Exception as e:
                print(f"   ❌ {file_path.name}: خطأ في التحقق - {e}")

        print(f"\n📊 نتائج التحقق:")
        print(f"   ✅ ملفات صحيحة: {valid_count}")
        print(f"   ⚠️ ملفات تحتاج مراجعة: {len(self.fixed_files) - valid_count}")

        return valid_count

def main():
    """الدالة الرئيسية"""
    fixer = AdvancedSyntaxFixer()

    # إصلاح الأخطاء
    fixed_count = fixer.fix_all_syntax_errors()

    # التحقق من الإصلاحات
    if fixed_count > 0:
        valid_count = fixer.validate_fixes()

        print(f"\n🎉 تم الانتهاء من إصلاح الأخطاء النحوية!")
        print(f"📊 إجمالي الملفات المصلحة: {fixed_count}")
        print(f"✅ ملفات صحيحة نحوياً: {valid_count}")

        success_rate = (valid_count / fixed_count) * 100 if fixed_count > 0 else 0
        print(f"📈 معدل النجاح: {success_rate:.1f}%")
    else:
        print(f"\n✅ لا توجد أخطاء نحوية تحتاج إصلاح")

if __name__ == "__main__":
    main()
