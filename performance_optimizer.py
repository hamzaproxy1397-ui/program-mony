#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة تحسين الأداء وإزالة التكرار في البرنامج المحاسبي
"""

import re
import json
from datetime import datetime
from pathlib import Path

class PerformanceOptimizer:
    """محسن الأداء وإزالة التكرار"""

    def __init__(self):
        self.project_root = Path(".")
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "duplicate_code": [],
            "unused_imports": [],
            "unused_variables": [],
            "performance_issues": [],
            "recommendations": []
        }

        # الملفات المراد فحصها
        self.python_files = []
        self.scan_python_files()

    def scan_python_files(self):
        """فحص ملفات Python في المشروع"""
        print("🔍 فحص ملفات Python...")

        for file_path in self.project_root.rglob("*.py"):
            # تجاهل ملفات معينة
            if any(skip in str(file_path) for skip in ["__pycache__", ".git", "venv", "env"]):
                continue

            self.python_files.append(file_path)

        print(f"📊 تم العثور على {len(self.python_files)} ملف Python")

    def analyze_imports(self):
        """تحليل الاستيرادات"""
        print("\n📦 تحليل الاستيرادات...")

        import_usage = defaultdict(list)

        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # البحث عن الاستيرادات
                import_lines = re.findall(r'^(import\s+\w+|from\s+\w+\s+import\s+.+)$', content, re.MULTILINE)

                for import_line in import_lines:
                    # استخراج اسم الوحدة
                    if import_line.startswith('import '):
                        module = import_line.replace('import ', '').split()[0]
                    elif import_line.startswith('from '):
                        module = import_line.split()[1]
                    else:
                        continue

                    # فحص الاستخدام
                    if module not in content.replace(import_line, ''):
                        self.analysis_results["unused_imports"].append({
                            "file": str(file_path),
                            "import": import_line,
                            "module": module
                        })

            except Exception as e:
                print(f"❌ خطأ في تحليل {file_path}: {e}")

    def find_duplicate_code(self):
        """البحث عن الكود المكرر"""
        print("\n🔍 البحث عن الكود المكرر...")

        code_blocks = defaultdict(list)

        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # تحليل الدوال والكلاسات
                for i, line in enumerate(lines):
                    line = line.strip()

                    # البحث عن تعريفات الدوال
                    if line.startswith('def ') and len(line) > 20:
                        # أخذ عينة من الكود
                        code_sample = ''.join(lines[i:i+5]).strip()
                        if len(code_sample) > 50:
                            code_blocks[code_sample].append({
                                "file": str(file_path),
                                "line": i + 1,
                                "function": line
                            })

            except Exception as e:
                print(f"❌ خطأ في فحص {file_path}: {e}")

        # العثور على التكرارات
        for code, locations in code_blocks.items():
            if len(locations) > 1:
                self.analysis_results["duplicate_code"].append({
                    "code_sample": code[:100] + "...",
                    "occurrences": len(locations),
                    "locations": locations
                })

    def analyze_performance_issues(self):
        """تحليل مشاكل الأداء"""
        print("\n⚡ تحليل مشاكل الأداء...")

        performance_patterns = [
            (r'for\s+\w+\s+in\s+range\(len\(', "استخدم enumerate بدلاً من range(len())"),
            (r'\.append\(\)\s*\n\s*for', "استخدم list comprehension بدلاً من append في حلقة"),
            (r'open\([^)]+\)(?!\s*as|\s*with)', "استخدم with statement لفتح الملفات"),
            (r'time\.sleep\(\d+\)', "تجنب استخدام sleep طويل في الواجهة الرئيسية"),
        ]

        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                for pattern, suggestion in performance_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        self.analysis_results["performance_issues"].append({
                            "file": str(file_path),
                            "line": line_num,
                            "issue": match.group(),
                            "suggestion": suggestion
                        })

            except Exception as e:
                print(f"❌ خطأ في تحليل الأداء {file_path}: {e}")

    def generate_recommendations(self):
        """إنشاء التوصيات"""
        recommendations = []

        # توصيات بناءً على الاستيرادات غير المستخدمة
        if self.analysis_results["unused_imports"]:
            recommendations.append(f"حذف {len(self.analysis_results['unused_imports'])} استيراد غير مستخدم")

        # توصيات بناءً على الكود المكرر
        if self.analysis_results["duplicate_code"]:
            recommendations.append(f"إعادة هيكلة {len(self.analysis_results['duplicate_code'])} قطعة كود مكررة")

        # توصيات بناءً على مشاكل الأداء
        if self.analysis_results["performance_issues"]:
            recommendations.append(f"إصلاح {len(self.analysis_results['performance_issues'])} مشكلة أداء")

        # توصيات عامة
        recommendations.extend([
            "استخدام lazy loading للوحدات الكبيرة",
            "تحسين استعلامات قاعدة البيانات",
            "استخدام connection pooling",
            "تحسين تحميل الصور والأيقونات",
            "إضافة caching للعمليات المتكررة"
        ])

        self.analysis_results["recommendations"] = recommendations

    def clean_unused_imports(self):
        """تنظيف الاستيرادات غير المستخدمة"""
        print("\n🧹 تنظيف الاستيرادات غير المستخدمة...")

        cleaned_count = 0

        for unused in self.analysis_results["unused_imports"]:
            file_path = Path(unused["file"])
            import_line = unused["import"]

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # حذف السطر
                lines = content.split('\n')
                new_lines = []

                for line in lines:
                    if line.strip() != import_line.strip():
                        new_lines.append(line)
                    else:
                        print(f"   ✅ حذف: {import_line} من {file_path.name}")
                        cleaned_count += 1

                # كتابة الملف المحدث
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))

            except Exception as e:
                print(f"❌ خطأ في تنظيف {file_path}: {e}")

        print(f"✅ تم تنظيف {cleaned_count} استيراد غير مستخدم")

    def save_report(self):
        """حفظ تقرير التحليل"""
        report_file = f"performance_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
            print(f"\n📋 تم حفظ تقرير التحليل: {report_file}")
        except Exception as e:
            print(f"❌ خطأ في حفظ التقرير: {e}")

    def run_optimization(self):
        """تشغيل التحسين الكامل"""
        print("⚡ بدء تحسين الأداء وإزالة التكرار")
        print("=" * 50)

        # تحليل المشروع
        self.analyze_imports()
        self.find_duplicate_code()
        self.analyze_performance_issues()
        self.generate_recommendations()

        # عرض النتائج
        print(f"\n📊 ملخص التحليل:")
        print(f"   📦 استيرادات غير مستخدمة: {len(self.analysis_results['unused_imports'])}")
        print(f"   🔄 كود مكرر: {len(self.analysis_results['duplicate_code'])}")
        print(f"   ⚡ مشاكل أداء: {len(self.analysis_results['performance_issues'])}")
        print(f"   💡 توصيات: {len(self.analysis_results['recommendations'])}")

        # سؤال المستخدم عن التنظيف
        if self.analysis_results["unused_imports"]:
            clean = input(f"\n❓ هل تريد حذف {len(self.analysis_results['unused_imports'])} استيراد غير مستخدم؟ (y/n): ").lower().strip()
            if clean in ['y', 'yes', 'نعم']:
                self.clean_unused_imports()

        # حفظ التقرير
        self.save_report()

        # عرض التوصيات
        print(f"\n💡 التوصيات:")
        for rec in self.analysis_results["recommendations"]:
            print(f"   - {rec}")

        print(f"\n🎉 تم الانتهاء من تحسين الأداء!")

def main():
    """الدالة الرئيسية"""
    optimizer = PerformanceOptimizer()
    optimizer.run_optimization()

if __name__ == "__main__":
    main()
