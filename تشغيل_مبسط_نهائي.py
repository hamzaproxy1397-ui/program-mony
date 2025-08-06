#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل مبسط نهائي للبرنامج المحاسبي
Simple Final Launcher for Accounting Software
"""

import sys
import os
from pathlib import Path

def main():
    """تشغيل البرنامج بطريقة مبسطة"""
    print("🏢 برنامج ست الكل للمحاسبة")
    print("🚀 التشغيل المبسط النهائي")
    print("="*50)
    
    # إعداد المسارات
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    sys.path.insert(0, str(project_root))
    
    print(f"📁 مجلد المشروع: {project_root}")
    
    # فحص المكتبات الأساسية
    try:
        import customtkinter as ctk
        print("✅ customtkinter متوفر")
    except ImportError:
        print("❌ customtkinter غير متوفر")
        print("💡 ثبت المكتبة: pip install customtkinter")
        input("اضغط Enter للخروج...")
        return
    
    # إنشاء نافذة بسيطة للتأكد من عمل البرنامج
    try:
        print("\n🎯 إنشاء نافذة تجريبية...")
        
        root = ctk.CTk()
        root.title("🏢 برنامج ست الكل للمحاسبة - تجريبي")
        root.geometry("600x400")
        
        # عنوان رئيسي
        title = ctk.CTkLabel(
            root,
            text="🏢 برنامج ست الكل للمحاسبة",
            font=("Arial", 24, "bold"),
            text_color="#2E8B57"
        )
        title.pack(pady=30)
        
        # رسالة ترحيب
        welcome_msg = ctk.CTkLabel(
            root,
            text="مرحباً بك في البرنامج المحاسبي المتكامل\nالبرنامج يعمل بنجاح!",
            font=("Arial", 16),
            justify="center"
        )
        welcome_msg.pack(pady=20)
        
        # معلومات النظام
        info_frame = ctk.CTkFrame(root)
        info_frame.pack(pady=20, padx=40, fill="x")
        
        info_text = f"""
📊 حالة النظام: جاهز للاستخدام
🐍 Python: {sys.version.split()[0]}
📁 المجلد: {project_root.name}
✅ المكتبات: متوفرة
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text.strip(),
            font=("Arial", 12),
            justify="left"
        )
        info_label.pack(pady=15)
        
        # أزرار التحكم
        buttons_frame = ctk.CTkFrame(root)
        buttons_frame.pack(pady=20)
        
        # زر تشغيل البرنامج الكامل
        def run_full_program():
            try:
                root.destroy()
                print("\n🚀 تشغيل البرنامج الكامل...")
                import subprocess
                subprocess.run([sys.executable, "main.py"])
            except Exception as e:
                print(f"❌ خطأ في تشغيل البرنامج الكامل: {e}")
        
        full_btn = ctk.CTkButton(
            buttons_frame,
            text="🚀 تشغيل البرنامج الكامل",
            command=run_full_program,
            width=200,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#2E8B57"
        )
        full_btn.pack(side="left", padx=10)
        
        # زر إغلاق
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ إغلاق",
            command=root.destroy,
            width=100,
            height=40,
            font=("Arial", 14),
            fg_color="#dc3545"
        )
        close_btn.pack(side="left", padx=10)
        
        # معلومات إضافية
        footer = ctk.CTkLabel(
            root,
            text="تم تطوير البرنامج بواسطة شركة ست الكل للبرمجيات",
            font=("Arial", 10),
            text_color="gray"
        )
        footer.pack(side="bottom", pady=10)
        
        print("✅ تم إنشاء النافذة التجريبية بنجاح")
        print("🎉 البرنامج جاهز للاستخدام!")
        print("\n📋 تعليمات:")
        print("   - انقر 'تشغيل البرنامج الكامل' لتشغيل البرنامج")
        print("   - أو أغلق هذه النافذة واستخدم ملفات التشغيل الأخرى")
        
        root.mainloop()
        
        print("\n✅ تم إغلاق النافذة التجريبية")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء النافذة التجريبية: {e}")
        print("\n💡 جرب:")
        print("   1. python main.py")
        print("   2. تشغيل_البرنامج_النهائي.py")
        print("   3. 🚀_تشغيل_البرنامج_النهائي_المحسن.bat")
        
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
