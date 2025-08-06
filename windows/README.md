# نافذة إدخال الأصناف الاحترافية
## Professional Item Entry Window

### 📋 الوصف
نافذة إدخال الأصناف هي واجهة احترافية مصممة خصيصاً للبرامج المحاسبية العربية. تتميز بالتصميم الحديث والدعم الكامل للغة العربية من اليمين إلى اليسار (RTL).

### ✨ المميزات الرئيسية

#### 🎨 التصميم والواجهة
- **تصميم حديث ومتجاوب**: واجهة عصرية مع تأثيرات بصرية جذابة
- **دعم الثيمات**: نمط فاتح ونمط داكن قابل للتبديل
- **دعم RTL كامل**: تخطيط من اليمين إلى اليسار للنصوص العربية
- **خطوط عربية**: دعم خط Cairo وخطوط عربية أخرى
- **تصميم متجاوب**: يتكيف مع أحجام الشاشات المختلفة

#### 📝 إدخال البيانات
- **معلومات أساسية**:
  - اسم الصنف (مطلوب)
  - رمز الصنف (توليد تلقائي أو يدوي)
  - التصنيف الرئيسي والفرعي
  - وحدة القياس
  - الكمية الابتدائية
  - الوصف التفصيلي

- **معلومات الأسعار**:
  - التكلفة
  - سعر البيع (مطلوب)
  - حساب نسبة الربح تلقائياً
  - نوع الضريبة (معفى، 15%، 5%)

#### 🖼️ إدارة الصور
- **تحميل الصور**: دعم PNG, JPG, JPEG, BMP, GIF
- **معاينة فورية**: عرض الصورة بعد التحميل
- **تحسين الحجم**: تغيير حجم الصور تلقائياً
- **حفظ منظم**: تخزين الصور بأسماء منظمة

#### 🔍 التحقق والتصديق
- **تحقق فوري**: التحقق من صحة البيانات أثناء الكتابة
- **رسائل خطأ واضحة**: إرشادات مفصلة للأخطاء
- **تحقق من التكرار**: منع تكرار الأسماء والرموز
- **تحقق من المنطق**: التأكد من منطقية الأسعار والنسب

#### 🤖 الذكاء الاصطناعي
- **توليد رموز ذكي**: رموز منظمة حسب التصنيف والتاريخ
- **اقتراحات ذكية**: اقتراح الوحدات والأسعار حسب التصنيف
- **تحليل الربحية**: تحليل نسب الربح وإعطاء تحذيرات
- **تصنيف الضرائب**: اقتراح نوع الضريبة حسب التصنيف

### 🏗️ البنية التقنية

#### 📁 الملفات الأساسية
```
windows/
├── item_entry_window.py      # النافذة الرئيسية
└── README.md                 # هذا الملف

core/
├── inventory_manager.py      # مدير المخزون
├── item_code_generator.py    # مولد رموز الأصناف
└── validation_engine.py      # محرك التحقق

models/
└── item_model.py            # نموذج بيانات الصنف

styles/
├── light.qss               # نمط فاتح
└── dark.qss                # نمط داكن
```

#### 🔧 المتطلبات التقنية
- **Python 3.7+**
- **PyQt5**: للواجهة الرسومية
- **SQLite**: لقاعدة البيانات المحلية
- **PIL/Pillow**: لمعالجة الصور
- **pathlib**: لإدارة المسارات

### 🚀 طريقة الاستخدام

#### 1️⃣ التشغيل المباشر
```python
python test_item_entry.py
```

#### 2️⃣ الاستيراد في التطبيق
```python
from windows.item_entry_window import ItemEntryWindow

# إنشاء نافذة جديدة
window = ItemEntryWindow()
window.show()

# تعديل صنف موجود
window = ItemEntryWindow(item_id=123)
window.show()
```

#### 3️⃣ التكامل مع التطبيق الرئيسي
```python
def open_item_entry(self):
    """فتح نافذة إدخال الأصناف"""
    self.item_window = ItemEntryWindow(self)
    self.item_window.show()
```

### 📊 قاعدة البيانات

#### 🗃️ جدول الأصناف (items)
```sql
CREATE TABLE items (
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
);
```

#### 🏷️ جدول التصنيفات (categories)
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER,
    suggested_unit TEXT,
    suggested_tax TEXT,
    FOREIGN KEY (parent_id) REFERENCES categories (id)
);
```

### 🎯 الميزات المتقدمة

#### 📈 تحليل الربحية
- حساب نسبة الربح تلقائياً
- تحذيرات للنسب غير المنطقية
- اقتراحات لتحسين الأسعار
- مؤشرات بصرية للحالة

#### 🔐 الأمان والتحقق
- تشفير البيانات الحساسة
- تسجيل جميع العمليات
- نسخ احتياطية تلقائية
- تحقق من صلاحيات المستخدم

#### 📱 سهولة الاستخدام
- اختصارات لوحة المفاتيح
- تنقل بالـ Tab بين الحقول
- حفظ تلقائي للمسودات
- استرجاع البيانات المحذوفة

### 🛠️ التخصيص والإعدادات

#### 🎨 تخصيص المظهر
```python
# تغيير الثيم
window.current_theme = "dark"
window.load_styles()

# تخصيص الألوان
window.setStyleSheet("QMainWindow { background-color: #custom; }")
```

#### ⚙️ إعدادات التحقق
```python
# إضافة قواعد تحقق مخصصة
validator = ValidationEngine()
validator.add_custom_validation_rule("item_name", "max_length", 50)
```

#### 🏷️ إضافة تصنيفات جديدة
```python
# إضافة تصنيف جديد
inventory_manager = InventoryManager()
inventory_manager.add_category("تصنيف جديد", parent_id=1)
```

### 🐛 استكشاف الأخطاء

#### ❌ مشاكل شائعة وحلولها

**1. خطأ في استيراد PyQt5**
```bash
pip install PyQt5
```

**2. خطأ في الخطوط العربية**
```python
# تثبيت خط Cairo
font = QFont("Arial", 10)  # كبديل
```

**3. مشاكل قاعدة البيانات**
```python
# إعادة إنشاء قاعدة البيانات
inventory_manager.init_database()
```

### 📞 الدعم والمساعدة

#### 🆘 طلب المساعدة
- تحقق من ملفات السجل في مجلد `logs/`
- راجع رسائل الخطأ في وحدة التحكم
- تأكد من تثبيت جميع المتطلبات

#### 🔄 التحديثات المستقبلية
- دعم المزيد من قواعد البيانات
- تكامل مع أنظمة ERP
- تصدير واستيراد البيانات
- تقارير تحليلية متقدمة

---

**تم تطوير هذه النافذة بواسطة فريق التطوير لتكون جزءاً من نظام محاسبي متكامل وحديث.**
