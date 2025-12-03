# 🚀 AQI Iran - Quick Start (یک کلیک نصب!)

## ⚡ سریع‌ترین راه شروع

### **Windows - فقط یک کلیک! 🖱️**

```batch
# 1. Clone کن
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 2. دوبار کلیک کن
install.bat

# همین! 🎉
```

### **Linux/Mac - یک دستور! 🐧**

```bash
# 1. Clone کن
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 2. اجرا کن
bash install.sh

# همین! 🎉
```

---

## 📋 نصب Script انجام می‌دهد:

- ✅ بررسی Python
- ✅ بررسی pip
- ✅ ایجاد دایرکتوری‌ها
- ✅ نصب تمام packages
- ✅ دانلود Playwright browsers
- ✅ تست syntax
- ✅ اجرای برنامه (اختیاری)

---

## 🎯 بعد از نصب:

### **Option 1: منوی تعاملی**

```bash
python run.py          # Windows
python3 run.py         # Linux/Mac

# سپس:
# 1. Start Scheduler
# 2. Start API Server
```

### **Option 2: Scheduler مستقیم**

```bash
python scheduler.py    # Windows
python3 scheduler.py   # Linux/Mac

# هر 30 دقیقه داده جمع‌آوری می‌کند
```

### **Option 3: API مستقیم**

```bash
python api.py          # Windows
python3 api.py         # Linux/Mac

# سپس: http://localhost:5000/api/health
```

---

## 🌐 API Endpoints

بعد از اجرای API:

```
http://localhost:5000/api/health              # Health check
http://localhost:5000/api/site-status         # Site status
http://localhost:5000/api/aqi                 # All 31 states
http://localhost:5000/api/aqi/Tehran          # Specific state
http://localhost:5000/api/aqi/stats           # Statistics
http://localhost:5000/api/time                # Current time
```

---

## 🔧 اگر مشکل داشتید:

### **"Python not found"**
```bash
# Windows: https://www.python.org/downloads/
# Linux: sudo apt install python3
# Mac: brew install python3
```

### **"Permission denied" (Linux/Mac)**
```bash
chmod +x install.sh
bash install.sh
```

### **"Module not found"**
```bash
pip install -r requirements.txt
```

### **"Port already in use"**
```bash
# Mac/Linux
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## 📚 مستندات:

- 📖 [README.md](README.md) - راهنمای کامل
- 📖 [USAGE.md](USAGE.md) - نحوه استفاده
- 📖 [RETRY_LOGIC.md](RETRY_LOGIC.md) - توضیح Retry Logic
- 📖 [FINAL_STATUS.md](FINAL_STATUS.md) - وضعیت فاینالی

---

## 🐧 برای Ubuntu/Linux (Automation):

```bash
chmod +x deploy.sh
./deploy.sh
# انتخاب 2 برای Systemd Service
```

---

## ✨ خلاصه:

| OS | دستور |
|----|--------|
| **Windows** | `install.bat` (دوبار کلیک) |
| **Linux** | `bash install.sh` |
| **Mac** | `bash install.sh` |

---

**حالا شروع کن! 🚀**

```bash
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll
# Windows: install.bat
# Linux/Mac: bash install.sh
```

**تمام! در 5 دقیقه آماده است!** ✨
