# -*- coding: utf-8 -*-
"""
مدير التبعيات المتقدم لنظام إدخال الأصناف
Advanced Dependency Manager for Item Entry System
"""

import sys
import subprocess
import importlib
import pkg_resources
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class AdvancedDependencyManager:
    """مدير التبعيات المتقدم"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.requirements_file = self.project_root / "requirements.txt"
        
        # المكتبات الأساسية المطلوبة لنظام إدخال الأصناف
        self.core_dependencies = {
            'tkinter': {'required': True, 'fallback': None},
            'customtkinter': {'required': True, 'fallback': 'tkinter'},
            'PIL': {'required': True, 'fallback': None},
            'matplotlib': {'required': True, 'fallback': None},
            'numpy': {'required': True, 'fallback': None},
            'pandas': {'required': True, 'fallback': None},
        }
        
        # المكتبات الاختيارية المتقدمة
        self.optional_dependencies = {
            'openpyxl': {'feature': 'Excel Export/Import'},
            'reportlab': {'feature': 'PDF Generation'},
            'qrcode': {'feature': 'QR Code Generation'},
            'python-barcode': {'feature': 'Barcode Generation'},
            'scikit-learn': {'feature': 'AI Predictions'},
            'scipy': {'feature': 'Advanced Analytics'},
            'opencv-python': {'feature': 'Image Processing'},
            'pyzbar': {'feature': 'Barcode Scanning'},
            'xlsxwriter': {'feature': 'Advanced Excel Features'},
            'lxml': {'feature': 'XML Processing'},
            'requests': {'feature': 'Cloud Integration'},
        }
        
        self.dependency_status = {}
        self.missing_dependencies = []
        self.available_features = []
        
    def check_dependency(self, package_name: str) -> Tuple[bool, Optional[str]]:
        """فحص توفر مكتبة معينة"""
        try:
            if package_name == 'tkinter':
                import tkinter
                return True, tkinter.TkVersion
            elif package_name == 'PIL':
                from PIL import Image
                return True, Image.__version__ if hasattr(Image, '__version__') else 'Unknown'
            else:
                module = importlib.import_module(package_name)
                version = getattr(module, '__version__', 'Unknown')
                return True, version
        except ImportError:
            return False, None
        except Exception as e:
            return False, str(e)
    
    def check_all_dependencies(self) -> Dict[str, Dict]:
        """فحص جميع التبعيات"""
        print("🔍 فحص التبعيات المطلوبة...")
        
        # فحص التبعيات الأساسية
        for package, config in self.core_dependencies.items():
            is_available, version = self.check_dependency(package)
            self.dependency_status[package] = {
                'available': is_available,
                'version': version,
                'required': config['required'],
                'fallback': config['fallback'],
                'type': 'core'
            }
            
            if is_available:
                print(f"✅ {package} - {version}")
            else:
                print(f"❌ {package} - غير متوفر")
                if config['required']:
                    self.missing_dependencies.append(package)
        
        # فحص التبعيات الاختيارية
        for package, config in self.optional_dependencies.items():
            is_available, version = self.check_dependency(package)
            self.dependency_status[package] = {
                'available': is_available,
                'version': version,
                'required': False,
                'feature': config['feature'],
                'type': 'optional'
            }
            
            if is_available:
                print(f"✅ {package} - {version} ({config['feature']})")
                self.available_features.append(config['feature'])
            else:
                print(f"⚠️ {package} - غير متوفر ({config['feature']})")
        
        return self.dependency_status
    
    def install_missing_dependencies(self) -> bool:
        """تثبيت التبعيات المفقودة"""
        if not self.missing_dependencies:
            print("✅ جميع التبعيات الأساسية متوفرة")
            return True
        
        print(f"📦 تثبيت التبعيات المفقودة: {', '.join(self.missing_dependencies)}")
        
        try:
            # قراءة requirements.txt
            if self.requirements_file.exists():
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '-r', 
                    str(self.requirements_file), '--upgrade'
                ])
            else:
                # تثبيت التبعيات الأساسية فقط
                basic_packages = ['customtkinter', 'Pillow', 'matplotlib', 'numpy', 'pandas']
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install'
                ] + basic_packages)
            
            print("✅ تم تثبيت التبعيات بنجاح")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ فشل في تثبيت التبعيات: {e}")
            return False
        except Exception as e:
            print(f"❌ خطأ في تثبيت التبعيات: {e}")
            return False
    
    def get_feature_availability(self) -> Dict[str, bool]:
        """الحصول على حالة توفر المميزات"""
        features = {
            'basic_ui': 'tkinter' in [pkg for pkg, status in self.dependency_status.items() 
                                    if status.get('available', False)],
            'modern_ui': 'customtkinter' in [pkg for pkg, status in self.dependency_status.items() 
                                           if status.get('available', False)],
            'image_processing': 'PIL' in [pkg for pkg, status in self.dependency_status.items() 
                                        if status.get('available', False)],
            'charts_analytics': 'matplotlib' in [pkg for pkg, status in self.dependency_status.items() 
                                                if status.get('available', False)],
            'data_processing': 'pandas' in [pkg for pkg, status in self.dependency_status.items() 
                                          if status.get('available', False)],
            'excel_export': 'openpyxl' in [pkg for pkg, status in self.dependency_status.items() 
                                         if status.get('available', False)],
            'pdf_export': 'reportlab' in [pkg for pkg, status in self.dependency_status.items() 
                                        if status.get('available', False)],
            'barcode_generation': 'python-barcode' in [pkg for pkg, status in self.dependency_status.items() 
                                                     if status.get('available', False)],
            'qr_generation': 'qrcode' in [pkg for pkg, status in self.dependency_status.items() 
                                        if status.get('available', False)],
            'ai_features': 'scikit-learn' in [pkg for pkg, status in self.dependency_status.items() 
                                            if status.get('available', False)],
        }
        return features
    
    def generate_dependency_report(self) -> str:
        """إنشاء تقرير شامل عن التبعيات"""
        report = []
        report.append("=" * 60)
        report.append("📋 تقرير التبعيات - نظام إدخال الأصناف المتقدم")
        report.append("=" * 60)
        
        # التبعيات الأساسية
        report.append("\n🔥 التبعيات الأساسية:")
        for package, status in self.dependency_status.items():
            if status['type'] == 'core':
                icon = "✅" if status['available'] else "❌"
                version = f" - {status['version']}" if status['version'] else ""
                report.append(f"  {icon} {package}{version}")
        
        # التبعيات الاختيارية
        report.append("\n⭐ التبعيات الاختيارية:")
        for package, status in self.dependency_status.items():
            if status['type'] == 'optional':
                icon = "✅" if status['available'] else "⚠️"
                version = f" - {status['version']}" if status['version'] else ""
                feature = f" ({status['feature']})" if 'feature' in status else ""
                report.append(f"  {icon} {package}{version}{feature}")
        
        # المميزات المتاحة
        features = self.get_feature_availability()
        report.append("\n🎯 المميزات المتاحة:")
        for feature, available in features.items():
            icon = "✅" if available else "❌"
            report.append(f"  {icon} {feature}")
        
        # التوصيات
        report.append("\n💡 التوصيات:")
        if self.missing_dependencies:
            report.append("  🔧 قم بتثبيت التبعيات المفقودة:")
            report.append(f"     pip install {' '.join(self.missing_dependencies)}")
        else:
            report.append("  🎉 جميع التبعيات الأساسية متوفرة!")
        
        missing_optional = [pkg for pkg, status in self.dependency_status.items() 
                          if status['type'] == 'optional' and not status['available']]
        if missing_optional:
            report.append("  📦 لتفعيل المميزات الإضافية:")
            report.append(f"     pip install {' '.join(missing_optional)}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)
    
    def save_dependency_report(self, filename: str = "dependency_report.txt"):
        """حفظ تقرير التبعيات في ملف"""
        report = self.generate_dependency_report()
        report_file = self.project_root / filename
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 تم حفظ تقرير التبعيات في: {report_file}")
            return True
        except Exception as e:
            print(f"❌ فشل في حفظ التقرير: {e}")
            return False

def main():
    """تشغيل فحص التبعيات"""
    manager = AdvancedDependencyManager()
    
    # فحص التبعيات
    manager.check_all_dependencies()
    
    # طباعة التقرير
    print(manager.generate_dependency_report())
    
    # حفظ التقرير
    manager.save_dependency_report()
    
    # تثبيت التبعيات المفقودة إذا لزم الأمر
    if manager.missing_dependencies:
        install = input("\n❓ هل تريد تثبيت التبعيات المفقودة؟ (y/n): ")
        if install.lower() in ['y', 'yes', 'نعم']:
            manager.install_missing_dependencies()

if __name__ == "__main__":
    main()
