# -*- coding: utf-8 -*-
"""
نافذة المشتريات - ملف توجيه للنافذة الأصلية
Purchases Window - Redirect to Original Window
"""

# استيراد النافذة الأصلية من views
try:
    from ui.views.purchases_window import PurchasesWindow
except ImportError:
    # في حالة عدم وجود النافذة الأصلية، إنشاء نافذة بسيطة
    import customtkinter as ctk
    from tkinter import messagebox
    
    class PurchasesWindow:
        def __init__(self, parent):
            self.parent = parent
            self.window = None
            self.create_window()
        
        def create_window(self):
            self.window = ctk.CTkToplevel(self.parent)
            self.window.title("نظام المشتريات")
            self.window.geometry("800x600")
            
            label = ctk.CTkLabel(
                self.window,
                text="🛍️ نظام المشتريات\nقيد التطوير",
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
__all__ = ['PurchasesWindow']
