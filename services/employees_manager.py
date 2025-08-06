# -*- coding: utf-8 -*-
"""
مدير الموظفين
"""

import logging
from database.database_manager import DatabaseManager
from datetime import date
from typing import Dict
from typing import List
from typing import Optional
from typing import List, Dict, Optional, Tuple, Any, Union, Callable

class EmployeesManager:
    """مدير الموظفين والرواتب"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db_manager = db_manager or DatabaseManager()
        self.logger = logging.getLogger(__name__)

    def add_employee(self, employee_data: Dict) -> Dict:
        """إضافة موظف جديد"""
        try:
            # التحقق من صحة البيانات
            validation = self._validate_employee_data(employee_data)
            if not validation['is_valid']:
                return {
                    'success': False,
                    'errors': validation['errors']
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO employees 
                    (name, position, department, phone, email, hire_date, salary, 
                     national_id, address, emergency_contact, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (
                    employee_data['name'],
                    employee_data.get('position', ''),
                    employee_data.get('department', ''),
                    employee_data.get('phone', ''),
                    employee_data.get('email', ''),
                    employee_data.get('hire_date', date.today()),
                    employee_data.get('salary', 0),
                    employee_data.get('national_id', ''),
                    employee_data.get('address', ''),
                    employee_data.get('emergency_contact', '')
                ))

                employee_id = cursor.lastrowid
                conn.commit()

                self.logger.info(f"تم إضافة موظف جديد: {employee_data['name']}")

                return {
                    'success': True,
                    'employee_id': employee_id,
                    'message': 'تم إضافة الموظف بنجاح'
                }

        except Exception as e:
            self.logger.error(f"خطأ في إضافة موظف: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في إضافة الموظف: {str(e)}']
            }

    def update_employee(self, employee_id: int, employee_data: Dict) -> Dict:
        """تحديث بيانات موظف"""
        try:
            # التحقق من صحة البيانات
            validation = self._validate_employee_data(employee_data)
            if not validation['is_valid']:
                return {
                    'success': False,
                    'errors': validation['errors']
                }

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    UPDATE employees 
                    SET name = ?, position = ?, department = ?, phone = ?, email = ?,
                        salary = ?, national_id = ?, address = ?, emergency_contact = ?
                    WHERE id = ?
                ''', (
                    employee_data['name'],
                    employee_data.get('position', ''),
                    employee_data.get('department', ''),
                    employee_data.get('phone', ''),
                    employee_data.get('email', ''),
                    employee_data.get('salary', 0),
                    employee_data.get('national_id', ''),
                    employee_data.get('address', ''),
                    employee_data.get('emergency_contact', ''),
                    employee_id
                ))

                conn.commit()

                if cursor.rowcount > 0:
                    self.logger.info(f"تم تحديث بيانات الموظف: {employee_id}")
                    return {
                        'success': True,
                        'message': 'تم تحديث بيانات الموظف بنجاح'
                    }
                else:
                    return {
                        'success': False,
                        'errors': ['الموظف غير موجود']
                    }

        except Exception as e:
            self.logger.error(f"خطأ في تحديث الموظف: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في تحديث الموظف: {str(e)}']
            }

    def get_employee(self, employee_id: int) -> Optional[Dict]:
        """جلب بيانات موظف"""
        try:
            query = "SELECT * FROM employees WHERE id = ?"
            employee = self.db_manager.fetch_one(query, (employee_id,))

            if employee:
                return dict(employee)
            return None

        except Exception as e:
            self.logger.error(f"خطأ في جلب بيانات الموظف: {e}")
            return None

    def get_all_employees(self, active_only: bool = True) -> List[Dict]:
        """جلب جميع الموظفين"""
        try:
            query = "SELECT * FROM employees"
            params = []

            if active_only:
                query += " WHERE is_active = 1"

            query += " ORDER BY name"

            employees = self.db_manager.fetch_all(query, params)
            return [dict(employee) for employee in employees]

        except Exception as e:
            self.logger.error(f"خطأ في جلب الموظفين: {e}")
            return []

    def deactivate_employee(self, employee_id: int) -> Dict:
        """إلغاء تفعيل موظف"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    UPDATE employees 
                    SET is_active = 0, termination_date = ?
                    WHERE id = ?
                ''', (date.today(), employee_id))

                conn.commit()

                if cursor.rowcount > 0:
                    self.logger.info(f"تم إلغاء تفعيل الموظف: {employee_id}")
                    return {
                        'success': True,
                        'message': 'تم إلغاء تفعيل الموظف بنجاح'
                    }
                else:
                    return {
                        'success': False,
                        'errors': ['الموظف غير موجود']
                    }

        except Exception as e:
            self.logger.error(f"خطأ في إلغاء تفعيل الموظف: {e}")
            return {
                'success': False,
                'errors': [f'خطأ في إلغاء تفعيل الموظف: {str(e)}']
            }

    def get_employees_by_department(self, department: str) -> List[Dict]:
        """جلب الموظفين حسب القسم"""
        try:
            query = """
                SELECT * FROM employees 
                WHERE department = ? AND is_active = 1
                ORDER BY name
            """
            employees = self.db_manager.fetch_all(query, (department,))
            return [dict(employee) for employee in employees]

        except Exception as e:
            self.logger.error(f"خطأ في جلب موظفي القسم: {e}")
            return []

    def search_employees(self, search_term: str) -> List[Dict]:
        """البحث في الموظفين"""
        try:
            query = """
                SELECT * FROM employees 
                WHERE (name LIKE ? OR position LIKE ? OR department LIKE ?)
                AND is_active = 1
                ORDER BY name
            """
            search_pattern = f"%{search_term}%"
            employees = self.db_manager.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            return [dict(employee) for employee in employees]

        except Exception as e:
            self.logger.error(f"خطأ في البحث عن الموظفين: {e}")
            return []

    def get_departments(self) -> List[str]:
        """جلب قائمة الأقسام"""
        try:
            query = """
                SELECT DISTINCT department FROM employees 
                WHERE department IS NOT NULL AND department != '' AND is_active = 1
                ORDER BY department
            """
            departments = self.db_manager.fetch_all(query)
            return [dept['department'] for dept in departments]

        except Exception as e:
            self.logger.error(f"خطأ في جلب الأقسام: {e}")
            return []

    def get_employee_statistics(self) -> Dict:
        """إحصائيات الموظفين"""
        try:
            # إجمالي الموظفين النشطين
            total_active = self.db_manager.fetch_one(
                "SELECT COUNT(*) as count FROM employees WHERE is_active = 1"
            )['count']

            # إجمالي الموظفين غير النشطين
            total_inactive = self.db_manager.fetch_one(
                "SELECT COUNT(*) as count FROM employees WHERE is_active = 0"
            )['count']

            # إجمالي الرواتب
            total_salaries = self.db_manager.fetch_one(
                "SELECT COALESCE(SUM(salary), 0) as total FROM employees WHERE is_active = 1"
            )['total']

            # متوسط الراتب
            avg_salary = self.db_manager.fetch_one(
                "SELECT COALESCE(AVG(salary), 0) as avg FROM employees WHERE is_active = 1"
            )['avg']

            # عدد الأقسام
            departments_count = len(self.get_departments())

            return {
                'total_active': total_active,
                'total_inactive': total_inactive,
                'total_employees': total_active + total_inactive,
                'total_salaries': total_salaries,
                'average_salary': avg_salary,
                'departments_count': departments_count
            }

        except Exception as e:
            self.logger.error(f"خطأ في جلب إحصائيات الموظفين: {e}")
            return {
                'total_active': 0,
                'total_inactive': 0,
                'total_employees': 0,
                'total_salaries': 0,
                'average_salary': 0,
                'departments_count': 0
            }

    def _validate_employee_data(self, employee_data: Dict) -> Dict:
        """التحقق من صحة بيانات الموظف"""
        errors = []

        # التحقق من الاسم
        if not employee_data.get('name', '').strip():
            errors.append('اسم الموظف مطلوب')

        # التحقق من الراتب
        try:
            salary = float(employee_data.get('salary', 0))
            if salary < 0:
                errors.append('الراتب لا يمكن أن يكون سالباً')
        except (ValueError, TypeError):
            errors.append('الراتب يجب أن يكون رقماً صحيحاً')

        # التحقق من البريد الإلكتروني
        email = employee_data.get('email', '').strip()
        if email and '@' not in email:
            errors.append('البريد الإلكتروني غير صحيح')

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
