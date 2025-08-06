#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار لوحة التحكم المركزية المطورة
تشغيل جميع الأقسام الـ11 المطورة بالتفصيل
"""

import sys
import os
from pathlib import Path

# إضافة المجلد الجذر للمشروع إلى مسار Python
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import customtkinter as ctk
from tkinter import messagebox
import traceback

# تعيين مظهر CustomTkinter
ctk.set_appearance_mode("light")  # أو "dark" أو "system"
ctk.set_default_color_theme("blue")

def main():
    """الدالة الرئيسية لتشغيل لوحة التحكم"""
    try:
        # إنشاء النافذة الرئيسية
        root = ctk.CTk()
        root.title("🎛️ لوحة التحكم المركزية المطورة - نظام المحاسبة الشامل")
        root.geometry("1400x900")
        root.state('zoomed')  # ملء الشاشة في Windows
        
        # تعيين أيقونة النافذة (إذا كانت متوفرة)
        try:
            root.iconbitmap("assets/icons/control_panel.ico")
        except:
            pass  # تجاهل إذا لم تكن الأيقونة متوفرة
        
        # استيراد وإنشاء لوحة التحكم
        from ui.central_control_panel import CentralControlPanel
        
        # إنشاء لوحة التحكم
        control_panel = CentralControlPanel(root)
        
        # رسالة ترحيب
        welcome_message = """
🎉 مرحباً بك في لوحة التحكم المركزية المطورة!

✨ الميزات الجديدة:
• 🧾 إعدادات الفواتير المتقدمة مع قوالب متعددة
• 💰 نظام الرواتب والضرائب الشامل
• 🏪 إدارة المخازن مع تكامل الباركود
• 👥 إدارة المستخدمين والصلاحيات المفصلة
• 🔧 التحكم الكامل في الموديلات
• 💾 نظام النسخ الاحتياطي المتقدم
• 📊 استيراد وتصدير البيانات
• 🎨 تخصيص الواجهة والثيمات
• 🛡️ نظام الأمان المتطور
• 🔢 الأرقام التسلسلية القابلة للتخصيص
• ⚙️ إعدادات النظام الشاملة

🚀 استكشف جميع الأقسام واستمتع بالتحكم الكامل في نظامك!
        """
        
        # عرض رسالة الترحيب
        messagebox.showinfo("🎛️ لوحة التحكم المطورة", welcome_message)
        
        # بدء حلقة الأحداث
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"""
❌ خطأ في الاستيراد:
{str(e)}

🔧 تأكد من وجود الملفات التالية:
• ui/central_control_panel.py
• ui/advanced_sections.py
• ui/advanced_sections_part2.py
• ui/control_panel_integration.py
• themes/modern_theme.py
• config/settings.py

📁 تأكد من أن جميع المجلدات موجودة في المسار الصحيح.
        """
        messagebox.showerror("خطأ في الاستيراد", error_msg)
        print(f"Import Error: {e}")
        traceback.print_exc()
        
    except Exception as e:
        error_msg = f"""
❌ حدث خطأ غير متوقع:
{str(e)}

🔍 تفاصيل الخطأ:
{traceback.format_exc()}

💡 نصائح لحل المشكلة:
• تأكد من تثبيت customtkinter: pip install customtkinter
• تأكد من وجود جميع الملفات المطلوبة
• تحقق من صحة مسارات الملفات
• تأكد من صلاحيات الكتابة في مجلد المشروع
        """
        messagebox.showerror("خطأ في التشغيل", error_msg)
        print(f"Runtime Error: {e}")
        traceback.print_exc()

def check_dependencies():
    """فحص التبعيات المطلوبة"""
    missing_deps = []
    
    try:
        import customtkinter
        print("✅ customtkinter متوفر")
    except ImportError:
        missing_deps.append("customtkinter")
    
    try:
        import tkinter
        print("✅ tkinter متوفر")
    except ImportError:
        missing_deps.append("tkinter")
    
    # فحص الملفات المطلوبة
    required_files = [
        "ui/central_control_panel.py",
        "ui/advanced_sections.py", 
        "ui/advanced_sections_part2.py",
        "ui/control_panel_integration.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path} موجود")
    
    if missing_deps:
        print(f"❌ مكتبات مفقودة: {', '.join(missing_deps)}")
        print("💡 قم بتثبيتها باستخدام: pip install " + " ".join(missing_deps))
        return False
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {', '.join(missing_files)}")
        return False
    
    print("🎉 جميع التبعيات والملفات متوفرة!")
    return True

def create_demo_data():
    """إنشاء بيانات تجريبية للاختبار"""
    try:
        # إنشاء مجلدات الإعدادات إذا لم تكن موجودة
        settings_dir = Path("data/settings")
        settings_dir.mkdir(parents=True, exist_ok=True)
        
        # إنشاء مجلد الأصول
        assets_dir = Path("assets/icons")
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ تم إنشاء المجلدات المطلوبة")
        
    except Exception as e:
        print(f"⚠️ تحذير: لم يتم إنشاء بعض المجلدات: {e}")

if __name__ == "__main__":
    print("🚀 بدء تشغيل لوحة التحكم المركزية المطورة...")
    print("=" * 60)
    
    # فحص التبعيات
    print("🔍 فحص التبعيات...")
    if not check_dependencies():
        print("❌ فشل في فحص التبعيات. يرجى حل المشاكل أولاً.")
        input("اضغط Enter للخروج...")
        sys.exit(1)
    
    # إنشاء البيانات التجريبية
    print("\n📁 إنشاء المجلدات المطلوبة...")
    create_demo_data()
    
    # تشغيل التطبيق
    print("\n🎛️ تشغيل لوحة التحكم...")
    print("=" * 60)
    main()
    
    print("\n👋 تم إغلاق لوحة التحكم. شكراً لاستخدام النظام!")
