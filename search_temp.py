#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# البحث عن المراجع في الملف
with open('ui/central_control_panel.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("البحث عن مراجع open_sales_window:")
for i, line in enumerate(lines, 1):
    if 'open_sales_window' in line and 'def ' not in line:
        print(f'Line {i}: {line.strip()}')

print("\nالبحث عن مراجع open_purchases_window:")
for i, line in enumerate(lines, 1):
    if 'open_purchases_window' in line and 'def ' not in line:
        print(f'Line {i}: {line.strip()}')

print("\nالبحث عن مراجع open_inventory_window:")
for i, line in enumerate(lines, 1):
    if 'open_inventory_window' in line and 'def ' not in line:
        print(f'Line {i}: {line.strip()}')
