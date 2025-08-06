import pandas as pd
import pandera as pa
import sqlite3
import re
import ast

# الاتصال بقاعدة بيانات SQLite
conn = sqlite3.connect('database.db')

# قراءة بيانات من جدول معين
df = pd.read_sql_query('SELECT * FROM your_table', conn)

# فحص القيم المفقودة في كل عمود
print("=== فحص القيم المفقودة ===")
for col in df.columns:
    miss = df[col].isnull().sum()
    if miss > 0:
        print(f"{col} يحتوي على {miss} قيمة مفقودة")
    else:
        print(f"{col} لا يحتوي على قيم مفقودة")

# إنشاء مخطط التحقق من صحة البيانات باستخدام pandera
print("\n=== التحقق من صحة البيانات ===")
schema = pa.DataFrameSchema({
    'id': pa.Column(pa.Int, checks=pa.Check.greater_than(0)),  # تأكد أن id رقم موجب
    'name': pa.Column(pa.String, nullable=False),              # الاسم غير فارغ
    'age': pa.Column(pa.Int, checks=pa.Check.in_range(18, 99)) # العمر بين 18 و99
})

try:
    validated_df = schema.validate(df)
    print("✅ كل البيانات متوافقة مع الشروط.")
except pa.errors.SchemaError as e:
    print("❌ هناك أخطاء في البيانات:", e)

# دالة تصحيح الكود البرمجي
def correct_code(code):
    """
    دالة تصحح الكود البرمجي بإزالة التعليقات الزائدة وتصحيح الإزاحة
    """
    lines = code.split("\n")
    corrected_lines = []

    for line in lines:
        stripped = line.strip()
        # تجاهل الأسطر الفارغة والتعليقات التي تبدأ بـ #
        if stripped.startswith("#") or not stripped:
            continue
        corrected_lines.append(stripped)

    return "\n".join(corrected_lines)

# دالة متقدمة لتصحيح وتنسيق الكود
def advanced_code_correction(code):
    """
    دالة متقدمة لتصحيح وتنسيق الكود البرمجي
    """
    try:
        # محاولة تحليل الكود للتأكد من صحته النحوية
        ast.parse(code)

        lines = code.split("\n")
        corrected_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()

            # تجاهل الأسطر الفارغة والتعليقات
            if not stripped or stripped.startswith("#"):
                continue

            # تقليل مستوى الإزاحة للكلمات المفتاحية التي تنهي الكتل
            if any(stripped.startswith(keyword) for keyword in ['except', 'elif', 'else', 'finally']):
                indent_level = max(0, indent_level - 1)

            # إضافة الإزاحة المناسبة
            corrected_line = "    " * indent_level + stripped
            corrected_lines.append(corrected_line)

            # زيادة مستوى الإزاحة للكلمات المفتاحية التي تبدأ كتل جديدة
            if stripped.endswith(":"):
                indent_level += 1

        return "\n".join(corrected_lines)

    except SyntaxError as e:
        return f"خطأ في بناء الجملة: {e}"

# مثال على استخدام دالة تصحيح الكود
print("\n=== مثال على تصحيح الكود ===")
example_code = '''
# كود للتجربة
def hello():
    # اطبع مرحباً
    print("مرحباً بالعالم!")
    if True:
        print("هذا صحيح")
# نهاية المثال
'''

print("الكود الأصلي:")
print(example_code)
print("\nالكود بعد التصحيح البسيط:")
print(correct_code(example_code))
print("\nالكود بعد التصحيح المتقدم:")
print(advanced_code_correction(example_code))

# إغلاق الاتصال بقاعدة البيانات
conn.close()
print("\n✅ تم إغلاق الاتصال بقاعدة البيانات بنجاح")