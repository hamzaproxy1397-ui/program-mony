#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
المصلح الشامل والعميق للنظام
Deep Comprehensive System Fixer
"""

import ast
import re
import json
from pathlib import Path
from datetime import datetime
import shutil
import logging

class DeepComprehensiveFixer:
    """المصلح الشامل والعميق للنظام"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.backup_dir = Path("backup_deep")
        self.backup_dir.mkdir(exist_ok=True)
        
        self.fixed_files = []
        self.failed_fixes = []
        self.critical_files = [
            "main.py",
            "ui/main_window.py", 
            "ui/login_window.py",
            "ui/pos_window.py",
            "ui/pos_simple.py",
            "database/hybrid_database_manager.py"
        ]
        
        # إعداد نظام السجلات
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def run_deep_comprehensive_fix(self):
        """تشغيل الإصلاح الشامل والعميق"""
        print("🔧 بدء الإصلاح الشامل والعميق للنظام...")
        print("=" * 70)
        
        # المرحلة 1: إصلاح الملفات الحرجة أولاً
        print("\n🎯 المرحلة 1: إصلاح الملفات الحرجة...")
        self.fix_critical_files_deeply()
        
        # المرحلة 2: إصلاح جميع ملفات UI
        print("\n🖥️  المرحلة 2: إصلاح ملفات واجهة المستخدم...")
        self.fix_all_ui_files_deeply()
        
        # المرحلة 3: إصلاح الملفات المساعدة
        print("\n🔧 المرحلة 3: إصلاح الملفات المساعدة...")
        self.fix_helper_files()
        
        # المرحلة 4: التحقق النهائي الشامل
        print("\n✅ المرحلة 4: التحقق النهائي الشامل...")
        self.comprehensive_final_verification()
        
        # إنشاء التقرير النهائي
        self.generate_comprehensive_report()
        
        return len(self.fixed_files)
    
    def fix_critical_files_deeply(self):
        """إصلاح عميق للملفات الحرجة"""
        for file_path in self.critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"🔧 إصلاح عميق: {file_path}")
                self.fix_file_with_deep_analysis(full_path, is_critical=True)
    
    def fix_all_ui_files_deeply(self):
        """إصلاح عميق لجميع ملفات واجهة المستخدم"""
        ui_dir = self.project_root / "ui"
        if ui_dir.exists():
            for py_file in ui_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    print(f"🖥️  إصلاح UI عميق: {py_file.name}")
                    self.fix_file_with_deep_analysis(py_file)
    
    def fix_helper_files(self):
        """إصلاح الملفات المساعدة"""
        helper_patterns = [
            "run_*.py",
            "start_*.py", 
            "safe_*.py",
            "*_demo.py"
        ]
        
        for pattern in helper_patterns:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file():
                    print(f"🔧 إصلاح مساعد: {file_path.name}")
                    self.fix_file_with_deep_analysis(file_path)
    
    def fix_file_with_deep_analysis(self, file_path: Path, is_critical: bool = False):
        """إصلاح ملف مع تحليل عميق"""
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
                
                # تطبيق الإصلاحات العميقة
                fixed_content = self.apply_deep_comprehensive_fixes(original_content, e, file_path)
                
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
    
    def apply_deep_comprehensive_fixes(self, content: str, error: SyntaxError, file_path: Path) -> str:
        """تطبيق إصلاحات شاملة وعميقة"""
        lines = content.split('\n')
        
        if not error.lineno or error.lineno > len(lines):
            return content
        
        error_line_idx = error.lineno - 1
        
        # إصلاحات شاملة متعددة المراحل
        content = self.fix_duplicate_patterns_deep(content)
        content = self.fix_indentation_issues_deep(content)
        content = self.fix_syntax_errors_deep(content, error)
        content = self.fix_escape_sequences_deep(content)
        content = self.fix_incomplete_blocks_deep(content)
        content = self.fix_bracket_issues_deep(content)
        
        return content
    
    def fix_duplicate_patterns_deep(self, content: str) -> str:
        """إصلاح عميق للأنماط المكررة"""
        # إصلاح النمط الأساسي المكرر
        patterns = [
            # النمط الأول: self.if window
            (r'(\s+)self\.if (\w+) and hasattr\(\2, "destroy"\):\s*\n\s+if \2 and hasattr\(\2, "destroy"\):\s*\n\s+\2\.destroy\(\)',
             r'\1if hasattr(self, \'\2\') and self.\2:\n\1    self.\2.destroy()'),
            
            # النمط الثاني: if window مكرر
            (r'(\s+)if (\w+) and hasattr\(\2, "destroy"\):\s*\n\s+if \2 and hasattr\(\2, "destroy"\):\s*\n\s+\2\.destroy\(\)',
             r'\1if \2 and hasattr(\2, "destroy"):\n\1    \2.destroy()'),
            
            # النمط الثالث: أسطر مكررة عامة
            (r'(\s+)(if .+:\s*\n)\s+\2',
             r'\1\2'),
            
            # النمط الرابع: escape characters خاطئة
            (r'hasattr\(self, \\\'(\w+)\\\')',
             r'hasattr(self, \'\1\')'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        return content
    
    def fix_indentation_issues_deep(self, content: str) -> str:
        """إصلاح عميق لمشاكل المسافات البادئة"""
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # إصلاح الأسطر التي تبدأ بمسافات خاطئة
            if re.match(r'^    \w+$', line.rstrip()):
                # التحقق من السياق
                if i > 0 and not lines[i-1].strip().endswith(':'):
                    fixed_lines.append(line.lstrip())
                else:
                    fixed_lines.append(line)
            # إصلاح الأسطر الفارغة مع مسافات
            elif re.match(r'^\s+$', line):
                fixed_lines.append('')
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_syntax_errors_deep(self, content: str, error: SyntaxError) -> str:
        """إصلاح عميق للأخطاء النحوية"""
        lines = content.split('\n')
        
        if error.lineno and error.lineno <= len(lines):
            error_line_idx = error.lineno - 1
            error_line = lines[error_line_idx]
            
            # إصلاحات متقدمة حسب نوع الخطأ
            if "expected an indented block" in error.msg:
                # البحث عن السطر الذي يحتاج مسافة بادئة
                for i in range(error_line_idx - 1, max(0, error_line_idx - 5), -1):
                    if lines[i].strip().endswith(':'):
                        base_indent = len(lines[i]) - len(lines[i].lstrip())
                        required_indent = base_indent + 4
                        lines.insert(error_line_idx, ' ' * required_indent + 'pass')
                        break
            
            elif "invalid syntax" in error.msg:
                # إصلاح الأقواس والفواصل
                if '(' in error_line and error_line.count('(') > error_line.count(')'):
                    lines[error_line_idx] = error_line + ')' * (error_line.count('(') - error_line.count(')'))
                elif not error_line.rstrip().endswith(':') and any(error_line.strip().startswith(kw) for kw in ['if ', 'for ', 'while ', 'def ', 'class ', 'try', 'except', 'else', 'elif']):
                    lines[error_line_idx] = error_line.rstrip() + ':'
            
            elif "unexpected indent" in error.msg:
                # إزالة المسافات البادئة الزائدة
                lines[error_line_idx] = error_line.lstrip()
        
        return '\n'.join(lines)
    
    def fix_escape_sequences_deep(self, content: str) -> str:
        """إصلاح عميق لتسلسلات الهروب"""
        # إصلاح escape sequences شائعة
        fixes = [
            (r'\\([^\\nrtbfav\'"0-7xuUN])', r'\\\\1'),
            (r'\\\'', r"'"),
            (r'\"', r'"'),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def fix_incomplete_blocks_deep(self, content: str) -> str:
        """إصلاح عميق للبلوكات غير المكتملة"""
        lines = content.split('\n')
        
        # البحث عن البلوكات المفتوحة
        open_blocks = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.endswith(':') and not stripped.startswith('#'):
                indent_level = len(line) - len(line.lstrip())
                open_blocks.append((i, indent_level))
            elif stripped and not line.startswith(' ') and open_blocks:
                # إغلاق البلوكات المفتوحة
                while open_blocks:
                    block_line, block_indent = open_blocks.pop()
                    if i < len(lines) and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) <= block_indent):
                        lines.insert(i, ' ' * (block_indent + 4) + 'pass')
                        i += 1
        
        return '\n'.join(lines)
    
    def fix_bracket_issues_deep(self, content: str) -> str:
        """إصلاح عميق لمشاكل الأقواس"""
        # تحليل الأقواس في المحتوى كاملاً
        bracket_pairs = {'(': ')', '[': ']', '{': '}'}
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            for open_bracket, close_bracket in bracket_pairs.items():
                open_count = line.count(open_bracket)
                close_count = line.count(close_bracket)
                
                if open_count > close_count:
                    lines[i] = line + close_bracket * (open_count - close_count)
                elif close_count > open_count:
                    lines[i] = open_bracket * (close_count - open_count) + line
        
        return '\n'.join(lines)
    
    def comprehensive_final_verification(self):
        """التحقق النهائي الشامل"""
        print("🔍 إجراء التحقق النهائي الشامل...")
        
        verification_results = {
            "critical_passed": 0,
            "critical_failed": 0,
            "ui_passed": 0,
            "ui_failed": 0,
            "total_passed": 0,
            "total_failed": 0
        }
        
        # فحص الملفات الحرجة
        for file_path in self.critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                if self.verify_file_syntax(full_path):
                    verification_results["critical_passed"] += 1
                    print(f"   ✅ {file_path} - حرج وسليم")
                else:
                    verification_results["critical_failed"] += 1
                    print(f"   ❌ {file_path} - حرج وبه أخطاء")
        
        # فحص ملفات UI
        ui_dir = self.project_root / "ui"
        if ui_dir.exists():
            for py_file in ui_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    if self.verify_file_syntax(py_file):
                        verification_results["ui_passed"] += 1
                    else:
                        verification_results["ui_failed"] += 1
        
        verification_results["total_passed"] = verification_results["critical_passed"] + verification_results["ui_passed"]
        verification_results["total_failed"] = verification_results["critical_failed"] + verification_results["ui_failed"]
        
        print(f"   🎯 ملفات حرجة سليمة: {verification_results['critical_passed']}")
        print(f"   🎯 ملفات حرجة بها أخطاء: {verification_results['critical_failed']}")
        print(f"   🖥️  ملفات UI سليمة: {verification_results['ui_passed']}")
        print(f"   🖥️  ملفات UI بها أخطاء: {verification_results['ui_failed']}")
        
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
    
    def generate_comprehensive_report(self):
        """إنشاء التقرير الشامل"""
        print("\n📊 إنشاء التقرير الشامل...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_files_processed": len(self.fixed_files) + len(self.failed_fixes),
            "successfully_fixed": len(self.fixed_files),
            "failed_to_fix": len(self.failed_fixes),
            "success_rate": len(self.fixed_files) / (len(self.fixed_files) + len(self.failed_fixes)) * 100 if (self.fixed_files or self.failed_fixes) else 0,
            "fixed_files": self.fixed_files,
            "failed_files": self.failed_fixes
        }
        
        report_file = f"deep_comprehensive_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 تم حفظ التقرير الشامل في: {report_file}")
        
        # طباعة الملخص
        print("\n" + "="*70)
        print("🎯 ملخص الإصلاح الشامل والعميق:")
        print(f"   📁 إجمالي الملفات المعالجة: {report['total_files_processed']}")
        print(f"   ✅ ملفات تم إصلاحها: {report['successfully_fixed']}")
        print(f"   ❌ ملفات فشل إصلاحها: {report['failed_to_fix']}")
        print(f"   📊 معدل النجاح: {report['success_rate']:.1f}%")
        print("="*70)

def main():
    """تشغيل المصلح الشامل والعميق"""
    fixer = DeepComprehensiveFixer()
    fixed_count = fixer.run_deep_comprehensive_fix()
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} ملف بنجاح!")
        print("🔍 النظام جاهز للاختبار الشامل")
    else:
        print("\n⚠️  لم يتم إصلاح ملفات إضافية")

if __name__ == "__main__":
    main()
