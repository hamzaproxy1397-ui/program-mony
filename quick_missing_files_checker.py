#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فاحص سريع للملفات المفقودة
Quick Missing Files Checker for Arabic Accounting Software
"""

import os
from pathlib import Path

def check_missing_files():
    """فحص سريع للملفات المفقودة"""
    
    # الملفات المطلوبة من main_window.py
    required_files = [
        # UI Files
        'ui/login_window.py',
        'ui/window_utils.py',
        'ui/simple_welcome_window.py',
        'ui/warehouses_management_window.py',
        'ui/purchases_window.py',
        'ui/sales_window.py',
        'ui/reports_window.py',
        'ui/advanced_financial_reports_window.py',
        'ui/accounts_window.py',
        'ui/journal_entries_window.py',
        'ui/add_items_window.py',
        'ui/categories_management_window.py',
        'ui/units_management_window.py',
        'ui/stock_management_window.py',
        'ui/user_management.py',
        'ui/hr_management_window.py',
        'ui/invoices_main_window.py',
        'ui/central_control_panel.py',
        
        # Database Files
        'database/hybrid_database_manager.py',
        'database/database_manager.py',
        'database/accounts_manager.py',
        'database/products_manager.py',
        'database/invoices_manager.py',
        'database/reports_manager.py',
        
        # Config Files
        'themes/theme_manager.py',
        'themes/modern_theme.py',
        'config/settings.py',
        'core/error_handler.py',
        'core/barcode_scanner.py',
        
        # Asset Files
        'assets/logo/222555.png',
        'assets/icons/6.png',
        'assets/icons/3.png',
        'assets/icons/23.png',
        'assets/icons/26.png',
        'assets/icons/53.ico',
        'assets/icons/12.png'
    ]
    
    print("🔍 فحص سريع للملفات المطلوبة...")
    print("=" * 50)
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print("\n" + "=" * 50)
    print("📊 ملخص الفحص:")
    print(f"✅ ملفات موجودة: {len(existing_files)}")
    print(f"❌ ملفات مفقودة: {len(missing_files)}")
    
    if missing_files:
        print("\n📋 الملفات المفقودة:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        
        print("\n💡 لإنشاء الملفات المفقودة، شغل:")
        print("   python comprehensive_dependency_checker.py")
    else:
        print("\n🎉 جميع الملفات المطلوبة موجودة!")
    
    return missing_files, existing_files

def check_packages():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات المطلوبة...")
    print("-" * 30)
    
    packages = ['customtkinter', 'PIL', 'numpy', 'matplotlib']
    missing_packages = []
    
    for package in packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 مكتبات مفقودة: {len(missing_packages)}")
        print("💡 لتثبيت المكتبات المفقودة:")
        for package in missing_packages:
            package_name = 'Pillow' if package == 'PIL' else package
            print(f"   pip install {package_name}")
    else:
        print("\n🎉 جميع المكتبات مثبتة!")
    
    return missing_packages

def main():
    """الدالة الرئيسية"""
    print("🔍 فاحص سريع للملفات والتبعيات المفقودة")
    print("=" * 60)
    
    # فحص الملفات
    missing_files, existing_files = check_missing_files()
    
    # فحص المكتبات
    missing_packages = check_packages()
    
    # تقرير نهائي
    print("\n" + "=" * 60)
    print("📊 التقرير النهائي:")
    print("=" * 60)
    
    if not missing_files and not missing_packages:
        print("🎉 البرنامج جاهز للتشغيل!")
        print("✅ جميع الملفات والمكتبات متوفرة")
        print("\n🚀 يمكنك تشغيل البرنامج الآن:")
        print("   python main.py")
    else:
        print("⚠️ هناك ملفات أو مكتبات مفقودة")
        print("\n🔧 للإصلاح التلقائي:")
        print("   python comprehensive_dependency_checker.py")
        print("\n📦 أو ثبت المكتبات يدوياً:")
        print("   pip install customtkinter pillow numpy matplotlib")
    
    input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
