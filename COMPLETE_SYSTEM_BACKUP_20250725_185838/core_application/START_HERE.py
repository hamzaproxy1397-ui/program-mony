#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎛️ لوحة التحكم المركزية المطورة
ابدأ من هنا - START HERE
"""

print("🎛️ لوحة التحكم المركزية المطورة")
print("=" * 50)

try:
    import customtkinter as ctk
    print("✅ customtkinter متوفر")
except ImportError:
    print("📦 تثبيت customtkinter...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'customtkinter'])
    import customtkinter as ctk
    print("✅ تم التثبيت بنجاح")

# تعيين المظهر
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# إنشاء النافذة
root = ctk.CTk()
root.title("🎛️ لوحة التحكم المركزية المطورة")
root.geometry("1400x900")

try:
    root.state('zoomed')
except:
    pass

# استيراد لوحة التحكم
from ui.central_control_panel import CentralControlPanel
import subprocess
import sys

# إنشاء لوحة التحكم
control_panel = CentralControlPanel(root)

print("🎉 تم تشغيل لوحة التحكم بنجاح!")
print("🔑 بيانات تسجيل الدخول:")
print("   اسم المستخدم: 123")
print("   كلمة المرور: 123")
print("🎮 اختصارات لوحة المفاتيح:")
print("   F11: تبديل ملء الشاشة")
print("   Ctrl+S: حفظ الإعدادات")
print("   Ctrl+R: تحديث لوحة التحكم")
print("   Escape: الخروج من ملء الشاشة")
print("=" * 50)

# تشغيل التطبيق
root.mainloop()
