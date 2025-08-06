#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
المصلح النهائي والشامل للنظام
Ultimate System Fixer - الإصدار المحسن
"""

import ast
import re
import json
from pathlib import Path
from datetime import datetime
import shutil
import logging

class UltimateSystemFixer:
    """المصلح النهائي والشامل للنظام"""

    def __init__(self):
        self.project_root = Path(".")
        self.backup_dir = Path("backup_ultimate")
        self.backup_dir.mkdir(exist_ok=True)

        self.fixed_files = []
        self.failed_fixes = []
        self.critical_errors = []

        # إعداد نظام السجلات
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # قائمة الملفات الحرجة التي يجب إصلاحها أولاً
        self.critical_files = [
            "main.py",
            "ui/main_window.py",
            "ui/pos_window.py",
            "ui/pos_simple.py",
            "ui/sales_analysis_window.py",
            "database/hybrid_database_manager.py"
        ]

    def run_ultimate_fix(self):
        """تشغيل الإصلاح النهائي والشامل"""
        print("🚀 بدء الإصلاح النهائي والشامل للنظام...")
        print("=" * 70)

        # المرحلة 1: إصلاح الملفات الحرجة
        print("\n🎯 المرحلة 1: إصلاح الملفات الحرجة...")
        self.fix_critical_files()

        # المرحلة 2: إصلاح جميع ملفات UI
        print("\n🖥️  المرحلة 2: إصلاح ملفات واجهة المستخدم...")
        self.fix_all_ui_files()

        # المرحلة 3: إصلاح ملفات قاعدة البيانات
        print("\n🗄️  المرحلة 3: إصلاح ملفات قاعدة البيانات...")
        self.fix_database_files()

        # المرحلة 4: إصلاح الملفات المساعدة
        print("\n🔧 المرحلة 4: إصلاح الملفات المساعدة...")
        self.fix_helper_files()

        # المرحلة 5: التحقق النهائي
        print("\n✅ المرحلة 5: التحقق النهائي...")
        self.final_verification()

        # إنشاء التقرير النهائي
        self.generate_ultimate_report()

        return len(self.fixed_files)

    def fix_critical_files(self):
        """إصلاح الملفات الحرجة"""
        for file_path in self.critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"🔧 إصلاح حرج: {file_path}")
                self.fix_file_intelligently(full_path, is_critical=True)

    def fix_all_ui_files(self):
        """إصلاح جميع ملفات واجهة المستخدم"""
        ui_dir = self.project_root / "ui"
        if ui_dir.exists():
            for py_file in ui_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    print(f"🖥️  إصلاح UI: {py_file.name}")
                    self.fix_file_intelligently(py_file)

    def fix_database_files(self):
        """إصلاح ملفات قاعدة البيانات"""
        db_dir = self.project_root / "database"
        if db_dir.exists():
            for py_file in db_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    print(f"🗄️  إصلاح DB: {py_file.name}")
                    self.fix_file_intelligently(py_file)

    def fix_helper_files(self):
        """إصلاح الملفات المساعدة"""
        helper_files = [
            "run_app.py", "safe_start.py", "start_with_scheduler.py",
            "comprehensive_income_formula_demo.py"
        ]

        for file_name in helper_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                print(f"🔧 إصلاح مساعد: {file_name}")
                self.fix_file_intelligently(file_path)

    def fix_file_intelligently(self, file_path: Path, is_critical: bool = False):
        """إصلاح ملف بذكاء وتحليل متقدم"""
        try:
            # قراءة المحتوى
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # محاولة تحليل الملف
            try:
                ast.parse(original_content)
                print(f"   ✅ {file_path.name} - سليم")
                return True
            except SyntaxError as e:
                print(f"   ❌ خطأ في {file_path.name}: {e.msg} (السطر {e.lineno})")

                # إنشاء نسخة احتياطية
                self.create_backup(file_path)

                # تطبيق الإصلاحات المتقدمة
                fixed_content = self.apply_advanced_fixes(original_content, e, file_path)

                if fixed_content != original_content:
                    # حفظ المحتوى المصلح
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)

                    # التحقق من الإصلاح
                    try:
                        ast.parse(fixed_content)
                        print(f"   ✅ تم إصلاح {file_path.name}")
                        self.fixed_files.append(str(file_path))
                        return True
                    except SyntaxError as new_error:
                        print(f"   ❌ فشل إصلاح {file_path.name}: {new_error.msg}")
                        if is_critical:
                            self.critical_errors.append(str(file_path))
                        self.failed_fixes.append(str(file_path))
                        # استعادة النسخة الأصلية
                        self.restore_backup(file_path)
                        return False
                else:
                    print(f"   ⚠️  لا يمكن إصلاح {file_path.name} تلقائياً")
                    if is_critical:
                        self.critical_errors.append(str(file_path))
                    self.failed_fixes.append(str(file_path))
                    return False

        except Exception as e:
            print(f"   ❌ خطأ في معالجة {file_path.name}: {e}")
            self.failed_fixes.append(str(file_path))
            return False

    def apply_advanced_fixes(self, content: str, error: SyntaxError, file_path: Path) -> str:
        """تطبيق إصلاحات متقدمة وذكية"""
        lines = content.split('\n')

        if not error.lineno or error.lineno > len(lines):
            return content

        error_line_idx = error.lineno - 1
        error_line = lines[error_line_idx]

        # إصلاحات متقدمة حسب نوع الخطأ
        if "expected an indented block" in error.msg:
            return self.fix_indentation_advanced(lines, error_line_idx)

        elif "invalid syntax" in error.msg:
            return self.fix_invalid_syntax_advanced(lines, error_line_idx, error)

        elif "unexpected indent" in error.msg:
            return self.fix_unexpected_indent(lines, error_line_idx)

        elif "unexpected EOF" in error.msg:
            return self.fix_unexpected_eof_advanced(lines)

        elif "unmatched" in error.msg or "closing parenthesis" in error.msg:
            return self.fix_unmatched_brackets_advanced(lines, error_line_idx)

        elif "invalid escape sequence" in error.msg:
            return self.fix_escape_sequences(lines, error_line_idx)

        return content

    def fix_indentation_advanced(self, lines: list, error_idx: int) -> str:
        """إصلاح متقدم لأخطاء المسافات البادئة"""
        # البحث عن السطر الذي يحتاج مسافة بادئة
        for i in range(error_idx - 1, max(0, error_idx - 5), -1):
            line = lines[i].strip()
            if line.endswith(':') and not line.startswith('#'):
                # حساب المسافة البادئة المطلوبة
                base_indent = len(lines[i]) - len(lines[i].lstrip())
                required_indent = base_indent + 4

                # التحقق من السطر التالي
                if error_idx < len(lines):
                    next_line = lines[error_idx].strip()
                    if not next_line or not lines[error_idx].startswith(' ' * required_indent):
                        # إضافة pass مع المسافة البادئة الصحيحة
                        lines.insert(error_idx, ' ' * required_indent + 'pass')
                        break

        return '\n'.join(lines)

    def fix_invalid_syntax_advanced(self, lines: list, error_idx: int, error: SyntaxError) -> str:
        """إصلاح متقدم للأخطاء النحوية"""
        error_line = lines[error_idx]

        # إصلاح الأقواس غير المكتملة
        if '(' in error_line and error_line.count('(') > error_line.count(')'):
            lines[error_idx] = error_line + ')' * (error_line.count('(') - error_line.count(')'))

        elif '[' in error_line and error_line.count('[') > error_line.count(']'):
            lines[error_idx] = error_line + ']' * (error_line.count('[') - error_line.count(']'))

        elif '{' in error_line and error_line.count('{') > error_line.count('}'):
            lines[error_idx] = error_line + '}' * (error_line.count('{') - error_line.count('}'))

        # إصلاح النقطتين المفقودتين
        elif any(error_line.strip().startswith(kw) for kw in ['if ', 'for ', 'while ', 'def ', 'class ', 'try', 'except', 'else', 'elif']):
            if not error_line.rstrip().endswith(':'):
                lines[error_idx] = error_line.rstrip() + ':'

        # إصلاح الفواصل المفقودة
        elif 'invalid syntax' in error.msg and error.offset:
            # محاولة إضافة فاصلة إذا كانت مفقودة
            if error.offset < len(error_line) and error_line[error.offset - 1] not in ',;:':
                lines[error_idx] = error_line[:error.offset] + ',' + error_line[error.offset:]

        return '\n'.join(lines)

    def fix_unexpected_indent(self, lines: list, error_idx: int) -> str:
        """إصلاح المسافات البادئة غير المتوقعة"""
        if error_idx < len(lines):
            # إزالة المسافات البادئة الزائدة
            lines[error_idx] = lines[error_idx].lstrip()

            # إذا كان السطر فارغاً بعد إزالة المسافات، احذفه
            if not lines[error_idx].strip():
                lines.pop(error_idx)

        return '\n'.join(lines)

    def fix_unexpected_eof_advanced(self, lines: list) -> str:
        """إصلاح متقدم لنهاية الملف غير المتوقعة"""
        # إضافة أسطر فارغة إذا انتهى الملف فجأة
        if lines and not lines[-1].strip():
            return '\n'.join(lines)

        # البحث عن البلوكات غير المكتملة
        open_blocks = 0
        for line in lines:
            stripped = line.strip()
            if stripped.endswith(':') and not stripped.startswith('#'):
                open_blocks += 1
            elif stripped and not line.startswith(' ') and open_blocks > 0:
                open_blocks -= 1

        # إضافة pass للبلوكات المفتوحة
        for _ in range(open_blocks):
            lines.append('    pass')

        return '\n'.join(lines)

    def fix_unmatched_brackets_advanced(self, lines: list, error_idx: int) -> str:
        """إصلاح متقدم للأقواس غير المتطابقة"""
        # تحليل الأقواس في الملف كاملاً
        bracket_pairs = {'(': ')', '[': ']', '{': '}'}
        stack = []

        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char in bracket_pairs:
                    stack.append((char, i, j))
                elif char in bracket_pairs.values():
                    if stack:
                        open_bracket, _, _ = stack[-1]
                        if bracket_pairs[open_bracket] == char:
                            stack.pop()

        # إغلاق الأقواس المفتوحة
        for open_bracket, line_idx, _ in reversed(stack):
            if line_idx < len(lines):
                lines[line_idx] += bracket_pairs[open_bracket]

        return '\n'.join(lines)

    def fix_escape_sequences(self, lines: list, error_idx: int) -> str:
        """إصلاح تسلسلات الهروب غير الصحيحة"""
        if error_idx < len(lines):
            line = lines[error_idx]
            # إصلاح escape sequences شائعة
            line = re.sub(r'\\([^\\nrtbfav'"0-7xuUN])', r'\\\\1', line)"
            lines[error_idx] = line

        return '\n'.join(lines)

    def final_verification(self):
        """التحقق النهائي من جميع الملفات"""
        print("🔍 إجراء التحقق النهائي...")

        verification_results = {
            "passed": [],
            "failed": [],
            "critical_failed": []
        }

        # فحص الملفات الحرجة
        for file_path in self.critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                if self.verify_file_syntax(full_path):
                    verification_results["passed"].append(file_path)
                else:
                    verification_results["critical_failed"].append(file_path)

        # فحص ملفات UI
        ui_dir = self.project_root / "ui"
        if ui_dir.exists():
            for py_file in ui_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    if self.verify_file_syntax(py_file):
                        verification_results["passed"].append(str(py_file))
                    else:
                        verification_results["failed"].append(str(py_file))

        print(f"   ✅ ملفات سليمة: {len(verification_results['passed'])}")
        print(f"   ❌ ملفات بها أخطاء: {len(verification_results['failed'])}")
        print(f"   🚨 ملفات حرجة بها أخطاء: {len(verification_results['critical_failed'])}")

        return verification_results

    def verify_file_syntax(self, file_path: Path) -> bool:
        """التحقق من صحة نحو الملف"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            return True
        except:
            return False

    def create_backup(self, file_path: Path):
        """إنشاء نسخة احتياطية"""
        backup_path = self.backup_dir / f"{file_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)

    def restore_backup(self, file_path: Path):
        """استعادة النسخة الاحتياطية"""
        backup_files = list(self.backup_dir.glob(f"{file_path.name}.backup_*"))
        if backup_files:
            latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
            shutil.copy2(latest_backup, file_path)

    def generate_ultimate_report(self):
        """إنشاء التقرير النهائي الشامل"""
        print("\n📊 إنشاء التقرير النهائي...")

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_files_processed": len(self.fixed_files) + len(self.failed_fixes),
            "successfully_fixed": len(self.fixed_files),
            "failed_to_fix": len(self.failed_fixes),
            "critical_errors": len(self.critical_errors),
            "success_rate": len(self.fixed_files) / (len(self.fixed_files) + len(self.failed_fixes)) * 100 if (self.fixed_files or self.failed_fixes) else 0,
            "fixed_files": self.fixed_files,
            "failed_files": self.failed_fixes,
            "critical_error_files": self.critical_errors
        }

        report_file = f"ultimate_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"📄 تم حفظ التقرير النهائي في: {report_file}")

        # طباعة الملخص
        print("\n" + "="*70)
        print("🎯 ملخص الإصلاح النهائي:")
        print(f"   📁 إجمالي الملفات المعالجة: {report['total_files_processed']}")
        print(f"   ✅ ملفات تم إصلاحها: {report['successfully_fixed']}")
        print(f"   ❌ ملفات فشل إصلاحها: {report['failed_to_fix']}")
        print(f"   🚨 أخطاء حرجة: {report['critical_errors']}")
        print(f"   📊 معدل النجاح: {report['success_rate']:.1f}%")
        print("="*70)

def main():
    """تشغيل المصلح النهائي"""
    fixer = UltimateSystemFixer()
    fixed_count = fixer.run_ultimate_fix()

    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} ملف بنجاح!")
        print("🔍 يُنصح بإجراء اختبار شامل للتأكد من عمل جميع الوحدات")
    else:
        print("\n⚠️  لم يتم إصلاح أي ملفات. النظام قد يحتاج مراجعة يدوية متخصصة")

if __name__ == "__main__":
    main()
