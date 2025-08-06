# -*- coding: utf-8 -*-
"""
نافذة إدخال الأصناف الاحترافية
Professional Item Entry Window
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.inventory_manager import InventoryManager
from core.item_code_generator import ItemCodeGenerator
from core.validator import Validator

class ItemEntryWindow(QMainWindow):
    """نافذة إدخال الأصناف الاحترافية"""
    
    def __init__(self, parent=None, item_id=None):
        super().__init__(parent)
        self.item_id = item_id  # للتعديل على صنف موجود
        self.current_theme = "light"  # الثيم الحالي
        self.image_path = None  # مسار الصورة المحملة

        # تهيئة مولد الرموز
        self.code_generator = ItemCodeGenerator()

        # تهيئة المدراء
        self.inventory_manager = InventoryManager()
        
        self.init_ui()
        self.load_styles()
        self.setup_connections()
        self.load_data()
        
        if self.item_id:
            self.load_item_data(self.item_id)
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("إدخال الأصناف - نظام إدارة المخزون")
        self.setGeometry(100, 100, 900, 700)
        self.setLayoutDirection(Qt.RightToLeft)
        
        # الويدجت الرئيسي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        # شريط العنوان
        self.create_header(self.main_layout)
        
        # المحتوى الرئيسي
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # الجانب الأيمن - النموذج
        self.create_form_section(content_layout)
        
        # الجانب الأيسر - الصورة والمعلومات
        self.create_info_section(content_layout)
        
        self.main_layout.addWidget(content_widget)
        
        # شريط الأزرار
        self.create_button_bar(self.main_layout)
        
        # شريط الحالة
        self.create_status_bar()
    
    def create_header(self, layout):
        """إنشاء شريط العنوان"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        
        # العنوان
        title_label = QLabel("إدخال صنف جديد" if not self.item_id else "تعديل الصنف")
        title_label.setObjectName("titleLabel")
        
        # زر تبديل الثيم
        theme_btn = QPushButton("🌙")
        theme_btn.setObjectName("themeButton")
        theme_btn.clicked.connect(self.toggle_theme)
        theme_btn.setFixedSize(40, 40)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(theme_btn)
        
        layout.addWidget(header_frame)
    
    def create_form_section(self, layout):
        """إنشاء قسم النموذج"""
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        font = QFont("Cairo", 12)

        # اسم الصنف
        self.item_name_edit = QLineEdit()
        self.item_name_edit.setObjectName("itemNameEdit")
        self.item_name_edit.setPlaceholderText("أدخل اسم الصنف...")
        self.item_name_edit.setFont(font)
        self.item_name_edit.textChanged.connect(self.validate_item_name)
        self.item_name_error = QLabel()
        self.item_name_error.setObjectName("errorLabel")
        self.item_name_error.hide()
        
        name_widget = QWidget()
        name_layout = QVBoxLayout(name_widget)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.addWidget(self.item_name_edit)
        name_layout.addWidget(self.item_name_error)
        
        form_layout.addRow("اسم الصنف *:", name_widget)
        
        # رمز الصنف
        self.item_code_edit = QLineEdit()
        self.item_code_edit.setObjectName("itemCodeEdit")
        self.item_code_edit.setPlaceholderText("سيتم توليده تلقائياً...")
        self.item_code_edit.setFont(font)
        self.item_code_edit.setReadOnly(True)
        self.item_code_edit.setText(generate_item_code())
        self.item_code_edit.textChanged.connect(self.validate_item_code)
        
        code_widget = QWidget()
        code_layout = QHBoxLayout(code_widget)
        code_layout.setContentsMargins(0, 0, 0, 0)
        code_layout.addWidget(self.item_code_edit)
        
        generate_code_btn = QPushButton("توليد")
        generate_code_btn.setObjectName("generateButton")
        generate_code_btn.clicked.connect(self.generate_item_code)
        code_layout.addWidget(generate_code_btn)
        
        self.item_code_error = QLabel()
        self.item_code_error.setObjectName("errorLabel")
        self.item_code_error.hide()
        
        code_container = QWidget()
        code_container_layout = QVBoxLayout(code_container)
        code_container_layout.setContentsMargins(0, 0, 0, 0)
        code_container_layout.addWidget(code_widget)
        code_container_layout.addWidget(self.item_code_error)
        
        form_layout.addRow("رمز الصنف *:", code_container)
        
        # التصنيف الرئيسي
        self.main_category_combo = QComboBox()
        self.main_category_combo.setObjectName("categoryCombo")
        self.main_category_combo.setFont(font)
        self.main_category_combo.currentTextChanged.connect(self.on_main_category_changed)
        form_layout.addRow("التصنيف الرئيسي *:", self.main_category_combo)
        
        # التصنيف الفرعي
        self.sub_category_combo = QComboBox()
        self.sub_category_combo.setObjectName("categoryCombo")
        self.sub_category_combo.setFont(font)
        self.sub_category_combo.currentTextChanged.connect(self.suggest_unit_and_price)
        form_layout.addRow("التصنيف الفرعي:", self.sub_category_combo)
        
        # وحدة القياس
        self.unit_combo = QComboBox()
        self.unit_combo.setObjectName("unitCombo")
        self.unit_combo.setFont(font)
        self.unit_combo.setEditable(True)
        form_layout.addRow("وحدة القياس *:", self.unit_combo)
        
        # الكمية الابتدائية
        self.initial_quantity_spin = QSpinBox()
        self.initial_quantity_spin.setObjectName("quantitySpinBox")
        self.initial_quantity_spin.setFont(font)
        self.initial_quantity_spin.setRange(0, 999999)
        self.initial_quantity_spin.setValue(0)
        form_layout.addRow("الكمية الابتدائية:", self.initial_quantity_spin)
        
        layout.addWidget(form_frame, 2)
    
    def create_info_section(self, layout):
        """إنشاء قسم المعلومات والصورة"""
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)
        
        # قسم الصورة
        image_group = QGroupBox("صورة الصنف")
        image_group.setObjectName("imageGroup")
        image_layout = QVBoxLayout(image_group)
        
        self.image_label = QLabel()
        self.image_label.setObjectName("imageLabel")
        self.image_label.setFixedSize(200, 200)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #ccc; border-radius: 10px;")
        self.image_label.setText("لا توجد صورة\n📷")
        
        upload_image_btn = QPushButton("تحميل صورة")
        upload_image_btn.setObjectName("uploadButton")
        upload_image_btn.clicked.connect(self.upload_image)
        
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(upload_image_btn)
        
        info_layout.addWidget(image_group)
        
        # قسم الأسعار
        self.create_price_section(info_layout)
        
        # قسم الوصف
        desc_group = QGroupBox("الوصف والملاحظات")
        desc_group.setObjectName("descGroup")
        desc_layout = QVBoxLayout(desc_group)
        
        self.description_edit = QTextEdit()
        self.description_edit.setObjectName("descriptionEdit")
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("أدخل وصف الصنف أو ملاحظات...")
        self.description_edit.setFont(font)
        
        desc_layout.addWidget(self.description_edit)
        info_layout.addWidget(desc_group)
        
        info_layout.addStretch()
        layout.addWidget(info_frame, 1)

    def create_price_section(self, layout):
        """إنشاء قسم الأسعار"""
        price_group = QGroupBox("الأسعار والتكلفة")
        price_group.setObjectName("priceGroup")
        price_layout = QFormLayout(price_group)

        font = QFont("Cairo", 12)

        # التكلفة
        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setObjectName("priceSpinBox")
        self.cost_spin.setFont(font)
        self.cost_spin.setRange(0.0, 999999.99)
        self.cost_spin.setDecimals(2)
        self.cost_spin.setSuffix(" ر.س")
        self.cost_spin.valueChanged.connect(self.calculate_profit_margin)
        price_layout.addRow("التكلفة:", self.cost_spin)

        # سعر البيع
        self.selling_price_spin = QDoubleSpinBox()
        self.selling_price_spin.setObjectName("priceSpinBox")
        self.selling_price_spin.setFont(font)
        self.selling_price_spin.setRange(0.0, 999999.99)
        self.selling_price_spin.setDecimals(2)
        self.selling_price_spin.setSuffix(" ر.س")
        self.selling_price_spin.valueChanged.connect(self.calculate_profit_margin)
        price_layout.addRow("سعر البيع *:", self.selling_price_spin)

        # نسبة الربح
        self.profit_margin_label = QLabel("0.00%")
        self.profit_margin_label.setObjectName("profitLabel")
        self.profit_margin_label.setFont(font)
        price_layout.addRow("نسبة الربح:", self.profit_margin_label)

        # الضريبة
        self.tax_combo = QComboBox()
        self.tax_combo.setObjectName("taxCombo")
        self.tax_combo.setFont(font)
        self.tax_combo.addItems(["معفى من الضريبة", "15% ضريبة القيمة المضافة", "5% ضريبة خاصة"])
        price_layout.addRow("الضريبة:", self.tax_combo)

        layout.addWidget(price_group)

    def create_button_bar(self, layout):
        """إنشاء شريط الأزرار"""
        button_frame = QFrame()
        button_frame.setObjectName("buttonFrame")
        button_layout = QHBoxLayout(button_frame)

        font = QFont("Cairo", 12)

        # زر الحفظ
        self.save_button = QPushButton("💾 حفظ")
        self.save_button.setObjectName("saveButton")
        self.save_button.setFont(font)
        self.save_button.clicked.connect(self.save_item)

        # زر الإلغاء
        cancel_btn = QPushButton("❌ إلغاء")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.setFont(font)
        cancel_btn.clicked.connect(self.close)

        # زر المسح
        clear_btn = QPushButton("🗑️ مسح")
        clear_btn.setObjectName("clearButton")
        clear_btn.setFont(font)
        clear_btn.clicked.connect(self.clear_form)

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(clear_btn)

        layout.addWidget(button_frame)

    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("جاهز لإدخال صنف جديد")

    def load_styles(self):
        """تحميل الأنماط"""
        style_path = project_root / "styles" / f"{self.current_theme}.qss"
        if style_path.exists():
            with open(style_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

    def setup_connections(self):
        """إعداد الاتصالات"""
        # تحديث رمز الصنف عند تغيير التصنيف
        self.main_category_combo.currentTextChanged.connect(self.auto_generate_code)
        self.sub_category_combo.currentTextChanged.connect(self.auto_generate_code)

    def load_data(self):
        """تحميل البيانات الأساسية"""
        # تحميل التصنيفات
        categories = self.inventory_manager.get_categories()
        self.main_category_combo.addItems(categories.get('main', []))

        # تحميل وحدات القياس
        units = self.inventory_manager.get_units()
        self.unit_combo.addItems(units)

    def on_main_category_changed(self, category):
        """عند تغيير التصنيف الرئيسي"""
        self.sub_category_combo.clear()
        if category:
            sub_categories = self.inventory_manager.get_sub_categories(category)
            self.sub_category_combo.addItems(sub_categories)

            # اقتراح الضريبة حسب التصنيف
            self.suggest_tax_by_category(category)

    def suggest_unit_and_price(self):
        """اقتراح الوحدة والسعر حسب التصنيف"""
        category = self.sub_category_combo.currentText()
        if category:
            # اقتراح الوحدة
            suggested_unit = self.inventory_manager.get_suggested_unit(category)
            if suggested_unit:
                index = self.unit_combo.findText(suggested_unit)
                if index >= 0:
                    self.unit_combo.setCurrentIndex(index)

            # اقتراح السعر
            suggested_price = self.inventory_manager.get_suggested_price(category)
            if suggested_price > 0:
                self.selling_price_spin.setValue(suggested_price)

    def suggest_tax_by_category(self, category):
        """اقتراح الضريبة حسب التصنيف"""
        tax_mapping = {
            "خدمات": 1,  # 15% ضريبة القيمة المضافة
            "منتجات مستوردة": 1,
            "منتجات محلية": 1,
            "أدوية": 0,  # معفى من الضريبة
            "مواد غذائية أساسية": 0
        }

        tax_index = tax_mapping.get(category, 1)
        self.tax_combo.setCurrentIndex(tax_index)

    def generate_item_code(self):
        """توليد رمز الصنف"""
        main_category = self.main_category_combo.currentText()
        sub_category = self.sub_category_combo.currentText()
        code = self.code_generator.generate_code(main_category, sub_category)
        self.item_code_edit.setText(code)

    def auto_generate_code(self):
        """توليد رمز الصنف تلقائياً"""
        if not self.item_code_edit.text() or self.item_code_edit.text().startswith("PRD-"):
            self.generate_item_code()

    def validate_item_name(self, name):
        """التحقق من اسم الصنف"""
        if len(name) < 2:
            self.show_field_error(self.item_name_error, "اسم الصنف يجب أن يكون أكثر من حرفين")
            return False

        if self.inventory_manager.item_name_exists(name, self.item_id):
            self.show_field_error(self.item_name_error, "اسم الصنف موجود مسبقاً")
            return False

        self.hide_field_error(self.item_name_error)
        return True

    def validate_item_code(self, code):
        """التحقق من رمز الصنف"""
        if len(code) < 3:
            self.show_field_error(self.item_code_error, "رمز الصنف قصير جداً")
            return False

        if self.inventory_manager.item_code_exists(code, self.item_id):
            self.show_field_error(self.item_code_error, "رمز الصنف موجود مسبقاً")
            return False

        self.hide_field_error(self.item_code_error)
        return True

    def show_field_error(self, error_label, message):
        """إظهار رسالة خطأ للحقل"""
        error_label.setText(message)
        error_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
        error_label.show()

    def hide_field_error(self, error_label):
        """إخفاء رسالة خطأ الحقل"""
        error_label.hide()

    def calculate_profit_margin(self):
        """حساب نسبة الربح"""
        cost = self.cost_spin.value()
        selling_price = self.selling_price_spin.value()

        if cost > 0:
            profit = selling_price - cost
            margin = (profit / cost) * 100
            self.profit_margin_label.setText(f"{margin:.2f}%")

            # تحذير إذا كان الفرق كبير
            if margin > 80:
                self.profit_margin_label.setStyleSheet("color: #e67e22; font-weight: bold;")
                self.status_bar.showMessage("تحذير: نسبة الربح عالية جداً!")
            elif margin < 10:
                self.profit_margin_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                self.status_bar.showMessage("تحذير: نسبة الربح منخفضة!")
            else:
                self.profit_margin_label.setStyleSheet("color: #27ae60; font-weight: bold;")
                self.status_bar.showMessage("نسبة ربح مناسبة")
        else:
            self.profit_margin_label.setText("0.00%")

    def upload_image(self):
        """تحميل صورة الصنف"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "اختر صورة الصنف", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.status_bar.showMessage("تم تحميل الصورة بنجاح")

    def toggle_theme(self):
        """تبديل الثيم"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.load_styles()

    def clear_form(self):
        """مسح النموذج"""
        reply = QMessageBox.question(
            self, "تأكيد المسح",
            "هل أنت متأكد من مسح جميع البيانات؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.item_name_edit.clear()
            self.item_code_edit.clear()
            self.main_category_combo.setCurrentIndex(0)
            self.sub_category_combo.clear()
            self.unit_combo.setCurrentIndex(0)
            self.initial_quantity_spin.setValue(0)
            self.cost_spin.setValue(0.0)
            self.selling_price_spin.setValue(0.0)
            self.tax_combo.setCurrentIndex(0)
            self.description_edit.clear()
            self.image_label.clear()
            self.image_label.setText("لا توجد صورة\n📷")
            self.image_path = None
            self.status_bar.showMessage("تم مسح النموذج")

    def validate_form(self):
        """التحقق من صحة النموذج"""
        errors = []

        if not self.item_name_edit.text().strip():
            errors.append("اسم الصنف مطلوب")

        if not self.item_code_edit.text().strip():
            errors.append("رمز الصنف مطلوب")

        if not self.main_category_combo.currentText():
            errors.append("التصنيف الرئيسي مطلوب")

        if not self.unit_combo.currentText():
            errors.append("وحدة القياس مطلوبة")

        if self.selling_price_spin.value() <= 0:
            errors.append("سعر البيع يجب أن يكون أكبر من صفر")

        return errors

    def save_item(self):
        """حفظ الصنف"""
        # التحقق من صحة البيانات
        errors = self.validate_form()
        if errors:
            QMessageBox.warning(self, "خطأ في البيانات", "\n".join(errors))
            return

        try:
            # إنشاء نموذج الصنف
            item_data = {
                'name': self.item_name_edit.text().strip(),
                'code': self.item_code_edit.text().strip(),
                'main_category': self.main_category_combo.currentText(),
                'sub_category': self.sub_category_combo.currentText(),
                'unit': self.unit_combo.currentText(),
                'initial_quantity': self.initial_quantity_spin.value(),
                'cost': self.cost_spin.value(),
                'selling_price': self.selling_price_spin.value(),
                'tax_type': self.tax_combo.currentText(),
                'description': self.description_edit.toPlainText(),
                'image_path': self.save_item_image() if self.image_path else None,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            # حفظ الصنف
            if self.item_id:
                success = self.inventory_manager.update_item(self.item_id, item_data)
                message = "تم تحديث الصنف بنجاح"
            else:
                success = self.inventory_manager.add_item(item_data)
                message = "تم حفظ الصنف بنجاح"

            if success:
                # تسجيل العملية
                self.log_operation(item_data)

                QMessageBox.information(self, "نجح الحفظ", message)
                self.close()
            else:
                QMessageBox.critical(self, "خطأ", "فشل في حفظ الصنف")

        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {str(e)}")

    def save_item_image(self):
        """حفظ صورة الصنف"""
        if not self.image_path:
            return None

        # إنشاء مجلد الصور إذا لم يكن موجود
        media_dir = project_root / "media" / "items"
        media_dir.mkdir(parents=True, exist_ok=True)

        # نسخ الصورة بالرمز كاسم
        item_code = self.item_code_edit.text().strip()
        file_extension = Path(self.image_path).suffix
        new_image_path = media_dir / f"{item_code}{file_extension}"

        import shutil
        shutil.copy2(self.image_path, new_image_path)

        return str(new_image_path)

    def log_operation(self, item_data):
        """تسجيل العملية في السجل"""
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "item_log.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': 'update' if self.item_id else 'create',
            'item_code': item_data['code'],
            'item_name': item_data['name'],
            'user': os.getenv('USERNAME', 'unknown')
        }

        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)

        logs.append(log_entry)

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def load_item_data(self, item_id):
        """تحميل بيانات صنف للتعديل"""
        item_data = self.inventory_manager.get_item(item_id)
        if item_data:
            self.item_name_edit.setText(item_data.get('name', ''))
            self.item_code_edit.setText(item_data.get('code', ''))

            # تحديد التصنيفات
            main_cat = item_data.get('main_category', '')
            if main_cat:
                index = self.main_category_combo.findText(main_cat)
                if index >= 0:
                    self.main_category_combo.setCurrentIndex(index)

            sub_cat = item_data.get('sub_category', '')
            if sub_cat:
                index = self.sub_category_combo.findText(sub_cat)
                if index >= 0:
                    self.sub_category_combo.setCurrentIndex(index)

            # باقي البيانات
            unit = item_data.get('unit', '')
            if unit:
                index = self.unit_combo.findText(unit)
                if index >= 0:
                    self.unit_combo.setCurrentIndex(index)

            self.initial_quantity_spin.setValue(item_data.get('initial_quantity', 0))
            self.cost_spin.setValue(item_data.get('cost', 0.0))
            self.selling_price_spin.setValue(item_data.get('selling_price', 0.0))

            tax_type = item_data.get('tax_type', '')
            if tax_type:
                index = self.tax_combo.findText(tax_type)
                if index >= 0:
                    self.tax_combo.setCurrentIndex(index)

            self.description_edit.setPlainText(item_data.get('description', ''))

            # تحميل الصورة
            image_path = item_data.get('image_path')
            if image_path and os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_path = image_path


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # تطبيق الخط العربي
    font = QFont("Cairo", 10)
    app.setFont(font)

    window = ItemEntryWindow()
    window.show()

    sys.exit(app.exec_())
