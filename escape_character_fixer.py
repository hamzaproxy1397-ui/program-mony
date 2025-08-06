#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مصلح escape characters
Escape Character Fixer
"""

import re
from pathlib import Path

def fix_escape_characters():
    """إصلاح جميع escape characters الخاطئة"""
    print("🔧 بدء إصلاح escape characters...")
    
    fixed_files = []
    
    # البحث في جميع ملفات Python
    for py_file in Path(".").rglob("*.py"):
        if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "backup"]):
            continue
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # إصلاح escape characters شائعة
            content = re.sub(r"\\'", "'", content)
            content = re.sub(r'\\"', '"', content)
            content = re.sub(r"hasattr\(self, \'(\w+)\'\)", r"hasattr(self, '\1')", content)
            
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ تم إصلاح {py_file.name}")
                fixed_files.append(str(py_file))
        
        except Exception as e:
            print(f"   ❌ خطأ في {py_file}: {e}")
    
    print(f"\n🎯 تم إصلاح {len(fixed_files)} ملف")
    return len(fixed_files)

if __name__ == "__main__":
    fix_escape_characters()
