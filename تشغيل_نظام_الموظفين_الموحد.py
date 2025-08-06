#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 تشغيل نظام إدارة الموظفين الموحد والمتطور
Unified Advanced Employee Management System Launcher

نظام شامل يجمع بين البساطة والتقدم التقني
يدمج جميع ميزات النظام الأساسي والمتقدم في واجهة واحدة موحدة
"""

import sys
import os
from pathlib import Path
import traceback

def setup_environment():
    """إعداد البيئة والمسارات"""
    try:
        # الحصول على مجلد المشروع
        project_root = Path(__file__).parent.absolute()
        os.chdir(project_root)
        
        # إضافة المسارات المطلوبة
        paths_to_add = [
            str(project_root),
            str(project_root / "ui"),
            str(project_root / "ui" / "views"),
            str(project_root / "config"),
            str(project_root / "themes"),
            str(project_root / "data"),
            str(project_root / "reports")
        ]
        
        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)
        
        print("✅ تم إعداد البيئة بنجاح")
        return project_root
        
    except Exception as e:
        print(f"❌ خطأ في إعداد البيئة: {e}")
        raise

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    try:
        print("🔍 فحص المكتبات المطلوبة...")
        
        # المكتبات الأساسية
        required_packages = {
            'customtkinter': 'customtkinter',
            'tkinter': 'tkinter (مدمج مع Python)',
            'sqlite3': 'sqlite3 (مدمج مع Python)',
            'pathlib': 'pathlib (مدمج مع Python)',
            'datetime': 'datetime (مدمج مع Python)'
        }
        
        missing_packages = []
        
        for package, description in required_packages.items():
            try:
                if package == 'customtkinter':
                    import customtkinter
                elif package == 'tkinter':
                    import tkinter
                elif package == 'sqlite3':
                    import sqlite3
                elif package == 'pathlib':
                    from pathlib import Path
                elif package == 'datetime':
                    from datetime import datetime
                
                print(f"  ✅ {description}")
                
            except ImportError:
                missing_packages.append((package, description))
                print(f"  ❌ {description}")
        
        # المكتبات الاختيارية
        optional_packages = {
            'PIL': 'Pillow (للصور)',
            'matplotlib': 'matplotlib (للرسوم البيانية)',
            'numpy': 'numpy (للتحليلات المتقدمة)'
        }
        
        print("\n🔍 فحص المكتبات الاختيارية...")
        
        for package, description in optional_packages.items():
            try:
                if package == 'PIL':
                    from PIL import Image
                elif package == 'matplotlib':
                    import matplotlib.pyplot as plt
                elif package == 'numpy':
                    import numpy as np
                
                print(f"  ✅ {description}")
                
            except ImportError:
                print(f"  ⚠️ {description} - غير متوفر (اختياري)")
        
        if missing_packages:
            print(f"\n❌ المكتبات المفقودة: {len(missing_packages)}")
            for package, description in missing_packages:
                print(f"  - {description}")
            
            print("\n💡 لتثبيت المكتبات المفقودة:")
            if any('customtkinter' in pkg for pkg, _ in missing_packages):
                print("  pip install customtkinter")
            
            return False
        
        print("\n✅ جميع المكتبات الأساسية متوفرة")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص المكتبات: {e}")
        return False

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    try:
        directories = [
            "data",
            "reports", 
            "exports",
            "backups",
            "logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ مجلد {directory} جاهز")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء المجلدات: {e}")
        return False

def run_unified_system():
    """تشغيل النظام الموحد"""
    try:
        print("🚀 بدء تشغيل نظام إدارة الموظفين الموحد...")
        
        # استيراد النظام الموحد
        from ui.views.unified_employees_management import UnifiedEmployeesManagement
        
        # إنشاء وتشغيل النظام
        unified_system = UnifiedEmployeesManagement()
        unified_system.run()
        
        print("✅ تم إغلاق النظام بنجاح")
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد النظام الموحد: {e}")
        print("💡 تأكد من وجود ملف unified_employees_management.py في مجلد ui/views/")
        raise
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام الموحد: {e}")
        traceback.print_exc()
        raise

def main():
    """الدالة الرئيسية"""
    try:
        print("=" * 60)
        print("🏢 نظام إدارة الموظفين الموحد والمتطور")
        print("   Unified Advanced Employee Management System")
        print("=" * 60)
        print()
        
        # إعداد البيئة
        print("1️⃣ إعداد البيئة...")
        project_root = setup_environment()
        print(f"   📁 مجلد المشروع: {project_root}")
        print()
        
        # فحص المكتبات
        print("2️⃣ فحص المكتبات...")
        if not check_dependencies():
            print("\n❌ فشل في فحص المكتبات - يرجى تثبيت المكتبات المفقودة")
            input("اضغط Enter للخروج...")
            return
        print()
        
        # إنشاء المجلدات
        print("3️⃣ إنشاء المجلدات...")
        if not create_directories():
            print("\n❌ فشل في إنشاء المجلدات")
            input("اضغط Enter للخروج...")
            return
        print()
        
        # تشغيل النظام
        print("4️⃣ تشغيل النظام الموحد...")
        print("   🎯 النظام يجمع بين:")
        print("      • الوظائف الأساسية لإدارة الموظفين")
        print("      • التحليلات المتقدمة والذكية")
        print("      • التقارير الشاملة")
        print("      • واجهة موحدة وسهلة الاستخدام")
        print()
        
        run_unified_system()
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف النظام بواسطة المستخدم")
        
    except Exception as e:
        print(f"\n❌ خطأ فادح في النظام: {e}")
        traceback.print_exc()
        print("\n💡 يرجى التحقق من:")
        print("   • تثبيت جميع المكتبات المطلوبة")
        print("   • صحة ملفات النظام")
        print("   • أذونات الكتابة في مجلد المشروع")
        
    finally:
        print("\n" + "=" * 60)
        print("شكراً لاستخدام نظام إدارة الموظفين الموحد")
        print("=" * 60)
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
