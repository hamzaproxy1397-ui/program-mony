#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل مباشر للبرنامج المحاسبي
Direct Launch for Accounting Software
"""

import sys
import os
from pathlib import Path

def main():
    """تشغيل البرنامج مباشرة"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🚀 تشغيل مباشر")
    print("="*50)
    
    # إعداد المسارات
    project_root = Path(__file__).parent
    os.chdir(project_root)
    sys.path.insert(0, str(project_root))
    
    print(f"📁 مجلد المشروع: {project_root}")
    
    # فحص الملفات الأساسية
    main_files = [
        "main.py",
        "ui/views/main_window.py",
        "🚀_تشغيل_البرنامج_النهائي_المحسن.bat"
    ]
    
    print("\n📋 فحص الملفات...")
    for file_path in main_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    # محاولة تشغيل main.py
    if os.path.exists("main.py"):
        print("\n🚀 تشغيل main.py...")
        try:
            import main
            main.main()
            return
        except Exception as e:
            print(f"❌ خطأ في main.py: {e}")
    
    # محاولة تشغيل البرنامج المحسن
    if os.path.exists("🚀_تشغيل_البرنامج_النهائي_المحسن.bat"):
        print("\n🚀 تشغيل الملف المحسن...")
        try:
            import subprocess
            subprocess.run(["🚀_تشغيل_البرنامج_النهائي_المحسن.bat"], shell=True)
            return
        except Exception as e:
            print(f"❌ خطأ في الملف المحسن: {e}")
    
    # محاولة أخيرة - تشغيل مباشر
    print("\n🔄 محاولة تشغيل مباشر...")
    try:
        import customtkinter as ctk
        
        # إنشاء نافذة بسيطة
        root = ctk.CTk()
        root.title("🏢 برنامج ست الكل للمحاسبة")
        root.geometry("800x600")
        
        # عنوان
        title = ctk.CTkLabel(
            root,
            text="🏢 برنامج ست الكل للمحاسبة",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=50)
        
        # رسالة
        message = ctk.CTkLabel(
            root,
            text="البرنامج جاهز للاستخدام\nيرجى استخدام ملفات التشغيل المحسنة",
            font=("Arial", 16)
        )
        message.pack(pady=20)
        
        # زر إغلاق
        close_btn = ctk.CTkButton(
            root,
            text="إغلاق",
            command=root.destroy,
            width=200,
            height=40
        )
        close_btn.pack(pady=30)
        
        print("✅ تم إنشاء نافذة بسيطة")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ خطأ في التشغيل المباشر: {e}")
        print("\n💡 للتشغيل الصحيح:")
        print("   1. استخدم: 🚀_تشغيل_البرنامج_النهائي_المحسن.bat")
        print("   2. أو استخدم: python main.py")
        print("   3. تأكد من تثبيت: pip install customtkinter pillow")

if __name__ == "__main__":
    main()
