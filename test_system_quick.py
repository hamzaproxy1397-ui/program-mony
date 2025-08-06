#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع للنظام المتقدم
"""

import sys
import os
sys.path.append('.')

def test_import():
    """اختبار استيراد النظام"""
    try:
        print("🔍 اختبار استيراد النظام...")
        from windows.advanced_item_entry_comprehensive import AdvancedItemEntryComprehensive
        print("✅ تم استيراد النظام بنجاح!")
        return True
    except Exception as e:
        print(f"❌ فشل في استيراد النظام: {e}")
        return False

def test_initialization():
    """اختبار تهيئة النظام"""
    try:
        print("🔍 اختبار تهيئة النظام...")
        from windows.advanced_item_entry_comprehensive import AdvancedItemEntryComprehensive
        
        # إنشاء النظام بدون عرض النافذة
        app = AdvancedItemEntryComprehensive()
        print("✅ تم تهيئة النظام بنجاح!")
        
        # إغلاق النافذة
        app.window.destroy()
        return True
    except Exception as e:
        print(f"❌ فشل في تهيئة النظام: {e}")
        return False

def main():
    """تشغيل الاختبارات"""
    print("🚀 بدء اختبار النظام المتقدم...")
    print("=" * 50)
    
    tests = [
        ("استيراد النظام", test_import),
        ("تهيئة النظام", test_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 النتائج النهائية:")
    print(f"✅ نجح: {passed}/{total}")
    print(f"❌ فشل: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام.")
        return True
    else:
        print("⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
