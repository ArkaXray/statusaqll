# 🌍 AQI Iran

سامانه جمع‌آوری و بررسی شاخص کیفیت هوای ایران

---

## ⚡ شروع سریع (یک کلیک!)

### **Windows**
```batch
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll
install.bat
```

### **Linux/Mac**
```bash
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll
bash install.sh
```

✅ **تمام!** برنامه به‌طور خودکار نصب می‌شود!

👉 [نقشه تفصیلی: QUICKSTART.md](QUICKSTART.md)

---

## ✨ ویژگی‌ها

- 📊 دریافت داده‌های AQI تمام 31 استان ایران
- 🔄 به‌روزرسانی خودکار هر 30 دقیقه
- 🔄 **Smart Retry Logic**: اگر سایت DOWN باشد، هر 10 دقیقه تست می‌کند
- 📝 لاگ جامع و قابل‌ردیابی
- 🌐 API RESTful برای دسترسی داده‌ها
- 🔒 عمومی - بدون نیاز به token یا secret
- 🕐 تمام زمان‌ها به منطقه زمانی تهران (UTC+03:30)
- 🐧 **اتوموشن کامل**: Cron/Systemd/Timer برای Ubuntu

## 📦 نصب دستی

```bash
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

## پیکربندی

فایل `config.py`:

```python
SCHEDULE_INTERVAL_MINUTES = 30
MAX_RETRIES = 3
RETRY_DELAY_MINUTES = 5

LOG_FILE = 'logs/scraper.log'
DATA_FILE = 'data/aqi_data.json'
```

## استفاده

### شروع Scheduler (دریافت خودکار)

```bash
python scheduler.py
```

### شروع API

```bash
python api.py
```

### دریافت دستی

```bash
python scraper.py
```

## API Endpoints

### همه داده‌ها

```
GET http://localhost:5000/api/aqi
```

### داده‌های یک استان

```
GET http://localhost:5000/api/aqi/تهران
```

### دامنه معین

```
GET http://localhost:5000/api/aqi/range/50-100
```

### بدترین وضعیت

```
GET http://localhost:5000/api/aqi/worst?limit=5
```

### بهترین وضعیت

```
GET http://localhost:5000/api/aqi/best?limit=5
```

### آمار

```
GET http://localhost:5000/api/aqi/stats
```

### ساعت تهران

```
GET http://localhost:5000/api/time
```

## ساختار پروژه

```
AQI_Iran/
├── config.py           # تنظیمات
├── scraper.py          # دریافت کننده اطلاعات
├── scheduler.py        # برنامه زمان‌بندی
├── api.py              # سرور API
├── requirements.txt    # وابستگی‌ها
├── data/
│   ├── aqi_data.json          # داده‌های فعلی
│   └── backups/               # پشتیبان‌گیری
└── logs/
    └── scraper.log           # لاگ‌ها
```

## منبع داده

- وبسایت: https://aqms.doe.ir/App/
- سازمان: وزارت محیط‌زیست ایران

## منطقه زمانی

تمام داده‌ها و لاگ‌ها به منطقه زمانی **Asia/Tehran** هستند.

- UTC Offset: **+03:30**
- مثال: `2025-12-03T21:44:12.167361+03:30`

## لاگ‌ها

فایل لاگ در `logs/scraper.log` ذخیره می‌شود.

نمونه:

```
[2025-12-03 21:44:12] INFO: شروع دریافت AQI در 2025-12-03T21:44:12.167361+03:30
[2025-12-03 21:44:15] INFO: ✓ تهران: 125
[2025-12-03 21:44:18] INFO: ✓ موفق: 31 استان دریافت شد
```

## ترتیب داده

```json
{
  "تهران": {
    "aqi": 125,
    "timestamp": "2025-12-03T21:44:12.167361+03:30"
  },
  "کردستان": {
    "aqi": 53,
    "timestamp": "2025-12-03T21:44:18.205123+03:30"
  }
}
```

## مجوز

MIT License - آزاد برای استفاده عمومی

## مشارکت

کمک‌ها خوش‌آمدند!
