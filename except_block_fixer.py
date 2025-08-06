#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مصلح except blocks المتخصص
Specialized Except Block Fixer
"""

import ast
from pathlib import Path
from typing import List

class ExceptBlockFixer:
    """مصلح except blocks المتخصص"""

    def __init__(self):
        self.project_root = Path(".")
        self.fixed_files = []

    def fix_except_blocks_in_file(self, file_path: Path) -> bool:
        """إصلاح except blocks في ملف واحد"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            new_lines = []
            i = 0
            fixed = False

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

                        # حساب المسافة البادئة المطلوبة
                        current_indent = len(line) - len(line.lstrip())
                        expected_indent = current_indent + 4

                        # إذا كان السطر التالي فارغ أو بدء كود جديد بنفس المستوى أو أقل
                        if (not next_stripped or 
                            (next_stripped and len(next_line) - len(next_line.lstrip()) <= current_indent)):
                            # إضافة pass
                            new_lines.append(' ' * expected_indent + 'pass')
                            fixed = True
                            print(f"   ✅ أضيف pass بعد except في السطر {i + 1}")
                else:
                    new_lines.append(line)

                i += 1

            # حفظ الملف إذا تم إصلاحه
            if fixed:
                # إنشاء نسخة احتياطية
                backup_path = file_path.with_suffix(f"{file_path.suffix}.except_backup")
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # حفظ الملف المصلح
                new_content = '\n'.join(new_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                # التحقق من صحة النحو
                try:
                    ast.parse(new_content)
                    print(f"   ✅ {file_path.name}: تم الإصلاح بنجاح")
                    return True
                except SyntaxError as e:
                    print(f"   ⚠️ {file_path.name}: لا يزال به خطأ نحوي - {e}")
                    return True  # تم الإصلاح جزئياً
            else:
                print(f"   ✅ {file_path.name}: لا يحتاج إصلاح")
                return False

        except Exception as e:
            print(f"   ❌ خطأ في إصلاح {file_path.name}: {e}")
            return False

    def fix_all_except_blocks(self):
        """إصلاح جميع except blocks في المشروع"""
        print("🔧 مصلح except blocks المتخصص")
        print("=" * 50)

        # البحث عن جميع ملفات Python
        python_files = list(self.project_root.rglob("*.py"))
        python_files = [f for f in python_files if not any(skip in str(f) for skip in ["__pycache__", ".git", "venv"])]

        print(f"📊 تم العثور على {len(python_files)} ملف Python")

        fixed_count = 0

        for file_path in python_files:
            print(f"\n🔍 فحص: {file_path.name}")

            if self.fix_except_blocks_in_file(file_path):
                fixed_count += 1
                self.fixed_files.append(str(file_path))

        print(f"\n📊 النتائج:")
        print(f"   🔧 ملفات تم إصلاحها: {fixed_count}")
        print(f"   📁 إجمالي الملفات: {len(python_files)}")

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

                try:
                    ast.parse(content)
                    valid_count += 1
                    print(f"   ✅ {file_path.name}: صحيح نحوياً")
                except SyntaxError as e:
                    print(f"   ⚠️ {file_path.name}: خطأ نحوي - السطر {e.lineno}: {e.msg}")

            except Exception as e:
                print(f"   ❌ {file_path.name}: خطأ في القراءة - {e}")

        print(f"\n📊 نتائج التحقق:")
        print(f"   ✅ ملفات صحيحة: {valid_count}")
        print(f"   ⚠️ ملفات تحتاج مراجعة: {len(self.fixed_files) - valid_count}")

        return valid_count

def main():
    """الدالة الرئيسية"""
    fixer = ExceptBlockFixer()

    # إصلاح جميع except blocks
    fixed_count = fixer.fix_all_except_blocks()

    # التحقق من الإصلاحات
    if fixed_count > 0:
        valid_count = fixer.validate_fixes()

        print(f"\n🎉 تم الانتهاء من إصلاح except blocks!")
        print(f"📊 إجمالي الملفات المصلحة: {fixed_count}")
        print(f"✅ ملفات صحيحة نحوياً: {valid_count}")

        success_rate = (valid_count / fixed_count) * 100 if fixed_count > 0 else 0
        print(f"📈 معدل النجاح: {success_rate:.1f}%")
    else:
        print("✅ جميع except blocks صحيحة!")

if __name__ == "__main__":
    main()
