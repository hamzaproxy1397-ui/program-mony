#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تشخيصي لمشكلة تحميل قائمة الأصناف
"""

import sys
import os
import sqlite3
sys.path.append('.')

def test_database_connection():
    """اختبار اتصال قاعدة البيانات"""
    print("🔍 اختبار اتصال قاعدة البيانات...")
    try:
        from database.advanced_items_database import AdvancedItemsDatabase
        db = AdvancedItemsDatabase()
        conn = db.get_connection()
        print("✅ تم الاتصال بقاعدة البيانات بنجاح")
        return db, conn
    except Exception as e:
        print(f"❌ فشل في الاتصال بقاعدة البيانات: {e}")
        return None, None

def test_tables_exist(conn):
    """اختبار وجود الجداول المطلوبة"""
    print("🔍 اختبار وجود الجداول...")
    try:
        cursor = conn.cursor()
        
        # فحص جدول الأصناف
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        items_table = cursor.fetchone()
        
        # فحص جدول الفئات
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
        categories_table = cursor.fetchone()
        
        print(f"جدول الأصناف: {'✅ موجود' if items_table else '❌ غير موجود'}")
        print(f"جدول الفئات: {'✅ موجود' if categories_table else '❌ غير موجود'}")
        
        return items_table is not None and categories_table is not None
    except Exception as e:
        print(f"❌ خطأ في فحص الجداول: {e}")
        return False

def test_table_structure(conn):
    """اختبار هيكل الجداول"""
    print("🔍 اختبار هيكل الجداول...")
    try:
        cursor = conn.cursor()
        
        # فحص أعمدة جدول الأصناف
        cursor.execute("PRAGMA table_info(items)")
        items_columns = cursor.fetchall()
        
        required_columns = ['id', 'code', 'name', 'category_id', 'selling_price', 'current_stock', 'is_active']
        existing_columns = [col[1] for col in items_columns]
        
        print("أعمدة جدول الأصناف:")
        for col in required_columns:
            status = "✅" if col in existing_columns else "❌"
            print(f"  {status} {col}")
        
        return all(col in existing_columns for col in required_columns)
    except Exception as e:
        print(f"❌ خطأ في فحص هيكل الجداول: {e}")
        return False

def test_sample_data(conn):
    """اختبار وجود بيانات تجريبية"""
    print("🔍 اختبار البيانات...")
    try:
        cursor = conn.cursor()
        
        # عدد الأصناف
        cursor.execute("SELECT COUNT(*) FROM items")
        items_count = cursor.fetchone()[0]
        
        # عدد الفئات
        cursor.execute("SELECT COUNT(*) FROM categories")
        categories_count = cursor.fetchone()[0]
        
        print(f"عدد الأصناف: {items_count}")
        print(f"عدد الفئات: {categories_count}")
        
        return True
    except Exception as e:
        print(f"❌ خطأ في فحص البيانات: {e}")
        return False

def test_query_execution(conn):
    """اختبار تنفيذ الاستعلام المستخدم في النافذة"""
    print("🔍 اختبار الاستعلام الأساسي...")
    try:
        cursor = conn.cursor()
        
        # نفس الاستعلام المستخدم في النافذة
        cursor.execute("""
            SELECT i.code, i.name, c.name as category, i.selling_price, i.current_stock
            FROM items i
            LEFT JOIN categories c ON i.category_id = c.id
            WHERE i.is_active = 1
            ORDER BY i.name
        """)
        
        items = cursor.fetchall()
        print(f"✅ تم تنفيذ الاستعلام بنجاح - عدد النتائج: {len(items)}")
        
        # عرض أول 3 نتائج
        for i, item in enumerate(items[:3]):
            print(f"  {i+1}. {item}")
        
        return True, items
    except Exception as e:
        print(f"❌ فشل في تنفيذ الاستعلام: {e}")
        return False, []

def add_sample_data(conn):
    """إضافة بيانات تجريبية"""
    print("🔧 إضافة بيانات تجريبية...")
    try:
        cursor = conn.cursor()
        
        # إضافة فئة تجريبية
        cursor.execute("""
            INSERT OR IGNORE INTO categories (code, name, description)
            VALUES ('CAT001', 'إلكترونيات', 'أجهزة إلكترونية متنوعة')
        """)
        
        # إضافة صنف تجريبي
        cursor.execute("""
            INSERT OR IGNORE INTO items (
                uuid, code, name, category_id, selling_price, current_stock, is_active
            ) VALUES (
                'test-item-001', 'ITEM001', 'لابتوب تجريبي', 1, 1500.00, 10.0, 1
            )
        """)
        
        conn.commit()
        print("✅ تم إضافة البيانات التجريبية")
        return True
    except Exception as e:
        print(f"❌ فشل في إضافة البيانات التجريبية: {e}")
        return False

def main():
    """تشغيل التشخيص الشامل"""
    print("🚀 بدء التشخيص الشامل لمشكلة تحميل قائمة الأصناف")
    print("=" * 60)
    
    # 1. اختبار اتصال قاعدة البيانات
    db, conn = test_database_connection()
    if not conn:
        return False
    
    print("-" * 40)
    
    # 2. اختبار وجود الجداول
    tables_exist = test_tables_exist(conn)
    if not tables_exist:
        print("⚠️ الجداول غير موجودة - سيتم إنشاؤها...")
        db.init_database()
        tables_exist = test_tables_exist(conn)
    
    print("-" * 40)
    
    # 3. اختبار هيكل الجداول
    structure_ok = test_table_structure(conn)
    
    print("-" * 40)
    
    # 4. اختبار البيانات
    test_sample_data(conn)
    
    print("-" * 40)
    
    # 5. اختبار الاستعلام
    query_ok, items = test_query_execution(conn)
    
    # إذا لم تكن هناك بيانات، أضف بيانات تجريبية
    if query_ok and len(items) == 0:
        print("-" * 40)
        add_sample_data(conn)
        print("-" * 40)
        query_ok, items = test_query_execution(conn)
    
    print("=" * 60)
    print("📊 ملخص التشخيص:")
    print(f"اتصال قاعدة البيانات: {'✅' if conn else '❌'}")
    print(f"وجود الجداول: {'✅' if tables_exist else '❌'}")
    print(f"هيكل الجداول: {'✅' if structure_ok else '❌'}")
    print(f"تنفيذ الاستعلام: {'✅' if query_ok else '❌'}")
    print(f"عدد الأصناف المحملة: {len(items) if query_ok else 0}")
    
    if conn:
        conn.close()
    
    return all([conn, tables_exist, structure_ok, query_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
