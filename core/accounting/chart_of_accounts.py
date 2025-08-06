# -*- coding: utf-8 -*-
"""
دليل الحسابات
Chart of Accounts Management
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
from enum import Enum

class AccountType(Enum):
    """أنواع الحسابات"""
    ASSET = "asset"  # أصول
    LIABILITY = "liability"  # خصوم
    EQUITY = "equity"  # حقوق الملكية
    REVENUE = "revenue"  # إيرادات
    EXPENSE = "expense"  # مصروفات

class AccountCategory(Enum):
    """فئات الحسابات"""
    # الأصول
    CURRENT_ASSETS = "current_assets"  # أصول متداولة
    FIXED_ASSETS = "fixed_assets"  # أصول ثابتة
    
    # الخصوم
    CURRENT_LIABILITIES = "current_liabilities"  # خصوم متداولة
    LONG_TERM_LIABILITIES = "long_term_liabilities"  # خصوم طويلة الأجل
    
    # حقوق الملكية
    CAPITAL = "capital"  # رأس المال
    RETAINED_EARNINGS = "retained_earnings"  # أرباح محتجزة
    
    # الإيرادات
    SALES_REVENUE = "sales_revenue"  # إيرادات المبيعات
    OTHER_REVENUE = "other_revenue"  # إيرادات أخرى
    
    # المصروفات
    COST_OF_GOODS_SOLD = "cost_of_goods_sold"  # تكلفة البضاعة المباعة
    OPERATING_EXPENSES = "operating_expenses"  # مصروفات تشغيلية
    ADMINISTRATIVE_EXPENSES = "administrative_expenses"  # مصروفات إدارية

class ChartOfAccounts:
    """مدير دليل الحسابات"""
    
    def __init__(self, database_manager=None):
        self.db_manager = database_manager
        self.accounts = {}  # account_code -> account_data
        self.account_hierarchy = {}  # parent_code -> [child_codes]
        self._initialize_default_accounts()
    
    def _initialize_default_accounts(self):
        """تهيئة الحسابات الافتراضية"""
        
        # الحسابات الرئيسية
        default_accounts = [
            # الأصول (1000-1999)
            {
                'code': '1000',
                'name': 'الأصول',
                'type': AccountType.ASSET,
                'category': None,
                'parent_code': None,
                'is_header': True
            },
            {
                'code': '1100',
                'name': 'الأصول المتداولة',
                'type': AccountType.ASSET,
                'category': AccountCategory.CURRENT_ASSETS,
                'parent_code': '1000',
                'is_header': True
            },
            {
                'code': '1110',
                'name': 'النقدية والبنوك',
                'type': AccountType.ASSET,
                'category': AccountCategory.CURRENT_ASSETS,
                'parent_code': '1100',
                'is_header': False
            },
            {
                'code': '1120',
                'name': 'العملاء',
                'type': AccountType.ASSET,
                'category': AccountCategory.CURRENT_ASSETS,
                'parent_code': '1100',
                'is_header': False
            },
            {
                'code': '1130',
                'name': 'المخزون',
                'type': AccountType.ASSET,
                'category': AccountCategory.CURRENT_ASSETS,
                'parent_code': '1100',
                'is_header': False
            },
            
            # الأصول الثابتة
            {
                'code': '1200',
                'name': 'الأصول الثابتة',
                'type': AccountType.ASSET,
                'category': AccountCategory.FIXED_ASSETS,
                'parent_code': '1000',
                'is_header': True
            },
            {
                'code': '1210',
                'name': 'الأراضي والمباني',
                'type': AccountType.ASSET,
                'category': AccountCategory.FIXED_ASSETS,
                'parent_code': '1200',
                'is_header': False
            },
            {
                'code': '1220',
                'name': 'المعدات والآلات',
                'type': AccountType.ASSET,
                'category': AccountCategory.FIXED_ASSETS,
                'parent_code': '1200',
                'is_header': False
            },
            
            # الخصوم (2000-2999)
            {
                'code': '2000',
                'name': 'الخصوم',
                'type': AccountType.LIABILITY,
                'category': None,
                'parent_code': None,
                'is_header': True
            },
            {
                'code': '2100',
                'name': 'الخصوم المتداولة',
                'type': AccountType.LIABILITY,
                'category': AccountCategory.CURRENT_LIABILITIES,
                'parent_code': '2000',
                'is_header': True
            },
            {
                'code': '2110',
                'name': 'الموردون',
                'type': AccountType.LIABILITY,
                'category': AccountCategory.CURRENT_LIABILITIES,
                'parent_code': '2100',
                'is_header': False
            },
            {
                'code': '2120',
                'name': 'ضريبة القيمة المضافة',
                'type': AccountType.LIABILITY,
                'category': AccountCategory.CURRENT_LIABILITIES,
                'parent_code': '2100',
                'is_header': False
            },
            
            # حقوق الملكية (3000-3999)
            {
                'code': '3000',
                'name': 'حقوق الملكية',
                'type': AccountType.EQUITY,
                'category': None,
                'parent_code': None,
                'is_header': True
            },
            {
                'code': '3100',
                'name': 'رأس المال',
                'type': AccountType.EQUITY,
                'category': AccountCategory.CAPITAL,
                'parent_code': '3000',
                'is_header': False
            },
            {
                'code': '3200',
                'name': 'الأرباح المحتجزة',
                'type': AccountType.EQUITY,
                'category': AccountCategory.RETAINED_EARNINGS,
                'parent_code': '3000',
                'is_header': False
            },
            
            # الإيرادات (4000-4999)
            {
                'code': '4000',
                'name': 'الإيرادات',
                'type': AccountType.REVENUE,
                'category': None,
                'parent_code': None,
                'is_header': True
            },
            {
                'code': '4100',
                'name': 'إيرادات المبيعات',
                'type': AccountType.REVENUE,
                'category': AccountCategory.SALES_REVENUE,
                'parent_code': '4000',
                'is_header': False
            },
            {
                'code': '4200',
                'name': 'إيرادات أخرى',
                'type': AccountType.REVENUE,
                'category': AccountCategory.OTHER_REVENUE,
                'parent_code': '4000',
                'is_header': False
            },
            
            # المصروفات (5000-5999)
            {
                'code': '5000',
                'name': 'المصروفات',
                'type': AccountType.EXPENSE,
                'category': None,
                'parent_code': None,
                'is_header': True
            },
            {
                'code': '5100',
                'name': 'تكلفة البضاعة المباعة',
                'type': AccountType.EXPENSE,
                'category': AccountCategory.COST_OF_GOODS_SOLD,
                'parent_code': '5000',
                'is_header': False
            },
            {
                'code': '5200',
                'name': 'مصروفات تشغيلية',
                'type': AccountType.EXPENSE,
                'category': AccountCategory.OPERATING_EXPENSES,
                'parent_code': '5000',
                'is_header': True
            },
            {
                'code': '5210',
                'name': 'رواتب وأجور',
                'type': AccountType.EXPENSE,
                'category': AccountCategory.OPERATING_EXPENSES,
                'parent_code': '5200',
                'is_header': False
            },
            {
                'code': '5220',
                'name': 'إيجارات',
                'type': AccountType.EXPENSE,
                'category': AccountCategory.OPERATING_EXPENSES,
                'parent_code': '5200',
                'is_header': False
            }
        ]
        
        for account in default_accounts:
            self.add_account(**account)
    
    def add_account(self, code: str, name: str, account_type: AccountType,
                   category: Optional[AccountCategory] = None,
                   parent_code: Optional[str] = None,
                   is_header: bool = False,
                   description: str = "") -> bool:
        """إضافة حساب جديد"""
        
        if code in self.accounts:
            return False  # الحساب موجود بالفعل
        
        account = {
            'code': code,
            'name': name,
            'type': account_type,
            'category': category,
            'parent_code': parent_code,
            'is_header': is_header,
            'description': description,
            'balance': Decimal('0'),
            'created_date': datetime.now(),
            'is_active': True
        }
        
        self.accounts[code] = account
        
        # تحديث التسلسل الهرمي
        if parent_code:
            if parent_code not in self.account_hierarchy:
                self.account_hierarchy[parent_code] = []
            self.account_hierarchy[parent_code].append(code)
        
        return True
    
    def get_account(self, code: str) -> Optional[Dict]:
        """الحصول على بيانات حساب"""
        return self.accounts.get(code)
    
    def get_accounts_by_type(self, account_type: AccountType) -> List[Dict]:
        """الحصول على الحسابات حسب النوع"""
        return [
            account for account in self.accounts.values()
            if account['type'] == account_type and account['is_active']
        ]
    
    def get_accounts_by_category(self, category: AccountCategory) -> List[Dict]:
        """الحصول على الحسابات حسب الفئة"""
        return [
            account for account in self.accounts.values()
            if account['category'] == category and account['is_active']
        ]
    
    def get_child_accounts(self, parent_code: str) -> List[Dict]:
        """الحصول على الحسابات الفرعية"""
        child_codes = self.account_hierarchy.get(parent_code, [])
        return [self.accounts[code] for code in child_codes if code in self.accounts]
    
    def get_account_hierarchy(self, root_code: Optional[str] = None) -> Dict:
        """الحصول على التسلسل الهرمي للحسابات"""
        
        def build_tree(code):
            account = self.accounts.get(code)
            if not account:
                return None
            
            tree = {
                'account': account,
                'children': []
            }
            
            child_codes = self.account_hierarchy.get(code, [])
            for child_code in child_codes:
                child_tree = build_tree(child_code)
                if child_tree:
                    tree['children'].append(child_tree)
            
            return tree
        
        if root_code:
            return build_tree(root_code)
        else:
            # إرجاع جميع الحسابات الجذرية
            root_accounts = [
                code for code, account in self.accounts.items()
                if account['parent_code'] is None
            ]
            
            return {
                'roots': [build_tree(code) for code in root_accounts]
            }
    
    def update_account_balance(self, code: str, amount: Decimal, 
                              is_debit: bool = True) -> bool:
        """تحديث رصيد الحساب"""
        
        if code not in self.accounts:
            return False
        
        account = self.accounts[code]
        account_type = account['type']
        
        # تحديد طبيعة الحساب (مدين أم دائن)
        if account_type in [AccountType.ASSET, AccountType.EXPENSE]:
            # الأصول والمصروفات طبيعتها مدينة
            if is_debit:
                account['balance'] += amount
            else:
                account['balance'] -= amount
        else:
            # الخصوم وحقوق الملكية والإيرادات طبيعتها دائنة
            if is_debit:
                account['balance'] -= amount
            else:
                account['balance'] += amount
        
        return True
    
    def get_trial_balance(self) -> List[Dict]:
        """إعداد ميزان المراجعة"""
        
        trial_balance = []
        
        for code, account in self.accounts.items():
            if not account['is_header'] and account['is_active']:
                balance = account['balance']
                
                # تحديد الجانب (مدين أم دائن)
                if account['type'] in [AccountType.ASSET, AccountType.EXPENSE]:
                    debit_balance = balance if balance >= 0 else Decimal('0')
                    credit_balance = abs(balance) if balance < 0 else Decimal('0')
                else:
                    debit_balance = abs(balance) if balance < 0 else Decimal('0')
                    credit_balance = balance if balance >= 0 else Decimal('0')
                
                trial_balance.append({
                    'code': code,
                    'name': account['name'],
                    'type': account['type'].value,
                    'debit_balance': debit_balance,
                    'credit_balance': credit_balance
                })
        
        return trial_balance
