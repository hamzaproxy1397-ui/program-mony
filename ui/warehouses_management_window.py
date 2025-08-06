# -*- coding: utf-8 -*-
# cSpell:disable
"""
نافذة إدارة المخازن والمستودعات الاحترافية
Professional Warehouse Management Window
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import os
import json
from datetime import datetime, date
import sqlite3
from pathlib import Path
import uuid
import pandas as pd

try:
    from themes.modern_theme import MODERN_COLORS, FONTS
    from ui.window_utils import configure_window_fullscreen
    from database.hybrid_database_manager import HybridDatabaseManager
except ImportError:
    MODERN_COLORS = {
        'primary': '#2E8B57',
        'secondary': '#4682B4', 
        'success': '#28a745',
        'background': '#f8f9fa',
        'surface': '#ffffff',
        'text_primary': '#212529',
        'text_secondary': '#6c757d',
        'border': '#dee2e6'
    }
    FONTS = {'arabic': 'Cairo', 'english': 'Arial'}

# نظام ألوان متطور ومتدرج للمخازن - تصميم احترافي حديث
WAREHOUSE_COLORS = {
    # ألوان أساسية متدرجة للواجهة
    'background_main': '#F8FAFC',  # خلفية ناعمة مع لمسة زرقاء
    'background_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'sidebar_bg': '#1E293B',  # شريط جانبي داكن عصري
    'sidebar_hover': '#334155',  # تفاعل الشريط الجانبي
    'sidebar_active': '#3B82F6',  # القسم النشط
    'main_content': '#FFFFFF',  # المحتوى الرئيسي
    'card_bg': '#FFFFFF',  # خلفية البطاقات
    'card_hover': '#F1F5F9',  # تمرير البطاقات
    'card_shadow': 'rgba(15, 23, 42, 0.08)',  # ظل البطاقات محسن
    'card_shadow_hover': 'rgba(15, 23, 42, 0.15)',  # ظل عند التمرير

    # ألوان العمليات مع تدرجات
    'add_operation': '#10B981',  # أخضر زمردي لإذن الإضافة
    'add_hover': '#059669',
    'add_light': '#D1FAE5',  # خلفية فاتحة للإضافة
    'add_gradient': 'linear-gradient(135deg, #10B981, #059669)',

    'out_operation': '#EF4444',  # أحمر حديث لإذن الصرف
    'out_hover': '#DC2626',
    'out_light': '#FEE2E2',  # خلفية فاتحة للصرف
    'out_gradient': 'linear-gradient(135deg, #EF4444, #DC2626)',

    'transfer_operation': '#3B82F6',  # أزرق حديث للتحويلات
    'transfer_hover': '#2563EB',
    'transfer_light': '#DBEAFE',  # خلفية فاتحة للتحويل
    'transfer_gradient': 'linear-gradient(135deg, #3B82F6, #2563EB)',

    'report_operation': '#8B5CF6',  # بنفسجي أنيق للتقارير
    'report_hover': '#7C3AED',
    'report_light': '#EDE9FE',  # خلفية فاتحة للتقارير
    'report_gradient': 'linear-gradient(135deg, #8B5CF6, #7C3AED)',

    # ألوان النصوص محسنة
    'text_primary': '#0F172A',  # نص رئيسي داكن
    'text_secondary': '#64748B',  # نص ثانوي
    'text_white': '#FFFFFF',  # نص أبيض
    'text_muted': '#94A3B8',  # نص خافت
    'text_success': '#10B981',  # نص نجاح
    'text_danger': '#EF4444',  # نص خطر
    'text_warning': '#F59E0B',  # نص تحذير
    'text_info': '#3B82F6',  # نص معلومات

    # ألوان الحدود والتفاصيل المحسنة
    'border_light': '#E2E8F0',  # حدود فاتحة
    'border_medium': '#CBD5E1',  # حدود متوسطة
    'border_strong': '#94A3B8',  # حدود قوية
    'accent_blue': '#3B82F6',  # أزرق مميز
    'accent_orange': '#F97316',  # برتقالي مميز
    'accent_purple': '#8B5CF6',  # بنفسجي مميز
    'accent_green': '#10B981',  # أخضر مميز
    'accent_red': '#EF4444',  # أحمر مميز

    # ألوان خاصة للحالات
    'success': '#10B981',  # نجاح
    'success_bg': '#ECFDF5',  # خلفية نجاح
    'warning': '#F59E0B',  # تحذير
    'warning_bg': '#FFFBEB',  # خلفية تحذير
    'text_warning': '#F59E0B',  # نص تحذير
    'error': '#EF4444',  # خطأ
    'error_bg': '#FEF2F2',  # خلفية خطأ
    'info': '#3B82F6',  # معلومات
    'info_bg': '#EFF6FF',  # خلفية معلومات

    # ألوان الأقسام المميزة
    'dashboard_primary': '#6366F1',  # بنفسجي للوحة التحكم
    'dashboard_secondary': '#8B5CF6',
    'inventory_primary': '#10B981',  # أخضر للمخزون
    'inventory_secondary': '#059669',
    'reports_primary': '#3B82F6',  # أزرق للتقارير
    'reports_secondary': '#2563EB',
    'tools_primary': '#F59E0B',  # أصفر للأدوات
    'tools_secondary': '#D97706',
}

# نظام خطوط متدرج ومحسن للمخازن
WAREHOUSE_FONTS = {
    # العناوين الرئيسية
    'hero_title': 32,  # عنوان البطل الرئيسي
    'title_large': 28,  # العناوين الكبيرة
    'title_medium': 24,  # العناوين المتوسطة
    'title_small': 20,  # العناوين الصغيرة

    # العناوين الفرعية
    'heading_large': 18,  # العناوين الفرعية الكبيرة
    'heading_medium': 16,  # العناوين الفرعية المتوسطة
    'heading_small': 14,  # العناوين الفرعية الصغيرة

    # النصوص الأساسية
    'body_large': 14,  # النص الأساسي الكبير
    'body_medium': 13,  # النص الأساسي المتوسط
    'body_small': 12,  # النص الأساسي الصغير

    # النصوص المساعدة
    'caption_large': 11,  # النص التوضيحي الكبير
    'caption_medium': 10,  # النص التوضيحي المتوسط
    'caption_small': 9,  # النص التوضيحي الصغير

    # خطوط خاصة
    'button_large': 15,  # أزرار كبيرة
    'button_medium': 13,  # أزرار متوسطة
    'button_small': 11,  # أزرار صغيرة
    'sidebar_title': 16,  # عناوين الشريط الجانبي
    'sidebar_item': 13,  # عناصر الشريط الجانبي
}

class WarehousesManagementWindow:
    """نافذة إدارة المخازن والمستودعات الاحترافية"""

    def __init__(self, parent, db_manager=None):
        self.parent = parent
        self.db_manager = db_manager or HybridDatabaseManager()
        self.window = None
        self.current_view = "dashboard"
        self.sidebar_buttons = {}
        self.main_content_frame = None

        # إعداد قاعدة البيانات
        self.setup_database()

        # فحص وإصلاح قاعدة البيانات
        self.database_health_check()

        # إنشاء النافذة
        self.create_window()

    def setup_database(self):
        """إعداد جداول قاعدة البيانات للمخازن"""
        try:
            # جدول المخازن
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS warehouses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    warehouse_code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    location TEXT,
                    manager_name TEXT,
                    capacity DECIMAL(10,2),
                    current_stock DECIMAL(10,2) DEFAULT 0,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # جدول الأصناف
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT,
                    unit TEXT,
                    cost_price DECIMAL(10,2),
                    sale_price DECIMAL(10,2),
                    min_stock DECIMAL(10,2) DEFAULT 0,
                    max_stock DECIMAL(10,2) DEFAULT 0,
                    barcode TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # جدول حركات المخزن
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS warehouse_movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number TEXT UNIQUE NOT NULL,
                    movement_type TEXT NOT NULL,
                    warehouse_id INTEGER,
                    item_id INTEGER,
                    quantity DECIMAL(10,2) NOT NULL,
                    unit_price DECIMAL(10,2),
                    total_value DECIMAL(10,2),
                    reference_number TEXT,
                    notes TEXT,
                    created_by TEXT,
                    movement_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            """)

            # جدول أرصدة المخزن
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS warehouse_stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    warehouse_id INTEGER,
                    item_id INTEGER,
                    quantity DECIMAL(10,2) DEFAULT 0,
                    last_cost DECIMAL(10,2),
                    total_value DECIMAL(10,2),
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (item_id) REFERENCES items (id),
                    UNIQUE(warehouse_id, item_id)
                )
            """)

            # جدول التحويلات
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS warehouse_transfers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number TEXT UNIQUE NOT NULL,
                    from_warehouse_id INTEGER,
                    to_warehouse_id INTEGER,
                    item_id INTEGER,
                    quantity DECIMAL(10,2) NOT NULL,
                    transfer_date DATE,
                    status TEXT DEFAULT 'pending',
                    notes TEXT,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (from_warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (to_warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            """)

            # إدراج بيانات افتراضية
            self.insert_default_data()

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إعداد قاعدة البيانات: {e}")

    def insert_default_data(self):
        """إدراج بيانات افتراضية"""
        try:
            # إدراج مخازن افتراضية
            warehouses = [
                ("WH001", "المخزن الرئيسي", "الطابق الأول", "أحمد محمد", 1000.00),
                ("WH002", "مخزن المواد الخام", "الطابق الثاني", "فاطمة علي", 500.00),
                ("WH003", "مخزن المنتجات النهائية", "الطابق الثالث", "محمد حسن", 800.00)
            ]

            for code, name, location, manager, capacity in warehouses:
                self.db_manager.execute_query(
                    "INSERT OR IGNORE INTO warehouses (warehouse_code, name, location, manager_name, capacity) VALUES (?, ?, ?, ?, ?)",
                    (code, name, location, manager, capacity)
                )

            # إدراج أصناف افتراضية
            items = [
                ("ITM001", "لابتوب ديل", "إلكترونيات", "قطعة", 15000.00, 18000.00, 5, 50),
                ("ITM002", "طابعة HP", "إلكترونيات", "قطعة", 2500.00, 3200.00, 3, 20),
                ("ITM003", "ورق A4", "مكتبية", "علبة", 45.00, 60.00, 10, 100)
            ]

            for code, name, category, unit, cost, sale, min_stock, max_stock in items:
                self.db_manager.execute_query(
                    "INSERT OR IGNORE INTO items (item_code, name, category, unit, cost_price, sale_price, min_stock, max_stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (code, name, category, unit, cost, sale, min_stock, max_stock)
                )

        except Exception as e:
            print(f"خطأ في إدراج البيانات الافتراضية: {e}")

    def database_health_check(self):
        """فحص شامل لصحة قاعدة البيانات وإصلاح المشاكل"""
        print("🔍 بدء فحص صحة قاعدة البيانات...")

        try:
            # 1. فحص وجود الجداول المطلوبة
            self.check_required_tables()

            # 2. فحص سلامة البيانات
            self.validate_data_integrity()

            # 3. فحص الفهارس والأداء
            self.check_database_indexes()

            # 4. فحص العلاقات الخارجية
            self.validate_foreign_keys()

            # 5. تنظيف البيانات المكررة أو التالفة
            self.cleanup_corrupted_data()

            # 6. تحديث الإحصائيات
            self.update_database_statistics()

            print("✅ تم فحص قاعدة البيانات بنجاح - لا توجد مشاكل")

        except Exception as e:
            print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
            messagebox.showerror("خطأ في قاعدة البيانات", f"تم اكتشاف مشكلة في قاعدة البيانات:\n{e}")

    def check_required_tables(self):
        """فحص وجود جميع الجداول المطلوبة"""
        required_tables = [
            'warehouses', 'items', 'warehouse_movements',
            'warehouse_stock', 'warehouse_transfers'
        ]

        for table in required_tables:
            try:
                result = self.db_manager.fetch_one(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table,)
                )
                if not result:
                    print(f"⚠️ الجدول {table} غير موجود - سيتم إنشاؤه")
                    self.create_missing_table(table)
                else:
                    print(f"✅ الجدول {table} موجود")
            except Exception as e:
                print(f"❌ خطأ في فحص الجدول {table}: {e}")

    def create_missing_table(self, table_name):
        """إنشاء الجداول المفقودة"""
        table_schemas = {
            'warehouses': """
                CREATE TABLE warehouses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    warehouse_code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    location TEXT,
                    manager_name TEXT,
                    capacity DECIMAL(10,2),
                    current_stock DECIMAL(10,2) DEFAULT 0,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'items': """
                CREATE TABLE items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT,
                    unit TEXT,
                    cost_price DECIMAL(10,2),
                    sale_price DECIMAL(10,2),
                    min_stock DECIMAL(10,2) DEFAULT 0,
                    max_stock DECIMAL(10,2) DEFAULT 0,
                    barcode TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'warehouse_movements': """
                CREATE TABLE warehouse_movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number TEXT UNIQUE NOT NULL,
                    movement_type TEXT NOT NULL,
                    warehouse_id INTEGER,
                    item_id INTEGER,
                    quantity DECIMAL(10,2) NOT NULL,
                    unit_price DECIMAL(10,2),
                    total_value DECIMAL(10,2),
                    reference_number TEXT,
                    notes TEXT,
                    created_by TEXT,
                    movement_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            """,
            'warehouse_stock': """
                CREATE TABLE warehouse_stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    warehouse_id INTEGER,
                    item_id INTEGER,
                    quantity DECIMAL(10,2) DEFAULT 0,
                    last_cost DECIMAL(10,2),
                    total_value DECIMAL(10,2),
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (item_id) REFERENCES items (id),
                    UNIQUE(warehouse_id, item_id)
                )
            """,
            'warehouse_transfers': """
                CREATE TABLE warehouse_transfers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number TEXT UNIQUE NOT NULL,
                    from_warehouse_id INTEGER,
                    to_warehouse_id INTEGER,
                    item_id INTEGER,
                    quantity DECIMAL(10,2) NOT NULL,
                    transfer_date DATE,
                    status TEXT DEFAULT 'pending',
                    notes TEXT,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (from_warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (to_warehouse_id) REFERENCES warehouses (id),
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            """
        }

        if table_name in table_schemas:
            self.db_manager.execute_query(table_schemas[table_name])
            print(f"✅ تم إنشاء الجدول {table_name} بنجاح")

    def validate_data_integrity(self):
        """فحص سلامة البيانات"""
        print("🔍 فحص سلامة البيانات...")

        # فحص البيانات المطلوبة في جدول المخازن
        warehouses_issues = self.db_manager.fetch_all("""
            SELECT id, warehouse_code, name FROM warehouses
            WHERE warehouse_code IS NULL OR warehouse_code = ''
            OR name IS NULL OR name = ''
        """)

        if warehouses_issues:
            print(f"⚠️ تم العثور على {len(warehouses_issues)} مخزن بدون كود أو اسم")
            for warehouse in warehouses_issues:
                # إصلاح البيانات المفقودة
                if not warehouse[1]:  # warehouse_code
                    new_code = f"WH{warehouse[0]:03d}"
                    self.db_manager.execute_query(
                        "UPDATE warehouses SET warehouse_code = ? WHERE id = ?",
                        (new_code, warehouse[0])
                    )
                    print(f"✅ تم إصلاح كود المخزن: {new_code}")

                if not warehouse[2]:  # name
                    new_name = f"مخزن رقم {warehouse[0]}"
                    self.db_manager.execute_query(
                        "UPDATE warehouses SET name = ? WHERE id = ?",
                        (new_name, warehouse[0])
                    )
                    print(f"✅ تم إصلاح اسم المخزن: {new_name}")

        # فحص البيانات المطلوبة في جدول الأصناف
        items_issues = self.db_manager.fetch_all("""
            SELECT id, item_code, name FROM items
            WHERE item_code IS NULL OR item_code = ''
            OR name IS NULL OR name = ''
        """)

        if items_issues:
            print(f"⚠️ تم العثور على {len(items_issues)} صنف بدون كود أو اسم")
            for item in items_issues:
                if not item[1]:  # item_code
                    new_code = f"ITM{item[0]:03d}"
                    self.db_manager.execute_query(
                        "UPDATE items SET item_code = ? WHERE id = ?",
                        (new_code, item[0])
                    )
                    print(f"✅ تم إصلاح كود الصنف: {new_code}")

                if not item[2]:  # name
                    new_name = f"صنف رقم {item[0]}"
                    self.db_manager.execute_query(
                        "UPDATE items SET name = ? WHERE id = ?",
                        (new_name, item[0])
                    )
                    print(f"✅ تم إصلاح اسم الصنف: {new_name}")

        # فحص الكميات السالبة
        negative_stock = self.db_manager.fetch_all("""
            SELECT warehouse_id, item_id, quantity FROM warehouse_stock
            WHERE quantity < 0
        """)

        if negative_stock:
            print(f"⚠️ تم العثور على {len(negative_stock)} رصيد سالب")
            for stock in negative_stock:
                self.db_manager.execute_query(
                    "UPDATE warehouse_stock SET quantity = 0 WHERE warehouse_id = ? AND item_id = ?",
                    (stock[0], stock[1])
                )
                print(f"✅ تم إصلاح الرصيد السالب للمخزن {stock[0]} والصنف {stock[1]}")

    def check_database_indexes(self):
        """فحص وإنشاء الفهارس المطلوبة لتحسين الأداء"""
        print("🔍 فحص فهارس قاعدة البيانات...")

        indexes_to_create = [
            ("idx_warehouses_code", "CREATE INDEX IF NOT EXISTS idx_warehouses_code ON warehouses(warehouse_code)"),
            ("idx_items_code", "CREATE INDEX IF NOT EXISTS idx_items_code ON items(item_code)"),
            ("idx_movements_serial", "CREATE INDEX IF NOT EXISTS idx_movements_serial ON warehouse_movements(serial_number)"),
            ("idx_movements_date", "CREATE INDEX IF NOT EXISTS idx_movements_date ON warehouse_movements(movement_date)"),
            ("idx_movements_warehouse", "CREATE INDEX IF NOT EXISTS idx_movements_warehouse ON warehouse_movements(warehouse_id)"),
            ("idx_movements_item", "CREATE INDEX IF NOT EXISTS idx_movements_item ON warehouse_movements(item_id)"),
            ("idx_stock_warehouse_item", "CREATE INDEX IF NOT EXISTS idx_stock_warehouse_item ON warehouse_stock(warehouse_id, item_id)"),
            ("idx_transfers_serial", "CREATE INDEX IF NOT EXISTS idx_transfers_serial ON warehouse_transfers(serial_number)"),
            ("idx_transfers_date", "CREATE INDEX IF NOT EXISTS idx_transfers_date ON warehouse_transfers(transfer_date)"),
            ("idx_transfers_status", "CREATE INDEX IF NOT EXISTS idx_transfers_status ON warehouse_transfers(status)")
        ]

        for index_name, create_sql in indexes_to_create:
            try:
                self.db_manager.execute_query(create_sql)
                print(f"✅ تم إنشاء/فحص الفهرس: {index_name}")
            except Exception as e:
                print(f"❌ خطأ في إنشاء الفهرس {index_name}: {e}")

    def validate_foreign_keys(self):
        """فحص سلامة العلاقات الخارجية"""
        print("🔍 فحص العلاقات الخارجية...")

        # فحص حركات المخزن - مخازن غير موجودة
        orphaned_movements_warehouse = self.db_manager.fetch_all("""
            SELECT wm.id, wm.serial_number, wm.warehouse_id
            FROM warehouse_movements wm
            LEFT JOIN warehouses w ON wm.warehouse_id = w.id
            WHERE wm.warehouse_id IS NOT NULL AND w.id IS NULL
        """)

        if orphaned_movements_warehouse:
            print(f"⚠️ تم العثور على {len(orphaned_movements_warehouse)} حركة مخزن مرتبطة بمخازن غير موجودة")
            for movement in orphaned_movements_warehouse:
                # حذف الحركات المرتبطة بمخازن غير موجودة
                self.db_manager.execute_query(
                    "DELETE FROM warehouse_movements WHERE id = ?",
                    (movement[0],)
                )
                print(f"✅ تم حذف الحركة {movement[1]} المرتبطة بالمخزن غير الموجود {movement[2]}")

        # فحص حركات المخزن - أصناف غير موجودة
        orphaned_movements_item = self.db_manager.fetch_all("""
            SELECT wm.id, wm.serial_number, wm.item_id
            FROM warehouse_movements wm
            LEFT JOIN items i ON wm.item_id = i.id
            WHERE wm.item_id IS NOT NULL AND i.id IS NULL
        """)

        if orphaned_movements_item:
            print(f"⚠️ تم العثور على {len(orphaned_movements_item)} حركة مخزن مرتبطة بأصناف غير موجودة")
            for movement in orphaned_movements_item:
                self.db_manager.execute_query(
                    "DELETE FROM warehouse_movements WHERE id = ?",
                    (movement[0],)
                )
                print(f"✅ تم حذف الحركة {movement[1]} المرتبطة بالصنف غير الموجود {movement[2]}")

        # فحص أرصدة المخزن - مخازن غير موجودة
        orphaned_stock_warehouse = self.db_manager.fetch_all("""
            SELECT ws.id, ws.warehouse_id, ws.item_id
            FROM warehouse_stock ws
            LEFT JOIN warehouses w ON ws.warehouse_id = w.id
            WHERE ws.warehouse_id IS NOT NULL AND w.id IS NULL
        """)

        if orphaned_stock_warehouse:
            print(f"⚠️ تم العثور على {len(orphaned_stock_warehouse)} رصيد مرتبط بمخازن غير موجودة")
            for stock in orphaned_stock_warehouse:
                self.db_manager.execute_query(
                    "DELETE FROM warehouse_stock WHERE id = ?",
                    (stock[0],)
                )
                print(f"✅ تم حذف الرصيد المرتبط بالمخزن غير الموجود {stock[1]}")

        # فحص أرصدة المخزن - أصناف غير موجودة
        orphaned_stock_item = self.db_manager.fetch_all("""
            SELECT ws.id, ws.warehouse_id, ws.item_id
            FROM warehouse_stock ws
            LEFT JOIN items i ON ws.item_id = i.id
            WHERE ws.item_id IS NOT NULL AND i.id IS NULL
        """)

        if orphaned_stock_item:
            print(f"⚠️ تم العثور على {len(orphaned_stock_item)} رصيد مرتبط بأصناف غير موجودة")
            for stock in orphaned_stock_item:
                self.db_manager.execute_query(
                    "DELETE FROM warehouse_stock WHERE id = ?",
                    (stock[0],)
                )
                print(f"✅ تم حذف الرصيد المرتبط بالصنف غير الموجود {stock[2]}")

    def cleanup_corrupted_data(self):
        """تنظيف البيانات المكررة أو التالفة"""
        print("🔍 تنظيف البيانات المكررة والتالفة...")

        # حذف المخازن المكررة (نفس الكود)
        duplicate_warehouses = self.db_manager.fetch_all("""
            SELECT warehouse_code, COUNT(*) as count
            FROM warehouses
            GROUP BY warehouse_code
            HAVING COUNT(*) > 1
        """)

        if duplicate_warehouses:
            print(f"⚠️ تم العثور على {len(duplicate_warehouses)} مخزن مكرر")
            for dup in duplicate_warehouses:
                # الاحتفاظ بأول مخزن وحذف الباقي
                warehouse_ids = self.db_manager.fetch_all(
                    "SELECT id FROM warehouses WHERE warehouse_code = ? ORDER BY id",
                    (dup[0],)
                )
                for i in range(1, len(warehouse_ids)):
                    self.db_manager.execute_query(
                        "DELETE FROM warehouses WHERE id = ?",
                        (warehouse_ids[i][0],)
                    )
                    print(f"✅ تم حذف المخزن المكرر {dup[0]} (ID: {warehouse_ids[i][0]})")

        # حذف الأصناف المكررة (نفس الكود)
        duplicate_items = self.db_manager.fetch_all("""
            SELECT item_code, COUNT(*) as count
            FROM items
            GROUP BY item_code
            HAVING COUNT(*) > 1
        """)

        if duplicate_items:
            print(f"⚠️ تم العثور على {len(duplicate_items)} صنف مكرر")
            for dup in duplicate_items:
                item_ids = self.db_manager.fetch_all(
                    "SELECT id FROM items WHERE item_code = ? ORDER BY id",
                    (dup[0],)
                )
                for i in range(1, len(item_ids)):
                    self.db_manager.execute_query(
                        "DELETE FROM items WHERE id = ?",
                        (item_ids[i][0],)
                    )
                    print(f"✅ تم حذف الصنف المكرر {dup[0]} (ID: {item_ids[i][0]})")

        # حذف الحركات المكررة (نفس الرقم التسلسلي)
        duplicate_movements = self.db_manager.fetch_all("""
            SELECT serial_number, COUNT(*) as count
            FROM warehouse_movements
            GROUP BY serial_number
            HAVING COUNT(*) > 1
        """)

        if duplicate_movements:
            print(f"⚠️ تم العثور على {len(duplicate_movements)} حركة مكررة")
            for dup in duplicate_movements:
                movement_ids = self.db_manager.fetch_all(
                    "SELECT id FROM warehouse_movements WHERE serial_number = ? ORDER BY id",
                    (dup[0],)
                )
                for i in range(1, len(movement_ids)):
                    self.db_manager.execute_query(
                        "DELETE FROM warehouse_movements WHERE id = ?",
                        (movement_ids[i][0],)
                    )
                    print(f"✅ تم حذف الحركة المكررة {dup[0]} (ID: {movement_ids[i][0]})")

    def update_database_statistics(self):
        """تحديث إحصائيات قاعدة البيانات"""
        print("🔍 تحديث إحصائيات قاعدة البيانات...")

        try:
            # تحديث إحصائيات SQLite
            self.db_manager.execute_query("ANALYZE")

            # إعادة حساب أرصدة المخزن من الحركات
            print("📊 إعادة حساب أرصدة المخزن...")

            # حذف الأرصدة الحالية
            self.db_manager.execute_query("DELETE FROM warehouse_stock")

            # إعادة حساب الأرصدة من الحركات
            movements_summary = self.db_manager.fetch_all("""
                SELECT
                    warehouse_id,
                    item_id,
                    SUM(CASE
                        WHEN movement_type IN ('add', 'adjustment_in', 'transfer_in') THEN quantity
                        WHEN movement_type IN ('out', 'adjustment_out', 'transfer_out') THEN -quantity
                        ELSE 0
                    END) as total_quantity,
                    AVG(unit_price) as avg_price
                FROM warehouse_movements
                WHERE warehouse_id IS NOT NULL AND item_id IS NOT NULL
                GROUP BY warehouse_id, item_id
                HAVING total_quantity != 0
            """)

            for summary in movements_summary:
                warehouse_id, item_id, quantity, avg_price = summary
                total_value = quantity * (avg_price or 0)

                self.db_manager.execute_query("""
                    INSERT INTO warehouse_stock
                    (warehouse_id, item_id, quantity, last_cost, total_value, last_updated)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (warehouse_id, item_id, quantity, avg_price, total_value))

            print(f"✅ تم إعادة حساب {len(movements_summary)} رصيد مخزن")

            # تحديث المخزون الحالي في جدول المخازن
            warehouse_totals = self.db_manager.fetch_all("""
                SELECT
                    warehouse_id,
                    SUM(total_value) as total_stock_value
                FROM warehouse_stock
                GROUP BY warehouse_id
            """)

            for total in warehouse_totals:
                self.db_manager.execute_query(
                    "UPDATE warehouses SET current_stock = ? WHERE id = ?",
                    (total[1], total[0])
                )

            print(f"✅ تم تحديث قيم المخزون لـ {len(warehouse_totals)} مخزن")

            # إنشاء تقرير صحة قاعدة البيانات
            self.generate_database_health_report()

        except Exception as e:
            print(f"❌ خطأ في تحديث الإحصائيات: {e}")

    def generate_database_health_report(self):
        """إنشاء تقرير صحة قاعدة البيانات"""
        print("📋 إنشاء تقرير صحة قاعدة البيانات...")

        try:
            # إحصائيات الجداول
            tables_stats = {}
            tables = ['warehouses', 'items', 'warehouse_movements', 'warehouse_stock', 'warehouse_transfers']

            for table in tables:
                count = self.db_manager.fetch_one(f"SELECT COUNT(*) FROM {table}")[0]
                tables_stats[table] = count

            # إحصائيات إضافية
            active_warehouses = self.db_manager.fetch_one(
                "SELECT COUNT(*) FROM warehouses WHERE status = 'active'"
            )[0]

            active_items = self.db_manager.fetch_one(
                "SELECT COUNT(*) FROM items WHERE status = 'active'"
            )[0]

            low_stock_items = self.db_manager.fetch_all("""
                SELECT COUNT(*) FROM (
                    SELECT ws.item_id
                    FROM warehouse_stock ws
                    JOIN items i ON ws.item_id = i.id
                    WHERE ws.quantity < i.min_stock AND i.min_stock > 0
                )
            """)[0][0] if self.db_manager.fetch_all("""
                SELECT ws.item_id
                FROM warehouse_stock ws
                JOIN items i ON ws.item_id = i.id
                WHERE ws.quantity < i.min_stock AND i.min_stock > 0
            """) else 0

            total_stock_value = self.db_manager.fetch_one(
                "SELECT COALESCE(SUM(total_value), 0) FROM warehouse_stock"
            )[0]

            # طباعة التقرير
            print("\n" + "="*50)
            print("📊 تقرير صحة قاعدة البيانات")
            print("="*50)
            print(f"📦 إجمالي المخازن: {tables_stats['warehouses']} (نشط: {active_warehouses})")
            print(f"📋 إجمالي الأصناف: {tables_stats['items']} (نشط: {active_items})")
            print(f"🔄 إجمالي الحركات: {tables_stats['warehouse_movements']}")
            print(f"📊 إجمالي الأرصدة: {tables_stats['warehouse_stock']}")
            print(f"🔄 إجمالي التحويلات: {tables_stats['warehouse_transfers']}")
            print(f"⚠️ أصناف تحت الحد الأدنى: {low_stock_items}")
            print(f"💰 إجمالي قيمة المخزون: {total_stock_value:,.2f} جنيه")
            print("="*50)
            print("✅ قاعدة البيانات في حالة جيدة")
            print("="*50 + "\n")

        except Exception as e:
            print(f"❌ خطأ في إنشاء التقرير: {e}")

    def backup_database(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            from datetime import datetime
            import shutil
            import os

            # إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجوداً
            backup_dir = "database_backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # اسم ملف النسخة الاحتياطية
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"warehouse_db_backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_filename)

            # نسخ قاعدة البيانات
            if hasattr(self.db_manager, 'db_path'):
                shutil.copy2(self.db_manager.db_path, backup_path)
                print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
                return backup_path
            else:
                print("⚠️ لا يمكن تحديد مسار قاعدة البيانات للنسخ الاحتياطي")
                return None

        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return None

    def optimize_database(self):
        """تحسين أداء قاعدة البيانات"""
        print("🔧 تحسين أداء قاعدة البيانات...")

        try:
            # تنظيف قاعدة البيانات وإعادة تنظيمها
            self.db_manager.execute_query("VACUUM")
            print("✅ تم تنظيف قاعدة البيانات")

            # إعادة تحليل الإحصائيات
            self.db_manager.execute_query("ANALYZE")
            print("✅ تم تحديث إحصائيات الاستعلام")

            # فحص سلامة قاعدة البيانات
            integrity_check = self.db_manager.fetch_one("PRAGMA integrity_check")
            if integrity_check and integrity_check[0] == "ok":
                print("✅ فحص سلامة قاعدة البيانات: ممتاز")
            else:
                print(f"⚠️ مشكلة في سلامة قاعدة البيانات: {integrity_check}")

            print("✅ تم تحسين قاعدة البيانات بنجاح")

        except Exception as e:
            print(f"❌ خطأ في تحسين قاعدة البيانات: {e}")

    def get_database_size_info(self):
        """الحصول على معلومات حجم قاعدة البيانات"""
        try:
            # حجم الصفحات
            page_size = self.db_manager.fetch_one("PRAGMA page_size")[0]
            page_count = self.db_manager.fetch_one("PRAGMA page_count")[0]

            # حساب الحجم الإجمالي
            total_size = page_size * page_count

            # معلومات إضافية
            freelist_count = self.db_manager.fetch_one("PRAGMA freelist_count")[0]
            unused_size = freelist_count * page_size

            print(f"📊 معلومات حجم قاعدة البيانات:")
            print(f"   - حجم الصفحة: {page_size:,} بايت")
            print(f"   - عدد الصفحات: {page_count:,}")
            print(f"   - الحجم الإجمالي: {total_size:,} بايت ({total_size/1024/1024:.2f} ميجابايت)")
            print(f"   - المساحة غير المستخدمة: {unused_size:,} بايت")
            print(f"   - كفاءة الاستخدام: {((total_size-unused_size)/total_size*100):.1f}%")

            return {
                'page_size': page_size,
                'page_count': page_count,
                'total_size': total_size,
                'unused_size': unused_size,
                'efficiency': (total_size-unused_size)/total_size*100
            }

        except Exception as e:
            print(f"❌ خطأ في الحصول على معلومات الحجم: {e}")
            return None

    def generate_serial_number(self, movement_type):
        """توليد رقم تسلسلي تلقائي"""
        try:
            # تحديد البادئة حسب نوع العملية
            prefixes = {
                'add': 'ADD',
                'out': 'OUT', 
                'transfer': 'TRF',
                'adjustment': 'ADJ'
            }

            prefix = prefixes.get(movement_type, 'GEN')
            current_date = datetime.now()
            year_month = current_date.strftime("%Y-%m")

            # البحث عن آخر رقم تسلسلي لنفس النوع والشهر
            query = """
                SELECT serial_number FROM warehouse_movements 
                WHERE serial_number LIKE ? 
                ORDER BY serial_number DESC LIMIT 1
            """
            pattern = f"{prefix}-{year_month}-%"
            result = self.db_manager.fetch_one(query, (pattern,))

            if result:
                # استخراج الرقم التسلسلي وزيادته
                last_serial = result[0]
                last_number = int(last_serial.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            # تكوين الرقم التسلسلي الجديد
            serial_number = f"{prefix}-{year_month}-{new_number:03d}"
            return serial_number

        except Exception as e:
            print(f"خطأ في توليد الرقم التسلسلي: {e}")
            return f"GEN-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = ctk.CTkToplevel(self.parent)

        # إعداد النافذة لتملأ الشاشة
        configure_window_fullscreen(self.window, "🏪 إدارة المخازن والمستودعات - برنامج ست الكل للمحاسبة")
        self.window.configure(fg_color=WAREHOUSE_COLORS['background_main'])

        # جعل النافذة في المقدمة
        self.window.transient(self.parent)
        self.window.grab_set()

        # إنشاء التخطيط الرئيسي
        self.create_main_layout()

        # عرض لوحة التحكم الافتراضية
        self.show_dashboard()

    def create_main_layout(self):
        """إنشاء التخطيط الرئيسي على غرار أنظمة ERP"""
        # إطار رئيسي
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # الشريط الجانبي
        self.create_sidebar(main_container)

        # المحتوى الرئيسي
        self.create_main_content(main_container)

    def create_sidebar(self, parent):
        """إنشاء الشريط الجانبي المحسن والاحترافي"""
        # الشريط الجانبي الرئيسي مع تأثيرات بصرية
        sidebar = ctk.CTkFrame(
            parent,
            width=300,  # عرض أكبر قليلاً
            fg_color=WAREHOUSE_COLORS['sidebar_bg'],
            corner_radius=0,
            border_width=0
        )
        sidebar.pack(side="right", fill="y")
        sidebar.pack_propagate(False)

        # رأس الشريط الجانبي مع تصميم متطور
        header_frame = ctk.CTkFrame(
            sidebar,
            fg_color=WAREHOUSE_COLORS['dashboard_primary'],
            height=120,
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        # أيقونة كبيرة مع تأثير بصري
        icon_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        icon_frame.pack(expand=True)

        ctk.CTkLabel(
            icon_frame,
            text="🏪",
            font=ctk.CTkFont(size=48),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            icon_frame,
            text="إدارة المخازن الذكية",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['sidebar_title'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(pady=(0, 10))

        # خط فاصل أنيق
        separator = ctk.CTkFrame(
            sidebar,
            height=2,
            fg_color=WAREHOUSE_COLORS['border_medium'],
            corner_radius=1
        )
        separator.pack(fill="x", padx=20, pady=10)

        # قائمة التنقل المحسنة
        self.create_navigation_menu(sidebar)

    def create_navigation_menu(self, parent):
        """إنشاء قائمة التنقل المحسنة والمنظمة"""
        menu_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            scrollbar_button_color=WAREHOUSE_COLORS['sidebar_hover'],
            scrollbar_button_hover_color=WAREHOUSE_COLORS['sidebar_active']
        )
        menu_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # تجميع العناصر حسب الفئات مع ألوان مميزة
        menu_sections = [
            {
                "title": "📊 لوحة التحكم",
                "items": [
                    ("📊", "لوحة التحكم", "dashboard", WAREHOUSE_COLORS['dashboard_primary'])
                ]
            },
            {
                "title": "📦 العمليات اليومية",
                "items": [
                    ("📦", "إذن إضافة", "add_receipt", WAREHOUSE_COLORS['add_operation']),
                    ("📤", "إذن صرف", "out_receipt", WAREHOUSE_COLORS['out_operation']),
                    ("🔄", "تحويل بين المخازن", "transfer", WAREHOUSE_COLORS['transfer_operation']),
                    ("🏢", "تحويل بين الفروع", "branch_transfer", WAREHOUSE_COLORS['transfer_operation'])
                ]
            },
            {
                "title": "📋 التقارير والاستعلامات",
                "items": [
                    ("📋", "رصيد المخزن", "stock_balance", WAREHOUSE_COLORS['reports_primary']),
                    ("📈", "حركة الأصناف", "item_movements", WAREHOUSE_COLORS['reports_primary']),
                    ("💰", "أرباح الأصناف", "item_profits", WAREHOUSE_COLORS['accent_orange']),
                    ("📊", "تقرير المبيعات", "sales_report", WAREHOUSE_COLORS['reports_primary']),
                    ("🔍", "جرد المخازن", "inventory", WAREHOUSE_COLORS['inventory_primary'])
                ]
            },
            {
                "title": "🛠️ الأدوات المساعدة",
                "items": [
                    ("🏷️", "طباعة الباركود", "barcode", WAREHOUSE_COLORS['tools_primary']),
                    ("⚠️", "تنبيهات المخزن", "alerts", WAREHOUSE_COLORS['error_bg']),
                    ("🔧", "فحص قاعدة البيانات", "database_health", WAREHOUSE_COLORS['info'])
                ]
            }
        ]

        # إنشاء الأقسام
        for section in menu_sections:
            self.create_menu_section(menu_frame, section["title"], section["items"])

    def create_menu_section(self, parent, title, items):
        """إنشاء قسم في القائمة مع عنوان"""
        # عنوان القسم
        if title != "📊 لوحة التحكم":  # لا نحتاج عنوان للوحة التحكم
            section_label = ctk.CTkLabel(
                parent,
                text=title,
                font=ctk.CTkFont(
                    family=FONTS['arabic'],
                    size=WAREHOUSE_FONTS['caption_large'],
                    weight="bold"
                ),
                text_color=WAREHOUSE_COLORS['text_muted'],
                anchor="e"
            )
            section_label.pack(fill="x", pady=(15, 5), padx=5)

        # عناصر القسم
        for icon, text, view_id, color in items:
            self.create_menu_button(parent, icon, text, view_id, color)

        # خط فاصل بين الأقسام
        if title != "🛠️ الأدوات المساعدة":  # لا نحتاج خط بعد القسم الأخير
            separator = ctk.CTkFrame(
                parent,
                height=1,
                fg_color=WAREHOUSE_COLORS['border_medium'],
                corner_radius=0
            )
            separator.pack(fill="x", pady=10, padx=20)

    def create_menu_button(self, parent, icon, text, view_id, color):
        """إنشاء زر محسن في القائمة مع تأثيرات بصرية"""
        # إطار الزر مع تأثيرات
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=3, padx=5)

        button = ctk.CTkButton(
            button_frame,
            text=f"{icon}  {text}",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['sidebar_item'],
                weight="bold"
            ),
            fg_color="transparent",
            hover_color=WAREHOUSE_COLORS['sidebar_hover'],
            text_color=WAREHOUSE_COLORS['text_white'],
            anchor="e",
            height=55,  # ارتفاع أكبر
            corner_radius=12,  # زوايا أكثر استدارة
            border_width=0,
            command=lambda: self.switch_view(view_id)
        )
        button.pack(fill="x")

        # إضافة مؤشر جانبي للقسم النشط
        indicator = ctk.CTkFrame(
            button_frame,
            width=4,
            height=35,
            fg_color=color,
            corner_radius=2
        )
        indicator.place(x=0, y=10)
        indicator.place_forget()  # مخفي افتراضياً

        # حفظ مراجع الزر والمؤشر
        self.sidebar_buttons[view_id] = {
            'button': button,
            'indicator': indicator,
            'color': color
        }

    def create_main_content(self, parent):
        """إنشاء منطقة المحتوى الرئيسي"""
        self.main_content_frame = ctk.CTkFrame(
            parent,
            fg_color=WAREHOUSE_COLORS['main_content'],
            corner_radius=0
        )
        self.main_content_frame.pack(side="left", fill="both", expand=True)

    # تحذير: دالة معقدة (تعقيد: 21) - استخدم list comprehensions بدلاً من loops معقدة
    def switch_view(self, view_id):
        """تبديل العرض مع تأثيرات بصرية محسنة"""
        # تحديث حالة الأزرار والمؤشرات
        for btn_id, btn_data in self.sidebar_buttons.items():
            if isinstance(btn_data, dict):  # النظام الجديد
                button = btn_data['button']
                indicator = btn_data['indicator']
                color = btn_data['color']

                if btn_id == view_id:
                    # تفعيل الزر النشط
                    button.configure(
                        fg_color=WAREHOUSE_COLORS['sidebar_active'],
                        text_color=WAREHOUSE_COLORS['text_white']
                    )
                    indicator.place(x=0, y=10)  # إظهار المؤشر
                else:
                    # إلغاء تفعيل الأزرار الأخرى
                    button.configure(
                        fg_color="transparent",
                        text_color=WAREHOUSE_COLORS['text_white']
                    )
                    indicator.place_forget()  # إخفاء المؤشر
            else:  # النظام القديم (للتوافق)
                if btn_id == view_id:
                    btn_data.configure(fg_color=WAREHOUSE_COLORS['sidebar_hover'])
                else:
                    btn_data.configure(fg_color="transparent")

        # مسح المحتوى الحالي مع تأثير انتقال
        for widget in self.main_content_frame.winfo_children():
            if widget and hasattr(widget, "destroy"):

                widget.destroy()

        # عرض المحتوى الجديد
        self.current_view = view_id

        # توجيه إلى الدوال المناسبة
        if view_id == "dashboard":
            self.show_dashboard()
        elif view_id == "add_receipt":
            self.show_add_receipt()
        elif view_id == "out_receipt":
            self.show_out_receipt()
        elif view_id == "transfer":
            self.show_transfer()
        elif view_id == "branch_transfer":
            self.show_coming_soon(view_id)
        elif view_id == "stock_balance":
            self.show_stock_balance()
        elif view_id == "item_movements":
            self.show_item_movements()
        elif view_id == "item_profits":
            self.show_coming_soon(view_id)
        elif view_id == "sales_report":
            self.show_coming_soon(view_id)
        elif view_id == "inventory":
            self.show_coming_soon(view_id)
        elif view_id == "barcode":
            self.show_barcode_generator()
        elif view_id == "alerts":
            self.show_coming_soon(view_id)
        elif view_id == "database_health":
            self.show_database_health_report()
        else:
            self.show_coming_soon(view_id)

    def show_dashboard(self):
        """عرض لوحة التحكم الرئيسية المحسنة"""
        # إطار لوحة التحكم مع خلفية متدرجة
        dashboard_frame = ctk.CTkScrollableFrame(
            self.main_content_frame,
            fg_color=WAREHOUSE_COLORS['background_main'],
            corner_radius=0
        )
        dashboard_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # رأس لوحة التحكم مع تصميم متطور
        header_frame = ctk.CTkFrame(
            dashboard_frame,
            fg_color=WAREHOUSE_COLORS['dashboard_primary'],
            height=120,
            corner_radius=20,
            border_width=0
        )
        header_frame.pack(fill="x", pady=20, padx=20)
        header_frame.pack_propagate(False)

        # محتوى الرأس
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(expand=True, fill="both", padx=30, pady=20)

        # العنوان الرئيسي
        ctk.CTkLabel(
            header_content,
            text="📊 لوحة التحكم الذكية",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['hero_title'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(anchor="e")

        # النص الفرعي
        ctk.CTkLabel(
            header_content,
            text="إدارة شاملة ومتطورة لجميع عمليات المخازن والمستودعات",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_large']
            ),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(anchor="e", pady=(5, 0))

        # إحصائيات سريعة محسنة
        self.create_enhanced_quick_stats(dashboard_frame)

        # العمليات السريعة محسنة
        self.create_enhanced_quick_operations(dashboard_frame)

        # التنبيهات والتحديثات محسنة
        self.create_enhanced_alerts_section(dashboard_frame)

    def create_enhanced_quick_stats(self, parent):
        """إنشاء قسم الإحصائيات السريعة المحسن"""
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="x", pady=20, padx=20)

        # عنوان القسم
        section_header = ctk.CTkFrame(stats_container, fg_color="transparent")
        section_header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            section_header,
            text="📈 الإحصائيات السريعة",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['title_medium'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(anchor="e")

        ctk.CTkLabel(
            section_header,
            text="نظرة سريعة على أهم المؤشرات",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_medium']
            ),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(anchor="e", pady=(2, 0))

        # إطار البطاقات مع تخطيط شبكي
        cards_grid = ctk.CTkFrame(stats_container, fg_color="transparent")
        cards_grid.pack(fill="x", pady=10)

        # بطاقات الإحصائيات المحسنة
        stats_data = [
            ("🏪", "إجمالي المخازن", "3", "مخازن نشطة", WAREHOUSE_COLORS['inventory_primary']),
            ("�", "إجمالي الأصناف", "150", "صنف متاح", WAREHOUSE_COLORS['add_operation']),
            ("💰", "قيمة المخزون", "2,500,000", "جنيه مصري", WAREHOUSE_COLORS['accent_orange']),
            ("⚠️", "تحت الحد الأدنى", "12", "صنف يحتاج تجديد", WAREHOUSE_COLORS['out_operation'])
        ]

        # إنشاء البطاقات في صفوف
        for i in range(0, len(stats_data), 2):
            row_frame = ctk.CTkFrame(cards_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)

            # البطاقة الأولى
            if i < len(stats_data):
                icon, title, value, subtitle, color = stats_data[i]
                self.create_enhanced_stat_card(row_frame, icon, title, value, subtitle, color, "right")

            # البطاقة الثانية
            if i + 1 < len(stats_data):
                icon, title, value, subtitle, color = stats_data[i + 1]
                self.create_enhanced_stat_card(row_frame, icon, title, value, subtitle, color, "left")

    def create_enhanced_stat_card(self, parent, icon, title, value, subtitle, color, side):
        """إنشاء بطاقة إحصائية محسنة مع تأثيرات بصرية"""
        # إطار البطاقة مع ظلال وتأثيرات
        card_container = ctk.CTkFrame(parent, fg_color="transparent")
        if side == "right":
            card_container.pack(side="right", fill="both", expand=True, padx=(0, 10))
        else:
            card_container.pack(side="left", fill="both", expand=True, padx=(10, 0))

        card = ctk.CTkFrame(
            card_container,
            fg_color=WAREHOUSE_COLORS['card_bg'],
            corner_radius=20,
            border_width=1,
            border_color=WAREHOUSE_COLORS['border_light'],
            height=120
        )
        card.pack(fill="both", expand=True, pady=5)
        card.pack_propagate(False)

        # محتوى البطاقة
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # الصف العلوي - الأيقونة والعنوان
        top_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 10))

        # الأيقونة مع خلفية ملونة
        icon_frame = ctk.CTkFrame(
            top_row,
            fg_color=color,
            corner_radius=12,
            width=40,
            height=40
        )
        icon_frame.pack(side="right")
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=ctk.CTkFont(size=20),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(expand=True)

        # العنوان
        ctk.CTkLabel(
            top_row,
            text=title,
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_medium'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_primary'],
            anchor="e"
        ).pack(side="right", padx=(0, 15))

        # الصف السفلي - القيمة والوصف
        bottom_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_row.pack(fill="x")

        # القيمة الرئيسية
        ctk.CTkLabel(
            bottom_row,
            text=value,
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['title_small'],
                weight="bold"
            ),
            text_color=color,
            anchor="e"
        ).pack(anchor="e")

        # النص الفرعي
        ctk.CTkLabel(
            bottom_row,
            text=subtitle,
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['caption_medium']
            ),
            text_color=WAREHOUSE_COLORS['text_secondary'],
            anchor="e"
        ).pack(anchor="e", pady=(2, 0))

    def create_stat_card(self, parent, icon, title, value, color, index):
        """إنشاء بطاقة إحصائية"""
        card = ctk.CTkFrame(
            parent,
            fg_color=WAREHOUSE_COLORS['card_bg'],
            corner_radius=15,
            border_width=2,
            border_color=color
        )
        card.grid(row=0, column=index, padx=10, pady=10, sticky="ew")
        parent.grid_columnconfigure(index, weight=1)

        # أيقونة
        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=40),
            text_color=color
        ).pack(pady=(20, 5))

        # القيمة
        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['title_medium'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(pady=5)

        # العنوان
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large']),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(pady=(5, 20))

    def create_enhanced_quick_operations(self, parent):
        """إنشاء قسم العمليات السريعة المحسن"""
        operations_container = ctk.CTkFrame(parent, fg_color="transparent")
        operations_container.pack(fill="x", pady=20, padx=20)

        # عنوان القسم
        section_header = ctk.CTkFrame(operations_container, fg_color="transparent")
        section_header.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            section_header,
            text="⚡ العمليات السريعة",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['title_medium'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(anchor="e")

        ctk.CTkLabel(
            section_header,
            text="الوصول السريع للعمليات الأكثر استخداماً",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_medium']
            ),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(anchor="e", pady=(2, 0))

        # إطار الأزرار المحسن
        buttons_grid = ctk.CTkFrame(operations_container, fg_color="transparent")
        buttons_grid.pack(fill="x", pady=10)

        # أزرار العمليات السريعة المحسنة
        operations = [
            ("📦", "إذن إضافة", "إضافة أصناف جديدة", "add_receipt", WAREHOUSE_COLORS['add_operation']),
            ("📤", "إذن صرف", "صرف من المخزن", "out_receipt", WAREHOUSE_COLORS['out_operation']),
            ("🔄", "تحويل", "نقل بين المخازن", "transfer", WAREHOUSE_COLORS['transfer_operation']),
            ("📋", "رصيد المخزن", "عرض الأرصدة", "stock_balance", WAREHOUSE_COLORS['reports_primary'])
        ]

        # إنشاء الأزرار في صفين
        for i in range(0, len(operations), 2):
            row_frame = ctk.CTkFrame(buttons_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=8)

            # الزر الأول
            if i < len(operations):
                icon, title, desc, view_id, color = operations[i]
                self.create_enhanced_operation_button(row_frame, icon, title, desc, view_id, color, "right")

            # الزر الثاني
            if i + 1 < len(operations):
                icon, title, desc, view_id, color = operations[i + 1]
                self.create_enhanced_operation_button(row_frame, icon, title, desc, view_id, color, "left")

    def create_enhanced_operation_button(self, parent, icon, title, description, view_id, color, side):
        """إنشاء زر عملية محسن مع تأثيرات بصرية"""
        # إطار الزر
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        if side == "right":
            button_container.pack(side="right", fill="both", expand=True, padx=(0, 10))
        else:
            button_container.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # الزر الرئيسي مع تصميم متطور
        button = ctk.CTkButton(
            button_container,
            text="",  # سنضع المحتوى يدوياً
            fg_color=color,
            hover_color=self.get_hover_color(color),
            corner_radius=18,
            height=100,
            border_width=0,
            command=lambda: self.switch_view(view_id)
        )
        button.pack(fill="both", expand=True)

        # محتوى الزر
        content_frame = ctk.CTkFrame(button, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # الأيقونة
        ctk.CTkLabel(
            content_frame,
            text=icon,
            font=ctk.CTkFont(size=32),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(pady=(5, 2))

        # العنوان
        ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['button_large'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(pady=(0, 2))

        # الوصف
        ctk.CTkLabel(
            content_frame,
            text=description,
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['caption_large']
            ),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(pady=(0, 5))

    def create_alerts_section(self, parent):
        """إنشاء قسم التنبيهات"""
        alerts_frame = ctk.CTkFrame(
            parent,
            fg_color=WAREHOUSE_COLORS['card_bg'],
            corner_radius=15,
            border_width=2,
            border_color=WAREHOUSE_COLORS['text_warning']
        )
        alerts_frame.pack(fill="x", pady=20)

        # رأس القسم
        header_frame = ctk.CTkFrame(alerts_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            header_frame,
            text="🔔 التنبيهات والإشعارات",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['title_medium'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(anchor="e")

        ctk.CTkLabel(
            header_frame,
            text="تنبيهات مهمة تحتاج انتباهك",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_medium']),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(anchor="e", pady=(2, 0))

        # قائمة التنبيهات
        alerts_list = [
            "🔴 12 صنف تحت الحد الأدنى للمخزون",
            "🟡 5 أصناف لم تتحرك منذ 30 يوم",
            "🟢 تم إضافة 25 صنف جديد هذا الأسبوع",
            "🔵 3 عمليات تحويل في انتظار الموافقة"
        ]

        for alert in alerts_list:
            alert_label = ctk.CTkLabel(
                alerts_frame,
                text=alert,
                font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large']),
                text_color=WAREHOUSE_COLORS['text_primary'],
                anchor="e"
            )
            alert_label.pack(fill="x", padx=20, pady=5)

    def create_enhanced_alerts_section(self, parent):
        """إنشاء قسم التنبيهات المحسن"""
        alerts_container = ctk.CTkFrame(parent, fg_color="transparent")
        alerts_container.pack(fill="x", pady=20, padx=20)

        # عنوان القسم
        section_header = ctk.CTkFrame(alerts_container, fg_color="transparent")
        section_header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            section_header,
            text="🔔 التنبيهات والإشعارات",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['title_medium'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(anchor="e")

        ctk.CTkLabel(
            section_header,
            text="تنبيهات مهمة تحتاج انتباهك",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_medium']
            ),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(anchor="e", pady=(2, 0))

        # إطار التنبيهات الرئيسي
        alerts_frame = ctk.CTkFrame(
            alerts_container,
            fg_color=WAREHOUSE_COLORS['card_bg'],
            corner_radius=20,
            border_width=1,
            border_color=WAREHOUSE_COLORS['border_light']
        )
        alerts_frame.pack(fill="x", pady=10)

        # قائمة التنبيهات المحسنة
        alerts_data = [
            ("⚠️", "أصناف تحت الحد الأدنى", "12 صنف يحتاج إعادة طلب", WAREHOUSE_COLORS['warning_bg'], WAREHOUSE_COLORS['text_warning']),
            ("📦", "عمليات معلقة", "3 عمليات تحويل في الانتظار", WAREHOUSE_COLORS['info_bg'], WAREHOUSE_COLORS['info']),
            ("🔄", "آخر تحديث", "تم تحديث الأرصدة منذ 5 دقائق", WAREHOUSE_COLORS['success_bg'], WAREHOUSE_COLORS['success'])
        ]

        for i, (icon, title, description, bg_color, text_color) in enumerate(alerts_data):
            self.create_enhanced_alert_item(alerts_frame, icon, title, description, bg_color, text_color, i == len(alerts_data) - 1)

    def create_enhanced_alert_item(self, parent, icon, title, description, bg_color, text_color, is_last=False):
        """إنشاء عنصر تنبيه محسن"""
        # إطار العنصر
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=15,
            height=70
        )
        item_frame.pack(fill="x", padx=20, pady=(15, 15 if is_last else 8))
        item_frame.pack_propagate(False)

        # محتوى العنصر
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # الصف العلوي - الأيقونة والعنوان
        top_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 5))

        # الأيقونة
        ctk.CTkLabel(
            top_row,
            text=icon,
            font=ctk.CTkFont(size=20),
            text_color=text_color
        ).pack(side="right", padx=(0, 10))

        # العنوان
        ctk.CTkLabel(
            top_row,
            text=title,
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_large'],
                weight="bold"
            ),
            text_color=text_color,
            anchor="e"
        ).pack(side="right")

        # الوصف
        ctk.CTkLabel(
            content_frame,
            text=description,
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_medium']
            ),
            text_color=WAREHOUSE_COLORS['text_secondary'],
            anchor="e"
        ).pack(anchor="e")

    def get_hover_color(self, base_color):
        """الحصول على لون التفاعل المحسن"""
        hover_colors = {
            WAREHOUSE_COLORS['add_operation']: WAREHOUSE_COLORS['add_hover'],
            WAREHOUSE_COLORS['out_operation']: WAREHOUSE_COLORS['out_hover'],
            WAREHOUSE_COLORS['transfer_operation']: WAREHOUSE_COLORS['transfer_hover'],
            WAREHOUSE_COLORS['report_operation']: WAREHOUSE_COLORS['report_hover'],
            WAREHOUSE_COLORS['reports_primary']: WAREHOUSE_COLORS['reports_secondary'],
            WAREHOUSE_COLORS['inventory_primary']: WAREHOUSE_COLORS['inventory_secondary'],
            WAREHOUSE_COLORS['dashboard_primary']: WAREHOUSE_COLORS['dashboard_secondary'],
            WAREHOUSE_COLORS['tools_primary']: WAREHOUSE_COLORS['tools_secondary']
        }
        return hover_colors.get(base_color, base_color)

    def show_add_receipt(self):
        """عرض نافذة إذن الإضافة"""
        # إطار إذن الإضافة
        receipt_frame = ctk.CTkScrollableFrame(
            self.main_content_frame,
            fg_color="transparent"
        )
        receipt_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # عنوان الإذن
        title_frame = ctk.CTkFrame(
            receipt_frame,
            fg_color=WAREHOUSE_COLORS['add_operation'],
            height=80,
            corner_radius=15
        )
        title_frame.pack(fill="x", pady=(0, 20))
        title_frame.pack_propagate(False)

        ctk.CTkLabel(
            title_frame,
            text="📦 إذن إضافة للمخزن",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['title_large'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_white']
        ).pack(expand=True)

        # معلومات الإذن
        self.create_receipt_header(receipt_frame, "add")

        # تفاصيل الأصناف
        self.create_items_section(receipt_frame)

        # أزرار الحفظ والطباعة
        self.create_receipt_buttons(receipt_frame, "add")

    def show_out_receipt(self):
        """عرض نافذة إذن الصرف"""
        # مشابه لإذن الإضافة مع تغيير الألوان
        self.show_add_receipt()  # مؤقتاً

    def show_transfer(self):
        """عرض نافذة التحويل"""
        messagebox.showinfo("قريباً", "سيتم إضافة نافذة التحويل قريباً")

    def show_stock_balance(self):
        """عرض رصيد المخزن"""
        messagebox.showinfo("قريباً", "سيتم إضافة تقرير رصيد المخزن قريباً")

    def show_item_movements(self):
        """عرض حركة الأصناف"""
        messagebox.showinfo("قريباً", "سيتم إضافة تقرير حركة الأصناف قريباً")

    def show_barcode_generator(self):
        """عرض مولد الباركود"""
        messagebox.showinfo("قريباً", "سيتم إضافة مولد الباركود قريباً")

    def show_coming_soon(self, view_id):
        """عرض رسالة قريباً للميزات قيد التطوير مع تصميم محسن"""
        # إطار رئيسي مع خلفية متدرجة
        coming_container = ctk.CTkFrame(
            self.main_content_frame,
            fg_color=WAREHOUSE_COLORS['background_main'],
            corner_radius=0
        )
        coming_container.pack(fill="both", expand=True)

        # إطار المحتوى المركزي
        content_frame = ctk.CTkFrame(
            coming_container,
            fg_color=WAREHOUSE_COLORS['card_bg'],
            corner_radius=25,
            border_width=1,
            border_color=WAREHOUSE_COLORS['border_light']
        )
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.6)

        # أيقونة كبيرة مع خلفية ملونة
        icon_frame = ctk.CTkFrame(
            content_frame,
            fg_color=WAREHOUSE_COLORS['info_bg'],
            corner_radius=50,
            width=100,
            height=100
        )
        icon_frame.pack(pady=(50, 20))
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(
            icon_frame,
            text="🚧",
            font=ctk.CTkFont(size=60),
            text_color=WAREHOUSE_COLORS['info']
        ).pack(expand=True)

        # رسالة رئيسية
        ctk.CTkLabel(
            content_frame,
            text="هذه الميزة قيد التطوير",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['title_large'],
                weight="bold"
            ),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(pady=(0, 10))

        # رسالة فرعية
        ctk.CTkLabel(
            content_frame,
            text="سيتم إضافتها في التحديث القادم إن شاء الله",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['body_large']
            ),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(pady=(0, 20))

        # زر العودة للوحة التحكم
        back_button = ctk.CTkButton(
            content_frame,
            text="🏠 العودة للوحة التحكم",
            font=ctk.CTkFont(
                family=FONTS['arabic'],
                size=WAREHOUSE_FONTS['button_medium'],
                weight="bold"
            ),
            fg_color=WAREHOUSE_COLORS['dashboard_primary'],
            hover_color=WAREHOUSE_COLORS['dashboard_secondary'],
            corner_radius=15,
            height=45,
            width=200,
            command=lambda: self.switch_view("dashboard")
        )
        back_button.pack(pady=(0, 30))

        # زر العودة للوحة التحكم
        ctk.CTkButton(
            coming_frame,
            text="🏠 العودة للوحة التحكم",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            fg_color=WAREHOUSE_COLORS['accent_blue'],
            hover_color=WAREHOUSE_COLORS['transfer_hover'],
            width=200,
            height=50,
            corner_radius=15,
            command=lambda: self.switch_view("dashboard")
        ).pack(expand=True)

    def show_out_receipt(self):
        """عرض نافذة إذن الصرف"""
        # مشابه لإذن الإضافة مع تغيير الألوان
        self.show_add_receipt()  # مؤقتاً

    def show_transfer(self):
        """عرض نافذة التحويل"""
        messagebox.showinfo("قريباً", "سيتم إضافة نافذة التحويل قريباً")

    def show_stock_balance(self):
        """عرض رصيد المخزن"""
        messagebox.showinfo("قريباً", "سيتم إضافة تقرير رصيد المخزن قريباً")

    def show_item_movements(self):
        """عرض حركة الأصناف"""
        messagebox.showinfo("قريباً", "سيتم إضافة تقرير حركة الأصناف قريباً")

    def show_barcode_generator(self):
        """عرض مولد الباركود"""
        messagebox.showinfo("قريباً", "سيتم إضافة مولد الباركود قريباً")

    def show_coming_soon(self, view_id):
        """عرض رسالة قريباً"""
        coming_frame = ctk.CTkFrame(
            self.main_content_frame,
            fg_color="transparent"
        )
        coming_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            coming_frame,
            text="🚧",
            font=ctk.CTkFont(size=100),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(expand=True)

        ctk.CTkLabel(
            coming_frame,
            text="هذه الميزة قيد التطوير",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['title_large'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(expand=True)

        ctk.CTkLabel(
            coming_frame,
            text="سيتم إضافتها في التحديث القادم",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large']),
            text_color=WAREHOUSE_COLORS['text_secondary']
        ).pack(expand=True)

    def create_receipt_header(self, parent, receipt_type):
        """إنشاء رأس الإذن"""
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=WAREHOUSE_COLORS['card_bg'],
            corner_radius=15,
            border_width=2,
            border_color=WAREHOUSE_COLORS['border_light']
        )
        header_frame.pack(fill="x", pady=10)

        # الصف الأول
        row1 = ctk.CTkFrame(header_frame, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=15)

        # الرقم التسلسلي
        ctk.CTkLabel(
            row1,
            text="الرقم التسلسلي:",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(side="right", padx=10)

        self.serial_number_var = tk.StringVar(value=self.generate_serial_number(receipt_type))
        serial_entry = ctk.CTkEntry(
            row1,
            textvariable=self.serial_number_var,
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            width=200,
            height=40,
            state="readonly",
            fg_color=WAREHOUSE_COLORS['accent_blue'],
            text_color=WAREHOUSE_COLORS['text_white']
        )
        serial_entry.pack(side="right", padx=10)

        # التاريخ
        ctk.CTkLabel(
            row1,
            text="التاريخ:",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(side="left", padx=10)

        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ctk.CTkEntry(
            row1,
            textvariable=self.date_var,
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large']),
            width=150,
            height=40
        )
        date_entry.pack(side="left", padx=10)

        # الصف الثاني
        row2 = ctk.CTkFrame(header_frame, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=15)

        # المخزن
        ctk.CTkLabel(
            row2,
            text="المخزن:",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(side="right", padx=10)

        self.warehouse_combo = ctk.CTkComboBox(
            row2,
            values=self.get_warehouses_list(),
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large']),
            width=200,
            height=40
        )
        self.warehouse_combo.pack(side="right", padx=10)

        # رقم المرجع
        ctk.CTkLabel(
            row2,
            text="رقم المرجع:",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(side="left", padx=10)

        self.reference_entry = ctk.CTkEntry(
            row2,
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large']),
            width=150,
            height=40,
            placeholder_text="اختياري"
        )
        self.reference_entry.pack(side="left", padx=10)

    def create_items_section(self, parent):
        """إنشاء قسم الأصناف"""
        items_frame = ctk.CTkFrame(
            parent,
            fg_color=WAREHOUSE_COLORS['card_bg'],
            corner_radius=15,
            border_width=2,
            border_color=WAREHOUSE_COLORS['border_light']
        )
        items_frame.pack(fill="both", expand=True, pady=10)

        # عنوان القسم
        ctk.CTkLabel(
            items_frame,
            text="📋 تفاصيل الأصناف",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['title_medium'], weight="bold"),
            text_color=WAREHOUSE_COLORS['text_primary']
        ).pack(anchor="e", padx=20, pady=10)

        # إطار إضافة صنف
        add_item_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
        add_item_frame.pack(fill="x", padx=20, pady=10)

        # حقول إضافة الصنف
        fields_frame = ctk.CTkFrame(add_item_frame, fg_color="transparent")
        fields_frame.pack(fill="x", pady=10)

        # الصنف
        ctk.CTkLabel(
            fields_frame,
            text="الصنف:",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.item_combo = ctk.CTkComboBox(
            fields_frame,
            values=self.get_items_list(),
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_medium']),
            width=200
        )
        self.item_combo.grid(row=0, column=1, padx=10, pady=5)

        # الكمية
        ctk.CTkLabel(
            fields_frame,
            text="الكمية:",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold")
        ).grid(row=0, column=2, padx=10, pady=5, sticky="e")

        self.quantity_entry = ctk.CTkEntry(
            fields_frame,
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_medium']),
            width=100
        )
        self.quantity_entry.grid(row=0, column=3, padx=10, pady=5)

        # السعر
        ctk.CTkLabel(
            fields_frame,
            text="السعر:",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold")
        ).grid(row=0, column=4, padx=10, pady=5, sticky="e")

        self.price_entry = ctk.CTkEntry(
            fields_frame,
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_medium']),
            width=100
        )
        self.price_entry.grid(row=0, column=5, padx=10, pady=5)

        # زر الإضافة
        add_button = ctk.CTkButton(
            fields_frame,
            text="➕ إضافة",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_medium'], weight="bold"),
            fg_color=WAREHOUSE_COLORS['add_operation'],
            hover_color=WAREHOUSE_COLORS['add_hover'],
            width=100,
            height=35,
            command=self.add_item_to_list
        )
        add_button.grid(row=0, column=6, padx=10, pady=5)

        # جدول الأصناف
        self.create_items_table(items_frame)

    def get_warehouses_list(self):
        """الحصول على قائمة المخازن"""
        try:
            result = self.db_manager.fetch_all("SELECT name FROM warehouses WHERE status = 'active'")
            return [row[0] for row in result] if result else ["المخزن الرئيسي"]
        except:
            return ["المخزن الرئيسي"]

    def get_items_list(self):
        """الحصول على قائمة الأصناف"""
        try:
            result = self.db_manager.fetch_all("SELECT name FROM items WHERE status = 'active'")
            return [row[0] for row in result] if result else ["لابتوب ديل", "طابعة HP"]
        except:
            return ["لابتوب ديل", "طابعة HP"]

    def create_items_table(self, parent):
        """إنشاء جدول الأصناف"""
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # إنشاء Treeview
        columns = ("الصنف", "الكمية", "الوحدة", "السعر", "الإجمالي")
        self.items_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        # تعريف العناوين
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=120, anchor="center")

        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)

        # تخطيط الجدول
        self.items_tree.pack(side="right", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

    def add_item_to_list(self):
        """إضافة صنف إلى القائمة"""
        try:
            item_name = self.item_combo.get()
            quantity = float(self.quantity_entry.get() or 0)
            price = float(self.price_entry.get() or 0)

            if not item_name or quantity <= 0 or price <= 0:
                messagebox.showerror("خطأ", "يرجى إدخال جميع البيانات بشكل صحيح")
                return

            total = quantity * price

            # إضافة إلى الجدول
            self.items_tree.insert("", "end", values=(
                item_name,
                f"{quantity:.2f}",
                "قطعة",  # يمكن تحسينها لاحقاً
                f"{price:.2f}",
                f"{total:.2f}"
            ))

            # مسح الحقول
            self.quantity_entry.delete(0, "end")
            self.price_entry.delete(0, "end")

        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للكمية والسعر")

    def create_receipt_buttons(self, parent, receipt_type):
        """إنشاء أزرار الإذن"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)

        # زر الحفظ
        save_button = ctk.CTkButton(
            buttons_frame,
            text="💾 حفظ الإذن",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            fg_color=WAREHOUSE_COLORS['add_operation'],
            hover_color=WAREHOUSE_COLORS['add_hover'],
            width=150,
            height=50,
            corner_radius=15,
            command=lambda: self.save_receipt(receipt_type)
        )
        save_button.pack(side="left", padx=10)

        # زر الطباعة
        print_button = ctk.CTkButton(
            buttons_frame,
            text="🖨️ طباعة",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            fg_color=WAREHOUSE_COLORS['accent_blue'],
            hover_color=WAREHOUSE_COLORS['transfer_hover'],
            width=150,
            height=50,
            corner_radius=15,
            command=self.print_receipt
        )
        print_button.pack(side="left", padx=10)

        # زر إلغاء
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ إلغاء",
            font=ctk.CTkFont(family=FONTS['arabic'], size=WAREHOUSE_FONTS['body_large'], weight="bold"),
            fg_color=WAREHOUSE_COLORS['out_operation'],
            hover_color=WAREHOUSE_COLORS['out_hover'],
            width=150,
            height=50,
            corner_radius=15,
            command=self.cancel_receipt
        )
        cancel_button.pack(side="left", padx=10)

    def save_receipt(self, receipt_type):
        """حفظ الإذن"""
        try:
            # التحقق من البيانات
            if not self.warehouse_combo.get():
                messagebox.showerror("خطأ", "يرجى اختيار المخزن")
                return

            if not self.items_tree.get_children():
                messagebox.showerror("خطأ", "يرجى إضافة أصناف للإذن")
                return

            # حفظ الإذن في قاعدة البيانات
            serial_number = self.serial_number_var.get()

            # هنا يمكن إضافة كود حفظ الإذن
            messagebox.showinfo("نجح", f"تم حفظ الإذن رقم {serial_number} بنجاح")

        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ الإذن: {e}")

    def print_receipt(self):
        """طباعة الإذن"""
        messagebox.showinfo("طباعة", "سيتم إضافة وظيفة الطباعة قريباً")

    def cancel_receipt(self):
        """إلغاء الإذن"""
        if messagebox.askyesno("تأكيد", "هل تريد إلغاء الإذن؟"):
            self.show_dashboard()
