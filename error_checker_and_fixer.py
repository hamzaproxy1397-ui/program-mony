#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة فحص وإصلاح أخطاء البرنامج المحاسبي
Error Checker and Fixer for Arabic Accounting Software
"""

import os
import sys
import ast
import traceback
import importlib.util
from pathlib import Path
from typing import List, Dict, Tuple

class ErrorChecker:
    """فاحص الأخطاء ومصلحها"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors_found = []
        self.fixes_applied = []
        
    def check_python_files(self) -> List[Dict]:
        """فحص جميع ملفات Python للأخطاء النحوية"""
        print("🔍 فحص ملفات Python للأخطاء النحوية...")
        
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        syntax_errors = []
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                ast.parse(code)
                print(f"✅ {file_path.name}")
            except SyntaxError as e:
                error_info = {
                    'file': str(file_path),
                    'line': e.lineno,
                    'error': str(e),
                    'text': e.text
                }
                syntax_errors.append(error_info)
                print(f"❌ {file_path.name}: خطأ نحوي في السطر {e.lineno}")
            except Exception as e:
                error_info = {
                    'file': str(file_path),
                    'line': 0,
                    'error': str(e),
                    'text': ''
                }
                syntax_errors.append(error_info)
                print(f"⚠️ {file_path.name}: خطأ في القراءة - {e}")
        
        return syntax_errors
    
    def check_imports(self) -> List[Dict]:
        """فحص الاستيرادات المفقودة"""
        print("\n🔍 فحص الاستيرادات المطلوبة...")
        
        required_packages = [
            'customtkinter',
            'PIL',
            'numpy',
            'matplotlib'
        ]
        
        missing_imports = []
        for package in required_packages:
            try:
                if package == 'PIL':
                    import PIL
                else:
                    __import__(package)
                print(f"✅ {package}")
            except ImportError:
                missing_imports.append(package)
                print(f"❌ {package} - مفقود")
        
        return missing_imports
    
    def check_file_structure(self) -> List[str]:
        """فحص هيكل الملفات المطلوبة"""
        print("\n🔍 فحص هيكل الملفات...")
        
        required_files = [
            'main.py',
            'ui/main_window.py',
            'ui/login_window.py',
            'database/hybrid_database_manager.py',
            'themes/modern_theme.py',
            'config/settings.py'
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                missing_files.append(file_path)
                print(f"❌ {file_path} - مفقود")
        
        return missing_files
    
    def fix_common_syntax_errors(self, file_path: str) -> bool:
        """إصلاح الأخطاء النحوية الشائعة"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # إصلاح الأخطاء الشائعة
            fixes = [
                # إصلاح الفواصل المفقودة
                (r'(\w+)\s*\n\s*(\w+\s*=)', r'\1,\n\2'),
                # إصلاح الأقواس غير المغلقة
                (r'(\([^)]*)\n([^)]*\))', r'\1\2'),
                # إصلاح المسافات البادئة
                (r'^    ([^\s])', r'    \1'),
            ]
            
            for pattern, replacement in fixes:
                import re
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            if content != original_content:
                # إنشاء نسخة احتياطية
                backup_path = file_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # كتابة المحتوى المصحح
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"🔧 تم إصلاح {file_path}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ فشل في إصلاح {file_path}: {e}")
            return False
    
    def install_missing_packages(self, missing_packages: List[str]) -> bool:
        """تثبيت الحزم المفقودة"""
        if not missing_packages:
            return True
            
        print(f"\n📦 تثبيت الحزم المفقودة: {', '.join(missing_packages)}")
        
        try:
            import subprocess
            for package in missing_packages:
                if package == 'PIL':
                    package = 'Pillow'
                
                print(f"تثبيت {package}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ تم تثبيت {package}")
                else:
                    print(f"❌ فشل في تثبيت {package}: {result.stderr}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تثبيت الحزم: {e}")
            return False
    
    def create_missing_directories(self) -> None:
        """إنشاء المجلدات المفقودة"""
        required_dirs = ['logs', 'database', 'reports/generated', 'backups']
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 تم إنشاء مجلد: {dir_path}")
    
    def run_comprehensive_check(self) -> bool:
        """تشغيل فحص شامل وإصلاح الأخطاء"""
        print("🔧 بدء الفحص الشامل وإصلاح الأخطاء...")
        print("=" * 50)
        
        # 1. فحص هيكل الملفات
        missing_files = self.check_file_structure()
        
        # 2. إنشاء المجلدات المفقودة
        self.create_missing_directories()
        
        # 3. فحص الاستيرادات
        missing_imports = self.check_imports()
        
        # 4. تثبيت الحزم المفقودة
        if missing_imports:
            if not self.install_missing_packages(missing_imports):
                print("⚠️ فشل في تثبيت بعض الحزم")
        
        # 5. فحص الأخطاء النحوية
        syntax_errors = self.check_python_files()
        
        # 6. إصلاح الأخطاء النحوية
        for error in syntax_errors:
            self.fix_common_syntax_errors(error['file'])
        
        # 7. فحص نهائي
        print("\n🔍 فحص نهائي...")
        final_syntax_errors = self.check_python_files()
        
        if not final_syntax_errors:
            print("\n✅ جميع الفحوصات تمت بنجاح!")
            print("🚀 البرنامج جاهز للتشغيل")
            return True
        else:
            print(f"\n⚠️ لا تزال هناك {len(final_syntax_errors)} أخطاء تحتاج إصلاح يدوي")
            for error in final_syntax_errors:
                print(f"   - {error['file']}: السطر {error['line']}")
            return False

def main():
    """الدالة الرئيسية"""
    print("🔧 أداة فحص وإصلاح أخطاء البرنامج المحاسبي")
    print("=" * 50)
    
    checker = ErrorChecker()
    success = checker.run_comprehensive_check()
    
    if success:
        print("\n🎉 تم إصلاح جميع الأخطاء بنجاح!")
        print("يمكنك الآن تشغيل البرنامج باستخدام:")
        print("  python main.py")
    else:
        print("\n⚠️ هناك أخطاء تحتاج إصلاح يدوي")
        print("يرجى مراجعة الأخطاء المذكورة أعلاه")
    
    input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
