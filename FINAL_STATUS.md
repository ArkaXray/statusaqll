# 🎉 AQI Iran - نسخه Final

## 📊 وضعیت پروژه

```
✅ Scraper       - تمام 31 استان
✅ Scheduler     - هر 30 دقیقه (با Retry Logic)
✅ API           - 8+ endpoints
✅ Retry Logic   - Smart fallback mechanism
✅ Health Check  - Site status monitoring
✅ Logging       - Detailed [Main] و [Retry] tags
✅ Automation    - Cron/Systemd/Timer
✅ Documentation - کامل و جامع
✅ GitHub Ready  - Deployment-ready
```

---

## 🚀 شروع سریع

### **Option 1: Windows (فوری)**

```powershell
# منوی اصلی
python run.py

# یا مستقیم
python scheduler.py
python api.py
```

### **Option 2: Ubuntu (Production)**

```bash
# نصب و راه‌اندازی
chmod +x deploy.sh
./deploy.sh
# انتخاب: 2 (برای Systemd Service)

# بررسی
systemctl --user status aqi-scheduler
journalctl --user -u aqi-scheduler -f
```

### **Option 3: Cron Job (ساده)**

```bash
chmod +x setup_automation.sh
./setup_automation.sh
# انتخاب: 1
```

---

## 🔄 Retry Logic (جدید!)

### **سناریو نرمال:**

```
12:00 ✅ [Main]   Success
12:30 ✅ [Main]   Success
13:00 ✅ [Main]   Success
```

### **سناریو با خرابی:**

```
12:00 ❌ [Main]   Site DOWN
12:10 🔄 [Retry]  Failed (retry 1)
12:20 🔄 [Retry]  Failed (retry 2)
12:30 🔄 [Retry]  Failed (retry 3)
12:30 ❌ [Main]   Back to schedule
13:00 ✅ [Main]   Success
```

---

## 📁 فایل‌های پروژه

### **کد اصلی:**

| فایل | توضیح | وضعیت |
|------|--------|-------|
| `config.py` | تنظیمات پروژه | ✅ |
| `scraper.py` | Web scraper | ✅ |
| `scheduler.py` | **Scheduler with Retry** | ✅ NEW! |
| `api.py` | **API with Health Check** | ✅ NEW! |
| `run.py` | منوی اصلی | ✅ |
| `log_viewer.py` | نمایش لاگ‌ها | ✅ |

### **Automation (Ubuntu):**

| فایل | توضیح |
|------|--------|
| `deploy.sh` | **Main deployment script** |
| `setup_automation.sh` | Setup script with menu |
| `setup_cron.sh` | Cron setup |
| `aqi-scheduler.service` | Systemd service |
| `aqi-scheduler.timer` | Systemd timer |

### **Documentation:**

| فایل | توضیح |
|------|--------|
| `README.md` | راهنمای فارسی |
| `USAGE.md` | نحوه استفاده |
| `RETRY_LOGIC.md` | **توضیح Retry Logic** |
| `INSTALL_UBUNTU.md` | نصب بر Ubuntu |

---

## 🔧 تنظیمات کلیدی

### `config.py`:

```python
SCHEDULE_INTERVAL_MINUTES = 30      # نیم‌ساعتی
MAX_RETRIES = 3                     # 3 تلاش
RETRY_DELAY_MINUTES = 10            # 10 دقیقه بین تلاش‌ها
```

---

## 🌐 API Endpoints

```bash
# Health Check
GET /api/health

# Site Status
GET /api/site-status

# AQI Data
GET /api/aqi
GET /api/aqi/<state>
GET /api/aqi/range/<min>-<max>
GET /api/aqi/worst?limit=5
GET /api/aqi/best?limit=5
GET /api/aqi/stats

# System
GET /api/time
```

---

## 📝 نمونه لاگ

### **موفق:**

```
[2025-12-03 12:00:15] INFO: ⏰ [Main] Starting main scrape at 2025-12-03T12:00:15+0330
[2025-12-03 12:00:15] INFO: ✅ [Main] Site is UP
[2025-12-03 12:00:35] INFO: ✅ [Main] Success: 31 states collected
```

### **با Retry:**

```
[2025-12-03 12:30:15] INFO: ⏰ [Main] Starting main scrape
[2025-12-03 12:30:15] WARNING: 🚨 [Main] Site is DOWN
[2025-12-03 12:30:35] WARNING: ⚠️ [Retry] Attempt 1 failed. Retrying in 10 min
[2025-12-03 12:40:15] INFO: 🔄 [Retry] Attempt 2
[2025-12-03 12:40:45] ERROR: ❌ [Retry] All 3 attempts failed
```

---

## ✨ ویژگی‌های جدید

### 1. **Smart Retry Logic**
- 🔄 اگر سایت DOWN باشد، هر 10 دقیقه تست می‌کند
- ⏱️ سه بار تلاش، سپس بازگشت به زمان‌بندی اصلی
- 🎯 هشدار اگر 3 بار متوالی ناموفق

### 2. **Health Check API**
- 🌐 endpoint برای بررسی وضعیت سایت
- 📊 endpoint برای status سیستم
- 🔗 integration با retry logic

### 3. **Detailed Logging**
- 📍 **[Main]** tags برای اجرای اصلی
- 🔄 **[Retry]** tags برای تلاش‌های دوباره
- 📝 تمام اطلاعات در لاگ

### 4. **Production Deployment**
- 🚀 `deploy.sh` - One-click deployment
- 🔒 Systemd integration
- 📊 Monitoring و logging

---

## 🎯 مقایسه Automation

| روش | سادگی | قابلیت‌اعتماد | بهتر برای |
|-----|-------|--------|----------|
| **Cron** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | سرورهای ساده |
| **Service** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **تولید** ⭐ |
| **Timer** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | دقت بیشتر |

---

## 📋 نقشه راه

- ✅ Scraper: تمام 31 استان
- ✅ Scheduler: هر 30 دقیقه
- ✅ Retry Logic: 3 تلاش × 10 دقیقه
- ✅ Health Check: قبل از هر scrape
- ✅ Logging: [Main] و [Retry] tags
- ✅ API: 8+ endpoints
- ✅ Automation: Cron/Systemd/Timer
- ✅ GitHub: deployment-ready

---

## 🚨 خرابی‌های ممکن و حل

### **مشکل: لاگ‌ها نمی‌رسند**

```bash
# بررسی permissions
chmod 755 logs/
chmod 755 data/

# پاک‌سازی و دوباره شروع
rm logs/scraper.log
python scheduler.py
```

### **مشکل: API کار نمی‌کند**

```bash
# بررسی port
netstat -tlnp | grep 5000

# یا (macOS/Linux)
lsof -i :5000
```

### **مشکل: Retry logic کار نمی‌کند**

```bash
# بررسی config
cat config.py | grep -i retry

# تست دستی
python -c "from scheduler import check_site_health; print(check_site_health())"
```

---

## 🔐 Security

- ✅ بدون secrets یا tokens
- ✅ Public endpoints
- ✅ CORS enabled
- ✅ No authentication needed

---

## 📊 Performance

- ⚡ تقریباً 20-30 ثانیه برای scrape
- 💾 کم حافظه (< 50MB)
- 🌐 Single threaded
- 🔄 Retry logic بدون اضافه‌بار

---

## 🎓 نحوه استفاده

### **برای تست:**

```bash
python scheduler.py
```

### **برای API:**

```bash
python api.py
# سپس http://localhost:5000/api/health
```

### **برای عملیات:**

```bash
# Windows
python run.py

# Ubuntu
./deploy.sh
```

---

## 📞 مشکلات رایج

1. **"Module not found"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Permission denied"**
   ```bash
   chmod +x *.sh
   ```

3. **"Port already in use"**
   ```bash
   pkill -f api.py
   ```

---

## ✅ بررسی قبل از Deployment

- ✅ تمام syntax درست است
- ✅ تمام dependencies نصب‌اند
- ✅ لاگ‌ها کار می‌کنند
- ✅ API responsive است
- ✅ Scheduler اجرا می‌شود
- ✅ Retry logic active است
- ✅ Health check کار می‌کند

---

## 🚀 نتیجه‌گیری

**پروژه شما اکنون:**
- ✨ Production-Ready است
- 🔄 با خرابی‌های سایت مقابله می‌کند
- 📊 جزئیات کامل ثبت می‌کند
- 🌐 API کامل دارد
- 🐧 برای Ubuntu آماده است
- 🔒 امن و قابل اعتماد است

---

**نسخه**: 2.0.0 (with Retry Logic)  
**وضعیت**: ✅ Production Ready  
**آخرین به‌روزرسانی**: 2025-12-03

---

**آماده برای GitHub! 🎉**
