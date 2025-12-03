# 🐧 Linux Setup - نصب کامل (Step by Step)

## 📋 مرحله‌به‌مرحله

### **مرحله 1: نیازمندی‌های سیستم**

```bash
# به‌روز رسانی لیست پکیج‌ها
sudo apt-get update

# نصب Python و Git
sudo apt-get install -y \
    python3 \
    python3-pip \
    git

# بررسی نسخه‌ها
python3 --version
pip3 --version
git --version
```

---

### **مرحله 2: Clone از GitHub**

```bash
# انتخاب مکان (یکی از:)
cd ~              # Home directory
cd /opt           # یا /opt
cd /home/user     # یا دایرکتوری خاص

# Clone
git clone https://github.com/ArkaXray/statusaqll.git

# رفتن داخل
cd statusaqll

# مشاهده فایل‌ها
ls -la
```

---

### **مرحله 3: نصب برنامه**

#### **راه 1: اسکریپ (آسان‌تر)**

```bash
# executable کردن
chmod +x install.sh

# اجرا
bash install.sh

# یا
./install.sh

# منتظر بمانید تا تکمیل شود (2-3 دقیقه)
```

#### **راه 2: دستی**

```bash
# 1. نصب Python packages
pip3 install -r requirements.txt

# 2. نصب Playwright browsers
python3 -m playwright install chromium

# 3. نصب system dependencies
sudo apt-get install -y \
    libgconf-2-4 \
    libx11-xcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-xfixes0 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libasound2
```

---

### **مرحله 4: اجرا**

#### **راه 1: منوی تعاملی**

```bash
python3 run.py
```

**منو:**
```
1. Start Scheduler (auto collect every 30 minutes)
2. Start API Server (port 5000)
3. Manual Collection
4. View Logs (last 50)
5. View Stats
0. Exit
```

#### **راه 2: Scheduler (جمع‌آوری خودکار)**

```bash
python3 scheduler.py

# نتیجه:
# [2025-12-03 22:37:37] INFO: 🚀 AQI Scheduler started
# [2025-12-03 22:37:37] INFO: ✅ [Main] Success: 31 states collected
# هر 30 دقیقه تکرار می‌شود
```

#### **راه 3: API Server**

```bash
python3 api.py

# نتیجه:
# * Running on http://0.0.0.0:5000/
# سپس: http://localhost:5000/api/aqi
```

---

### **مرحله 5: Automation (اختیاری)**

برای اجرای خودکار بدون دستور:

```bash
# executable کردن
chmod +x deploy.sh

# اجرا
./deploy.sh

# انتخاب کنید:
# 1) Cron Job
# 2) Systemd Service (بهترین)
# 3) Systemd Timer
```

**بعدش بدون دستور کار می‌کند!**

---

## 🔄 آپدیت نسخه‌های جدید

```bash
# آپدیت ساده
git pull origin main

# یا اسکریپ
chmod +x update.sh
./update.sh
```

---

## 📝 دستورات مفید:

```bash
# وضعیت
git status

# لاگ‌های اخیر
git log --oneline -5

# مشاهده فایل‌های تغییر کرده
git diff HEAD~1

# بازگشت به نسخه قبلی
git reset --hard HEAD~1

# حذف همه تغییرات ناخواسته
git checkout -- .
```

---

## 🐛 حل مشکلات:

### **"Python3 not found"**
```bash
sudo apt-get install python3
```

### **"Permission denied"**
```bash
chmod +x *.sh
```

### **"Playwright error"**
```bash
bash fix-playwright.sh
```

### **"Port already in use"**
```bash
pkill -f "api.py"
```

---

## 📊 ساختار نهایی:

```
/home/user/statusaqll/
├── install.sh              ← نصب اول
├── update.sh               ← آپدیت
├── fix-playwright.sh       ← اگر مشکل
├── deploy.sh              ← Automation
├── run.py                 ← منوی اصلی
├── scheduler.py           ← Scheduler
├── api.py                 ← API
├── logs/                  ← لاگ‌ها
│   └── scraper.log
├── data/                  ← داده‌ها
│   ├── aqi_data.json
│   └── backups/
└── requirements.txt       ← Dependencies
```

---

## ✨ سناریو کامل:

```bash
# 1. نصب
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll
bash install.sh

# 2. اجرا
python3 run.py

# 3. آپدیت (بعدتر)
git pull origin main
python3 run.py

# 4. Automation (اختیاری)
./deploy.sh
```

---

## 🎯 خلاصه:

| Step | فرمان | وقت |
|------|-------|-----|
| 1. Clone | `git clone ...` | 30 ثانیه |
| 2. نصب | `bash install.sh` | 3 دقیقه |
| 3. اجرا | `python3 run.py` | فوری |
| 4. آپدیت | `git pull origin main` | 30 ثانیه |

**کل: ~5 دقیقه!** ⏱️

---

**آماده‌اید! 🚀**
