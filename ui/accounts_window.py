# -*- coding: utf-8 -*-
"""
نافذة الحسابات - ملف توجيه للنافذة الأصلية
Accounts Window - Redirect to Original Window
"""

# استيراد النافذة الأصلية من views
try:
    from ui.views.accounts_window import AccountsWindow
except ImportError:
    # في حالة عدم وجود النافذة الأصلية، إنشاء نافذة بسيطة
    import customtkinter as ctk
    from tkinter import messagebox
    
    class AccountsWindow:
        def __init__(self, parent):
            self.parent = parent
            self.window = None
            self.create_window()
        
        def create_window(self):
            self.window = ctk.CTkToplevel(self.parent)
            self.window.title("نظام الحسابات")
            self.window.geometry("800x600")
            
            label = ctk.CTkLabel(
                self.window,
                text="💳 نظام الحسابات\nقيد التطوير",
                font=("Arial", 20)
            )
            label.pack(expand=True)
            
            close_btn = ctk.CTkButton(
                self.window,
                text="إغلاق",
                command=self.window.destroy
            )
            close_btn.pack(pady=20)

# تصدير الفئة
__all__ = ['AccountsWindow']
