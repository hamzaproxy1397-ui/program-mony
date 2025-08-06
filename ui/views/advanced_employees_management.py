#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 نافذة إدارة الموظفين المتقدمة والذكية - الإصدار المحسن
Advanced Smart Employee Management Window - Enhanced Version

نافذة احترافية ومتقدمة تتضمن:
- تصميم Material Design مع ألوان متدرجة
- خوارزميات ذكية لإدارة الموظفين
- لوحة معلومات تفاعلية مع رسوم بيانية
- نظام تحليل الأداء والإنتاجية
- ميزات البحث المتقدم والفلترة الذكية
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
import numpy as np

# استيراد الثيمات والألوان
try:
    from themes.modern_theme import MODERN_COLORS, FONTS, DIMENSIONS
    from ui.window_utils import configure_window_fullscreen
    from database.hybrid_database_manager import HybridDatabaseManager
except ImportError as e:
    print(f"تحذير: لم يتم العثور على بعض الوحدات: {e}")

# إعداد customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# نظام الألوان المتقدم والمتدرج المحسن
ADVANCED_COLORS = {
    # الألوان الأساسية المتدرجة الجديدة - أكثر جمالاً وحيوية
    'primary_gradient': ['#6c5ce7', '#a29bfe'],  # بنفسجي عميق إلى بنفسجي فاتح
    'secondary_gradient': ['#fd79a8', '#fdcb6e'],  # وردي إلى ذهبي
    'success_gradient': ['#00b894', '#55efc4'],  # أخضر زمردي إلى أخضر نعناعي
    'warning_gradient': ['#fdcb6e', '#e17055'],  # ذهبي إلى برتقالي
    'danger_gradient': ['#e84393', '#fd79a8'],  # وردي غامق إلى وردي فاتح
    'info_gradient': ['#74b9ff', '#0984e3'],  # أزرق سماوي إلى أزرق عميق

    # ألوان إضافية جميلة
    'emerald_gradient': ['#00b894', '#00cec9'],  # زمردي إلى تركوازي
    'sunset_gradient': ['#fab1a0', '#e17055'],  # خوخي إلى برتقالي
    'ocean_gradient': ['#74b9ff', '#0984e3'],  # أزرق محيطي
    'forest_gradient': ['#00b894', '#6c5ce7'],  # أخضر غابات إلى بنفسجي
    'royal_gradient': ['#a29bfe', '#6c5ce7'],  # بنفسجي ملكي
    'fire_gradient': ['#fd79a8', '#e84393'],  # وردي ناري

    # ألوان الخلفية المتدرجة المحسنة
    'background_gradient': ['#ddd6fe', '#e0e7ff'],  # بنفسجي فاتح إلى أزرق فاتح
    'card_gradient': ['#ffffff', '#f8fafc'],  # أبيض نقي إلى رمادي فاتح جداً
    'sidebar_gradient': ['#6366f1', '#8b5cf6'],  # إنديجو إلى بنفسجي

    # ألوان النصوص المحسنة
    'text_primary': '#1e293b',      # رمادي غامق أنيق
    'text_secondary': '#64748b',    # رمادي متوسط
    'text_accent': '#3b82f6',       # أزرق لامع
    'text_white': '#ffffff',        # أبيض نقي
    'text_gold': '#f59e0b',         # ذهبي
    'text_emerald': '#10b981',      # زمردي

    # ألوان الحالة المحسنة والجميلة
    'status_active': '#10b981',     # أخضر زمردي
    'status_inactive': '#ef4444',   # أحمر لامع
    'status_pending': '#f59e0b',    # ذهبي
    'status_suspended': '#8b5cf6',  # بنفسجي
    'status_excellent': '#059669',  # أخضر ممتاز
    'status_good': '#0ea5e9',       # أزرق جيد

    # ألوان الظلال المحسنة
    'shadow_light': '#f1f5f9',      # ظل فاتح
    'shadow_medium': '#e2e8f0',     # ظل متوسط
    'shadow_dark': '#cbd5e1',       # ظل غامق
}

# إعدادات التأثيرات البصرية المحسنة
VISUAL_EFFECTS = {
    'corner_radius': 20,           # زوايا أكثر استدارة
    'shadow_blur': 15,             # ظلال أكثر نعومة
    'animation_duration': 400,      # حركة أكثر سلاسة
    'hover_scale': 1.08,           # تكبير أكثر وضوحاً
    'transition_ease': 'ease-in-out'
}

# إعدادات الخطوط المحسنة والمكبرة
ENHANCED_FONTS = {
    'title_large': ('Arial', 36, 'bold'),      # عناوين كبيرة
    'title_medium': ('Arial', 28, 'bold'),     # عناوين متوسطة
    'title_small': ('Arial', 22, 'bold'),      # عناوين صغيرة
    'header': ('Arial', 20, 'bold'),           # رؤوس الأقسام
    'subheader': ('Arial', 18, 'bold'),        # رؤوس فرعية
    'button_large': ('Arial', 16, 'bold'),     # أزرار كبيرة
    'button_medium': ('Arial', 14, 'bold'),    # أزرار متوسطة
    'button_small': ('Arial', 12, 'bold'),     # أزرار صغيرة
    'text_large': ('Arial', 16),               # نص كبير
    'text_medium': ('Arial', 14),              # نص متوسط
    'text_small': ('Arial', 12),               # نص صغير
    'label': ('Arial', 14, 'bold'),            # تسميات
    'input': ('Arial', 14),                    # حقول الإدخال
}

# إعدادات الأبعاد المحسنة
ENHANCED_DIMENSIONS = {
    'button_height_large': 55,      # ارتفاع الأزرار الكبيرة
    'button_height_medium': 45,     # ارتفاع الأزرار المتوسطة
    'button_height_small': 35,      # ارتفاع الأزرار الصغيرة
    'button_width_large': 180,      # عرض الأزرار الكبيرة
    'button_width_medium': 140,     # عرض الأزرار المتوسطة
    'button_width_small': 100,      # عرض الأزرار الصغيرة
    'input_height': 45,             # ارتفاع حقول الإدخال
    'header_height': 120,           # ارتفاع الهيدر
    'toolbar_height': 90,           # ارتفاع شريط الأدوات
    'dashboard_height': 250,        # ارتفاع لوحة المعلومات
}

class SmartEmployeeAnalytics:
    """فئة التحليلات الذكية للموظفين"""
    
    def __init__(self):
        self.performance_weights = {
            'attendance': 0.3,
            'productivity': 0.4,
            'teamwork': 0.2,
            'innovation': 0.1
        }
    
    def suggest_salary(self, position: str, experience_years: int, performance_score: float = 0.8) -> float:
        """خوارزمية ذكية لاقتراح الراتب المناسب"""
        base_salaries = {
            'مدير عام': 20000,
            'مدير قسم': 15000,
            'محاسب أول': 10000,
            'محاسب': 8000,
            'موظف مبيعات': 6000,
            'مطور': 12000,
            'سكرتير': 5000,
            'موظف': 4000
        }
        
        base_salary = base_salaries.get(position, 4000)
        
        # تطبيق معادلة ذكية للراتب
        experience_multiplier = 1 + (experience_years * 0.05)  # 5% زيادة لكل سنة خبرة
        performance_multiplier = 0.8 + (performance_score * 0.4)  # من 80% إلى 120% حسب الأداء
        
        suggested_salary = base_salary * experience_multiplier * performance_multiplier
        
        return round(suggested_salary, 2)
    
    def analyze_performance(self, employee_data: Dict) -> Dict:
        """تحليل أداء الموظف بناءً على البيانات المتاحة"""
        analysis = {
            'overall_score': 0.0,
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        # محاكاة تحليل الأداء (في التطبيق الحقيقي سيتم استخدام بيانات فعلية)
        attendance_score = random.uniform(0.7, 1.0)
        productivity_score = random.uniform(0.6, 1.0)
        teamwork_score = random.uniform(0.8, 1.0)
        innovation_score = random.uniform(0.5, 0.9)
        
        # حساب النتيجة الإجمالية
        analysis['overall_score'] = (
            attendance_score * self.performance_weights['attendance'] +
            productivity_score * self.performance_weights['productivity'] +
            teamwork_score * self.performance_weights['teamwork'] +
            innovation_score * self.performance_weights['innovation']
        )
        
        # تحديد نقاط القوة والضعف
        if attendance_score > 0.9:
            analysis['strengths'].append('حضور ممتاز')
        elif attendance_score < 0.8:
            analysis['weaknesses'].append('حضور يحتاج تحسين')
            
        if productivity_score > 0.85:
            analysis['strengths'].append('إنتاجية عالية')
        elif productivity_score < 0.7:
            analysis['weaknesses'].append('إنتاجية منخفضة')
            
        if teamwork_score > 0.9:
            analysis['strengths'].append('عمل جماعي ممتاز')
            
        if innovation_score > 0.8:
            analysis['strengths'].append('مبدع ومبتكر')
        elif innovation_score < 0.6:
            analysis['weaknesses'].append('يحتاج تطوير الإبداع')
        
        # توصيات ذكية
        if analysis['overall_score'] > 0.9:
            analysis['recommendations'].append('مرشح للترقية')
            analysis['recommendations'].append('يمكن إسناد مسؤوليات إضافية')
        elif analysis['overall_score'] < 0.7:
            analysis['recommendations'].append('يحتاج برنامج تدريبي')
            analysis['recommendations'].append('متابعة دورية للأداء')
        
        return analysis
    
    def predict_attendance(self, historical_data: List) -> Dict:
        """التنبؤ بالحضور بناءً على البيانات التاريخية"""
        # محاكاة خوارزمية التنبؤ
        prediction = {
            'next_week_probability': random.uniform(0.85, 0.98),
            'risk_factors': [],
            'recommendations': []
        }
        
        # تحليل المخاطر
        if prediction['next_week_probability'] < 0.9:
            prediction['risk_factors'].append('انخفاض في معدل الحضور مؤخراً')
            prediction['recommendations'].append('متابعة مع الموظف')
        
        return prediction
    
    def optimize_task_distribution(self, employees: List, tasks: List) -> Dict:
        """خوارزمية ذكية لتوزيع المهام على الموظفين"""
        distribution = {}
        
        # محاكاة خوارزمية التوزيع الذكي
        for i, task in enumerate(tasks):
            # اختيار الموظف الأنسب بناءً على المهارات والحمولة
            best_employee = employees[i % len(employees)] if employees else None
            if best_employee:
                if best_employee not in distribution:
                    distribution[best_employee] = []
                distribution[best_employee].append(task)
        
        return distribution

class AdvancedEmployeesManagement:
    """نافذة إدارة الموظفين المتقدمة والذكية"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.db_manager = None
        
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
        
        # نظام التحليلات الذكية
        self.analytics = SmartEmployeeAnalytics()
        
        # متغيرات التأثيرات البصرية
        self.animation_running = False
        self.hover_effects = {}
        
        # إنشاء النافذة
        self.create_window()
        
        # تهيئة قاعدة البيانات
        self.init_database()
        
        # تحميل البيانات
        self.load_employees_data_smart()
        
        # بدء التحديثات الذكية
        self.start_smart_updates()
    
    def create_window(self):
        """إنشاء النافذة الرئيسية المحسنة"""
        try:
            self.window = ctk.CTkToplevel(self.parent) if self.parent else ctk.CTk()
            self.window.title("🚀 إدارة الموظفين الذكية - الإصدار المتقدم")
            
            # تكوين النافذة المحسنة
            try:
                configure_window_fullscreen(self.window)
            except:
                self.window.geometry("1800x1000")  # زيادة العرض من 1600 إلى 1800 (+12.5%)
                self.window.minsize(1400, 900)     # حد أدنى محسن
                self.window.state('zoomed')
            
            # تطبيق الخلفية المتدرجة
            self.apply_gradient_background()
            
            # جعل النافذة في المقدمة
            if self.parent:
                self.window.transient(self.parent)
                self.window.grab_set()
            
            # إنشاء المحتوى المحسن
            self.create_enhanced_content()
            
            # تطبيق التأثيرات البصرية
            self.apply_visual_effects()
            
        except Exception as e:
            print(f"خطأ في إنشاء النافذة: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء النافذة: {e}")
    
    def apply_gradient_background(self):
        """تطبيق خلفية متدرجة للنافذة"""
        # تطبيق لون خلفية أساسي (سيتم تحسينه لاحقاً مع Canvas)
        self.window.configure(fg_color="#f8f9fa")
    
    def create_enhanced_content(self):
        """إنشاء المحتوى المحسن"""
        # الإطار الرئيسي مع تأثيرات بصرية
        main_frame = ctk.CTkFrame(
            self.window, 
            fg_color="transparent",
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # إنشاء الهيدر المحسن
        self.create_enhanced_header(main_frame)
        
        # إنشاء لوحة المعلومات التفاعلية
        self.create_dashboard(main_frame)
        
        # إنشاء شريط الأدوات المحسن
        self.create_enhanced_toolbar(main_frame)
        
        # إنشاء المحتوى الرئيسي المحسن
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(15, 0))
        
        # تقسيم المحتوى مع تحسينات
        self.create_enhanced_content_sections(content_frame)
    
    def create_enhanced_header(self, parent):
        """إنشاء الهيدر المحسن مع تدرجات لونية جميلة"""
        header_frame = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['header_height'],
            fg_color=ADVANCED_COLORS['royal_gradient'][0],  # بنفسجي ملكي
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # إضافة تأثير الظل (محاكاة)
        shadow_frame = ctk.CTkFrame(
            parent,
            height=5,
            fg_color="#e0e0e0",
            corner_radius=0
        )
        shadow_frame.place(in_=header_frame, relx=0, rely=1, relwidth=1)
        
        # المحتوى الرئيسي للهيدر المحسن
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=25)

        # الجانب الأيسر - العنوان والوصف المحسن
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y")

        # عنوان محسن مع أيقونة أكبر وأجمل
        title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_frame.pack(anchor="w")

        title_label = ctk.CTkLabel(
            title_frame,
            text="🚀 إدارة الموظفين الذكية والمتطورة",
            font=ENHANCED_FONTS['title_large'],  # خط أكبر
            text_color=ADVANCED_COLORS['text_white']
        )
        title_label.pack(side="left")

        # وصف محسن بخط أكبر
        subtitle_label = ctk.CTkLabel(
            left_frame,
            text="💎 نظام متقدم وذكي لإدارة الموظفين مع تحليلات الأداء والتنبؤات المستقبلية",
            font=ENHANCED_FONTS['text_large'],  # خط أكبر
            text_color="#f1f5f9"  # لون أفتح وأجمل
        )
        subtitle_label.pack(anchor="w", pady=(8, 0))
        
        # الجانب الأيمن - الإحصائيات المحسنة
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        # إنشاء بطاقات الإحصائيات
        self.create_stats_cards(right_frame)
    
    def create_stats_cards(self, parent):
        """إنشاء بطاقات الإحصائيات المحسنة"""
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="both", expand=True)
        
        # بيانات الإحصائيات المحسنة مع ألوان جميلة
        stats_data = [
            ("👥", "إجمالي الموظفين", "0", ADVANCED_COLORS['emerald_gradient'][0]),
            ("✅", "الموظفين النشطين", "0", ADVANCED_COLORS['success_gradient'][0]),
            ("📊", "متوسط الأداء", "87%", ADVANCED_COLORS['ocean_gradient'][0]),
            ("🎯", "معدل الحضور", "94%", ADVANCED_COLORS['sunset_gradient'][0])
        ]
        
        # إنشاء البطاقات في صفين
        for i, (icon, title, value, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            card_frame = ctk.CTkFrame(
                stats_container,
                width=170,  # أعرض
                height=85,  # أطول
                fg_color=color,
                corner_radius=18  # زوايا أكثر استدارة
            )
            card_frame.grid(row=row, column=col, padx=8, pady=4, sticky="nsew")
            card_frame.pack_propagate(False)
            
            # محتوى البطاقة المحسن
            content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=15, pady=12)

            # الأيقونة والقيمة المحسنة
            top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            top_frame.pack(fill="x")

            icon_label = ctk.CTkLabel(
                top_frame,
                text=icon,
                font=("Arial", 28),  # أيقونة أكبر
                text_color="white"
            )
            icon_label.pack(side="left")

            value_label = ctk.CTkLabel(
                top_frame,
                text=value,
                font=ENHANCED_FONTS['title_small'],  # خط أكبر وأجمل
                text_color="white"
            )
            value_label.pack(side="right")

            # العنوان المحسن
            title_label = ctk.CTkLabel(
                content_frame,
                text=title,
                font=ENHANCED_FONTS['text_medium'],  # خط أكبر
                text_color="#f8fafc"  # لون أجمل
            )
            title_label.pack(anchor="w")
            
            # حفظ مرجع للتحديث اللاحق
            if title == "إجمالي الموظفين":
                self.total_employees_label = value_label
            elif title == "النشطين":
                self.active_employees_label = value_label

    def create_dashboard(self, parent):
        """إنشاء لوحة المعلومات التفاعلية المحسنة"""
        dashboard_frame = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['dashboard_height'],  # أطول
            fg_color=ADVANCED_COLORS['card_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        dashboard_frame.pack(fill="x", pady=(0, 20))
        dashboard_frame.pack_propagate(False)

        # عنوان لوحة المعلومات
        title_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent", height=40)
        title_frame.pack(fill="x", padx=20, pady=(15, 0))
        title_frame.pack_propagate(False)

        dashboard_title = ctk.CTkLabel(
            title_frame,
            text="📊 لوحة المعلومات التفاعلية والذكية",
            font=ENHANCED_FONTS['title_medium'],  # خط أكبر
            text_color=ADVANCED_COLORS['text_primary']
        )
        dashboard_title.pack(side="left", pady=12)

        # زر تحديث البيانات المحسن
        refresh_btn = ctk.CTkButton(
            title_frame,
            text="🔄 تحديث البيانات",
            command=self.refresh_dashboard,
            width=ENHANCED_DIMENSIONS['button_width_medium'],  # أعرض
            height=ENHANCED_DIMENSIONS['button_height_medium'],  # أطول
            font=ENHANCED_FONTS['button_medium'],  # خط أكبر
            fg_color=ADVANCED_COLORS['ocean_gradient'][0],
            hover_color=ADVANCED_COLORS['ocean_gradient'][1],
            corner_radius=18  # زوايا أكثر استدارة
        )
        refresh_btn.pack(side="right", pady=12)

        # محتوى لوحة المعلومات
        content_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # تقسيم لوحة المعلومات إلى أقسام
        self.create_dashboard_sections(content_frame)

    def create_dashboard_sections(self, parent):
        """إنشاء أقسام لوحة المعلومات"""
        # القسم الأيسر - الرسوم البيانية
        left_section = ctk.CTkFrame(
            parent,
            fg_color=ADVANCED_COLORS['background_gradient'][0],
            corner_radius=12
        )
        left_section.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # عنوان القسم
        chart_title = ctk.CTkLabel(
            left_section,
            text="📈 توزيع الموظفين حسب الأقسام",
            font=("Arial", 14, "bold"),
            text_color=ADVANCED_COLORS['text_primary']
        )
        chart_title.pack(pady=(15, 10))

        # منطقة الرسم البياني (محاكاة)
        chart_frame = ctk.CTkFrame(left_section, fg_color="white", corner_radius=8)
        chart_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # إنشاء رسم بياني بسيط
        self.create_simple_chart(chart_frame)

        # القسم الأوسط - التحليلات الذكية
        middle_section = ctk.CTkFrame(
            parent,
            fg_color=ADVANCED_COLORS['background_gradient'][1],
            corner_radius=12
        )
        middle_section.pack(side="left", fill="both", expand=True, padx=5)

        # عنوان القسم
        analytics_title = ctk.CTkLabel(
            middle_section,
            text="🧠 التحليلات الذكية",
            font=("Arial", 14, "bold"),
            text_color=ADVANCED_COLORS['text_primary']
        )
        analytics_title.pack(pady=(15, 10))

        # محتوى التحليلات
        self.create_analytics_content(middle_section)

        # القسم الأيمن - الإشعارات والتنبيهات
        right_section = ctk.CTkFrame(
            parent,
            fg_color=ADVANCED_COLORS['info_gradient'][0],
            corner_radius=12
        )
        right_section.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # عنوان القسم
        notifications_title = ctk.CTkLabel(
            right_section,
            text="🔔 التنبيهات الذكية",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        notifications_title.pack(pady=(15, 10))

        # محتوى التنبيهات
        self.create_notifications_content(right_section)

    def create_simple_chart(self, parent):
        """إنشاء رسم بياني بسيط"""
        # محاكاة بيانات الرسم البياني
        departments = ["الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية"]
        values = [15, 25, 30, 20, 10]  # نسب مئوية
        colors = [
            ADVANCED_COLORS['primary_gradient'][0],
            ADVANCED_COLORS['success_gradient'][0],
            ADVANCED_COLORS['warning_gradient'][0],
            ADVANCED_COLORS['secondary_gradient'][0],
            ADVANCED_COLORS['info_gradient'][0]
        ]

        # إنشاء عناصر الرسم البياني
        for i, (dept, value, color) in enumerate(zip(departments, values, colors)):
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=2)

            # اسم القسم
            dept_label = ctk.CTkLabel(
                row_frame,
                text=dept,
                font=("Arial", 10),
                text_color=ADVANCED_COLORS['text_secondary'],
                width=80
            )
            dept_label.pack(side="left")

            # شريط التقدم
            progress_frame = ctk.CTkFrame(row_frame, fg_color="#e0e0e0", corner_radius=5)
            progress_frame.pack(side="left", fill="x", expand=True, padx=(10, 5))

            progress_bar = ctk.CTkFrame(
                progress_frame,
                fg_color=color,
                corner_radius=5,
                width=max(10, int(float(value) * 1.5)),  # تحويل النسبة إلى عرض مع حد أدنى
                height=15
            )
            progress_bar.pack(side="left", pady=2, padx=2)
            progress_bar.pack_propagate(False)

            # القيمة
            value_label = ctk.CTkLabel(
                row_frame,
                text=f"{value}%",
                font=("Arial", 10, "bold"),
                text_color=ADVANCED_COLORS['text_primary'],
                width=40
            )
            value_label.pack(side="right")

    def create_analytics_content(self, parent):
        """إنشاء محتوى التحليلات الذكية"""
        analytics_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        analytics_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # تحليلات ذكية محاكاة
        analytics_data = [
            ("🎯", "متوسط الأداء العام", "87.5%", "ممتاز"),
            ("📈", "نمو الإنتاجية", "+12%", "إيجابي"),
            ("⏰", "معدل الحضور", "94.2%", "جيد جداً"),
            ("💡", "مؤشر الابتكار", "78%", "جيد")
        ]

        for icon, metric, value, status in analytics_data:
            metric_frame = ctk.CTkFrame(analytics_frame, fg_color="transparent")
            metric_frame.pack(fill="x", padx=10, pady=5)

            # الأيقونة
            icon_label = ctk.CTkLabel(
                metric_frame,
                text=icon,
                font=("Arial", 16),
                width=30
            )
            icon_label.pack(side="left")

            # المقياس
            metric_label = ctk.CTkLabel(
                metric_frame,
                text=metric,
                font=("Arial", 10),
                text_color=ADVANCED_COLORS['text_secondary']
            )
            metric_label.pack(side="left", padx=(5, 0))

            # القيمة والحالة
            value_frame = ctk.CTkFrame(metric_frame, fg_color="transparent")
            value_frame.pack(side="right")

            value_label = ctk.CTkLabel(
                value_frame,
                text=value,
                font=("Arial", 12, "bold"),
                text_color=ADVANCED_COLORS['text_primary']
            )
            value_label.pack(side="top")

            status_label = ctk.CTkLabel(
                value_frame,
                text=status,
                font=("Arial", 8),
                text_color=ADVANCED_COLORS['status_active']
            )
            status_label.pack(side="bottom")

    def create_notifications_content(self, parent):
        """إنشاء محتوى التنبيهات الذكية"""
        notifications_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="white",
            corner_radius=8
        )
        notifications_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # تنبيهات ذكية محاكاة
        notifications = [
            ("🎂", "عيد ميلاد أحمد محمد غداً", "تذكير"),
            ("📅", "انتهاء فترة تجربة 3 موظفين", "مهم"),
            ("⚠️", "انخفاض حضور قسم المبيعات", "تحذير"),
            ("🏆", "فاطمة حسن حققت أداء متميز", "إنجاز"),
            ("📊", "حان وقت تقييم الأداء الشهري", "مهمة")
        ]

        for icon, message, type_msg in notifications:
            notif_frame = ctk.CTkFrame(
                notifications_frame,
                fg_color="white",
                corner_radius=6,
                height=50
            )
            notif_frame.pack(fill="x", pady=3)
            notif_frame.pack_propagate(False)

            # محتوى التنبيه
            content_frame = ctk.CTkFrame(notif_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=8, pady=5)

            # الأيقونة
            icon_label = ctk.CTkLabel(
                content_frame,
                text=icon,
                font=("Arial", 14),
                width=25
            )
            icon_label.pack(side="left")

            # النص
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

            message_label = ctk.CTkLabel(
                text_frame,
                text=message,
                font=("Arial", 9),
                text_color=ADVANCED_COLORS['text_primary'],
                anchor="w"
            )
            message_label.pack(anchor="w")

            type_label = ctk.CTkLabel(
                text_frame,
                text=type_msg,
                font=("Arial", 7),
                text_color=ADVANCED_COLORS['text_secondary'],
                anchor="w"
            )
            type_label.pack(anchor="w")

    def refresh_dashboard(self):
        """تحديث لوحة المعلومات"""
        # محاكاة تحديث البيانات
        print("🔄 تحديث لوحة المعلومات...")
        # هنا يمكن إضافة كود تحديث البيانات الفعلية

    def create_enhanced_toolbar(self, parent):
        """إنشاء شريط الأدوات المحسن والجميل"""
        toolbar_frame = ctk.CTkFrame(
            parent,
            height=ENHANCED_DIMENSIONS['toolbar_height'],  # أطول
            fg_color=ADVANCED_COLORS['card_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        toolbar_frame.pack(fill="x", pady=(0, 20))
        toolbar_frame.pack_propagate(False)

        # الجانب الأيسر - أزرار العمليات المحسنة والجميلة
        left_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=25, pady=18)

        # أزرار العمليات الرئيسية مع تصميم محسن وألوان جميلة
        buttons_data = [
            ("➕", "إضافة موظف جديد", self.add_employee_smart, ADVANCED_COLORS['emerald_gradient']),
            ("✏️", "تعديل ذكي", self.edit_employee_smart, ADVANCED_COLORS['ocean_gradient']),
            ("🗑️", "حذف آمن", self.delete_employee_safe, ADVANCED_COLORS['fire_gradient']),
            ("📊", "تحليل الأداء", self.analyze_performance, ADVANCED_COLORS['sunset_gradient']),
            ("💰", "إدارة الرواتب", self.manage_salaries_smart, ADVANCED_COLORS['forest_gradient']),
            ("🤖", "اقتراحات ذكية", self.show_smart_suggestions, ADVANCED_COLORS['royal_gradient'])
        ]

        for icon, text, command, gradient in buttons_data:
            btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
            btn_frame.pack(side="left", padx=12)

            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}\n{text}",
                command=command,
                width=ENHANCED_DIMENSIONS['button_width_medium'],  # أعرض
                height=ENHANCED_DIMENSIONS['button_height_medium'] + 10,  # أطول
                font=ENHANCED_FONTS['button_medium'],  # خط أكبر
                fg_color=gradient[0],
                hover_color=gradient[1],
                corner_radius=20,  # زوايا أكثر استدارة
                text_color="white",
                text_color_disabled="gray"
            )
            btn.pack()

            # إضافة تأثير الظل المحسن
            shadow = ctk.CTkFrame(
                btn_frame,
                width=ENHANCED_DIMENSIONS['button_width_medium'],
                height=4,  # ظل أكثر وضوحاً
                fg_color=ADVANCED_COLORS['shadow_medium'],
                corner_radius=20
            )
            shadow.place(in_=btn, relx=0, rely=1, y=3)

        # الجانب الأيمن - البحث والفلترة المتقدمة والجميلة
        right_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=25, pady=18)

        # شريط البحث الذكي المحسن
        search_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=18)

        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Arial", 22),  # أيقونة أكبر
            text_color=ADVANCED_COLORS['text_primary']
        )
        search_label.pack(side="left", padx=(0, 8))

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_smart_search)

        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="🔎 بحث ذكي في جميع بيانات الموظفين...",
            width=300,  # أعرض
            height=ENHANCED_DIMENSIONS['input_height'],  # أطول
            font=ENHANCED_FONTS['input'],  # خط أكبر
            corner_radius=25,  # زوايا أكثر استدارة
            border_width=3,  # حدود أكثر وضوحاً
            border_color=ADVANCED_COLORS['royal_gradient'][0],
            fg_color="white",
            text_color=ADVANCED_COLORS['text_primary']
        )
        search_entry.pack(side="left")

        # فلاتر ذكية محسنة وجميلة
        filters_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        filters_frame.pack(side="right", padx=18)

        # فلتر القسم المحسن والجميل
        dept_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        dept_frame.pack(side="right", padx=12)

        dept_label = ctk.CTkLabel(
            dept_frame,
            text="🏢 القسم:",
            font=ENHANCED_FONTS['label'],  # خط أكبر
            text_color=ADVANCED_COLORS['text_primary']
        )
        dept_label.pack(side="left", padx=(0, 8))

        self.department_filter_var = ctk.StringVar(value="الكل")
        dept_combo = ctk.CTkComboBox(
            dept_frame,
            variable=self.department_filter_var,
            values=["الكل", "الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية", "التسويق"],
            width=160,  # أعرض
            height=ENHANCED_DIMENSIONS['input_height'],  # أطول
            font=ENHANCED_FONTS['input'],  # خط أكبر
            command=self.on_smart_filter,
            corner_radius=20,  # زوايا أكثر استدارة
            border_color=ADVANCED_COLORS['emerald_gradient'][0],
            fg_color="white",
            text_color=ADVANCED_COLORS['text_primary'],
            button_color=ADVANCED_COLORS['emerald_gradient'][0],
            button_hover_color=ADVANCED_COLORS['emerald_gradient'][1]
        )
        dept_combo.pack(side="left")

        # فلتر الحالة المحسن والجميل
        status_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        status_frame.pack(side="right", padx=12)

        status_label = ctk.CTkLabel(
            status_frame,
            text="📊 الحالة:",
            font=ENHANCED_FONTS['label'],  # خط أكبر
            text_color=ADVANCED_COLORS['text_primary']
        )
        status_label.pack(side="left", padx=(0, 8))

        self.status_filter_var = ctk.StringVar(value="الكل")
        status_combo = ctk.CTkComboBox(
            status_frame,
            variable=self.status_filter_var,
            values=["الكل", "نشط", "غير نشط", "معلق", "مستقيل"],
            width=140,  # أعرض
            height=ENHANCED_DIMENSIONS['input_height'],  # أطول
            font=ENHANCED_FONTS['input'],  # خط أكبر
            command=self.on_smart_filter,
            corner_radius=20,  # زوايا أكثر استدارة
            border_color=ADVANCED_COLORS['sunset_gradient'][0],
            fg_color="white",
            text_color=ADVANCED_COLORS['text_primary'],
            button_color=ADVANCED_COLORS['sunset_gradient'][0],
            button_hover_color=ADVANCED_COLORS['sunset_gradient'][1]
        )
        status_combo.pack(side="left")

    def create_enhanced_content_sections(self, parent):
        """إنشاء أقسام المحتوى المحسنة"""
        # تقسيم إلى ثلاثة أجزاء: جدول الموظفين، نموذج التفاصيل، لوحة التحليلات

        # الجزء الأيسر - جدول الموظفين المحسن
        left_frame = ctk.CTkFrame(
            parent,
            fg_color=ADVANCED_COLORS['card_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.create_enhanced_employees_table(left_frame)

        # الجزء الأوسط - نموذج التفاصيل المحسن
        middle_frame = ctk.CTkFrame(
            parent,
            fg_color=ADVANCED_COLORS['card_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius'],
            width=400
        )
        middle_frame.pack(side="left", fill="y", padx=4)
        middle_frame.pack_propagate(False)

        self.create_enhanced_employee_form(middle_frame)

        # الجزء الأيمن - لوحة التحليلات الذكية
        right_frame = ctk.CTkFrame(
            parent,
            fg_color=ADVANCED_COLORS['background_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius'],
            width=300
        )
        right_frame.pack(side="right", fill="y", padx=(8, 0))
        right_frame.pack_propagate(False)

        self.create_smart_analytics_panel(right_frame)

    def create_enhanced_employees_table(self, parent):
        """إنشاء جدول الموظفين المحسن"""
        # عنوان الجدول المحسن والجميل
        table_header = ctk.CTkFrame(
            parent,
            height=75,  # أطول
            fg_color=ADVANCED_COLORS['forest_gradient'][0],  # لون جميل
            corner_radius=(VISUAL_EFFECTS['corner_radius'], VISUAL_EFFECTS['corner_radius'], 0, 0)
        )
        table_header.pack(fill="x", padx=0, pady=(0, 0))
        table_header.pack_propagate(False)

        # محتوى الهيدر المحسن
        header_content = ctk.CTkFrame(table_header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=25, pady=18)

        title_label = ctk.CTkLabel(
            header_content,
            text="👥 قائمة الموظفين الذكية والمتطورة",
            font=ENHANCED_FONTS['title_small'],  # خط أكبر
            text_color="white"
        )
        title_label.pack(side="left")

        # مؤشر عدد النتائج المحسن
        self.results_label = ctk.CTkLabel(
            header_content,
            text="عرض 0 من 0 موظف",
            font=ENHANCED_FONTS['text_large'],  # خط أكبر
            text_color="#f1f5f9"  # لون أجمل
        )
        self.results_label.pack(side="right")

        # إطار الجدول المحسن
        table_frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=(0, 0, VISUAL_EFFECTS['corner_radius'], VISUAL_EFFECTS['corner_radius'])
        )
        table_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # إنشاء Treeview محسن
        columns = ("ID", "الرقم", "الاسم الكامل", "القسم", "المنصب", "الراتب", "الأداء", "الحالة")

        # إنشاء إطار للجدول مع شريط التمرير
        tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # إنشاء الجدول
        style = ttk.Style()
        style.theme_use("clam")

        # تخصيص ألوان الجدول
        style.configure("Treeview",
                       background="white",
                       foreground=ADVANCED_COLORS['text_primary'],
                       rowheight=35,
                       fieldbackground="white",
                       font=("Arial", 11))

        style.configure("Treeview.Heading",
                       background=ADVANCED_COLORS['primary_gradient'][0],
                       foreground="white",
                       font=("Arial", 12, "bold"))

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # تكوين الأعمدة المحسن
        column_configs = {
            "ID": {"width": 50, "anchor": "center"},
            "الرقم": {"width": 80, "anchor": "center"},
            "الاسم الكامل": {"width": 180, "anchor": "w"},
            "القسم": {"width": 120, "anchor": "center"},
            "المنصب": {"width": 140, "anchor": "center"},
            "الراتب": {"width": 100, "anchor": "center"},
            "الأداء": {"width": 80, "anchor": "center"},
            "الحالة": {"width": 80, "anchor": "center"}
        }

        for col, config in column_configs.items():
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=config["width"], anchor=config["anchor"])

        # أشرطة التمرير المحسنة
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # تخطيط الجدول
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # ربط الأحداث المحسنة
        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select_smart)
        self.tree.bind("<Double-1>", self.on_employee_double_click_smart)
        self.tree.bind("<Button-3>", self.show_context_menu)  # قائمة السياق

    def create_enhanced_employee_form(self, parent):
        """إنشاء نموذج تفاصيل الموظف المحسن"""
        # عنوان النموذج المحسن
        form_header = ctk.CTkFrame(
            parent,
            height=60,
            fg_color=ADVANCED_COLORS['secondary_gradient'][0],
            corner_radius=(VISUAL_EFFECTS['corner_radius'], VISUAL_EFFECTS['corner_radius'], 0, 0)
        )
        form_header.pack(fill="x")
        form_header.pack_propagate(False)

        # محتوى الهيدر
        header_content = ctk.CTkFrame(form_header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=15)

        self.form_title_label = ctk.CTkLabel(
            header_content,
            text="📝 نموذج الموظف الذكي",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        self.form_title_label.pack(side="left")

        # زر الاقتراحات الذكية
        smart_btn = ctk.CTkButton(
            header_content,
            text="🤖",
            command=self.show_smart_form_suggestions,
            width=30,
            height=30,
            font=("Arial", 14),
            fg_color="#f0f0f0",
            hover_color="#e0e0e0",
            corner_radius=15
        )
        smart_btn.pack(side="right")

        # إطار النموذج القابل للتمرير المحسن
        form_scroll_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="white",
            corner_radius=(0, 0, VISUAL_EFFECTS['corner_radius'], VISUAL_EFFECTS['corner_radius'])
        )
        form_scroll_frame.pack(fill="both", expand=True)

        # تهيئة متغيرات النموذج
        self.init_enhanced_form_variables()

        # إنشاء حقول النموذج المحسنة
        self.create_enhanced_form_fields(form_scroll_frame)

        # أزرار النموذج المحسنة
        self.create_enhanced_form_buttons(parent)

    def init_enhanced_form_variables(self):
        """تهيئة متغيرات النموذج المحسنة"""
        self.form_vars = {
            'employee_id': ctk.StringVar(),
            'employee_number': ctk.StringVar(),
            'full_name': ctk.StringVar(),
            'national_id': ctk.StringVar(),
            'phone': ctk.StringVar(),
            'email': ctk.StringVar(),
            'address': ctk.StringVar(),
            'department': ctk.StringVar(value="الإدارة"),
            'position': ctk.StringVar(value="موظف"),
            'hire_date': ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            'birth_date': ctk.StringVar(),
            'basic_salary': ctk.StringVar(value="0"),
            'suggested_salary': ctk.StringVar(value="0"),  # راتب مقترح ذكي
            'experience_years': ctk.StringVar(value="0"),  # سنوات الخبرة
            'performance_score': ctk.StringVar(value="80"),  # نقاط الأداء
            'skills': ctk.StringVar(),  # المهارات
            'status': ctk.StringVar(value="نشط"),
            'photo_path': ctk.StringVar(),
            'notes': ctk.StringVar()
        }

    def create_enhanced_form_fields(self, parent):
        """إنشاء حقول النموذج المحسنة"""
        # قسم الصورة الشخصية المحسن
        photo_section = ctk.CTkFrame(parent, fg_color="transparent")
        photo_section.pack(fill="x", pady=15, padx=20)

        photo_frame = ctk.CTkFrame(
            photo_section,
            fg_color=ADVANCED_COLORS['background_gradient'][0],
            corner_radius=15,
            width=120,
            height=140
        )
        photo_frame.pack()
        photo_frame.pack_propagate(False)

        self.photo_label = ctk.CTkLabel(
            photo_frame,
            text="📷\nصورة الموظف",
            width=100,
            height=120,
            fg_color="transparent",
            corner_radius=10,
            font=("Arial", 12)
        )
        self.photo_label.pack(pady=10)

        photo_btn = ctk.CTkButton(
            photo_section,
            text="📁 اختيار صورة شخصية",
            command=self.select_photo_enhanced,
            width=180,  # أعرض
            height=ENHANCED_DIMENSIONS['button_height_medium'],  # أطول
            font=ENHANCED_FONTS['button_medium'],  # خط أكبر
            fg_color=ADVANCED_COLORS['ocean_gradient'][0],
            hover_color=ADVANCED_COLORS['ocean_gradient'][1],
            corner_radius=18,  # زوايا أكثر استدارة
            text_color="white"
        )
        photo_btn.pack(pady=(15, 0))

        # الحقول الأساسية المحسنة
        sections = [
            ("👤 البيانات الشخصية", [
                ("رقم الموظف:", "employee_number", "entry", True),
                ("الاسم الكامل:", "full_name", "entry", True),
                ("الرقم القومي:", "national_id", "entry", False),
                ("تاريخ الميلاد:", "birth_date", "date", False)
            ]),
            ("📞 بيانات الاتصال", [
                ("رقم الهاتف:", "phone", "entry", False),
                ("البريد الإلكتروني:", "email", "entry", False),
                ("العنوان:", "address", "text", False)
            ]),
            ("💼 بيانات العمل", [
                ("القسم:", "department", "combo", True),
                ("المنصب:", "position", "combo", True),
                ("تاريخ التوظيف:", "hire_date", "date", True),
                ("سنوات الخبرة:", "experience_years", "number", False)
            ]),
            ("💰 الراتب والأداء", [
                ("الراتب الأساسي:", "basic_salary", "number", True),
                ("الراتب المقترح:", "suggested_salary", "display", False),
                ("نقاط الأداء:", "performance_score", "slider", False),
                ("الحالة:", "status", "combo", True)
            ]),
            ("🎯 المهارات والملاحظات", [
                ("المهارات:", "skills", "text", False),
                ("ملاحظات:", "notes", "text", False)
            ])
        ]

        for section_title, fields in sections:
            self.create_form_section(parent, section_title, fields)

    def create_form_section(self, parent, title, fields):
        """إنشاء قسم في النموذج"""
        # عنوان القسم
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_frame = ctk.CTkFrame(
            section_frame,
            fg_color=ADVANCED_COLORS['royal_gradient'][0],  # لون جميل
            corner_radius=15,  # زوايا أكثر استدارة
            height=50  # أطول
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=ENHANCED_FONTS['subheader'],  # خط أكبر
            text_color="white"
        )
        title_label.pack(pady=12)

        # حقول القسم
        fields_frame = ctk.CTkFrame(
            section_frame,
            fg_color=ADVANCED_COLORS['card_gradient'][1],
            corner_radius=10
        )
        fields_frame.pack(fill="x", pady=(5, 0))

        for label_text, var_name, field_type, required in fields:
            self.create_enhanced_form_field(fields_frame, label_text, var_name, field_type, required)

    def create_enhanced_form_field(self, parent, label_text, var_name, field_type, required=False):
        """إنشاء حقل نموذج محسن"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=8, padx=15)

        # التسمية مع مؤشر الحقل المطلوب
        label_frame = ctk.CTkFrame(field_frame, fg_color="transparent")
        label_frame.pack(fill="x", pady=(0, 5))

        label_text_display = f"{label_text} *" if required else label_text
        label_color = ADVANCED_COLORS['danger_gradient'][0] if required else ADVANCED_COLORS['text_primary']

        label = ctk.CTkLabel(
            label_frame,
            text=label_text_display,
            font=ENHANCED_FONTS['label'],  # خط أكبر
            text_color=label_color,
            anchor="w"
        )
        label.pack(side="left")

        # إنشاء الحقل حسب النوع مع تحسينات جميلة
        if field_type == "entry":
            widget = ctk.CTkEntry(
                field_frame,
                textvariable=self.form_vars[var_name],
                font=ENHANCED_FONTS['input'],  # خط أكبر
                height=ENHANCED_DIMENSIONS['input_height'],  # أطول
                corner_radius=15,  # زوايا أكثر استدارة
                border_width=3,  # حدود أكثر وضوحاً
                border_color=ADVANCED_COLORS['royal_gradient'][0] if required else ADVANCED_COLORS['shadow_medium'],
                fg_color="white",
                text_color=ADVANCED_COLORS['text_primary']
            )
        elif field_type == "text":
            widget = ctk.CTkTextbox(
                field_frame,
                height=75,  # أطول
                font=ENHANCED_FONTS['input'],  # خط أكبر
                corner_radius=15,  # زوايا أكثر استدارة
                border_width=3,  # حدود أكثر وضوحاً
                border_color=ADVANCED_COLORS['shadow_medium'],
                fg_color="white",
                text_color=ADVANCED_COLORS['text_primary']
            )
            widget.bind("<KeyRelease>", lambda e, var=var_name: self.update_text_var(var, widget))
        elif field_type == "combo":
            values = self.get_enhanced_combo_values(var_name)
            widget = ctk.CTkComboBox(
                field_frame,
                variable=self.form_vars[var_name],
                values=values,
                font=ENHANCED_FONTS['input'],  # خط أكبر
                height=ENHANCED_DIMENSIONS['input_height'],  # أطول
                corner_radius=15,  # زوايا أكثر استدارة
                border_width=3,  # حدود أكثر وضوحاً
                border_color=ADVANCED_COLORS['emerald_gradient'][0] if required else ADVANCED_COLORS['shadow_medium'],
                command=lambda value, var=var_name: self.on_combo_change(var, value),
                fg_color="white",
                text_color=ADVANCED_COLORS['text_primary'],
                button_color=ADVANCED_COLORS['emerald_gradient'][0],
                button_hover_color=ADVANCED_COLORS['emerald_gradient'][1]
            )
        elif field_type == "number":
            widget = ctk.CTkEntry(
                field_frame,
                textvariable=self.form_vars[var_name],
                font=ENHANCED_FONTS['input'],  # خط أكبر
                height=ENHANCED_DIMENSIONS['input_height'],  # أطول
                corner_radius=15,  # زوايا أكثر استدارة
                border_width=3,  # حدود أكثر وضوحاً
                border_color=ADVANCED_COLORS['sunset_gradient'][0],
                fg_color="white",
                text_color=ADVANCED_COLORS['text_primary']
            )
            widget.bind("<KeyRelease>", lambda e, var=var_name: self.on_number_change(var))
        elif field_type == "slider":
            widget = ctk.CTkSlider(
                field_frame,
                from_=0,
                to=100,
                variable=self.form_vars[var_name],
                width=250,  # أعرض
                height=25,  # أطول
                corner_radius=15,  # زوايا أكثر استدارة
                command=lambda value, var=var_name: self.on_slider_change(var, value),
                fg_color=ADVANCED_COLORS['shadow_light'],
                progress_color=ADVANCED_COLORS['ocean_gradient'][0],
                button_color=ADVANCED_COLORS['ocean_gradient'][1],
                button_hover_color=ADVANCED_COLORS['royal_gradient'][0]
            )
            # إضافة تسمية القيمة المحسنة
            value_label = ctk.CTkLabel(
                field_frame,
                text=f"{self.form_vars[var_name].get()}%",
                font=ENHANCED_FONTS['text_medium'],  # خط أكبر
                text_color=ADVANCED_COLORS['text_primary']
            )
            value_label.pack(side="right", padx=(15, 0))
            setattr(widget, 'value_label', value_label)
        elif field_type == "display":
            widget = ctk.CTkLabel(
                field_frame,
                textvariable=self.form_vars[var_name],
                font=ENHANCED_FONTS['button_medium'],  # خط أكبر وجريء
                text_color=ADVANCED_COLORS['emerald_gradient'][0],
                fg_color=ADVANCED_COLORS['background_gradient'][0],
                corner_radius=15,  # زوايا أكثر استدارة
                height=ENHANCED_DIMENSIONS['input_height']  # أطول
            )
        elif field_type == "date":
            widget = ctk.CTkEntry(
                field_frame,
                textvariable=self.form_vars[var_name],
                placeholder_text="📅 YYYY-MM-DD",
                font=ENHANCED_FONTS['input'],  # خط أكبر
                height=ENHANCED_DIMENSIONS['input_height'],  # أطول
                corner_radius=15,  # زوايا أكثر استدارة
                border_width=3,  # حدود أكثر وضوحاً
                border_color=ADVANCED_COLORS['ocean_gradient'][0],
                fg_color="white",
                text_color=ADVANCED_COLORS['text_primary']
            )

        widget.pack(fill="x")
        return widget

    def get_enhanced_combo_values(self, var_name):
        """الحصول على قيم القائمة المنسدلة المحسنة"""
        if var_name == "department":
            return ["الإدارة", "المحاسبة", "المبيعات", "التقنية", "الموارد البشرية", "التسويق", "الإنتاج"]
        elif var_name == "position":
            return ["مدير عام", "مدير قسم", "نائب مدير", "محاسب أول", "محاسب", "موظف مبيعات",
                   "مطور أول", "مطور", "مصمم", "سكرتير", "موظف", "متدرب"]
        elif var_name == "status":
            return ["نشط", "غير نشط", "معلق", "مستقيل", "في إجازة", "منتدب"]
        return []

    def on_combo_change(self, var_name, value):
        """عند تغيير قيمة القائمة المنسدلة"""
        if var_name == "position":
            # اقتراح راتب ذكي عند تغيير المنصب
            self.suggest_smart_salary()
        elif var_name == "department":
            # تحديث المناصب المتاحة حسب القسم
            self.update_positions_by_department(value)

    def on_number_change(self, var_name):
        """عند تغيير قيمة رقمية"""
        if var_name in ["basic_salary", "experience_years"]:
            # إعادة حساب الراتب المقترح
            self.suggest_smart_salary()

    def on_slider_change(self, var_name, value):
        """عند تغيير قيمة المنزلق"""
        if var_name == "performance_score":
            # تحديث تسمية القيمة
            widget = None
            for widget in self.form_vars[var_name].get():
                if hasattr(widget, 'value_label'):
                    widget.value_label.configure(text=f"{int(float(value))}%")
            # إعادة حساب الراتب المقترح
            self.suggest_smart_salary()

    def suggest_smart_salary(self):
        """اقتراح راتب ذكي"""
        try:
            position = self.form_vars['position'].get()
            experience = float(self.form_vars['experience_years'].get() or 0)
            performance = float(self.form_vars['performance_score'].get() or 80) / 100

            suggested = self.analytics.suggest_salary(position, experience, performance)
            self.form_vars['suggested_salary'].set(f"{suggested:,.0f} ج.م")
        except:
            self.form_vars['suggested_salary'].set("0 ج.م")

    def update_positions_by_department(self, department):
        """تحديث المناصب حسب القسم"""
        positions_by_dept = {
            "الإدارة": ["مدير عام", "نائب مدير", "سكرتير", "موظف إداري"],
            "المحاسبة": ["مدير مالي", "محاسب أول", "محاسب", "مساعد محاسب"],
            "المبيعات": ["مدير مبيعات", "موظف مبيعات أول", "موظف مبيعات", "مندوب مبيعات"],
            "التقنية": ["مدير تقني", "مطور أول", "مطور", "مصمم", "فني دعم"],
            "الموارد البشرية": ["مدير موارد بشرية", "أخصائي موارد بشرية", "موظف شؤون"],
            "التسويق": ["مدير تسويق", "أخصائي تسويق", "منسق تسويق"],
            "الإنتاج": ["مدير إنتاج", "مشرف إنتاج", "عامل ماهر", "عامل"]
        }
        # هذا يتطلب تحديث القائمة المنسدلة ديناميكياً

    def create_enhanced_form_buttons(self, parent):
        """إنشاء أزرار النموذج المحسنة والجميلة"""
        buttons_frame = ctk.CTkFrame(
            parent,
            height=85,  # أطول
            fg_color=ADVANCED_COLORS['card_gradient'][0],
            corner_radius=(0, 0, VISUAL_EFFECTS['corner_radius'], VISUAL_EFFECTS['corner_radius'])
        )
        buttons_frame.pack(fill="x")
        buttons_frame.pack_propagate(False)

        # إطار الأزرار المحسن
        btn_container = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        btn_container.pack(fill="both", expand=True, padx=25, pady=18)

        # أزرار العمليات المحسنة مع ألوان جميلة
        buttons_data = [
            ("💾", "حفظ ذكي", self.save_employee_smart, ADVANCED_COLORS['emerald_gradient']),
            ("🤖", "تحليل الأداء", self.analyze_current_employee, ADVANCED_COLORS['ocean_gradient']),
            ("🗑️", "مسح النموذج", self.clear_form_smart, ADVANCED_COLORS['sunset_gradient']),
            ("❌", "إلغاء العملية", self.cancel_operation_smart, ADVANCED_COLORS['fire_gradient'])
        ]

        for icon, text, command, gradient in buttons_data:
            btn = ctk.CTkButton(
                btn_container,
                text=f"{icon} {text}",
                command=command,
                width=ENHANCED_DIMENSIONS['button_width_medium'],  # أعرض
                height=ENHANCED_DIMENSIONS['button_height_medium'],  # أطول
                font=ENHANCED_FONTS['button_medium'],  # خط أكبر
                fg_color=gradient[0],
                hover_color=gradient[1],
                corner_radius=18,  # زوايا أكثر استدارة
                text_color="white"
            )
            btn.pack(side="left", padx=12, expand=True)

    def create_smart_analytics_panel(self, parent):
        """إنشاء لوحة التحليلات الذكية"""
        # عنوان اللوحة
        panel_header = ctk.CTkFrame(
            parent,
            height=60,
            fg_color=ADVANCED_COLORS['warning_gradient'][0],
            corner_radius=(VISUAL_EFFECTS['corner_radius'], VISUAL_EFFECTS['corner_radius'], 0, 0)
        )
        panel_header.pack(fill="x")
        panel_header.pack_propagate(False)

        header_content = ctk.CTkFrame(panel_header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=15)

        title_label = ctk.CTkLabel(
            header_content,
            text="🧠 التحليلات الذكية",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        title_label.pack(side="left")

        # محتوى اللوحة
        panel_content = ctk.CTkScrollableFrame(
            parent,
            fg_color="white",
            corner_radius=(0, 0, VISUAL_EFFECTS['corner_radius'], VISUAL_EFFECTS['corner_radius'])
        )
        panel_content.pack(fill="both", expand=True)

        # أقسام التحليلات
        self.create_performance_analysis(panel_content)
        self.create_predictions_section(panel_content)
        self.create_recommendations_section(panel_content)

    def create_performance_analysis(self, parent):
        """إنشاء قسم تحليل الأداء"""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=15, padx=15)

        # عنوان القسم
        title_frame = ctk.CTkFrame(
            section_frame,
            fg_color=ADVANCED_COLORS['success_gradient'][0],
            corner_radius=8,
            height=30
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame,
            text="📊 تحليل الأداء",
            font=("Arial", 12, "bold"),
            text_color="white"
        )
        title_label.pack(pady=5)

        # محتوى التحليل
        analysis_frame = ctk.CTkFrame(
            section_frame,
            fg_color=ADVANCED_COLORS['background_gradient'][0],
            corner_radius=8
        )
        analysis_frame.pack(fill="x", pady=(5, 0))

        # مؤشرات الأداء
        self.performance_indicators = {}
        indicators = [
            ("🎯", "النتيجة الإجمالية", "overall_score"),
            ("📈", "الإنتاجية", "productivity"),
            ("⏰", "الحضور", "attendance"),
            ("🤝", "العمل الجماعي", "teamwork"),
            ("💡", "الابتكار", "innovation")
        ]

        for icon, name, key in indicators:
            indicator_frame = ctk.CTkFrame(analysis_frame, fg_color="transparent")
            indicator_frame.pack(fill="x", padx=10, pady=3)

            # الأيقونة والاسم
            left_frame = ctk.CTkFrame(indicator_frame, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)

            icon_label = ctk.CTkLabel(
                left_frame,
                text=icon,
                font=("Arial", 12),
                width=20
            )
            icon_label.pack(side="left")

            name_label = ctk.CTkLabel(
                left_frame,
                text=name,
                font=("Arial", 10),
                text_color=ADVANCED_COLORS['text_secondary']
            )
            name_label.pack(side="left", padx=(5, 0))

            # شريط التقدم والقيمة
            right_frame = ctk.CTkFrame(indicator_frame, fg_color="transparent")
            right_frame.pack(side="right")

            progress_bar = ctk.CTkProgressBar(
                right_frame,
                width=80,
                height=10,
                corner_radius=5
            )
            progress_bar.pack(side="left", padx=(0, 5))
            progress_bar.set(0.8)  # قيمة افتراضية

            value_label = ctk.CTkLabel(
                right_frame,
                text="80%",
                font=("Arial", 9, "bold"),
                text_color=ADVANCED_COLORS['text_primary'],
                width=30
            )
            value_label.pack(side="right")

            # حفظ المراجع للتحديث
            self.performance_indicators[key] = {
                'progress': progress_bar,
                'label': value_label
            }

    def create_predictions_section(self, parent):
        """إنشاء قسم التنبؤات"""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=15, padx=15)

        # عنوان القسم
        title_frame = ctk.CTkFrame(
            section_frame,
            fg_color=ADVANCED_COLORS['info_gradient'][0],
            corner_radius=8,
            height=30
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame,
            text="🔮 التنبؤات الذكية",
            font=("Arial", 12, "bold"),
            text_color="white"
        )
        title_label.pack(pady=5)

        # محتوى التنبؤات
        predictions_frame = ctk.CTkFrame(
            section_frame,
            fg_color=ADVANCED_COLORS['background_gradient'][1],
            corner_radius=8
        )
        predictions_frame.pack(fill="x", pady=(5, 0))

        # تنبؤات محاكاة
        predictions = [
            ("📅", "احتمالية الحضور الأسبوع القادم", "95%", "عالية"),
            ("📈", "توقع تحسن الأداء", "+8%", "إيجابي"),
            ("🎯", "احتمالية تحقيق الأهداف", "87%", "جيدة"),
            ("⚠️", "مخاطر ترك العمل", "12%", "منخفضة")
        ]

        for icon, prediction, value, status in predictions:
            pred_frame = ctk.CTkFrame(predictions_frame, fg_color="transparent")
            pred_frame.pack(fill="x", padx=10, pady=3)

            # الأيقونة والوصف
            left_frame = ctk.CTkFrame(pred_frame, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)

            icon_label = ctk.CTkLabel(
                left_frame,
                text=icon,
                font=("Arial", 12),
                width=20
            )
            icon_label.pack(side="left")

            desc_label = ctk.CTkLabel(
                left_frame,
                text=prediction,
                font=("Arial", 9),
                text_color=ADVANCED_COLORS['text_secondary']
            )
            desc_label.pack(side="left", padx=(5, 0))

            # القيمة والحالة
            right_frame = ctk.CTkFrame(pred_frame, fg_color="transparent")
            right_frame.pack(side="right")

            value_label = ctk.CTkLabel(
                right_frame,
                text=value,
                font=("Arial", 10, "bold"),
                text_color=ADVANCED_COLORS['text_primary']
            )
            value_label.pack(side="top")

            status_label = ctk.CTkLabel(
                right_frame,
                text=status,
                font=("Arial", 8),
                text_color=ADVANCED_COLORS['status_active']
            )
            status_label.pack(side="bottom")

    def create_recommendations_section(self, parent):
        """إنشاء قسم التوصيات"""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=15, padx=15)

        # عنوان القسم
        title_frame = ctk.CTkFrame(
            section_frame,
            fg_color=ADVANCED_COLORS['secondary_gradient'][0],
            corner_radius=8,
            height=30
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame,
            text="💡 التوصيات الذكية",
            font=("Arial", 12, "bold"),
            text_color="white"
        )
        title_label.pack(pady=5)

        # محتوى التوصيات
        recommendations_frame = ctk.CTkFrame(
            section_frame,
            fg_color="white",
            corner_radius=8
        )
        recommendations_frame.pack(fill="x", pady=(5, 0))

        # توصيات محاكاة
        recommendations = [
            "🎓 يُنصح بدورة تدريبية في الإدارة",
            "🏆 مرشح للترقية خلال 6 أشهر",
            "💰 يستحق زيادة راتب بنسبة 10%",
            "🤝 يمكن إسناد مهام قيادية إضافية",
            "📊 يحتاج متابعة أداء شهرية"
        ]

        for i, recommendation in enumerate(recommendations):
            rec_frame = ctk.CTkFrame(recommendations_frame, fg_color="transparent")
            rec_frame.pack(fill="x", padx=10, pady=2)

            rec_label = ctk.CTkLabel(
                rec_frame,
                text=recommendation,
                font=("Arial", 9),
                text_color=ADVANCED_COLORS['text_primary'],
                anchor="w"
            )
            rec_label.pack(anchor="w")

    # الوظائف الذكية المحسنة
    def add_employee_smart(self):
        """إضافة موظف جديد مع ميزات ذكية"""
        self.clear_form_smart()
        self.current_employee = None
        if hasattr(self, 'form_title_label') and self.form_title_label:
            self.form_title_label.configure(text="📝 إضافة موظف جديد - النمط الذكي")

        # توليد رقم موظف ذكي
        new_number = self.generate_smart_employee_number()
        self.form_vars['employee_number'].set(new_number)

        # تطبيق الإعدادات الافتراضية الذكية
        self.apply_smart_defaults()

        # عرض اقتراحات ذكية
        self.show_smart_form_suggestions()

    def edit_employee_smart(self):
        """تعديل الموظف المحدد مع تحليلات ذكية"""
        selection = self.tree.selection()
        if not selection:
            self.show_smart_notification("تحذير", "يرجى اختيار موظف للتعديل", "warning")
            return

        item = self.tree.item(selection[0])
        employee_id = item['values'][0]
        self.load_employee_details_smart(employee_id)
        if hasattr(self, 'form_title_label') and self.form_title_label:
            self.form_title_label.configure(text="📝 تعديل بيانات الموظف - النمط الذكي")

        # تحليل الموظف تلقائياً
        self.analyze_current_employee()

    def delete_employee_safe(self):
        """حذف الموظف المحدد مع تأكيد متقدم"""
        selection = self.tree.selection()
        if not selection:
            self.show_smart_notification("تحذير", "يرجى اختيار موظف للحذف", "warning")
            return

        item = self.tree.item(selection[0])
        employee_name = item['values'][2]
        employee_id = item['values'][0]

        # نافذة تأكيد متقدمة
        result = self.show_advanced_confirmation(
            "تأكيد الحذف الآمن",
            f"هل أنت متأكد من حذف الموظف:\n\n👤 {employee_name}\n\n"
            "⚠️ تحذير: هذا الإجراء لا يمكن التراجع عنه\n"
            "📊 سيتم حذف جميع البيانات المرتبطة بالموظف\n"
            "💾 هل تريد إنشاء نسخة احتياطية أولاً؟"
        )

        if result == "delete":
            try:
                # حذف الموظف من قاعدة البيانات
                self.delete_employee_from_database(employee_id)

                # تحديث الواجهة
                self.load_employees_data_smart()
                self.clear_form_smart()

                self.show_smart_notification("نجح", f"تم حذف الموظف {employee_name} بنجاح", "success")

            except Exception as e:
                self.show_smart_notification("خطأ", f"خطأ في حذف الموظف: {e}", "error")

    def analyze_performance(self):
        """تحليل أداء جميع الموظفين"""
        # إنشاء نافذة تحليل الأداء
        analysis_window = ctk.CTkToplevel(self.window)
        analysis_window.title("📊 تحليل الأداء الشامل")
        analysis_window.geometry("1150x750")  # زيادة الحجم للوضوح الأفضل
        analysis_window.transient(self.window)
        analysis_window.grab_set()

        # تطبيق تصميم متقدم
        main_frame = ctk.CTkFrame(
            analysis_window,
            fg_color=ADVANCED_COLORS['background_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # عنوان النافذة
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 تحليل الأداء الشامل والذكي",
            font=("Arial", 24, "bold"),
            text_color=ADVANCED_COLORS['text_primary']
        )
        title_label.pack(pady=30)

        # محتوى التحليل
        self.create_performance_analysis_content(main_frame)

    def manage_salaries_smart(self):
        """إدارة الرواتب الذكية"""
        # إنشاء نافذة إدارة الرواتب الذكية
        salary_window = ctk.CTkToplevel(self.window)
        salary_window.title("💰 إدارة الرواتب الذكية")
        salary_window.geometry("1350x850")  # زيادة الحجم لعرض أفضل للبيانات
        salary_window.transient(self.window)
        salary_window.grab_set()

        # تطبيق تصميم متقدم
        main_frame = ctk.CTkFrame(
            salary_window,
            fg_color=ADVANCED_COLORS['background_gradient'][1],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # عنوان النافذة
        title_label = ctk.CTkLabel(
            main_frame,
            text="💰 نظام إدارة الرواتب الذكي",
            font=("Arial", 24, "bold"),
            text_color=ADVANCED_COLORS['text_primary']
        )
        title_label.pack(pady=30)

        # محتوى إدارة الرواتب
        self.create_smart_salary_management(main_frame)

    def show_smart_suggestions(self):
        """عرض الاقتراحات الذكية"""
        # إنشاء نافذة الاقتراحات الذكية
        suggestions_window = ctk.CTkToplevel(self.window)
        suggestions_window.title("🤖 الاقتراحات الذكية")
        suggestions_window.geometry("900x650")  # زيادة الحجم لعرض أوضح
        suggestions_window.transient(self.window)
        suggestions_window.grab_set()

        # تطبيق تصميم متقدم
        main_frame = ctk.CTkFrame(
            suggestions_window,
            fg_color=ADVANCED_COLORS['primary_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # عنوان النافذة
        title_label = ctk.CTkLabel(
            main_frame,
            text="🤖 الاقتراحات الذكية لإدارة الموظفين",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=30)

        # محتوى الاقتراحات
        self.create_smart_suggestions_content(main_frame)

    def on_smart_search(self, *args):
        """البحث الذكي المحسن"""
        search_term = self.search_var.get().lower()

        if len(search_term) >= 2:  # بدء البحث من حرفين
            # تطبيق خوارزمية البحث الذكي
            self.apply_smart_filters()

            # إضافة تأثير بصري للبحث
            self.animate_search_results()

    def on_smart_filter(self, *args):
        """الفلترة الذكية المحسنة"""
        self.apply_smart_filters()

    def apply_smart_filters(self):
        """تطبيق الفلاتر الذكية"""
        try:
            search_term = self.search_var.get().lower() if self.search_var else ""
            dept_filter = self.department_filter_var.get() if self.department_filter_var else "الكل"
            status_filter = self.status_filter_var.get() if self.status_filter_var else "الكل"

            self.filtered_employees = []

            for emp in self.employees_data:
                # خوارزمية البحث الذكي (البحث في عدة حقول)
                if search_term:
                    searchable_text = f"{emp[2]} {emp[3]} {emp[4]} {emp[1]}".lower()  # الاسم، القسم، المنصب، الرقم
                    if search_term not in searchable_text:
                        continue

                # فلتر القسم
                if dept_filter != "الكل" and emp[3] != dept_filter:
                    continue

                # فلتر الحالة
                if status_filter != "الكل" and emp[6] != status_filter:
                    continue

                self.filtered_employees.append(emp)

            # تحديث الجدول مع تأثيرات بصرية
            self.update_table_smart()

            # تحديث مؤشر النتائج
            self.update_results_indicator()

        except Exception as e:
            print(f"خطأ في تطبيق الفلاتر الذكية: {e}")

    def update_table_smart(self):
        """تحديث جدول الموظفين مع تحسينات ذكية"""
        try:
            # التحقق من وجود الجدول
            if not hasattr(self, 'tree') or self.tree is None:
                return

            # مسح البيانات الحالية
            for item in self.tree.get_children():
                self.tree.delete(item)

            # إضافة البيانات المفلترة مع تحسينات
            for emp in self.filtered_employees:
                # حساب نقاط الأداء (محاكاة)
                performance_score = random.randint(70, 100)

                # تنسيق البيانات للعرض
                display_data = (
                    emp[0],  # ID
                    emp[1],  # رقم الموظف
                    emp[2],  # الاسم
                    emp[3],  # القسم
                    emp[4],  # المنصب
                    f"{emp[5]:,.0f} ج.م",  # الراتب
                    f"{performance_score}%",  # الأداء
                    emp[6]   # الحالة
                )

                # تحديد لون الصف حسب الحالة والأداء
                tags = []
                if emp[6] == "نشط":
                    if performance_score >= 90:
                        tags = ["excellent"]
                    elif performance_score >= 80:
                        tags = ["good"]
                    else:
                        tags = ["active"]
                elif emp[6] == "غير نشط":
                    tags = ["inactive"]
                elif emp[6] == "معلق":
                    tags = ["suspended"]

                self.tree.insert("", "end", values=display_data, tags=tags)

            # تكوين ألوان الصفوف المحسنة
            self.tree.tag_configure("excellent", background="#d1f2eb", foreground="#0e6b3a")
            self.tree.tag_configure("good", background="#d4edda", foreground="#155724")
            self.tree.tag_configure("active", background="#f8f9fa", foreground="#495057")
            self.tree.tag_configure("inactive", background="#f8d7da", foreground="#721c24")
            self.tree.tag_configure("suspended", background="#fff3cd", foreground="#856404")

        except Exception as e:
            print(f"خطأ في تحديث الجدول الذكي: {e}")

    def update_results_indicator(self):
        """تحديث مؤشر النتائج"""
        try:
            # التحقق من وجود مؤشر النتائج
            if not hasattr(self, 'results_label') or self.results_label is None:
                return

            total = len(self.employees_data)
            filtered = len(self.filtered_employees)

            if filtered == total:
                text = f"عرض جميع الموظفين ({total})"
            else:
                text = f"عرض {filtered} من {total} موظف"

            self.results_label.configure(text=text)

        except Exception as e:
            print(f"خطأ في تحديث مؤشر النتائج: {e}")

    def animate_search_results(self):
        """تحريك نتائج البحث"""
        # محاكاة تأثير بصري للبحث
        if not self.animation_running:
            self.animation_running = True
            # هنا يمكن إضافة تأثيرات بصرية متقدمة
            self.window.after(500, lambda: setattr(self, 'animation_running', False))

    def on_employee_select_smart(self, event):
        """عند اختيار موظف من الجدول مع ميزات ذكية"""
        try:
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                employee_id = item['values'][0]
                self.load_employee_details_smart(employee_id)

                # تحديث لوحة التحليلات تلقائياً
                self.update_analytics_panel()

        except Exception as e:
            print(f"خطأ في اختيار الموظف الذكي: {e}")

    def on_employee_double_click_smart(self, event):
        """عند النقر المزدوج على موظف مع ميزات ذكية"""
        self.edit_employee_smart()

    def show_context_menu(self, event):
        """عرض قائمة السياق المحسنة"""
        # إنشاء قائمة سياق ذكية
        context_menu = tk.Menu(self.window, tearoff=0)

        context_menu.add_command(label="📝 تعديل", command=self.edit_employee_smart)
        context_menu.add_command(label="📊 تحليل الأداء", command=self.analyze_current_employee)
        context_menu.add_command(label="💰 إدارة الراتب", command=self.manage_employee_salary)
        context_menu.add_separator()
        context_menu.add_command(label="📋 نسخ البيانات", command=self.copy_employee_data)
        context_menu.add_command(label="📄 طباعة التقرير", command=self.print_employee_report)
        context_menu.add_separator()
        context_menu.add_command(label="🗑️ حذف", command=self.delete_employee_safe)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    # الوظائف المساعدة والذكية
    def generate_smart_employee_number(self):
        """توليد رقم موظف ذكي"""
        try:
            # خوارزمية ذكية لتوليد رقم الموظف
            current_year = datetime.now().year

            # البحث عن آخر رقم في السنة الحالية
            query = f"SELECT MAX(CAST(SUBSTR(employee_number, 4) AS INTEGER)) FROM employees WHERE employee_number LIKE 'EMP%'"

            if hasattr(self, 'db_cursor'):
                self.db_cursor.execute(query)
                result = self.db_cursor.fetchone()
                max_num = result[0] if result and result[0] else 0
            else:
                max_num = len(self.employees_data)

            # تنسيق ذكي للرقم
            new_number = f"EMP{current_year}{max_num + 1:04d}"
            return new_number

        except Exception as e:
            print(f"خطأ في توليد رقم الموظف الذكي: {e}")
            return f"EMP{datetime.now().year}0001"

    def apply_smart_defaults(self):
        """تطبيق الإعدادات الافتراضية الذكية"""
        # تطبيق قيم افتراضية ذكية بناءً على الإحصائيات
        self.form_vars['hire_date'].set(datetime.now().strftime("%Y-%m-%d"))
        self.form_vars['status'].set("نشط")
        self.form_vars['performance_score'].set("80")
        self.form_vars['experience_years'].set("0")

        # اقتراح قسم بناءً على التوزيع الحالي
        dept_distribution = self.analyze_department_distribution()
        suggested_dept = min(dept_distribution.items(), key=lambda x: x[1])[0]
        self.form_vars['department'].set(suggested_dept)

    def analyze_department_distribution(self):
        """تحليل توزيع الموظفين على الأقسام"""
        distribution = {
            "الإدارة": 0,
            "المحاسبة": 0,
            "المبيعات": 0,
            "التقنية": 0,
            "الموارد البشرية": 0,
            "التسويق": 0
        }

        for emp in self.employees_data:
            dept = emp[3] if len(emp) > 3 else "الإدارة"
            if dept in distribution:
                distribution[dept] += 1

        return distribution

    def show_smart_form_suggestions(self):
        """عرض اقتراحات ذكية للنموذج"""
        # إنشاء نافذة اقتراحات صغيرة
        suggestions_popup = ctk.CTkToplevel(self.window)
        suggestions_popup.title("💡 اقتراحات ذكية")
        suggestions_popup.geometry("400x300")
        suggestions_popup.transient(self.window)

        # محتوى الاقتراحات
        main_frame = ctk.CTkFrame(suggestions_popup, fg_color=ADVANCED_COLORS['info_gradient'][0])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(
            main_frame,
            text="💡 اقتراحات ذكية للموظف الجديد",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        title_label.pack(pady=20)

        # اقتراحات ذكية
        suggestions = [
            "🎯 القسم الأقل كثافة: " + min(self.analyze_department_distribution().items(), key=lambda x: x[1])[0],
            "💰 متوسط الراتب في الشركة: " + f"{self.calculate_average_salary():,.0f} ج.م",
            "📊 معدل الأداء المطلوب: 80% أو أكثر",
            "📅 فترة التجربة المعتادة: 3 أشهر",
            "🎓 التدريب الأولي: أسبوعين"
        ]

        for suggestion in suggestions:
            suggestion_label = ctk.CTkLabel(
                main_frame,
                text=suggestion,
                font=("Arial", 12),
                text_color="white",
                anchor="w"
            )
            suggestion_label.pack(anchor="w", padx=20, pady=5)

        # زر إغلاق
        close_btn = ctk.CTkButton(
            main_frame,
            text="✅ فهمت",
            command=suggestions_popup.destroy,
            width=100,
            height=30,
            fg_color="white",
            text_color=ADVANCED_COLORS['info_gradient'][0],
            hover_color="#f0f0f0"
        )
        close_btn.pack(pady=20)

    def calculate_average_salary(self):
        """حساب متوسط الراتب في الشركة"""
        if not self.employees_data:
            return 5000

        total_salary = sum(emp[5] for emp in self.employees_data if len(emp) > 5 and emp[5])
        return total_salary / len(self.employees_data) if self.employees_data else 5000

    def load_employee_details_smart(self, employee_id):
        """تحميل تفاصيل موظف محدد مع ميزات ذكية"""
        try:
            query = "SELECT * FROM employees WHERE id = ?"

            if hasattr(self, 'db_cursor'):
                self.db_cursor.execute(query, (employee_id,))
                result = self.db_cursor.fetchone()
            else:
                result = None

            if result:
                self.current_employee = result
                self.populate_form_smart(result)

                # تحديث العنوان مع معلومات ذكية
                employee_name = result[2] if len(result) > 2 else "غير محدد"
                performance = random.randint(70, 100)  # محاكاة
                if hasattr(self, 'form_title_label') and self.form_title_label:
                    self.form_title_label.configure(
                        text=f"📝 {employee_name} - الأداء: {performance}%"
                    )

                # تحليل تلقائي للموظف
                self.analyze_current_employee()

        except Exception as e:
            print(f"خطأ في تحميل تفاصيل الموظف الذكي: {e}")

    def populate_form_smart(self, employee_data):
        """ملء النموذج ببيانات الموظف مع تحسينات ذكية"""
        try:
            # ملء الحقول الأساسية
            field_mapping = {
                'employee_id': 0,
                'employee_number': 1,
                'full_name': 2,
                'national_id': 3,
                'phone': 4,
                'email': 5,
                'address': 6,
                'department': 7,
                'position': 8,
                'hire_date': 9,
                'birth_date': 10,
                'basic_salary': 11,
                'status': 12,
                'photo_path': 13,
                'notes': 14
            }

            for var_name, index in field_mapping.items():
                if var_name in self.form_vars and index < len(employee_data):
                    value = employee_data[index] if employee_data[index] is not None else ""
                    self.form_vars[var_name].set(str(value))

            # حساب سنوات الخبرة تلقائياً
            if len(employee_data) > 9 and employee_data[9]:
                hire_date = datetime.strptime(employee_data[9], "%Y-%m-%d")
                experience_years = (datetime.now() - hire_date).days / 365.25
                self.form_vars['experience_years'].set(f"{experience_years:.1f}")

            # حساب نقاط الأداء (محاكاة)
            performance_score = random.randint(70, 100)
            self.form_vars['performance_score'].set(str(performance_score))

            # اقتراح راتب ذكي
            self.suggest_smart_salary()

            # تحميل الصورة إذا كانت موجودة
            if len(employee_data) > 13 and employee_data[13]:
                self.load_photo_preview_enhanced(employee_data[13])
            else:
                self.photo_label.configure(text="📷\nلا توجد صورة", image="")

        except Exception as e:
            print(f"خطأ في ملء النموذج الذكي: {e}")

    def analyze_current_employee(self):
        """تحليل الموظف الحالي"""
        if not self.current_employee:
            self.show_smart_notification("تحذير", "يرجى اختيار موظف للتحليل", "warning")
            return

        # إجراء تحليل شامل للموظف
        employee_data = {
            'name': self.current_employee[2] if len(self.current_employee) > 2 else "غير محدد",
            'position': self.current_employee[8] if len(self.current_employee) > 8 else "غير محدد",
            'department': self.current_employee[7] if len(self.current_employee) > 7 else "غير محدد",
            'hire_date': self.current_employee[9] if len(self.current_employee) > 9 else None
        }

        # تحليل الأداء
        analysis = self.analytics.analyze_performance(employee_data)

        # تحديث لوحة التحليلات
        self.update_performance_indicators(analysis)

        # عرض نتائج التحليل
        self.show_analysis_results(analysis)

    def update_performance_indicators(self, analysis):
        """تحديث مؤشرات الأداء"""
        try:
            # تحديث المؤشرات في لوحة التحليلات
            if hasattr(self, 'performance_indicators'):
                # النتيجة الإجمالية
                overall_score = analysis.get('overall_score', 0.8)
                if 'overall_score' in self.performance_indicators:
                    self.performance_indicators['overall_score']['progress'].set(overall_score)
                    self.performance_indicators['overall_score']['label'].configure(
                        text=f"{int(overall_score * 100)}%"
                    )

                # باقي المؤشرات (محاكاة)
                indicators = ['productivity', 'attendance', 'teamwork', 'innovation']
                for indicator in indicators:
                    if indicator in self.performance_indicators:
                        value = random.uniform(0.6, 1.0)
                        self.performance_indicators[indicator]['progress'].set(value)
                        self.performance_indicators[indicator]['label'].configure(
                            text=f"{int(value * 100)}%"
                        )
        except Exception as e:
            print(f"خطأ في تحديث مؤشرات الأداء: {e}")

    def show_analysis_results(self, analysis):
        """عرض نتائج التحليل"""
        # إنشاء نافذة نتائج التحليل
        results_window = ctk.CTkToplevel(self.window)
        results_window.title("📊 نتائج تحليل الأداء")
        results_window.geometry("700x550")  # زيادة الحجم لعرض النتائج بوضوح
        results_window.transient(self.window)
        results_window.grab_set()

        # تطبيق تصميم متقدم
        main_frame = ctk.CTkFrame(
            results_window,
            fg_color=ADVANCED_COLORS['success_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # عنوان النتائج
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 نتائج تحليل الأداء الذكي",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=30)

        # النتيجة الإجمالية
        score_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=15)
        score_frame.pack(fill="x", padx=30, pady=20)

        score_label = ctk.CTkLabel(
            score_frame,
            text=f"النتيجة الإجمالية: {analysis['overall_score']:.1%}",
            font=("Arial", 18, "bold"),
            text_color=ADVANCED_COLORS['text_primary']
        )
        score_label.pack(pady=20)

        # نقاط القوة
        if analysis['strengths']:
            strengths_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
            strengths_frame.pack(fill="x", padx=30, pady=10)

            strengths_title = ctk.CTkLabel(
                strengths_frame,
                text="💪 نقاط القوة:",
                font=("Arial", 14, "bold"),
                text_color=ADVANCED_COLORS['text_primary']
            )
            strengths_title.pack(anchor="w", padx=15, pady=(10, 5))

            for strength in analysis['strengths']:
                strength_label = ctk.CTkLabel(
                    strengths_frame,
                    text=f"✅ {strength}",
                    font=("Arial", 12),
                    text_color=ADVANCED_COLORS['text_secondary'],
                    anchor="w"
                )
                strength_label.pack(anchor="w", padx=25, pady=2)

        # نقاط الضعف
        if analysis['weaknesses']:
            weaknesses_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
            weaknesses_frame.pack(fill="x", padx=30, pady=10)

            weaknesses_title = ctk.CTkLabel(
                weaknesses_frame,
                text="⚠️ نقاط تحتاج تحسين:",
                font=("Arial", 14, "bold"),
                text_color=ADVANCED_COLORS['text_primary']
            )
            weaknesses_title.pack(anchor="w", padx=15, pady=(10, 5))

            for weakness in analysis['weaknesses']:
                weakness_label = ctk.CTkLabel(
                    weaknesses_frame,
                    text=f"🔸 {weakness}",
                    font=("Arial", 12),
                    text_color=ADVANCED_COLORS['text_secondary'],
                    anchor="w"
                )
                weakness_label.pack(anchor="w", padx=25, pady=2)

        # التوصيات
        if analysis['recommendations']:
            recommendations_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
            recommendations_frame.pack(fill="x", padx=30, pady=10)

            recommendations_title = ctk.CTkLabel(
                recommendations_frame,
                text="💡 التوصيات:",
                font=("Arial", 14, "bold"),
                text_color=ADVANCED_COLORS['text_primary']
            )
            recommendations_title.pack(anchor="w", padx=15, pady=(10, 5))

            for recommendation in analysis['recommendations']:
                rec_label = ctk.CTkLabel(
                    recommendations_frame,
                    text=f"🎯 {recommendation}",
                    font=("Arial", 12),
                    text_color=ADVANCED_COLORS['text_secondary'],
                    anchor="w"
                )
                rec_label.pack(anchor="w", padx=25, pady=2)

        # زر إغلاق
        close_btn = ctk.CTkButton(
            main_frame,
            text="✅ إغلاق",
            command=results_window.destroy,
            width=120,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="white",
            text_color=ADVANCED_COLORS['success_gradient'][0],
            hover_color="#f0f0f0"
        )
        close_btn.pack(pady=30)

    # الوظائف الأساسية المحسنة
    def save_employee_smart(self):
        """حفظ بيانات الموظف مع التحقق الذكي"""
        try:
            # التحقق الذكي من صحة البيانات
            if not self.validate_form_smart():
                return

            # جمع البيانات مع التحسينات
            employee_data = self.collect_form_data_smart()

            if self.current_employee:
                # تحديث موظف موجود
                self.update_employee_smart(employee_data)
            else:
                # إضافة موظف جديد
                self.insert_employee_smart(employee_data)

            # إعادة تحميل البيانات مع تأثيرات بصرية
            self.load_employees_data_smart()

            # عرض إشعار نجاح ذكي
            self.show_smart_notification("نجح", "تم حفظ بيانات الموظف بنجاح", "success")

        except Exception as e:
            self.show_smart_notification("خطأ", f"خطأ في حفظ البيانات: {e}", "error")

    def validate_form_smart(self):
        """التحقق الذكي من صحة بيانات النموذج"""
        try:
            # التحقق من الحقول المطلوبة
            required_fields = {
                'employee_number': 'رقم الموظف',
                'full_name': 'الاسم الكامل',
                'department': 'القسم',
                'position': 'المنصب'
            }

            for field, label in required_fields.items():
                if not self.form_vars[field].get().strip():
                    self.show_smart_notification("خطأ", f"يجب إدخال {label}", "error")
                    return False

            # التحقق الذكي من صحة الراتب
            try:
                salary = float(self.form_vars['basic_salary'].get() or 0)
                if salary < 0:
                    self.show_smart_notification("خطأ", "الراتب يجب أن يكون رقم موجب", "error")
                    return False

                # تحذير ذكي للراتب غير المعقول
                avg_salary = self.calculate_average_salary()
                if salary > avg_salary * 3:
                    result = messagebox.askyesno(
                        "تحذير ذكي",
                        f"الراتب المدخل ({salary:,.0f} ج.م) أعلى بكثير من المتوسط ({avg_salary:,.0f} ج.م)\n"
                        "هل تريد المتابعة؟"
                    )
                    if not result:
                        return False

            except ValueError:
                self.show_smart_notification("خطأ", "الراتب يجب أن يكون رقم صحيح", "error")
                return False

            # التحقق الذكي من البريد الإلكتروني
            email = self.form_vars['email'].get().strip()
            if email and '@' not in email:
                self.show_smart_notification("خطأ", "البريد الإلكتروني غير صحيح", "error")
                return False

            # التحقق من تفرد رقم الموظف
            emp_number = self.form_vars['employee_number'].get().strip()
            if self.is_employee_number_exists(emp_number):
                self.show_smart_notification("خطأ", "رقم الموظف موجود مسبقاً", "error")
                return False

            return True

        except Exception as e:
            print(f"خطأ في التحقق الذكي من البيانات: {e}")
            return False

    def is_employee_number_exists(self, emp_number):
        """التحقق من وجود رقم الموظف"""
        if not self.current_employee:  # موظف جديد
            for emp in self.employees_data:
                if len(emp) > 1 and emp[1] == emp_number:
                    return True
        else:  # تعديل موظف موجود
            for emp in self.employees_data:
                if len(emp) > 1 and emp[1] == emp_number and emp[0] != self.current_employee[0]:
                    return True
        return False

    def collect_form_data_smart(self):
        """جمع بيانات النموذج مع تحسينات ذكية"""
        data = {
            'employee_number': self.form_vars['employee_number'].get().strip(),
            'full_name': self.form_vars['full_name'].get().strip(),
            'national_id': self.form_vars['national_id'].get().strip(),
            'phone': self.form_vars['phone'].get().strip(),
            'email': self.form_vars['email'].get().strip(),
            'address': self.form_vars['address'].get().strip(),
            'department': self.form_vars['department'].get(),
            'position': self.form_vars['position'].get(),
            'hire_date': self.form_vars['hire_date'].get(),
            'birth_date': self.form_vars['birth_date'].get(),
            'basic_salary': float(self.form_vars['basic_salary'].get() or 0),
            'status': self.form_vars['status'].get(),
            'photo_path': self.form_vars['photo_path'].get(),
            'notes': self.form_vars['notes'].get(),
            'experience_years': float(self.form_vars['experience_years'].get() or 0),
            'performance_score': float(self.form_vars['performance_score'].get() or 80)
        }

        return data

    def insert_employee_smart(self, employee_data):
        """إدراج موظف جديد مع ميزات ذكية"""
        try:
            query = """
            INSERT INTO employees
            (employee_number, full_name, national_id, phone, email, address,
             department, position, hire_date, birth_date, basic_salary,
             status, photo_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                employee_data['photo_path'],
                employee_data['notes']
            )

            if hasattr(self, 'db_cursor'):
                self.db_cursor.execute(query, values)
                self.db_connection.commit()

            # مسح النموذج بعد الحفظ
            self.clear_form_smart()

            # إضافة إلى سجل النشاطات
            self.log_activity(f"تم إضافة موظف جديد: {employee_data['full_name']}")

        except Exception as e:
            raise Exception(f"خطأ في إضافة الموظف: {e}")

    def update_employee_smart(self, employee_data):
        """تحديث بيانات موظف موجود مع ميزات ذكية"""
        try:
            query = """
            UPDATE employees SET
            employee_number=?, full_name=?, national_id=?, phone=?, email=?,
            address=?, department=?, position=?, hire_date=?, birth_date=?,
            basic_salary=?, status=?, photo_path=?, notes=?,
            updated_at=CURRENT_TIMESTAMP
            WHERE id=?
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
                employee_data['photo_path'],
                employee_data['notes'],
                self.current_employee[0]  # ID
            )

            if hasattr(self, 'db_cursor'):
                self.db_cursor.execute(query, values)
                self.db_connection.commit()

            # إضافة إلى سجل النشاطات
            self.log_activity(f"تم تحديث بيانات الموظف: {employee_data['full_name']}")

        except Exception as e:
            raise Exception(f"خطأ في تحديث الموظف: {e}")

    def clear_form_smart(self):
        """مسح النموذج مع تأثيرات ذكية"""
        try:
            # مسح جميع الحقول
            for var in self.form_vars.values():
                var.set("")

            # إعادة تعيين القيم الافتراضية الذكية
            self.apply_smart_defaults()

            # مسح الصورة
            self.photo_label.configure(text="📷\nصورة الموظف", image="")

            # إعادة تعيين العنوان
            if hasattr(self, 'form_title_label') and self.form_title_label:
                self.form_title_label.configure(text="📝 نموذج الموظف الذكي")

            # مسح التحديد من الجدول
            if hasattr(self, 'tree') and self.tree:
                for item in self.tree.selection():
                    self.tree.selection_remove(item)

            self.current_employee = None

            # تأثير بصري للمسح
            self.animate_form_clear()

        except Exception as e:
            print(f"خطأ في مسح النموذج الذكي: {e}")

    def cancel_operation_smart(self):
        """إلغاء العملية مع تأكيد ذكي"""
        if self.has_unsaved_changes():
            result = messagebox.askyesno(
                "تأكيد الإلغاء",
                "هناك تغييرات غير محفوظة. هل تريد إلغاء العملية؟"
            )
            if not result:
                return

        self.clear_form_smart()

    def has_unsaved_changes(self):
        """التحقق من وجود تغييرات غير محفوظة"""
        # فحص ذكي للتغييرات
        if not self.current_employee:
            # موظف جديد - فحص إذا كان هناك بيانات مدخلة
            for var_name, var in self.form_vars.items():
                if var_name in ['department', 'position', 'status', 'hire_date', 'performance_score', 'experience_years']:
                    continue  # تجاهل القيم الافتراضية
                if var.get().strip():
                    return True
        else:
            # موظف موجود - فحص التغييرات
            # هذا يتطلب مقارنة القيم الحالية مع القيم الأصلية
            pass

        return False

    def animate_form_clear(self):
        """تحريك مسح النموذج"""
        # محاكاة تأثير بصري لمسح النموذج
        pass

    def log_activity(self, activity):
        """تسجيل النشاطات"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {activity}")
        # يمكن إضافة تسجيل في قاعدة البيانات أو ملف

    # وظائف التأثيرات البصرية والإشعارات
    def show_smart_notification(self, title, message, type_msg="info"):
        """عرض إشعار ذكي مع تأثيرات بصرية"""
        # ألوان الإشعارات
        colors = {
            "success": ADVANCED_COLORS['success_gradient'][0],
            "error": ADVANCED_COLORS['danger_gradient'][0],
            "warning": ADVANCED_COLORS['warning_gradient'][0],
            "info": ADVANCED_COLORS['info_gradient'][0]
        }

        # أيقونات الإشعارات
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }

        # إنشاء نافذة إشعار مخصصة
        notification = ctk.CTkToplevel(self.window)
        notification.title(title)
        notification.geometry("400x150")
        notification.transient(self.window)
        notification.configure(fg_color=colors.get(type_msg, colors["info"]))

        # محتوى الإشعار
        content_frame = ctk.CTkFrame(notification, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # الأيقونة والعنوان
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))

        icon_label = ctk.CTkLabel(
            header_frame,
            text=icons.get(type_msg, "ℹ️"),
            font=("Arial", 24),
            text_color="white"
        )
        icon_label.pack(side="left")

        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=(10, 0))

        # الرسالة
        message_label = ctk.CTkLabel(
            content_frame,
            text=message,
            font=("Arial", 12),
            text_color="white",
            wraplength=350
        )
        message_label.pack(fill="x", pady=(0, 10))

        # زر إغلاق
        close_btn = ctk.CTkButton(
            content_frame,
            text="موافق",
            command=notification.destroy,
            width=80,
            height=30,
            fg_color="white",
            text_color=colors.get(type_msg, colors["info"]),
            hover_color="#f0f0f0"
        )
        close_btn.pack()

        # إغلاق تلقائي بعد 3 ثوان
        notification.after(3000, notification.destroy)

        # توسيط النافذة
        notification.update_idletasks()
        x = (notification.winfo_screenwidth() // 2) - (400 // 2)
        y = (notification.winfo_screenheight() // 2) - (150 // 2)
        notification.geometry(f"400x150+{x}+{y}")

    def show_advanced_confirmation(self, title, message):
        """عرض نافذة تأكيد متقدمة"""
        # إنشاء نافذة تأكيد مخصصة
        confirm_window = ctk.CTkToplevel(self.window)
        confirm_window.title(title)
        confirm_window.geometry("500x300")
        confirm_window.transient(self.window)
        confirm_window.grab_set()

        result = {"value": None}

        # محتوى النافذة
        main_frame = ctk.CTkFrame(
            confirm_window,
            fg_color=ADVANCED_COLORS['danger_gradient'][0],
            corner_radius=VISUAL_EFFECTS['corner_radius']
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # العنوان
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        title_label.pack(pady=20)

        # الرسالة
        message_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        message_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        message_label = ctk.CTkLabel(
            message_frame,
            text=message,
            font=("Arial", 12),
            text_color=ADVANCED_COLORS['text_primary'],
            wraplength=400,
            justify="right"
        )
        message_label.pack(pady=20)

        # الأزرار
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

        def on_delete():
            result["value"] = "delete"
            confirm_window.destroy()

        def on_backup():
            result["value"] = "backup"
            confirm_window.destroy()

        def on_cancel():
            result["value"] = "cancel"
            confirm_window.destroy()

        # أزرار العمليات
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ حذف",
            command=on_delete,
            width=100,
            height=40,
            fg_color=ADVANCED_COLORS['danger_gradient'][1],
            hover_color="#c82333"
        )
        delete_btn.pack(side="left", padx=5)

        backup_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 نسخ احتياطي",
            command=on_backup,
            width=120,
            height=40,
            fg_color=ADVANCED_COLORS['warning_gradient'][0],
            hover_color=ADVANCED_COLORS['warning_gradient'][1]
        )
        backup_btn.pack(side="left", padx=5)

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ إلغاء",
            command=on_cancel,
            width=100,
            height=40,
            fg_color="white",
            text_color=ADVANCED_COLORS['danger_gradient'][0],
            hover_color="#f0f0f0"
        )
        cancel_btn.pack(side="right", padx=5)

        # انتظار النتيجة
        confirm_window.wait_window()
        return result["value"]

    # الوظائف الأساسية المتبقية
    def init_database(self):
        """تهيئة قاعدة البيانات المحسنة"""
        try:
            # استخدام SQLite مباشرة لضمان الاستقرار
            self.init_sqlite_database()

            # إنشاء الجداول
            self.create_enhanced_tables()

            # إدراج بيانات افتراضية
            self.insert_enhanced_default_data()

        except Exception as e:
            print(f"خطأ في تهيئة قاعدة البيانات المحسنة: {e}")

    def init_sqlite_database(self):
        """تهيئة قاعدة بيانات SQLite"""
        try:
            db_path = "data/advanced_employees.db"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            self.db_connection = sqlite3.connect(db_path)
            self.db_cursor = self.db_connection.cursor()
            print("✅ تم تهيئة قاعدة البيانات المتقدمة بنجاح")
        except Exception as e:
            print(f"خطأ في تهيئة SQLite: {e}")
            # إنشاء قاعدة بيانات في الذاكرة كبديل
            self.db_connection = sqlite3.connect(":memory:")
            self.db_cursor = self.db_connection.cursor()
            print("✅ تم إنشاء قاعدة بيانات في الذاكرة")

    def create_enhanced_tables(self):
        """إنشاء جداول قاعدة البيانات المحسنة"""
        try:
            # جدول الموظفين المحسن
            employees_table = """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                national_id TEXT UNIQUE,
                phone TEXT,
                email TEXT,
                address TEXT,
                department TEXT,
                position TEXT,
                hire_date DATE,
                birth_date DATE,
                basic_salary REAL DEFAULT 0,
                suggested_salary REAL DEFAULT 0,
                experience_years REAL DEFAULT 0,
                performance_score REAL DEFAULT 80,
                skills TEXT,
                status TEXT DEFAULT 'نشط',
                photo_path TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

            # جدول تقييم الأداء
            performance_table = """
            CREATE TABLE IF NOT EXISTS performance_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                evaluation_date DATE,
                overall_score REAL,
                productivity_score REAL,
                attendance_score REAL,
                teamwork_score REAL,
                innovation_score REAL,
                strengths TEXT,
                weaknesses TEXT,
                recommendations TEXT,
                evaluator_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
            """

            # جدول الأنشطة والسجلات
            activities_table = """
            CREATE TABLE IF NOT EXISTS activities_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                activity_type TEXT,
                activity_description TEXT,
                activity_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
            """

            # تنفيذ إنشاء الجداول
            self.db_cursor.execute(employees_table)
            self.db_cursor.execute(performance_table)
            self.db_cursor.execute(activities_table)
            self.db_connection.commit()
            print("✅ تم إنشاء جداول قاعدة البيانات المحسنة بنجاح")

        except Exception as e:
            print(f"خطأ في إنشاء الجداول المحسنة: {e}")

    def insert_enhanced_default_data(self):
        """إدراج بيانات افتراضية محسنة"""
        try:
            # التحقق من وجود بيانات
            self.db_cursor.execute("SELECT COUNT(*) FROM employees")
            count = self.db_cursor.fetchone()[0]

            if count == 0:
                # إدراج موظفين افتراضيين محسنين
                default_employees = [
                    ("EMP20250001", "أحمد محمد علي", "12345678901", "01234567890", "ahmed@company.com",
                     "القاهرة، مصر", "الإدارة", "مدير عام", "2020-01-15", "1985-05-20",
                     15000, 16500, 5.0, 92, "القيادة، الإدارة، التخطيط الاستراتيجي", "نشط"),
                    ("EMP20250002", "فاطمة أحمد حسن", "12345678902", "01234567891", "fatma@company.com",
                     "الجيزة، مصر", "المحاسبة", "محاسب أول", "2021-03-10", "1990-08-15",
                     8000, 8800, 3.5, 88, "المحاسبة، التحليل المالي، Excel", "نشط"),
                    ("EMP20250003", "محمد عبد الله", "12345678903", "01234567892", "mohamed@company.com",
                     "الإسكندرية، مصر", "المبيعات", "موظف مبيعات", "2022-06-01", "1992-12-10",
                     5000, 5500, 2.5, 85, "المبيعات، التفاوض، خدمة العملاء", "نشط"),
                    ("EMP20250004", "سارة حسام الدين", "12345678904", "01234567893", "sara@company.com",
                     "طنطا، مصر", "التقنية", "مطور أول", "2019-09-15", "1988-03-25",
                     12000, 13200, 6.0, 95, "البرمجة، Python، JavaScript، قواعد البيانات", "نشط"),
                    ("EMP20250005", "خالد عبد الرحمن", "12345678905", "01234567894", "khaled@company.com",
                     "المنصورة، مصر", "الموارد البشرية", "أخصائي موارد بشرية", "2023-01-10", "1993-11-08",
                     6500, 7150, 1.5, 82, "إدارة الموارد البشرية، التدريب، التوظيف", "نشط")
                ]

                for emp_data in default_employees:
                    query = """
                    INSERT INTO employees
                    (employee_number, full_name, national_id, phone, email, address,
                     department, position, hire_date, birth_date, basic_salary,
                     suggested_salary, experience_years, performance_score, skills, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """

                    self.db_cursor.execute(query, emp_data)

                self.db_connection.commit()
                print("✅ تم إدراج البيانات الافتراضية المحسنة بنجاح")

        except Exception as e:
            print(f"خطأ في إدراج البيانات الافتراضية المحسنة: {e}")

    def load_employees_data_smart(self):
        """تحميل بيانات الموظفين مع ميزات ذكية"""
        try:
            query = """
            SELECT id, employee_number, full_name, department, position,
                   basic_salary, status, phone, email, hire_date, performance_score
            FROM employees
            ORDER BY full_name
            """

            self.db_cursor.execute(query)
            self.employees_data = self.db_cursor.fetchall()

            # تطبيق الفلاتر الذكية
            self.apply_smart_filters()

            # تحديث الإحصائيات الذكية
            self.update_smart_statistics()

        except Exception as e:
            print(f"خطأ في تحميل بيانات الموظفين الذكية: {e}")
            self.employees_data = []
            self.filtered_employees = []

    def update_smart_statistics(self):
        """تحديث الإحصائيات الذكية"""
        try:
            total_employees = len(self.employees_data)
            active_employees = len([emp for emp in self.employees_data if len(emp) > 6 and emp[6] == "نشط"])

            # تحديث بطاقات الإحصائيات في الهيدر
            if hasattr(self, 'total_employees_label'):
                self.total_employees_label.configure(text=str(total_employees))
            if hasattr(self, 'active_employees_label'):
                self.active_employees_label.configure(text=str(active_employees))

            # حساب متوسط الأداء
            if self.employees_data:
                avg_performance = sum(emp[10] if len(emp) > 10 and emp[10] else 80 for emp in self.employees_data) / len(self.employees_data)
            else:
                avg_performance = 80

            # حساب معدل الحضور (محاكاة)
            attendance_rate = random.uniform(90, 98)

            print(f"📊 الإحصائيات المحدثة: {total_employees} موظف، {active_employees} نشط، أداء {avg_performance:.1f}%، حضور {attendance_rate:.1f}%")

        except Exception as e:
            print(f"خطأ في تحديث الإحصائيات الذكية: {e}")

    def update_analytics_panel(self):
        """تحديث لوحة التحليلات"""
        # تحديث لوحة التحليلات بناءً على الموظف المحدد
        if self.current_employee:
            # تحليل الموظف الحالي
            self.analyze_current_employee()

    def apply_visual_effects(self):
        """تطبيق التأثيرات البصرية"""
        # تطبيق تأثيرات بصرية متقدمة
        try:
            # إضافة تأثيرات الظل والانتقالات
            # هذا يتطلب مكتبات إضافية أو تنفيذ مخصص
            pass
        except Exception as e:
            print(f"خطأ في تطبيق التأثيرات البصرية: {e}")

    def start_smart_updates(self):
        """بدء التحديثات الذكية"""
        # بدء تحديثات دورية للبيانات والتحليلات
        def update_loop():
            try:
                # تحديث الإحصائيات كل 30 ثانية
                self.update_smart_statistics()

                # تحديث التحليلات كل دقيقة
                if hasattr(self, 'current_employee') and self.current_employee:
                    self.update_analytics_panel()

                # جدولة التحديث التالي
                self.window.after(30000, update_loop)  # 30 ثانية

            except Exception as e:
                print(f"خطأ في التحديثات الذكية: {e}")

        # بدء حلقة التحديثات
        self.window.after(1000, update_loop)  # بدء بعد ثانية واحدة

    # وظائف إضافية مساعدة
    def select_photo_enhanced(self):
        """اختيار صورة شخصية محسنة"""
        try:
            file_path = filedialog.askopenfilename(
                title="اختيار صورة شخصية",
                filetypes=[
                    ("ملفات الصور", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                    ("جميع الملفات", "*.*")
                ]
            )

            if file_path:
                self.form_vars['photo_path'].set(file_path)
                self.load_photo_preview_enhanced(file_path)

        except Exception as e:
            self.show_smart_notification("خطأ", f"خطأ في اختيار الصورة: {e}", "error")

    def load_photo_preview_enhanced(self, file_path):
        """تحميل معاينة الصورة المحسنة"""
        try:
            # تحميل وتغيير حجم الصورة مع تحسينات
            image = Image.open(file_path)

            # تطبيق تحسينات على الصورة
            image = image.resize((100, 120), Image.Resampling.LANCZOS)

            # إضافة إطار دائري (اختياري)
            # mask = Image.new('L', (100, 120), 0)
            # draw = ImageDraw.Draw(mask)
            # draw.ellipse((0, 0, 100, 120), fill=255)
            # image.putalpha(mask)

            # تحويل إلى PhotoImage
            photo = ImageTk.PhotoImage(image)

            # عرض الصورة
            self.photo_label.configure(image=photo, text="")
            self.photo_label.image = photo  # الاحتفاظ بمرجع

        except Exception as e:
            print(f"خطأ في تحميل الصورة المحسنة: {e}")
            self.photo_label.configure(text="📷\nخطأ في الصورة")

    def delete_employee_from_database(self, employee_id):
        """حذف الموظف من قاعدة البيانات"""
        try:
            query = "DELETE FROM employees WHERE id = ?"
            self.db_cursor.execute(query, (employee_id,))
            self.db_connection.commit()
        except Exception as e:
            raise Exception(f"خطأ في حذف الموظف من قاعدة البيانات: {e}")

    def update_text_var(self, var_name, widget):
        """تحديث متغير النص"""
        try:
            content = widget.get("1.0", "end-1c")
            self.form_vars[var_name].set(content)
        except:
            pass

    # وظائف إضافية للقوائم السياقية
    def manage_employee_salary(self):
        """إدارة راتب الموظف المحدد"""
        if not self.current_employee:
            self.show_smart_notification("تحذير", "يرجى اختيار موظف أولاً", "warning")
            return

        # فتح نافذة إدارة الراتب للموظف المحدد
        self.manage_salaries_smart()

    def copy_employee_data(self):
        """نسخ بيانات الموظف"""
        if not self.current_employee:
            self.show_smart_notification("تحذير", "يرجى اختيار موظف أولاً", "warning")
            return

        # نسخ البيانات إلى الحافظة
        employee_info = f"""
        الاسم: {self.current_employee[2]}
        الرقم: {self.current_employee[1]}
        القسم: {self.current_employee[7]}
        المنصب: {self.current_employee[8]}
        الراتب: {self.current_employee[11]} ج.م
        """

        self.window.clipboard_clear()
        self.window.clipboard_append(employee_info)
        self.show_smart_notification("نجح", "تم نسخ بيانات الموظف", "success")

    def print_employee_report(self):
        """طباعة تقرير الموظف"""
        if not self.current_employee:
            self.show_smart_notification("تحذير", "يرجى اختيار موظف أولاً", "warning")
            return

        # إنشاء تقرير للطباعة
        self.show_smart_notification("معلومات", "ميزة الطباعة قيد التطوير", "info")

    # وظائف إنشاء المحتوى المتقدم (ستكون فارغة للآن)
    def create_performance_analysis_content(self, parent):
        """إنشاء محتوى تحليل الأداء"""
        info_label = ctk.CTkLabel(
            parent,
            text="📊 نظام تحليل الأداء الشامل قيد التطوير\nسيتم إضافة المزيد من الميزات قريباً",
            font=("Arial", 16),
            text_color=ADVANCED_COLORS['text_primary']
        )
        info_label.pack(pady=50)

    def create_smart_salary_management(self, parent):
        """إنشاء محتوى إدارة الرواتب الذكية"""
        info_label = ctk.CTkLabel(
            parent,
            text="💰 نظام إدارة الرواتب الذكي قيد التطوير\nسيتم إضافة المزيد من الميزات قريباً",
            font=("Arial", 16),
            text_color=ADVANCED_COLORS['text_primary']
        )
        info_label.pack(pady=50)

    def create_smart_suggestions_content(self, parent):
        """إنشاء محتوى الاقتراحات الذكية"""
        info_label = ctk.CTkLabel(
            parent,
            text="🤖 نظام الاقتراحات الذكية قيد التطوير\nسيتم إضافة المزيد من الميزات قريباً",
            font=("Arial", 16),
            text_color="white"
        )
        info_label.pack(pady=50)

    def close_window_smart(self):
        """إغلاق النافذة مع تنظيف ذكي"""
        try:
            # التحقق من التغييرات غير المحفوظة
            if self.has_unsaved_changes():
                result = messagebox.askyesno(
                    "إغلاق النافذة",
                    "هناك تغييرات غير محفوظة. هل تريد إغلاق النافذة؟"
                )
                if not result:
                    return

            # إغلاق قاعدة البيانات
            if hasattr(self, 'db_connection'):
                self.db_connection.close()

            # إغلاق النافذة
            if self.window:
                self.window.destroy()

        except Exception as e:
            print(f"خطأ في إغلاق النافذة الذكية: {e}")

# للتوافق مع الكود الموجود
class EmployeesWindow(AdvancedEmployeesManagement):
    """كلاس للتوافق مع الكود الموجود"""
    pass

# دالة لتشغيل النافذة مستقلة
def main():
    """تشغيل نافذة الموظفين المتقدمة مستقلة"""
    try:
        app = AdvancedEmployeesManagement()
        app.window.mainloop()
    except Exception as e:
        print(f"خطأ في تشغيل النافذة المتقدمة: {e}")

if __name__ == "__main__":
    main()
