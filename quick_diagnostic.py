#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص سريع للبرنامج المحاسبي
Quick Diagnostic for Arabic Accounting Software
"""

import sys
import os
import traceback
from pathlib import Path

def check_python_version():
    """فحص إصدار Python"""
    print("🐍 فحص إصدار Python...")
    version = sys.version_info
    print(f"   الإصدار: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ إصدار Python مناسب")
        return True
    else:
        print("   ❌ يتطلب Python 3.8 أو أحدث")
        return False

def check_basic_imports():
    """فحص الاستيرادات الأساسية"""
    print("\n📦 فحص الاستيرادات الأساسية...")
    
    imports_status = {}
    
    # فحص tkinter
    try:
        import tkinter
        print("   ✅ tkinter")
        imports_status['tkinter'] = True
    except ImportError:
        print("   ❌ tkinter - مطلوب لواجهة المستخدم")
        imports_status['tkinter'] = False
    
    # فحص customtkinter
    try:
        import customtkinter
        print("   ✅ customtkinter")
        imports_status['customtkinter'] = True
    except ImportError:
        print("   ❌ customtkinter - قم بتثبيته: pip install customtkinter")
        imports_status['customtkinter'] = False
    
    # فحص PIL
    try:
        from PIL import Image, ImageTk
        print("   ✅ PIL/Pillow")
        imports_status['PIL'] = True
    except ImportError:
        print("   ⚠️ PIL/Pillow - اختياري للصور: pip install Pillow")
        imports_status['PIL'] = False
    
    # فحص numpy
    try:
        import numpy
        print("   ✅ numpy")
        imports_status['numpy'] = True
    except ImportError:
        print("   ⚠️ numpy - اختياري للمعالجة: pip install numpy")
        imports_status['numpy'] = False
    
    return imports_status

def check_file_structure():
    """فحص هيكل الملفات"""
    print("\n📁 فحص هيكل الملفات...")
    
    required_files = [
        'main.py',
        'ui/main_window.py',
        'ui/__init__.py',
        'database/__init__.py',
        'themes/__init__.py',
        'config/__init__.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    return missing_files

def test_main_import():
    """اختبار استيراد الملف الرئيسي"""
    print("\n🔍 اختبار استيراد الملف الرئيسي...")
    
    try:
        # إضافة المسار الحالي
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # محاولة استيراد الملف الرئيسي
        from ui.main_window import MainApplication
        print("   ✅ تم استيراد MainApplication بنجاح")
        return True
        
    except ImportError as e:
        print(f"   ❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"   ❌ خطأ عام: {e}")
        traceback.print_exc()
        return False

def check_database_files():
    """فحص ملفات قاعدة البيانات"""
    print("\n🗄️ فحص ملفات قاعدة البيانات...")
    
    db_files = [
        'database/hybrid_database_manager.py',
        'database/database_manager.py'
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"   ✅ {db_file}")
        else:
            print(f"   ❌ {db_file}")

def create_minimal_test():
    """إنشاء اختبار مبسط"""
    print("\n🧪 إنشاء اختبار مبسط...")
    
    test_code = '''
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    import customtkinter as ctk
    
    # إنشاء نافذة اختبار بسيطة
    root = ctk.CTk()
    root.title("اختبار البرنامج المحاسبي")
    root.geometry("400x300")
    
    label = ctk.CTkLabel(root, text="✅ البرنامج يعمل بشكل صحيح!", font=("Arial", 16))
    label.pack(pady=50)
    
    button = ctk.CTkButton(root, text="إغلاق", command=root.destroy)
    button.pack(pady=20)
    
    print("✅ تم إنشاء نافذة الاختبار")
    root.mainloop()
    
except Exception as e:
    print(f"❌ خطأ في الاختبار: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open('test_simple.py', 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    print("   ✅ تم إنشاء test_simple.py")
    print("   🚀 يمكنك تشغيله: python test_simple.py")

def main():
    """الدالة الرئيسية للتشخيص"""
    print("🔍 تشخيص سريع للبرنامج المحاسبي")
    print("=" * 40)
    
    # فحص إصدار Python
    python_ok = check_python_version()
    
    # فحص الاستيرادات
    imports_status = check_basic_imports()
    
    # فحص هيكل الملفات
    missing_files = check_file_structure()
    
    # فحص قاعدة البيانات
    check_database_files()
    
    # اختبار الاستيراد الرئيسي
    main_import_ok = test_main_import()
    
    # إنشاء اختبار مبسط
    create_minimal_test()
    
    # تقرير نهائي
    print("\n📊 تقرير التشخيص:")
    print("=" * 30)
    
    if python_ok:
        print("✅ Python: مناسب")
    else:
        print("❌ Python: يحتاج تحديث")
    
    if imports_status.get('tkinter') and imports_status.get('customtkinter'):
        print("✅ الاستيرادات الأساسية: متوفرة")
    else:
        print("❌ الاستيرادات الأساسية: ناقصة")
    
    if not missing_files:
        print("✅ هيكل الملفات: مكتمل")
    else:
        print(f"❌ هيكل الملفات: {len(missing_files)} ملف مفقود")
    
    if main_import_ok:
        print("✅ الملف الرئيسي: يعمل")
    else:
        print("❌ الملف الرئيسي: يحتاج إصلاح")
    
    # توصيات
    print("\n💡 التوصيات:")
    if not imports_status.get('customtkinter'):
        print("   📦 قم بتثبيت: pip install customtkinter")
    if not imports_status.get('PIL'):
        print("   📦 قم بتثبيت: pip install Pillow")
    if not imports_status.get('numpy'):
        print("   📦 قم بتثبيت: pip install numpy")
    
    if missing_files:
        print("   📁 تحقق من الملفات المفقودة")
    
    if not main_import_ok:
        print("   🔧 قم بتشغيل error_checker_and_fixer.py")
    
    print("\n🚀 لتشغيل اختبار بسيط: python test_simple.py")
    
    input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
