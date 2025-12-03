# راهنمای استفاده

## برای اولین بار

### 1. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 2. اجرای برنامه اصلی

```bash
python run.py
```

## استفاده‌های متفاوت

### دریافت خودکار (هر 30 دقیقه)

```bash
python scheduler.py
```

خروجی:

```
[2025-12-03 21:44:12] INFO: AQI Scheduler شروع شد
[2025-12-03 21:44:12] INFO: فاصله: 30 دقیقه
[2025-12-03 21:44:15] INFO: شروع دریافت AQI در 2025-12-03T21:44:15.123456+03:30
[2025-12-03 21:44:45] INFO: ✓ موفق: 31 استان دریافت شد
```

### API سرور

```bash
python api.py
```

سپس در مرورگر:

```
http://localhost:5000/api/aqi
http://localhost:5000/api/aqi/تهران
http://localhost:5000/api/aqi/stats
```

### دریافت دستی

```bash
python scraper.py
```

### مشاهده لاگ‌ها

```bash
python log_viewer.py              # 50 لاگ آخر
python log_viewer.py tail 100     # 100 لاگ آخر
python log_viewer.py stats        # آمار
python log_viewer.py watch        # نظارت Real-time
```

## ساختار داده‌ها

### فایل JSON اطلاعات

`data/aqi_data.json`

```json
{
  "تهران": {
    "aqi": 125,
    "timestamp": "2025-12-03T21:44:12.123456+03:30"
  },
  "کردستان": {
    "aqi": 53,
    "timestamp": "2025-12-03T21:44:18.654321+03:30"
  },
  ...
}
```

### فایل لاگ‌ها

`logs/scraper.log`

```
[2025-12-03 21:44:12] INFO: شروع دریافت AQI در 2025-12-03T21:44:12.123456+03:30
[2025-12-03 21:44:15] INFO: ✓ تهران: 125
[2025-12-03 21:44:18] INFO: ✓ کردستان: 53
```

### پشتیبان‌گیری

`data/backups/aqi_backup_20251203_214412.json`

خودکار ایجاد می‌شود و داده‌های قدیمی‌تر از 7 روز حذف می‌شوند.

## API مثال‌ها

### دریافت تمام داده‌ها

```bash
curl http://localhost:5000/api/aqi
```

### یک استان خاص

```bash
curl http://localhost:5000/api/aqi/تهران
```

### دامنه AQI

```bash
curl http://localhost:5000/api/aqi/range/50-100
```

### بدترین وضعیت

```bash
curl http://localhost:5000/api/aqi/worst?limit=10
```

### بهترین وضعیت

```bash
curl http://localhost:5000/api/aqi/best?limit=5
```

### آمار کلی

```bash
curl http://localhost:5000/api/aqi/stats
```

جواب:

```json
{
  "stats": {
    "total_states": 31,
    "average": 92.5,
    "minimum": 53,
    "maximum": 156,
    "median": 89
  }
}
```

## منطقه زمانی

**تمام داده‌ها به تهران (UTC+03:30) هستند**

مثال:

- ISO Format: `2025-12-03T21:44:12.123456+03:30`
- Offset: `+03:30` = 3 ساعت 30 دقیقه جلوتر از UTC
- منطقه: `Asia/Tehran`

## توسعه

### ساختار پروژه

```
├── config.py          # تنظیمات
├── scraper.py         # دریافت کننده
├── scheduler.py       # زمان‌بندی
├── api.py             # API REST
├── log_viewer.py      # مشاهده لاگ‌ها
├── run.py             # برنامه اصلی
├── data/              # داده‌ها
│   ├── aqi_data.json
│   └── backups/
└── logs/
    └── scraper.log
```

### تغییر فاصله دریافت

فایل `config.py`:

```python
SCHEDULE_INTERVAL_MINUTES = 30  # تغییر دهید
```

### تغییر مقدار حفاظ لاگ‌ها

فایل `scraper.py` تابع `cleanup_old_backups()`:

```python
cleanup_old_backups(days=7)  # تغییر دهید
```

## مشکل‌گیری

### لاگ ثبت نمی‌شود

```bash
python log_viewer.py stats
```

### API کار نمی‌کند

```bash
curl http://localhost:5000/api/health
```

### دریافت ناموفق

```bash
python log_viewer.py tail 50
```

لاگ‌های آخر را بررسی کنید.

## مشارکت

کمک‌ها خوش‌آمدند!
