# -*- coding: utf-8 -*-
"""
تشغيل نافذة إدخال الأصناف المتقدمة
Run Advanced Item Entry Window
"""

import sys
import os
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """تشغيل النافذة المتقدمة"""
    
    print("🚀 بدء تشغيل نافذة إدخال الأصناف المتقدمة...")
    print("=" * 60)
    
    try:
        # استيراد النافذة المتقدمة
        from windows.advanced_item_entry import AdvancedItemEntry
        
        print("✅ تم تحميل النافذة المتقدمة بنجاح")
        print("🎉 فتح النافذة...")
        
        # إنشاء وعرض النافذة
        app = AdvancedItemEntry()
        app.show()
        
        print("✅ تم إغلاق النافذة بنجاح")
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("💡 تأكد من تثبيت جميع المكتبات المطلوبة:")
        print("   pip install Pillow matplotlib numpy pandas")
        
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
