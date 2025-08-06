#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة إصلاح عميقة واحترافية لمشاكل الاستيرادات
Deep Professional Import Fixer
"""

import os
import re
import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import traceback
from typing import Any
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class DeepImportFixer:
    """مصلح الاستيرادات العميق والاحترافي"""

    def __init__(self):
        self.project_root = Path(".")
        self.python_files = []
        self.import_issues = []
        self.fixed_files = []
        self.errors = []

        # خريطة الاستيرادات المطلوبة
        self.required_imports = {
            'List': 'from typing import List',
            'Dict': 'from typing import Dict', 
            'Optional': 'from typing import Optional',
            'Tuple': 'from typing import Tuple',
            'Any': 'from typing import Any',
            'Union': 'from typing import Union',
            'Callable': 'from typing import Callable',
            'Enum': 'from enum import Enum',
            'Path': 'from pathlib import Path',
            'datetime': 'from datetime import datetime',
            'date': 'from datetime import date',
            'timedelta': 'from datetime import timedelta',
        }

        # أنماط الاستخدام
        self.usage_patterns = {
            'List': [r'\bList\[', r':\s*List\b', r'->\s*List\b'],
            'Dict': [r'\bDict\[', r':\s*Dict\b', r'->\s*Dict\b'],
            'Optional': [r'\bOptional\[', r':\s*Optional\b', r'->\s*Optional\b'],
            'Tuple': [r'\bTuple\[', r':\s*Tuple\b', r'->\s*Tuple\b'],
            'Any': [r'\bAny\b', r':\s*Any\b', r'->\s*Any\b'],
            'Union': [r'\bUnion\[', r':\s*Union\b', r'->\s*Union\b'],
            'Callable': [r'\bCallable\[', r':\s*Callable\b', r'->\s*Callable\b'],
            'Enum': [r'class\s+\w+\(Enum\)', r':\s*Enum\b'],
            'Path': [r'\bPath\(', r':\s*Path\b', r'->\s*Path\b'],
            'datetime': [r'\bdatetime\.(now|today|strptime)', r':\s*datetime\b'],
            'date': [r'\bdate\.(today|fromordinal)', r':\s*date\b'],
            'timedelta': [r'\btimedelta\(', r':\s*timedelta\b'],
        }

    def scan_python_files(self):
        """فحص جميع ملفات Python"""
        print("🔍 فحص ملفات Python في المشروع...")

        for file_path in self.project_root.rglob("*.py"):
            # تجاهل ملفات معينة
            if any(skip in str(file_path) for skip in ["__pycache__", ".git", "venv", "env"]):
                continue

            self.python_files.append(file_path)

        print(f"📊 تم العثور على {len(self.python_files)} ملف Python")

    def analyze_file(self, file_path: Path) -> Dict:
        """تحليل ملف واحد للبحث عن مشاكل الاستيرادات"""
        analysis = {
            'file': str(file_path),
            'existing_imports': set(),
            'missing_imports': set(),
            'used_types': set(),
            'syntax_errors': [],
            'content': ''
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            analysis['content'] = content

            # البحث عن الاستيرادات الموجودة
            import_lines = re.findall(r'^(from\s+[\w.]+\s+import\s+[^#\n]+|import\s+[^#\n]+)', content, re.MULTILINE)

            for import_line in import_lines:
                # استخراج الأسماء المستوردة
                if 'from' in import_line and 'import' in import_line:
                    parts = import_line.split('import', 1)
                    if len(parts) == 2:
                        imported_names = [name.strip() for name in parts[1].split(',')]
                        for name in imported_names:
                            # إزالة الأسماء المستعارة
                            clean_name = name.split(' as ')[0].strip()
                            analysis['existing_imports'].add(clean_name)
                elif import_line.startswith('import'):
                    module_name = import_line.replace('import', '').strip().split()[0]
                    analysis['existing_imports'].add(module_name)

            # البحث عن الأنواع المستخدمة
            for type_name, patterns in self.usage_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content):
                        analysis['used_types'].add(type_name)

            # تحديد الاستيرادات المفقودة
            for used_type in analysis['used_types']:
                if used_type not in analysis['existing_imports']:
                    analysis['missing_imports'].add(used_type)

            # فحص الأخطاء النحوية
            try:
                ast.parse(content)
            except SyntaxError as e:
                analysis['syntax_errors'].append(str(e))

        except Exception as e:
            analysis['syntax_errors'].append(f"خطأ في قراءة الملف: {e}")

        return analysis

    def fix_file_imports(self, analysis: Dict) -> bool:
        """إصلاح استيرادات ملف واحد"""
        if not analysis['missing_imports']:
            return True

        file_path = Path(analysis['file'])
        content = analysis['content']
        lines = content.split('\n')

        # العثور على موقع إدراج الاستيرادات
        insert_position = self.find_import_position(lines)

        # إنشاء الاستيرادات المطلوبة
        new_imports = []
        for missing_type in analysis['missing_imports']:
            if missing_type in self.required_imports:
                import_statement = self.required_imports[missing_type]
                new_imports.append(import_statement)

        # إدراج الاستيرادات الجديدة
        if new_imports:
            # إزالة التكرارات وترتيب الاستيرادات
            unique_imports = list(set(new_imports))
            unique_imports.sort()

            # إدراج الاستيرادات في الموقع المناسب
            for i, import_line in enumerate(unique_imports):
                lines.insert(insert_position + i, import_line)

            # كتابة الملف المحدث
            try:
                new_content = '\n'.join(lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"✅ تم إصلاح: {file_path.name}")
                print(f"   📦 أضيف: {', '.join(unique_imports)}")

                return True

            except Exception as e:
                error_msg = f"خطأ في كتابة {file_path}: {e}"
                print(f"❌ {error_msg}")
                self.errors.append(error_msg)
                return False

        return True

    def find_import_position(self, lines: List[str]) -> int:
        """العثور على الموقع المناسب لإدراج الاستيرادات"""
        # البحث عن آخر استيراد موجود
        last_import_line = -1

        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped.startswith('import ') or 
                stripped.startswith('from ') or
                stripped.startswith('#') and 'coding' in stripped):
                last_import_line = i

        # إذا لم نجد استيرادات، ابحث عن نهاية التعليقات الأولية
        if last_import_line == -1:
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                    return i

        return last_import_line + 1

    def valHidate_fix(self, file_path: Path) -> bool:
        """التحقق من صحة الإصلاح"""
        try:
            # محاولة استيراد الملف
            spec = None
            module_name = str(file_path).replace('/', '.').replace('\\', '.').replace('.py', '')

            # إزالة المسار النسبي
            if module_name.startswith('.'):
                module_name = module_name[1:]

            # محاولة تحليل الملف نحوياً
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            ast.parse(content)
            return True

        except Exception as e:
            print(f"⚠️ تحذير: مشكلة في التحقق من {file_path}: {e}")
            return False

    def run_deep_fix(self):
        """تشغيل الإصلاح العميق"""
        print("🔧 بدء الإصلاح العميق والاحترافي للاستيرادات")
        print("=" * 60)

        # فحص الملفات
        self.scan_python_files()

        # تحليل كل ملف
        print(f"\n📋 تحليل {len(self.python_files)} ملف...")

        files_with_issues = []

        for file_path in self.python_files:
            analysis = self.analyze_file(file_path)

            if analysis['missing_imports'] or analysis['syntax_errors']:
                files_with_issues.append(analysis)

                if analysis['missing_imports']:
                    print(f"⚠️ {file_path.name}: استيرادات مفقودة: {', '.join(analysis['missing_imports'])}")

                if analysis['syntax_errors']:
                    print(f"❌ {file_path.name}: أخطاء نحوية: {len(analysis['syntax_errors'])}")

        print(f"\n📊 ملخص التحليل:")
        print(f"   📁 ملفات تم فحصها: {len(self.python_files)}")
        print(f"   ⚠️ ملفات بها مشاكل: {len(files_with_issues)}")

        # إصلاح الملفات
        if files_with_issues:
            print(f"\n🔧 بدء إصلاح {len(files_with_issues)} ملف...")

            fixed_count = 0
            for analysis in files_with_issues:
                if analysis['missing_imports']:
                    if self.fix_file_imports(analysis):
                        fixed_count += 1
                        self.fixed_files.append(analysis['file'])

            print(f"\n✅ تم إصلاح {fixed_count} ملف بنجاح")

            # التحقق من الإصلاحات
            print(f"\n🔍 التحقق من الإصلاحات...")
            validation_passed = 0

            for file_path_str in self.fixed_files:
                file_path = Path(file_path_str)
                if self.validate_fix(file_path):
                    validation_passed += 1

            print(f"✅ تم التحقق من {validation_passed} ملف بنجاح")

        else:
            print("✅ لا توجد مشاكل في الاستيرادات!")

        # عرض الأخطاء إن وجدت
        if self.errors:
            print(f"\n⚠️ أخطاء حدثت أثناء الإصلاح:")
            for error in self.errors:
                print(f"   - {error}")

        print(f"\n🎉 تم الانتهاء من الإصلاح العميق!")

        return len(files_with_issues), len(self.fixed_files)

def main():
    """الدالة الرئيسية"""
    fixer = DeepImportFixer()
    issues_found, files_fixed = fixer.run_deep_fix()

    print(f"\n📊 النتائج النهائية:")
    print(f"   🔍 مشاكل تم اكتشافها: {issues_found}")
    print(f"   🔧 ملفات تم إصلاحها: {files_fixed}")

    if files_fixed > 0:
        print(f"\n💡 يُنصح بإعادة تشغيل البرنامج للتأكد من عمله بشكل صحيح")

if __name__ == "__main__":
    main()
