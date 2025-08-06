-- إنشاء جداول قاعدة البيانات للنظام المحاسبي المتطور
-- Advanced Accounting System Database Tables

-- جدول تصنيفات المنتجات (هرمي)
CREATE TABLE IF NOT EXISTS item_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar TEXT NOT NULL,
    name_en TEXT,
    parent_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES item_categories(id) ON DELETE SET NULL
);

-- فهرس للبحث السريع في التصنيفات
CREATE INDEX IF NOT EXISTS idx_categories_parent ON item_categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_categories_name_ar ON item_categories(name_ar);

-- جدول وحدات القياس
CREATE TABLE IF NOT EXISTS units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar TEXT NOT NULL,
    name_en TEXT,
    symbol TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- فهرس للبحث السريع في الوحدات
CREATE INDEX IF NOT EXISTS idx_units_name_ar ON units(name_ar);
CREATE INDEX IF NOT EXISTS idx_units_symbol ON units(symbol);

-- جدول المخازن
CREATE TABLE IF NOT EXISTS warehouses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    city TEXT,
    phone TEXT,
    manager_name TEXT,
    manager_phone TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- فهرس للبحث السريع في المخازن
CREATE INDEX IF NOT EXISTS idx_warehouses_code ON warehouses(warehouse_code);
CREATE INDEX IF NOT EXISTS idx_warehouses_active ON warehouses(is_active);

-- جدول الأصناف المحدث والمتطور
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_code TEXT UNIQUE NOT NULL,
    name_ar TEXT NOT NULL,
    name_en TEXT,
    description TEXT,
    category_id INTEGER,
    unit_id INTEGER,
    secondary_unit_id INTEGER,
    conversion_factor REAL DEFAULT 1.0,
    default_warehouse_id INTEGER,
    cost_price REAL DEFAULT 0.0,
    sale_price REAL DEFAULT 0.0,
    wholesale_price REAL DEFAULT 0.0,
    last_purchase_price REAL DEFAULT 0.0,
    vat_rate REAL DEFAULT 0.0,
    min_stock REAL DEFAULT 0.0,
    max_stock REAL DEFAULT 0.0,
    reorder_level REAL DEFAULT 0.0,
    serial_tracking BOOLEAN DEFAULT 0,
    batch_tracking BOOLEAN DEFAULT 0,
    expiry_date_required BOOLEAN DEFAULT 0,
    is_service BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    image_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES item_categories(id) ON DELETE SET NULL,
    FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE SET NULL,
    FOREIGN KEY (secondary_unit_id) REFERENCES units(id) ON DELETE SET NULL,
    FOREIGN KEY (default_warehouse_id) REFERENCES warehouses(id) ON DELETE SET NULL
);

-- فهارس للبحث السريع في الأصناف
CREATE INDEX IF NOT EXISTS idx_items_code ON items(item_code);
CREATE INDEX IF NOT EXISTS idx_items_name_ar ON items(name_ar);
CREATE INDEX IF NOT EXISTS idx_items_category ON items(category_id);
CREATE INDEX IF NOT EXISTS idx_items_active ON items(is_active);
CREATE INDEX IF NOT EXISTS idx_items_warehouse ON items(default_warehouse_id);

-- جدول حركات المخزون المحدث
CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL, -- 'in', 'out', 'transfer', 'adjust'
    quantity REAL NOT NULL,
    cost_price REAL DEFAULT 0.0,
    reference_no TEXT,
    date DATE DEFAULT CURRENT_DATE,
    notes TEXT,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE CASCADE
);

-- فهارس لحركات المخزون
CREATE INDEX IF NOT EXISTS idx_movements_item ON stock_movements(item_id);
CREATE INDEX IF NOT EXISTS idx_movements_warehouse ON stock_movements(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_movements_type ON stock_movements(movement_type);
CREATE INDEX IF NOT EXISTS idx_movements_date ON stock_movements(date);
CREATE INDEX IF NOT EXISTS idx_movements_created ON stock_movements(created_at);

-- جدول الأرصدة اللحظية (cache)
CREATE TABLE IF NOT EXISTS stock_balance (
    item_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    quantity REAL DEFAULT 0.0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (item_id, warehouse_id),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE CASCADE
);

-- فهارس للأرصدة اللحظية
CREATE INDEX IF NOT EXISTS idx_balance_item ON stock_balance(item_id);
CREATE INDEX IF NOT EXISTS idx_balance_warehouse ON stock_balance(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_balance_quantity ON stock_balance(quantity);
CREATE INDEX IF NOT EXISTS idx_balance_updated ON stock_balance(last_updated);

-- جدول الأرقام التسلسلية (للأصناف التي تتطلب تتبع)
CREATE TABLE IF NOT EXISTS item_serials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    serial_number TEXT NOT NULL,
    status TEXT DEFAULT 'AVAILABLE', -- 'AVAILABLE', 'SOLD', 'RESERVED', 'DAMAGED'
    purchase_date DATE,
    sale_date DATE,
    expiry_date DATE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE CASCADE,
    UNIQUE(item_id, serial_number)
);

-- فهارس للأرقام التسلسلية
CREATE INDEX IF NOT EXISTS idx_serials_item ON item_serials(item_id);
CREATE INDEX IF NOT EXISTS idx_serials_number ON item_serials(serial_number);
CREATE INDEX IF NOT EXISTS idx_serials_status ON item_serials(status);

-- جدول الدفعات (للأصناف التي تتطلب تتبع دفعات)
CREATE TABLE IF NOT EXISTS item_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    batch_number TEXT NOT NULL,
    quantity REAL NOT NULL,
    remaining_quantity REAL NOT NULL,
    production_date DATE,
    expiry_date DATE,
    supplier_id INTEGER,
    purchase_price REAL,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE CASCADE,
    UNIQUE(item_id, batch_number)
);

-- فهارس للدفعات
CREATE INDEX IF NOT EXISTS idx_batches_item ON item_batches(item_id);
CREATE INDEX IF NOT EXISTS idx_batches_number ON item_batches(batch_number);
CREATE INDEX IF NOT EXISTS idx_batches_expiry ON item_batches(expiry_date);

-- جدول سجل تغيرات الأسعار
CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    price_type TEXT NOT NULL, -- 'COST', 'SALE', 'WHOLESALE'
    old_price REAL,
    new_price REAL NOT NULL,
    change_reason TEXT,
    changed_by INTEGER,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- فهارس لسجل الأسعار
CREATE INDEX IF NOT EXISTS idx_price_history_item ON price_history(item_id);
CREATE INDEX IF NOT EXISTS idx_price_history_date ON price_history(changed_at);

-- جدول المرفقات (ملفات إضافية للأصناف)
CREATE TABLE IF NOT EXISTS item_attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT, -- 'IMAGE', 'PDF', 'DOCUMENT'
    file_size INTEGER,
    description TEXT,
    uploaded_by INTEGER,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- فهارس للمرفقات
CREATE INDEX IF NOT EXISTS idx_attachments_item ON item_attachments(item_id);
CREATE INDEX IF NOT EXISTS idx_attachments_type ON item_attachments(file_type);

-- إدراج بيانات أولية للتصنيفات
INSERT OR IGNORE INTO item_categories (id, name_ar, name_en, parent_id) VALUES
(1, 'إلكترونيات', 'Electronics', NULL),
(2, 'أجهزة كمبيوتر', 'Computers', 1),
(3, 'لابتوب', 'Laptops', 2),
(4, 'أجهزة مكتبية', 'Desktop', 2),
(5, 'هواتف ذكية', 'Smartphones', 1),
(6, 'ملابس', 'Clothing', NULL),
(7, 'ملابس رجالية', 'Men''s Clothing', 6),
(8, 'ملابس نسائية', 'Women''s Clothing', 6),
(9, 'أحذية', 'Shoes', 6),
(10, 'طعام ومشروبات', 'Food & Beverages', NULL),
(11, 'مشروبات ساخنة', 'Hot Beverages', 10),
(12, 'مشروبات باردة', 'Cold Beverages', 10),
(13, 'خدمات', 'Services', NULL);

-- إدراج بيانات أولية لوحدات القياس
INSERT OR IGNORE INTO units (id, name_ar, name_en, symbol) VALUES
(1, 'قطعة', 'Piece', 'قطعة'),
(2, 'كيلوجرام', 'Kilogram', 'كجم'),
(3, 'جرام', 'Gram', 'جم'),
(4, 'لتر', 'Liter', 'لتر'),
(5, 'متر', 'Meter', 'م'),
(6, 'سنتيمتر', 'Centimeter', 'سم'),
(7, 'علبة', 'Box', 'علبة'),
(8, 'كرتونة', 'Carton', 'كرتون'),
(9, 'دزينة', 'Dozen', 'دزينة'),
(10, 'طن', 'Ton', 'طن'),
(11, 'باوند', 'Pound', 'باوند'),
(12, 'ساعة', 'Hour', 'ساعة');

-- إدراج بيانات أولية للمخازن
INSERT OR IGNORE INTO warehouses (id, warehouse_code, name, description, is_active) VALUES
(1, 'WH001', 'المخزن الرئيسي', 'المخزن الرئيسي للشركة', 1),
(2, 'WH002', 'مخزن الفرع الأول', 'مخزن فرع المدينة', 1),
(3, 'WH003', 'مخزن الفرع الثاني', 'مخزن فرع الضواحي', 1),
(4, 'WH004', 'مخزن المواد الخام', 'مخزن خاص بالمواد الخام', 1),
(5, 'WH005', 'مخزن المنتجات الجاهزة', 'مخزن المنتجات النهائية', 1);

-- إدراج بيانات أولية للأصناف
INSERT OR IGNORE INTO items (id, item_code, name_ar, name_en, category_id, unit_id, cost_price, sale_price, wholesale_price, vat_rate, min_stock, max_stock, reorder_level, is_active) VALUES
(1, 'ITM001', 'لابتوب ديل', 'Dell Laptop', 3, 1, 2500.00, 3000.00, 2800.00, 15.0, 5, 50, 10, 1),
(2, 'ITM002', 'قميص قطني', 'Cotton Shirt', 7, 1, 50.00, 75.00, 65.00, 15.0, 20, 200, 50, 1),
(3, 'ITM003', 'قهوة عربية', 'Arabic Coffee', 11, 2, 80.00, 120.00, 100.00, 0.0, 50, 500, 100, 1),
(4, 'ITM004', 'دفتر ملاحظات', 'Notebook', 4, 1, 15.00, 25.00, 20.00, 15.0, 100, 1000, 200, 1),
(5, 'ITM005', 'زيت محرك 5W30', 'Engine Oil 5W30', 1, 4, 22.50, 35.00, 30.00, 15.0, 50, 500, 100, 1);

-- إدراج بيانات أولية لحركات المخزون
INSERT OR IGNORE INTO stock_movements (id, item_id, warehouse_id, movement_type, quantity, cost_price, reference_no, date, notes) VALUES
(1, 1, 1, 'in', 20, 2500.00, 'PO-001', '2024-01-15', 'شراء أولي - لابتوب ديل'),
(2, 2, 2, 'in', 100, 50.00, 'PO-002', '2024-01-16', 'شراء أولي - قمصان قطنية'),
(3, 3, 1, 'in', 200, 80.00, 'PO-003', '2024-01-17', 'شراء أولي - قهوة عربية'),
(4, 4, 1, 'in', 500, 15.00, 'PO-004', '2024-01-18', 'شراء أولي - دفاتر ملاحظات'),
(5, 5, 4, 'in', 300, 22.50, 'PO-005', '2024-01-19', 'شراء أولي - زيت محرك'),
(6, 1, 1, 'out', 3, 2500.00, 'SO-001', '2024-01-20', 'بيع للعميل أحمد محمد'),
(7, 2, 2, 'out', 15, 50.00, 'SO-002', '2024-01-20', 'بيع للعميل فاطمة علي'),
(8, 3, 1, 'out', 25, 80.00, 'SO-003', '2024-01-21', 'بيع بالجملة'),
(9, 1, 1, 'transfer', 5, 2500.00, 'TR-001', '2024-01-22', 'تحويل للفرع الأول'),
(10, 1, 2, 'in', 5, 2500.00, 'TR-001', '2024-01-22', 'استلام من المخزن الرئيسي'),
(11, 4, 1, 'adjust', 10, 15.00, 'ADJ-001', '2024-01-23', 'تسوية جرد - زيادة'),
(12, 5, 4, 'out', 50, 22.50, 'SO-004', '2024-01-24', 'بيع لورشة السيارات');

-- إدراج بيانات أولية للأرصدة اللحظية
INSERT OR IGNORE INTO stock_balance (item_id, warehouse_id, quantity, last_updated) VALUES
(1, 1, 12, '2024-01-24 10:00:00'),  -- لابتوب ديل - المخزن الرئيسي
(1, 2, 5, '2024-01-22 14:30:00'),   -- لابتوب ديل - الفرع الأول
(2, 2, 85, '2024-01-20 16:45:00'),  -- قميص قطني - الفرع الأول
(3, 1, 175, '2024-01-21 11:20:00'), -- قهوة عربية - المخزن الرئيسي
(4, 1, 510, '2024-01-23 09:15:00'), -- دفتر ملاحظات - المخزن الرئيسي
(5, 4, 250, '2024-01-24 13:00:00'); -- زيت محرك - مخزن المواد الخام
