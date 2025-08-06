# -*- coding: utf-8 -*-
"""
مدير القيود المحاسبية
"""

import logging
from datetime import datetime, date
from database.database_manager import DatabaseManager
from database.accounts_manager import AccountsManager
from typing import Dict
from typing import List
from typing import Optional
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class JournalEntriesManager:
    """مدير القيود المحاسبية"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db_manager = db_manager or DatabaseManager()
        self.accounts_manager = AccountsManager(self.db_manager)
        self.logger = logging.getLogger(__name__)

    def create_journal_entry(self, entry_data: Dict) -> Dict:
        """إنشاء قيد محاسبي جديد"""
        try:
            # التحقق من صحة البيانات
            validation = self._validate_entry_data(entry_data)
            if not validation['is_valid']:
                return {
                    'success': False,
                    'errors': validation['errors']
                }

            # التحقق من التوازن
            balance_check = self._check_balance(entry_data['details'])
            if not balance_check['is_balanced']:
                return {
                    'success': False,
                    'errors': ['القيد غير متوازن - مجموع المدين يجب أن يساوي مجموع الدائن'],
                    'balance_info': balance_check
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # إنشاء رقم القيد
                entry_number = self._generate_entry_number()

                # إدراج القيد الرئيسي
                cursor.execute('''
                    INSERT INTO journal_entries 
                    (entry_number, entry_date, description, reference_type, reference_id,
                     total_debit, total_credit, is_balanced, status, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry_number,
                    entry_data['entry_date'],
                    entry_data['description'],
                    entry_data.get('reference_type'),
                    entry_data.get('reference_id'),
                    balance_check['total_debit'],
                    balance_check['total_credit'],
                    True,
                    'draft',
                    entry_data.get('created_by')
                ))

                entry_id = cursor.lastrowid

                # إدراج تفاصيل القيد
                for i, detail in enumerate(entry_data['details'], 1):
                    cursor.execute('''
                        INSERT INTO journal_entry_details 
                        (journal_entry_id, account_id, description, debit_amount, 
                         credit_amount, line_number)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        entry_id,
                        detail['account_id'],
                        detail.get('description', ''),
                        detail.get('debit_amount', 0),
                        detail.get('credit_amount', 0),
                        i
                    ))

                conn.commit()

                self.logger.info(f"تم إنشاء القيد: {entry_number}")

                return {
                    'success': True,
                    'entry_id': entry_id,
                    'entry_number': entry_number,
                    'message': 'تم إنشاء القيد بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء القيد: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في إنشاء القيد: {str(e)}']
            }

    def post_journal_entry(self, entry_id: int, posted_by: int) -> Dict:
        """ترحيل القيد المحاسبي"""
        try:
            # جلب القيد
            entry = self.get_journal_entry(entry_id)
            if not entry:
                return {
                    'success': False,
                    'errors': ['القيد غير موجود']
                }

            if entry['status'] == 'posted':
                return {
                    'success': False,
                    'errors': ['القيد مرحل بالفعل']
                }

            if not entry['is_balanced']:
                return {
                    'success': False,
                    'errors': ['لا يمكن ترحيل قيد غير متوازن']
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # تحديث أرصدة الحسابات
                for detail in entry['details']:
                    result = self.accounts_manager.update_account_balance(
                        detail['account_id'],
                        detail['debit_amount'],
                        detail['credit_amount']
                    )

                    if not result['success']:
                        conn.rollback()
                        return {
                            'success': False,
                            'errors': [f'خطأ في تحديث رصيد الحساب: {result["errors"]}']
                        }

                # تحديث حالة القيد
                cursor.execute('''
                    UPDATE journal_entries 
                    SET status = 'posted', posted_at = ?, posted_by = ?
                    WHERE id = ?
                ''', (datetime.now(), posted_by, entry_id))

                conn.commit()

                self.logger.info(f"تم ترحيل القيد: {entry['entry_number']}")

                return {
                    'success': True,
                    'message': 'تم ترحيل القيد بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في ترحيل القيد: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في ترحيل القيد: {str(e)}']
            }

    def get_journal_entry(self, entry_id: int) -> Optional[Dict]:
        """جلب قيد محاسبي"""
        try:
            # جلب القيد الرئيسي
            query = """
                SELECT je.*, u1.full_name as created_by_name, u2.full_name as posted_by_name
                FROM journal_entries je
                LEFT JOIN users u1 ON je.created_by = u1.id
                LEFT JOIN users u2 ON je.posted_by = u2.id
                WHERE je.id = ?
            """
            entry = self.db_manager.fetch_one(query, (entry_id,))

            if not entry:
                return None

            entry_dict = dict(entry)

            # جلب تفاصيل القيد
            details_query = """
                SELECT jed.*, coa.account_code, coa.account_name
                FROM journal_entry_details jed
                JOIN chart_of_accounts coa ON jed.account_id = coa.id
                WHERE jed.journal_entry_id = ?
                ORDER BY jed.line_number
            """
            details = self.db_manager.fetch_all(details_query, (entry_id,))
            entry_dict['details'] = [dict(detail) for detail in details]

            return entry_dict

        except Exception as e:
            self.logger.error(f"خطأ في جلب القيد: {e}")
            return None

    def get_all_journal_entries(self, status: str = None, start_date: date = None, 
                               end_date: date = None) -> List[Dict]:
        """جلب جميع القيود المحاسبية"""
        try:
            query = """
                SELECT je.*, u1.full_name as created_by_name
                FROM journal_entries je
                LEFT JOIN users u1 ON je.created_by = u1.id
                WHERE 1=1
            """
            params = []

            if status:
                query += " AND je.status = ?"
                params.append(status)

            if start_date:
                query += " AND je.entry_date >= ?"
                params.append(start_date)

            if end_date:
                query += " AND je.entry_date <= ?"
                params.append(end_date)

            query += " ORDER BY je.entry_date DESC, je.entry_number DESC"

            entries = self.db_manager.fetch_all(query, params)
            return [dict(entry) for entry in entries]

        except Exception as e:
            self.logger.error(f"خطأ في جلب القيود: {e}")
            return []

    def delete_journal_entry(self, entry_id: int) -> Dict:
        """حذف قيد محاسبي"""
        try:
            # التحقق من وجود القيد
            entry = self.get_journal_entry(entry_id)
            if not entry:
                return {
                    'success': False,
                    'errors': ['القيد غير موجود']
                }

            if entry['status'] == 'posted':
                return {
                    'success': False,
                    'errors': ['لا يمكن حذف قيد مرحل']
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # حذف تفاصيل القيد
                cursor.execute('DELETE FROM journal_entry_details WHERE journal_entry_id = ?', 
                             (entry_id,))

                # حذف القيد الرئيسي
                cursor.execute('DELETE FROM journal_entries WHERE id = ?', (entry_id,))

                conn.commit()

                self.logger.info(f"تم حذف القيد: {entry['entry_number']}")

                return {
                    'success': True,
                    'message': 'تم حذف القيد بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في حذف القيد: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في حذف القيد: {str(e)}']
            }

    def _validate_entry_data(self, entry_data: Dict) -> Dict:
        """التحقق من صحة بيانات القيد"""
        errors = []

        # التحقق من الحقول المطلوبة
        required_fields = ['entry_date', 'description', 'details']
        for field in required_fields:
            if not entry_data.get(field):
                errors.append(f'{field} مطلوب')

        # التحقق من وجود تفاصيل
        details = entry_data.get('details', [])
        if len(details) < 2:
            errors.append('يجب أن يحتوي القيد على سطرين على الأقل')

        # التحقق من صحة التفاصيل
        for i, detail in enumerate(details, 1):
            if not detail.get('account_id'):
                errors.append(f'معرف الحساب مطلوب في السطر {i}')

            debit = detail.get('debit_amount', 0)
            credit = detail.get('credit_amount', 0)

            if debit == 0 and credit == 0:
                errors.append(f'يجب إدخال مبلغ في السطر {i}')

            if debit > 0 and credit > 0:
                errors.append(f'لا يمكن إدخال مدين ودائن في نفس السطر {i}')

            if debit < 0 or credit < 0:
                errors.append(f'المبالغ يجب أن تكون موجبة في السطر {i}')

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def _check_balance(self, details: List[Dict]) -> Dict:
        """التحقق من توازن القيد"""
        total_debit = sum(detail.get('debit_amount', 0) for detail in details)
        total_credit = sum(detail.get('credit_amount', 0) for detail in details)

        return {
            'is_balanced': abs(total_debit - total_credit) < 0.01,  # تسامح للأخطاء العشرية
            'total_debit': total_debit,
            'total_credit': total_credit,
            'difference': total_debit - total_credit
        }

    def _generate_entry_number(self) -> str:
        """توليد رقم القيد"""
        try:
            # الحصول على آخر رقم قيد
            query = "SELECT MAX(CAST(SUBSTR(entry_number, 3) AS INTEGER)) FROM journal_entries WHERE entry_number LIKE 'JE%'"
            result = self.db_manager.fetch_one(query)

            last_number = result[0] if result and result[0] else 0
            new_number = last_number + 1

            return f"JE{new_number:06d}"

        except Exception as e:
            self.logger.error(f"خطأ في توليد رقم القيد: {e}")
            # في حالة الخطأ، استخدم timestamp
            return f"JE{int(datetime.now().timestamp())}"
