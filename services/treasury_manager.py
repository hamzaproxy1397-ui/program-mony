# -*- coding: utf-8 -*-
"""
مدير الخزينة
"""

import logging
from database.database_manager import DatabaseManager
from database.journal_entries_manager import JournalEntriesManager
from database.accounts_manager import AccountsManager
from datetime import date
from typing import Dict
from typing import List
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class TreasuryManager:
    """مدير الخزينة والعمليات النقدية"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db_manager = db_manager or DatabaseManager()
        self.journal_manager = JournalEntriesManager(self.db_manager)
        self.accounts_manager = AccountsManager(self.db_manager)
        self.logger = logging.getLogger(__name__)

    def get_cash_balance(self) -> float:
        """الحصول على رصيد النقدية"""
        try:
            # البحث عن حساب النقدية
            cash_account = self.accounts_manager.get_account_by_code('1110')  # النقدية في الصندوق
            if cash_account:
                return cash_account['current_balance']
            else:
                return 0.0
        except Exception as e:
            self.logger.error(f"خطأ في جلب رصيد النقدية: {e}")
            return 0.0

    def get_bank_balance(self) -> float:
        """الحصول على رصيد البنك"""
        try:
            # البحث عن حساب البنك
            bank_account = self.accounts_manager.get_account_by_code('1120')  # النقدية في البنك
            if bank_account:
                return bank_account['current_balance']
            else:
                return 0.0
        except Exception as e:
            self.logger.error(f"خطأ في جلب رصيد البنك: {e}")
            return 0.0

    def get_total_treasury_balance(self) -> float:
        """الحصول على إجمالي رصيد الخزينة"""
        return self.get_cash_balance() + self.get_bank_balance()

    def add_cash_receipt(self, amount: float, description: str, from_party: str = "", 
                        reference_type: str = "", reference_id: int = None) -> Dict:
        """إضافة قبض نقدي"""
        try:
            if amount <= 0:
                return {
                    'success': False,
                    'errors': ['المبلغ يجب أن يكون أكبر من صفر']
                }

            # البحث عن الحسابات المطلوبة
            cash_account = self.accounts_manager.get_account_by_code('1110')  # النقدية في الصندوق

            if not cash_account:
                return {
                    'success': False,
                    'errors': ['لم يتم العثور على حساب النقدية']
                }

            # إعداد تفاصيل القيد
            entry_details = [
                {
                    'account_id': cash_account['id'],
                    'description': f'قبض نقدي - {description}',
                    'debit_amount': amount,
                    'credit_amount': 0
                }
            ]

            # تحديد الحساب المقابل حسب نوع المرجع
            if reference_type == 'sales':
                # قبض من مبيعات
                sales_account = self.accounts_manager.get_account_by_code('4110')  # إيرادات المبيعات
                if sales_account:
                    entry_details.append({
                        'account_id': sales_account['id'],
                        'description': f'إيرادات مبيعات - {description}',
                        'debit_amount': 0,
                        'credit_amount': amount
                    })
            else:
                # قبض عام - حساب إيرادات متنوعة
                misc_income_account = self.accounts_manager.get_account_by_code('4900')  # إيرادات متنوعة
                if not misc_income_account:
                    # إنشاء حساب إيرادات متنوعة إذا لم يكن موجود
                    misc_income_account = self.accounts_manager.get_account_by_code('4110')  # إيرادات المبيعات

                if misc_income_account:
                    entry_details.append({
                        'account_id': misc_income_account['id'],
                        'description': f'إيرادات متنوعة - {description}',
                        'debit_amount': 0,
                        'credit_amount': amount
                    })

            # إنشاء القيد
            entry_data = {
                'entry_date': date.today(),
                'description': f'قبض نقدي - {description}',
                'reference_type': reference_type or 'cash_receipt',
                'reference_id': reference_id,
                'details': entry_details,
                'created_by': 1
            }

            result = self.journal_manager.create_journal_entry(entry_data)

            if result['success']:
                # ترحيل القيد تلقائياً
                post_result = self.journal_manager.post_journal_entry(result['entry_id'], 1)

                return {
                    'success': True,
                    'entry_id': result['entry_id'],
                    'entry_number': result['entry_number'],
                    'amount': amount,
                    'new_balance': self.get_cash_balance(),
                    'message': 'تم تسجيل القبض النقدي بنجاح'
                }
            else:
                return result

        except Exception as e:
            self.logger.error(f"خطأ في إضافة قبض نقدي: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في إضافة قبض نقدي: {str(e)}']
            }

    def add_cash_payment(self, amount: float, description: str, to_party: str = "", 
                        reference_type: str = "", reference_id: int = None) -> Dict:
        """إضافة دفع نقدي"""
        try:
            if amount <= 0:
                return {
                    'success': False,
                    'errors': ['المبلغ يجب أن يكون أكبر من صفر']
                }

            # التحقق من توفر الرصيد
            current_balance = self.get_cash_balance()
            if current_balance < amount:
                return {
                    'success': False,
                    'errors': [f'الرصيد غير كافي. الرصيد الحالي: {current_balance:.2f}']
                }

            # البحث عن الحسابات المطلوبة
            cash_account = self.accounts_manager.get_account_by_code('1110')  # النقدية في الصندوق

            if not cash_account:
                return {
                    'success': False,
                    'errors': ['لم يتم العثور على حساب النقدية']
                }

            # إعداد تفاصيل القيد
            entry_details = [
                {
                    'account_id': cash_account['id'],
                    'description': f'دفع نقدي - {description}',
                    'debit_amount': 0,
                    'credit_amount': amount
                }
            ]

            # تحديد الحساب المقابل حسب نوع المرجع
            if reference_type == 'purchases':
                # دفع للمشتريات
                purchases_account = self.accounts_manager.get_account_by_code('5110')  # تكلفة المبيعات
                if purchases_account:
                    entry_details.append({
                        'account_id': purchases_account['id'],
                        'description': f'مشتريات - {description}',
                        'debit_amount': amount,
                        'credit_amount': 0
                    })
            else:
                # دفع عام - حساب مصروفات متنوعة
                misc_expense_account = self.accounts_manager.get_account_by_code('5900')  # مصروفات متنوعة
                if misc_expense_account:
                    entry_details.append({
                        'account_id': misc_expense_account['id'],
                        'description': f'مصروفات متنوعة - {description}',
                        'debit_amount': amount,
                        'credit_amount': 0
                    })

            # إنشاء القيد
            entry_data = {
                'entry_date': date.today(),
                'description': f'دفع نقدي - {description}',
                'reference_type': reference_type or 'cash_payment',
                'reference_id': reference_id,
                'details': entry_details,
                'created_by': 1
            }

            result = self.journal_manager.create_journal_entry(entry_data)

            if result['success']:
                # ترحيل القيد تلقائياً
                post_result = self.journal_manager.post_journal_entry(result['entry_id'], 1)

                return {
                    'success': True,
                    'entry_id': result['entry_id'],
                    'entry_number': result['entry_number'],
                    'amount': amount,
                    'new_balance': self.get_cash_balance(),
                    'message': 'تم تسجيل الدفع النقدي بنجاح'
                }
            else:
                return result

        except Exception as e:
            self.logger.error(f"خطأ في إضافة دفع نقدي: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في إضافة دفع نقدي: {str(e)}']
            }

    def get_treasury_movements(self, start_date: date = None, end_date: date = None) -> List[Dict]:
        """جلب حركات الخزينة"""
        try:
            # جلب القيود المحاسبية المتعلقة بالنقدية
            query = """
                SELECT
                    je.entry_date,
                    je.entry_number,
                    je.description,
                    jed.description as detail_description,
                    jed.debit_amount,
                    jed.credit_amount,
                    ca.name as account_name,
                    je.reference_type
                FROM journal_entries je
                JOIN journal_entry_details jed ON je.id = jed.journal_entry_id
                JOIN chart_of_accounts ca ON jed.account_id = ca.id
                WHERE ca.code IN ('1110', '1120')  -- النقدية في الصندوق والبنك
                AND je.status = 'posted'
            """
            params = []

            if start_date:
                query += " AND je.entry_date >= ?"
                params.append(start_date)

            if end_date:
                query += " AND je.entry_date <= ?"
                params.append(end_date)

            query += " ORDER BY je.entry_date DESC, je.id DESC"

            movements = self.db_manager.fetch_all(query, params)

            # تحويل إلى تنسيق مناسب للعرض
            formatted_movements = []
            for movement in movements:
                movement_type = "قبض" if movement['debit_amount'] > 0 else "دفع"
                amount = movement['debit_amount'] if movement['debit_amount'] > 0 else movement['credit_amount']

                formatted_movements.append({
                    'date': movement['entry_date'],
                    'entry_number': movement['entry_number'],
                    'type': movement_type,
                    'description': movement['detail_description'],
                    'amount': amount,
                    'account': movement['account_name'],
                    'reference_type': movement['reference_type']
                })

            return formatted_movements

        except Exception as e:
            self.logger.error(f"خطأ في جلب حركات الخزينة: {e}")
            return []

    def get_daily_summary(self, target_date: date = None) -> Dict:
        """ملخص يومي للخزينة"""
        try:
            if not target_date:
                target_date = date.today()

            movements = self.get_treasury_movements(target_date, target_date)

            total_receipts = sum(m['amount'] for m in movements if m['type'] == 'قبض')
            total_payments = sum(m['amount'] for m in movements if m['type'] == 'دفع')

            return {
                'date': target_date,
                'opening_balance': self.get_total_treasury_balance() - (total_receipts - total_payments),
                'total_receipts': total_receipts,
                'total_payments': total_payments,
                'net_movement': total_receipts - total_payments,
                'closing_balance': self.get_total_treasury_balance(),
                'movements_count': len(movements)
            }

        except Exception as e:
            self.logger.error(f"خطأ في ملخص الخزينة اليومي: {e}")
            return {
                'date': target_date,
                'opening_balance': 0,
                'total_receipts': 0,
                'total_payments': 0,
                'net_movement': 0,
                'closing_balance': 0,
                'movements_count': 0
            }
