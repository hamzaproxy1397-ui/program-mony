#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Comprehensive Audit Tool
Arabic Accounting Software Complete System Analysis
"""

import os
import json
from pathlib import Path
from datetime import datetime

def analyze_directory_structure():
    """Analyze the complete directory structure"""
    print("📁 Analyzing directory structure...")
    
    structure = {
        'total_files': 0,
        'total_directories': 0,
        'by_extension': {},
        'by_category': {
            'core_files': [],
            'ui_files': [],
            'database_files': [],
            'config_files': [],
            'backup_files': [],
            'documentation': [],
            'assets': [],
            'utility_scripts': []
        },
        'largest_files': [],
        'python_files': []
    }
    
    # Walk through all files
    for root, dirs, files in os.walk('.'):
        root_path = Path(root)
        
        structure['total_directories'] += len(dirs)
        
        for file in files:
            file_path = root_path / file
            relative_path = str(file_path)
            
            try:
                file_size = file_path.stat().st_size
                structure['total_files'] += 1
                
                # Track by extension
                ext = file_path.suffix.lower()
                structure['by_extension'][ext] = structure['by_extension'].get(ext, 0) + 1
                
                # Categorize files
                if file in ['main.py', 'START_HERE.py', 'app_core.py']:
                    structure['by_category']['core_files'].append(relative_path)
                elif 'ui' in str(file_path) and ext == '.py':
                    structure['by_category']['ui_files'].append(relative_path)
                elif 'database' in str(file_path):
                    structure['by_category']['database_files'].append(relative_path)
                elif 'config' in str(file_path) or ext in ['.json', '.ini']:
                    structure['by_category']['config_files'].append(relative_path)
                elif 'backup' in relative_path.lower() or ext in ['.backup', '.bak']:
                    structure['by_category']['backup_files'].append(relative_path)
                elif ext in ['.md', '.txt'] or 'docs' in str(file_path):
                    structure['by_category']['documentation'].append(relative_path)
                elif 'assets' in str(file_path) or ext in ['.png', '.jpg', '.ico', '.ttf']:
                    structure['by_category']['assets'].append(relative_path)
                elif any(pattern in file for pattern in ['_fixer', '_checker', '_analyzer', 'test_']):
                    structure['by_category']['utility_scripts'].append(relative_path)
                
                # Track Python files
                if ext == '.py':
                    structure['python_files'].append(relative_path)
                
                # Track largest files
                structure['largest_files'].append((relative_path, file_size))
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    # Sort largest files
    structure['largest_files'].sort(key=lambda x: x[1], reverse=True)
    structure['largest_files'] = structure['largest_files'][:20]  # Top 20
    
    return structure

def check_critical_files():
    """Check for critical system files"""
    print("🔍 Checking critical files...")
    
    critical_files = {
        'core_application': [
            'main.py',
            'START_HERE.py',
            'ui/main_window.py',
            'ui/login_window.py'
        ],
        'database_system': [
            'database/hybrid_database_manager.py',
            'database/database_manager.py',
            'database/accounting.db'
        ],
        'configuration': [
            'config/settings.py',
            'themes/modern_theme.py',
            'requirements.txt'
        ],
        'essential_ui': [
            'ui/sales_window.py',
            'ui/purchases_window.py',
            'ui/reports_window.py',
            'ui/accounts_window.py'
        ]
    }
    
    status = {}
    missing_files = []
    
    for category, files in critical_files.items():
        status[category] = {'found': [], 'missing': []}
        
        for file_path in files:
            if os.path.exists(file_path):
                status[category]['found'].append(file_path)
            else:
                status[category]['missing'].append(file_path)
                missing_files.append(file_path)
    
    return status, missing_files

def analyze_backup_system():
    """Analyze the backup system"""
    print("💾 Analyzing backup system...")
    
    backup_analysis = {
        'backup_directories': [],
        'backup_files_count': 0,
        'backup_patterns': {},
        'total_backup_size': 0
    }
    
    # Find backup directories
    for item in os.listdir('.'):
        if os.path.isdir(item) and 'backup' in item.lower():
            backup_analysis['backup_directories'].append(item)
            
            # Count files in backup directory
            try:
                for root, dirs, files in os.walk(item):
                    backup_analysis['backup_files_count'] += len(files)
                    
                    for file in files:
                        file_path = Path(root) / file
                        try:
                            backup_analysis['total_backup_size'] += file_path.stat().st_size
                        except:
                            pass
            except Exception as e:
                print(f"Error analyzing backup directory {item}: {e}")
    
    # Analyze backup patterns
    for root, dirs, files in os.walk('.'):
        for file in files:
            if '.backup' in file or '.bak' in file:
                backup_analysis['backup_files_count'] += 1
                
                # Extract date pattern
                import re
                date_match = re.search(r'(\d{8})', file)
                if date_match:
                    date = date_match.group(1)
                    backup_analysis['backup_patterns'][date] = backup_analysis['backup_patterns'].get(date, 0) + 1
    
    return backup_analysis

def generate_preservation_recommendations():
    """Generate preservation recommendations"""
    print("📋 Generating preservation recommendations...")
    
    recommendations = [
        "🔥 CRITICAL: Backup the entire 'ui' directory - contains all user interface components",
        "🔥 CRITICAL: Backup the entire 'database' directory - contains all data management code",
        "🔥 CRITICAL: Backup main.py and START_HERE.py - core application entry points",
        "⚠️ IMPORTANT: Backup 'config' directory - contains system configuration",
        "⚠️ IMPORTANT: Backup 'themes' directory - contains UI styling",
        "⚠️ IMPORTANT: Backup 'assets' directory - contains images, fonts, and icons",
        "📦 USEFUL: Archive old backup directories to reduce clutter",
        "📦 USEFUL: Backup 'services' directory - contains business logic",
        "📦 USEFUL: Backup all .md and .txt documentation files",
        "🔧 MAINTENANCE: Consider archiving utility scripts after system is stable"
    ]
    
    return recommendations

def create_comprehensive_report():
    """Create the comprehensive audit report"""
    print("📊 Creating comprehensive audit report...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gather all analysis data
    structure = analyze_directory_structure()
    critical_status, missing_files = check_critical_files()
    backup_analysis = analyze_backup_system()
    recommendations = generate_preservation_recommendations()
    
    # Create comprehensive report
    report = {
        'audit_metadata': {
            'timestamp': timestamp,
            'audit_type': 'Comprehensive System Audit and Backup Analysis',
            'system_name': 'Arabic Accounting Software - Complete Business System'
        },
        
        'system_overview': {
            'total_files': structure['total_files'],
            'total_directories': structure['total_directories'],
            'python_files_count': len(structure['python_files']),
            'backup_files_count': backup_analysis['backup_files_count'],
            'backup_directories_count': len(backup_analysis['backup_directories'])
        },
        
        'file_analysis': {
            'by_extension': dict(sorted(structure['by_extension'].items(), key=lambda x: x[1], reverse=True)),
            'by_category': {k: len(v) for k, v in structure['by_category'].items()},
            'largest_files': structure['largest_files'][:10]
        },
        
        'critical_files_status': critical_status,
        'missing_critical_files': missing_files,
        
        'backup_system_analysis': backup_analysis,
        
        'file_categories': structure['by_category'],
        
        'preservation_strategy': {
            'priority_1_critical': structure['by_category']['core_files'] + structure['by_category']['ui_files'] + structure['by_category']['database_files'],
            'priority_2_important': structure['by_category']['config_files'] + structure['by_category']['assets'],
            'priority_3_useful': structure['by_category']['documentation'] + structure['by_category']['utility_scripts'],
            'priority_4_archival': structure['by_category']['backup_files']
        },
        
        'recommendations': recommendations,
        
        'system_health': {
            'critical_files_missing': len(missing_files),
            'backup_system_active': len(backup_analysis['backup_directories']) > 0,
            'total_system_size_mb': sum(size for _, size in structure['largest_files']) / (1024 * 1024),
            'backup_coverage': 'Extensive' if backup_analysis['backup_files_count'] > 100 else 'Moderate' if backup_analysis['backup_files_count'] > 10 else 'Limited'
        }
    }
    
    return report, timestamp

def main():
    """Main execution function"""
    print("🔍 COMPREHENSIVE SYSTEM AUDIT AND BACKUP ANALYSIS")
    print("=" * 70)
    print("Arabic Accounting Software - Complete Business System")
    print("=" * 70)
    
    try:
        # Generate comprehensive report
        report, timestamp = create_comprehensive_report()
        
        # Save report to JSON file
        report_filename = f"COMPREHENSIVE_AUDIT_REPORT_{timestamp}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Print executive summary
        print("\n📊 EXECUTIVE SUMMARY")
        print("=" * 50)
        
        overview = report['system_overview']
        health = report['system_health']
        
        print(f"📁 Total Files: {overview['total_files']:,}")
        print(f"📂 Total Directories: {overview['total_directories']:,}")
        print(f"🐍 Python Files: {overview['python_files_count']:,}")
        print(f"💾 Backup Files: {overview['backup_files_count']:,}")
        print(f"📦 Backup Directories: {overview['backup_directories_count']}")
        
        print(f"\n🏥 SYSTEM HEALTH")
        print(f"   Critical Files Missing: {health['critical_files_missing']}")
        print(f"   Backup System: {'✅ Active' if health['backup_system_active'] else '❌ Inactive'}")
        print(f"   Backup Coverage: {health['backup_coverage']}")
        print(f"   System Size: {health['total_system_size_mb']:.1f} MB")
        
        print(f"\n🎯 TOP RECOMMENDATIONS")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n📄 DETAILED REPORT SAVED: {report_filename}")
        print("\n✅ COMPREHENSIVE AUDIT COMPLETED SUCCESSFULLY!")
        
        return report_filename
        
    except Exception as e:
        print(f"❌ Error during audit: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
