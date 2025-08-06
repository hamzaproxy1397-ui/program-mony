#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تشغيل نافذة العرض الرئيسية
Test script for running the main window
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """اختبار الاستيرادات الأساسية"""
    try:
        print("🔍 اختبار الاستيرادات...")
        
        # اختبار customtkinter
        try:
            import customtkinter as ctk
            print("✅ customtkinter متوفر")
        except ImportError as e:
            print(f"❌ customtkinter غير متوفر: {e}")
            return False
        
        # اختبار tkinter
        try:
            import tkinter as tk
            print("✅ tkinter متوفر")
        except ImportError as e:
            print(f"❌ tkinter غير متوفر: {e}")
            return False
            
        # اختبار PIL
        try:
            from PIL import Image, ImageTk
            print("✅ PIL متوفر")
        except ImportError:
            print("⚠️ PIL غير متوفر - سيتم استخدام النص بدلاً من الصور")
            
        # اختبار numpy
        try:
            import numpy as np
            print("✅ numpy متوفر")
        except ImportError:
            print("⚠️ numpy غير متوفر - سيتم استخدام معالجة بديلة للصور")
            
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الاستيرادات: {e}")
        return False

def test_main_window():
    """اختبار تشغيل النافذة الرئيسية"""
    try:
        print("\n🚀 تشغيل النافذة الرئيسية...")
        
        # استيراد الكلاس الرئيسي
        from ui.main_window import MainApplication
        
        print("✅ تم استيراد MainApplication بنجاح")
        
        # إنشاء التطبيق
        app = MainApplication()
        print("✅ تم إنشاء التطبيق بنجاح")
        
        # تشغيل التطبيق
        print("🎉 تشغيل التطبيق...")
        print("📝 ملاحظة: لإغلاق التطبيق، أغلق النافذة أو اضغط Ctrl+C")
        
        app.run()
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("💡 تأكد من وجود جميع الملفات المطلوبة")
        return False
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True

def main():
    """الدالة الرئيسية"""
    print("🎛️ اختبار تشغيل برنامج ست الكل للمحاسبة")
    print("=" * 50)
    
    # اختبار الاستيرادات
    if not test_imports():
        print("\n❌ فشل في اختبار الاستيرادات")
        input("اضغط Enter للخروج...")
        return
    
    print("\n✅ جميع الاستيرادات الأساسية متوفرة")
    
    # اختبار تشغيل النافذة الرئيسية
    if test_main_window():
        print("\n✅ تم تشغيل التطبيق بنجاح")
    else:
        print("\n❌ فشل في تشغيل التطبيق")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
