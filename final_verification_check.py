#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 فحص التحقق النهائي من سلامة المشروع
Final Verification Check

يتحقق هذا الملف من سلامة المشروع بعد التحسينات والإصلاحات
"""

import os
import sys
import ast
import json
from pathlib import Path
from datetime import datetime

class FinalVerificationCheck:
    """فئة فحص التحقق النهائي"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.verification_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "UNKNOWN",
            "essential_files_check": {},
            "syntax_check": {},
            "import_check": {},
            "performance_metrics": {},
            "recommendations": []
        }
        
        # الملفات الأساسية المطلوبة
        self.essential_files = [
            "main.py",
            "ui/views/main_window.py",
            "ui/views/login_window.py",
            "database/hybrid_database_manager.py",
            "themes/modern_theme.py",
            "config/settings.py"
        ]

    def run_verification(self):
        """تشغيل فحص التحقق النهائي"""
        print("🔍 بدء فحص التحقق النهائي من سلامة المشروع...")
        print("=" * 60)
        
        # 1. فحص الملفات الأساسية
        essential_status = self._check_essential_files()
        
        # 2. فحص الأخطاء النحوية
        syntax_status = self._check_syntax_errors()
        
        # 3. فحص الاستيرادات الأساسية
        import_status = self._check_critical_imports()
        
        # 4. فحص مقاييس الأداء
        performance_status = self._check_performance_metrics()
        
        # 5. تحديد الحالة العامة
        self._determine_overall_status(essential_status, syntax_status, import_status, performance_status)
        
        # 6. إنشاء التوصيات
        self._generate_final_recommendations()
        
        # 7. حفظ التقرير
        self._save_verification_report()
        
        # 8. عرض النتائج
        self._display_results()

    def _check_essential_files(self):
        """فحص الملفات الأساسية"""
        print("\n📁 فحص الملفات الأساسية...")
        
        missing_files = []
        existing_files = []
        
        for file_path in self.essential_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                existing_files.append(file_path)
                print(f"✅ {file_path}")
            else:
                missing_files.append(file_path)
                print(f"❌ {file_path} - مفقود")
        
        self.verification_report["essential_files_check"] = {
            "total_files": len(self.essential_files),
            "existing_files": len(existing_files),
            "missing_files": len(missing_files),
            "missing_list": missing_files,
            "status": "PASS" if len(missing_files) == 0 else "FAIL"
        }
        
        return len(missing_files) == 0

    def _check_syntax_errors(self):
        """فحص الأخطاء النحوية في الملفات الأساسية"""
        print("\n🐍 فحص الأخطاء النحوية...")
        
        syntax_errors = []
        files_checked = 0
        
        for file_path in self.essential_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                files_checked += 1
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    ast.parse(content)
                    print(f"✅ {file_path}")
                except SyntaxError as e:
                    syntax_errors.append({
                        "file": file_path,
                        "line": e.lineno,
                        "error": str(e)
                    })
                    print(f"❌ {file_path} - خطأ نحوي: {e}")
                except Exception as e:
                    print(f"⚠️ {file_path} - خطأ في القراءة: {e}")
        
        self.verification_report["syntax_check"] = {
            "files_checked": files_checked,
            "syntax_errors": len(syntax_errors),
            "error_details": syntax_errors,
            "status": "PASS" if len(syntax_errors) == 0 else "FAIL"
        }
        
        return len(syntax_errors) == 0

    def _check_critical_imports(self):
        """فحص الاستيرادات الحرجة"""
        print("\n📦 فحص الاستيرادات الحرجة...")
        
        critical_imports = [
            "customtkinter",
            "PIL",
            "sqlite3",
            "json",
            "os",
            "sys"
        ]
        
        import_status = {}
        failed_imports = []
        
        for module in critical_imports:
            try:
                if module == "PIL":
                    from PIL import Image
                else:
                    __import__(module)
                import_status[module] = "SUCCESS"
                print(f"✅ {module}")
            except ImportError:
                import_status[module] = "FAILED"
                failed_imports.append(module)
                print(f"❌ {module} - غير متوفر")
        
        self.verification_report["import_check"] = {
            "total_imports": len(critical_imports),
            "successful_imports": len(critical_imports) - len(failed_imports),
            "failed_imports": len(failed_imports),
            "failed_list": failed_imports,
            "import_details": import_status,
            "status": "PASS" if len(failed_imports) == 0 else "FAIL"
        }
        
        return len(failed_imports) == 0

    def _check_performance_metrics(self):
        """فحص مقاييس الأداء"""
        print("\n📊 فحص مقاييس الأداء...")
        
        # حساب حجم المشروع
        total_size = 0
        file_count = 0
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                    file_count += 1
                except:
                    pass
        
        # تحويل إلى MB
        total_size_mb = total_size / (1024 * 1024)
        
        # فحص وجود تقارير التحسين
        audit_reports = list(self.project_root.glob("*audit_report*.json"))
        cleanup_reports = list(self.project_root.glob("*cleanup_report*.json"))
        
        self.verification_report["performance_metrics"] = {
            "project_size_mb": round(total_size_mb, 2),
            "total_files": file_count,
            "audit_reports_found": len(audit_reports),
            "cleanup_reports_found": len(cleanup_reports),
            "optimization_applied": len(audit_reports) > 0 and len(cleanup_reports) > 0
        }
        
        print(f"📁 حجم المشروع: {total_size_mb:.2f} MB")
        print(f"📄 عدد الملفات: {file_count}")
        print(f"📊 تقارير الفحص: {len(audit_reports)}")
        print(f"🧹 تقارير التنظيف: {len(cleanup_reports)}")
        
        return True

    def _determine_overall_status(self, essential_status, syntax_status, import_status, performance_status):
        """تحديد الحالة العامة للمشروع"""
        if essential_status and syntax_status and import_status:
            self.verification_report["overall_status"] = "EXCELLENT"
        elif essential_status and syntax_status:
            self.verification_report["overall_status"] = "GOOD"
        elif essential_status:
            self.verification_report["overall_status"] = "FAIR"
        else:
            self.verification_report["overall_status"] = "POOR"

    def _generate_final_recommendations(self):
        """إنشاء التوصيات النهائية"""
        recommendations = []
        
        # توصيات بناءً على الفحوصات
        if self.verification_report["essential_files_check"]["status"] == "FAIL":
            recommendations.append("إنشاء الملفات الأساسية المفقودة")
        
        if self.verification_report["syntax_check"]["status"] == "FAIL":
            recommendations.append("إصلاح الأخطاء النحوية المتبقية")
        
        if self.verification_report["import_check"]["status"] == "FAIL":
            recommendations.append("تثبيت المكتبات المفقودة")
        
        # توصيات عامة
        recommendations.extend([
            "إجراء نسخة احتياطية دورية",
            "مراقبة الأداء بانتظام",
            "تحديث التوثيق عند الحاجة",
            "إجراء اختبارات دورية للوظائف"
        ])
        
        self.verification_report["recommendations"] = recommendations

    def _save_verification_report(self):
        """حفظ تقرير التحقق"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"final_verification_report_{timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.verification_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ تقرير التحقق في: {report_path}")

    def _display_results(self):
        """عرض النتائج النهائية"""
        print("\n" + "=" * 60)
        print("📊 نتائج فحص التحقق النهائي")
        print("=" * 60)
        
        status = self.verification_report["overall_status"]
        status_icons = {
            "EXCELLENT": "🟢 ممتاز",
            "GOOD": "🟡 جيد", 
            "FAIR": "🟠 مقبول",
            "POOR": "🔴 ضعيف"
        }
        
        print(f"\n🎯 الحالة العامة: {status_icons.get(status, status)}")
        
        # عرض تفاصيل الفحوصات
        checks = [
            ("الملفات الأساسية", self.verification_report["essential_files_check"]["status"]),
            ("الأخطاء النحوية", self.verification_report["syntax_check"]["status"]),
            ("الاستيرادات", self.verification_report["import_check"]["status"])
        ]
        
        print("\n📋 تفاصيل الفحوصات:")
        for check_name, check_status in checks:
            icon = "✅" if check_status == "PASS" else "❌"
            print(f"   {icon} {check_name}: {check_status}")
        
        # عرض مقاييس الأداء
        metrics = self.verification_report["performance_metrics"]
        print(f"\n📊 مقاييس الأداء:")
        print(f"   📁 حجم المشروع: {metrics['project_size_mb']} MB")
        print(f"   📄 عدد الملفات: {metrics['total_files']}")
        
        # عرض التوصيات
        if self.verification_report["recommendations"]:
            print(f"\n💡 التوصيات:")
            for i, rec in enumerate(self.verification_report["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        print("\n🎉 تم الانتهاء من فحص التحقق النهائي!")

def main():
    """الدالة الرئيسية"""
    print("🔍 فحص التحقق النهائي من سلامة المشروع")
    print("=" * 50)
    
    verifier = FinalVerificationCheck()
    verifier.run_verification()

if __name__ == "__main__":
    main()
