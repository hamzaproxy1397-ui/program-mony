#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة الإصلاح السريع للأنماط المتبقية
Quick Pattern Fixer for Remaining Issues
"""

import re
from pathlib import Path

class QuickPatternFixer:
    """أداة الإصلاح السريع للأنماط المتبقية"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.fixed_files = []
    
    def fix_all_remaining_patterns(self):
        """إصلاح جميع الأنماط المتبقية"""
        print("🔧 بدء الإصلاح السريع للأنماط المتبقية...")
        
        # البحث في جميع ملفات Python
        for py_file in self.project_root.rglob("*.py"):
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # إصلاح النمط الأساسي المتكرر
                pattern1 = r'(\s+)self\.if window and hasattr\(window, "destroy"\):\s*\n\s+if window and hasattr\(window, "destroy"\):\s*\n\s+window\.destroy\(\)'
                replacement1 = r'\1if hasattr(self, 'window') and self.window:\n\1    self.window.destroy()':
                content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE)
                
                # إصلاح النمط الثاني
                pattern2 = r'(\s+)if (\w+) and hasattr\(\2, "destroy"\):\s*\n\s+if \2 and hasattr\(\2, "destroy"\):\s*\n\s+\2\.destroy\(\)'
                replacement2 = r'\1if \2 and hasattr(\2, "destroy"):\n\1    \2.destroy()'
                content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)
                
                # إصلاح النمط الثالث - الأسطر المكررة
                pattern3 = r'(\s+)(self\.)?if (\w+) and hasattr\(\3, "destroy"\):\s*\n\s+if \3 and hasattr\(\3, "destroy"\):\s*\n\s+\3\.destroy\(\)'
                replacement3 = r'\1if \3 and hasattr(\3, "destroy"):\n\1    \3.destroy()'
                content = re.sub(pattern3, replacement3, content, flags=re.MULTILINE)
                
                # إصلاح النمط الرابع - مع self
                pattern4 = r'(\s+)self\.if (\w+) and hasattr\(\2, "destroy"\):\s*\n\s+if \2 and hasattr\(\2, "destroy"\):\s*\n\s+\2\.destroy\(\)'
                replacement4 = r'\1if hasattr(self, '\2') and self.\2:\n\1    self.\2.destroy()'
                content = re.sub(pattern4, replacement4, content, flags=re.MULTILINE)
                
                if content != original_content:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"   ✅ تم إصلاح {py_file.name}")
                    self.fixed_files.append(str(py_file))
                    
            except Exception as e:
                print(f"   ❌ خطأ في معالجة {py_file}: {e}")
        
        print(f"\n🎯 تم إصلاح {len(self.fixed_files)} ملف")
        return len(self.fixed_files)

def main():
    """تشغيل أداة الإصلاح السريع"""
    fixer = QuickPatternFixer()
    fixed_count = fixer.fix_all_remaining_patterns()
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} ملف بنجاح!")
    else:
        print("\n✅ لا توجد ملفات تحتاج إصلاح")

if __name__ == "__main__":
    main()
