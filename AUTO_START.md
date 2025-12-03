# 🚀 AQI Iran - Full Auto-Start Guide

**تنظیم خودکار برنامه بدون نیاز به دستور دستی**

---

## 📋 Quick Setup (2 دقیقه)

```bash
# اجرا کردن setup script
bash setup-service.sh

# تمام! سرویس خودکار شروع می‌شود
```

---

## ✅ چه اتفاقی می‌افتد؟

1. **Service File** کپی و تنظیم می‌شود
2. **systemd** فعال می‌شود
3. **Scheduler + API** خودکار شروع می‌شوند
4. **هر 30 دقیقه** اطلاعات خودکار جمع‌آوری می‌شود
5. **هر بوت** سیستم، سرویس خودکار فعال می‌شود

---

## 🔍 بررسی وضعیت

### سرویس در حال اجرا است؟

```bash
systemctl --user status aqi-full
```

**Output Example:**
```
● aqi-full.service - AQI Iran Auto-Start Service
     Loaded: loaded (/home/user/.config/systemd/user/aqi-full.service; enabled; preset: enabled)
     Active: active (running) since Wed 2024-01-10 14:30:00 +0330; 5h ago
   Main PID: 12345 (python3)
      Tasks: 5 (limit: 512)
     Memory: 85.2M
        CPU: 2m 34.123s
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/aqi-full.service
             ├─12345 python3 run.py
             ├─12346 python3 -m scheduler
             └─12347 python3 -m api
```

---

## 📊 مشاهده لاگ‌ها

### لاگ زنده (Real-time)

```bash
# آخرین لاگ‌ها را ببینید
journalctl --user -u aqi-full -f

# Output:
# Jan 10 14:30:00 hostname python3[12345]: [Main] Starting Scheduler...
# Jan 10 14:30:02 hostname python3[12345]: [Main] Starting API on port 5000...
# Jan 10 14:30:03 hostname python3[12345]: [Main] API listening: http://localhost:5000
# Jan 10 15:00:00 hostname python3[12346]: [Main] Collection started for 31 provinces...
```

### لاگ‌های گذشته

```bash
# آخرین 50 لاگ
journalctl --user -u aqi-full -n 50

# لاگ‌های آخر ساعت
journalctl --user -u aqi-full --since "1 hour ago"

# لاگ‌های میانسالی retry
journalctl --user -u aqi-full | grep "\[Retry\]"

# لاگ‌های خطا
journalctl --user -u aqi-full --priority err
```

---

## 🎛️ کنترل سرویس

### شروع

```bash
systemctl --user start aqi-full
```

### متوقف کردن

```bash
systemctl --user stop aqi-full
```

### Restart

```bash
systemctl --user restart aqi-full
```

### Reload (بدون قطع سرویس)

```bash
systemctl --user reload aqi-full
```

### Disable (خودکار فعال نشود)

```bash
systemctl --user disable aqi-full

# برای دوباره فعال کردن:
systemctl --user enable aqi-full
```

---

## 🌐 دسترسی به API

سرویس خودکار درگاهپورت **5000** را باز می‌کند

### از طریق Terminal:

```bash
# همه استان‌ها
curl http://localhost:5000/api/aqi | jq

# استان خاص (تهران)
curl http://localhost:5000/api/aqi/tehran | jq

# آمار
curl http://localhost:5000/api/aqi/stats | jq

# بهترین هوا
curl http://localhost:5000/api/aqi/best?limit=5 | jq

# بدترین هوا
curl http://localhost:5000/api/aqi/worst?limit=5 | jq

# زمان تهران
curl http://localhost:5000/api/time | jq
```

### از طریق مرورگر:

```
http://localhost:5000/api/aqi
http://localhost:5000/api/aqi/tehran
http://localhost:5000/api/aqi/stats
```

---

## 📁 فایل‌های مهم

```
~/.config/systemd/user/aqi-full.service      # فایل Service
~/aqi-full.log                               # فایل لاگ (اگر داشته باشد)
~/.local/share/aqi-iran/                     # داده‌های ذخیره‌شده
```

---

## 🐛 عیب یابی

### سرویس شروع نمی‌شود

```bash
# بررسی لاگ‌ها
journalctl --user -u aqi-full -n 20

# بررسی Python
which python3
python3 --version

# بررسی دسترسی‌های فایل
ls -la ~/.config/systemd/user/aqi-full.service
```

### API جواب نمی‌دهد

```bash
# بررسی سرویس
systemctl --user status aqi-full

# بررسی درگاه
ss -tulpn | grep 5000

# دوباره شروع
systemctl --user restart aqi-full

# صبر کنید 5 ثانیه بعد از شروع
sleep 5
curl http://localhost:5000/api/health
```

### Scheduler اطلاعات جمع‌آوری نمی‌کند

```bash
# بررسی لاگ‌های retry
journalctl --user -u aqi-full | grep "\[Retry\]"

# بررسی وضعیت سایت
curl http://localhost:5000/api/site-status

# بررسی اتصال اینترنت
ping aqms.doe.ir
```

### حافظه زیاد استفاده می‌شود

```bash
# مشاهده استفاده‌ی حافظه
journalctl --user -u aqi-full | grep "Memory"

# restart کردن سرویس
systemctl --user restart aqi-full

# بررسی فایل‌های backup قدیمی
ls -lah ~/.local/share/aqi-iran/backups/
```

---

## 🔄 به‌روزرسانی

### برای اپدیت کردن پروژه:

```bash
cd ~/statusaqll  # یا مسیر پروژه

# اپدیت از GitHub
git pull origin main

# اگر اپدیت داشت، restart کنید
systemctl --user restart aqi-full
```

---

## 📈 مشاهده Performance

```bash
# استفاده‌ی CPU و حافظه
watch -n 1 'systemctl --user status aqi-full | grep -A5 "Memory"'

# تعداد فرآیند‌های جاری
systemctl --user status aqi-full | grep "Tasks"

# تاریخچه مصرف
journalctl --user -u aqi-full | grep -E "Memory|CPU|Tasks"
```

---

## ✨ نکات مهم

- **Scheduler** هر 30 دقیقه اطلاعات جمع‌آوری می‌کند
- **Retry Logic** در صورت خرابی 3 بار سعی می‌کند
- **API** بدون قطع مستمر جواب می‌دهد
- **Timezone** همیشه Asia/Tehran است
- **Auto-Restart** اگر سرویس ریخت، خودکار دوباره شروع می‌شود
- **Persistent** اطلاعات در JSON فایل ذخیره می‌شود

---

## 📞 کمک و پشتیبانی

### لاگ کامل صادر کردن:

```bash
# صادر کردن لاگ‌های امروز
journalctl --user -u aqi-full --since "today" > aqi-logs.txt

# صادر کردن تمام لاگ‌ها
journalctl --user -u aqi-full > aqi-logs-full.txt
```

### مسائل معمول:

| مسئله | حل |
|------|-----|
| سرویس شروع نمی‌شود | `journalctl --user -u aqi-full -n 20` |
| API جواب نمی‌دهد | `systemctl --user restart aqi-full` |
| دیتا آپدیت نمی‌شود | بررسی `[Main]` لاگ‌ها |
| Retry زیاد می‌شود | بررسی وضعیت سایت `aqi-full.service` |

---

## 🎉 تمام!

حالا سیستم شما **کاملاً خودکار** است! 

- ✅ هر 30 دقیقه اطلاعات جمع‌آوری می‌شود
- ✅ API همیشه در دسترس است
- ✅ هر بوت، سرویس خودکار شروع می‌شود
- ✅ لاگ‌ها دائماً ثبت می‌شوند
- ✅ خطاها خودکار تلاش دوباره می‌شوند

**دیگر نیازی به دستور دستی نیست!** 🚀
