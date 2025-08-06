#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    try:
        import customtkinter as ctk
        from ui.main_window import MainWindow
        
        ctk.set_appearance_mode("light")
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
