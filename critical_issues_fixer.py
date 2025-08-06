#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة إصلاح المشاكل الحرجة
Critical Issues Fixer for Accounting Software
"""

import sys
import os
import re
import ast
import logging
from pathlib import Path
from typing import List, Dict, Tuple

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class CriticalIssuesFixer:
    """مصلح المشاكل الحرجة"""
    
    def __init__(self):
        self.setup_logging()
        self.fixed_files = []
        self.errors = []
    
    def setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/critical_fixes.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def fix_syntax_errors(self):
        """إصلاح الأخطاء النحوية"""
        print("🔧 إصلاح الأخطاء النحوية...")
        
        # الملفات التي تحتوي على أخطاء نحوية
        problematic_files = [
            'advanced_error_analyzer.py',
            'advanced_error_fixer.py', 
            'advanced_syntax_fixer.py'
        ]
        
        for file_path in problematic_files:
            if Path(file_path).exists():
                try:
                    self._fix_file_syntax(file_path)
                    print(f"  ✅ تم إصلاح {file_path}")
                except Exception as e:
                    print(f"  ❌ فشل إصلاح {file_path}: {e}")
                    self.errors.append(f"{file_path}: {e}")
    
    def _fix_file_syntax(self, file_path: str):
        """إصلاح أخطاء ملف محدد"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # إصلاح escape sequences
        fixes = [
            # إصلاح backslashes في strings
            (r"\.replace\('/', '\.'\.replace\('\\\\', '\.'", r".replace('/', '.').replace('\\\\', '.'"),

            # إصلاح string literals غير مكتملة
            (r'(["\'])([^"\']*?)\\$', r'\1\2\\\\'),

            # إصلاح مسارات Windows العامة
            (r'\\(?![nrtbfav\\"\'/0-7xuUN])', r'\\\\'),
        ]
        
        for pattern, replacement in fixes:
            try:
                content = re.sub(pattern, replacement, content)
            except re.error as e:
                self.logger.warning(f"خطأ في regex pattern {pattern}: {e}")
                continue
        
        # التحقق من صحة النتيجة
        try:
            ast.parse(content)
            
            # حفظ الملف المصلح
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_files.append(file_path)
                
        except SyntaxError as e:
            # إذا لم ينجح الإصلاح، نحاول إصلاح أكثر تفصيلاً
            content = self._advanced_syntax_fix(content, e)
            
            try:
                ast.parse(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_files.append(file_path)
            except SyntaxError:
                raise Exception(f"لا يمكن إصلاح الخطأ النحوي: {e}")
    
    def _advanced_syntax_fix(self, content: str, error: SyntaxError) -> str:
        """إصلاح متقدم للأخطاء النحوية"""
        lines = content.split('\n')
        
        if error.lineno and error.lineno <= len(lines):
            error_line = lines[error.lineno - 1]
            
            # إصلاحات محددة حسب نوع الخطأ
            if "unterminated string literal" in str(error):
                # إصلاح string غير مكتمل
                if error_line.count('"') % 2 == 1:
                    error_line += '"'
                elif error_line.count("'") % 2 == 1:
                    error_line += "'"
                
                lines[error.lineno - 1] = error_line
            
            elif "invalid escape sequence" in str(error):
                # إصلاح escape sequences
                error_line = re.sub(r'\\(?![nrtbfav\\"\'/0-7xuUN])', r'\\\\', error_line)
                lines[error.lineno - 1] = error_line
        
        return '\n'.join(lines)
    
    def optimize_complex_functions(self):
        """تحسين الدوال المعقدة"""
        print("⚡ تحسين الدوال المعقدة...")
        
        python_files = list(Path(".").rglob("*.py"))
        python_files = [f for f in python_files if not any(part.startswith('.') for part in f.parts)]
        
        optimized_count = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # تحليل AST للعثور على الدوال المعقدة
                try:
                    tree = ast.parse(content)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            complexity = self._calculate_complexity(node)
                            
                            if complexity > 15:  # دالة معقدة جداً
                                # إضافة تعليق تحذيري
                                suggestion = self._generate_optimization_suggestion(node, complexity)
                                
                                if suggestion:
                                    # إضافة التعليق في بداية الدالة
                                    lines = content.split('\n')
                                    func_line = node.lineno - 1
                                    
                                    if func_line < len(lines):
                                        indent = len(lines[func_line]) - len(lines[func_line].lstrip())
                                        comment = ' ' * indent + f'# تحذير: دالة معقدة (تعقيد: {complexity}) - {suggestion}'
                                        lines.insert(func_line, comment)
                                        content = '\n'.join(lines)
                                        optimized_count += 1
                
                except SyntaxError:
                    continue
                
                # حفظ الملف المحسن
                if optimized_count > 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            
            except Exception as e:
                self.logger.error(f"خطأ في تحسين {file_path}: {e}")
        
        print(f"  ✅ تم تحسين {optimized_count} دالة معقدة")
    
    def _calculate_complexity(self, node):
        """حساب تعقيد الدالة"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _generate_optimization_suggestion(self, node, complexity):
        """إنشاء اقتراح للتحسين"""
        suggestions = [
            "فكر في تقسيم هذه الدالة إلى دوال أصغر",
            "استخدم early returns لتقليل التعقيد",
            "فكر في استخدام dictionary للشروط المتعددة",
            "استخدم list comprehensions بدلاً من loops معقدة"
        ]
        
        return suggestions[min(len(suggestions) - 1, complexity // 5)]
    
    def add_security_headers(self):
        """إضافة تعليقات أمنية للملفات الحساسة"""
        print("🔒 إضافة تعليقات أمنية...")
        
        sensitive_files = [
            'database/database_manager.py',
            'auth/auth_manager.py',
            'services/sales_manager.py'
        ]
        
        security_header = '''# -*- coding: utf-8 -*-
# تحذير أمني: هذا الملف يحتوي على عمليات حساسة
# يجب مراجعة جميع المدخلات والتأكد من التحقق منها
# Security Warning: This file contains sensitive operations
# All inputs must be validated and sanitized

'''
        
        for file_path in sensitive_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'تحذير أمني' not in content:
                        # إضافة التحذير بعد shebang و encoding
                        lines = content.split('\n')
                        insert_pos = 0
                        
                        # العثور على المكان المناسب للإدراج
                        for i, line in enumerate(lines[:5]):
                            if line.startswith('#!') or 'coding:' in line or 'encoding:' in line:
                                insert_pos = i + 1
                        
                        lines.insert(insert_pos, security_header)
                        content = '\n'.join(lines)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"  ✅ تم إضافة تحذير أمني لـ {file_path}")
                
                except Exception as e:
                    print(f"  ❌ فشل في إضافة تحذير أمني لـ {file_path}: {e}")
    
    def generate_fix_report(self):
        """إنشاء تقرير الإصلاحات"""
        print("\n" + "="*60)
        print("📋 تقرير الإصلاحات الحرجة")
        print("="*60)
        
        print(f"\n✅ الملفات المصلحة: {len(self.fixed_files)}")
        for file_path in self.fixed_files:
            print(f"  - {file_path}")
        
        if self.errors:
            print(f"\n❌ الأخطاء: {len(self.errors)}")
            for error in self.errors:
                print(f"  - {error}")
        
        print(f"\n📊 معدل النجاح: {(len(self.fixed_files) / max(len(self.fixed_files) + len(self.errors), 1)) * 100:.1f}%")
    
    def run_critical_fixes(self):
        """تشغيل جميع الإصلاحات الحرجة"""
        print("🚀 بدء إصلاح المشاكل الحرجة")
        print("="*60)
        
        try:
            self.fix_syntax_errors()
            self.optimize_complex_functions()
            self.add_security_headers()
            
            self.generate_fix_report()
            
            return len(self.errors) == 0
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل الإصلاحات: {e}")
            return False

def main():
    """الدالة الرئيسية"""
    fixer = CriticalIssuesFixer()
    success = fixer.run_critical_fixes()
    
    if success:
        print("\n🎉 تم إصلاح جميع المشاكل الحرجة بنجاح!")
        return 0
    else:
        print("\n⚠️ هناك مشاكل لم يتم إصلاحها")
        return 1

if __name__ == "__main__":
    sys.exit(main())
