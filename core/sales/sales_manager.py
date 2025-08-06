# -*- coding: utf-8 -*-
"""
مدير المبيعات
Sales Manager
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, date
from enum import Enum
import uuid

class InvoiceStatus(Enum):
    """حالات الفاتورة"""
    DRAFT = "draft"  # مسودة
    CONFIRMED = "confirmed"  # مؤكدة
    PAID = "paid"  # مدفوعة
    PARTIALLY_PAID = "partially_paid"  # مدفوعة جزئياً
    CANCELLED = "cancelled"  # ملغاة

class PaymentMethod(Enum):
    """طرق الدفع"""
    CASH = "cash"  # نقداً
    BANK_TRANSFER = "bank_transfer"  # تحويل بنكي
    CREDIT_CARD = "credit_card"  # بطاقة ائتمان
    CHECK = "check"  # شيك
    CREDIT = "credit"  # آجل

class SalesInvoice:
    """فاتورة مبيعات"""
    
    def __init__(self, invoice_id: str = None):
        self.invoice_id = invoice_id or str(uuid.uuid4())
        self.invoice_number = None  # رقم الفاتورة التسلسلي
        self.date = date.today()
        self.due_date = None
        self.customer_id = None
        self.customer_name = ""
        self.customer_tax_number = ""
        self.status = InvoiceStatus.DRAFT
        self.payment_method = PaymentMethod.CASH
        self.items = []  # بنود الفاتورة
        self.subtotal = Decimal('0')
        self.tax_amount = Decimal('0')
        self.discount_amount = Decimal('0')
        self.total_amount = Decimal('0')
        self.paid_amount = Decimal('0')
        self.remaining_amount = Decimal('0')
        self.tax_rate = Decimal('15')  # ضريبة القيمة المضافة 15%
        self.notes = ""
        self.created_by = None
        self.created_date = datetime.now()
        self.confirmed_date = None
    
    def add_item(self, product_id: int, product_name: str, quantity: int,
                unit_price: Decimal, discount_percent: Decimal = Decimal('0')) -> bool:
        """إضافة منتج للفاتورة"""
        
        if quantity <= 0 or unit_price < 0:
            return False
        
        # حساب المبالغ
        line_total = unit_price * quantity
        discount_amount = line_total * (discount_percent / 100)
        net_amount = line_total - discount_amount
        
        item = {
            'item_id': str(uuid.uuid4()),
            'product_id': product_id,
            'product_name': product_name,
            'quantity': quantity,
            'unit_price': unit_price,
            'line_total': line_total,
            'discount_percent': discount_percent,
            'discount_amount': discount_amount,
            'net_amount': net_amount
        }
        
        self.items.append(item)
        self._calculate_totals()
        return True
    
    def remove_item(self, item_id: str) -> bool:
        """حذف منتج من الفاتورة"""
        for i, item in enumerate(self.items):
            if item['item_id'] == item_id:
                del self.items[i]
                self._calculate_totals()
                return True
        return False
    
    def update_item_quantity(self, item_id: str, new_quantity: int) -> bool:
        """تحديث كمية منتج"""
        for item in self.items:
            if item['item_id'] == item_id:
                if new_quantity <= 0:
                    return False
                
                item['quantity'] = new_quantity
                item['line_total'] = item['unit_price'] * new_quantity
                item['discount_amount'] = item['line_total'] * (item['discount_percent'] / 100)
                item['net_amount'] = item['line_total'] - item['discount_amount']
                
                self._calculate_totals()
                return True
        return False
    
    def _calculate_totals(self):
        """حساب المجاميع"""
        self.subtotal = sum(item['net_amount'] for item in self.items)
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.remaining_amount = self.total_amount - self.paid_amount
    
    def apply_discount(self, discount_amount: Decimal):
        """تطبيق خصم على الفاتورة"""
        self.discount_amount = discount_amount
        self._calculate_totals()
    
    def add_payment(self, amount: Decimal, payment_method: PaymentMethod = None,
                   reference: str = "", payment_date: date = None) -> bool:
        """إضافة دفعة للفاتورة"""
        
        if amount <= 0:
            return False
        
        if self.paid_amount + amount > self.total_amount:
            return False  # المبلغ المدفوع يتجاوز إجمالي الفاتورة
        
        self.paid_amount += amount
        self.remaining_amount = self.total_amount - self.paid_amount
        
        # تحديث حالة الفاتورة
        if self.remaining_amount == 0:
            self.status = InvoiceStatus.PAID
        elif self.paid_amount > 0:
            self.status = InvoiceStatus.PARTIALLY_PAID
        
        return True
    
    def confirm_invoice(self) -> bool:
        """تأكيد الفاتورة"""
        if self.status != InvoiceStatus.DRAFT:
            return False
        
        if not self.items:
            return False
        
        self.status = InvoiceStatus.CONFIRMED
        self.confirmed_date = datetime.now()
        return True
    
    def cancel_invoice(self) -> bool:
        """إلغاء الفاتورة"""
        if self.status in [InvoiceStatus.PAID, InvoiceStatus.PARTIALLY_PAID]:
            return False  # لا يمكن إلغاء فاتورة مدفوعة
        
        self.status = InvoiceStatus.CANCELLED
        return True
    
    def to_dict(self) -> Dict:
        """تحويل الفاتورة إلى قاموس"""
        return {
            'invoice_id': self.invoice_id,
            'invoice_number': self.invoice_number,
            'date': self.date.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'customer_tax_number': self.customer_tax_number,
            'status': self.status.value,
            'payment_method': self.payment_method.value,
            'items': self.items,
            'subtotal': str(self.subtotal),
            'tax_amount': str(self.tax_amount),
            'discount_amount': str(self.discount_amount),
            'total_amount': str(self.total_amount),
            'paid_amount': str(self.paid_amount),
            'remaining_amount': str(self.remaining_amount),
            'tax_rate': str(self.tax_rate),
            'notes': self.notes,
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat(),
            'confirmed_date': self.confirmed_date.isoformat() if self.confirmed_date else None
        }

class SalesManager:
    """مدير المبيعات"""
    
    def __init__(self, database_manager=None):
        self.db_manager = database_manager
        self.invoices = {}  # invoice_id -> SalesInvoice
        self.next_invoice_number = 1
        self.customers = {}  # customer_id -> customer_data
        self.products = {}  # product_id -> product_data
    
    def create_invoice(self, customer_id: int, customer_name: str = "",
                      payment_method: PaymentMethod = PaymentMethod.CASH,
                      created_by: str = None) -> SalesInvoice:
        """إنشاء فاتورة جديدة"""
        
        invoice = SalesInvoice()
        invoice.customer_id = customer_id
        invoice.customer_name = customer_name
        invoice.payment_method = payment_method
        invoice.created_by = created_by
        
        self.invoices[invoice.invoice_id] = invoice
        return invoice
    
    def get_invoice(self, invoice_id: str) -> Optional[SalesInvoice]:
        """الحصول على فاتورة"""
        return self.invoices.get(invoice_id)
    
    def confirm_invoice(self, invoice_id: str) -> Tuple[bool, str]:
        """تأكيد فاتورة"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return False, "الفاتورة غير موجودة"
        
        if invoice.confirm_invoice():
            # ترقيم الفاتورة
            invoice.invoice_number = self.next_invoice_number
            self.next_invoice_number += 1
            
            return True, f"تم تأكيد الفاتورة رقم {invoice.invoice_number}"
        else:
            return False, "لا يمكن تأكيد الفاتورة"
    
    def get_invoices_by_customer(self, customer_id: int) -> List[SalesInvoice]:
        """الحصول على فواتير العميل"""
        return [
            invoice for invoice in self.invoices.values()
            if invoice.customer_id == customer_id
        ]
    
    def get_invoices_by_date_range(self, start_date: date, end_date: date) -> List[SalesInvoice]:
        """الحصول على الفواتير في فترة زمنية"""
        return [
            invoice for invoice in self.invoices.values()
            if start_date <= invoice.date <= end_date
        ]
    
    def get_sales_summary(self, start_date: date = None, end_date: date = None) -> Dict:
        """ملخص المبيعات"""
        
        invoices = list(self.invoices.values())
        
        # تطبيق فلتر التاريخ
        if start_date or end_date:
            filtered_invoices = []
            for invoice in invoices:
                if start_date and invoice.date < start_date:
                    continue
                if end_date and invoice.date > end_date:
                    continue
                filtered_invoices.append(invoice)
            invoices = filtered_invoices
        
        # حساب الإحصائيات
        total_invoices = len(invoices)
        confirmed_invoices = [inv for inv in invoices if inv.status != InvoiceStatus.DRAFT]
        
        total_sales = sum(inv.total_amount for inv in confirmed_invoices)
        total_paid = sum(inv.paid_amount for inv in confirmed_invoices)
        total_outstanding = sum(inv.remaining_amount for inv in confirmed_invoices)
        
        # تجميع حسب الحالة
        status_summary = {}
        for status in InvoiceStatus:
            count = len([inv for inv in invoices if inv.status == status])
            status_summary[status.value] = count
        
        return {
            'total_invoices': total_invoices,
            'confirmed_invoices': len(confirmed_invoices),
            'total_sales': total_sales,
            'total_paid': total_paid,
            'total_outstanding': total_outstanding,
            'collection_rate': (total_paid / total_sales * 100) if total_sales > 0 else 0,
            'status_summary': status_summary
        }
    
    def get_top_customers(self, limit: int = 10, start_date: date = None,
                         end_date: date = None) -> List[Dict]:
        """أفضل العملاء"""
        
        customer_sales = {}
        
        for invoice in self.invoices.values():
            # تطبيق فلتر التاريخ
            if start_date and invoice.date < start_date:
                continue
            if end_date and invoice.date > end_date:
                continue
            
            if invoice.status != InvoiceStatus.DRAFT:
                customer_id = invoice.customer_id
                if customer_id not in customer_sales:
                    customer_sales[customer_id] = {
                        'customer_id': customer_id,
                        'customer_name': invoice.customer_name,
                        'total_sales': Decimal('0'),
                        'total_invoices': 0
                    }
                
                customer_sales[customer_id]['total_sales'] += invoice.total_amount
                customer_sales[customer_id]['total_invoices'] += 1
        
        # ترتيب حسب المبيعات
        sorted_customers = sorted(
            customer_sales.values(),
            key=lambda x: x['total_sales'],
            reverse=True
        )
        
        return sorted_customers[:limit]
    
    def get_overdue_invoices(self, as_of_date: date = None) -> List[SalesInvoice]:
        """الفواتير المتأخرة"""
        
        if as_of_date is None:
            as_of_date = date.today()
        
        overdue_invoices = []
        
        for invoice in self.invoices.values():
            if (invoice.status in [InvoiceStatus.CONFIRMED, InvoiceStatus.PARTIALLY_PAID] and
                invoice.due_date and invoice.due_date < as_of_date and
                invoice.remaining_amount > 0):
                overdue_invoices.append(invoice)
        
        # ترتيب حسب تاريخ الاستحقاق
        overdue_invoices.sort(key=lambda x: x.due_date)
        
        return overdue_invoices
    
    def export_invoices(self, start_date: date = None, end_date: date = None) -> List[Dict]:
        """تصدير الفواتير"""
        
        invoices_to_export = []
        
        for invoice in self.invoices.values():
            # تطبيق فلتر التاريخ
            if start_date and invoice.date < start_date:
                continue
            if end_date and invoice.date > end_date:
                continue
            
            invoices_to_export.append(invoice.to_dict())
        
        # ترتيب حسب التاريخ ورقم الفاتورة
        invoices_to_export.sort(key=lambda x: (x['date'], x['invoice_number'] or 0))
        
        return invoices_to_export
