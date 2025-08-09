from ui.components.window_utils import configure_window_fullscreen

def run(self):
    """تشغيل التطبيق"""
    try:
        self.initialize_core_components()
        self.show_welcome_window()
        # تطبيق ملأ الشاشة على النافذة الرئيسية
        configure_window_fullscreen(self.welcome_window, "برنامج ست الكل للمحاسبة")
    except Exception as e:
        self.handle_startup_error(e)
# -*- coding: utf-8 -*-
# cSpell:disable
"""
أدوات النوافذ المساعدة
Window Utilities - Helper functions for window management
"""

import customtkinter as ctk
import tkinter as tk

def make_window_fullscreen(window):
    """
    جعل النافذة تملأ الشاشة بالكامل
    Make window fullscreen

    Args:
        window: النافذة المراد تكبيرها (CTk or CTkToplevel)
    """
    try:
        # الطريقة الأولى - Windows
        if hasattr(window, 'state'):
            window.state('zoomed')
            return True
    except Exception:
        pass

    try:
        # الطريقة الثانية - Linux/Unix
        if hasattr(window, 'attributes'):
            window.attributes('-zoomed', True)
            return True
    except Exception:
        pass

    try:
        # الطريقة الثالثة - الحصول على حجم الشاشة وتطبيقه
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.geometry(f"{screen_width}x{screen_height}+0+0")
        return True
    except Exception:
        pass

    try:
        # الطريقة الرابعة - استخدام tkinter
        window.wm_state('zoomed')
        return True
    except Exception:
        pass

    # إذا فشلت جميع الطرق، استخدم حجم افتراضي كبير
    try:
        window.geometry("1920x1080+0+0")
        return True
    except Exception:
        return False

def configure_window_fullscreen(window, title="برنامج ست الكل للمحاسبة"):
    """
    إعداد النافذة لتملأ الشاشة مع الإعدادات الأساسية
    Configure window for fullscreen with basic settings

    Args:
        window: النافذة المراد إعدادها
        title: عنوان النافذة
    """
    try:
        # تعيين العنوان
        window.title(title)

        # جعل النافذة تملأ الشاشة
        make_window_fullscreen(window)

        # إعدادات إضافية
        try:
            # منع تغيير الحجم (اختياري)
            # window.resizable(False, False)

            # جعل النافذة في المقدمة
            window.lift()
            window.focus_force()

        except Exception:
            pass

        return True

    except Exception as e:
        print(f"خطأ في إعداد النافذة: {e}")
        return False

def create_fullscreen_window(parent=None, title="برنامج ست الكل للمحاسبة"):
    """
    إنشاء نافذة جديدة تملأ الشاشة
    Create new fullscreen window

    Args:
        parent: النافذة الأب (اختياري)
        title: عنوان النافذة

    Returns:
        النافذة الجديدة
    """
    try:
        if parent:
            window = ctk.CTkToplevel(parent)
        else:
            window = ctk.CTk()

        # إعداد النافذة لتملأ الشاشة
        configure_window_fullscreen(window, title)

        return window

    except Exception as e:
        print(f"خطأ في إنشاء النافذة: {e}")
        return None

def center_window_on_screen(window, width=800, height=600):
    """
    توسيط النافذة على الشاشة (للنوافذ الصغيرة)
    Center window on screen (for small windows)

    Args:
        window: النافذة المراد توسيطها
        width: العرض المطلوب
        height: الارتفاع المطلوب
    """
    try:
        # الحصول على أبعاد الشاشة
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # حساب الموضع للتوسيط
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # تطبيق الحجم والموضع
        window.geometry(f"{width}x{height}+{x}+{y}")

        return True

    except Exception as e:
        print(f"خطأ في توسيط النافذة: {e}")
        return False

def apply_fullscreen_to_existing_window(window):
    """
    تطبيق ملء الشاشة على نافذة موجودة
    Apply fullscreen to existing window

    Args:
        window: النافذة الموجودة
    """
    try:
        # تحديث النافذة أولاً
        window.update_idletasks()

        # تطبيق ملء الشاشة
        success = make_window_fullscreen(window)

        if success:
            print("تم تطبيق ملء الشاشة بنجاح")
        else:
            print("فشل في تطبيق ملء الشاشة")

        return success

    except Exception as e:
        print(f"خطأ في تطبيق ملء الشاشة: {e}")
        return False

# إعدادات افتراضية للنوافذ
DEFAULT_WINDOW_CONFIG = {
    'fg_color': '#f0f8ff',  # لون الخلفية الافتراضي
    'corner_radius': 0,     # بدون زوايا مستديرة لملء الشاشة
}

def apply_default_fullscreen_style(window):
    """
    تطبيق الستايل الافتراضي للنوافذ التي تملأ الشاشة
    Apply default fullscreen style

    Args:
        window: النافذة المراد تطبيق الستايل عليها
    """
    try:
        # تطبيق الإعدادات الافتراضية
        for key, value in DEFAULT_WINDOW_CONFIG.items():
            if hasattr(window, 'configure'):
                window.configure(**{key: value})

        return True

    except Exception as e:
        print(f"خطأ في تطبيق الستايل: {e}")
        return False
