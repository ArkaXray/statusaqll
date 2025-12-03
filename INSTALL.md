# 📥 نصب و اجرا - راهنمای کامل

## 🚀 شروع فوری (بدون دردسر)

### **Windows - One-Click! 🖱️**

```
1. دانلود و یا Clone:
   git clone https://github.com/ArkaXray/statusaqll.git
   cd statusaqll

2. دوبار کلیک روی:
   install.bat

3. تمام! ✨
```

### **Linux/Mac - One Command! 🐧**

```bash
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll
bash install.sh
```

---

## 📋 Install Script چیکار می‌کند:

✅ بررسی Python  
✅ بررسی pip  
✅ ایجاد دایرکتوری‌ها (logs, data)  
✅ نصب تمام Python packages  
✅ دانلود Playwright browsers  
✅ تست syntax تمام فایل‌ها  
✅ اجرای برنامه (اختیاری)  

---

## 🎯 بعد از نصب:

### **Option 1: منوی اصلی (توصیه می‌شود)**

```bash
# Windows
python run.py

# Linux/Mac
python3 run.py
```

**منو:**
```
1. Start Scheduler (30-min intervals)
2. Start API Server (port 5000)
3. Manual Collection
4. View Logs
5. View Stats
0. Exit
```

---

### **Option 2: مستقیم اجرا**

#### **Scheduler (دریافت خودکار)**
```bash
# Windows
python scheduler.py

# Linux/Mac
python3 scheduler.py

# نتیجه:
# ✅ هر 30 دقیقه داده جمع‌آوری می‌کند
# 🔄 اگر سایت DOWN باشد: retry هر 10 دقیقه
# 📊 تمام اطلاعات در logs/scraper.log
```

#### **API Server (وب دسترسی)**
```bash
# Windows
python api.py

# Linux/Mac
python3 api.py

# نتیجه:
# 🌐 http://localhost:5000/api/health
# 📊 http://localhost:5000/api/aqi
```

---

## 🌐 API Endpoints

بعد از اجرای API:

```
Health Check:
  http://localhost:5000/api/health

Site Status:
  http://localhost:5000/api/site-status

AQI Data:
  http://localhost:5000/api/aqi              # تمام 31 استان
  http://localhost:5000/api/aqi/Tehran       # استان خاص
  http://localhost:5000/api/aqi/range/0-100  # حد مشخص
  http://localhost:5000/api/aqi/worst?limit=5
  http://localhost:5000/api/aqi/best?limit=5
  http://localhost:5000/api/aqi/stats

System:
  http://localhost:5000/api/time             # زمان فعلی (تهران)
```

---

## 🐧 برای Ubuntu/Linux (Automation)

اگر می‌خواهید خودکار اجرا شود:

```bash
chmod +x deploy.sh
./deploy.sh

# انتخاب کنید:
# 1) Cron Job (ساده)
# 2) Systemd Service (بهترین) ⭐
# 3) Systemd Timer (دقیق)
```

---

## 🔍 بررسی لاگ‌ها

### **Logs مکان:**
- `logs/scraper.log` - لاگ‌های scraper

### **نمایش:**

**Windows:**
```batch
type logs\scraper.log
```

**Linux/Mac:**
```bash
tail -f logs/scraper.log
```

---

## 🐛 حل مشکلات

### **"Python not found"**

**Windows:**
- دانلود از: https://www.python.org/downloads/
- نصب با checkbox "Add Python to PATH"

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Mac:**
```bash
brew install python3
```

---

### **"Permission denied" (Linux/Mac)**

```bash
chmod +x install.sh
bash install.sh
```

---

### **"Module not found"**

```bash
# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

---

### **"Port already in use"**

**Mac/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

**Windows:**
```batch
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

### **"Playwright not installed"**

```bash
# Windows
python -m playwright install chromium

# Linux/Mac
python3 -m playwright install chromium
```

---

## 📚 مستندات بیشتر

| فایل | توضیح |
|------|--------|
| [README.md](README.md) | راهنمای کامل |
| [QUICKSTART.md](QUICKSTART.md) | شروع سریع |
| [USAGE.md](USAGE.md) | نحوه استفاده |
| [RETRY_LOGIC.md](RETRY_LOGIC.md) | توضیح Retry Logic |
| [INSTALL_UBUNTU.md](INSTALL_UBUNTU.md) | نصب بر Ubuntu |
| [FINAL_STATUS.md](FINAL_STATUS.md) | وضعیت فاینالی |

---

## ✨ مثال کامل

### **یک جلسه نموج:**

```bash
# 1. Clone
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 2. نصب (Windows: install.bat, Linux: bash install.sh)
bash install.sh

# 3. انتخاب:
# - Scheduler: python3 scheduler.py
# - یا API: python3 api.py
# - یا Menu: python3 run.py

# 4. بررسی:
# - Logs: tail -f logs/scraper.log
# - API: http://localhost:5000/api/aqi

# 5. برای اتوموشن:
chmod +x deploy.sh
./deploy.sh
```

---

## 🎯 خلاصه

| مرحله | فرمان | وقت |
|------|-------|------|
| 1. Clone | `git clone ...` | 30 ثانیه |
| 2. Install | `bash install.sh` یا `install.bat` | 2-3 دقیقه |
| 3. Run | `python3 run.py` | فوری |
| 4. Test | `http://localhost:5000/api/aqi` | 10 ثانیه |

**کل: حدود 5 دقیقه!** ⏱️

---

**آماده شروع؟ 🚀**

```bash
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll
bash install.sh  # یا install.bat (Windows)
```
