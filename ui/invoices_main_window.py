# -*- coding: utf-8 -*-
"""
نافذة الفواتير الرئيسية - ملف توجيه للنافذة الأصلية
Main Invoices Window - Redirect to Original Window
"""

# استيراد النافذة الأصلية من views
try:
    from ui.views.invoices_main_window import InvoicesMainWindow
except ImportError:
    # في حالة عدم وجود النافذة الأصلية، إنشاء نافذة بسيطة
    import customtkinter as ctk
    from tkinter import messagebox
    
    class InvoicesMainWindow:
        def __init__(self, parent):
            self.parent = parent
            self.window = None
            self.create_window()
        
        def create_window(self):
            self.window = ctk.CTkToplevel(self.parent)
            self.window.title("نظام الفواتير")
            self.window.geometry("800x600")
            
            label = ctk.CTkLabel(
                self.window,
                text="📋 نظام الفواتير\nقيد التطوير",
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
__all__ = ['InvoicesMainWindow']
