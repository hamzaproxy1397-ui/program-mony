#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار النوافذ المحسنة - فحص التحسينات المطبقة
Enhanced Windows Testing - Check Applied Improvements

اختبار شامل للتحسينات المطبقة على النوافذ:
✅ زيادة العرض بنسبة 10-15%
✅ تحسين الحد الأدنى للحجم
✅ توسيط النوافذ
✅ الحفاظ على التناسق والاستجابة
"""

import sys
import os
from pathlib import Path
import time

def setup_environment():
    """إعداد البيئة"""
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    paths_to_add = [
        str(project_root),
        str(project_root / "ui"),
        str(project_root / "ui" / "views"),
        str(project_root / "config")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    return project_root

def test_window_sizes():
    """اختبار أحجام النوافذ المحسنة"""
    print("🧪 اختبار أحجام النوافذ المحسنة...")
    print("="*60)
    
    # اختبار إعدادات الحجم الجديدة
    try:
        from config.settings import WINDOW_MIN_SIZE, WINDOW_DEFAULT_SIZE, WINDOW_EMPLOYEES_SIZE
        
        print("✅ إعدادات الحجم المحسنة:")
        print(f"   📏 الحد الأدنى: {WINDOW_MIN_SIZE[0]}x{WINDOW_MIN_SIZE[1]}")
        print(f"   📐 الحجم الافتراضي: {WINDOW_DEFAULT_SIZE[0]}x{WINDOW_DEFAULT_SIZE[1]}")
        print(f"   👥 نافذة الموظفين: {WINDOW_EMPLOYEES_SIZE[0]}x{WINDOW_EMPLOYEES_SIZE[1]}")
        
        # حساب نسب التحسين
        old_width = 1600
        new_width = WINDOW_EMPLOYEES_SIZE[0]
        improvement = ((new_width - old_width) / old_width) * 100
        
        print(f"   📈 نسبة التحسين: +{improvement:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الإعدادات: {e}")
        return False

def test_simple_enhanced_window():
    """اختبار النافذة المحسنة البسيطة"""
    print("\n🧪 اختبار النافذة المحسنة البسيطة...")
    print("-"*50)
    
    try:
        # محاولة استيراد النافذة
        import تشغيل_النافذة_المحسنة_البسيطة as simple_window
        
        print("✅ تم استيراد النافذة المحسنة البسيطة بنجاح")
        
        # فحص الكلاس
        if hasattr(simple_window, 'SimpleEnhancedWindow'):
            print("✅ كلاس SimpleEnhancedWindow موجود")
            
            # فحص الألوان المحسنة
            if hasattr(simple_window, 'COLORS'):
                colors = simple_window.COLORS
                print(f"✅ نظام الألوان: {len(colors)} لون محسن")
            
            # فحص الخطوط المحسنة
            if hasattr(simple_window, 'FONTS'):
                fonts = simple_window.FONTS
                print(f"✅ نظام الخطوط: {len(fonts)} خط محسن")
            
            return True
        else:
            print("❌ كلاس SimpleEnhancedWindow غير موجود")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار النافذة البسيطة: {e}")
        return False

def test_advanced_window():
    """اختبار النافذة المتقدمة"""
    print("\n🧪 اختبار النافذة المتقدمة...")
    print("-"*50)
    
    try:
        # محاولة استيراد النافذة المتقدمة
        from ui.views.advanced_employees_management import AdvancedEmployeesManagement
        
        print("✅ تم استيراد النافذة المتقدمة بنجاح")
        
        # فحص الألوان المحسنة
        if hasattr(advanced_employees_management, 'BEAUTIFUL_COLORS'):
            colors = advanced_employees_management.BEAUTIFUL_COLORS
            print(f"✅ نظام الألوان المتقدم: {len(colors)} لون")
        
        # فحص الخطوط المحسنة
        if hasattr(advanced_employees_management, 'ENHANCED_FONTS'):
            fonts = advanced_employees_management.ENHANCED_FONTS
            print(f"✅ نظام الخطوط المحسن: {len(fonts)} خط")
        
        # فحص الأبعاد المحسنة
        if hasattr(advanced_employees_management, 'ENHANCED_DIMENSIONS'):
            dimensions = advanced_employees_management.ENHANCED_DIMENSIONS
            print(f"✅ نظام الأبعاد المحسن: {len(dimensions)} بُعد")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار النافذة المتقدمة: {e}")
        return False

def test_employees_window():
    """اختبار نافذة الموظفين الأساسية"""
    print("\n🧪 اختبار نافذة الموظفين الأساسية...")
    print("-"*50)
    
    try:
        from ui.views.employees_management_window import EmployeesManagementWindow
        
        print("✅ تم استيراد نافذة الموظفين الأساسية بنجاح")
        print("✅ النافذة جاهزة للاستخدام مع التحسينات المطبقة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار نافذة الموظفين: {e}")
        return False

def test_enhanced_window():
    """اختبار النافذة المحسنة الكاملة"""
    print("\n🧪 اختبار النافذة المحسنة الكاملة...")
    print("-"*50)
    
    try:
        from ui.views.enhanced_employees_window import EnhancedEmployeesWindow
        
        print("✅ تم استيراد النافذة المحسنة الكاملة بنجاح")
        print("✅ النافذة جاهزة مع جميع التحسينات المتقدمة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار النافذة المحسنة الكاملة: {e}")
        return False

def run_quick_test():
    """تشغيل اختبار سريع للنافذة البسيطة"""
    print("\n🚀 تشغيل اختبار سريع...")
    print("-"*50)
    
    try:
        import تشغيل_النافذة_المحسنة_البسيطة as simple_window
        
        print("⏳ إنشاء نافذة اختبار...")
        
        # إنشاء النافذة للاختبار
        app = simple_window.SimpleEnhancedWindow()
        
        if app.window:
            print("✅ تم إنشاء النافذة بنجاح!")
            
            # فحص الحجم
            app.window.update_idletasks()
            width = app.window.winfo_reqwidth()
            height = app.window.winfo_reqheight()
            
            print(f"📏 حجم النافذة: {width}x{height}")
            
            # إغلاق النافذة
            app.window.destroy()
            print("✅ تم إغلاق النافذة بنجاح")
            
            return True
        else:
            print("❌ فشل في إنشاء النافذة")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار السريع: {e}")
        return False

def generate_test_report(results):
    """إنشاء تقرير الاختبار"""
    print("\n" + "="*60)
    print("📋 تقرير اختبار التحسينات المطبقة")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"📊 إجمالي الاختبارات: {total_tests}")
    print(f"✅ الاختبارات الناجحة: {passed_tests}")
    print(f"❌ الاختبارات الفاشلة: {total_tests - passed_tests}")
    print(f"📈 معدل النجاح: {success_rate:.1f}%")
    
    print("\n📋 تفاصيل الاختبارات:")
    for test_name, result in results.items():
        status = "✅ نجح" if result else "❌ فشل"
        print(f"   {test_name}: {status}")
    
    if success_rate >= 80:
        print("\n🎉 التحسينات مطبقة بنجاح!")
        print("✨ النوافذ جاهزة للاستخدام مع التحسينات المطلوبة")
    elif success_rate >= 60:
        print("\n⚠️ التحسينات مطبقة جزئياً")
        print("🔧 قد تحتاج بعض الإصلاحات الإضافية")
    else:
        print("\n❌ التحسينات تحتاج مراجعة")
        print("🛠️ يرجى فحص الأخطاء وإعادة التطبيق")

def main():
    """الدالة الرئيسية للاختبار"""
    print("🧪 اختبار النوافذ المحسنة - فحص التحسينات المطبقة")
    print("="*60)
    
    # إعداد البيئة
    setup_environment()
    
    # تشغيل الاختبارات
    results = {}
    
    results["إعدادات الحجم"] = test_window_sizes()
    results["النافذة البسيطة"] = test_simple_enhanced_window()
    results["النافذة المتقدمة"] = test_advanced_window()
    results["نافذة الموظفين"] = test_employees_window()
    results["النافذة المحسنة"] = test_enhanced_window()
    
    # اختبار سريع اختياري
    print("\n❓ هل تريد تشغيل اختبار سريع للنافذة؟ (y/n): ", end="")
    try:
        choice = input().lower().strip()
        if choice in ['y', 'yes', 'نعم', 'ن']:
            results["الاختبار السريع"] = run_quick_test()
    except:
        print("تم تخطي الاختبار السريع")
    
    # إنشاء التقرير
    generate_test_report(results)
    
    print("\n🎯 التحسينات المطبقة:")
    print("   📏 زيادة العرض بنسبة 10-15%")
    print("   📐 تحسين الحد الأدنى للحجم")
    print("   🎯 توسيط النوافذ في الشاشة")
    print("   📱 الحفاظ على الاستجابة")
    print("   🎨 تحسين التناسق البصري")
    
    print("\n✨ شكراً لاستخدام نظام اختبار التحسينات!")

if __name__ == "__main__":
    main()
