#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل النافذة الرئيسية فقط بدون نافذة تسجيل الدخول
Run Main Window Only - No Login Required
"""

import sys
import os

def run_main_window():
    """تشغيل النافذة الرئيسية مباشرة"""
    try:
        # استيراد النافذة الرئيسية
        from ui.main_window import AccountingApp
        
        # إنشاء التطبيق
        app = AccountingApp()
        
        # تعيين مستخدم افتراضي
        app.current_user = {
            'username': 'admin',
            'role': 'admin'
        }
        
        # تشغيل النافذة الرئيسية
        app.create_main_window()
        
    except Exception as e:
        print(f"Error: {e}")
        # تشغيل البرنامج العادي كبديل
        try:
            import main
            main.main()
        except:
            pass

if __name__ == "__main__":
    run_main_window()
