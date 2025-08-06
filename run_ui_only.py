#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل الواجهة الرئيسية فقط - بدون قاعدة البيانات
Run main UI only - without database
"""

import sys
import os
from pathlib import Path

# إضافة المسار الحالي
project_root = Path('.').absolute()
sys.path.insert(0, str(project_root))

try:
    print("🚀 بدء تشغيل الواجهة الرئيسية...")
    
    # استيراد المكتبات الأساسية
    import customtkinter as ctk
    print("✅ تم استيراد customtkinter")
    
    # تعطيل استيراد قاعدة البيانات مؤقتاً
    import sys
    
    # إنشاء mock لقاعدة البيانات
    class MockDatabaseManager:
        def __init__(self):
            pass
        def get_connection(self):
            return None
        def close_connection(self):
            pass
    
    # إضافة mock إلى sys.modules
    sys.modules['database.hybrid_database_manager'] = type('MockModule', (), {
        'HybridDatabaseManager': MockDatabaseManager
    })()
    
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
    print("pip install customtkinter pillow")
    
except Exception as e:
    print(f"❌ خطأ عام: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    print("🏁 انتهى التشغيل")
