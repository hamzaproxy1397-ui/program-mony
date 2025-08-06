# -*- coding: utf-8 -*-
"""
مدير شجرة الحسابات المحاسبية
Chart of Accounts Tree Manager
"""

import logging
from database.database_manager import DatabaseManager
from typing import Dict
from typing import List
from typing import Optional
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class AccountsTreeManager:
    """مدير شجرة الحسابات مع خوارزميات متقدمة"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db_manager = db_manager or DatabaseManager()
        self.logger = logging.getLogger(__name__)

    def add_account(self, name: str, code: str, account_type: str, 
                   parent_id: int = None, description: str = "") -> Dict:
        """
        إضافة حساب جديد إلى شجرة الحسابات

        الخوارزمية:
        1. التحقق من صحة البيانات
        2. حساب المستوى من الحساب الأب
        3. تحديد نوع الحساب (ورقة أم عقدة)
        4. تحديث الحساب الأب ليصبح عقدة
        5. إدراج الحساب في قاعدة البيانات
        """
        try:
            # 1. التحقق من صحة البيانات
            validation = self._validate_account_data(name, code, account_type, parent_id)
            if not validation['is_valid']:
                return {
                    'success': False,
                    'errors': validation['errors']
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # 2. حساب المستوى من الحساب الأب
                level = self._get_level_from_parent(cursor, parent_id)

                # 3. تحديد أن الحساب الجديد ورقة (is_leaf = True)
                is_leaf = True

                # 4. تحديث الحساب الأب ليصبح عقدة إذا كان موجود
                if parent_id:
                    self._update_parent_to_non_leaf(cursor, parent_id)

                # 5. إدراج الحساب الجديد
                cursor.execute('''
                    INSERT INTO chart_of_accounts
                    (account_name, account_code, account_type, parent_account_id, account_level,
                     is_main_account, current_balance, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, 0.0, 1)
                ''', (name, code, account_type, parent_id, level, 0 if parent_id else 1))

                account_id = cursor.lastrowid
                conn.commit()

                self.logger.info(f"تم إضافة حساب جديد: {name} ({code})")

                return {
                    'success': True,
                    'account_id': account_id,
                    'level': level,
                    'message': f'تم إضافة الحساب {name} بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في إضافة الحساب: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في إضافة الحساب: {str(e)}']
            }

    def delete_account(self, account_id: int) -> Dict:
        """
        حذف حساب من شجرة الحسابات

        الخوارزمية:
        1. التحقق من وجود الحساب
        2. التحقق من عدم وجود حسابات فرعية
        3. التحقق من عدم وجود حركات محاسبية
        4. حذف الحساب
        5. تحديث حالة الحساب الأب إذا لزم الأمر
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # 1. التحقق من وجود الحساب
                account = self._get_account_by_id(cursor, account_id)
                if not account:
                    return {
                        'success': False,
                        'errors': ['الحساب غير موجود']
                    }

                # 2. التحقق من عدم وجود حسابات فرعية
                children = self._get_children_accounts(cursor, account_id)
                if children:
                    return {
                        'success': False,
                        'errors': ['لا يمكن حذف حساب يحتوي على حسابات فرعية']
                    }

                # 3. التحقق من عدم وجود حركات محاسبية
                has_transactions = self._has_transactions(cursor, account_id)
                if has_transactions:
                    return {
                        'success': False,
                        'errors': ['لا يمكن حذف حساب يحتوي على حركات محاسبية']
                    }

                # 4. حذف الحساب
                cursor.execute('DELETE FROM chart_of_accounts WHERE id = ?', (account_id,))

                # 5. تحديث حالة الحساب الأب إذا لزم الأمر
                if account['parent_id']:
                    self._update_parent_leaf_status(cursor, account['parent_id'])

                conn.commit()

                self.logger.info(f"تم حذف الحساب: {account['name']} ({account['code']})")

                return {
                    'success': True,
                    'message': f'تم حذف الحساب {account["name"]} بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في حذف الحساب: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في حذف الحساب: {str(e)}']
            }

    def move_account(self, account_id: int, new_parent_id: int = None) -> Dict:
        """
        نقل حساب إلى موقع جديد في الشجرة

        الخوارزمية:
        1. التحقق من صحة العملية
        2. حفظ الحساب الأب القديم
        3. تحديث الحساب بالأب الجديد
        4. إعادة حساب المستويات للحساب وفروعه
        5. تحديث حالة الحسابات الأب
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # 1. التحقق من صحة العملية
                validation = self._validate_move_operation(cursor, account_id, new_parent_id)
                if not validation['is_valid']:
                    return {
                        'success': False,
                        'errors': validation['errors']
                    }

                account = self._get_account_by_id(cursor, account_id)
                old_parent_id = account['parent_id']

                # 2. تحديث الحساب بالأب الجديد
                new_level = self._get_level_from_parent(cursor, new_parent_id)

                cursor.execute('''
                    UPDATE chart_of_accounts 
                    SET parent_id = ?, level = ?
                    WHERE id = ?
                ''', (new_parent_id, new_level, account_id))

                # 3. إعادة حساب المستويات للحسابات الفرعية
                self._recalculate_levels_recursive(cursor, account_id)

                # 4. تحديث حالة الحسابات الأب
                if new_parent_id:
                    self._update_parent_to_non_leaf(cursor, new_parent_id)

                if old_parent_id:
                    self._update_parent_leaf_status(cursor, old_parent_id)

                conn.commit()

                self.logger.info(f"تم نقل الحساب: {account['name']} إلى أب جديد")

                return {
                    'success': True,
                    'message': f'تم نقل الحساب {account["name"]} بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في نقل الحساب: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في نقل الحساب: {str(e)}']
            }

    def get_account_tree(self, parent_id: int = None, max_depth: int = None) -> List[Dict]:
        """
        جلب شجرة الحسابات بشكل هرمي

        الخوارزمية:
        1. جلب الحسابات الجذر أو الفرعية
        2. ترتيب الحسابات حسب الكود
        3. بناء الشجرة بشكل تكراري
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                return self._build_tree_recursive(cursor, parent_id, 0, max_depth)

        except Exception as e:
            self.logger.error(f"خطأ في جلب شجرة الحسابات: {e}")
            return []

    def get_account_path(self, account_id: int) -> List[Dict]:
        """
        جلب مسار الحساب من الجذر إلى الحساب المحدد

        الخوارزمية:
        1. البدء من الحساب المحدد
        2. التنقل عبر الحسابات الأب
        3. بناء المسار من الجذر إلى الحساب
        """
        try:
            path = []
            current_id = account_id

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                while current_id:
                    account = self._get_account_by_id(cursor, current_id)
                    if not account:
                        break

                    path.insert(0, {
                        'id': account['id'],
                        'name': account['name'],
                        'code': account['code'],
                        'level': account['level']
                    })

                    current_id = account['parent_id']

                return path

        except Exception as e:
            self.logger.error(f"خطأ في جلب مسار الحساب: {e}")
            return []

    def get_leaf_accounts(self, account_type: str = None) -> List[Dict]:
        """جلب الحسابات الورقية (التي يمكن إجراء حركات عليها)"""
        try:
            query = """
                SELECT id, name, code, account_type, current_balance, level
                FROM chart_of_accounts 
                WHERE is_leaf = 1 AND is_active = 1
            """
            params = []

            if account_type:
                query += " AND account_type = ?"
                params.append(account_type)

            query += " ORDER BY code"

            accounts = self.db_manager.fetch_all(query, params)
            return [dict(account) for account in accounts]

        except Exception as e:
            self.logger.error(f"خطأ في جلب الحسابات الورقية: {e}")
            return []

    def validate_tree_integrity(self) -> Dict:
        """
        التحقق من سلامة شجرة الحسابات

        الفحوصات:
        1. عدم وجود دورات في الشجرة
        2. صحة المستويات
        3. صحة حالة is_leaf
        4. فرادة الأكواد
        """
        try:
            errors = []
            warnings = []

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # 1. فحص الدورات
                cycles = self._detect_cycles(cursor)
                if cycles:
                    errors.extend([f"دورة مكتشفة في الحساب: {cycle}" for cycle in cycles])

                # 2. فحص المستويات
                level_errors = self._validate_levels(cursor)
                errors.extend(level_errors)

                # 3. فحص حالة is_leaf
                leaf_errors = self._validate_leaf_status(cursor)
                errors.extend(leaf_errors)

                # 4. فحص فرادة الأكواد
                duplicate_codes = self._find_duplicate_codes(cursor)
                if duplicate_codes:
                    errors.extend([f"كود مكرر: {code}" for code in duplicate_codes])

                return {
                    'is_valid': len(errors) == 0,
                    'errors': errors,
                    'warnings': warnings
                }

        except Exception as e:
            self.logger.error(f"خطأ في فحص سلامة الشجرة: {e}")
            return {
                'is_valid': False,
                'errors': [f'خطأ في فحص سلامة الشجرة: {str(e)}'],
                'warnings': []
            }

    # ==================== الدوال المساعدة ====================

    def _get_level_from_parent(self, cursor, parent_id: int) -> int:
        """حساب مستوى الحساب من الحساب الأب"""
        if not parent_id:
            return 0

        cursor.execute('SELECT account_level FROM chart_of_accounts WHERE id = ?', (parent_id,))
        parent = cursor.fetchone()

        return (parent['account_level'] + 1) if parent else 0

    def _update_parent_to_non_leaf(self, cursor, parent_id: int):
        """تحديث الحساب الأب ليصبح عقدة (غير ورقة)"""
        cursor.execute('''
            UPDATE chart_of_accounts
            SET is_main_account = 0
            WHERE id = ?
        ''', (parent_id,))

    def _update_parent_leaf_status(self, cursor, parent_id: int):
        """تحديث حالة is_main_account للحساب الأب حسب وجود أطفال"""
        cursor.execute('''
            SELECT COUNT(*) as children_count
            FROM chart_of_accounts
            WHERE parent_account_id = ? AND is_active = 1
        ''', (parent_id,))

        result = cursor.fetchone()
        has_children = result['children_count'] > 0

        cursor.execute('''
            UPDATE chart_of_accounts
            SET is_main_account = ?
            WHERE id = ?
        ''', (0 if has_children else 1, parent_id))

    def _get_account_by_id(self, cursor, account_id: int) -> Optional[Dict]:
        """جلب حساب بالمعرف"""
        cursor.execute('SELECT * FROM chart_of_accounts WHERE id = ?', (account_id,))
        account = cursor.fetchone()
        return dict(account) if account else None

    def _get_children_accounts(self, cursor, parent_id: int) -> List[Dict]:
        """جلب الحسابات الفرعية"""
        cursor.execute('''
            SELECT * FROM chart_of_accounts
            WHERE parent_account_id = ? AND is_active = 1
        ''', (parent_id,))

        return [dict(account) for account in cursor.fetchall()]

    def _has_transactions(self, cursor, account_id: int) -> bool:
        """التحقق من وجود حركات محاسبية للحساب"""
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM journal_entry_details 
            WHERE account_id = ?
        ''', (account_id,))

        result = cursor.fetchone()
        return result['count'] > 0

    def _validate_account_data(self, name: str, code: str, account_type: str, 
                              parent_id: int) -> Dict:
        """التحقق من صحة بيانات الحساب"""
        errors = []

        if not name.strip():
            errors.append('اسم الحساب مطلوب')

        if not code.strip():
            errors.append('كود الحساب مطلوب')

        if not account_type:
            errors.append('نوع الحساب مطلوب')

        # التحقق من فرادة الكود
        existing = self.db_manager.fetch_one(
            'SELECT id FROM chart_of_accounts WHERE account_code = ?', (code,)
        )
        if existing:
            errors.append('كود الحساب موجود مسبقاً')

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def _validate_move_operation(self, cursor, account_id: int, new_parent_id: int) -> Dict:
        """التحقق من صحة عملية النقل"""
        errors = []

        # التحقق من وجود الحساب
        account = self._get_account_by_id(cursor, account_id)
        if not account:
            errors.append('الحساب المراد نقله غير موجود')
            return {'is_valid': False, 'errors': errors}

        # التحقق من عدم نقل الحساب إلى نفسه
        if account_id == new_parent_id:
            errors.append('لا يمكن نقل الحساب إلى نفسه')

        # التحقق من عدم نقل الحساب إلى أحد فروعه
        if new_parent_id and self._is_descendant(cursor, new_parent_id, account_id):
            errors.append('لا يمكن نقل الحساب إلى أحد فروعه')

        # التحقق من وجود الحساب الأب الجديد
        if new_parent_id:
            new_parent = self._get_account_by_id(cursor, new_parent_id)
            if not new_parent:
                errors.append('الحساب الأب الجديد غير موجود')

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def _is_descendant(self, cursor, potential_descendant: int, ancestor: int) -> bool:
        """التحقق من كون حساب فرع لحساب آخر"""
        current_id = potential_descendant

        while current_id:
            if current_id == ancestor:
                return True

            cursor.execute('SELECT parent_account_id FROM chart_of_accounts WHERE id = ?', (current_id,))
            result = cursor.fetchone()
            current_id = result['parent_account_id'] if result else None

        return False

    def _recalculate_levels_recursive(self, cursor, account_id: int):
        """إعادة حساب المستويات للحساب وجميع فروعه"""
        # جلب الحساب الحالي
        account = self._get_account_by_id(cursor, account_id)
        if not account:
            return

        # حساب المستوى الجديد
        new_level = self._get_level_from_parent(cursor, account['parent_account_id'])

        # تحديث مستوى الحساب
        cursor.execute('UPDATE chart_of_accounts SET account_level = ? WHERE id = ?',
                      (new_level, account_id))

        # إعادة حساب مستويات الفروع
        children = self._get_children_accounts(cursor, account_id)
        for child in children:
            self._recalculate_levels_recursive(cursor, child['id'])

    def _build_tree_recursive(self, cursor, parent_id: int, current_depth: int,
                             max_depth: int) -> List[Dict]:
        """بناء الشجرة بشكل تكراري"""
        if max_depth is not None and current_depth >= max_depth:
            return []

        # جلب الحسابات الفرعية
        if parent_id is None:
            cursor.execute('''
                SELECT * FROM chart_of_accounts
                WHERE parent_id IS NULL AND is_active = 1
                ORDER BY code
            ''')
        else:
            cursor.execute('''
                SELECT * FROM chart_of_accounts
                WHERE parent_id = ? AND is_active = 1
                ORDER BY code
            ''', (parent_id,))

        accounts = cursor.fetchall()
        tree = []

        for account in accounts:
            account_dict = dict(account)

            # إضافة الفروع
            children = self._build_tree_recursive(
                cursor, account['id'], current_depth + 1, max_depth
            )
            account_dict['children'] = children
            account_dict['has_children'] = len(children) > 0

            tree.append(account_dict)

        return tree

    def _detect_cycles(self, cursor) -> List[int]:
        """اكتشاف الدورات في الشجرة"""
        cycles = []

        cursor.execute('SELECT id FROM chart_of_accounts WHERE is_active = 1')
        all_accounts = cursor.fetchall()

        for account in all_accounts:
            visited = set()
            current_id = account['id']

            while current_id and current_id not in visited:
                visited.add(current_id)

                cursor.execute('SELECT parent_id FROM chart_of_accounts WHERE id = ?',
                              (current_id,))
                result = cursor.fetchone()
                current_id = result['parent_id'] if result else None

            if current_id and current_id in visited:
                cycles.append(current_id)

        return list(set(cycles))

    def _validate_levels(self, cursor) -> List[str]:
        """التحقق من صحة المستويات"""
        errors = []

        cursor.execute('''
            SELECT c.id, c.name, c.level, p.level as parent_level
            FROM chart_of_accounts c
            LEFT JOIN chart_of_accounts p ON c.parent_id = p.id
            WHERE c.is_active = 1
        ''')

        accounts = cursor.fetchall()

        for account in accounts:
            expected_level = (account['parent_level'] + 1) if account['parent_level'] is not None else 0

            if account['level'] != expected_level:
                errors.append(f"مستوى خاطئ للحساب {account['name']}: "
                            f"متوقع {expected_level}, موجود {account['level']}")

        return errors

    def _validate_leaf_status(self, cursor) -> List[str]:
        """التحقق من صحة حالة is_leaf"""
        errors = []

        cursor.execute('''
            SELECT c.id, c.name, c.is_leaf,
                   COUNT(child.id) as children_count
            FROM chart_of_accounts c
            LEFT JOIN chart_of_accounts child ON c.id = child.parent_id AND child.is_active = 1
            WHERE c.is_active = 1
            GROUP BY c.id, c.name, c.is_leaf
        ''')

        accounts = cursor.fetchall()

        for account in accounts:
            has_children = account['children_count'] > 0
            should_be_leaf = not has_children

            if account['is_leaf'] != should_be_leaf:
                status = "ورقة" if should_be_leaf else "عقدة"
                errors.append(f"حالة خاطئة للحساب {account['name']}: يجب أن يكون {status}")

        return errors

    def _find_duplicate_codes(self, cursor) -> List[str]:
        """البحث عن الأكواد المكررة"""
        cursor.execute('''
            SELECT code, COUNT(*) as count
            FROM chart_of_accounts
            WHERE is_active = 1
            GROUP BY code
            HAVING COUNT(*) > 1
        ''')

        duplicates = cursor.fetchall()
        return [dup['code'] for dup in duplicates]

    def get_account_balance_with_children(self, account_id: int) -> float:
        """حساب رصيد الحساب مع جميع فروعه"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # جلب رصيد الحساب نفسه
                account = self._get_account_by_id(cursor, account_id)
                if not account:
                    return 0.0

                total_balance = account['current_balance']

                # إضافة أرصدة الفروع
                children = self._get_children_accounts(cursor, account_id)
                for child in children:
                    total_balance += self.get_account_balance_with_children(child['id'])

                return total_balance

        except Exception as e:
            self.logger.error(f"خطأ في حساب رصيد الحساب مع الفروع: {e}")
            return 0.0

    def get_accounts_by_type_tree(self, account_type: str) -> List[Dict]:
        """جلب شجرة الحسابات حسب النوع"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # جلب الحسابات الجذر من النوع المحدد
                cursor.execute('''
                    SELECT * FROM chart_of_accounts
                    WHERE account_type = ? AND parent_id IS NULL AND is_active = 1
                    ORDER BY code
                ''', (account_type,))

                root_accounts = cursor.fetchall()
                tree = []

                for account in root_accounts:
                    account_dict = dict(account)
                    account_dict['children'] = self._build_tree_recursive(cursor, account['id'], 0, None)
                    tree.append(account_dict)

                return tree

        except Exception as e:
            self.logger.error(f"خطأ في جلب شجرة الحسابات حسب النوع: {e}")
            return []
