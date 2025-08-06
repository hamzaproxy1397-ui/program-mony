# -*- coding: utf-8 -*-
"""
مولد التقارير
"""

import os
from datetime import datetime, timedelta
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager
import arabic_reshaper
from bidi.algorithm import get_display

from database.database_manager import DatabaseManager
from config.settings import REPORTS_PATH

class ReportGenerator:
    """مولد التقارير"""

    def __init__(self):
        self.db = DatabaseManager()
        self.reports_path = REPORTS_PATH
        self.setup_fonts()

    def setup_fonts(self):
        """إعداد الخطوط العربية"""
        try:
            # البحث عن خط عربي متاح
            arabic_fonts = ['Cairo', 'Amiri', 'Scheherazade', 'Arial Unicode MS']
            self.arabic_font = None

            for font_name in arabic_fonts:
                try:
                    font_path = font_manager.findfont(font_name)
                    if font_path:
                        self.arabic_font = font_name
                        break
                except:
                    continue

            if not self.arabic_font:
                self.arabic_font = 'DejaVu Sans'  # خط احتياطي

        except Exception as e:
            print(f"خطأ في إعداد الخطوط: {e}")
            self.arabic_font = 'DejaVu Sans'

    def format_arabic_text(self, text):
        """تنسيق النص العربي للعرض الصحيح"""
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        except:
            return text

    def generate_sales_report(self, start_date=None, end_date=None, format_type='PDF'):
        """إنشاء تقرير المبيعات"""
        try:
            # تحديد التواريخ الافتراضية
            if not end_date:
                end_date = datetime.now()
            if not start_date:
                start_date = end_date - timedelta(days=30)

            # جلب بيانات المبيعات
            query = '''
                SELECT 
                    si.invoice_number,
                    si.invoice_date,
                    c.name as customer_name,
                    si.total_amount,
                    si.discount_amount,
                    si.tax_amount,
                    si.net_amount,
                    si.payment_status
                FROM sales_invoices si
                LEFT JOIN customers c ON si.customer_id = c.id
                WHERE si.invoice_date BETWEEN ? AND ?
                ORDER BY si.invoice_date DESC
            '''

            results = self.db.fetch_all(query, (start_date, end_date))

            if not results:
                return None, "لا توجد بيانات للفترة المحددة"

            # تحويل إلى DataFrame
            df = pd.DataFrame([dict(row) for row in results])

            # إنشاء التقرير حسب النوع المطلوب
            if format_type.upper() == 'PDF':
                return self.create_sales_pdf_report(df, start_date, end_date)
            elif format_type.upper() == 'EXCEL':
                return self.create_sales_excel_report(df, start_date, end_date)
            else:
                return None, "نوع التقرير غير مدعوم"

        except Exception as e:
            return None, f"خطأ في إنشاء تقرير المبيعات: {e}"

    def create_sales_pdf_report(self, df, start_date, end_date):
        """إنشاء تقرير المبيعات PDF"""
        try:
            # اسم الملف
            filename = f"sales_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pdf"
            filepath = self.reports_path / filename

            # إنشاء المستند
            doc = SimpleDocTemplate(str(filepath), pagesize=A4, rightMargin=72, leftMargin=72,
                                  topMargin=72, bottomMargin=18)

            # قائمة العناصر
            story = []
            styles = getSampleStyleSheet()

            # عنوان التقرير
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=2,  # محاذاة يمين
                fontName='Helvetica-Bold'
            )

            title = Paragraph(self.format_arabic_text("تقرير المبيعات"), title_style)
            story.append(title)

            # فترة التقرير
            period_text = f"من {start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}"
            period = Paragraph(self.format_arabic_text(period_text), styles['Normal'])
            story.append(period)
            story.append(Spacer(1, 20))

            # إحصائيات سريعة
            total_sales = df['net_amount'].sum()
            total_invoices = len(df)
            avg_invoice = df['net_amount'].mean()

            stats_data = [
                [self.format_arabic_text("إجمالي المبيعات"), f"{total_sales:,.2f} ر.س"],
                [self.format_arabic_text("عدد الفواتير"), str(total_invoices)],
                [self.format_arabic_text("متوسط الفاتورة"), f"{avg_invoice:,.2f} ر.س"]
            ]

            stats_table = Table(stats_data, colWidths=[200, 150])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(stats_table)
            story.append(Spacer(1, 30))

            # جدول تفاصيل الفواتير
            table_data = [[
                self.format_arabic_text("رقم الفاتورة"),
                self.format_arabic_text("التاريخ"),
                self.format_arabic_text("العميل"),
                self.format_arabic_text("المبلغ الصافي"),
                self.format_arabic_text("الحالة")
            ]]

            for _, row in df.iterrows():
                table_data.append([
                    row['invoice_number'],
                    row['invoice_date'][:10] if row['invoice_date'] else '',
                    self.format_arabic_text(row['customer_name'] or 'غير محدد'),
                    f"{row['net_amount']:,.2f}",
                    self.format_arabic_text('مدفوع' if row['payment_status'] == 'paid' else 'معلق')
                ])

            # إنشاء الجدول
            table = Table(table_data, colWidths=[80, 80, 120, 80, 60])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))

            story.append(table)

            # بناء المستند
            doc.build(story)

            return str(filepath), "تم إنشاء التقرير بنجاح"

        except Exception as e:
            return None, f"خطأ في إنشاء تقرير PDF: {e}"

    def create_sales_excel_report(self, df, start_date, end_date):
        """إنشاء تقرير المبيعات Excel"""
        try:
            # اسم الملف
            filename = f"sales_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx"
            filepath = self.reports_path / filename

            # إنشاء كاتب Excel
            with pd.ExcelWriter(str(filepath), engine='openpyxl') as writer:
                # ورقة البيانات الرئيسية
                df_display = df.copy()
                df_display.columns = [
                    'رقم الفاتورة', 'التاريخ', 'العميل', 'المبلغ الإجمالي',
                    'الخصم', 'الضريبة', 'المبلغ الصافي', 'حالة الدفع'
                ]

                df_display.to_excel(writer, sheet_name='تفاصيل المبيعات', index=False)

                # ورقة الإحصائيات
                stats_df = pd.DataFrame({
                    'المؤشر': ['إجمالي المبيعات', 'عدد الفواتير', 'متوسط الفاتورة'],
                    'القيمة': [
                        f"{df['net_amount'].sum():,.2f} ر.س",
                        str(len(df)),
                        f"{df['net_amount'].mean():,.2f} ر.س"
                    ]
                })

                stats_df.to_excel(writer, sheet_name='الإحصائيات', index=False)

                # ورقة المبيعات اليومية
                df['invoice_date'] = pd.to_datetime(df['invoice_date'])
                daily_sales = df.groupby(df['invoice_date'].dt.date)['net_amount'].sum().reset_index()
                daily_sales.columns = ['التاريخ', 'إجمالي المبيعات']
                daily_sales.to_excel(writer, sheet_name='المبيعات اليومية', index=False)

            return str(filepath), "تم إنشاء التقرير بنجاح"

        except Exception as e:
            return None, f"خطأ في إنشاء تقرير Excel: {e}"

    def generate_inventory_report(self, format_type='PDF'):
        """إنشاء تقرير المخزون"""
        try:
            # جلب بيانات المخزون
            query = '''
                SELECT 
                    name,
                    barcode,
                    category,
                    unit,
                    current_stock,
                    min_stock,
                    cost_price,
                    selling_price,
                    (current_stock * cost_price) as stock_value
                FROM products
                WHERE is_active = 1
                ORDER BY name
            '''

            results = self.db.fetch_all(query)

            if not results:
                return None, "لا توجد منتجات في المخزون"

            # تحويل إلى DataFrame
            df = pd.DataFrame([dict(row) for row in results])

            if format_type.upper() == 'PDF':
                return self.create_inventory_pdf_report(df)
            elif format_type.upper() == 'EXCEL':
                return self.create_inventory_excel_report(df)
            else:
                return None, "نوع التقرير غير مدعوم"

        except Exception as e:
            return None, f"خطأ في إنشاء تقرير المخزون: {e}"

    def create_inventory_excel_report(self, df):
        """إنشاء تقرير المخزون Excel"""
        try:
            filename = f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = self.reports_path / filename

            with pd.ExcelWriter(str(filepath), engine='openpyxl') as writer:
                # ورقة المخزون الرئيسية
                df_display = df.copy()
                df_display.columns = [
                    'اسم المنتج', 'الباركود', 'الفئة', 'الوحدة', 'المخزون الحالي',
                    'الحد الأدنى', 'سعر التكلفة', 'سعر البيع', 'قيمة المخزون'
                ]

                df_display.to_excel(writer, sheet_name='تقرير المخزون', index=False)

                # ورقة المنتجات ناقصة المخزون
                low_stock = df[df['current_stock'] <= df['min_stock']].copy()
                if not low_stock.empty:
                    low_stock_display = low_stock[['name', 'current_stock', 'min_stock']].copy()
                    low_stock_display.columns = ['اسم المنتج', 'المخزون الحالي', 'الحد الأدنى']
                    low_stock_display.to_excel(writer, sheet_name='نقص المخزون', index=False)

                # ورقة الإحصائيات
                stats_df = pd.DataFrame({
                    'المؤشر': [
                        'إجمالي المنتجات',
                        'إجمالي قيمة المخزون',
                        'المنتجات ناقصة المخزون',
                        'متوسط قيمة المنتج'
                    ],
                    'القيمة': [
                        str(len(df)),
                        f"{df['stock_value'].sum():,.2f} ر.س",
                        str(len(low_stock)),
                        f"{df['stock_value'].mean():,.2f} ر.س"
                    ]
                })

                stats_df.to_excel(writer, sheet_name='إحصائيات المخزون', index=False)

            return str(filepath), "تم إنشاء تقرير المخزون بنجاح"

        except Exception as e:
            return None, f"خطأ في إنشاء تقرير المخزون Excel: {e}"

    def generate_sales_analysis(self):
        """تحليل المبيعات الذكي"""
        try:
            # جلب بيانات المبيعات للشهر الماضي
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)

            query = '''
                SELECT 
                    si.invoice_date,
                    si.net_amount,
                    sii.product_id,
                    sii.quantity,
                    p.name as product_name,
                    c.name as customer_name
                FROM sales_invoices si
                JOIN sales_invoice_items sii ON si.id = sii.invoice_id
                JOIN products p ON sii.product_id = p.id
                LEFT JOIN customers c ON si.customer_id = c.id
                WHERE si.invoice_date BETWEEN ? AND ?
            '''

            results = self.db.fetch_all(query, (start_date, end_date))

            if not results:
                return {
                    'total_sales': 0,
                    'top_products': [],
                    'top_customers': [],
                    'sales_trend': 'مستقر',
                    'recommendations': ['لا توجد بيانات كافية للتحليل']
                }

            df = pd.DataFrame([dict(row) for row in results])

            # تحليل المنتجات الأكثر مبيعاً
            top_products = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(5)

            # تحليل العملاء الأكثر شراءً
            customer_sales = df.groupby('customer_name')['net_amount'].sum().sort_values(ascending=False).head(5)

            # تحليل اتجاه المبيعات
            df['invoice_date'] = pd.to_datetime(df['invoice_date'])
            daily_sales = df.groupby(df['invoice_date'].dt.date)['net_amount'].sum()

            # حساب الاتجاه
            if len(daily_sales) > 7:
                recent_avg = daily_sales.tail(7).mean()
                previous_avg = daily_sales.head(7).mean()

                if recent_avg > previous_avg * 1.1:
                    trend = 'متزايد'
                elif recent_avg < previous_avg * 0.9:
                    trend = 'متناقص'
                else:
                    trend = 'مستقر'
            else:
                trend = 'غير محدد'

            # توصيات ذكية
            recommendations = self.generate_recommendations(df, top_products, customer_sales, trend)

            return {
                'total_sales': df['net_amount'].sum(),
                'top_products': top_products.to_dict(),
                'top_customers': customer_sales.to_dict(),
                'sales_trend': trend,
                'recommendations': recommendations
            }

        except Exception as e:
            return {'error': f"خطأ في تحليل المبيعات: {e}"}

    def generate_recommendations(self, df, top_products, top_customers, trend):
        """توليد التوصيات الذكية"""
        recommendations = []

        # توصيات بناءً على الاتجاه
        if trend == 'متزايد':
            recommendations.append("المبيعات في تحسن! فكر في زيادة المخزون للمنتجات الأكثر مبيعاً")
        elif trend == 'متناقص':
            recommendations.append("المبيعات في تراجع. راجع استراتيجية التسويق والأسعار")

        # توصيات بناءً على المنتجات
        if not top_products.empty:
            best_product = top_products.index[0]
            recommendations.append(f"المنتج الأكثر مبيعاً: {best_product}. تأكد من توفر مخزون كافٍ")

        # توصيات بناءً على العملاء
        if not top_customers.empty:
            best_customer = top_customers.index[0]
            recommendations.append(f"أفضل عميل: {best_customer}. قدم له عروض خاصة للاحتفاظ به")

        # توصيات عامة
        recommendations.append("راجع المنتجات ناقصة المخزون بانتظام")
        recommendations.append("تابع أداء المبيعات يومياً لاتخاذ قرارات سريعة")

        return recommendations


