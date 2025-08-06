
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    import customtkinter as ctk
    
    # إنشاء نافذة اختبار بسيطة
    root = ctk.CTk()
    root.title("اختبار البرنامج المحاسبي")
    root.geometry("400x300")
    
    label = ctk.CTkLabel(root, text="✅ البرنامج يعمل بشكل صحيح!", font=("Arial", 16))
    label.pack(pady=50)
    
    button = ctk.CTkButton(root, text="إغلاق", command=root.destroy)
    button.pack(pady=20)
    
    print("✅ تم إنشاء نافذة الاختبار")
    root.mainloop()
    
except Exception as e:
    print(f"❌ خطأ في الاختبار: {e}")
    import traceback
    traceback.print_exc()
