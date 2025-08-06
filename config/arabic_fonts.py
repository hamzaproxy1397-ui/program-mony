# -*- coding: utf-8 -*-
from pathlib import Path
"""
إعدادات الخطوط العربية
"""


# مسار مجلد الخطوط
FONTS_DIR = Path("assets/fonts")

# الخطوط العربية المتاحة
ARABIC_FONTS = {
    "cairo": {
        "name": "Cairo",
        "files": [
            "Cairo-Regular.ttf",
            "Cairo-Bold.ttf", 
            "Cairo-Light.ttf",
            "Cairo-Medium.ttf",
            "Cairo-SemiBold.ttf"
        ],
        "description": "خط Cairo الحديث والأنيق"
    },

    "amiri": {
        "name": "Amiri", 
        "files": [
            "Amiri-Regular.ttf",
            "Amiri-Bold.ttf",
            "Amiri-Italic.ttf",
            "Amiri-BoldItalic.ttf"
        ],
        "description": "خط Amiri التقليدي والجميل"
    },

    "noto_naskh": {
        "name": "Noto Naskh Arabic",
        "files": [
            "NotoNaskhArabic-Regular.ttf",
            "NotoNaskhArabic-Bold.ttf",
            "NotoNaskhArabic-Medium.ttf",
            "NotoNaskhArabic-SemiBold.ttf"
        ],
        "description": "خط Noto Naskh Arabic الواضح"
    }
}

# الخط الافتراضي
DEFAULT_FONT = "cairo"

# أحجام الخطوط
FONT_SIZES = {
    "small": 10,
    "normal": 12,
    "medium": 14,
    "large": 16,
    "xlarge": 18,
    "title": 20,
    "header": 24
}

def get_font_path(font_family, style="Regular"):
    """الحصول على مسار ملف الخط"""
    if font_family not in ARABIC_FONTS:
        font_family = DEFAULT_FONT

    font_info = ARABIC_FONTS[font_family]

    # البحث عن الملف المناسب
    for font_file in font_info["files"]:
        if style.lower() in font_file.lower():
            font_path = FONTS_DIR / font_file
            if font_path.exists():
                return str(font_path)

    # إرجاع أول ملف متاح
    for font_file in font_info["files"]:
        font_path = FONTS_DIR / font_file
        if font_path.exists():
            return str(font_path)

    return None

def get_available_fonts():
    """الحصول على قائمة الخطوط المتاحة"""
    available = []

    for font_key, font_info in ARABIC_FONTS.items():
        for font_file in font_info["files"]:
            font_path = FONTS_DIR / font_file
            if font_path.exists():
                available.append({
                    "key": font_key,
                    "name": font_info["name"],
                    "file": font_file,
                    "path": str(font_path),
                    "description": font_info["description"]
                })
                break

    return available

def is_font_available(font_family):
    """التحقق من توفر خط معين"""
    return get_font_path(font_family) is not None
