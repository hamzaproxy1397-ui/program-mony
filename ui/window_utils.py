# -*- coding: utf-8 -*-
"""
أدوات النوافذ المساعدة
Window Utilities
"""

def configure_window_fullscreen(window, enable=True):
    """تكوين النافذة لملء الشاشة"""
    if not enable:
        return

    try:
        window.state('zoomed')  # Windows
    except:
        try:
            window.attributes('-zoomed', True)  # Linux
        except:
            # كبديل - استخدام حجم الشاشة
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            window.geometry(f"{screen_width}x{screen_height}+0+0")
