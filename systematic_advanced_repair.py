#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الإصلاح المنهجي المتقدم
Systematic Advanced Repair System
"""

import ast
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class SystematicAdvancedRepair:
    """نظام الإصلاح المنهجي المتقدم"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.backup_dir = Path("backup_systematic")
        self.backup_dir.mkdir(exist_ok=True)
        
        self.repair_results = {
            "timestamp": datetime.now().isoformat(),
            "files_processed": 0,
            "files_repaired": 0,
            "files_failed": 0,
            "repair_categories": {
                "syntax_errors": 0,
                "indentation_fixes": 0,
                "import_fixes": 0,
                "string_literal_fixes": 0,
                "bracket_fixes": 0,
                "code_quality_improvements": 0
            },
            "repaired_files": [],
            "failed_files": [],
            "performance_improvements": []
        }
        
        # قائمة الملفات المشكلة من التشخيص
        self.problematic_files = [
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
    
    def run_systematic_repair(self):
        """تشغيل الإصلاح المنهجي المتقدم"""
        print("🔧 بدء الإصلاح المنهجي المتقدم...")
        print("=" * 70)
        
        # المرحلة 1: إصلاح الملفات المشكلة المحددة
        print("\n🎯 المرحلة 1: إصلاح الملفات المشكلة المحددة...")
        self.repair_problematic_files()
        
        # المرحلة 2: فحص وإصلاح شامل لجميع الملفات
        print("\n🔍 المرحلة 2: فحص وإصلاح شامل...")
        self.comprehensive_repair_scan()
        
        # المرحلة 3: تحسينات الأداء والجودة
        print("\n⚡ المرحلة 3: تحسينات الأداء والجودة...")
        self.apply_performance_improvements()
        
        # المرحلة 4: التحقق النهائي
        print("\n✅ المرحلة 4: التحقق النهائي...")
        self.final_verification()
        
        # إنشاء التقرير
        self.generate_repair_report()
        
        return self.repair_results
    
    def repair_problematic_files(self):
        """إصلاح الملفات المشكلة المحددة"""
        for file_path in self.problematic_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"🔧 إصلاح: {file_path}")
                self.repair_single_file(full_path, is_priority=True)
            else:
                print(f"⚠️  {file_path} - غير موجود")
    
    def comprehensive_repair_scan(self):
        """فحص وإصلاح شامل لجميع الملفات"""
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            # تخطي الملفات التي تم إصلاحها بالفعل
            if str(py_file.relative_to(self.project_root)) in [f.replace('\\', '/') for f in self.repair_results["repaired_files"]]:
                continue
            
            # فحص الملف للأخطاء
            if self.needs_repair(py_file):
                print(f"🔧 إصلاح إضافي: {py_file.name}")
                self.repair_single_file(py_file)
    
    def repair_single_file(self, file_path: Path, is_priority: bool = False):
        """إصلاح ملف واحد بشكل منهجي"""
        self.repair_results["files_processed"] += 1
        
        try:
            # قراءة المحتوى الأصلي
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # فحص النحو الأولي
            try:
                ast.parse(original_content)
                print(f"   ✅ {file_path.name} - سليم بالفعل")
                return True
            except SyntaxError as e:
                print(f"   🔧 إصلاح {file_path.name}: {e.msg} (السطر {e.lineno})")
                
                # إنشاء نسخة احتياطية
                self.create_backup(file_path)
                
                # تطبيق الإصلاحات المنهجية
                repaired_content = self.apply_systematic_repairs(original_content, e, file_path)
                
                if repaired_content != original_content:
                    # حفظ المحتوى المصلح
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(repaired_content)
                    
                    # التحقق من الإصلاح
                    try:
                        ast.parse(repaired_content)
                        print(f"   ✅ تم إصلاح {file_path.name}")
                        self.repair_results["files_repaired"] += 1
                        self.repair_results["repaired_files"].append(str(file_path.relative_to(self.project_root)))
                        return True
                    except SyntaxError as new_error:
                        print(f"   ❌ فشل إصلاح {file_path.name}: {new_error.msg}")
                        self.repair_results["files_failed"] += 1
                        self.repair_results["failed_files"].append(str(file_path.relative_to(self.project_root)))
                        # استعادة النسخة الأصلية
                        self.restore_backup(file_path)
                        return False
                else:
                    print(f"   ⚠️  لا يمكن إصلاح {file_path.name} تلقائياً")
                    self.repair_results["files_failed"] += 1
                    self.repair_results["failed_files"].append(str(file_path.relative_to(self.project_root)))
                    return False
                    
        except Exception as e:
            print(f"   ❌ خطأ في معالجة {file_path.name}: {e}")
            self.repair_results["files_failed"] += 1
            self.repair_results["failed_files"].append(str(file_path.relative_to(self.project_root)))
            return False
    
    def apply_systematic_repairs(self, content: str, error: SyntaxError, file_path: Path) -> str:
        """تطبيق الإصلاحات المنهجية"""
        lines = content.split('\n')
        
        if not error.lineno or error.lineno > len(lines):
            return content
        
        error_line_idx = error.lineno - 1
        
        # تطبيق الإصلاحات حسب نوع الخطأ
        if "unterminated string literal" in error.msg:
            content = self.fix_unterminated_strings_advanced(content, error_line_idx)
            self.repair_results["repair_categories"]["string_literal_fixes"] += 1
        
        elif "unexpected indent" in error.msg:
            content = self.fix_indentation_systematic(content, error_line_idx)
            self.repair_results["repair_categories"]["indentation_fixes"] += 1
        
        elif "unexpected character after line continuation character" in error.msg:
            content = self.fix_line_continuation_advanced(content, error_line_idx)
            self.repair_results["repair_categories"]["string_literal_fixes"] += 1
        
        elif "invalid syntax" in error.msg:
            content = self.fix_invalid_syntax_systematic(content, error_line_idx, error)
            self.repair_results["repair_categories"]["syntax_errors"] += 1
        
        elif "expected an indented block" in error.msg:
            content = self.fix_missing_indentation(content, error_line_idx)
            self.repair_results["repair_categories"]["indentation_fixes"] += 1
        
        elif "unmatched" in error.msg or "was never closed" in error.msg:
            content = self.fix_bracket_issues_systematic(content, error_line_idx)
            self.repair_results["repair_categories"]["bracket_fixes"] += 1
        
        # تطبيق إصلاحات إضافية شاملة
        content = self.apply_comprehensive_fixes(content)
        
        return content
    
    def fix_unterminated_strings_advanced(self, content: str, error_line_idx: int) -> str:
        """إصلاح متقدم للنصوص غير المكتملة"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            line = lines[error_line_idx]
            
            # إصلاح علامات الاقتباس المفقودة
            if line.count('"') % 2 == 1:
                # البحث عن آخر علامة اقتباس وإضافة الإغلاق
                last_quote_pos = line.rfind('"')
                if last_quote_pos != -1:
                    lines[error_line_idx] = line + '"'
            
            elif line.count("'") % 2 == 1:
                last_quote_pos = line.rfind("'")
                if last_quote_pos != -1:
                    lines[error_line_idx] = line + "'"
            
            elif '"""' in line and line.count('"""') == 1:
                lines[error_line_idx] = line + '"""'
            
            elif "'''" in line and line.count("'''") == 1:
                lines[error_line_idx] = line + "'''"
        
        return '\n'.join(lines)
    
    def fix_indentation_systematic(self, content: str, error_line_idx: int) -> str:
        """إصلاح منهجي للمسافات البادئة"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            current_line = lines[error_line_idx]
            
            # إزالة المسافات البادئة الزائدة
            stripped_line = current_line.lstrip()
            
            if stripped_line:
                # حساب المسافة البادئة الصحيحة بناءً على السياق
                correct_indent = self.calculate_correct_indentation(lines, error_line_idx)
                lines[error_line_idx] = ' ' * correct_indent + stripped_line
            else:
                # سطر فارغ - احذفه
                lines.pop(error_line_idx)
        
        return '\n'.join(lines)
    
    def fix_line_continuation_advanced(self, content: str, error_line_idx: int) -> str:
        """إصلاح متقدم لمشاكل استمرار الأسطر"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            line = lines[error_line_idx]
            
            # إصلاح escape characters شائعة
            fixes = [
                (r"\\\'", "'"),
                (r'\\"', '"'),
                (r"hasattr\(self, \\'(\w+)\\'\)", r"hasattr(self, '\1')"),
                (r"hasattr\((\w+), \\'(\w+)\\'\)", r"hasattr(\1, '\2')"),
                (r"\\'(\w+)\\'", r"'\1'"),
            ]
            
            for pattern, replacement in fixes:
                line = re.sub(pattern, replacement, line)
            
            lines[error_line_idx] = line
        
        return '\n'.join(lines)
    
    def fix_invalid_syntax_systematic(self, content: str, error_line_idx: int, error: SyntaxError) -> str:
        """إصلاح منهجي للأخطاء النحوية"""
        lines = content.split('\n')
        
        if error_line_idx < len(lines):
            line = lines[error_line_idx]
            
            # إصلاح الأقواس المفقودة
            bracket_fixes = [
                ('(', ')'),
                ('[', ']'),
                ('{', '}')
            ]
            
            for open_bracket, close_bracket in bracket_fixes:
                open_count = line.count(open_bracket)
                close_count = line.count(close_bracket)
                
                if open_count > close_count:
                    lines[error_line_idx] = line + close_bracket * (open_count - close_count)
                    break
            
            # إصلاح النقطتين المفقودتين
            control_keywords = ['if ', 'for ', 'while ', 'def ', 'class ', 'try', 'except', 'else', 'elif', 'with ', 'finally']
            if any(line.strip().startswith(kw) for kw in control_keywords):
                if not line.rstrip().endswith(':'):
                    lines[error_line_idx] = line.rstrip() + ':'
            
            # إصلاح الفواصل المفقودة في القوائم والمعاملات
            if error.offset and error.offset < len(line):
                char_at_error = line[error.offset - 1] if error.offset > 0 else ''
                if char_at_error not in ',;:' and line[error.offset:error.offset+1] not in ' \t\n':
                    lines[error_line_idx] = line[:error.offset] + ',' + line[error.offset:]
        
        return '\n'.join(lines)
    
    def fix_missing_indentation(self, content: str, error_line_idx: int) -> str:
        """إصلاح المسافات البادئة المفقودة"""
        lines = content.split('\n')
        
        # البحث عن السطر الذي يحتاج مسافة بادئة
        for i in range(error_line_idx - 1, max(0, error_line_idx - 5), -1):
            if i < len(lines) and lines[i].strip().endswith(':'):
                base_indent = len(lines[i]) - len(lines[i].lstrip())
                required_indent = base_indent + 4
                
                # إضافة pass مع المسافة البادئة الصحيحة
                if error_line_idx < len(lines):
                    if not lines[error_line_idx].strip():
                        lines[error_line_idx] = ' ' * required_indent + 'pass'
                    else:
                        lines.insert(error_line_idx, ' ' * required_indent + 'pass')
                break
        
        return '\n'.join(lines)
    
    def fix_bracket_issues_systematic(self, content: str, error_line_idx: int) -> str:
        """إصلاح منهجي لمشاكل الأقواس"""
        lines = content.split('\n')
        
        # تحليل الأقواس في الملف كاملاً
        bracket_stack = []
        bracket_pairs = {'(': ')', '[': ']', '{': '}'}
        
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char in bracket_pairs:
                    bracket_stack.append((char, i, j))
                elif char in bracket_pairs.values():
                    if bracket_stack:
                        open_bracket, open_line, open_pos = bracket_stack[-1]
                        if bracket_pairs[open_bracket] == char:
                            bracket_stack.pop()
                        else:
                            # عدم تطابق الأقواس
                            if i == error_line_idx:
                                # إصلاح في السطر الحالي
                                correct_close = bracket_pairs[open_bracket]
                                lines[i] = line[:j] + correct_close + line[j+1:]
                                break
        
        # إغلاق الأقواس المفتوحة
        for open_bracket, line_idx, pos in reversed(bracket_stack):
            if line_idx < len(lines):
                lines[line_idx] += bracket_pairs[open_bracket]
        
        return '\n'.join(lines)
    
    def apply_comprehensive_fixes(self, content: str) -> str:
        """تطبيق إصلاحات شاملة إضافية"""
        # إصلاحات عامة للجودة
        fixes = [
            # إزالة المسافات الزائدة في نهاية الأسطر
            (r'\s+$', ''),
            
            # إصلاح الأسطر الفارغة المتعددة
            (r'\n\n\n+', '\n\n'),
            
            # إصلاح المسافات حول العمليات
            (r'(\w+)=(\w+)', r'\1 = \2'),
            (r'(\w+)\+(\w+)', r'\1 + \2'),
            (r'(\w+)-(\w+)', r'\1 - \2'),
            
            # إصلاح الفواصل
            (r',(\w)', r', \1'),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        self.repair_results["repair_categories"]["code_quality_improvements"] += 1
        
        return content
    
    def calculate_correct_indentation(self, lines: list, line_idx: int) -> int:
        """حساب المسافة البادئة الصحيحة"""
        # البحث عن السطر السابق غير الفارغ
        for i in range(line_idx - 1, -1, -1):
            if lines[i].strip():
                prev_line = lines[i]
                prev_indent = len(prev_line) - len(prev_line.lstrip())
                
                # إذا كان السطر السابق ينتهي بـ :، زيد المسافة البادئة
                if prev_line.strip().endswith(':'):
                    return prev_indent + 4
                else:
                    return prev_indent
        
        return 0  # بداية الملف
    
    def needs_repair(self, file_path: Path) -> bool:
        """فحص ما إذا كان الملف يحتاج إصلاح"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            return False  # الملف سليم
        except SyntaxError:
            return True  # الملف يحتاج إصلاح
        except Exception:
            return False  # خطأ في القراءة - تخطي
    
    def apply_performance_improvements(self):
        """تطبيق تحسينات الأداء"""
        improvements = []
        
        # تحسين الملفات الكبيرة
        large_files = []
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            file_size = py_file.stat().st_size
            if file_size > 100000:  # أكبر من 100KB
                large_files.append((py_file, file_size))
        
        if large_files:
            print(f"   📊 تم العثور على {len(large_files)} ملف كبير الحجم")
            for file_path, size in large_files:
                improvement = f"مراجعة وتقسيم الملف الكبير: {file_path.name} ({size/1024:.1f} KB)"
                improvements.append(improvement)
                print(f"      ⚠️  {improvement}")
        
        # تحسين الاستيرادات المكررة
        duplicate_imports = self.find_duplicate_imports()
        if duplicate_imports:
            print(f"   📦 تم العثور على {len(duplicate_imports)} استيراد مكرر")
            for file_path, imports in duplicate_imports.items():
                improvement = f"إزالة الاستيرادات المكررة في: {file_path}"
                improvements.append(improvement)
                print(f"      🔧 {improvement}")
        
        self.repair_results["performance_improvements"] = improvements
    
    def find_duplicate_imports(self) -> dict:
        """البحث عن الاستيرادات المكررة"""
        duplicate_imports = {}
        
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                import_lines = []
                for line_num, line in enumerate(content.split('\n'), 1):
                    if line.strip().startswith(('import ', 'from ')):
                        import_lines.append((line_num, line.strip()))
                
                # البحث عن المكررات
                seen_imports = set()
                duplicates = []
                
                for line_num, import_line in import_lines:
                    if import_line in seen_imports:
                        duplicates.append((line_num, import_line))
                    else:
                        seen_imports.add(import_line)
                
                if duplicates:
                    duplicate_imports[str(py_file.relative_to(self.project_root))] = duplicates
                    
            except Exception:
                continue
        
        return duplicate_imports
    
    def final_verification(self):
        """التحقق النهائي من جميع الإصلاحات"""
        print("   🔍 التحقق من الملفات المصلحة...")
        
        verified_count = 0
        failed_verification = []
        
        for file_path_str in self.repair_results["repaired_files"]:
            file_path = self.project_root / file_path_str
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                    verified_count += 1
                    print(f"      ✅ {file_path.name} - تم التحقق")
                except SyntaxError as e:
                    failed_verification.append(file_path_str)
                    print(f"      ❌ {file_path.name} - لا يزال به خطأ: {e.msg}")
        
        print(f"   📊 تم التحقق من {verified_count} ملف بنجاح")
        if failed_verification:
            print(f"   ⚠️  {len(failed_verification)} ملف لا يزال به أخطاء")
    
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
    
    def generate_repair_report(self):
        """إنشاء تقرير الإصلاح"""
        report_file = f"systematic_repair_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.repair_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ تقرير الإصلاح في: {report_file}")
        
        # طباعة ملخص التقرير
        print("\n" + "="*70)
        print("🎯 ملخص الإصلاح المنهجي المتقدم:")
        print(f"   📁 إجمالي الملفات المعالجة: {self.repair_results['files_processed']}")
        print(f"   ✅ ملفات تم إصلاحها: {self.repair_results['files_repaired']}")
        print(f"   ❌ ملفات فشل إصلاحها: {self.repair_results['files_failed']}")
        
        success_rate = (self.repair_results['files_repaired'] / self.repair_results['files_processed'] * 100) if self.repair_results['files_processed'] > 0 else 0
        print(f"   📊 معدل النجاح: {success_rate:.1f}%")
        
        print("\n🔧 تفاصيل الإصلاحات:")
        for category, count in self.repair_results['repair_categories'].items():
            if count > 0:
                print(f"   - {category}: {count}")
        
        if self.repair_results['performance_improvements']:
            print(f"\n⚡ تحسينات الأداء المقترحة: {len(self.repair_results['performance_improvements'])}")
        
        print("="*70)

def main():
    """تشغيل نظام الإصلاح المنهجي المتقدم"""
    repair_system = SystematicAdvancedRepair()
    results = repair_system.run_systematic_repair()
    
    return results

if __name__ == "__main__":
    main()
