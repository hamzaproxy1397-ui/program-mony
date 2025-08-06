#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء الهيكل المعماري الجديد لبرنامج ست الكل للمحاسبة
"""

import os
from pathlib import Path

def create_directory_structure():
    """إنشاء الهيكل المعماري الجديد"""
    
    # الهيكل المطلوب
    directories = [
        # مجلدات النواة الأساسية
        "core/accounting",
        "core/sales", 
        "core/purchases",
        "core/inventory",
        "core/warehouse",
        "core/hr",
        "core/pos",
        "core/crm",
        "core/projects",
        "core/reports",
        "core/security",
        
        # محرك المبيعات الذكي
        "sales_engine",
        
        # نماذج البيانات
        "models",
        
        # واجهة المستخدم الجديدة
        "ui/views",
        "ui/components",
        
        # الخدمات المساعدة
        "services",
        
        # الملفات الثابتة
        "static/fonts",
        
        # ملفات الترجمة
        "translations",
        
        # ملفات التكوين (موجود بالفعل)
        # "config" - موجود
    ]
    
    print("🏗️ إنشاء الهيكل المعماري الجديد...")
    
    created_dirs = []
    existing_dirs = []
    
    for directory in directories:
        dir_path = Path(directory)
        
        if dir_path.exists():
            existing_dirs.append(directory)
            print(f"✅ موجود بالفعل: {directory}")
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(directory)
                print(f"🆕 تم إنشاء: {directory}")
            except Exception as e:
                print(f"❌ خطأ في إنشاء {directory}: {e}")
    
    # إنشاء ملفات __init__.py للمجلدات الجديدة
    init_files = []
    for directory in directories:
        init_file = Path(directory) / "__init__.py"
        if not init_file.exists():
            try:
                init_file.write_text("# -*- coding: utf-8 -*-\n", encoding='utf-8')
                init_files.append(str(init_file))
                print(f"📄 تم إنشاء: {init_file}")
            except Exception as e:
                print(f"❌ خطأ في إنشاء {init_file}: {e}")
    
    print("\n" + "="*60)
    print("📊 ملخص إنشاء الهيكل")
    print("="*60)
    print(f"🆕 مجلدات جديدة: {len(created_dirs)}")
    print(f"✅ مجلدات موجودة: {len(existing_dirs)}")
    print(f"📄 ملفات __init__.py: {len(init_files)}")
    
    if created_dirs:
        print("\n🆕 المجلدات الجديدة:")
        for d in created_dirs:
            print(f"   - {d}")
    
    return created_dirs, existing_dirs, init_files

if __name__ == "__main__":
    create_directory_structure()
