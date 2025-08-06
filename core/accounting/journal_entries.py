# -*- coding: utf-8 -*-
"""
نظام القيود المحاسبية
Journal Entries System
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, date
from enum import Enum
import uuid

class EntryType(Enum):
    """أنواع القيود"""
    MANUAL = "manual"  # قيد يدوي
    SALES = "sales"  # قيد مبيعات
    PURCHASE = "purchase"  # قيد مشتريات
    PAYMENT = "payment"  # قيد دفع
    RECEIPT = "receipt"  # قيد استلام
    ADJUSTMENT = "adjustment"  # قيد تسوية
    CLOSING = "closing"  # قيد إقفال

class EntryStatus(Enum):
    """حالات القيد"""
    DRAFT = "draft"  # مسودة
    POSTED = "posted"  # مرحل
    REVERSED = "reversed"  # مُلغى

class JournalEntry:
    """قيد محاسبي"""
    
    def __init__(self, entry_id: str = None):
        self.entry_id = entry_id or str(uuid.uuid4())
        self.entry_number = None  # رقم القيد التسلسلي
        self.date = date.today()
        self.description = ""
        self.entry_type = EntryType.MANUAL
        self.status = EntryStatus.DRAFT
        self.reference = ""  # مرجع القيد (رقم فاتورة، إيصال، إلخ)
        self.lines = []  # بنود القيد
        self.created_by = None
        self.created_date = datetime.now()
        self.posted_date = None
        self.total_debit = Decimal('0')
        self.total_credit = Decimal('0')
    
    def add_line(self, account_code: str, description: str,
                debit_amount: Decimal = Decimal('0'),
                credit_amount: Decimal = Decimal('0'),
                cost_center: str = None) -> bool:
        """إضافة بند للقيد"""
        
        if debit_amount == 0 and credit_amount == 0:
            return False
        
        if debit_amount > 0 and credit_amount > 0:
            return False  # لا يمكن أن يكون البند مدين ودائن في نفس الوقت
        
        line = {
            'line_id': str(uuid.uuid4()),
            'account_code': account_code,
            'description': description,
            'debit_amount': debit_amount,
            'credit_amount': credit_amount,
            'cost_center': cost_center
        }
        
        self.lines.append(line)
        self._update_totals()
        return True
    
    def remove_line(self, line_id: str) -> bool:
        """حذف بند من القيد"""
        for i, line in enumerate(self.lines):
            if line['line_id'] == line_id:
                del self.lines[i]
                self._update_totals()
                return True
        return False
    
    def _update_totals(self):
        """تحديث المجاميع"""
        self.total_debit = sum(line['debit_amount'] for line in self.lines)
        self.total_credit = sum(line['credit_amount'] for line in self.lines)
    
    def is_balanced(self) -> bool:
        """فحص توازن القيد"""
        return self.total_debit == self.total_credit
    
    def validate(self) -> Tuple[bool, List[str]]:
        """التحقق من صحة القيد"""
        errors = []
        
        if not self.description.strip():
            errors.append("وصف القيد مطلوب")
        
        if not self.lines:
            errors.append("القيد يجب أن يحتوي على بند واحد على الأقل")
        
        if len(self.lines) < 2:
            errors.append("القيد يجب أن يحتوي على بندين على الأقل")
        
        if not self.is_balanced():
            errors.append("القيد غير متوازن - مجموع المدين يجب أن يساوي مجموع الدائن")
        
        # فحص الحسابات
        for line in self.lines:
            if not line['account_code']:
                errors.append("رمز الحساب مطلوب لجميع البنود")
            
            if not line['description'].strip():
                errors.append("وصف البند مطلوب")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict:
        """تحويل القيد إلى قاموس"""
        return {
            'entry_id': self.entry_id,
            'entry_number': self.entry_number,
            'date': self.date.isoformat(),
            'description': self.description,
            'entry_type': self.entry_type.value,
            'status': self.status.value,
            'reference': self.reference,
            'lines': self.lines,
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat(),
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'total_debit': str(self.total_debit),
            'total_credit': str(self.total_credit)
        }

class JournalManager:
    """مدير القيود المحاسبية"""
    
    def __init__(self, database_manager=None, chart_of_accounts=None):
        self.db_manager = database_manager
        self.chart_of_accounts = chart_of_accounts
        self.entries = {}  # entry_id -> JournalEntry
        self.next_entry_number = 1
    
    def create_entry(self, description: str, entry_type: EntryType = EntryType.MANUAL,
                    reference: str = "", created_by: str = None) -> JournalEntry:
        """إنشاء قيد جديد"""
        
        entry = JournalEntry()
        entry.description = description
        entry.entry_type = entry_type
        entry.reference = reference
        entry.created_by = created_by
        
        self.entries[entry.entry_id] = entry
        return entry
    
    def get_entry(self, entry_id: str) -> Optional[JournalEntry]:
        """الحصول على قيد"""
        return self.entries.get(entry_id)
    
    def post_entry(self, entry_id: str) -> Tuple[bool, List[str]]:
        """ترحيل القيد"""
        
        entry = self.get_entry(entry_id)
        if not entry:
            return False, ["القيد غير موجود"]
        
        if entry.status != EntryStatus.DRAFT:
            return False, ["لا يمكن ترحيل قيد غير مسودة"]
        
        # التحقق من صحة القيد
        is_valid, errors = entry.validate()
        if not is_valid:
            return False, errors
        
        # ترقيم القيد
        entry.entry_number = self.next_entry_number
        self.next_entry_number += 1
        
        # تحديث حالة القيد
        entry.status = EntryStatus.POSTED
        entry.posted_date = datetime.now()
        
        # تحديث أرصدة الحسابات
        if self.chart_of_accounts:
            for line in entry.lines:
                account_code = line['account_code']
                
                if line['debit_amount'] > 0:
                    self.chart_of_accounts.update_account_balance(
                        account_code, line['debit_amount'], is_debit=True
                    )
                
                if line['credit_amount'] > 0:
                    self.chart_of_accounts.update_account_balance(
                        account_code, line['credit_amount'], is_debit=False
                    )
        
        return True, []
    
    def reverse_entry(self, entry_id: str, reason: str = "") -> Tuple[bool, str]:
        """عكس القيد (إلغاء)"""
        
        entry = self.get_entry(entry_id)
        if not entry:
            return False, "القيد غير موجود"
        
        if entry.status != EntryStatus.POSTED:
            return False, "لا يمكن عكس قيد غير مرحل"
        
        # إنشاء قيد عكسي
        reverse_entry = self.create_entry(
            description=f"عكس القيد رقم {entry.entry_number} - {reason}",
            entry_type=EntryType.ADJUSTMENT,
            reference=f"REV-{entry.entry_number}"
        )
        
        # إضافة البنود المعكوسة
        for line in entry.lines:
            reverse_entry.add_line(
                account_code=line['account_code'],
                description=f"عكس: {line['description']}",
                debit_amount=line['credit_amount'],  # عكس المبالغ
                credit_amount=line['debit_amount'],
                cost_center=line['cost_center']
            )
        
        # ترحيل القيد العكسي
        success, errors = self.post_entry(reverse_entry.entry_id)
        if success:
            # تحديث حالة القيد الأصلي
            entry.status = EntryStatus.REVERSED
            return True, f"تم إنشاء القيد العكسي رقم {reverse_entry.entry_number}"
        else:
            return False, f"فشل في إنشاء القيد العكسي: {', '.join(errors)}"
    
    def get_entries_by_date_range(self, start_date: date, end_date: date) -> List[JournalEntry]:
        """الحصول على القيود في فترة زمنية"""
        return [
            entry for entry in self.entries.values()
            if start_date <= entry.date <= end_date
        ]
    
    def get_entries_by_account(self, account_code: str) -> List[Dict]:
        """الحصول على القيود المتعلقة بحساب معين"""
        account_entries = []
        
        for entry in self.entries.values():
            if entry.status == EntryStatus.POSTED:
                for line in entry.lines:
                    if line['account_code'] == account_code:
                        account_entries.append({
                            'entry': entry,
                            'line': line
                        })
        
        return account_entries
    
    def get_account_ledger(self, account_code: str, start_date: date = None,
                          end_date: date = None) -> List[Dict]:
        """دفتر الأستاذ للحساب"""
        
        ledger = []
        running_balance = Decimal('0')
        
        # الحصول على القيود المتعلقة بالحساب
        account_entries = self.get_entries_by_account(account_code)
        
        # ترتيب حسب التاريخ
        account_entries.sort(key=lambda x: (x['entry'].date, x['entry'].entry_number))
        
        for item in account_entries:
            entry = item['entry']
            line = item['line']
            
            # تطبيق فلتر التاريخ
            if start_date and entry.date < start_date:
                continue
            if end_date and entry.date > end_date:
                continue
            
            # حساب الرصيد الجاري
            if line['debit_amount'] > 0:
                running_balance += line['debit_amount']
            else:
                running_balance -= line['credit_amount']
            
            ledger.append({
                'date': entry.date,
                'entry_number': entry.entry_number,
                'description': line['description'],
                'reference': entry.reference,
                'debit_amount': line['debit_amount'],
                'credit_amount': line['credit_amount'],
                'balance': running_balance
            })
        
        return ledger
    
    def get_general_ledger(self, start_date: date = None, end_date: date = None) -> Dict:
        """دفتر الأستاذ العام"""
        
        general_ledger = {}
        
        # الحصول على جميع الحسابات المستخدمة
        used_accounts = set()
        for entry in self.entries.values():
            if entry.status == EntryStatus.POSTED:
                for line in entry.lines:
                    used_accounts.add(line['account_code'])
        
        # إنشاء دفتر أستاذ لكل حساب
        for account_code in used_accounts:
            general_ledger[account_code] = self.get_account_ledger(
                account_code, start_date, end_date
            )
        
        return general_ledger
    
    def export_entries(self, start_date: date = None, end_date: date = None) -> List[Dict]:
        """تصدير القيود"""
        
        entries_to_export = []
        
        for entry in self.entries.values():
            # تطبيق فلتر التاريخ
            if start_date and entry.date < start_date:
                continue
            if end_date and entry.date > end_date:
                continue
            
            entries_to_export.append(entry.to_dict())
        
        # ترتيب حسب التاريخ ورقم القيد
        entries_to_export.sort(key=lambda x: (x['date'], x['entry_number'] or 0))
        
        return entries_to_export
