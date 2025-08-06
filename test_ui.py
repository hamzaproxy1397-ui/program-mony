#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار الواجهة الجديدة
Test file for new UI
"""

import sys
import os
from pathlib import Path

# إضافة المسار الحالي
project_root = Path('.').absolute()
sys.path.insert(0, str(project_root))

try:
    print("🚀 بدء تشغيل اختبار الواجهة...")
    
    # استيراد المكتبات الأساسية
    import customtkinter as ctk
    print("✅ تم استيراد customtkinter")
    
    # استيراد الواجهة الرئيسية
    from ui.main_window import MainApplication
    print("✅ تم استيراد MainApplication")
    
    # إنشاء التطبيق
    print("🔧 إنشاء التطبيق...")
    app = MainApplication()
    print("✅ تم إنشاء التطبيق بنجاح")
    
    # تشغيل التطبيق
    print("🎯 تشغيل التطبيق...")
    app.run()
    
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("تأكد من تثبيت جميع المكتبات المطلوبة:")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ خطأ عام: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    print("🏁 انتهى الاختبار")
