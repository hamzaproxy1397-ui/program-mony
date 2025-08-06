# -*- coding: utf-8 -*-
"""
اختبار تكامل نظام الإعدادات
Settings Integration Test
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_settings_import():
    """اختبار استيراد نظام الإعدادات"""
    try:
        from core.settings_manager import SettingsManager
        print("✅ تم استيراد SettingsManager بنجاح")
        
        # اختبار إنشاء مثيل
        settings = SettingsManager()
        print("✅ تم إنشاء مثيل SettingsManager بنجاح")
        
        # اختبار تحميل الإعدادات
        settings.load_settings()
        print("✅ تم تحميل الإعدادات بنجاح")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في استيراد نظام الإعدادات: {e}")
        return False

def test_control_panel_import():
    """اختبار استيراد لوحة التحكم"""
    try:
        from control_panel.control_panel_window import ControlPanelWindow
        print("✅ تم استيراد ControlPanelWindow بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في استيراد لوحة التحكم: {e}")
        return False

def test_settings_pages_import():
    """اختبار استيراد صفحات الإعدادات"""
    pages = [
        ("general_settings", "control_panel.settings_pages.general_settings", "GeneralSettingsPage"),
        ("company_settings", "control_panel.settings_pages.company_settings", "CompanySettingsPage"),
        ("accounting_settings", "control_panel.settings_pages.accounting_settings", "AccountingSettingsPage")
    ]
    
    success_count = 0
    
    for page_name, module_path, class_name in pages:
        try:
            module = __import__(module_path, fromlist=[class_name])
            page_class = getattr(module, class_name)
            print(f"✅ تم استيراد {page_name} بنجاح")
            success_count += 1
        except Exception as e:
            print(f"❌ خطأ في استيراد {page_name}: {e}")
    
    return success_count == len(pages)

def test_customtkinter_availability():
    """اختبار توفر CustomTkinter"""
    try:
        import customtkinter as ctk
        print(f"✅ CustomTkinter متوفر - الإصدار: {ctk.__version__}")
        return True
    except ImportError:
        print("❌ CustomTkinter غير متوفر")
        return False

def test_pil_availability():
    """اختبار توفر PIL/Pillow"""
    try:
        from PIL import Image, ImageTk
        print("✅ PIL/Pillow متوفر")
        return True
    except ImportError:
        print("❌ PIL/Pillow غير متوفر")
        return False

def test_file_structure():
    """اختبار هيكل الملفات"""
    required_files = [
        "large_font_run.py",
        "core/settings_manager.py",
        "control_panel/control_panel_window.py",
        "control_panel/settings_pages/general_settings.py",
        "control_panel/settings_pages/company_settings.py",
        "control_panel/settings_pages/accounting_settings.py",
        "control_panel/styles.qss"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ ملفات مفقودة:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True

def run_comprehensive_test():
    """تشغيل الاختبار الشامل"""
    print("🧪 بدء اختبار تكامل نظام الإعدادات...")
    print("=" * 60)
    
    tests = [
        ("هيكل الملفات", test_file_structure),
        ("CustomTkinter", test_customtkinter_availability),
        ("PIL/Pillow", test_pil_availability),
        ("نظام الإعدادات", test_settings_import),
        ("لوحة التحكم", test_control_panel_import),
        ("صفحات الإعدادات", test_settings_pages_import)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 اختبار {test_name}...")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: نجح")
            else:
                print(f"❌ {test_name}: فشل")
        except Exception as e:
            print(f"❌ {test_name}: خطأ - {e}")
    
    print(f"\n📊 نتائج الاختبار:")
    print(f"   ✅ اختبارات نجحت: {passed_tests}/{total_tests}")
    print(f"   ❌ اختبارات فشلت: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام.")
        return True
    else:
        print("⚠️ بعض الاختبارات فشلت. يحتاج النظام إلى إصلاحات.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
