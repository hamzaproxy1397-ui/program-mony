# -*- coding: utf-8 -*-
"""
نافذة تسجيل الدخول المبسطة
Simple Login Window
"""

import customtkinter as ctk
from tkinter import messagebox

class LoginWindow:
    """نافذة تسجيل الدخول المبسطة"""
    
    def __init__(self, on_success_callback=None):
        self.on_success_callback = on_success_callback
        self.window = None
        
    def show(self):
        """عرض نافذة تسجيل الدخول"""
        self.window = ctk.CTk()
        self.window.title("تسجيل الدخول")
        self.window.geometry("400x300")
        
        # عنوان
        title = ctk.CTkLabel(
            self.window,
            text="🏢 برنامج ست الكل للمحاسبة",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=30)
        
        # اسم المستخدم
        username_label = ctk.CTkLabel(self.window, text="اسم المستخدم:")
        username_label.pack(pady=5)
        
        self.username_entry = ctk.CTkEntry(self.window, width=200)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "admin")
        
        # كلمة المرور
        password_label = ctk.CTkLabel(self.window, text="كلمة المرور:")
        password_label.pack(pady=5)
        
        self.password_entry = ctk.CTkEntry(self.window, width=200, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "admin")
        
        # زر تسجيل الدخول
        login_btn = ctk.CTkButton(
            self.window,
            text="تسجيل الدخول",
            command=self.login,
            width=200
        )
        login_btn.pack(pady=20)
        
        self.window.mainloop()
    
    def login(self):
        """تسجيل الدخول"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # تحقق بسيط
        if username in ["admin", "123"] and password in ["admin", "123"]:
            user_data = {
                'username': username,
                'full_name': 'مدير النظام',
                'role': 'admin',
                'user_id': 1
            }

            self.window.destroy()

            if self.on_success_callback:
                self.on_success_callback(user_data)
        else:
            messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

    def create_window(self, parent=None):
        """إنشاء النافذة - للتوافق مع الكود القديم"""
        return self.show()

# للتوافق مع الكود القديم
class AuthenticationManager:
    """مدير المصادقة المبسط"""
    
    def __init__(self):
        self.current_user = None
    
    def authenticate(self, username, password):
        """مصادقة المستخدم"""
        if username in ["admin", "123"] and password in ["admin", "123"]:
            self.current_user = {
                'username': username,
                'full_name': 'مدير النظام',
                'role': 'admin',
                'user_id': 1
            }
            return True
        return False
    
    def logout(self):
        """تسجيل الخروج"""
        self.current_user = None
