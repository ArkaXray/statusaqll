# 📖 Linux - نصب و آپدیت (خلاصه)

## 🚀 شروع فوری (3 دستور):

```bash
# 1. Clone
git clone https://github.com/ArkaXray/statusaqll.git && cd statusaqll

# 2. نصب
bash install.sh

# 3. اجرا
python3 run.py
```

**وقت: 5 دقیقه** ⏱️

---

## 🔄 آپدیت (یک دستور):

```bash
bash update.sh
```

یا:
```bash
git pull origin main
```

---

## 📚 راهنما‌های تفصیلی:

| راهنما | توضیح |
|--------|--------|
| **[LINUX_SETUP.md](LINUX_SETUP.md)** | نصب step-by-step |
| **[LINUX_UPDATE.md](LINUX_UPDATE.md)** | آپدیت و نگهداری |
| **[QUICKSTART.md](QUICKSTART.md)** | شروع سریع |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | حل مشکلات |

---

## 🎯 مرحله‌ها:

### **اول (یک بار):**

```bash
# 1. نیازمندی‌ها
sudo apt-get install python3 python3-pip git

# 2. Clone
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 3. نصب
bash install.sh

# 4. اجرا
python3 run.py
```

### **بعدی‌ها (آپدیت):**

```bash
# آپدیت
bash update.sh

# یا
git pull origin main
```

---

## 🔧 دستورات مهم:

```bash
# نصب برنامه
bash install.sh

# آپدیت
bash update.sh

# Fix Playwright
bash fix-playwright.sh

# Automation
bash deploy.sh

# منوی اصلی
python3 run.py

# Scheduler
python3 scheduler.py

# API
python3 api.py
```

---

## 📁 فایل‌های مهم:

| فایل | توضیح |
|------|--------|
| `install.sh` | نصب اول |
| `update.sh` | آپدیت |
| `fix-playwright.sh` | اگر مشکل |
| `deploy.sh` | Automation |
| `run.py` | منوی اصلی |

---

## ⚠️ اگر مشکلی بود:

```bash
# Playwright مشکل دارد؟
bash fix-playwright.sh

# Permission مشکل؟
chmod +x *.sh

# خودکار نصب؟
./deploy.sh
```

---

**خلاصه: Clone → Bash Install → Python Run!** ✨

👉 [راهنمای مفصل: LINUX_SETUP.md](LINUX_SETUP.md)
