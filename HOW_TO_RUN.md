# 🏢 How to Run the Arabic Accounting Software

## 📋 Prerequisites

### 1. Install Python
- Go to: https://www.python.org/downloads/
- Download the latest Python version (3.8 or newer)
- **IMPORTANT**: Check "Add Python to PATH" during installation

### 2. Install Required Libraries
After installing Python, open Command Prompt and run:
```bash
pip install customtkinter pillow numpy matplotlib
```

## 🚀 Ways to Run the Application

### Method 1: Run Main Window Directly
1. Double-click `launch_main_window.bat`
2. Or run `run_main_window.py` directly

### Method 2: Run Full Application
1. Double-click `run.bat`
2. Or run `main.py` directly

### Method 3: Central Control Panel
1. Double-click `START_HERE.py`
2. Or run command: `python START_HERE.py`

## 🔐 Default Login Credentials

### For Main Application:
- **Username**: admin
- **Password**: admin

### For Central Control Panel:
- **Username**: 123
- **Password**: 123

## 📁 Project Structure

```
📦 Arabic Accounting Software
├── 🚀 Launch Files
│   ├── main.py                    # Main application file
│   ├── START_HERE.py              # Central control panel
│   ├── run_main_window.py         # Main window launcher
│   ├── launch_main_window.bat     # Windows batch file
│   └── run.bat                    # Complete launcher
├── 🎨 User Interface
│   ├── ui/main_window.py          # Main window
│   ├── ui/login_window.py         # Login window
│   ├── ui/sales_window.py         # Sales window
│   └── ui/...                     # Other windows
├── 🗄️ Database
│   ├── database/                  # Database managers
│   └── database/accounting.db     # Local database
├── 🎭 Themes & Design
│   └── themes/                    # Theme files
└── 📊 Reports & Logs
    ├── reports/                   # Generated reports
    └── logs/                      # Log files
```

## 🛠️ Troubleshooting

### Issue: "Python not found"
**Solution**: 
1. Make sure Python is installed
2. Make sure Python is added to PATH
3. Restart Command Prompt

### Issue: "Module not found"
**Solution**:
```bash
pip install --upgrade customtkinter pillow numpy matplotlib
```

### Issue: Window doesn't appear
**Solution**:
1. Check taskbar
2. Check log files in `logs/` folder
3. Try running `test_main_window.py` for diagnosis

### Issue: Database error
**Solution**:
1. Check if `database/` folder exists
2. Check write permissions
3. Try deleting `database/accounting.db` to recreate it

## 📞 Technical Support

If you encounter any issues:
1. Check log files in `logs/app.log`
2. Try running `test_main_window.py` for diagnosis
3. Make sure all requirements are installed

## 🎯 Key Features

- ✅ Sales and Purchase Management
- ✅ Inventory and Warehouse Management
- ✅ Integrated Accounting System
- ✅ Financial Reports
- ✅ Customer and Supplier Management
- ✅ Invoice System
- ✅ Employee Management
- ✅ Automatic Backup System

## 🔧 Development Notes

The application has been comprehensively refactored with:
- Enhanced error handling and exception management
- Improved Arabic/RTL UI support
- Cross-platform compatibility
- Security best practices
- Performance optimizations
- Comprehensive documentation

---
**Developed by Set Al-Kol Software Team**
