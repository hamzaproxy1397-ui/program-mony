# -*- coding: utf-8 -*-
"""
أداة إصلاح سريعة للأخطاء النحوية الأساسية
Quick Syntax Error Fixer
"""

import ast
import re
from pathlib import Path

class QuickSyntaxFixer:
    def __init__(self):
        self.fixed_files = []
        self.failed_files = []
        
    def fix_common_syntax_errors(self, content):
        """إصلاح الأخطاء النحوية الشائعة"""
        
        # إصلاح الاستيرادات المكررة
        lines = content.split('\n')
        imports_seen = set()
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # إزالة الاستيرادات المكررة
            if stripped.startswith(('import ', 'from ')) and stripped in imports_seen:
                continue
            elif stripped.startswith(('import ', 'from ')):
                imports_seen.add(stripped)
                
            fixed_lines.append(line)
            
        content = '\n'.join(fixed_lines)
        
        # إصلاحات أخرى شائعة
        fixes = [
            # إصلاح try blocks بدون except
            (r'(\s+)try:\s*\n(\s+.*?\n)(?=\s*(?:def|class|if|for|while|try|$))', 
             r'\1try:\n\2\1except Exception as e:\n\1    pass\n'),
             
            # إصلاح escape sequences خاطئة
            (r'\\([^\\nrtbfav\'"0-7xuUN])', r'\\\\\1'),
            
            # إصلاح أقواس غير مغلقة في f-strings
            (r'f\'([^\']*)\{([^}]*)\}([^\']*)\'\)', r'f\'\1{\2}\3\''),
            
            # إصلاح مسافات في f-strings
            (r'f\'([^\']*)\{([^}]*)\}([^\']*)\'\s*\)', r'f\'\1{\2}\3\''),
        ]
        
        for pattern, replacement in fixes:
            try:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            except Exception:
                continue
                
        return content
        
    def fix_file(self, file_path):
        """إصلاح ملف واحد"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            # محاولة تحليل الملف أولاً
            try:
                ast.parse(original_content)
                print(f"✅ {file_path.name} - لا يحتاج إصلاح")
                return True
            except SyntaxError:
                pass
                
            # تطبيق الإصلاحات
            fixed_content = self.fix_common_syntax_errors(original_content)
            
            # التحقق من الإصلاح
            try:
                ast.parse(fixed_content)
                
                # حفظ الملف المُصلح
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                    
                print(f"🔧 {file_path.name} - تم الإصلاح")
                self.fixed_files.append(str(file_path))
                return True
                
            except SyntaxError as e:
                print(f"❌ {file_path.name} - فشل الإصلاح: السطر {e.lineno}")
                self.failed_files.append(str(file_path))
                return False
                
        except Exception as e:
            print(f"⚠️ {file_path.name} - خطأ في المعالجة: {e}")
            self.failed_files.append(str(file_path))
            return False
            
    def fix_critical_files(self):
        """إصلاح الملفات الحرجة أولاً"""
        critical_files = [
            "core/app_core.py",
            "comprehensive_income_formula_demo.py", 
            "deep_comprehensive_fixer.py",
            "config/postgresql_config.py",
            "database/comprehensive_income_manager.py",
            "database/fix_database.py"
        ]
        
        print("🔧 إصلاح الملفات الحرجة...")
        
        for file_path in critical_files:
            full_path = Path(file_path)
            if full_path.exists():
                self.fix_file(full_path)
            else:
                print(f"⚠️ ملف غير موجود: {file_path}")
                
    def fix_all_syntax_errors(self):
        """إصلاح جميع الأخطاء النحوية"""
        print("🔧 بدء إصلاح جميع الأخطاء النحوية...")
        
        # إصلاح الملفات الحرجة أولاً
        self.fix_critical_files()
        
        # إصلاح باقي الملفات
        python_files = list(Path('.').rglob('*.py'))
        
        for py_file in python_files:
            # تجاهل المجلدات المؤقتة والنسخ الاحتياطية
            if any(skip in str(py_file) for skip in ['__pycache__', '.git', 'venv', 'backup', 'BACKUP']):
                continue
                
            if str(py_file) not in [str(Path(f)) for f in [
                "core/app_core.py",
                "comprehensive_income_formula_demo.py", 
                "deep_comprehensive_fixer.py",
                "config/postgresql_config.py",
                "database/comprehensive_income_manager.py",
                "database/fix_database.py"
            ]]:
                self.fix_file(py_file)
                
        # طباعة التقرير
        print(f"\n📊 تقرير الإصلاح:")
        print(f"   ✅ ملفات تم إصلاحها: {len(self.fixed_files)}")
        print(f"   ❌ ملفات فشل إصلاحها: {len(self.failed_files)}")
        
        if self.failed_files:
            print(f"\n❌ الملفات التي فشل إصلاحها:")
            for file_path in self.failed_files:
                print(f"   - {file_path}")

if __name__ == "__main__":
    fixer = QuickSyntaxFixer()
    fixer.fix_all_syntax_errors()
