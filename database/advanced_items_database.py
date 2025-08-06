# -*- coding: utf-8 -*-
"""
قاعدة البيانات المتقدمة للأصناف
Advanced Items Database Manager
"""

import sqlite3
import json
import uuid
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging

class AdvancedItemsDatabase:
    """مدير قاعدة البيانات المتقدمة للأصناف"""
    
    def __init__(self, db_path: str = None):
        self.project_root = Path(__file__).parent.parent
        self.db_path = db_path or str(self.project_root / "database" / "advanced_items.db")
        self.connection = None
        
        # إعداد نظام السجلات
        self.setup_logging()
        
        # تهيئة قاعدة البيانات
        self.init_database()
    
    def setup_logging(self):
        """إعداد نظام السجلات"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "items_database.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_connection(self) -> sqlite3.Connection:
        """الحصول على اتصال قاعدة البيانات"""
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False,
                    timeout=30.0
                )
                self.connection.row_factory = sqlite3.Row
                self.connection.execute("PRAGMA foreign_keys = ON")
                self.connection.execute("PRAGMA journal_mode = WAL")
                self.logger.info("تم إنشاء اتصال قاعدة البيانات بنجاح")
            except Exception as e:
                self.logger.error(f"فشل في الاتصال بقاعدة البيانات: {e}")
                raise
        return self.connection
    
    def init_database(self):
        """تهيئة قاعدة البيانات وإنشاء الجداول"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # جدول الفئات الرئيسية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    name_en TEXT,
                    description TEXT,
                    parent_id INTEGER,
                    level INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES categories (id)
                )
            ''')
            
            # جدول الوحدات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS units (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    name_en TEXT,
                    symbol TEXT,
                    base_unit_id INTEGER,
                    conversion_factor DECIMAL(15,6) DEFAULT 1.0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (base_unit_id) REFERENCES units (id)
                )
            ''')
            
            # جدول الأصناف الرئيسي
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uuid TEXT UNIQUE NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    name_en TEXT,
                    description TEXT,
                    category_id INTEGER,
                    unit_id INTEGER,
                    barcode TEXT,
                    qr_code TEXT,
                    
                    -- معلومات التسعير
                    cost_price DECIMAL(15,4) DEFAULT 0.0,
                    selling_price DECIMAL(15,4) DEFAULT 0.0,
                    min_selling_price DECIMAL(15,4) DEFAULT 0.0,
                    max_selling_price DECIMAL(15,4) DEFAULT 0.0,
                    profit_margin DECIMAL(5,2) DEFAULT 0.0,
                    tax_rate DECIMAL(5,2) DEFAULT 0.0,
                    discount_rate DECIMAL(5,2) DEFAULT 0.0,
                    
                    -- معلومات المخزون
                    current_stock DECIMAL(15,4) DEFAULT 0.0,
                    min_stock_level DECIMAL(15,4) DEFAULT 0.0,
                    max_stock_level DECIMAL(15,4) DEFAULT 0.0,
                    reorder_point DECIMAL(15,4) DEFAULT 0.0,
                    reorder_quantity DECIMAL(15,4) DEFAULT 0.0,
                    
                    -- معلومات الجودة
                    quality_grade TEXT DEFAULT 'A',
                    expiry_date DATE,
                    manufacturing_date DATE,
                    batch_number TEXT,
                    serial_number TEXT,
                    
                    -- معلومات إضافية
                    weight DECIMAL(10,4),
                    dimensions TEXT, -- JSON: {"length": 0, "width": 0, "height": 0}
                    color TEXT,
                    size TEXT,
                    material TEXT,
                    brand TEXT,
                    model TEXT,
                    
                    -- معلومات المورد
                    supplier_id INTEGER,
                    supplier_code TEXT,
                    supplier_price DECIMAL(15,4),
                    
                    -- معلومات الصور والملفات
                    image_path TEXT,
                    images_json TEXT, -- JSON array of image paths
                    documents_json TEXT, -- JSON array of document paths
                    
                    -- معلومات التتبع
                    is_active BOOLEAN DEFAULT 1,
                    is_sellable BOOLEAN DEFAULT 1,
                    is_purchasable BOOLEAN DEFAULT 1,
                    is_trackable BOOLEAN DEFAULT 1,
                    
                    -- معلومات النظام
                    created_by INTEGER,
                    updated_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    -- فهارس خارجية
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (unit_id) REFERENCES units (id)
                )
            ''')
            
            # جدول خصائص الأصناف المخصصة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS item_attributes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    attribute_name TEXT NOT NULL,
                    attribute_value TEXT,
                    attribute_type TEXT DEFAULT 'text', -- text, number, date, boolean, json
                    is_searchable BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
                )
            ''')
            
            # جدول حركات المخزون
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory_movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    movement_type TEXT NOT NULL, -- in, out, adjustment, transfer
                    quantity DECIMAL(15,4) NOT NULL,
                    unit_cost DECIMAL(15,4),
                    total_cost DECIMAL(15,4),
                    reference_type TEXT, -- sale, purchase, adjustment, transfer
                    reference_id INTEGER,
                    notes TEXT,
                    warehouse_from TEXT,
                    warehouse_to TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            ''')
            
            # جدول أسعار الأصناف التاريخية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS item_price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    price_type TEXT NOT NULL, -- cost, selling, min_selling, max_selling
                    old_price DECIMAL(15,4),
                    new_price DECIMAL(15,4),
                    change_reason TEXT,
                    effective_date DATE,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            ''')
            
            # جدول تقييمات الأصناف
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS item_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    review_text TEXT,
                    reviewer_name TEXT,
                    reviewer_email TEXT,
                    is_verified BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
            ''')
            
            # إنشاء الفهارس لتحسين الأداء
            self.create_indexes(cursor)
            
            # إدراج البيانات الافتراضية
            self.insert_default_data(cursor)
            
            conn.commit()
            self.logger.info("تم تهيئة قاعدة البيانات بنجاح")
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"فشل في تهيئة قاعدة البيانات: {e}")
            raise
    
    def create_indexes(self, cursor):
        """إنشاء الفهارس لتحسين الأداء"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_items_code ON items (code)",
            "CREATE INDEX IF NOT EXISTS idx_items_name ON items (name)",
            "CREATE INDEX IF NOT EXISTS idx_items_barcode ON items (barcode)",
            "CREATE INDEX IF NOT EXISTS idx_items_category ON items (category_id)",
            "CREATE INDEX IF NOT EXISTS idx_items_active ON items (is_active)",
            "CREATE INDEX IF NOT EXISTS idx_items_created_at ON items (created_at)",
            "CREATE INDEX IF NOT EXISTS idx_inventory_movements_item ON inventory_movements (item_id)",
            "CREATE INDEX IF NOT EXISTS idx_inventory_movements_date ON inventory_movements (created_at)",
            "CREATE INDEX IF NOT EXISTS idx_item_attributes_item ON item_attributes (item_id)",
            "CREATE INDEX IF NOT EXISTS idx_item_attributes_name ON item_attributes (attribute_name)",
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except Exception as e:
                self.logger.warning(f"فشل في إنشاء فهرس: {e}")
    
    def insert_default_data(self, cursor):
        """إدراج البيانات الافتراضية"""
        try:
            # الوحدات الافتراضية
            default_units = [
                ('PIECE', 'قطعة', 'Piece', 'قطعة'),
                ('KG', 'كيلوجرام', 'Kilogram', 'كجم'),
                ('GRAM', 'جرام', 'Gram', 'جم'),
                ('LITER', 'لتر', 'Liter', 'لتر'),
                ('METER', 'متر', 'Meter', 'م'),
                ('BOX', 'صندوق', 'Box', 'صندوق'),
                ('PACK', 'عبوة', 'Pack', 'عبوة'),
            ]
            
            for code, name, name_en, symbol in default_units:
                cursor.execute('''
                    INSERT OR IGNORE INTO units (code, name, name_en, symbol)
                    VALUES (?, ?, ?, ?)
                ''', (code, name, name_en, symbol))
            
            # الفئات الافتراضية
            default_categories = [
                ('GENERAL', 'عام', 'General', 'فئة عامة للأصناف'),
                ('ELECTRONICS', 'إلكترونيات', 'Electronics', 'الأجهزة الإلكترونية'),
                ('CLOTHING', 'ملابس', 'Clothing', 'الملابس والأزياء'),
                ('FOOD', 'أغذية', 'Food', 'المواد الغذائية'),
                ('BOOKS', 'كتب', 'Books', 'الكتب والمطبوعات'),
                ('TOOLS', 'أدوات', 'Tools', 'الأدوات والمعدات'),
            ]
            
            for code, name, name_en, description in default_categories:
                cursor.execute('''
                    INSERT OR IGNORE INTO categories (code, name, name_en, description)
                    VALUES (?, ?, ?, ?)
                ''', (code, name, name_en, description))
            
        except Exception as e:
            self.logger.warning(f"فشل في إدراج البيانات الافتراضية: {e}")
    
    def close_connection(self):
        """إغلاق اتصال قاعدة البيانات"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("تم إغلاق اتصال قاعدة البيانات")

def main():
    """اختبار قاعدة البيانات"""
    print("🗄️ تهيئة قاعدة البيانات المتقدمة للأصناف...")
    
    try:
        db = AdvancedItemsDatabase()
        print("✅ تم إنشاء قاعدة البيانات بنجاح")
        
        # اختبار الاتصال
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # عرض الجداول المنشأة
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n📋 الجداول المنشأة:")
        for table in tables:
            print(f"  ✅ {table[0]}")
        
        db.close_connection()
        print("\n🎉 تم اختبار قاعدة البيانات بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")

if __name__ == "__main__":
    main()
