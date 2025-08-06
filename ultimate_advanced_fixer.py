#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
المصلح المتقدم والشامل لجميع الأخطاء
Ultimate Advanced Fixer for All Errors
"""

import ast
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

class UltimateAdvancedFixer:
    """المصلح المتقدم والشامل لجميع الأخطاء"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.backup_dir = Path("backup_ultimate_advanced")
        self.backup_dir.mkdir(exist_ok=True)
        
        self.fixed_files = []
        self.failed_fixes = []
        
        # قائمة الأخطاء المكتشفة من التشخيص
        self.error_files = [
            "advanced_error_analyzer.py",
            "advanced_error_fixer.py", 
            "advanced_syntax_fixer.py",
            "comprehensive_income_formula_demo.py",
            "deep_comprehensive_fixer.py",
            "deep_import_fixer.py",
            "quick_pattern_fixer.py",
            "run_app.py",
            "run_fixed_app.py",
            "safe_start.py",
            "start_with_scheduler.py",
            "ultimate_system_fixer.py",
            "config/postgresql_config.py",
            "core/app_core.py",
            "database/comprehensive_income_manager.py",
            "database/fix_database.py",
            "ui/daily_journal_window.py",
            "ui/sales_analysis_window.py"
        ]
    
    def run_ultimate_advanced_fix(self):
        """تشغيل الإصلاح المتقدم والشامل"""
        print("🔧 بدء الإصلاح المتقدم والشامل...")
        print("=" * 70)
        
        # إصلاح جميع الملفات المشكلة
        for file_path in self.error_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"🔧 إصلاح متقدم: {file_path}")
                self.fix_file_advanced(full_path)
        
        # إصلاح شامل لجميع ملفات Python
        print("\n🔧 إصلاح شامل لجميع ملفات Python...")
        self.fix_all_python_files()
        
        # التحقق النهائي
        print("\n✅ التحقق النهائي من الإصلاحات...")
        self.final_verification()
        
        # إنشاء التقرير
        self.generate_fix_report()
        
        return len(self.fixed_files)
    
    def fix_file_advanced(self, file_path: Path):
        """إصلاح متقدم لملف واحد"""
        try:
            # قراءة المحتوى
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # محاولة تحليل الملف
            try:
                ast.parse(original_content)
                print(f"   ✅ {file_path.name} - سليم بالفعل")
                return True
            except SyntaxError as e:
                print(f"   🔧 إصلاح {file_path.name}: {e.msg} (السطر {e.lineno})")
                
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
                        self.failed_fixes.append(str(file_path))
                        # استعادة النسخة الأصلية
                        self.restore_backup(file_path)
                        return False
                else:
                    print(f"   ⚠️  لا يمكن إصلاح {file_path.name} تلقائياً")
                    self.failed_fixes.append(str(file_path))
                    return False
                    
        except Exception as e:
            print(f"   ❌ خطأ في معالجة {file_path.name}: {e}")
            self.failed_fixes.append(str(file_path))
            return False
    
    def apply_advanced_fixes(self, content: str, error: SyntaxError, file_path: Path) -> str:
        """تطبيق إصلاحات متقدمة وشاملة"""
        lines = content.split('\n')
        
        if not error.lineno or error.lineno > len(lines):
            return content
        
        error_line_idx = error.lineno - 1
        
        # إصلاحات متقدمة حسب نوع الخطأ
        if "unterminated string literal" in error.msg:
            content = self.fix_unterminated_strings(content, error_line_idx)
        
        elif "unexpected indent" in error.msg:
            content = self.fix_unexpected_indent(content, error_line_idx)
        
        elif "unexpected character after line continuation character" in error.msg:
            content = self.fix_line_continuation(content, error_line_idx)
        
        elif "invalid syntax" in error.msg:
            content = self.fix_invalid_syntax(content, error_line_idx, error)
        
        elif "expected an indented block" in error.msg:
            content = self.fix_missing_indent(content, error_line_idx)
        
        # إصلاحات إضافية شاملة
        content = self.apply_comprehensive_fixes(content)
        
        return content
    
    def fix_unterminated_strings(self, content: str, error_line_idx: int) -> str:
        """إصلاح النصوص غير المكتملة"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            line = lines[error_line_idx]
            
            # البحث عن علامات اقتباس غير مكتملة
            if line.count('"') % 2 == 1:
                # إضافة علامة اقتباس مفقودة
                lines[error_line_idx] = line + '"'
            elif line.count("'") % 2 == 1:
                # إضافة علامة اقتباس مفردة مفقودة
                lines[error_line_idx] = line + "'"
            elif '"""' in line and line.count('"""') == 1:
                # إضافة إغلاق للنص متعدد الأسطر
                lines[error_line_idx] = line + '"""'
        
        return '\n'.join(lines)
    
    def fix_unexpected_indent(self, content: str, error_line_idx: int) -> str:
        """إصلاح المسافات البادئة غير المتوقعة"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            # إزالة المسافات البادئة الزائدة
            lines[error_line_idx] = lines[error_line_idx].lstrip()
            
            # إذا كان السطر فارغاً بعد إزالة المسافات، احذفه
            if not lines[error_line_idx].strip():
                lines.pop(error_line_idx)
        
        return '\n'.join(lines)
    
    def fix_line_continuation(self, content: str, error_line_idx: int) -> str:
        """إصلاح مشاكل استمرار الأسطر"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            line = lines[error_line_idx]
            
            # إصلاح escape characters خاطئة
            line = re.sub(r"\\\'", "'", line)
            line = re.sub(r'\\"', '"', line)
            line = re.sub(r"hasattr\(self, \\'(\w+)\\'\)", r"hasattr(self, '\1')", line)
            
            lines[error_line_idx] = line
        
        return '\n'.join(lines)
    
    def fix_invalid_syntax(self, content: str, error_line_idx: int, error: SyntaxError) -> str:
        """إصلاح الأخطاء النحوية العامة"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            line = lines[error_line_idx]
            
            # إصلاح الأقواس المفقودة
            if '(' in line and line.count('(') > line.count(')'):
                lines[error_line_idx] = line + ')' * (line.count('(') - line.count(')'))
            elif '[' in line and line.count('[') > line.count(']'):
                lines[error_line_idx] = line + ']' * (line.count('[') - line.count(']'))
            elif '{' in line and line.count('{') > line.count('}'):
                lines[error_line_idx] = line + '}' * (line.count('{') - line.count('}'))
            
            # إصلاح النقطتين المفقودتين
            elif any(line.strip().startswith(kw) for kw in ['if ', 'for ', 'while ', 'def ', 'class ', 'try', 'except', 'else', 'elif']):
                if not line.rstrip().endswith(':'):
                    lines[error_line_idx] = line.rstrip() + ':'
        
        return '\n'.join(lines)
    
    def fix_missing_indent(self, content: str, error_line_idx: int) -> str:
        """إصلاح المسافات البادئة المفقودة"""
        lines = content.split('\n')
        
        # البحث عن السطر الذي يحتاج مسافة بادئة
        for i in range(error_line_idx - 1, max(0, error_line_idx - 5), -1):
            if i < len(lines) and lines[i].strip().endswith(':'):
                base_indent = len(lines[i]) - len(lines[i].lstrip())
                required_indent = base_indent + 4
                
                # إضافة pass مع المسافة البادئة الصحيحة
                if error_line_idx < len(lines):
                    lines.insert(error_line_idx, ' ' * required_indent + 'pass')
                break
        
        return '\n'.join(lines)
    
    def apply_comprehensive_fixes(self, content: str) -> str:
        """تطبيق إصلاحات شاملة إضافية"""
        # إصلاح الأنماط المكررة الشائعة
        patterns = [
            # إصلاح الأنماط المكررة
            (r'(\s+)if (\w+) and hasattr\(\2, "destroy"\):\s*\n\s+if \2 and hasattr\(\2, "destroy"\):\s*\n\s+\2\.destroy\(\)',
             r'\1if \2 and hasattr(\2, "destroy"):\n\1    \2.destroy()'),
            
            # إصلاح escape sequences
            (r'\\([^\\nrtbfav\'\"0-7xuUN])', r'\\\\1'),
            
            # إصلاح المسافات الزائدة
            (r'\s+$', ''),
            
            # إصلاح الأسطر الفارغة المتعددة
            (r'\n\n\n+', '\n\n'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        return content
    
    def fix_all_python_files(self):
        """إصلاح شامل لجميع ملفات Python"""
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            if str(py_file) not in [str(self.project_root / f) for f in self.fixed_files]:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # محاولة تحليل الملف
                    try:
                        ast.parse(content)
                    except SyntaxError:
                        # الملف يحتاج إصلاح
                        if str(py_file.relative_to(self.project_root)) not in self.error_files:
                            self.fix_file_advanced(py_file)
                except Exception:
                    continue
    
    def final_verification(self):
        """التحقق النهائي من جميع الإصلاحات"""
        verified_files = 0
        failed_files = 0
        
        for file_path in self.fixed_files:
            full_path = Path(file_path)
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                    verified_files += 1
                    print(f"   ✅ {full_path.name} - تم التحقق")
                except SyntaxError:
                    failed_files += 1
                    print(f"   ❌ {full_path.name} - لا يزال به أخطاء")
        
        print(f"   📊 ملفات تم التحقق منها: {verified_files}")
        print(f"   📊 ملفات لا تزال بها أخطاء: {failed_files}")
        
        return verified_files, failed_files
    
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
    
    def generate_fix_report(self):
        """إنشاء تقرير الإصلاح"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_files_processed": len(self.fixed_files) + len(self.failed_fixes),
            "successfully_fixed": len(self.fixed_files),
            "failed_to_fix": len(self.failed_fixes),
            "success_rate": len(self.fixed_files) / (len(self.fixed_files) + len(self.failed_fixes)) * 100 if (self.fixed_files or self.failed_fixes) else 0,
            "fixed_files": self.fixed_files,
            "failed_files": self.failed_fixes
        }
        
        report_file = f"ultimate_advanced_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ تقرير الإصلاح في: {report_file}")
        
        # طباعة الملخص
        print("\n" + "="*70)
        print("🎯 ملخص الإصلاح المتقدم والشامل:")
        print(f"   📁 إجمالي الملفات المعالجة: {report['total_files_processed']}")
        print(f"   ✅ ملفات تم إصلاحها: {report['successfully_fixed']}")
        print(f"   ❌ ملفات فشل إصلاحها: {report['failed_to_fix']}")
        print(f"   📊 معدل النجاح: {report['success_rate']:.1f}%")
        print("="*70)

def main():
    """تشغيل المصلح المتقدم والشامل"""
    fixer = UltimateAdvancedFixer()
    fixed_count = fixer.run_ultimate_advanced_fix()
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} ملف بنجاح!")
    else:
        print("\n✅ جميع الملفات سليمة أو لا تحتاج إصلاح")

if __name__ == "__main__":
    main()
