# دليل نظام الجدولة التلقائية - APScheduler

## 📋 نظرة عامة

تم تثبيت وتكوين مكتبة **APScheduler** في برنامج المحاسبة لتوفير نظام جدولة تلقائية متقدم يقوم بتنفيذ المهام التالية:

### 🔄 المهام المجدولة تلقائياً:

1. **النسخ الاحتياطي اليومي** 📅
   - الوقت: يومياً الساعة 11:00 مساءً
   - الوظيفة: إنشاء نسخة احتياطية من قاعدة البيانات
   - المكان: مجلد `backups/`

2. **تنظيف النسخ الاحتياطية القديمة** 🗑️
   - الوقت: كل أحد الساعة 1:00 صباحاً
   - الوظيفة: حذف النسخ الاحتياطية الزائدة (الاحتفاظ بآخر 30 نسخة)

3. **تنظيف ملفات السجلات القديمة** 📝
   - الوقت: أول كل شهر الساعة 2:00 صباحاً
   - الوظيفة: حذف ملفات السجلات الأقدم من 90 يوم

## 🚀 طرق التشغيل

### الطريقة الأولى: التشغيل العادي
```bash
python main.py
```
- يشغل البرنامج مع نظام الجدولة تلقائياً

### الطريقة الثانية: التشغيل المحسن
```bash
python start_with_scheduler.py
```
- يعرض معلومات مفصلة عن نظام الجدولة
- يظهر المهام المجدولة وأوقات تنفيذها

### الطريقة الثالثة: اختبار النظام
```bash
python test_scheduler.py
```
- لاختبار عمل نظام الجدولة
- خيارات: اختبار كامل أو اختبار النسخ الاحتياطي فقط

## ⚙️ ملفات التكوين

### 1. إعدادات الجدولة (`config/scheduler_settings.py`)
```python
# إعدادات النسخ الاحتياطي
BACKUP_SETTINGS = {
    'daily_backup_time': {
        'hour': 23,  # 11:00 PM
        'minute': 0
    },
    'max_backups_to_keep': 30,
    'auto_backup_enabled': True
}
```

### 2. إعدادات التنظيف
```python
CLEANUP_SETTINGS = {
    'backup_cleanup': {
        'enabled': True,
        'day_of_week': 0,  # الأحد
        'hour': 1,
        'minute': 0,
        'keep_count': 30
    }
}
```

## 📁 هيكل الملفات الجديدة

```
accounting-software/
├── core/
│   └── scheduler_manager.py      # مدير المهام المجدولة
├── config/
│   └── scheduler_settings.py     # إعدادات الجدولة
├── start_with_scheduler.py       # تشغيل محسن مع الجدولة
├── test_scheduler.py             # اختبار النظام
├── SCHEDULER_GUIDE.md            # هذا الدليل
└── requirements.txt              # محدث بـ APScheduler
```

## 🔧 الميزات المتقدمة

### 1. إضافة مهام مخصصة
```python
from core.scheduler_manager import SchedulerManager
from apscheduler.triggers.cron import CronTrigger

scheduler = SchedulerManager()
scheduler.add_custom_job(
    func=my_custom_function,
    trigger=CronTrigger(hour=9, minute=0),
    job_id='custom_task',
    name='مهمة مخصصة'
)
```

### 2. عرض المهام المجدولة
```python
jobs = scheduler.get_scheduled_jobs()
for job in jobs:
    print(f"المهمة: {job['name']}")
    print(f"التشغيل التالي: {job['next_run']}")
```

### 3. حذف مهمة
```python
scheduler.remove_job('job_id')
```

## 📊 مراقبة النظام

### 1. ملفات السجلات
- `logs/app.log` - سجل التطبيق الرئيسي
- `logs/scheduler.log` - سجل نظام الجدولة (إذا تم تفعيله)

### 2. مجلد النسخ الاحتياطية
- `backups/` - يحتوي على جميع النسخ الاحتياطية
- تسمية الملفات: `scheduled_backup_YYYYMMDD_HHMMSS.db`

## 🛡️ الأمان والاستقرار

### 1. العمل في الخلفية
- النظام يعمل في الخلفية حتى لو تم إغلاق النافذة الرئيسية
- يتوقف فقط عند إنهاء العملية بالكامل

### 2. معالجة الأخطاء
- تسجيل جميع الأخطاء في ملفات السجلات
- إعادة المحاولة التلقائية عند فشل المهام
- إيقاف آمن عند إنهاء البرنامج

### 3. إدارة الموارد
- تنظيف تلقائي للملفات القديمة
- حد أقصى لعدد النسخ الاحتياطية المحفوظة
- تحسين استخدام مساحة القرص

## 🔄 التخصيص

### تغيير وقت النسخ الاحتياطي
في ملف `config/scheduler_settings.py`:
```python
BACKUP_SETTINGS = {
    'daily_backup_time': {
        'hour': 22,  # 10:00 PM بدلاً من 11:00 PM
        'minute': 30  # 10:30 PM
    }
}
```

### تعطيل النسخ الاحتياطي التلقائي
```python
BACKUP_SETTINGS = {
    'auto_backup_enabled': False
}
```

### تغيير المنطقة الزمنية
```python
SCHEDULER_SETTINGS = {
    'timezone': 'Asia/Dubai'  # أو أي منطقة زمنية أخرى
}
```

## 🆘 استكشاف الأخطاء

### 1. المجدول لا يعمل
- تحقق من ملف `logs/app.log`
- تأكد من تثبيت مكتبة APScheduler: `pip install APScheduler`

### 2. النسخ الاحتياطي لا يتم إنشاؤه
- تحقق من صلاحيات الكتابة في مجلد `backups/`
- تأكد من وجود مساحة كافية على القرص

### 3. المهام لا تنفذ في الوقت المحدد
- تحقق من إعدادات المنطقة الزمنية
- تأكد من أن النظام يعمل في الوقت المحدد

## 📞 الدعم

للحصول على المساعدة:
1. راجع ملفات السجلات في مجلد `logs/`
2. استخدم `python test_scheduler.py` لاختبار النظام
3. تحقق من إعدادات `config/scheduler_settings.py`

---

**ملاحظة**: النظام مصمم ليعمل بشكل مستقل ولا يحتاج تدخل يدوي. جميع المهام تتم تلقائياً في الخلفية.
