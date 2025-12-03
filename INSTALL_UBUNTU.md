# 🐧 Ubuntu - راهنمای خودکارسازی

## 📋 نمای کلی

این راهنما برای راه‌اندازی خودکار **AQI Iran Scheduler** بر روی Ubuntu است.

---

## 🚀 روش‌های خودکارسازی

### ✅ **روش 1: Cron Job (سادگی: 10/10)**

**بهترین برای:**
- سرورهای کوچک
- درخواست‌های ساده
- سادگی بیشتر

**نصب:**
```bash
chmod +x setup_automation.sh
./setup_automation.sh
# انتخاب 1
```

**بررسی:**
```bash
crontab -l
```

**لاگ:**
```bash
tail -f logs/cron.log
```

---

### ✅ **روش 2: Systemd Service (قابلیت اعتماد: 10/10)**

**بهترین برای:**
- سرورهای تولیدی
- نیاز به restart خودکار
- مدیریت بهتر

**نصب:**
```bash
chmod +x setup_automation.sh
./setup_automation.sh
# انتخاب 2
```

**فرمان‌ها:**
```bash
# وضعیت
systemctl --user status aqi-scheduler

# شروع
systemctl --user start aqi-scheduler

# متوقف کردن
systemctl --user stop aqi-scheduler

# راه‌اندازی مجدد
systemctl --user restart aqi-scheduler

# لاگ زنده
journalctl --user -u aqi-scheduler -f
```

---

### ✅ **روش 3: Systemd Timer (دقت: 10/10)**

**بهترین برای:**
- کنترل دقیق زمان
- فاصلات منظم
- پیشرفته‌ترین

**نصب:**
```bash
chmod +x setup_automation.sh
./setup_automation.sh
# انتخاب 3
```

**فرمان‌ها:**
```bash
# لیست تایمرها
systemctl --user list-timers

# وضعیت تایمر
systemctl --user status aqi-scheduler.timer

# لاگ‌ها
journalctl --user -u aqi-scheduler.service -f
```

---

## 🔧 نصب دستی

اگر می‌خواهید دستی نصب کنید:

### **برای Cron:**

```bash
# ویرایش cron
crontab -e

# اضافه کردن این خط:
*/30 * * * * cd /path/to/AQI_Iran && python3 scheduler.py >> logs/cron.log 2>&1
```

### **برای Systemd Service:**

```bash
# ایجاد دایرکتوری
mkdir -p ~/.config/systemd/user

# کپی کردن فایل
cp aqi-scheduler.service ~/.config/systemd/user/

# فعال‌سازی
systemctl --user daemon-reload
systemctl --user enable aqi-scheduler.service
systemctl --user start aqi-scheduler.service
```

### **برای Systemd Timer:**

```bash
# کپی کردن فایل‌ها
cp aqi-scheduler.service ~/.config/systemd/user/
cp aqi-scheduler.timer ~/.config/systemd/user/

# فعال‌سازی
systemctl --user daemon-reload
systemctl --user enable aqi-scheduler.timer
systemctl --user start aqi-scheduler.timer
```

---

## 📊 مقایسه روش‌ها

| ویژگی | Cron | Service | Timer |
|-------|------|---------|-------|
| سادگی | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| قابلیت‌اعتماد | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| restart خودکار | ❌ | ✅ | ❌ |
| دقت زمان | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| مدیریت سهل | ❌ | ✅ | ✅ |
| نیاز به root | ❌ | ❌ | ❌ |

---

## ⚙️ تنظیمات اضافی

### تغییر فاصله زمانی

اگر می‌خواهید هر **60 دقیقه** به جای 30 دقیقه:

**Cron:**
```bash
crontab -e
# تغییر: */30 → */60
```

**Timer:**
```bash
nano ~/.config/systemd/user/aqi-scheduler.timer
# تغییر: OnUnitActiveSec=30min → OnUnitActiveSec=60min
systemctl --user restart aqi-scheduler.timer
```

---

## 🐛 حل مشکلات

### مشکل: Scheduler کار نمی‌کند

**Cron:**
```bash
# بررسی cron logs
grep CRON /var/log/syslog | tail -20

# یا
journalctl -xeu cron
```

**Systemd:**
```bash
# بررسی وضعیت
systemctl --user status aqi-scheduler

# لاگ‌های دقیق
journalctl --user -u aqi-scheduler -n 50
```

### مشکل: Permission denied

```bash
# اطمینان حاصل کنید فایل‌های setup قابل اجرا هستند
chmod +x setup_automation.sh
chmod +x setup_cron.sh
```

### مشکل: Python modules یافت نشدند

```bash
# نصب مجدد dependencies
cd /path/to/AQI_Iran
pip3 install -r requirements.txt
```

---

## 🎯 بهترین عملکرد

### برای **سرور تولیدی**: Systemd Service
```bash
./setup_automation.sh  # انتخاب 2
```

### برای **استفاده شخصی**: Cron Job
```bash
./setup_automation.sh  # انتخاب 1
```

### برای **دقت بیشتر**: Systemd Timer
```bash
./setup_automation.sh  # انتخاب 3
```

---

## 📝 لاگ‌ها

### مسیر لاگ‌ها:
- **Cron**: `logs/cron.log`
- **Systemd**: `journalctl --user -u aqi-scheduler`

### نمایش لاگ‌های زنده:
```bash
# Cron
tail -f logs/cron.log

# Systemd
journalctl --user -u aqi-scheduler -f
```

---

## ✅ بررسی اینکه همه چیز کار می‌کند

```bash
# 1. بررسی وضعیت
systemctl --user status aqi-scheduler  # یا crontab -l

# 2. بررسی لاگ‌ها
tail -f logs/cron.log  # یا journalctl --user -u aqi-scheduler -f

# 3. بررسی داده‌ها
cat data/aqi_data.json | python3 -m json.tool

# 4. تست دستی
python3 scheduler.py
```

---

## 🚀 دستورات مفید

```bash
# نمایش تمام فرآیندهای Python
ps aux | grep python3

# کشتن scheduler
pkill -f "scheduler.py"

# بررسی استفاده از منابع
top -p $(pgrep -f scheduler.py)

# مشاهده فایل‌های باز
lsof -p $(pgrep -f scheduler.py)
```

---

## 📞 پشتیبانی

اگر مشکلی داشتید:

1. لاگ‌ها را بررسی کنید
2. دستور را دستی اجرا کنید
3. بررسی کنید Python و dependencies نصب‌اند

---

**نسخه**: 1.0.0  
**آخرین به‌روزرسانی**: 2025-12-03  
**وضعیت**: ✅ آماده برای تولید
