# -*- coding: utf-8 -*-
"""
معالج الأخطاء المتقدم للبرنامج المحاسبي
Advanced Error Handler for Accounting Software
"""

import functools
import traceback
import logging
from datetime import datetime

# إعداد نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/error.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def error_handler(func):
    """مُزخرف لمعالجة الأخطاء العامة"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"خطأ في {func.__name__}: {e}"
            logger.error(error_msg)
            print(error_msg)
            return None
    return wrapper

def db_error_handler(func):
    """مُزخرف لمعالجة أخطاء قاعدة البيانات"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"خطأ في قاعدة البيانات - {func.__name__}: {e}"
            logger.error(error_msg)
            print(error_msg)
            return None
    return wrapper

def setup_global_exception_handler():
    """إعداد معالج الأخطاء العام"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = f"خطأ غير معالج: {exc_type.__name__}: {exc_value}"
        logger.critical(error_msg, exc_info=(exc_type, exc_value, exc_traceback))
    
    import sys
    sys.excepthook = handle_exception

def handle_ui_error(error):
    """معالجة أخطاء الواجهة"""
    error_msg = f"خطأ في الواجهة: {error}"
    logger.error(error_msg)
    print(error_msg)

def handle_db_operation(func):
    """معالجة عمليات قاعدة البيانات"""
    return db_error_handler(func)

def log_error(message):
    """تسجيل خطأ"""
    logger.error(message)
    print(f"خطأ: {message}")

def log_info(message):
    """تسجيل معلومات"""
    logger.info(message)
    print(f"معلومات: {message}")

def log_warning(message):
    """تسجيل تحذير"""
    logger.warning(message)
    print(f"تحذير: {message}")

def log_debug(message):
    """تسجيل تصحيح"""
    logger.debug(message)

def safe_execute(func, *args, **kwargs):
    """تنفيذ آمن للدوال"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_error(f"خطأ في تنفيذ {func.__name__}: {e}")
        return None
