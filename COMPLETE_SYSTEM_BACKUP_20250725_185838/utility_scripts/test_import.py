#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import customtkinter as ctk
    print("✅ CustomTkinter imported successfully!")
    print(f"Version: {ctk.__version__}")
    
    # Test creating a simple window
    root = ctk.CTk()
    root.title("Test")
    root.geometry("300x200")
    
    label = ctk.CTkLabel(root, text="CustomTkinter is working!")
    label.pack(pady=20)
    
    print("✅ CustomTkinter window created successfully!")
    root.destroy()  # Close immediately for testing
    
except ImportError as e:
    print(f"❌ Error importing CustomTkinter: {e}")
    print("Please install CustomTkinter using: pip install customtkinter")
except Exception as e:
    print(f"❌ Error testing CustomTkinter: {e}")

try:
    import tkinter as tk
    print("✅ Standard Tkinter is available")
except ImportError:
    print("❌ Standard Tkinter is not available")
