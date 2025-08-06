#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test file to verify customtkinter installation
try:
    import customtkinter as ctk
    print("✅ customtkinter imported successfully!")
    print(f"Version: {ctk.__version__}")
    
    # Create a simple test window
    root = ctk.CTk()
    root.title("CustomTkinter Test")
    root.geometry("300x200")
    
    label = ctk.CTkLabel(root, text="CustomTkinter is working!")
    label.pack(pady=20)
    
    button = ctk.CTkButton(root, text="Close", command=root.destroy)
    button.pack(pady=10)
    
    print("✅ CustomTkinter widgets created successfully!")
    print("Test window will appear briefly...")
    
    # Show window briefly then close
    root.after(2000, root.destroy)  # Close after 2 seconds
    root.mainloop()
    
    print("✅ CustomTkinter test completed successfully!")
    
except ImportError as e:
    print(f"❌ Failed to import customtkinter: {e}")
except Exception as e:
    print(f"❌ Error during test: {e}")
