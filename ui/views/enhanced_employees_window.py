#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 نافذة إدارة الموظفين المحسنة والمطورة - الإصدار النهائي
Enhanced Employee Management Window - Final Version

نافذة احترافية ومتطورة مع:
- أزرار محسنة بأحجام أكبر وتأثيرات بصرية
- نظام ألوان متدرج جميل وحديث
- خطوط مكبرة وواضحة
- إصلاح جميع الأخطاء البرمجية
- تحسينات شاملة لتجربة المستخدم
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
import os
import math
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import threading
import time
from PIL import Image, ImageTk, ImageDraw, ImageFilter

# إعداد customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# نظام الألوان المتدرج المحسن والجميل
BEAUTIFUL_COLORS = {
    # الألوان الأساسية المتدرجة الجديدة - أكثر جمالاً وحيوية
    'royal_blue': ['#667eea', '#764ba2'],        # أزرق ملكي إلى بنفسجي
    'sunset_orange': ['#ff9a9e', '#fecfef'],     # برتقالي غروب إلى وردي
    'emerald_green': ['#a8edea', '#fed6e3'],     # زمردي إلى وردي فاتح
    'golden_yellow': ['#ffecd2', '#fcb69f'],     # ذهبي إلى خوخي
    'ocean_blue': ['#74b9ff', '#0984e3'],        # أزرق محيطي
    'forest_green': ['#00b894', '#55efc4'],      # أخضر غابات إلى نعناعي
    'purple_magic': ['#a29bfe', '#6c5ce7'],      # بنفسجي سحري
    'coral_pink': ['#fd79a8', '#fdcb6e'],        # مرجاني إلى ذهبي
    
    # ألوان خاصة للحالات
    'success_gradient': ['#00b894', '#55efc4'],  # نجاح
    'warning_gradient': ['#fdcb6e', '#e17055'],  # تحذير
    'danger_gradient': ['#e84393', '#fd79a8'],   # خطر
    'info_gradient': ['#74b9ff', '#0984e3'],     # معلومات
    
    # ألوان الخلفية والبطاقات
    'background_light': '#f8f9fa',
    'card_white': '#ffffff',
    'card_light': '#f1f3f4',
    'shadow_color': '#e9ecef',
    
    # ألوان النصوص المحسنة
    'text_dark': '#2d3436',
    'text_medium': '#636e72',
    'text_light': '#b2bec3',
    'text_white': '#ffffff',
    'text_accent': '#0984e3',
}

# إعدادات الخطوط المحسنة والمكبرة
ENHANCED_FONTS = {
    # خطوط العناوين
    'title_huge': ('Arial', 42, 'bold'),         # عناوين ضخمة
    'title_large': ('Arial', 36, 'bold'),        # عناوين كبيرة
    'title_medium': ('Arial', 28, 'bold'),       # عناوين متوسطة
    'title_small': ('Arial', 22, 'bold'),        # عناوين صغيرة
    
    # خطوط الرؤوس والأقسام
    'header_large': ('Arial', 24, 'bold'),       # رؤوس كبيرة
    'header_medium': ('Arial', 20, 'bold'),      # رؤوس متوسطة
    'header_small': ('Arial', 18, 'bold'),       # رؤوس صغيرة
    
    # خطوط الأزرار
    'button_huge': ('Arial', 20, 'bold'),        # أزرار ضخمة
    'button_large': ('Arial', 18, 'bold'),       # أزرار كبيرة
    'button_medium': ('Arial', 16, 'bold'),      # أزرار متوسطة
    'button_small': ('Arial', 14, 'bold'),       # أزرار صغيرة
    
    # خطوط النصوص
    'text_huge': ('Arial', 20),                  # نص ضخم
    'text_large': ('Arial', 18),                 # نص كبير
    'text_medium': ('Arial', 16),                # نص متوسط
    'text_small': ('Arial', 14),                 # نص صغير
    
    # خطوط خاصة
    'label_large': ('Arial', 18, 'bold'),        # تسميات كبيرة
    'label_medium': ('Arial', 16, 'bold'),       # تسميات متوسطة
    'input_large': ('Arial', 16),                # حقول إدخال كبيرة
    'input_medium': ('Arial', 14),               # حقول إدخال متوسطة
}

# إعدادات الأبعاد المحسنة
ENHANCED_DIMENSIONS = {
    # أبعاد الأزرار المحسنة
    'button_huge_width': 220,
    'button_huge_height': 70,
    'button_large_width': 200,
    'button_large_height': 60,
    'button_medium_width': 180,
    'button_medium_height': 50,
    'button_small_width': 140,
    'button_small_height': 40,
    
    # أبعاد حقول الإدخال
    'input_large_height': 55,
    'input_medium_height': 45,
    'input_small_height': 35,
    
    # أبعاد الأقسام
    'header_height': 140,
    'toolbar_height': 100,
    'dashboard_height': 280,
    'section_height': 60,
    
    # الزوايا والظلال
    'corner_radius_large': 25,
    'corner_radius_medium': 20,
    'corner_radius_small': 15,
    'shadow_offset': 5,
    'shadow_blur': 15,
}

# إعدادات التأثيرات البصرية المحسنة
VISUAL_EFFECTS = {
    'hover_scale': 1.1,                    # تكبير عند التمرير
    'animation_duration': 500,             # مدة الحركة
    'transition_ease': 'ease-in-out',      # نوع الانتقال
    'shadow_intensity': 0.3,               # شدة الظل
    'gradient_angle': 45,                  # زاوية التدرج
}

class EnhancedEmployeesWindow:
    """نافذة إدارة الموظفين المحسنة والمطورة"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.db_connection = None
        self.db_cursor = None
        
        # متغيرات البيانات
        self.employees_data = []
        self.filtered_employees = []
        self.current_employee = None
        
        # متغيرات النماذج
        self.form_vars = {}
        
        # متغيرات الواجهة
        self.tree = None
        self.search_var = None
        self.department_filter_var = None
        self.status_filter_var = None
        self.form_title_label = None
        self.results_label = None
        self.total_employees_label = None
        self.active_employees_label = None
        self.photo_label = None
        
        # إنشاء النافذة
        self.create_enhanced_window()
        
        # تهيئة قاعدة البيانات
        self.init_database()
        
        # تحميل البيانات
        self.load_employees_data()
    
    def create_enhanced_window(self):
        """إنشاء النافذة المحسنة والجميلة"""
        try:
            # إنشاء النافذة الرئيسية
            if self.parent:
                self.window = ctk.CTkToplevel(self.parent)
                self.window.transient(self.parent)
                self.window.grab_set()
            else:
                self.window = ctk.CTk()
            
            # تكوين النافذة المحسنة
            self.window.title("🚀 نظام إدارة الموظفين المحسن والمتطور")
            self.window.geometry("1850x1050")  # زيادة العرض والارتفاع (+2.8% و +5%)
            self.window.minsize(1450, 950)     # حد أدنى محسن للحجم
            self.window.state('zoomed')
            
            # تطبيق الخلفية الجميلة
            self.window.configure(fg_color=BEAUTIFUL_COLORS['background_light'])
            
            # إنشاء المحتوى المحسن
            self.create_main_content()
            
            print("✅ تم إنشاء النافذة المحسنة بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء النافذة المحسنة: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء النافذة: {e}")
    
    def create_main_content(self):
        """إنشاء المحتوى الرئيسي المحسن"""
        # الإطار الرئيسي
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # إنشاء الهيدر المحسن
        self.create_beautiful_header(main_frame)
        
        # إنشاء لوحة المعلومات المحسنة
        self.create_enhanced_dashboard(main_frame)
        
        # إنشاء شريط الأدوات المحسن
        self.create_enhanced_toolbar(main_frame)
        
        # إنشاء المحتوى الرئيسي
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # تقسيم المحتوى
        self.create_content_sections(content_frame)
    
    def create_beautiful_header(self, parent):
        """إنشاء الهيدر الجميل والمحسن"""
        # إطار الهيدر مع تدرج لوني جميل
        header_frame = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['header_height'],
            fg_color=BEAUTIFUL_COLORS['royal_blue'][0],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_large']
        )
        header_frame.pack(fill="x", pady=(0, 25))
        header_frame.pack_propagate(False)
        
        # إضافة تأثير الظل
        shadow_frame = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['shadow_offset'],
            fg_color=BEAUTIFUL_COLORS['shadow_color'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_large']
        )
        shadow_frame.place(
            in_=header_frame, 
            relx=0, 
            rely=1, 
            relwidth=1, 
            y=ENHANCED_DIMENSIONS['shadow_offset']
        )
        
        # محتوى الهيدر
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # الجانب الأيسر - العنوان والوصف
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # العنوان الرئيسي
        title_label = ctk.CTkLabel(
            left_frame,
            text="🚀 نظام إدارة الموظفين المتطور",
            font=ENHANCED_FONTS['title_huge'],
            text_color=BEAUTIFUL_COLORS['text_white']
        )
        title_label.pack(anchor="w")
        
        # الوصف
        subtitle_label = ctk.CTkLabel(
            left_frame,
            text="💎 إدارة شاملة ومتقدمة لجميع بيانات الموظفين مع تحليلات ذكية",
            font=ENHANCED_FONTS['text_large'],
            text_color="#f1f3f4"
        )
        subtitle_label.pack(anchor="w", pady=(10, 0))
        
        # الجانب الأيمن - بطاقات الإحصائيات
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        self.create_stats_cards(right_frame)
    
    def create_stats_cards(self, parent):
        """إنشاء بطاقات الإحصائيات المحسنة"""
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="both", expand=True)
        
        # بيانات الإحصائيات مع ألوان جميلة
        stats_data = [
            ("👥", "إجمالي الموظفين", "0", BEAUTIFUL_COLORS['emerald_green'][0]),
            ("✅", "الموظفين النشطين", "0", BEAUTIFUL_COLORS['forest_green'][0]),
            ("📊", "متوسط الأداء", "89%", BEAUTIFUL_COLORS['ocean_blue'][0]),
            ("🎯", "معدل الحضور", "96%", BEAUTIFUL_COLORS['coral_pink'][0])
        ]
        
        # إنشاء البطاقات في صفين
        for i, (icon, title, value, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            # إطار البطاقة مع تحسينات
            card_frame = ctk.CTkFrame(
                stats_container,
                width=200,  # أعرض
                height=100,  # أطول
                fg_color=color,
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium']
            )
            card_frame.grid(row=row, column=col, padx=15, pady=8, sticky="nsew")
            card_frame.pack_propagate(False)
            
            # محتوى البطاقة
            content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=20, pady=15)
            
            # الأيقونة والقيمة
            top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            top_frame.pack(fill="x")
            
            icon_label = ctk.CTkLabel(
                top_frame,
                text=icon,
                font=("Arial", 32),  # أيقونة أكبر
                text_color="white"
            )
            icon_label.pack(side="left")
            
            value_label = ctk.CTkLabel(
                top_frame,
                text=value,
                font=ENHANCED_FONTS['title_medium'],
                text_color="white"
            )
            value_label.pack(side="right")
            
            # العنوان
            title_label = ctk.CTkLabel(
                content_frame,
                text=title,
                font=ENHANCED_FONTS['text_medium'],
                text_color="#f8f9fa"
            )
            title_label.pack(anchor="w", pady=(5, 0))
            
            # حفظ المراجع للتحديث
            if title == "إجمالي الموظفين":
                self.total_employees_label = value_label
            elif title == "الموظفين النشطين":
                self.active_employees_label = value_label

    def create_enhanced_dashboard(self, parent):
        """إنشاء لوحة المعلومات المحسنة"""
        dashboard_frame = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['dashboard_height'],
            fg_color=BEAUTIFUL_COLORS['card_white'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_large']
        )
        dashboard_frame.pack(fill="x", pady=(0, 25))
        dashboard_frame.pack_propagate(False)

        # عنوان لوحة المعلومات
        title_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=(20, 10))

        dashboard_title = ctk.CTkLabel(
            title_frame,
            text="📊 لوحة المعلومات التفاعلية والذكية",
            font=ENHANCED_FONTS['header_large'],
            text_color=BEAUTIFUL_COLORS['text_dark']
        )
        dashboard_title.pack(side="left")

        # زر تحديث محسن
        refresh_btn = ctk.CTkButton(
            title_frame,
            text="🔄 تحديث البيانات",
            command=self.refresh_dashboard,
            width=ENHANCED_DIMENSIONS['button_medium_width'],
            height=ENHANCED_DIMENSIONS['button_medium_height'],
            font=ENHANCED_FONTS['button_medium'],
            fg_color=BEAUTIFUL_COLORS['info_gradient'][0],
            hover_color=BEAUTIFUL_COLORS['info_gradient'][1],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium']
        )
        refresh_btn.pack(side="right")

        # محتوى لوحة المعلومات
        content_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # تقسيم المحتوى إلى ثلاثة أقسام
        self.create_dashboard_sections(content_frame)

    def create_dashboard_sections(self, parent):
        """إنشاء أقسام لوحة المعلومات"""
        # القسم الأول - الرسوم البيانية
        charts_frame = ctk.CTkFrame(
            parent,
            fg_color=BEAUTIFUL_COLORS['card_light'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium']
        )
        charts_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        charts_title = ctk.CTkLabel(
            charts_frame,
            text="📈 توزيع الموظفين",
            font=ENHANCED_FONTS['header_small'],
            text_color=BEAUTIFUL_COLORS['text_dark']
        )
        charts_title.pack(pady=(15, 10))

        # محاكاة رسم بياني
        self.create_mock_chart(charts_frame)

        # القسم الثاني - التحليلات
        analytics_frame = ctk.CTkFrame(
            parent,
            fg_color=BEAUTIFUL_COLORS['card_light'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium']
        )
        analytics_frame.pack(side="left", fill="both", expand=True, padx=5)

        analytics_title = ctk.CTkLabel(
            analytics_frame,
            text="🧠 التحليلات الذكية",
            font=ENHANCED_FONTS['header_small'],
            text_color=BEAUTIFUL_COLORS['text_dark']
        )
        analytics_title.pack(pady=(15, 10))

        self.create_analytics_content(analytics_frame)

        # القسم الثالث - التنبيهات
        alerts_frame = ctk.CTkFrame(
            parent,
            fg_color=BEAUTIFUL_COLORS['card_light'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium']
        )
        alerts_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        alerts_title = ctk.CTkLabel(
            alerts_frame,
            text="🔔 التنبيهات الذكية",
            font=ENHANCED_FONTS['header_small'],
            text_color=BEAUTIFUL_COLORS['text_dark']
        )
        alerts_title.pack(pady=(15, 10))

        self.create_alerts_content(alerts_frame)

    def create_mock_chart(self, parent):
        """إنشاء رسم بياني محاكي"""
        chart_frame = ctk.CTkFrame(parent, fg_color="transparent")
        chart_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # بيانات الأقسام
        departments = ["الإدارة", "المحاسبة", "المبيعات", "التقنية"]
        colors = [
            BEAUTIFUL_COLORS['royal_blue'][0],
            BEAUTIFUL_COLORS['emerald_green'][0],
            BEAUTIFUL_COLORS['coral_pink'][0],
            BEAUTIFUL_COLORS['golden_yellow'][0]
        ]
        values = [25, 35, 20, 20]  # نسب مئوية

        for i, (dept, color, value) in enumerate(zip(departments, colors, values)):
            # شريط القسم
            dept_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
            dept_frame.pack(fill="x", pady=5)

            # اسم القسم
            dept_label = ctk.CTkLabel(
                dept_frame,
                text=dept,
                font=ENHANCED_FONTS['text_medium'],
                text_color=BEAUTIFUL_COLORS['text_dark']
            )
            dept_label.pack(side="left", padx=(0, 10))

            # شريط التقدم
            progress_frame = ctk.CTkFrame(
                dept_frame,
                height=25,
                fg_color=BEAUTIFUL_COLORS['shadow_color'],
                corner_radius=12
            )
            progress_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

            # الشريط الملون
            progress_bar = ctk.CTkFrame(
                progress_frame,
                width=max(10, int(float(value) * 2)),  # تحويل النسبة إلى عرض مع حد أدنى
                height=21,
                fg_color=color,
                corner_radius=10
            )
            progress_bar.pack(side="left", padx=2, pady=2)

            # النسبة المئوية
            percent_label = ctk.CTkLabel(
                dept_frame,
                text=f"{value}%",
                font=ENHANCED_FONTS['text_small'],
                text_color=BEAUTIFUL_COLORS['text_medium']
            )
            percent_label.pack(side="right")

    def create_analytics_content(self, parent):
        """إنشاء محتوى التحليلات"""
        analytics_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent"
        )
        analytics_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # بيانات التحليلات
        analytics_data = [
            ("🎯", "متوسط الأداء العام", "89.2%", "ممتاز"),
            ("📈", "نمو الإنتاجية", "+15%", "إيجابي"),
            ("⏰", "معدل الحضور", "96.8%", "ممتاز"),
            ("💡", "مؤشر الرضا", "85%", "جيد جداً")
        ]

        for icon, metric, value, status in analytics_data:
            metric_frame = ctk.CTkFrame(
                analytics_frame,
                fg_color=BEAUTIFUL_COLORS['card_white'],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_small']
            )
            metric_frame.pack(fill="x", pady=8)

            content_frame = ctk.CTkFrame(metric_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=15, pady=10)

            # الأيقونة
            icon_label = ctk.CTkLabel(
                content_frame,
                text=icon,
                font=("Arial", 20),
                text_color=BEAUTIFUL_COLORS['text_accent']
            )
            icon_label.pack(side="left")

            # المعلومات
            info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))

            metric_label = ctk.CTkLabel(
                info_frame,
                text=metric,
                font=ENHANCED_FONTS['text_small'],
                text_color=BEAUTIFUL_COLORS['text_dark'],
                anchor="w"
            )
            metric_label.pack(anchor="w")

            value_label = ctk.CTkLabel(
                info_frame,
                text=f"{value} - {status}",
                font=ENHANCED_FONTS['text_small'],
                text_color=BEAUTIFUL_COLORS['text_medium'],
                anchor="w"
            )
            value_label.pack(anchor="w")

    def create_alerts_content(self, parent):
        """إنشاء محتوى التنبيهات"""
        alerts_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent"
        )
        alerts_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # بيانات التنبيهات
        alerts_data = [
            ("🎂", "عيد ميلاد أحمد محمد غداً", "info"),
            ("📅", "انتهاء فترة تجربة سارة أحمد", "warning"),
            ("🏆", "تميز في الأداء - محمد علي", "success"),
            ("⚠️", "تأخير متكرر - فاطمة حسن", "danger"),
            ("📊", "موعد تقييم ربع سنوي", "info")
        ]

        alert_colors = {
            "info": BEAUTIFUL_COLORS['info_gradient'][0],
            "warning": BEAUTIFUL_COLORS['warning_gradient'][0],
            "success": BEAUTIFUL_COLORS['success_gradient'][0],
            "danger": BEAUTIFUL_COLORS['danger_gradient'][0]
        }

        for icon, message, alert_type in alerts_data:
            alert_frame = ctk.CTkFrame(
                alerts_frame,
                fg_color=alert_colors[alert_type],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_small']
            )
            alert_frame.pack(fill="x", pady=5)

            content_frame = ctk.CTkFrame(alert_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=12, pady=8)

            # الأيقونة
            icon_label = ctk.CTkLabel(
                content_frame,
                text=icon,
                font=("Arial", 16),
                text_color="white"
            )
            icon_label.pack(side="left")

            # الرسالة
            message_label = ctk.CTkLabel(
                content_frame,
                text=message,
                font=ENHANCED_FONTS['text_small'],
                text_color="white",
                anchor="w"
            )
            message_label.pack(side="left", fill="x", expand=True, padx=(8, 0))

    def create_enhanced_toolbar(self, parent):
        """إنشاء شريط الأدوات المحسن مع أزرار جميلة"""
        toolbar_frame = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['toolbar_height'],
            fg_color=BEAUTIFUL_COLORS['card_white'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_large']
        )
        toolbar_frame.pack(fill="x", pady=(0, 25))
        toolbar_frame.pack_propagate(False)

        # محتوى شريط الأدوات
        content_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # الجانب الأيسر - أزرار العمليات المحسنة
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y")

        # أزرار العمليات الرئيسية مع تصميم محسن وألوان جميلة
        buttons_data = [
            ("➕", "إضافة موظف", self.add_employee, BEAUTIFUL_COLORS['success_gradient']),
            ("✏️", "تعديل بيانات", self.edit_employee, BEAUTIFUL_COLORS['info_gradient']),
            ("🗑️", "حذف موظف", self.delete_employee, BEAUTIFUL_COLORS['danger_gradient']),
            ("📊", "تحليل الأداء", self.analyze_performance, BEAUTIFUL_COLORS['warning_gradient']),
            ("💰", "إدارة الرواتب", self.manage_salaries, BEAUTIFUL_COLORS['purple_magic']),
            ("📋", "تقارير شاملة", self.generate_reports, BEAUTIFUL_COLORS['ocean_blue'])
        ]

        for i, (icon, text, command, gradient) in enumerate(buttons_data):
            # إطار الزر مع تأثير الظل
            btn_container = ctk.CTkFrame(left_frame, fg_color="transparent")
            btn_container.pack(side="left", padx=15)

            # الزر المحسن
            btn = ctk.CTkButton(
                btn_container,
                text=f"{icon}\n{text}",
                command=command,
                width=ENHANCED_DIMENSIONS['button_large_width'],
                height=ENHANCED_DIMENSIONS['button_large_height'],
                font=ENHANCED_FONTS['button_large'],
                fg_color=gradient[0],
                hover_color=gradient[1],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
                text_color="white",
                border_width=0
            )
            btn.pack()

            # تأثير الظل المحسن
            shadow = ctk.CTkFrame(
                btn_container,
                width=ENHANCED_DIMENSIONS['button_large_width'],
                height=ENHANCED_DIMENSIONS['shadow_offset'],
                fg_color=BEAUTIFUL_COLORS['shadow_color'],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium']
            )
            shadow.place(
                in_=btn,
                relx=0,
                rely=1,
                y=ENHANCED_DIMENSIONS['shadow_offset']
            )

        # الجانب الأيمن - البحث والفلترة المحسنة
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y")

        self.create_search_and_filters(right_frame)

    def create_search_and_filters(self, parent):
        """إنشاء منطقة البحث والفلترة المحسنة"""
        # شريط البحث المحسن
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(side="right", padx=20)

        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Arial", 28),
            text_color=BEAUTIFUL_COLORS['text_accent']
        )
        search_label.pack(side="left", padx=(0, 10))

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_search_change)

        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="🔎 بحث شامل في جميع بيانات الموظفين...",
            width=350,
            height=ENHANCED_DIMENSIONS['input_large_height'],
            font=ENHANCED_FONTS['input_large'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
            border_width=3,
            border_color=BEAUTIFUL_COLORS['royal_blue'][0],
            fg_color="white",
            text_color=BEAUTIFUL_COLORS['text_dark']
        )
        search_entry.pack(side="left")

        # فلاتر محسنة
        filters_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filters_frame.pack(side="right", padx=20)

        # فلتر القسم
        dept_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        dept_frame.pack(side="right", padx=15)

        dept_label = ctk.CTkLabel(
            dept_frame,
            text="🏢 القسم:",
            font=ENHANCED_FONTS['label_medium'],
            text_color=BEAUTIFUL_COLORS['text_dark']
        )
        dept_label.pack(side="left", padx=(0, 10))

        self.department_filter_var = ctk.StringVar(value="الكل")
        dept_combo = ctk.CTkComboBox(
            dept_frame,
            variable=self.department_filter_var,
            values=["الكل", "الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية", "التسويق"],
            width=180,
            height=ENHANCED_DIMENSIONS['input_large_height'],
            font=ENHANCED_FONTS['input_medium'],
            command=self.on_filter_change,
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
            border_color=BEAUTIFUL_COLORS['emerald_green'][0],
            fg_color="white",
            text_color=BEAUTIFUL_COLORS['text_dark'],
            button_color=BEAUTIFUL_COLORS['emerald_green'][0],
            button_hover_color=BEAUTIFUL_COLORS['emerald_green'][1]
        )
        dept_combo.pack(side="left")

        # فلتر الحالة
        status_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        status_frame.pack(side="right", padx=15)

        status_label = ctk.CTkLabel(
            status_frame,
            text="📊 الحالة:",
            font=ENHANCED_FONTS['label_medium'],
            text_color=BEAUTIFUL_COLORS['text_dark']
        )
        status_label.pack(side="left", padx=(0, 10))

        self.status_filter_var = ctk.StringVar(value="الكل")
        status_combo = ctk.CTkComboBox(
            status_frame,
            variable=self.status_filter_var,
            values=["الكل", "نشط", "غير نشط", "معلق", "مستقيل"],
            width=160,
            height=ENHANCED_DIMENSIONS['input_large_height'],
            font=ENHANCED_FONTS['input_medium'],
            command=self.on_filter_change,
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
            border_color=BEAUTIFUL_COLORS['coral_pink'][0],
            fg_color="white",
            text_color=BEAUTIFUL_COLORS['text_dark'],
            button_color=BEAUTIFUL_COLORS['coral_pink'][0],
            button_hover_color=BEAUTIFUL_COLORS['coral_pink'][1]
        )
        status_combo.pack(side="left")

    def create_content_sections(self, parent):
        """إنشاء أقسام المحتوى الرئيسي"""
        # تقسيم المحتوى إلى جانبين
        left_panel = ctk.CTkFrame(
            parent,
            fg_color=BEAUTIFUL_COLORS['card_white'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_large']
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))

        right_panel = ctk.CTkFrame(
            parent,
            width=500,
            fg_color=BEAUTIFUL_COLORS['card_white'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_large']
        )
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # إنشاء جدول الموظفين المحسن
        self.create_enhanced_table(left_panel)

        # إنشاء نموذج الموظف المحسن
        self.create_enhanced_form(right_panel)

    def create_enhanced_table(self, parent):
        """إنشاء جدول الموظفين المحسن"""
        # عنوان الجدول
        table_header = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['section_height'],
            fg_color=BEAUTIFUL_COLORS['forest_green'][0],
            corner_radius=(ENHANCED_DIMENSIONS['corner_radius_large'],
                          ENHANCED_DIMENSIONS['corner_radius_large'], 0, 0)
        )
        table_header.pack(fill="x")
        table_header.pack_propagate(False)

        # محتوى العنوان
        header_content = ctk.CTkFrame(table_header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)

        title_label = ctk.CTkLabel(
            header_content,
            text="👥 قائمة الموظفين الشاملة والمتطورة",
            font=ENHANCED_FONTS['header_medium'],
            text_color="white"
        )
        title_label.pack(side="left")

        # مؤشر عدد النتائج
        self.results_label = ctk.CTkLabel(
            header_content,
            text="عرض 0 من 0 موظف",
            font=ENHANCED_FONTS['text_large'],
            text_color="#f1f3f4"
        )
        self.results_label.pack(side="right")

        # إطار الجدول
        table_frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=(0, 0, ENHANCED_DIMENSIONS['corner_radius_large'],
                          ENHANCED_DIMENSIONS['corner_radius_large'])
        )
        table_frame.pack(fill="both", expand=True)

        # إنشاء Treeview محسن
        self.create_treeview(table_frame)

    def create_treeview(self, parent):
        """إنشاء جدول البيانات المحسن"""
        # إطار للجدول مع شريط التمرير
        tree_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # تكوين الأعمدة
        columns = (
            "الرقم", "رقم الموظف", "الاسم الكامل", "القسم",
            "المنصب", "الراتب", "الحالة", "تاريخ التوظيف"
        )

        # إنشاء Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )

        # تكوين الأعمدة
        column_widths = [80, 120, 200, 120, 150, 120, 100, 130]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=width, anchor="center")

        # تطبيق ستايل محسن
        style = ttk.Style()
        style.theme_use("clam")

        # تخصيص الألوان
        style.configure(
            "Treeview",
            background="white",
            foreground=BEAUTIFUL_COLORS['text_dark'],
            rowheight=35,
            fieldbackground="white",
            font=ENHANCED_FONTS['text_medium']
        )

        style.configure(
            "Treeview.Heading",
            background=BEAUTIFUL_COLORS['royal_blue'][0],
            foreground="white",
            font=ENHANCED_FONTS['label_medium']
        )

        # ألوان الصفوف المتناوبة
        self.tree.tag_configure("oddrow", background="#f8f9fa")
        self.tree.tag_configure("evenrow", background="white")

        # شريط التمرير العمودي
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # شريط التمرير الأفقي
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        # تخطيط الجدول
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # تكوين الشبكة
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # ربط الأحداث
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_enhanced_form(self, parent):
        """إنشاء نموذج الموظف المحسن"""
        # عنوان النموذج
        form_header = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['section_height'],
            fg_color=BEAUTIFUL_COLORS['purple_magic'][0],
            corner_radius=(ENHANCED_DIMENSIONS['corner_radius_large'],
                          ENHANCED_DIMENSIONS['corner_radius_large'], 0, 0)
        )
        form_header.pack(fill="x")
        form_header.pack_propagate(False)

        # عنوان النموذج
        self.form_title_label = ctk.CTkLabel(
            form_header,
            text="📝 نموذج بيانات الموظف المتطور",
            font=ENHANCED_FONTS['header_medium'],
            text_color="white"
        )
        self.form_title_label.pack(pady=15)

        # محتوى النموذج القابل للتمرير
        form_content = ctk.CTkScrollableFrame(
            parent,
            fg_color="white",
            corner_radius=(0, 0, ENHANCED_DIMENSIONS['corner_radius_large'],
                          ENHANCED_DIMENSIONS['corner_radius_large'])
        )
        form_content.pack(fill="both", expand=True)

        # إنشاء حقول النموذج
        self.create_form_fields(form_content)

        # أزرار النموذج
        self.create_form_buttons(parent)

    def create_form_fields(self, parent):
        """إنشاء حقول النموذج المحسنة"""
        # تهيئة متغيرات النموذج
        self.form_vars = {
            'employee_number': ctk.StringVar(),
            'full_name': ctk.StringVar(),
            'national_id': ctk.StringVar(),
            'phone': ctk.StringVar(),
            'email': ctk.StringVar(),
            'address': ctk.StringVar(),
            'department': ctk.StringVar(),
            'position': ctk.StringVar(),
            'hire_date': ctk.StringVar(),
            'birth_date': ctk.StringVar(),
            'basic_salary': ctk.StringVar(),
            'status': ctk.StringVar(value="نشط"),
            'notes': ctk.StringVar()
        }

        # تعريف الحقول مع تحسينات
        fields_config = [
            # القسم الأول - البيانات الشخصية
            ("👤 البيانات الشخصية", [
                ("رقم الموظف", "employee_number", "entry", True),
                ("الاسم الكامل", "full_name", "entry", True),
                ("رقم الهوية", "national_id", "entry", True),
                ("تاريخ الميلاد", "birth_date", "date", False)
            ]),

            # القسم الثاني - بيانات الاتصال
            ("📞 بيانات الاتصال", [
                ("رقم الهاتف", "phone", "entry", True),
                ("البريد الإلكتروني", "email", "entry", False),
                ("العنوان", "address", "text", False)
            ]),

            # القسم الثالث - بيانات العمل
            ("💼 بيانات العمل", [
                ("القسم", "department", "combo", True),
                ("المنصب", "position", "combo", True),
                ("تاريخ التوظيف", "hire_date", "date", True),
                ("الحالة", "status", "combo", True)
            ]),

            # القسم الرابع - الراتب والملاحظات
            ("💰 الراتب والملاحظات", [
                ("الراتب الأساسي", "basic_salary", "number", True),
                ("ملاحظات", "notes", "text", False)
            ])
        ]

        # إنشاء الأقسام والحقول
        for section_title, fields in fields_config:
            self.create_form_section(parent, section_title, fields)

    def create_form_section(self, parent, title, fields):
        """إنشاء قسم في النموذج"""
        # إطار القسم
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=BEAUTIFUL_COLORS['card_light'],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium']
        )
        section_frame.pack(fill="x", padx=20, pady=15)

        # عنوان القسم
        title_frame = ctk.CTkFrame(
            section_frame,
            fg_color=BEAUTIFUL_COLORS['royal_blue'][0],
            corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
            height=50
        )
        title_frame.pack(fill="x", padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=ENHANCED_FONTS['header_small'],
            text_color="white"
        )
        title_label.pack(pady=12)

        # محتوى القسم
        content_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=10)

        # إنشاء الحقول
        for field_label, field_var, field_type, required in fields:
            self.create_form_field(content_frame, field_label, field_var, field_type, required)

    def create_form_field(self, parent, label_text, var_name, field_type, required):
        """إنشاء حقل في النموذج"""
        # إطار الحقل
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=8)

        # إطار التسمية
        label_frame = ctk.CTkFrame(field_frame, fg_color="transparent")
        label_frame.pack(fill="x", pady=(0, 5))

        # التسمية مع علامة المطلوب
        label_text_display = f"{label_text} *" if required else label_text
        label_color = BEAUTIFUL_COLORS['text_accent'] if required else BEAUTIFUL_COLORS['text_dark']

        label = ctk.CTkLabel(
            label_frame,
            text=label_text_display,
            font=ENHANCED_FONTS['label_medium'],
            text_color=label_color,
            anchor="w"
        )
        label.pack(side="left")

        # إنشاء الحقل حسب النوع
        widget = self.create_field_widget(field_frame, var_name, field_type, required)
        if widget:
            widget.pack(fill="x", pady=(0, 5))

    def create_field_widget(self, parent, var_name, field_type, required):
        """إنشاء عنصر الحقل حسب النوع"""
        border_color = BEAUTIFUL_COLORS['royal_blue'][0] if required else BEAUTIFUL_COLORS['shadow_color']

        if field_type == "entry":
            widget = ctk.CTkEntry(
                parent,
                textvariable=self.form_vars[var_name],
                font=ENHANCED_FONTS['input_large'],
                height=ENHANCED_DIMENSIONS['input_large_height'],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
                border_width=3,
                border_color=border_color,
                fg_color="white",
                text_color=BEAUTIFUL_COLORS['text_dark']
            )
            return widget

        elif field_type == "text":
            widget = ctk.CTkTextbox(
                parent,
                height=80,
                font=ENHANCED_FONTS['input_medium'],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
                border_width=3,
                border_color=border_color,
                fg_color="white",
                text_color=BEAUTIFUL_COLORS['text_dark']
            )
            # ربط التحديث
            widget.bind("<KeyRelease>", lambda e: self.update_text_var(var_name, widget))
            return widget

        elif field_type == "combo":
            values = self.get_combo_values(var_name)
            widget = ctk.CTkComboBox(
                parent,
                variable=self.form_vars[var_name],
                values=values,
                font=ENHANCED_FONTS['input_medium'],
                height=ENHANCED_DIMENSIONS['input_large_height'],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
                border_width=3,
                border_color=border_color,
                fg_color="white",
                text_color=BEAUTIFUL_COLORS['text_dark'],
                button_color=BEAUTIFUL_COLORS['emerald_green'][0],
                button_hover_color=BEAUTIFUL_COLORS['emerald_green'][1]
            )
            return widget

        elif field_type == "number":
            widget = ctk.CTkEntry(
                parent,
                textvariable=self.form_vars[var_name],
                font=ENHANCED_FONTS['input_large'],
                height=ENHANCED_DIMENSIONS['input_large_height'],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
                border_width=3,
                border_color=border_color,
                fg_color="white",
                text_color=BEAUTIFUL_COLORS['text_dark']
            )
            # ربط التحقق من الأرقام
            widget.bind("<KeyRelease>", lambda e: self.validate_number(var_name))
            return widget

        elif field_type == "date":
            widget = ctk.CTkEntry(
                parent,
                textvariable=self.form_vars[var_name],
                placeholder_text="📅 YYYY-MM-DD",
                font=ENHANCED_FONTS['input_large'],
                height=ENHANCED_DIMENSIONS['input_large_height'],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
                border_width=3,
                border_color=border_color,
                fg_color="white",
                text_color=BEAUTIFUL_COLORS['text_dark']
            )
            return widget

        return None

    def create_form_buttons(self, parent):
        """إنشاء أزرار النموذج المحسنة"""
        buttons_frame = ctk.CTkFrame(
            parent,
            height=80,
            fg_color=BEAUTIFUL_COLORS['card_light'],
            corner_radius=(0, 0, ENHANCED_DIMENSIONS['corner_radius_large'],
                          ENHANCED_DIMENSIONS['corner_radius_large'])
        )
        buttons_frame.pack(fill="x")
        buttons_frame.pack_propagate(False)

        # محتوى الأزرار
        content_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # أزرار العمليات
        buttons_data = [
            ("💾", "حفظ", self.save_employee, BEAUTIFUL_COLORS['success_gradient']),
            ("🔄", "تحديث", self.update_employee, BEAUTIFUL_COLORS['info_gradient']),
            ("🗑️", "مسح", self.clear_form, BEAUTIFUL_COLORS['warning_gradient']),
            ("❌", "إلغاء", self.cancel_operation, BEAUTIFUL_COLORS['danger_gradient'])
        ]

        for icon, text, command, gradient in buttons_data:
            btn = ctk.CTkButton(
                content_frame,
                text=f"{icon} {text}",
                command=command,
                width=ENHANCED_DIMENSIONS['button_medium_width'],
                height=ENHANCED_DIMENSIONS['button_medium_height'],
                font=ENHANCED_FONTS['button_medium'],
                fg_color=gradient[0],
                hover_color=gradient[1],
                corner_radius=ENHANCED_DIMENSIONS['corner_radius_medium'],
                text_color="white"
            )
            btn.pack(side="left", padx=10, expand=True)

    # ==================== وظائف قاعدة البيانات ====================

    def init_database(self):
        """تهيئة قاعدة البيانات"""
        try:
            # إنشاء مجلد قاعدة البيانات إذا لم يكن موجوداً
            db_dir = "database"
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)

            # الاتصال بقاعدة البيانات
            db_path = os.path.join(db_dir, "employees.db")
            self.db_connection = sqlite3.connect(db_path)
            self.db_cursor = self.db_connection.cursor()

            # إنشاء جدول الموظفين
            self.create_employees_table()

            # إدراج بيانات تجريبية إذا كان الجدول فارغاً
            self.insert_sample_data()

            print("✅ تم تهيئة قاعدة البيانات بنجاح")

        except Exception as e:
            print(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في تهيئة قاعدة البيانات: {e}")

    def create_employees_table(self):
        """إنشاء جدول الموظفين"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_number TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            national_id TEXT UNIQUE,
            phone TEXT,
            email TEXT,
            address TEXT,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            hire_date DATE NOT NULL,
            birth_date DATE,
            basic_salary REAL NOT NULL,
            status TEXT DEFAULT 'نشط',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.db_cursor.execute(create_table_sql)
        self.db_connection.commit()

    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        # التحقق من وجود بيانات
        self.db_cursor.execute("SELECT COUNT(*) FROM employees")
        count = self.db_cursor.fetchone()[0]

        if count == 0:
            sample_employees = [
                ("EMP001", "أحمد محمد علي", "1234567890", "0501234567", "ahmed@company.com",
                 "الرياض، المملكة العربية السعودية", "الإدارة", "مدير عام", "2020-01-15",
                 "1985-03-20", 15000, "نشط", "موظف متميز"),
                ("EMP002", "فاطمة حسن أحمد", "1234567891", "0501234568", "fatima@company.com",
                 "جدة، المملكة العربية السعودية", "المحاسبة", "محاسب أول", "2021-03-10",
                 "1990-07-15", 8000, "نشط", "دقيقة في العمل"),
                ("EMP003", "محمد عبدالله سالم", "1234567892", "0501234569", "mohammed@company.com",
                 "الدمام، المملكة العربية السعودية", "المبيعات", "مندوب مبيعات", "2021-06-01",
                 "1988-12-05", 6000, "نشط", "مبدع في المبيعات"),
                ("EMP004", "سارة أحمد محمد", "1234567893", "0501234570", "sara@company.com",
                 "الرياض، المملكة العربية السعودية", "التقنية", "مطور برمجيات", "2022-01-20",
                 "1992-09-10", 9000, "نشط", "خبيرة في البرمجة"),
                ("EMP005", "عبدالرحمن خالد", "1234567894", "0501234571", "abdulrahman@company.com",
                 "مكة، المملكة العربية السعودية", "الموارد البشرية", "أخصائي موارد بشرية", "2022-05-15",
                 "1987-04-25", 7000, "نشط", "متخصص في التدريب")
            ]

            insert_sql = """
            INSERT INTO employees (employee_number, full_name, national_id, phone, email,
                                 address, department, position, hire_date, birth_date,
                                 basic_salary, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self.db_cursor.executemany(insert_sql, sample_employees)
            self.db_connection.commit()
            print("✅ تم إدراج البيانات التجريبية")

    def load_employees_data(self):
        """تحميل بيانات الموظفين"""
        try:
            self.db_cursor.execute("""
                SELECT id, employee_number, full_name, department, position,
                       basic_salary, status, hire_date
                FROM employees
                ORDER BY full_name
            """)

            self.employees_data = self.db_cursor.fetchall()
            self.filtered_employees = self.employees_data.copy()

            # تحديث الجدول
            self.update_table()

            # تحديث الإحصائيات
            self.update_statistics()

            print(f"✅ تم تحميل {len(self.employees_data)} موظف")

        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في تحميل البيانات: {e}")

    def update_table(self):
        """تحديث جدول الموظفين"""
        try:
            # مسح البيانات الحالية
            if hasattr(self, 'tree') and self.tree:
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # إدراج البيانات الجديدة
                for i, employee in enumerate(self.filtered_employees):
                    # تحديد لون الصف
                    tag = "evenrow" if i % 2 == 0 else "oddrow"

                    # تنسيق البيانات
                    formatted_data = (
                        employee[0],  # ID
                        employee[1],  # رقم الموظف
                        employee[2],  # الاسم
                        employee[3],  # القسم
                        employee[4],  # المنصب
                        f"{employee[5]:,.0f} ريال",  # الراتب
                        employee[6],  # الحالة
                        employee[7]   # تاريخ التوظيف
                    )

                    self.tree.insert("", "end", values=formatted_data, tags=(tag,))

                # تحديث مؤشر النتائج
                self.update_results_indicator()

        except Exception as e:
            print(f"❌ خطأ في تحديث الجدول: {e}")

    def update_statistics(self):
        """تحديث الإحصائيات"""
        try:
            total_employees = len(self.employees_data)
            active_employees = len([emp for emp in self.employees_data if emp[6] == "نشط"])

            # تحديث بطاقات الإحصائيات
            if hasattr(self, 'total_employees_label') and self.total_employees_label:
                self.total_employees_label.configure(text=str(total_employees))

            if hasattr(self, 'active_employees_label') and self.active_employees_label:
                self.active_employees_label.configure(text=str(active_employees))

        except Exception as e:
            print(f"❌ خطأ في تحديث الإحصائيات: {e}")

    def update_results_indicator(self):
        """تحديث مؤشر النتائج"""
        try:
            if hasattr(self, 'results_label') and self.results_label:
                total = len(self.employees_data)
                filtered = len(self.filtered_employees)

                if filtered == total:
                    text = f"عرض جميع الموظفين ({total})"
                else:
                    text = f"عرض {filtered} من {total} موظف"

                self.results_label.configure(text=text)

        except Exception as e:
            print(f"❌ خطأ في تحديث مؤشر النتائج: {e}")

    # ==================== وظائف مساعدة ====================

    def get_combo_values(self, var_name):
        """الحصول على قيم القوائم المنسدلة"""
        combo_values = {
            'department': ["الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية", "التسويق", "الأمن"],
            'position': ["مدير عام", "مدير قسم", "رئيس قسم", "موظف أول", "موظف", "متدرب"],
            'status': ["نشط", "غير نشط", "معلق", "مستقيل", "متقاعد"]
        }
        return combo_values.get(var_name, [])

    def update_text_var(self, var_name, widget):
        """تحديث متغير النص"""
        try:
            content = widget.get("1.0", "end-1c")
            self.form_vars[var_name].set(content)
        except Exception as e:
            print(f"خطأ في تحديث النص: {e}")

    def validate_number(self, var_name):
        """التحقق من صحة الأرقام"""
        try:
            value = self.form_vars[var_name].get()
            if value and not value.replace(".", "").replace(",", "").isdigit():
                # إزالة الأحرف غير الرقمية
                cleaned = ''.join(c for c in value if c.isdigit() or c in '.,')
                self.form_vars[var_name].set(cleaned)
        except Exception as e:
            print(f"خطأ في التحقق من الرقم: {e}")

    # ==================== وظائف الأحداث ====================

    def on_search_change(self, *args):
        """عند تغيير البحث"""
        try:
            search_term = self.search_var.get().lower()
            self.apply_filters()
        except Exception as e:
            print(f"خطأ في البحث: {e}")

    def on_filter_change(self, *args):
        """عند تغيير الفلاتر"""
        try:
            self.apply_filters()
        except Exception as e:
            print(f"خطأ في الفلترة: {e}")

    def apply_filters(self):
        """تطبيق الفلاتر والبحث"""
        try:
            search_term = self.search_var.get().lower() if self.search_var else ""
            dept_filter = self.department_filter_var.get() if self.department_filter_var else "الكل"
            status_filter = self.status_filter_var.get() if self.status_filter_var else "الكل"

            self.filtered_employees = []

            for employee in self.employees_data:
                # فلتر البحث
                if search_term:
                    searchable_text = f"{employee[1]} {employee[2]} {employee[3]} {employee[4]}".lower()
                    if search_term not in searchable_text:
                        continue

                # فلتر القسم
                if dept_filter != "الكل" and employee[3] != dept_filter:
                    continue

                # فلتر الحالة
                if status_filter != "الكل" and employee[6] != status_filter:
                    continue

                self.filtered_employees.append(employee)

            # تحديث الجدول
            self.update_table()

        except Exception as e:
            print(f"خطأ في تطبيق الفلاتر: {e}")

    def on_tree_select(self, event):
        """عند تحديد صف في الجدول"""
        try:
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                employee_id = item['values'][0]
                self.load_employee_details(employee_id)
        except Exception as e:
            print(f"خطأ في تحديد الموظف: {e}")

    def on_tree_double_click(self, event):
        """عند النقر المزدوج على الجدول"""
        try:
            selection = self.tree.selection()
            if selection:
                self.edit_employee()
        except Exception as e:
            print(f"خطأ في النقر المزدوج: {e}")

    def show_context_menu(self, event):
        """إظهار قائمة السياق"""
        try:
            # إنشاء قائمة السياق
            context_menu = tk.Menu(self.window, tearoff=0)
            context_menu.add_command(label="✏️ تعديل", command=self.edit_employee)
            context_menu.add_command(label="🗑️ حذف", command=self.delete_employee)
            context_menu.add_separator()
            context_menu.add_command(label="📊 تحليل الأداء", command=self.analyze_performance)
            context_menu.add_command(label="💰 إدارة الراتب", command=self.manage_salaries)

            # إظهار القائمة
            context_menu.post(event.x_root, event.y_root)

        except Exception as e:
            print(f"خطأ في قائمة السياق: {e}")

    def load_employee_details(self, employee_id):
        """تحميل تفاصيل الموظف"""
        try:
            self.db_cursor.execute("""
                SELECT * FROM employees WHERE id = ?
            """, (employee_id,))

            employee = self.db_cursor.fetchone()
            if employee:
                # تحديث النموذج
                self.form_vars['employee_number'].set(employee[1] or "")
                self.form_vars['full_name'].set(employee[2] or "")
                self.form_vars['national_id'].set(employee[3] or "")
                self.form_vars['phone'].set(employee[4] or "")
                self.form_vars['email'].set(employee[5] or "")
                self.form_vars['address'].set(employee[6] or "")
                self.form_vars['department'].set(employee[7] or "")
                self.form_vars['position'].set(employee[8] or "")
                self.form_vars['hire_date'].set(employee[9] or "")
                self.form_vars['birth_date'].set(employee[10] or "")
                self.form_vars['basic_salary'].set(str(employee[11]) if employee[11] else "")
                self.form_vars['status'].set(employee[12] or "نشط")
                self.form_vars['notes'].set(employee[13] or "")

                # حفظ الموظف الحالي
                self.current_employee = employee

                # تحديث عنوان النموذج
                if hasattr(self, 'form_title_label') and self.form_title_label:
                    self.form_title_label.configure(
                        text=f"📝 تفاصيل الموظف: {employee[2]}"
                    )

        except Exception as e:
            print(f"خطأ في تحميل تفاصيل الموظف: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في تحميل تفاصيل الموظف: {e}")

    # ==================== وظائف العمليات ====================

    def add_employee(self):
        """إضافة موظف جديد"""
        try:
            self.clear_form()
            self.current_employee = None

            # تحديث عنوان النموذج
            if hasattr(self, 'form_title_label') and self.form_title_label:
                self.form_title_label.configure(text="📝 إضافة موظف جديد")

            # توليد رقم موظف جديد
            self.generate_employee_number()

            self.show_success_message("تم تحضير النموذج لإضافة موظف جديد")

        except Exception as e:
            print(f"خطأ في إضافة موظف: {e}")
            self.show_error_message(f"حدث خطأ في إضافة موظف: {e}")

    def edit_employee(self):
        """تعديل موظف"""
        try:
            selection = self.tree.selection()
            if not selection:
                self.show_warning_message("يرجى تحديد موظف للتعديل")
                return

            item = self.tree.item(selection[0])
            employee_id = item['values'][0]
            self.load_employee_details(employee_id)

            self.show_info_message("تم تحميل بيانات الموظف للتعديل")

        except Exception as e:
            print(f"خطأ في تعديل الموظف: {e}")
            self.show_error_message(f"حدث خطأ في تعديل الموظف: {e}")

    def delete_employee(self):
        """حذف موظف"""
        try:
            selection = self.tree.selection()
            if not selection:
                self.show_warning_message("يرجى تحديد موظف للحذف")
                return

            item = self.tree.item(selection[0])
            employee_name = item['values'][2]

            # تأكيد الحذف
            result = messagebox.askyesno(
                "تأكيد الحذف",
                f"هل أنت متأكد من حذف الموظف: {employee_name}؟\n\nهذا الإجراء لا يمكن التراجع عنه.",
                icon="warning"
            )

            if result:
                employee_id = item['values'][0]

                # حذف من قاعدة البيانات
                self.db_cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
                self.db_connection.commit()

                # إعادة تحميل البيانات
                self.load_employees_data()

                # مسح النموذج
                self.clear_form()

                self.show_success_message(f"تم حذف الموظف {employee_name} بنجاح")

        except Exception as e:
            print(f"خطأ في حذف الموظف: {e}")
            self.show_error_message(f"حدث خطأ في حذف الموظف: {e}")

    def save_employee(self):
        """حفظ بيانات الموظف"""
        try:
            # التحقق من البيانات المطلوبة
            if not self.validate_form():
                return

            # جمع البيانات
            employee_data = {
                'employee_number': self.form_vars['employee_number'].get(),
                'full_name': self.form_vars['full_name'].get(),
                'national_id': self.form_vars['national_id'].get(),
                'phone': self.form_vars['phone'].get(),
                'email': self.form_vars['email'].get(),
                'address': self.form_vars['address'].get(),
                'department': self.form_vars['department'].get(),
                'position': self.form_vars['position'].get(),
                'hire_date': self.form_vars['hire_date'].get(),
                'birth_date': self.form_vars['birth_date'].get(),
                'basic_salary': float(self.form_vars['basic_salary'].get() or 0),
                'status': self.form_vars['status'].get(),
                'notes': self.form_vars['notes'].get()
            }

            if self.current_employee:
                # تحديث موظف موجود
                self.update_employee_data(employee_data)
            else:
                # إضافة موظف جديد
                self.insert_employee_data(employee_data)

        except Exception as e:
            print(f"خطأ في حفظ الموظف: {e}")
            self.show_error_message(f"حدث خطأ في حفظ الموظف: {e}")

    def validate_form(self):
        """التحقق من صحة بيانات النموذج"""
        try:
            # الحقول المطلوبة
            required_fields = {
                'employee_number': 'رقم الموظف',
                'full_name': 'الاسم الكامل',
                'department': 'القسم',
                'position': 'المنصب',
                'hire_date': 'تاريخ التوظيف',
                'basic_salary': 'الراتب الأساسي'
            }

            # التحقق من الحقول المطلوبة
            for field, label in required_fields.items():
                if not self.form_vars[field].get().strip():
                    self.show_warning_message(f"يرجى إدخال {label}")
                    return False

            # التحقق من صحة الراتب
            try:
                salary = float(self.form_vars['basic_salary'].get())
                if salary <= 0:
                    self.show_warning_message("يجب أن يكون الراتب أكبر من صفر")
                    return False
            except ValueError:
                self.show_warning_message("يرجى إدخال راتب صحيح")
                return False

            return True

        except Exception as e:
            print(f"خطأ في التحقق من النموذج: {e}")
            return False

    def insert_employee_data(self, employee_data):
        """إدراج موظف جديد"""
        try:
            insert_sql = """
            INSERT INTO employees (employee_number, full_name, national_id, phone, email,
                                 address, department, position, hire_date, birth_date,
                                 basic_salary, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            values = (
                employee_data['employee_number'],
                employee_data['full_name'],
                employee_data['national_id'],
                employee_data['phone'],
                employee_data['email'],
                employee_data['address'],
                employee_data['department'],
                employee_data['position'],
                employee_data['hire_date'],
                employee_data['birth_date'],
                employee_data['basic_salary'],
                employee_data['status'],
                employee_data['notes']
            )

            self.db_cursor.execute(insert_sql, values)
            self.db_connection.commit()

            # إعادة تحميل البيانات
            self.load_employees_data()

            # مسح النموذج
            self.clear_form()

            self.show_success_message(f"تم إضافة الموظف {employee_data['full_name']} بنجاح")

        except sqlite3.IntegrityError as e:
            if "employee_number" in str(e):
                self.show_error_message("رقم الموظف موجود مسبقاً")
            elif "national_id" in str(e):
                self.show_error_message("رقم الهوية موجود مسبقاً")
            else:
                self.show_error_message("خطأ في البيانات المدخلة")
        except Exception as e:
            print(f"خطأ في إدراج الموظف: {e}")
            self.show_error_message(f"حدث خطأ في إضافة الموظف: {e}")

    def update_employee_data(self, employee_data):
        """تحديث بيانات موظف موجود"""
        try:
            update_sql = """
            UPDATE employees SET
                employee_number = ?, full_name = ?, national_id = ?, phone = ?,
                email = ?, address = ?, department = ?, position = ?,
                hire_date = ?, birth_date = ?, basic_salary = ?, status = ?,
                notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                employee_data['employee_number'],
                employee_data['full_name'],
                employee_data['national_id'],
                employee_data['phone'],
                employee_data['email'],
                employee_data['address'],
                employee_data['department'],
                employee_data['position'],
                employee_data['hire_date'],
                employee_data['birth_date'],
                employee_data['basic_salary'],
                employee_data['status'],
                employee_data['notes'],
                self.current_employee[0]  # ID
            )

            self.db_cursor.execute(update_sql, values)
            self.db_connection.commit()

            # إعادة تحميل البيانات
            self.load_employees_data()

            self.show_success_message(f"تم تحديث بيانات الموظف {employee_data['full_name']} بنجاح")

        except sqlite3.IntegrityError as e:
            if "employee_number" in str(e):
                self.show_error_message("رقم الموظف موجود مسبقاً")
            elif "national_id" in str(e):
                self.show_error_message("رقم الهوية موجود مسبقاً")
            else:
                self.show_error_message("خطأ في البيانات المدخلة")
        except Exception as e:
            print(f"خطأ في تحديث الموظف: {e}")
            self.show_error_message(f"حدث خطأ في تحديث الموظف: {e}")

    def update_employee(self):
        """تحديث الموظف الحالي"""
        if self.current_employee:
            self.save_employee()
        else:
            self.show_warning_message("لا يوجد موظف محدد للتحديث")

    def clear_form(self):
        """مسح النموذج"""
        try:
            for var in self.form_vars.values():
                var.set("")

            # إعادة تعيين الحالة الافتراضية
            self.form_vars['status'].set("نشط")

            # مسح الموظف الحالي
            self.current_employee = None

            # تحديث عنوان النموذج
            if hasattr(self, 'form_title_label') and self.form_title_label:
                self.form_title_label.configure(text="📝 نموذج بيانات الموظف المتطور")

            self.show_info_message("تم مسح النموذج")

        except Exception as e:
            print(f"خطأ في مسح النموذج: {e}")

    def cancel_operation(self):
        """إلغاء العملية"""
        try:
            self.clear_form()

            # مسح التحديد من الجدول
            if hasattr(self, 'tree') and self.tree:
                for item in self.tree.selection():
                    self.tree.selection_remove(item)

            self.show_info_message("تم إلغاء العملية")

        except Exception as e:
            print(f"خطأ في إلغاء العملية: {e}")

    def generate_employee_number(self):
        """توليد رقم موظف جديد"""
        try:
            # الحصول على السنة الحالية
            current_year = datetime.now().year

            # البحث عن آخر رقم موظف في السنة الحالية
            self.db_cursor.execute("""
                SELECT employee_number FROM employees
                WHERE employee_number LIKE ?
                ORDER BY employee_number DESC LIMIT 1
            """, (f"EMP{current_year}%",))

            result = self.db_cursor.fetchone()

            if result:
                # استخراج الرقم التسلسلي
                last_number = result[0]
                sequence = int(last_number.split(str(current_year))[1]) + 1
            else:
                sequence = 1

            # تكوين رقم الموظف الجديد
            new_number = f"EMP{current_year}{sequence:03d}"
            self.form_vars['employee_number'].set(new_number)

        except Exception as e:
            print(f"خطأ في توليد رقم الموظف: {e}")
            # رقم افتراضي
            self.form_vars['employee_number'].set(f"EMP{datetime.now().year}001")

    # ==================== وظائف إضافية ====================

    def refresh_dashboard(self):
        """تحديث لوحة المعلومات"""
        try:
            self.load_employees_data()
            self.show_success_message("تم تحديث البيانات بنجاح")
        except Exception as e:
            print(f"خطأ في تحديث لوحة المعلومات: {e}")
            self.show_error_message(f"حدث خطأ في تحديث البيانات: {e}")

    def analyze_performance(self):
        """تحليل الأداء"""
        self.show_info_message("ميزة تحليل الأداء قيد التطوير")

    def manage_salaries(self):
        """إدارة الرواتب"""
        self.show_info_message("ميزة إدارة الرواتب قيد التطوير")

    def generate_reports(self):
        """إنشاء التقارير"""
        self.show_info_message("ميزة التقارير قيد التطوير")

    # ==================== وظائف الرسائل المحسنة ====================

    def show_success_message(self, message):
        """إظهار رسالة نجاح"""
        self.show_custom_message(message, "نجاح", "success")

    def show_error_message(self, message):
        """إظهار رسالة خطأ"""
        self.show_custom_message(message, "خطأ", "error")

    def show_warning_message(self, message):
        """إظهار رسالة تحذير"""
        self.show_custom_message(message, "تحذير", "warning")

    def show_info_message(self, message):
        """إظهار رسالة معلومات"""
        self.show_custom_message(message, "معلومات", "info")

    def show_custom_message(self, message, title, msg_type):
        """إظهار رسالة مخصصة"""
        try:
            if msg_type == "success":
                messagebox.showinfo(title, message)
            elif msg_type == "error":
                messagebox.showerror(title, message)
            elif msg_type == "warning":
                messagebox.showwarning(title, message)
            else:
                messagebox.showinfo(title, message)
        except Exception as e:
            print(f"خطأ في إظهار الرسالة: {e}")

    def __del__(self):
        """تنظيف الموارد"""
        try:
            if hasattr(self, 'db_connection') and self.db_connection:
                self.db_connection.close()
        except Exception as e:
            print(f"خطأ في إغلاق قاعدة البيانات: {e}")

# ==================== تشغيل النافذة ====================

def main():
    """الدالة الرئيسية لتشغيل النافذة"""
    try:
        print("🚀 بدء تشغيل نافذة إدارة الموظفين المحسنة...")

        app = EnhancedEmployeesWindow()

        if app.window:
            print("✅ تم إنشاء النافذة بنجاح")
            app.window.mainloop()
        else:
            print("❌ فشل في إنشاء النافذة")

    except Exception as e:
        print(f"❌ خطأ في تشغيل النافذة: {e}")
        messagebox.showerror("خطأ", f"حدث خطأ في تشغيل النافذة: {e}")

if __name__ == "__main__":
    main()
