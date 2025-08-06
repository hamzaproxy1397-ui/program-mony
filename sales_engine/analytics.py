# -*- coding: utf-8 -*-
"""
تحليل المبيعات المتقدم
Advanced Sales Analytics
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, date, timedelta
from collections import defaultdict, Counter
import statistics
from enum import Enum

class AnalyticsPeriod(Enum):
    """فترات التحليل"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class SalesAnalytics:
    """محلل المبيعات المتقدم"""
    
    def __init__(self, database_manager=None):
        self.db_manager = database_manager
        self.sales_data = []  # قائمة المبيعات
        self.customer_data = {}  # بيانات العملاء
        self.product_data = {}  # بيانات المنتجات
        
    def add_sale_record(self, sale_id: int, customer_id: int, 
                       products: List[Dict], sale_date: datetime,
                       total_amount: Decimal, discount_amount: Decimal = Decimal('0')):
        """إضافة سجل مبيعات للتحليل"""
        
        sale_record = {
            'sale_id': sale_id,
            'customer_id': customer_id,
            'products': products,  # [{'product_id': int, 'quantity': int, 'price': Decimal}]
            'sale_date': sale_date,
            'total_amount': total_amount,
            'discount_amount': discount_amount,
            'net_amount': total_amount - discount_amount,
            'items_count': sum(p['quantity'] for p in products)
        }
        
        self.sales_data.append(sale_record)
        
        # تحديث بيانات العميل
        if customer_id not in self.customer_data:
            self.customer_data[customer_id] = {
                'total_purchases': 0,
                'total_spent': Decimal('0'),
                'first_purchase': sale_date,
                'last_purchase': sale_date,
                'purchase_frequency': 0
            }
        
        customer = self.customer_data[customer_id]
        customer['total_purchases'] += 1
        customer['total_spent'] += sale_record['net_amount']
        customer['last_purchase'] = max(customer['last_purchase'], sale_date)
        customer['purchase_frequency'] = customer['total_purchases']
        
        # تحديث بيانات المنتجات
        for product in products:
            product_id = product['product_id']
            if product_id not in self.product_data:
                self.product_data[product_id] = {
                    'total_sold': 0,
                    'total_revenue': Decimal('0'),
                    'sales_count': 0,
                    'avg_price': Decimal('0')
                }
            
            prod_data = self.product_data[product_id]
            prod_data['total_sold'] += product['quantity']
            prod_data['total_revenue'] += product['price'] * product['quantity']
            prod_data['sales_count'] += 1
            prod_data['avg_price'] = prod_data['total_revenue'] / prod_data['total_sold']
    
    def get_sales_summary(self, start_date: date = None, 
                         end_date: date = None) -> Dict:
        """ملخص المبيعات للفترة المحددة"""
        
        filtered_sales = self._filter_sales_by_date(start_date, end_date)
        
        if not filtered_sales:
            return {
                'total_sales': 0,
                'total_revenue': Decimal('0'),
                'total_discount': Decimal('0'),
                'net_revenue': Decimal('0'),
                'avg_order_value': Decimal('0'),
                'total_items_sold': 0,
                'unique_customers': 0
            }
        
        total_revenue = sum(sale['total_amount'] for sale in filtered_sales)
        total_discount = sum(sale['discount_amount'] for sale in filtered_sales)
        net_revenue = sum(sale['net_amount'] for sale in filtered_sales)
        total_items = sum(sale['items_count'] for sale in filtered_sales)
        unique_customers = len(set(sale['customer_id'] for sale in filtered_sales))
        
        return {
            'total_sales': len(filtered_sales),
            'total_revenue': total_revenue,
            'total_discount': total_discount,
            'net_revenue': net_revenue,
            'avg_order_value': net_revenue / len(filtered_sales),
            'total_items_sold': total_items,
            'unique_customers': unique_customers,
            'avg_items_per_order': total_items / len(filtered_sales),
            'discount_rate': (total_discount / total_revenue * 100) if total_revenue > 0 else Decimal('0')
        }
    
    def get_top_products(self, limit: int = 10, 
                        start_date: date = None, end_date: date = None,
                        sort_by: str = 'revenue') -> List[Dict]:
        """أفضل المنتجات مبيعاً"""
        
        filtered_sales = self._filter_sales_by_date(start_date, end_date)
        product_stats = defaultdict(lambda: {
            'product_id': 0,
            'quantity_sold': 0,
            'revenue': Decimal('0'),
            'sales_count': 0
        })
        
        for sale in filtered_sales:
            for product in sale['products']:
                product_id = product['product_id']
                stats = product_stats[product_id]
                stats['product_id'] = product_id
                stats['quantity_sold'] += product['quantity']
                stats['revenue'] += product['price'] * product['quantity']
                stats['sales_count'] += 1
        
        # ترتيب حسب المعيار المحدد
        if sort_by == 'quantity':
            sorted_products = sorted(product_stats.values(), 
                                   key=lambda x: x['quantity_sold'], reverse=True)
        elif sort_by == 'sales_count':
            sorted_products = sorted(product_stats.values(), 
                                   key=lambda x: x['sales_count'], reverse=True)
        else:  # revenue
            sorted_products = sorted(product_stats.values(), 
                                   key=lambda x: x['revenue'], reverse=True)
        
        return sorted_products[:limit]
    
    def get_customer_analysis(self, limit: int = 10) -> Dict:
        """تحليل العملاء"""
        
        # أفضل العملاء حسب الإنفاق
        top_customers_by_spending = sorted(
            self.customer_data.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )[:limit]
        
        # أكثر العملاء شراءً
        top_customers_by_frequency = sorted(
            self.customer_data.items(),
            key=lambda x: x[1]['total_purchases'],
            reverse=True
        )[:limit]
        
        # إحصائيات عامة
        if self.customer_data:
            avg_customer_value = statistics.mean(
                [data['total_spent'] for data in self.customer_data.values()]
            )
            avg_purchase_frequency = statistics.mean(
                [data['total_purchases'] for data in self.customer_data.values()]
            )
        else:
            avg_customer_value = Decimal('0')
            avg_purchase_frequency = 0
        
        return {
            'total_customers': len(self.customer_data),
            'avg_customer_value': avg_customer_value,
            'avg_purchase_frequency': avg_purchase_frequency,
            'top_customers_by_spending': [
                {
                    'customer_id': customer_id,
                    'total_spent': data['total_spent'],
                    'total_purchases': data['total_purchases']
                }
                for customer_id, data in top_customers_by_spending
            ],
            'top_customers_by_frequency': [
                {
                    'customer_id': customer_id,
                    'total_purchases': data['total_purchases'],
                    'total_spent': data['total_spent']
                }
                for customer_id, data in top_customers_by_frequency
            ]
        }
    
    def get_sales_trends(self, period: AnalyticsPeriod = AnalyticsPeriod.MONTHLY,
                        months_back: int = 12) -> List[Dict]:
        """اتجاهات المبيعات"""
        
        end_date = date.today()
        start_date = end_date - timedelta(days=months_back * 30)
        
        filtered_sales = self._filter_sales_by_date(start_date, end_date)
        
        # تجميع البيانات حسب الفترة
        period_data = defaultdict(lambda: {
            'sales_count': 0,
            'revenue': Decimal('0'),
            'items_sold': 0
        })
        
        for sale in filtered_sales:
            period_key = self._get_period_key(sale['sale_date'], period)
            period_data[period_key]['sales_count'] += 1
            period_data[period_key]['revenue'] += sale['net_amount']
            period_data[period_key]['items_sold'] += sale['items_count']
        
        # تحويل إلى قائمة مرتبة
        trends = []
        for period_key in sorted(period_data.keys()):
            data = period_data[period_key]
            trends.append({
                'period': period_key,
                'sales_count': data['sales_count'],
                'revenue': data['revenue'],
                'items_sold': data['items_sold'],
                'avg_order_value': data['revenue'] / data['sales_count'] if data['sales_count'] > 0 else Decimal('0')
            })
        
        return trends
    
    def get_seasonal_analysis(self) -> Dict:
        """تحليل الموسمية"""
        
        monthly_sales = defaultdict(lambda: {'count': 0, 'revenue': Decimal('0')})
        daily_sales = defaultdict(lambda: {'count': 0, 'revenue': Decimal('0')})
        hourly_sales = defaultdict(lambda: {'count': 0, 'revenue': Decimal('0')})
        
        for sale in self.sales_data:
            sale_date = sale['sale_date']
            
            # تحليل شهري
            month_key = sale_date.strftime('%m')
            monthly_sales[month_key]['count'] += 1
            monthly_sales[month_key]['revenue'] += sale['net_amount']
            
            # تحليل يومي (أيام الأسبوع)
            day_key = sale_date.strftime('%A')
            daily_sales[day_key]['count'] += 1
            daily_sales[day_key]['revenue'] += sale['net_amount']
            
            # تحليل ساعي
            hour_key = sale_date.strftime('%H')
            hourly_sales[hour_key]['count'] += 1
            hourly_sales[hour_key]['revenue'] += sale['net_amount']
        
        return {
            'monthly_patterns': dict(monthly_sales),
            'daily_patterns': dict(daily_sales),
            'hourly_patterns': dict(hourly_sales)
        }
    
    def get_cohort_analysis(self, months: int = 6) -> Dict:
        """تحليل الأفواج (Cohort Analysis)"""
        
        # تجميع العملاء حسب شهر أول شراء
        cohorts = defaultdict(list)
        
        for customer_id, data in self.customer_data.items():
            first_purchase_month = data['first_purchase'].strftime('%Y-%m')
            cohorts[first_purchase_month].append(customer_id)
        
        # تحليل الاحتفاظ بالعملاء
        cohort_analysis = {}
        
        for cohort_month, customer_ids in cohorts.items():
            cohort_analysis[cohort_month] = {
                'initial_customers': len(customer_ids),
                'retention_rates': {}
            }
            
            # حساب معدلات الاحتفاظ لكل شهر
            for month_offset in range(1, months + 1):
                target_month = datetime.strptime(cohort_month, '%Y-%m') + timedelta(days=month_offset * 30)
                
                active_customers = 0
                for customer_id in customer_ids:
                    customer_sales = [
                        sale for sale in self.sales_data 
                        if (sale['customer_id'] == customer_id and 
                            sale['sale_date'].year == target_month.year and
                            sale['sale_date'].month == target_month.month)
                    ]
                    if customer_sales:
                        active_customers += 1
                
                retention_rate = (active_customers / len(customer_ids)) * 100
                cohort_analysis[cohort_month]['retention_rates'][f'month_{month_offset}'] = round(retention_rate, 2)
        
        return cohort_analysis
    
    def _filter_sales_by_date(self, start_date: date = None, 
                             end_date: date = None) -> List[Dict]:
        """تصفية المبيعات حسب التاريخ"""
        
        if start_date is None and end_date is None:
            return self.sales_data
        
        filtered = []
        for sale in self.sales_data:
            sale_date = sale['sale_date'].date()
            
            if start_date and sale_date < start_date:
                continue
            if end_date and sale_date > end_date:
                continue
                
            filtered.append(sale)
        
        return filtered
    
    def _get_period_key(self, date_obj: datetime, period: AnalyticsPeriod) -> str:
        """الحصول على مفتاح الفترة"""
        
        if period == AnalyticsPeriod.DAILY:
            return date_obj.strftime('%Y-%m-%d')
        elif period == AnalyticsPeriod.WEEKLY:
            year, week, _ = date_obj.isocalendar()
            return f'{year}-W{week:02d}'
        elif period == AnalyticsPeriod.MONTHLY:
            return date_obj.strftime('%Y-%m')
        elif period == AnalyticsPeriod.QUARTERLY:
            quarter = (date_obj.month - 1) // 3 + 1
            return f'{date_obj.year}-Q{quarter}'
        elif period == AnalyticsPeriod.YEARLY:
            return str(date_obj.year)
        
        return date_obj.strftime('%Y-%m-%d')
    
    def export_analytics_report(self, file_path: str, 
                               start_date: date = None, 
                               end_date: date = None) -> bool:
        """تصدير تقرير التحليلات"""
        
        try:
            report = {
                'report_date': datetime.now().isoformat(),
                'period': {
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None
                },
                'sales_summary': self.get_sales_summary(start_date, end_date),
                'top_products': self.get_top_products(20, start_date, end_date),
                'customer_analysis': self.get_customer_analysis(20),
                'seasonal_analysis': self.get_seasonal_analysis(),
                'sales_trends': self.get_sales_trends()
            }
            
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            
            return True
            
        except Exception as e:
            print(f"خطأ في تصدير تقرير التحليلات: {e}")
            return False
