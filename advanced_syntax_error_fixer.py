#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 أداة إصلاح الأخطاء النحوية المتقدمة
Advanced Syntax Error Fixer Tool

تقوم هذه الأداة بإصلاح الأخطاء النحوية المكتشفة في تقرير الفحص الشامل
"""

import os
import re
import json
import shutil
import ast
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

class AdvancedSyntaxErrorFixer:
    """فئة إصلاح الأخطاء النحوية المتقدمة"""
    
    def __init__(self):
        self.fixes_applied = []
        self.backup_dir = Path("syntax_fixes_backup")
        self.backup_dir.mkdir(exist_ok=True)
        
        # قائمة الملفات التي تحتوي على أخطاء نحوية من التقرير
        self.syntax_errors = [
            {"file": "deep_comprehensive_system_audit.py", "line": 673, "error": "expected 'except' or 'finally' block"},
            {"file": "final_cleanup_tool.py", "line": 219, "error": "unexpected indent"},
            {"file": "quick_pattern_fixer.py", "line": 35, "error": "invalid syntax"},
            {"file": "run_control_panel_safe.py", "line": 112, "error": "expected 'except' or 'finally' block"},
            {"file": "run_control_panel_simple.py", "line": 58, "error": "unexpected indent"},
            {"file": "run_fixed_app.py", "line": 155, "error": "unexpected indent"},
            {"file": "safe_main.py", "line": 106, "error": "expected 'except' or 'finally' block"},
            {"file": "ultimate_system_fixer.py", "line": 302, "error": "unterminated string literal"}
        ]

    def fix_all_errors(self):
        """إصلاح جميع الأخطاء النحوية"""
        print("🔧 بدء إصلاح الأخطاء النحوية المتقدم...")
        print("=" * 60)
        
        for error in self.syntax_errors:
            try:
                self._fix_single_error(error)
            except Exception as e:
                print(f"❌ فشل في إصلاح {error['file']}: {e}")
        
        print(f"\n✅ تم إصلاح {len(self.fixes_applied)} ملف")
        self._save_fixes_report()

    def _fix_single_error(self, error_info: Dict):
        """إصلاح خطأ واحد"""
        file_path = Path(error_info['file'])
        line_number = error_info['line']
        error_message = error_info['error']
        
        print(f"\n🔍 فحص: {file_path}")
        print(f"   السطر {line_number}: {error_message}")
        
        if not file_path.exists():
            print(f"⚠️ الملف غير موجود: {file_path}")
            return
        
        # إنشاء نسخة احتياطية
        backup_path = self.backup_dir / f"{file_path.name}.backup"
        shutil.copy2(file_path, backup_path)
        
        # قراءة الملف
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
        except Exception as e:
            print(f"❌ خطأ في قراءة الملف: {e}")
            return
        
        # تطبيق الإصلاحات حسب نوع الخطأ
        fixed = False
        
        if "expected 'except' or 'finally' block" in error_message:
            fixed, lines = self._fix_incomplete_try_block(lines, line_number)
        elif "unexpected indent" in error_message:
            fixed, lines = self._fix_indentation_error(lines, line_number)
        elif "invalid syntax" in error_message:
            fixed, lines = self._fix_invalid_syntax(lines, line_number)
        elif "unterminated string literal" in error_message:
            fixed, lines = self._fix_unterminated_string(lines, line_number)
        
        if fixed:
            # حفظ الملف المُصلح
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines) + '\n')
                
                self.fixes_applied.append({
                    "file": str(file_path),
                    "line": line_number,
                    "error": error_message,
                    "backup": str(backup_path),
                    "timestamp": datetime.now().isoformat()
                })
                print(f"✅ تم إصلاح: {file_path}")
                
                # التحقق من صحة الإصلاح
                self._verify_fix(file_path)
                
            except Exception as e:
                print(f"❌ خطأ في حفظ الملف: {e}")
        else:
            print(f"⚠️ لم يتم إصلاح: {file_path}")

    def _fix_incomplete_try_block(self, lines: List[str], line_number: int) -> Tuple[bool, List[str]]:
        """إصلاح كتلة try غير مكتملة"""
        try:
            # البحث عن try block في المنطقة المحيطة
            start_search = max(0, line_number - 20)
            end_search = min(len(lines), line_number + 10)
            
            for i in range(start_search, end_search):
                if i < len(lines):
                    line = lines[i].strip()
                    if line.endswith('try:') or 'try:' in line:
                        # حساب المسافة البادئة
                        indent = len(lines[i]) - len(lines[i].lstrip())
                        
                        # إضافة except block
                        except_line = ' ' * indent + "except Exception as e:"
                        pass_line = ' ' * (indent + 4) + "pass"
                        
                        # البحث عن نهاية try block
                        insert_pos = i + 1
                        while insert_pos < len(lines) and (lines[insert_pos].strip() == '' or 
                                                         len(lines[insert_pos]) - len(lines[insert_pos].lstrip()) > indent):
                            insert_pos += 1
                        
                        # إدراج except block
                        lines.insert(insert_pos, except_line)
                        lines.insert(insert_pos + 1, pass_line)
                        return True, lines
            
            return False, lines
        except Exception:
            return False, lines

    def _fix_indentation_error(self, lines: List[str], line_number: int) -> Tuple[bool, List[str]]:
        """إصلاح خطأ المسافات البادئة"""
        try:
            if line_number <= len(lines):
                line_idx = line_number - 1
                
                if line_idx < len(lines):
                    line = lines[line_idx]
                    
                    # إذا كان السطر فارغاً أو يحتوي على مسافات فقط
                    if line.strip() == '':
                        lines[line_idx] = ''
                        return True, lines
                    
                    # إزالة المسافات الزائدة في بداية السطر
                    stripped_line = line.lstrip()
                    if stripped_line:
                        # الحصول على المسافة البادئة من السطر السابق
                        prev_indent = 0
                        if line_idx > 0:
                            prev_line = lines[line_idx - 1]
                            prev_indent = len(prev_line) - len(prev_line.lstrip())
                        
                        # تطبيق مسافة بادئة مناسبة
                        lines[line_idx] = ' ' * prev_indent + stripped_line
                        return True, lines
            
            return False, lines
        except Exception:
            return False, lines

    def _fix_invalid_syntax(self, lines: List[str], line_number: int) -> Tuple[bool, List[str]]:
        """إصلاح بناء الجملة غير الصحيح"""
        try:
            if line_number <= len(lines):
                line_idx = line_number - 1
                
                if line_idx < len(lines):
                    line = lines[line_idx]
                    original_line = line
                    
                    # إصلاحات شائعة
                    # 1. إضافة نقطتين مفقودة
                    if any(keyword in line for keyword in ['if ', 'for ', 'while ', 'def ', 'class ', 'try:', 'except']):
                        if not line.rstrip().endswith(':') and not line.rstrip().endswith('\\'):
                            line = line.rstrip() + ':'
                    
                    # 2. إزالة الأحرف غير الصحيحة
                    line = re.sub(r'[^\w\s=+\-*/()[\]{},.:\'\"#\\]', '', line)
                    
                    # 3. إصلاح علامات الاقتباس
                    if line.count('"') % 2 == 1:
                        line = line + '"'
                    elif line.count("'") % 2 == 1:
                        line = line + "'"
                    
                    if line != original_line:
                        lines[line_idx] = line
                        return True, lines
            
            return False, lines
        except Exception:
            return False, lines

    def _fix_unterminated_string(self, lines: List[str], line_number: int) -> Tuple[bool, List[str]]:
        """إصلاح النصوص غير المنتهية"""
        try:
            if line_number <= len(lines):
                line_idx = line_number - 1
                
                if line_idx < len(lines):
                    line = lines[line_idx]
                    
                    # البحث عن علامات اقتباس غير مغلقة
                    if line.count('"') % 2 == 1:
                        lines[line_idx] = line.rstrip() + '"'
                        return True, lines
                    elif line.count("'") % 2 == 1:
                        lines[line_idx] = line.rstrip() + "'"
                        return True, lines
                    
                    # البحث عن نصوص متعددة الأسطر غير مكتملة
                    if '"""' in line and line.count('"""') % 2 == 1:
                        lines[line_idx] = line + '"""'
                        return True, lines
                    elif "'''" in line and line.count("'''") % 2 == 1:
                        lines[line_idx] = line + "'''"
                        return True, lines
            
            return False, lines
        except Exception:
            return False, lines

    def _verify_fix(self, file_path: Path):
        """التحقق من صحة الإصلاح"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # محاولة تحليل الملف
            ast.parse(content)
            print(f"   ✅ تم التحقق من صحة الإصلاح")
        except SyntaxError as e:
            print(f"   ⚠️ لا يزال هناك خطأ نحوي: {e}")
        except Exception as e:
            print(f"   ⚠️ خطأ في التحقق: {e}")

    def _save_fixes_report(self):
        """حفظ تقرير الإصلاحات"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"advanced_syntax_fixes_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "fixes_applied": self.fixes_applied,
            "total_fixes": len(self.fixes_applied),
            "backup_directory": str(self.backup_dir),
            "summary": {
                "files_fixed": len(self.fixes_applied),
                "total_errors_attempted": len(self.syntax_errors)
            }
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ تقرير الإصلاحات في: {report_path}")

def main():
    """الدالة الرئيسية"""
    print("🔧 أداة إصلاح الأخطاء النحوية المتقدمة")
    print("=" * 50)
    
    # إنشاء مُصلح الأخطاء
    fixer = AdvancedSyntaxErrorFixer()
    
    # تطبيق الإصلاحات
    fixer.fix_all_errors()
    
    print("\n🎯 تم الانتهاء من عملية الإصلاح")
    print("💡 تحقق من الملفات المُصلحة وقم بتشغيل الفحص مرة أخرى للتأكد")

if __name__ == "__main__":
    main()
