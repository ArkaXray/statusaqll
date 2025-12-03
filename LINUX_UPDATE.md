# 🚀 Linux - Clone و Setup و Update

## 📥 مرحله 1: Clone کردن از GitHub

### شروع ساده‌ترین راه:

```bash
# 1. رفتن به دایرکتوری دلخواه
cd ~
# یا
cd /opt
# یا
cd /home/your-username

# 2. Clone کردن
git clone https://github.com/ArkaXray/statusaqll.git

# 3. رفتن داخل پوشه
cd statusaqll
```

---

## 🔧 مرحله 2: نصب اول‌بار

### **راه 1: اسکریپ خودکار (توصیه می‌شود)**

```bash
# اسکریپ رو executable کنید
chmod +x install.sh

# اجرا کنید
bash install.sh

# یا
./install.sh
```

**این اسکریپ:**

- ✅ بررسی Python
- ✅ نصب requirements
- ✅ نصب Playwright
- ✅ ایجاد دایرکتوری‌ها

### **راه 2: دستی**

```bash
# Python packages
pip3 install -r requirements.txt

# Playwright
python3 -m playwright install chromium

# نصب system dependencies
sudo apt-get update
sudo apt-get install -y libgconf-2-4 libx11-xcb1 ...

# اجرا
python3 run.py
```

---

## 🔄 مرحله 3: آپدیت کردن فایل‌ها

### **آپدیت ساده (فقط یک دستور!):**

```bash
git pull origin main
```

**این دستور:**

- ✅ دانلود تمام تغییرات
- ✅ آپدیت فایل‌ها
- ✅ نگه‌داشتن فایل‌های شما

---

## 🎯 چند سناریو مختلف:

### **سناریو 1: Clone → نصب → اجرا**

```bash
# 1. Clone
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 2. نصب
bash install.sh

# 3. اجرا
python3 run.py
```

**وقت: 5-10 دقیقه**

---

### **سناریو 2: Clone → نصب → Automation**

```bash
# 1. Clone
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 2. نصب
bash install.sh

# 3. Automation
chmod +x deploy.sh
./deploy.sh
# انتخاب 2 برای Systemd Service
```

**نتیجه:** خودکار هر 30 دقیقه کار می‌کند

---

### **سناریو 3: بعدتر آپدیت کردن**

```bash
# آپدیت
git pull origin main

# اجرا دوباره
python3 run.py
```

---

## 📝 دستورات Git مهم:

```bash
# مشاهده تغییرات
git status

# آپدیت
git pull origin main

# دیدن history
git log --oneline

# بازگشت به نسخه قبلی (اگر مشکلی بود)
git reset --hard HEAD~1

# مشاهده برنچ‌ها
git branch -a
```

---

## 🔐 اگر مشکل آپدیت داشتید:

### **مشکل: "Your local changes..."**

```bash
# راه 1: ذخیره تغییرات
git stash
git pull origin main

# راه 2: حذف تغییرات
git checkout -- .
git pull origin main
```

### **مشکل: "Permission denied"**

```bash
chmod +x *.sh
chmod +x install.sh
chmod +x deploy.sh
chmod +x fix-playwright.sh
```

---

## 💡 نکات مهم:

✅ **اول بار:** `bash install.sh`  
✅ **بعدی‌ها:** `git pull origin main`  
✅ **اگر Playwright مشکل:** `bash fix-playwright.sh`  
✅ **اگر permission:** `chmod +x *.sh`

---

## 📁 ساختار پوشه‌ها:

```
statusaqll/
├── install.sh              # نصب اول‌بار
├── fix-playwright.sh       # اگر Playwright مشکل دارد
├── deploy.sh              # برای automation
├── run.py                 # شروع برنامه
├── scheduler.py           # جمع‌آوری خودکار
├── api.py                 # API server
├── logs/                  # لاگ‌های برنامه
├── data/                  # داده‌های جمع‌آوری شده
└── requirements.txt       # Python packages
```

---

## 🚀 بعد از نصب:

```bash
# شروع برنامه
python3 run.py

# یا Scheduler
python3 scheduler.py

# یا API
python3 api.py

# یا Automation
./deploy.sh
```

---

## 📚 راهنمای‌های بیشتر:

- 📖 [QUICKSTART.md](QUICKSTART.md) - شروع سریع
- 📖 [INSTALL.md](INSTALL.md) - نصب مفصل
- 📖 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - حل مشکلات
- 📖 [PLAYWRIGHT_FIX.md](PLAYWRIGHT_FIX.md) - اگر Playwright مشکل دارد

---

**خلاصه: Clone → نصب → اجرا!** 🎉
