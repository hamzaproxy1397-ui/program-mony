# -*- coding: utf-8 -*-
"""
محرك التحليلات المتقدم - نظام الرسوم البيانية والتحليلات
Advanced Analytics Engine - Charts and Analytics System
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from decimal import Decimal
from pathlib import Path
import tempfile
import base64
from io import BytesIO

# محاولة استيراد مكتبات الرسوم البيانية
try:
    import matplotlib
    matplotlib.use('Agg')  # استخدام backend غير تفاعلي
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle
    plt.rcParams['font.family'] = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans']
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class AdvancedAnalyticsEngine:
    """محرك التحليلات المتقدم"""
    
    def __init__(self, db_connection=None):
        self.db_connection = db_connection
        self.project_root = Path(__file__).parent.parent
        self.charts_dir = self.project_root / "temp" / "charts"
        self.charts_dir.mkdir(parents=True, exist_ok=True)
        
        # إعدادات الرسوم البيانية
        self.chart_config = {
            'figsize': (12, 8),
            'dpi': 100,
            'style': 'seaborn-v0_8',
            'colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4CAF50', '#FF9800'],
            'rtl_support': True
        }
        
        # إعداد matplotlib للعربية
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('default')
            plt.rcParams['figure.figsize'] = self.chart_config['figsize']
            plt.rcParams['figure.dpi'] = self.chart_config['dpi']
            plt.rcParams['axes.unicode_minus'] = False
    
    def generate_sales_trend_chart(self, days: int = 30) -> Dict[str, Any]:
        """إنشاء رسم بياني لاتجاه المبيعات"""
        if not MATPLOTLIB_AVAILABLE or not self.db_connection:
            return {'error': 'المكتبات المطلوبة غير متوفرة'}
        
        try:
            # الحصول على بيانات المبيعات
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT DATE(created_at) as sale_date,
                       SUM(quantity * unit_cost) as daily_revenue,
                       SUM(quantity) as daily_quantity,
                       COUNT(DISTINCT item_id) as items_sold
                FROM inventory_movements
                WHERE movement_type = 'out' 
                      AND created_at BETWEEN ? AND ?
                GROUP BY DATE(created_at)
                ORDER BY sale_date
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            data = cursor.fetchall()
            
            if not data:
                return {'error': 'لا توجد بيانات مبيعات للفترة المحددة'}
            
            # تحضير البيانات
            dates = [datetime.strptime(row['sale_date'], '%Y-%m-%d') for row in data]
            revenues = [float(row['daily_revenue'] or 0) for row in data]
            quantities = [float(row['daily_quantity'] or 0) for row in data]
            
            # إنشاء الرسم البياني
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.chart_config['figsize'])
            
            # رسم الإيرادات
            ax1.plot(dates, revenues, color=self.chart_config['colors'][0], 
                    linewidth=2, marker='o', markersize=4)
            ax1.set_title('اتجاه الإيرادات اليومية', fontsize=14, fontweight='bold')
            ax1.set_ylabel('الإيرادات (ريال)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
            
            # رسم الكميات
            ax2.bar(dates, quantities, color=self.chart_config['colors'][1], alpha=0.7)
            ax2.set_title('الكميات المباعة يومياً', fontsize=14, fontweight='bold')
            ax2.set_ylabel('الكمية', fontsize=12)
            ax2.set_xlabel('التاريخ', fontsize=12)
            ax2.grid(True, alpha=0.3)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax2.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # حفظ الرسم
            chart_path = self.charts_dir / f"sales_trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            
            # حساب الإحصائيات
            total_revenue = sum(revenues)
            avg_daily_revenue = total_revenue / len(revenues) if revenues else 0
            total_quantity = sum(quantities)
            
            return {
                'chart_path': str(chart_path),
                'statistics': {
                    'total_revenue': round(total_revenue, 2),
                    'avg_daily_revenue': round(avg_daily_revenue, 2),
                    'total_quantity': round(total_quantity, 2),
                    'days_analyzed': len(data),
                    'best_day': {
                        'date': dates[revenues.index(max(revenues))].strftime('%Y-%m-%d'),
                        'revenue': max(revenues)
                    } if revenues else None
                }
            }
            
        except Exception as e:
            return {'error': f'خطأ في إنشاء رسم المبيعات: {e}'}
    
    def generate_category_distribution_chart(self) -> Dict[str, Any]:
        """إنشاء رسم بياني لتوزيع الأصناف حسب الفئات"""
        if not MATPLOTLIB_AVAILABLE or not self.db_connection:
            return {'error': 'المكتبات المطلوبة غير متوفرة'}
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT c.name as category_name,
                       COUNT(i.id) as item_count,
                       SUM(i.current_stock * i.selling_price) as category_value
                FROM categories c
                LEFT JOIN items i ON c.id = i.category_id AND i.is_active = 1
                GROUP BY c.id, c.name
                HAVING item_count > 0
                ORDER BY item_count DESC
            ''')
            
            data = cursor.fetchall()
            
            if not data:
                return {'error': 'لا توجد بيانات فئات'}
            
            # تحضير البيانات
            categories = [row['category_name'] for row in data]
            counts = [row['item_count'] for row in data]
            values = [float(row['category_value'] or 0) for row in data]
            
            # إنشاء الرسم البياني
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # رسم دائري لعدد الأصناف
            colors = self.chart_config['colors'][:len(categories)]
            wedges, texts, autotexts = ax1.pie(counts, labels=categories, colors=colors,
                                              autopct='%1.1f%%', startangle=90)
            ax1.set_title('توزيع الأصناف حسب الفئات', fontsize=14, fontweight='bold')
            
            # رسم عمودي للقيم
            bars = ax2.bar(categories, values, color=colors)
            ax2.set_title('قيمة المخزون حسب الفئات', fontsize=14, fontweight='bold')
            ax2.set_ylabel('القيمة (ريال)', fontsize=12)
            ax2.set_xlabel('الفئات', fontsize=12)
            ax2.tick_params(axis='x', rotation=45)
            
            # إضافة قيم على الأعمدة
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:,.0f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # حفظ الرسم
            chart_path = self.charts_dir / f"category_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            
            return {
                'chart_path': str(chart_path),
                'statistics': {
                    'total_categories': len(categories),
                    'total_items': sum(counts),
                    'total_value': round(sum(values), 2),
                    'top_category': {
                        'name': categories[0],
                        'count': counts[0],
                        'percentage': round((counts[0] / sum(counts)) * 100, 1)
                    } if categories else None
                }
            }
            
        except Exception as e:
            return {'error': f'خطأ في إنشاء رسم التوزيع: {e}'}
    
    def generate_profit_analysis_chart(self, days: int = 30) -> Dict[str, Any]:
        """إنشاء رسم بياني لتحليل الربحية"""
        if not MATPLOTLIB_AVAILABLE or not self.db_connection:
            return {'error': 'المكتبات المطلوبة غير متوفرة'}
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT i.name as item_name,
                       SUM(im.quantity) as total_sold,
                       AVG(i.selling_price - i.cost_price) as avg_profit_per_unit,
                       SUM(im.quantity * (i.selling_price - i.cost_price)) as total_profit
                FROM inventory_movements im
                JOIN items i ON im.item_id = i.id
                WHERE im.movement_type = 'out' 
                      AND im.created_at BETWEEN ? AND ?
                      AND i.selling_price > 0 AND i.cost_price > 0
                GROUP BY i.id, i.name
                HAVING total_sold > 0
                ORDER BY total_profit DESC
                LIMIT 10
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            data = cursor.fetchall()
            
            if not data:
                return {'error': 'لا توجد بيانات ربحية للفترة المحددة'}
            
            # تحضير البيانات
            items = [row['item_name'][:20] + '...' if len(row['item_name']) > 20 
                    else row['item_name'] for row in data]
            profits = [float(row['total_profit'] or 0) for row in data]
            quantities = [float(row['total_sold'] or 0) for row in data]
            
            # إنشاء الرسم البياني
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # رسم عمودي للأرباح
            bars = ax.bar(items, profits, color=self.chart_config['colors'][2])
            ax.set_title('تحليل الربحية - أفضل 10 أصناف', fontsize=16, fontweight='bold')
            ax.set_ylabel('إجمالي الربح (ريال)', fontsize=12)
            ax.set_xlabel('الأصناف', fontsize=12)
            
            # إضافة قيم على الأعمدة
            for bar, profit in zip(bars, profits):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{profit:,.0f}', ha='center', va='bottom', fontsize=10)
            
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            
            # حفظ الرسم
            chart_path = self.charts_dir / f"profit_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            
            return {
                'chart_path': str(chart_path),
                'statistics': {
                    'total_profit': round(sum(profits), 2),
                    'avg_profit_per_item': round(sum(profits) / len(profits), 2),
                    'best_performer': {
                        'name': data[0]['item_name'],
                        'profit': round(float(data[0]['total_profit']), 2),
                        'quantity_sold': float(data[0]['total_sold'])
                    } if data else None,
                    'items_analyzed': len(data)
                }
            }
            
        except Exception as e:
            return {'error': f'خطأ في إنشاء رسم الربحية: {e}'}
    
    def generate_inventory_status_chart(self) -> Dict[str, Any]:
        """إنشاء رسم بياني لحالة المخزون"""
        if not MATPLOTLIB_AVAILABLE or not self.db_connection:
            return {'error': 'المكتبات المطلوبة غير متوفرة'}
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT 
                    name,
                    current_stock,
                    min_stock_level,
                    reorder_point,
                    CASE 
                        WHEN current_stock <= 0 THEN 'نفد المخزون'
                        WHEN current_stock <= min_stock_level THEN 'مخزون منخفض'
                        WHEN current_stock <= reorder_point THEN 'يحتاج إعادة طلب'
                        ELSE 'مخزون جيد'
                    END as stock_status
                FROM items 
                WHERE is_active = 1 AND is_trackable = 1
                ORDER BY current_stock ASC
                LIMIT 20
            ''')
            
            data = cursor.fetchall()
            
            if not data:
                return {'error': 'لا توجد بيانات مخزون'}
            
            # تجميع البيانات حسب الحالة
            status_counts = {}
            for row in data:
                status = row['stock_status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # إنشاء الرسم البياني
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # رسم دائري لحالة المخزون
            statuses = list(status_counts.keys())
            counts = list(status_counts.values())
            colors = ['#F44336', '#FF9800', '#FFC107', '#4CAF50'][:len(statuses)]
            
            ax1.pie(counts, labels=statuses, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('توزيع حالة المخزون', fontsize=14, fontweight='bold')
            
            # رسم عمودي لمستويات المخزون
            items = [row['name'][:15] + '...' if len(row['name']) > 15 
                    else row['name'] for row in data[:10]]
            current_stocks = [float(row['current_stock']) for row in data[:10]]
            min_levels = [float(row['min_stock_level'] or 0) for row in data[:10]]
            
            x = range(len(items))
            ax2.bar(x, current_stocks, label='المخزون الحالي', color=self.chart_config['colors'][0])
            ax2.bar(x, min_levels, label='الحد الأدنى', color=self.chart_config['colors'][1], alpha=0.7)
            
            ax2.set_title('مستويات المخزون - أقل 10 أصناف', fontsize=14, fontweight='bold')
            ax2.set_ylabel('الكمية', fontsize=12)
            ax2.set_xlabel('الأصناف', fontsize=12)
            ax2.set_xticks(x)
            ax2.set_xticklabels(items, rotation=45, ha='right')
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            
            # حفظ الرسم
            chart_path = self.charts_dir / f"inventory_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_path, dpi=self.chart_config['dpi'], bbox_inches='tight')
            plt.close()
            
            return {
                'chart_path': str(chart_path),
                'statistics': {
                    'total_items_tracked': len(data),
                    'status_breakdown': status_counts,
                    'critical_items': status_counts.get('نفد المخزون', 0) + 
                                    status_counts.get('مخزون منخفض', 0),
                    'reorder_needed': status_counts.get('يحتاج إعادة طلب', 0)
                }
            }
            
        except Exception as e:
            return {'error': f'خطأ في إنشاء رسم المخزون: {e}'}

def main():
    """اختبار محرك التحليلات"""
    print("📊 اختبار محرك التحليلات المتقدم...")
    
    if not MATPLOTLIB_AVAILABLE:
        print("❌ matplotlib غير متوفر - لا يمكن إنشاء الرسوم البيانية")
        return
    
    analytics = AdvancedAnalyticsEngine()
    
    print("✅ تم إنشاء محرك التحليلات بنجاح")
    print(f"📁 مجلد الرسوم البيانية: {analytics.charts_dir}")
    
    # اختبار إنشاء رسم بياني بسيط
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3], marker='o')
        ax.set_title('اختبار الرسم البياني', fontsize=14)
        ax.set_xlabel('المحور السيني')
        ax.set_ylabel('المحور الصادي')
        
        test_chart = analytics.charts_dir / "test_chart.png"
        plt.savefig(test_chart, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✅ تم إنشاء رسم بياني تجريبي: {test_chart}")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الرسم التجريبي: {e}")
    
    print("\n🎉 تم اختبار محرك التحليلات بنجاح!")

if __name__ == "__main__":
    main()
