#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة إصلاح كتل try الفارغة
"""

import re
from pathlib import Path

def fix_empty_try_blocks(file_path):
    """إصلاح كتل try الفارغة في ملف"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # البحث عن كتل try فارغة وإصلاحها
        patterns = [
            # try: \n except ImportError:
            (r'try:\s*\n\s*except ImportError:\s*\n\s*pass\s*\n\s*pass\s*\n\s*print\("تحذير: فشل في استيراد المكتبة"\)\s*\n\s*(\w+) = None',
             r'try:\n    from ui.\1_window import \1\nexcept ImportError:\n    print("تحذير: فشل في استيراد المكتبة")\n    \1 = None'),
            
            # try: \n except ImportError: (عام)
            (r'try:\s*\n\s*except ImportError:',
             r'try:\n    pass  # TODO: إضافة الاستيراد المناسب\nexcept ImportError:'),
            
            # try: \n except Exception:
            (r'try:\s*\n\s*except Exception:',
             r'try:\n    pass  # TODO: إضافة الكود المناسب\nexcept Exception:'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # إصلاح خاص لكتل try فارغة محددة
        specific_fixes = [
            # ReportsWindow
            ('try:\nexcept ImportError:\n    pass\n    pass\n    print("تحذير: فشل في استيراد المكتبة")\n    ReportsWindow = None',
             'try:\n    from ui.reports_window import ReportsWindow\nexcept ImportError:\n    print("تحذير: فشل في استيراد المكتبة")\n    ReportsWindow = None'),
            
            # AdvancedFinancialReportsWindow
            ('try:\nexcept ImportError:\n    pass\n    pass\n    print("تحذير: فشل في استيراد المكتبة")\n    AdvancedFinancialReportsWindow = None',
             'try:\n    from ui.advanced_financial_reports_window import AdvancedFinancialReportsWindow\nexcept ImportError:\n    print("تحذير: فشل في استيراد المكتبة")\n    AdvancedFinancialReportsWindow = None'),
            
            # AccountsWindow
            ('try:\nexcept ImportError:\n    pass\n    pass\n    print("تحذير: فشل في استيراد المكتبة")\n    AccountsWindow = None',
             'try:\n    from ui.accounts_window import AccountsWindow\nexcept ImportError:\n    print("تحذير: فشل في استيراد المكتبة")\n    AccountsWindow = None'),
            
            # JournalEntriesWindow
            ('try:\nexcept ImportError:\n    pass\n    pass\n    print("تحذير: فشل في استيراد المكتبة")\n    JournalEntriesWindow = None',
             'try:\n    from ui.journal_entries_window import JournalEntriesWindow\nexcept ImportError:\n    print("تحذير: فشل في استيراد المكتبة")\n    JournalEntriesWindow = None'),
            
            # AddItemsWindow
            ('try:\nexcept ImportError:\n    pass\n    pass\n    print("تحذير: فشل في استيراد المكتبة")\n    AddItemsWindow = None',
             'try:\n    from ui.add_items_window import AddItemsWindow\nexcept ImportError:\n    print("تحذير: فشل في استيراد المكتبة")\n    AddItemsWindow = None'),
        ]
        
        for old, new in specific_fixes:
            content = content.replace(old, new)
        
        # حفظ الملف إذا تم تغييره
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ تم إصلاح: {file_path}")
            return True
        else:
            print(f"ℹ️ لا يحتاج إصلاح: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إصلاح {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔧 بدء إصلاح كتل try الفارغة...")
    
    # إصلاح main_window.py
    main_window_path = Path("ui/main_window.py")
    if main_window_path.exists():
        fix_empty_try_blocks(main_window_path)
    
    print("🎉 تم الانتهاء من الإصلاح!")

if __name__ == "__main__":
    main()
