# Copilot Instructions for AI Agents

## Overview
This repository contains a comprehensive accounting and sales management system tailored for Arabic-speaking businesses. The system supports RTL (Right-to-Left) layouts and offers advanced features for database management, user authentication, inventory tracking, and more. The project is structured to support both SQLite and PostgreSQL databases with seamless switching capabilities.

## Key Components

### 1. Core Modules
- **Sales Management**: Handles invoice creation, tax calculations, and payment tracking.
- **Purchases Management**: Manages supplier invoices and stock updates.
- **Inventory Management**: Tracks stock levels, generates alerts, and provides movement reports.
- **User Authentication**: Implements secure login with role-based access control (Admin, Accountant, User).

### 2. Control Panel
- Located in `control_panel/`.
- Provides a modern, responsive UI for managing application settings.
- Key files:
  - `control_panel_window.py`: Main control panel interface.
  - `settings_pages/`: Contains modules for specific settings (e.g., `general_settings.py`, `accounting_settings.py`).

### 3. Windows
- Located in `windows/`.
- Example: `Professional Item Entry Window` for managing item details with advanced validation and AI-driven suggestions.

## Developer Workflows

### 1. Setting Up the Environment
- Ensure Python 3.9+ is installed.
- Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Running the Application
- Use the provided batch files for quick execution:
  - `🚀_تشغيل_البرنامج_المحاسبي_النهائي.bat`
  - `🚀_تشغيل_البرنامج_المحاسبي_المحسن_2025.bat`

### 3. Testing
- Run tests using:
  ```bash
  pytest tests/
  ```

### 4. Debugging
- Logs are stored in the `logs/` directory.
- Use `advanced_error_analyzer.py` for detailed error analysis.

## Project-Specific Conventions

### 1. Localization
- All UI components must support Arabic and RTL layouts.
- Use `Cairo` font for consistency.

### 2. Database Management
- Default database: SQLite.
- For production, switch to PostgreSQL by updating the configuration in `config.py`.

### 3. Code Style
- Follow PEP 8 guidelines.
- Use descriptive variable names in Arabic where applicable.

## Integration Points

### 1. External Libraries
- `PyQt5`: For UI components.
- `SQLAlchemy`: For database interactions.

### 2. Cross-Component Communication
- Use the `event_bus` module for decoupled communication between components.

## Examples

### Adding a New Setting Page
1. Create a new file in `control_panel/settings_pages/` (e.g., `new_setting.py`).
2. Define the UI and logic for the setting.
3. Register the page in `control_panel_window.py`.

### Debugging a Database Issue
1. Check the logs in `logs/`.
2. Use `comprehensive_system_checker.py` to validate database integrity.
3. Run `comprehensive_dependency_checker.py` to identify missing dependencies.

---

For further details, refer to the `README.md` files in the root, `control_panel/`, and `windows/` directories.
