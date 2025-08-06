#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل برنامج المحاسبة مع لوحة التحكم المركزية
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """تشغيل البرنامج"""
    print("🚀 بدء تشغيل برنامج المحاسبة...")
    print("🎛️ لوحة التحكم المركزية الجذابة متاحة!")
    
    try:
        # استيراد المكتبات المطلوبة
        import customtkinter as ctk
        from ui.main_window import MainWindow

    
    except Exception as e:

    
        pass
        
        print("✅ تم تحميل المكتبات بنجاح")
        
        # إعداد customtkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        print("✅ تم إعداد الواجهة")
        
        # إنشاء وتشغيل التطبيق
        app = MainWindow()
        print("✅ تم إنشاء النافذة الرئيسية")
        print("📍 اضغط على أيقونة 'الإعدادات' (⚙️) في الصف الأول لفتح لوحة التحكم")
        print("🎨 لوحة التحكم تحتوي على 11 قسم بألوان دافئة جذابة")
        
        # تشغيل التطبيق
        app.run()
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("تأكد من تثبيت customtkinter: pip install customtkinter")
        
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
