#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive System Audit and Backup Tool
Arabic Accounting Software Complete Preservation System
"""

import os
import sys
import ast
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any
import traceback

class ComprehensiveSystemAudit:
    """Complete system audit and backup tool for Arabic Accounting Software"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.audit_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize data structures
        self.file_inventory = {}
        self.python_files = {}
        self.dependencies = {}
        self.backup_files = {}
        self.critical_files = {
            'core_application': [],
            'ui_components': [],
            'database_files': [],
            'configuration': [],
            'assets': [],
            'documentation': [],
            'backup_files': [],
            'utility_scripts': []
        }
        self.syntax_errors = []
        self.missing_dependencies = []
        self.file_sizes = {}
        self.modification_dates = {}
        
        # Define critical file patterns
        self.critical_patterns = {
            'core_application': ['main.py', 'START_HERE.py', 'app_core.py'],
            'ui_components': ['ui/*.py', 'themes/*.py'],
            'database_files': ['database/*.py', 'database/*.db', 'database/*.sql'],
            'configuration': ['config/*.py', 'config/*.json', '*.ini', 'requirements*.txt'],
            'assets': ['assets/**/*', 'fonts/**/*', 'icons/**/*', 'images/**/*'],
            'documentation': ['*.md', '*.txt', 'docs/**/*'],
            'backup_files': ['backup*/**/*', '*.backup', '*.bak'],
            'utility_scripts': ['*_fixer.py', '*_checker.py', '*_analyzer.py', 'test_*.py']
        }

    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get comprehensive file information"""
        try:
            stat = file_path.stat()
            
            # Calculate file hash for integrity checking
            file_hash = ""
            if file_path.is_file() and stat.st_size < 50 * 1024 * 1024:  # Skip files > 50MB
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                except:
                    pass
            
            return {
                'path': str(file_path.relative_to(self.root_path)),
                'absolute_path': str(file_path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'is_file': file_path.is_file(),
                'is_directory': file_path.is_dir(),
                'extension': file_path.suffix.lower(),
                'hash': file_hash,
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK)
            }
        except Exception as e:
            return {
                'path': str(file_path.relative_to(self.root_path)),
                'error': str(e)
            }

    def inventory_all_files(self) -> None:
        """Create complete inventory of all files and directories"""
        print("📁 Creating complete file inventory...")
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            # Process directories
            for dir_name in dirs:
                dir_path = root_path / dir_name
                self.file_inventory[str(dir_path.relative_to(self.root_path))] = self.get_file_info(dir_path)
            
            # Process files
            for file_name in files:
                file_path = root_path / file_name
                relative_path = str(file_path.relative_to(self.root_path))
                
                file_info = self.get_file_info(file_path)
                self.file_inventory[relative_path] = file_info
                
                # Store size and modification date for quick access
                if file_info.get('size'):
                    self.file_sizes[relative_path] = file_info['size']
                if file_info.get('modified'):
                    self.modification_dates[relative_path] = file_info['modified']
                
                # Categorize files
                self.categorize_file(file_path, file_info)

    def categorize_file(self, file_path: Path, file_info: Dict) -> None:
        """Categorize files by their importance and type"""
        relative_path = str(file_path.relative_to(self.root_path))
        
        # Check against critical patterns
        if file_path.name in ['main.py', 'START_HERE.py', 'app_core.py']:
            self.critical_files['core_application'].append(relative_path)
        elif file_path.suffix == '.py' and 'ui' in file_path.parts:
            self.critical_files['ui_components'].append(relative_path)
        elif 'database' in file_path.parts:
            self.critical_files['database_files'].append(relative_path)
        elif 'config' in file_path.parts or file_path.suffix in ['.json', '.ini']:
            self.critical_files['configuration'].append(relative_path)
        elif 'assets' in file_path.parts or file_path.suffix in ['.png', '.jpg', '.ico', '.ttf']:
            self.critical_files['assets'].append(relative_path)
        elif file_path.suffix in ['.md', '.txt'] or 'docs' in file_path.parts:
            self.critical_files['documentation'].append(relative_path)
        elif 'backup' in relative_path.lower() or file_path.suffix in ['.backup', '.bak']:
            self.critical_files['backup_files'].append(relative_path)
            self.backup_files[relative_path] = file_info
        elif any(pattern in file_path.name for pattern in ['_fixer', '_checker', '_analyzer', 'test_']):
            self.critical_files['utility_scripts'].append(relative_path)

    def analyze_python_dependencies(self) -> None:
        """Analyze all Python files for imports and dependencies"""
        print("🔍 Analyzing Python file dependencies...")
        
        for file_path, file_info in self.file_inventory.items():
            if file_info.get('extension') == '.py' and file_info.get('is_file'):
                try:
                    full_path = self.root_path / file_path
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Parse AST to find imports
                    try:
                        tree = ast.parse(content)
                        imports = []
                        
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.append(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.append(node.module)
                        
                        self.python_files[file_path] = {
                            'imports': imports,
                            'lines': len(content.splitlines()),
                            'size': len(content),
                            'syntax_valid': True
                        }
                        
                    except SyntaxError as e:
                        self.syntax_errors.append({
                            'file': file_path,
                            'error': str(e),
                            'line': getattr(e, 'lineno', 'unknown')
                        })
                        self.python_files[file_path] = {
                            'imports': [],
                            'lines': 0,
                            'size': len(content),
                            'syntax_valid': False,
                            'syntax_error': str(e)
                        }
                        
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")

    def check_missing_dependencies(self) -> None:
        """Check for missing file dependencies"""
        print("🔗 Checking for missing dependencies...")
        
        all_imports = set()
        local_modules = set()
        
        # Collect all imports and local modules
        for file_path, info in self.python_files.items():
            all_imports.update(info.get('imports', []))
            
            # Check if this is a local module
            if file_path.endswith('.py'):
                module_path = file_path.replace('/', '.').replace('\\', '.').replace('.py', '')
                local_modules.add(module_path)
        
        # Check for missing local dependencies
        for import_name in all_imports:
            if '.' in import_name:
                # Check if local module exists
                possible_paths = [
                    import_name.replace('.', '/') + '.py',
                    import_name.replace('.', '\\') + '.py'
                ]
                
                found = False
                for possible_path in possible_paths:
                    if possible_path in self.file_inventory:
                        found = True
                        break
                
                if not found and not self.is_external_library(import_name):
                    self.missing_dependencies.append(import_name)

    def is_external_library(self, module_name: str) -> bool:
        """Check if module is an external library"""
        external_libs = {
            'tkinter', 'customtkinter', 'PIL', 'numpy', 'matplotlib', 
            'sqlite3', 'json', 'os', 'sys', 'datetime', 'pathlib',
            'typing', 'functools', 'traceback', 'logging', 'subprocess'
        }
        
        root_module = module_name.split('.')[0]
        return root_module in external_libs

    def generate_backup_strategy(self) -> Dict[str, Any]:
        """Generate comprehensive backup strategy"""
        print("💾 Generating backup strategy...")
        
        # Calculate total sizes by category
        category_sizes = {}
        for category, files in self.critical_files.items():
            total_size = sum(self.file_sizes.get(f, 0) for f in files)
            category_sizes[category] = total_size
        
        # Identify most recent files
        recent_files = sorted(
            self.modification_dates.items(),
            key=lambda x: x[1],
            reverse=True
        )[:50]  # Top 50 most recent files
        
        backup_strategy = {
            'priority_levels': {
                'critical': self.critical_files['core_application'] + 
                          self.critical_files['ui_components'] + 
                          self.critical_files['database_files'],
                'important': self.critical_files['configuration'] + 
                           self.critical_files['assets'],
                'useful': self.critical_files['documentation'] + 
                         self.critical_files['utility_scripts'],
                'archival': self.critical_files['backup_files']
            },
            'category_sizes': category_sizes,
            'total_files': len(self.file_inventory),
            'total_size': sum(self.file_sizes.values()),
            'recent_files': recent_files[:20],  # Top 20 most recent
            'backup_recommendations': self.get_backup_recommendations()
        }
        
        return backup_strategy

    def get_backup_recommendations(self) -> List[str]:
        """Get specific backup recommendations"""
        recommendations = []
        
        # Check for critical files
        if len(self.critical_files['core_application']) > 0:
            recommendations.append("✅ Core application files identified - MUST backup")
        
        if len(self.syntax_errors) > 0:
            recommendations.append(f"⚠️ {len(self.syntax_errors)} files have syntax errors - backup before fixing")
        
        if len(self.missing_dependencies) > 0:
            recommendations.append(f"⚠️ {len(self.missing_dependencies)} missing dependencies found")
        
        # Check backup file age
        backup_count = len(self.critical_files['backup_files'])
        if backup_count > 100:
            recommendations.append(f"📦 {backup_count} backup files found - consider archiving old backups")
        
        total_size_mb = sum(self.file_sizes.values()) / (1024 * 1024)
        recommendations.append(f"💾 Total system size: {total_size_mb:.1f} MB")
        
        return recommendations

    def create_preservation_backup(self) -> str:
        """Create a complete preservation backup"""
        print("💾 Creating preservation backup...")

        backup_dir = self.root_path / f"COMPLETE_SYSTEM_BACKUP_{self.audit_timestamp}"
        backup_dir.mkdir(exist_ok=True)

        # Copy critical files with structure preservation
        for category, files in self.critical_files.items():
            if not files:
                continue

            category_dir = backup_dir / category
            category_dir.mkdir(exist_ok=True)

            for file_path in files:
                try:
                    source = self.root_path / file_path
                    if source.exists():
                        # Preserve directory structure
                        relative_path = Path(file_path)
                        dest_file = category_dir / relative_path.name

                        # Handle name conflicts
                        counter = 1
                        while dest_file.exists():
                            stem = relative_path.stem
                            suffix = relative_path.suffix
                            dest_file = category_dir / f"{stem}_{counter}{suffix}"
                            counter += 1

                        if source.is_file():
                            shutil.copy2(source, dest_file)

                except Exception as e:
                    print(f"Error backing up {file_path}: {e}")

        return str(backup_dir)

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate the complete audit report"""
        print("📊 Generating comprehensive report...")

        # Run all analysis steps
        self.inventory_all_files()
        self.analyze_python_dependencies()
        self.check_missing_dependencies()
        backup_strategy = self.generate_backup_strategy()

        # Create comprehensive report
        report = {
            'audit_metadata': {
                'timestamp': self.audit_timestamp,
                'root_path': str(self.root_path),
                'total_files': len(self.file_inventory),
                'total_python_files': len(self.python_files),
                'total_size_bytes': sum(self.file_sizes.values()),
                'total_size_mb': sum(self.file_sizes.values()) / (1024 * 1024)
            },

            'file_inventory': {
                'summary': {
                    'total_files': len([f for f in self.file_inventory.values() if f.get('is_file')]),
                    'total_directories': len([f for f in self.file_inventory.values() if f.get('is_directory')]),
                    'largest_files': self.get_largest_files(10),
                    'most_recent_files': self.get_most_recent_files(10)
                },
                'by_extension': self.get_files_by_extension(),
                'by_category': {cat: len(files) for cat, files in self.critical_files.items()}
            },

            'python_analysis': {
                'total_python_files': len(self.python_files),
                'syntax_errors': self.syntax_errors,
                'total_lines_of_code': sum(info.get('lines', 0) for info in self.python_files.values()),
                'most_imported_modules': self.get_most_imported_modules(),
                'files_with_most_imports': self.get_files_with_most_imports()
            },

            'dependency_analysis': {
                'missing_dependencies': self.missing_dependencies,
                'external_dependencies': self.get_external_dependencies(),
                'internal_dependencies': self.get_internal_dependencies(),
                'dependency_graph': self.build_dependency_graph()
            },

            'backup_analysis': {
                'backup_files_found': len(self.backup_files),
                'backup_file_details': self.backup_files,
                'backup_patterns': self.analyze_backup_patterns()
            },

            'critical_files_analysis': {
                'by_category': self.critical_files,
                'missing_critical_files': self.find_missing_critical_files(),
                'file_integrity': self.check_file_integrity()
            },

            'backup_strategy': backup_strategy,

            'recommendations': self.generate_recommendations()
        }

        return report

    def get_largest_files(self, count: int) -> List[Tuple[str, int]]:
        """Get the largest files"""
        return sorted(self.file_sizes.items(), key=lambda x: x[1], reverse=True)[:count]

    def get_most_recent_files(self, count: int) -> List[Tuple[str, str]]:
        """Get the most recently modified files"""
        return sorted(self.modification_dates.items(), key=lambda x: x[1], reverse=True)[:count]

    def get_files_by_extension(self) -> Dict[str, int]:
        """Group files by extension"""
        extensions = {}
        for file_info in self.file_inventory.values():
            if file_info.get('is_file'):
                ext = file_info.get('extension', 'no_extension')
                extensions[ext] = extensions.get(ext, 0) + 1
        return dict(sorted(extensions.items(), key=lambda x: x[1], reverse=True))

    def get_most_imported_modules(self) -> List[Tuple[str, int]]:
        """Get most frequently imported modules"""
        import_counts = {}
        for info in self.python_files.values():
            for imp in info.get('imports', []):
                import_counts[imp] = import_counts.get(imp, 0) + 1
        return sorted(import_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    def get_files_with_most_imports(self) -> List[Tuple[str, int]]:
        """Get files with the most imports"""
        file_imports = [(f, len(info.get('imports', []))) for f, info in self.python_files.items()]
        return sorted(file_imports, key=lambda x: x[1], reverse=True)[:10]

    def get_external_dependencies(self) -> List[str]:
        """Get list of external dependencies"""
        all_imports = set()
        for info in self.python_files.values():
            all_imports.update(info.get('imports', []))

        return [imp for imp in all_imports if self.is_external_library(imp)]

    def get_internal_dependencies(self) -> List[str]:
        """Get list of internal dependencies"""
        all_imports = set()
        for info in self.python_files.values():
            all_imports.update(info.get('imports', []))

        return [imp for imp in all_imports if not self.is_external_library(imp)]

    def build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build a dependency graph"""
        graph = {}
        for file_path, info in self.python_files.items():
            graph[file_path] = info.get('imports', [])
        return graph

    def analyze_backup_patterns(self) -> Dict[str, Any]:
        """Analyze backup file patterns"""
        patterns = {
            'by_date': {},
            'by_type': {},
            'by_source': {}
        }

        for backup_path, info in self.backup_files.items():
            # Extract date from filename
            import re
            date_match = re.search(r'(\d{8})', backup_path)
            if date_match:
                date = date_match.group(1)
                patterns['by_date'][date] = patterns['by_date'].get(date, 0) + 1

            # Extract backup type
            if '.backup' in backup_path:
                patterns['by_type']['backup'] = patterns['by_type'].get('backup', 0) + 1
            elif '.bak' in backup_path:
                patterns['by_type']['bak'] = patterns['by_type'].get('bak', 0) + 1

            # Extract source directory
            source_dir = Path(backup_path).parts[0] if Path(backup_path).parts else 'root'
            patterns['by_source'][source_dir] = patterns['by_source'].get(source_dir, 0) + 1

        return patterns

    def find_missing_critical_files(self) -> List[str]:
        """Find missing critical files"""
        expected_critical = [
            'main.py', 'ui/main_window.py', 'ui/login_window.py',
            'database/hybrid_database_manager.py', 'config/settings.py',
            'themes/modern_theme.py'
        ]

        missing = []
        for expected in expected_critical:
            if expected not in self.file_inventory:
                missing.append(expected)

        return missing

    def check_file_integrity(self) -> Dict[str, Any]:
        """Check file integrity"""
        integrity_report = {
            'files_with_hash': 0,
            'files_without_hash': 0,
            'unreadable_files': [],
            'empty_files': [],
            'large_files': []
        }

        for file_path, info in self.file_inventory.items():
            if info.get('is_file'):
                if info.get('hash'):
                    integrity_report['files_with_hash'] += 1
                else:
                    integrity_report['files_without_hash'] += 1

                if not info.get('readable'):
                    integrity_report['unreadable_files'].append(file_path)

                size = info.get('size', 0)
                if size == 0:
                    integrity_report['empty_files'].append(file_path)
                elif size > 10 * 1024 * 1024:  # > 10MB
                    integrity_report['large_files'].append((file_path, size))

        return integrity_report

    def generate_recommendations(self) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []

        # File system recommendations
        if len(self.syntax_errors) > 0:
            recommendations.append(f"🔧 URGENT: Fix {len(self.syntax_errors)} Python syntax errors before deployment")

        if len(self.missing_dependencies) > 0:
            recommendations.append(f"📦 CRITICAL: Resolve {len(self.missing_dependencies)} missing dependencies")

        # Backup recommendations
        backup_count = len(self.backup_files)
        if backup_count > 200:
            recommendations.append(f"🗂️ Consider archiving {backup_count} backup files to reduce clutter")
        elif backup_count < 10:
            recommendations.append("💾 Implement regular backup strategy - few backup files found")

        # Code quality recommendations
        total_loc = sum(info.get('lines', 0) for info in self.python_files.values())
        if total_loc > 50000:
            recommendations.append(f"📊 Large codebase ({total_loc:,} lines) - consider modularization")

        # Security recommendations
        config_files = len(self.critical_files['configuration'])
        if config_files > 0:
            recommendations.append(f"🔒 Review {config_files} configuration files for sensitive data")

        return recommendations

def main():
    """Main execution function"""
    print("🔍 COMPREHENSIVE SYSTEM AUDIT AND BACKUP TOOL")
    print("=" * 60)
    print("Arabic Accounting Software Complete Preservation System")
    print("=" * 60)

    try:
        # Initialize audit system
        auditor = ComprehensiveSystemAudit()

        # Generate comprehensive report
        report = auditor.generate_comprehensive_report()

        # Save report to file
        report_file = f"COMPLETE_SYSTEM_AUDIT_REPORT_{auditor.audit_timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        # Create preservation backup
        backup_location = auditor.create_preservation_backup()

        # Print summary
        print("\n" + "=" * 60)
        print("📊 AUDIT SUMMARY")
        print("=" * 60)

        metadata = report['audit_metadata']
        print(f"📁 Total Files: {metadata['total_files']:,}")
        print(f"🐍 Python Files: {metadata['total_python_files']:,}")
        print(f"💾 Total Size: {metadata['total_size_mb']:.1f} MB")

        print(f"\n🔍 Analysis Results:")
        print(f"   ✅ Syntax Errors: {len(report['python_analysis']['syntax_errors'])}")
        print(f"   ⚠️ Missing Dependencies: {len(report['dependency_analysis']['missing_dependencies'])}")
        print(f"   📦 Backup Files: {len(report['backup_analysis']['backup_files_found'])}")

        print(f"\n💾 Backup Created: {backup_location}")
        print(f"📄 Report Saved: {report_file}")

        print(f"\n🎯 Key Recommendations:")
        for rec in report['recommendations'][:5]:
            print(f"   {rec}")

        print("\n✅ AUDIT COMPLETED SUCCESSFULLY!")

    except Exception as e:
        print(f"❌ Error during audit: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
