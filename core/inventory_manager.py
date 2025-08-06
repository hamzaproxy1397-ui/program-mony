# -*- coding: utf-8 -*-
"""
مدير المخزون
Inventory Manager
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

class InventoryManager:
    """مدير المخزون الذكي"""
    
    def __init__(self, db_path: str = None):
        self.project_root = Path(__file__).parent.parent
        self.db_path = db_path or str(self.project_root / "database" / "inventory.db")
        self.settings_path = self.project_root / "settings.json"
        
        self.init_database()
        self.load_settings()
    
    def init_database(self):
        """تهيئة قاعدة البيانات"""
        # إنشاء مجلد قاعدة البيانات
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الأصناف
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                code TEXT NOT NULL UNIQUE,
                main_category TEXT NOT NULL,
                sub_category TEXT,
                unit TEXT NOT NULL,
                initial_quantity INTEGER DEFAULT 0,
                current_quantity INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                selling_price REAL NOT NULL,
                tax_type TEXT,
                description TEXT,
                image_path TEXT,
                created_at TEXT,
                updated_at TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # جدول التصنيفات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                parent_id INTEGER,
                suggested_unit TEXT,
                suggested_tax TEXT,
                FOREIGN KEY (parent_id) REFERENCES categories (id)
            )
        ''')
        
        # جدول وحدات القياس
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS units (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                symbol TEXT,
                type TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # إدراج البيانات الأساسية
        self.insert_default_data()
    
    def insert_default_data(self):
        """إدراج البيانات الافتراضية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # التصنيفات الرئيسية
        main_categories = [
            ("إلكترونيات", None, "قطعة", "15% ضريبة القيمة المضافة"),
            ("ملابس", None, "قطعة", "15% ضريبة القيمة المضافة"),
            ("مواد غذائية", None, "كيلو", "معفى من الضريبة"),
            ("أدوية", None, "علبة", "معفى من الضريبة"),
            ("خدمات", None, "ساعة", "15% ضريبة القيمة المضافة"),
            ("مواد بناء", None, "متر", "15% ضريبة القيمة المضافة"),
        ]
        
        for category in main_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, parent_id, suggested_unit, suggested_tax)
                VALUES (?, ?, ?, ?)
            ''', category)
        
        # التصنيفات الفرعية
        sub_categories = [
            ("هواتف ذكية", 1), ("حاسوب", 1), ("أجهزة منزلية", 1),
            ("ملابس رجالية", 2), ("ملابس نسائية", 2), ("ملابس أطفال", 2),
            ("خضروات", 3), ("فواكه", 3), ("لحوم", 3),
            ("أدوية عامة", 4), ("مكملات غذائية", 4),
            ("استشارات", 5), ("صيانة", 5),
            ("أسمنت", 6), ("حديد", 6), ("دهانات", 6)
        ]
        
        for sub_cat, parent_id in sub_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, parent_id)
                VALUES (?, ?)
            ''', (sub_cat, parent_id))
        
        # وحدات القياس
        units = [
            ("قطعة", "قطعة", "عدد"),
            ("كيلو", "كجم", "وزن"),
            ("جرام", "جم", "وزن"),
            ("لتر", "لتر", "حجم"),
            ("متر", "م", "طول"),
            ("سنتيمتر", "سم", "طول"),
            ("علبة", "علبة", "تعبئة"),
            ("كرتون", "كرتون", "تعبئة"),
            ("ساعة", "ساعة", "وقت"),
            ("يوم", "يوم", "وقت")
        ]
        
        for unit in units:
            cursor.execute('''
                INSERT OR IGNORE INTO units (name, symbol, type)
                VALUES (?, ?, ?)
            ''', unit)
        
        conn.commit()
        conn.close()
    
    def load_settings(self):
        """تحميل الإعدادات"""
        if self.settings_path.exists():
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                "default_tax": "15% ضريبة القيمة المضافة",
                "default_profit_margin": 25.0,
                "auto_generate_codes": True,
                "code_prefix": "PRD"
            }
            self.save_settings()
    
    def save_settings(self):
        """حفظ الإعدادات"""
        with open(self.settings_path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)
    
    def get_categories(self) -> Dict[str, List[str]]:
        """الحصول على التصنيفات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # التصنيفات الرئيسية
        cursor.execute('SELECT name FROM categories WHERE parent_id IS NULL ORDER BY name')
        main_categories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return {"main": main_categories}
    
    def get_sub_categories(self, main_category: str) -> List[str]:
        """الحصول على التصنيفات الفرعية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c2.name FROM categories c1
            JOIN categories c2 ON c1.id = c2.parent_id
            WHERE c1.name = ?
            ORDER BY c2.name
        ''', (main_category,))
        
        sub_categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sub_categories
    
    def get_units(self) -> List[str]:
        """الحصول على وحدات القياس"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name FROM units ORDER BY name')
        units = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return units
    
    def get_suggested_unit(self, category: str) -> Optional[str]:
        """اقتراح وحدة القياس حسب التصنيف"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT suggested_unit FROM categories 
            WHERE name = ? AND suggested_unit IS NOT NULL
        ''', (category,))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_suggested_price(self, category: str) -> float:
        """اقتراح السعر حسب التصنيف"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # حساب متوسط الأسعار في نفس التصنيف
        cursor.execute('''
            SELECT AVG(selling_price) FROM items 
            WHERE sub_category = ? AND selling_price > 0
        ''', (category,))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result and result[0] else 0.0
    
    def item_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """التحقق من وجود اسم الصنف"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if exclude_id:
            cursor.execute('SELECT id FROM items WHERE name = ? AND id != ?', (name, exclude_id))
        else:
            cursor.execute('SELECT id FROM items WHERE name = ?', (name,))
        
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def item_code_exists(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """التحقق من وجود رمز الصنف"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if exclude_id:
            cursor.execute('SELECT id FROM items WHERE code = ? AND id != ?', (code, exclude_id))
        else:
            cursor.execute('SELECT id FROM items WHERE code = ?', (code,))
        
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def add_item(self, item_data: Dict[str, Any]) -> bool:
        """إضافة صنف جديد"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # تحديد الكمية الحالية = الكمية الابتدائية
            item_data['current_quantity'] = item_data.get('initial_quantity', 0)
            
            cursor.execute('''
                INSERT INTO items (
                    name, code, main_category, sub_category, unit,
                    initial_quantity, current_quantity, cost, selling_price,
                    tax_type, description, image_path, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item_data['name'], item_data['code'], item_data['main_category'],
                item_data['sub_category'], item_data['unit'], item_data['initial_quantity'],
                item_data['current_quantity'], item_data['cost'], item_data['selling_price'],
                item_data['tax_type'], item_data['description'], item_data['image_path'],
                item_data['created_at'], item_data['updated_at']
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"خطأ في إضافة الصنف: {e}")
            return False
    
    def update_item(self, item_id: int, item_data: Dict[str, Any]) -> bool:
        """تحديث صنف موجود"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE items SET
                    name = ?, code = ?, main_category = ?, sub_category = ?, unit = ?,
                    initial_quantity = ?, cost = ?, selling_price = ?, tax_type = ?,
                    description = ?, image_path = ?, updated_at = ?
                WHERE id = ?
            ''', (
                item_data['name'], item_data['code'], item_data['main_category'],
                item_data['sub_category'], item_data['unit'], item_data['initial_quantity'],
                item_data['cost'], item_data['selling_price'], item_data['tax_type'],
                item_data['description'], item_data['image_path'], item_data['updated_at'],
                item_id
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"خطأ في تحديث الصنف: {e}")
            return False
    
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات صنف"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            item_data = dict(zip(columns, row))
            conn.close()
            return item_data
        
        conn.close()
        return None
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """الحصول على جميع الأصناف"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM items WHERE is_active = 1 ORDER BY name')
        rows = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        items = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return items
