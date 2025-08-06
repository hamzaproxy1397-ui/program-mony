# -*- coding: utf-8 -*-
"""
مدير التطبيق المركزي - Application Manager
نظام إدارة دورة حياة التطبيق الموحد للبرنامج المحاسبي العربي

هذا الملف يوفر:
- إدارة موحدة لدورة حياة التطبيق
- نقاط دخول متعددة ومرنة
- معالجة شاملة للأخطاء
- إدارة الموارد والتنظيف
- تكوين موحد للتطبيق
"""

import sys
import os
import logging
import traceback
from pathlib import Path
from typing import Optional, Dict, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# إضافة مسار المشروع
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# استيراد المكتبات الأساسية
try:
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import messagebox
    CTK_AVAILABLE = True
except ImportError as e:
    print(f"تحذير: فشل في استيراد customtkinter: {e}")
    CTK_AVAILABLE = False

# استيراد الوحدات المحلية
try:
    from config.settings import WINDOW_TITLE, WINDOW_MIN_SIZE
    from themes.theme_manager import ThemeManager
    from database.hybrid_database_manager import HybridDatabaseManager
except ImportError as e:
    print(f"تحذير: فشل في استيراد بعض الوحدات: {e}")

class LaunchMode(Enum):
    """أنماط تشغيل التطبيق"""
    NORMAL = "normal"           # التشغيل العادي مع الترحيب وتسجيل الدخول
    DIRECT = "direct"           # التشغيل المباشر للنافذة الرئيسية
    ADMIN = "admin"             # التشغيل بصلاحيات المدير
    DEVELOPMENT = "development" # وضع التطوير
    PRODUCTION = "production"   # وضع الإنتاج

@dataclass
class ApplicationConfig:
    """تكوين التطبيق الموحد"""
    launch_mode: LaunchMode = LaunchMode.NORMAL
    skip_welcome: bool = False
    skip_login: bool = False
    auto_login_user: Optional[Dict[str, Any]] = None
    enable_scheduler: bool = True
    enable_error_handling: bool = True
    enable_logging: bool = True
    fullscreen: bool = True
    debug_mode: bool = False

class ApplicationState(Enum):
    """حالات التطبيق"""
    INITIALIZING = "initializing"
    WELCOME = "welcome"
    LOGIN = "login"
    MAIN_WINDOW = "main_window"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    ERROR = "error"

class ApplicationManager:
    """
    مدير التطبيق المركزي
    Central Application Manager

    يدير جميع جوانب دورة حياة التطبيق:
    - التهيئة والإعداد
    - إدارة النوافذ
    - معالجة الأخطاء
    - تنظيف الموارد
    - نقاط الدخول المتعددة
    """

    _instance: Optional['ApplicationManager'] = None
    _initialized: bool = False

    def __new__(cls, config: Optional[ApplicationConfig] = None):
        """تطبيق نمط Singleton لضمان وجود مثيل واحد فقط"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[ApplicationConfig] = None):
        """تهيئة مدير التطبيق"""
        if self._initialized:
            return

        # تكوين التطبيق
        self.config = config or ApplicationConfig()
        self.state = ApplicationState.INITIALIZING

        # متغيرات التطبيق الأساسية
        self.main_application: Optional[Any] = None
        self.current_window: Optional[ctk.CTk] = None
        self.current_user: Optional[Dict[str, Any]] = None
        self.scheduler_manager: Optional[Any] = None
        self.theme_manager: Optional[ThemeManager] = None
        self.db_manager: Optional[HybridDatabaseManager] = None

        # معلومات التشغيل
        self.start_time = datetime.now()
        self.launch_mode = self.config.launch_mode
        self.error_count = 0
        self.last_error: Optional[Exception] = None

        # إعداد النظام
        self._setup_logging()
        self._setup_error_handling()
        self._setup_customtkinter()

        self._initialized = True
        self.logger.info("تم تهيئة مدير التطبيق بنجاح")

    def _setup_logging(self) -> None:
        """إعداد نظام السجلات"""
        if not self.config.enable_logging:
            return

        try:
            # إنشاء مجلد السجلات إذا لم يكن موجوداً
            logs_dir = PROJECT_ROOT / "logs"
            logs_dir.mkdir(exist_ok=True)

            # إعداد السجل
            log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"

            logging.basicConfig(
                level=logging.DEBUG if self.config.debug_mode else logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.info(f"بدء تشغيل التطبيق - وضع: {self.launch_mode.value}")

        except Exception as e:
            print(f"تحذير: فشل في إعداد نظام السجلات: {e}")
            self.logger = logging.getLogger(self.__class__.__name__)

    def _setup_error_handling(self) -> None:
        """إعداد معالجة الأخطاء العامة"""
        if not self.config.enable_error_handling:
            return

        def handle_exception(exc_type, exc_value, exc_traceback):
            """معالج الاستثناءات العام"""
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            self.error_count += 1
            self.last_error = exc_value

            error_msg = f"خطأ غير متوقع: {exc_value}"
            self.logger.error(error_msg, exc_info=(exc_type, exc_value, exc_traceback))

            # عرض رسالة خطأ للمستخدم
            try:
                if CTK_AVAILABLE:
                    messagebox.showerror("خطأ في التطبيق", error_msg)
            except:
                print(f"خطأ حرج: {error_msg}")

        sys.excepthook = handle_exception

    def _setup_customtkinter(self) -> None:
        """إعداد customtkinter"""
        if not CTK_AVAILABLE:
            return

        try:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            self.logger.info("تم إعداد customtkinter بنجاح")
        except Exception as e:
            self.logger.warning(f"فشل في إعداد customtkinter: {e}")

    def initialize_components(self) -> bool:
        """تهيئة مكونات التطبيق الأساسية"""
        try:
            # تهيئة مدير الثيم
            self._initialize_theme_manager()

            # تهيئة مدير قاعدة البيانات
            self._initialize_database_manager()

            # تهيئة مدير الجدولة إذا كان مطلوباً
            if self.config.enable_scheduler:
                self._initialize_scheduler()

            self.logger.info("تم تهيئة جميع مكونات التطبيق بنجاح")
            return True

        except Exception as e:
            self.logger.error(f"فشل في تهيئة مكونات التطبيق: {e}")
            return False

    def _initialize_theme_manager(self) -> None:
        """تهيئة مدير الثيم"""
        try:
            self.theme_manager = ThemeManager()
            self.logger.info("تم تحميل مدير الثيم بنجاح")
        except Exception as e:
            self.logger.warning(f"فشل في تحميل مدير الثيم: {e}")
            self.theme_manager = None

    def _initialize_database_manager(self) -> None:
        """تهيئة مدير قاعدة البيانات"""
        try:
            self.db_manager = HybridDatabaseManager()
            self.logger.info("تم تهيئة مدير قاعدة البيانات بنجاح")
        except Exception as e:
            self.logger.error(f"فشل في تهيئة مدير قاعدة البيانات: {e}")
            self.db_manager = None

    def _initialize_scheduler(self) -> None:
        """تهيئة مدير الجدولة"""
        try:
            from core.scheduler_manager import SchedulerManager
            self.scheduler_manager = SchedulerManager()
            self.scheduler_manager.start_scheduler()
            self.logger.info("تم تشغيل نظام الجدولة التلقائية")
        except Exception as e:
            self.logger.warning(f"فشل في تهيئة مدير الجدولة: {e}")
            self.scheduler_manager = None

    def launch_application(self) -> bool:
        """تشغيل التطبيق حسب الوضع المحدد"""
        try:
            self.logger.info(f"بدء تشغيل التطبيق - الوضع: {self.launch_mode.value}")

            # تهيئة المكونات
            if not self.initialize_components():
                self.logger.error("فشل في تهيئة مكونات التطبيق")
                return False

            # تحديد مسار التشغيل حسب الوضع
            if self.launch_mode == LaunchMode.DIRECT:
                return self._launch_direct_mode()
            elif self.launch_mode == LaunchMode.ADMIN:
                return self._launch_admin_mode()
            elif self.launch_mode == LaunchMode.DEVELOPMENT:
                return self._launch_development_mode()
            elif self.launch_mode == LaunchMode.PRODUCTION:
                return self._launch_production_mode()
            else:  # NORMAL
                return self._launch_normal_mode()

        except Exception as e:
            self.logger.error(f"فشل في تشغيل التطبيق: {e}")
            return False

    def _launch_normal_mode(self) -> bool:
        """تشغيل التطبيق في الوضع العادي"""
        try:
            from ui.main_window import MainApplication

            self.main_application = MainApplication()
            self.main_application.scheduler_manager = self.scheduler_manager

            # تشغيل التطبيق (ترحيب -> تسجيل دخول -> نافذة رئيسية)
            self.state = ApplicationState.RUNNING
            self.main_application.run()

            return True

        except Exception as e:
            self.logger.error(f"فشل في تشغيل الوضع العادي: {e}")
            return False

    def _launch_direct_mode(self) -> bool:
        """تشغيل التطبيق في الوضع المباشر (تخطي الترحيب وتسجيل الدخول)"""
        try:
            from ui.main_window import MainApplication

            self.main_application = MainApplication()
            self.main_application.scheduler_manager = self.scheduler_manager

            # تعيين مستخدم افتراضي
            default_user = self.config.auto_login_user or {
                'username': 'admin',
                'user_id': 1,
                'role': 'admin',
                'permissions': ['all'],
                'full_name': 'مدير النظام',
                'email': 'admin@company.com'
            }

            self.main_application.current_user = default_user
            self.current_user = default_user

            # الانتقال مباشرة للنافذة الرئيسية
            self.state = ApplicationState.MAIN_WINDOW
            self.main_application.create_main_window()

            return True

        except Exception as e:
            self.logger.error(f"فشل في تشغيل الوضع المباشر: {e}")
            return False

    def _launch_admin_mode(self) -> bool:
        """تشغيل التطبيق في وضع المدير"""
        try:
            from ui.main_window import MainApplication

            self.main_application = MainApplication()
            self.main_application.scheduler_manager = self.scheduler_manager

            # تعيين مستخدم مدير
            admin_user = {
                'username': 'admin',
                'user_id': 1,
                'role': 'admin',
                'permissions': ['all'],
                'full_name': 'مدير النظام',
                'email': 'admin@company.com',
                'is_admin': True
            }

            self.main_application.current_user = admin_user
            self.current_user = admin_user

            self.logger.info("تم تشغيل التطبيق في وضع المدير")

            # الانتقال مباشرة للنافذة الرئيسية
            self.state = ApplicationState.MAIN_WINDOW
            self.main_application.create_main_window()

            return True

        except Exception as e:
            self.logger.error(f"فشل في تشغيل وضع المدير: {e}")
            return False

    def _launch_development_mode(self) -> bool:
        """تشغيل التطبيق في وضع التطوير"""
        try:
            # تفعيل وضع التطوير
            self.config.debug_mode = True
            self.logger.setLevel(logging.DEBUG)

            self.logger.debug("تشغيل التطبيق في وضع التطوير")

            # تشغيل مثل الوضع المباشر مع تسجيل إضافي
            return self._launch_direct_mode()

        except Exception as e:
            self.logger.error(f"فشل في تشغيل وضع التطوير: {e}")
            return False

    def _launch_production_mode(self) -> bool:
        """تشغيل التطبيق في وضع الإنتاج"""
        try:
            # إعدادات الإنتاج
            self.config.debug_mode = False
            self.logger.setLevel(logging.INFO)

            self.logger.info("تشغيل التطبيق في وضع الإنتاج")

            # تشغيل الوضع العادي
            return self._launch_normal_mode()

        except Exception as e:
            self.logger.error(f"فشل في تشغيل وضع الإنتاج: {e}")
            return False

    def shutdown(self) -> None:
        """إغلاق التطبيق وتنظيف الموارد"""
        try:
            self.state = ApplicationState.SHUTTING_DOWN
            self.logger.info("بدء إغلاق التطبيق...")

            # تنظيف الموارد
            self._cleanup_resources()

            # إغلاق النوافذ
            if self.current_window:
                try:
                    self.current_window.destroy()
                except:
                    pass

            # إيقاف الجدولة
            if self.scheduler_manager:
                try:
                    self.scheduler_manager.stop_scheduler()
                except:
                    pass

            # إغلاق قاعدة البيانات
            if self.db_manager:
                try:
                    self.db_manager.close_connection()
                except:
                    pass

            self.logger.info("تم إغلاق التطبيق بنجاح")

        except Exception as e:
            self.logger.error(f"خطأ أثناء إغلاق التطبيق: {e}")

    def _cleanup_resources(self) -> None:
        """تنظيف الموارد"""
        try:
            # مسح ذاكرة التخزين المؤقت للصور
            if self.main_application and hasattr(self.main_application, 'clear_image_cache'):
                self.main_application.clear_image_cache()

            # تنظيف المتغيرات
            self.current_user = None
            self.last_error = None

            self.logger.info("تم تنظيف الموارد بنجاح")

        except Exception as e:
            self.logger.warning(f"خطأ في تنظيف الموارد: {e}")

    def get_application_info(self) -> Dict[str, Any]:
        """الحصول على معلومات التطبيق"""
        uptime = datetime.now() - self.start_time

        return {
            'launch_mode': self.launch_mode.value,
            'state': self.state.value,
            'uptime': str(uptime),
            'error_count': self.error_count,
            'current_user': self.current_user.get('username') if self.current_user else None,
            'components': {
                'theme_manager': self.theme_manager is not None,
                'db_manager': self.db_manager is not None,
                'scheduler_manager': self.scheduler_manager is not None
            }
        }