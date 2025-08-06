#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار قاعدة البيانات
"""

from database.hybrid_database_manager import HybridDatabaseManager

try:
    print("🔍 اختبار قاعدة البيانات...")
    db = HybridDatabaseManager()
    print("✅ تم الاتصال بقاعدة البيانات بنجاح")
    
    # اختبار المنتجات
    try:
        products = db.get_all_products()
        print(f"📦 عدد المنتجات: {len(products)}")
    except Exception as e:
        print(f"⚠️ خطأ في جلب المنتجات: {e}")
    
    # اختبار الحسابات
    try:
        accounts = db.get_all_accounts()
        print(f"💰 عدد الحسابات: {len(accounts)}")
    except Exception as e:
        print(f"⚠️ خطأ في جلب الحسابات: {e}")
    
    print("✅ اختبار قاعدة البيانات مكتمل")
    
except Exception as e:
    print(f"❌ خطأ في قاعدة البيانات: {e}")
