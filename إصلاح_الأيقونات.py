#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 أداة إصلاح الأيقونات في النافذة الرئيسية
Icon Fix Tool for Main Window

إصلاح مسارات الأيقونات وتحويلها من .png/.jpg إلى .ico
"""

import os
import shutil
from pathlib import Path

def scan_available_icons():
    """فحص الأيقونات المتاحة"""
    icons_dir = Path("assets/icons")
    if not icons_dir.exists():
        print("❌ مجلد الأيقونات غير موجود")
        return {}
    
    available_icons = {}
    for icon_file in icons_dir.glob("*"):
        if icon_file.is_file():
            name = icon_file.stem
            ext = icon_file.suffix
            available_icons[name] = str(icon_file)
    
    print(f"📁 تم العثور على {len(available_icons)} أيقونة")
    return available_icons

def create_icon_mapping():
    """إنشاء خريطة الأيقونات المطلوبة"""
    # الأيقونات المطلوبة للشريط الأخضر
    green_icons_needed = [
        ("employees", "الموظفين"),
        ("48", "المحاسبة"),
        ("43", "الحسابات"),
        ("40", "الخزينة"),
        ("5", "الفواتير"),
        ("4", "التقارير")
    ]
    
    # الأيقونات المطلوبة للصف الأول
    first_row_icons_needed = [
        ("welcome", "أهلاً بكم"),
        ("settings", "إعداد"),
        ("items", "إدخال الأصناف"),
        ("accounts", "إدخال الحسابات"),
        ("daily", "الحركة اليومية"),
        ("analysis", "تحليل المبيعات")
    ]
    
    # الأيقونات المطلوبة للصف الثاني
    second_row_icons_needed = [
        ("warehouse", "مخزن"),
        ("sell", "بيع"),
        ("buy", "شراء"),
        ("expense", "صرف"),
        ("indicators", "مؤشرات"),
        ("return_sell", "مرتجع بيع")
    ]
    
    # الأيقونات المطلوبة للصف الثالث
    third_row_icons_needed = [
        ("quote", "عرض أسعار"),
        ("return_buy", "مرتجع شراء"),
        ("quantity", "كمية"),
        ("transfer", "تحويل لمخزن"),
        ("inventory", "تسوية مخزن"),
        ("reports", "مؤشرات")
    ]
    
    return {
        "green_icons": green_icons_needed,
        "first_row": first_row_icons_needed,
        "second_row": second_row_icons_needed,
        "third_row": third_row_icons_needed
    }

def map_available_to_needed(available_icons, needed_mapping):
    """ربط الأيقونات المتاحة بالمطلوبة"""
    mapping_results = {}
    
    for category, icons_list in needed_mapping.items():
        mapping_results[category] = []
        
        for icon_name, description in icons_list:
            found_icon = None
            
            # البحث المباشر
            if icon_name in available_icons:
                found_icon = available_icons[icon_name]
            
            # البحث بأسماء بديلة
            elif icon_name == "employees" and "employees" in available_icons:
                found_icon = available_icons["employees"]
            elif icon_name == "welcome" and "1" in available_icons:
                found_icon = available_icons["1"]
            elif icon_name == "settings" and "2" in available_icons:
                found_icon = available_icons["2"]
            elif icon_name == "items" and "3" in available_icons:
                found_icon = available_icons["3"]
            elif icon_name == "accounts" and "43" in available_icons:
                found_icon = available_icons["43"]
            elif icon_name == "daily" and "6" in available_icons:
                found_icon = available_icons["6"]
            elif icon_name == "analysis" and "7" in available_icons:
                found_icon = available_icons["7"]
            elif icon_name == "warehouse" and "8" in available_icons:
                found_icon = available_icons["8"]
            elif icon_name == "sell" and "9" in available_icons:
                found_icon = available_icons["9"]
            elif icon_name == "buy" and "10" in available_icons:
                found_icon = available_icons["10"]
            elif icon_name == "expense" and "11" in available_icons:
                found_icon = available_icons["11"]
            elif icon_name == "indicators" and "12" in available_icons:
                found_icon = available_icons["12"]
            elif icon_name == "return_sell" and "13" in available_icons:
                found_icon = available_icons["13"]
            elif icon_name == "quote" and "14" in available_icons:
                found_icon = available_icons["14"]
            elif icon_name == "return_buy" and "15" in available_icons:
                found_icon = available_icons["15"]
            elif icon_name == "quantity" and "16" in available_icons:
                found_icon = available_icons["16"]
            elif icon_name == "transfer" and "17" in available_icons:
                found_icon = available_icons["17"]
            elif icon_name == "inventory" and "18" in available_icons:
                found_icon = available_icons["18"]
            elif icon_name == "reports" and "19" in available_icons:
                found_icon = available_icons["19"]
            
            if found_icon:
                mapping_results[category].append((found_icon, description))
                print(f"✅ {description}: {found_icon}")
            else:
                # استخدام أيقونة افتراضية
                default_icon = list(available_icons.values())[0] if available_icons else None
                mapping_results[category].append((default_icon, description))
                print(f"⚠️ {description}: استخدام أيقونة افتراضية")
    
    return mapping_results

def generate_fixed_code(mapping_results):
    """إنشاء الكود المُصحح"""
    code_parts = []
    
    # كود الشريط الأخضر
    green_icons_code = "        green_icons = [\n"
    for icon_path, description in mapping_results["green_icons"]:
        if icon_path:
            green_icons_code += f'            ("{icon_path}", "{description}"),\n'
        else:
            green_icons_code += f'            ("assets/icons/1.ico", "{description}"),  # افتراضي\n'
    green_icons_code += "        ]"
    
    # كود الصف الأول
    first_row_code = "        first_row_icons = [\n"
    colors = ["#5DADE2", "#5DADE2", "#4ECDC4", "#F39C12", "#8E44AD", "#3498DB"]
    for i, (icon_path, description) in enumerate(mapping_results["first_row"]):
        color = colors[i] if i < len(colors) else "#5DADE2"
        if icon_path:
            first_row_code += f'            ("{icon_path}", "{description}", "{color}"),\n'
        else:
            first_row_code += f'            ("assets/icons/{i+1}.ico", "{description}", "{color}"),  # افتراضي\n'
    first_row_code += "        ]"
    
    # كود الصف الثاني
    second_row_code = "        second_row_icons = [\n"
    colors = ["#F39C12", "#27AE60", "#E74C3C", "#E67E22", "#16A085", "#27AE60"]
    for i, (icon_path, description) in enumerate(mapping_results["second_row"]):
        color = colors[i] if i < len(colors) else "#F39C12"
        if icon_path:
            second_row_code += f'            ("{icon_path}", "{description}", "{color}"),\n'
        else:
            second_row_code += f'            ("assets/icons/{i+7}.ico", "{description}", "{color}"),  # افتراضي\n'
    second_row_code += "        ]"
    
    # كود الصف الثالث
    third_row_code = "        third_row_icons = [\n"
    colors = ["#16A085", "#8E44AD", "#9B59B6", "#3498DB", "#1ABC9C", "#16A085"]
    for i, (icon_path, description) in enumerate(mapping_results["third_row"]):
        color = colors[i] if i < len(colors) else "#16A085"
        if icon_path:
            third_row_code += f'            ("{icon_path}", "{description}", "{color}"),\n'
        else:
            third_row_code += f'            ("assets/icons/{i+13}.ico", "{description}", "{color}"),  # افتراضي\n'
    third_row_code += "        ]"
    
    return {
        "green_icons": green_icons_code,
        "first_row": first_row_code,
        "second_row": second_row_code,
        "third_row": third_row_code
    }

def main():
    """الدالة الرئيسية"""
    print("🔧 أداة إصلاح الأيقونات في النافذة الرئيسية")
    print("="*60)
    
    # فحص الأيقونات المتاحة
    print("\n📁 فحص الأيقونات المتاحة...")
    available_icons = scan_available_icons()
    
    if not available_icons:
        print("❌ لا توجد أيقونات متاحة")
        return
    
    # إنشاء خريطة الأيقونات المطلوبة
    print("\n🗺️ إنشاء خريطة الأيقونات...")
    needed_mapping = create_icon_mapping()
    
    # ربط الأيقونات
    print("\n🔗 ربط الأيقونات المتاحة بالمطلوبة...")
    mapping_results = map_available_to_needed(available_icons, needed_mapping)
    
    # إنشاء الكود المُصحح
    print("\n💻 إنشاء الكود المُصحح...")
    fixed_code = generate_fixed_code(mapping_results)
    
    # حفظ النتائج
    print("\n💾 حفظ النتائج...")
    with open("كود_الأيقونات_المُصحح.txt", "w", encoding="utf-8") as f:
        f.write("# كود الشريط الأخضر المُصحح\n")
        f.write(fixed_code["green_icons"])
        f.write("\n\n# كود الصف الأول المُصحح\n")
        f.write(fixed_code["first_row"])
        f.write("\n\n# كود الصف الثاني المُصحح\n")
        f.write(fixed_code["second_row"])
        f.write("\n\n# كود الصف الثالث المُصحح\n")
        f.write(fixed_code["third_row"])
    
    print("✅ تم حفظ الكود المُصحح في: كود_الأيقونات_المُصحح.txt")
    print("\n🎉 تم إصلاح مسارات الأيقونات بنجاح!")
    
    return fixed_code

if __name__ == "__main__":
    main()
