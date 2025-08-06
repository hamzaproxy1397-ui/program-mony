#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نسخة آمنة من البرنامج الرئيسي
Safe version of main program - تجنب الملفات المشكلة مؤقتاً
"""

import sys
import os
import logging
from pathlib import Path

# إضافة المسار الجذر للمشروع
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# إعداد نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """تشغيل البرنامج الآمن"""
    try:
        print("🚀 بدء تشغيل برنامج المحاسبة العربي...")
        print("=" * 60)
        
        # استيراد المكتبات الأساسية
        import customtkinter as ctk
        from tkinter import messagebox
        
        print("✅ تم استيراد المكتبات الأساسية بنجاح")
        
        # تهيئة قاعدة البيانات
        try:
            from database.hybrid_database_manager import HybridDatabaseManager
            db_manager = HybridDatabaseManager()
            print("✅ تم تهيئة قاعدة البيانات بنجاح")
        except Exception as e:
            print(f"⚠️  تحذير في قاعدة البيانات: {e}")
            db_manager = None
        
        # تهيئة مدير المهام المجدولة
        try:
            from core.scheduler_manager import SchedulerManager
            scheduler_manager = SchedulerManager()
            scheduler_manager.start()
            print("✅ تم تشغيل نظام الجدولة التلقائية للنسخ الاحتياطي")
        except Exception as e:
            print(f"⚠️  تحذير في مدير المهام: {e}")
            scheduler_manager = None
        
        # تهيئة نظام المصادقة
        try:
            from auth.auth_manager import AuthManager
            auth_manager = AuthManager()
            print("✅ تم تهيئة نظام المصادقة")
        except Exception as e:
            print(f"⚠️  تحذير في نظام المصادقة: {e}")
            auth_manager = None
        
        # تشغيل نافذة تسجيل الدخول
        try:
            from ui.login_window import LoginWindow
            
            # إنشاء النافذة الرئيسية المخفية
            root = ctk.CTk()
            root.withdraw()  # إخفاء النافذة الرئيسية
            
            # تطبيق الثيم
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            
            print("✅ تم إنشاء النافذة الأساسية")
            
            # إنشاء نافذة تسجيل الدخول
            login_window = LoginWindow(
                parent=root,
                db_manager=db_manager,
                auth_manager=auth_manager,
                scheduler_manager=scheduler_manager
            )
            
            print("✅ تم إنشاء نافذة تسجيل الدخول")
            print("🎯 البرنامج جاهز للاستخدام!")
            print("=" * 60)
            
            # تشغيل الحلقة الرئيسية
            root.mainloop()
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل واجهة المستخدم: {e}")
            logger.error(f"خطأ في تشغيل واجهة المستخدم: {e}")
            
            # محاولة تشغيل لوحة التحكم الشاملة كبديل
            try:
                print("\n🎛️  محاولة تشغيل لوحة التحكم الشاملة...")
                from ui.advanced_settings_window import ComprehensiveAdminPanel
            except Exception as e:
                pass
from tkinter import messagebox
import re
                
                root = ctk.CTk()
                root.withdraw()
                
                admin_panel = ComprehensiveAdminPanel()
                print("✅ تم تشغيل لوحة التحكم الشاملة بنجاح!")
                
                root.mainloop()
                
            except Exception as e2:
                print(f"❌ خطأ في تشغيل لوحة التحكم: {e2}")
                messagebox.showerror("خطأ", f"فشل في تشغيل البرنامج:\n{str(e)}\n\nلوحة التحكم:\n{str(e2)}")
        
        # تنظيف الموارد
        try:
            if scheduler_manager:
                scheduler_manager.shutdown()
                print("✅ تم إيقاف مدير المهام المجدولة")
        except Exception as e:
            print(f"⚠️  تحذير في إيقاف المهام: {e}")
            
    except ImportError as e:
        error_msg = f"خطأ في استيراد المكتبات المطلوبة: {str(e)}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        
        try:
            messagebox.showerror("خطأ في المكتبات", 
                               f"{error_msg}\n\nتأكد من تثبيت:\n- customtkinter\n- pillow\n- apscheduler")
        except:
            print("تأكد من تثبيت المكتبات المطلوبة:")
            print("pip install customtkinter pillow apscheduler")
            
    except Exception as e:
        error_msg = f"خطأ عام في تشغيل البرنامج: {str(e)}"
        print(f"❌ {error_msg}")
        logger.error(error_msg, exc_info=True)
        
        try:
            messagebox.showerror("خطأ", error_msg)
        except:
            pass

if __name__ == "__main__":
    # إنشاء مجلد السجلات إذا لم يكن موجوداً
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    main()
