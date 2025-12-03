# 🎯 Playwright Browsers - راهنمای نصب

## ⚠️ مشکل: Playwright Browsers یافت نشد

اگر این خطا دیدید:

```
Executable doesn't exist at ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome
```

## ✅ حل فوری:

### **Option 1: اسکریپ Fix (بهترین)**

```bash
chmod +x fix-playwright.sh
./fix-playwright.sh
```

این اسکریپت:

- ✅ حذف cache
- ✅ نصب system dependencies
- ✅ نصب Playwright browsers

### **Option 2: دستی**

```bash
# Step 1: نصب system dependencies
sudo apt-get update
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

# Step 2: نصب Playwright
python3 -m playwright install chromium

# Step 3: نصب تمام browsers (اختیاری)
python3 -m playwright install
```

### **Option 3: حذف Cache و دوباره نصب**

```bash
# حذف cache
rm -rf ~/.cache/ms-playwright/

# نصب دوباره
python3 -m playwright install chromium

# یا
python3 -m playwright install chromium --verbose
```

---

## 🔍 بررسی:

```bash
# تست Playwright
python3 -c "from playwright.sync_api import sync_playwright; print('✓ Playwright working')"

# تست scraper
python3 -c "from scraper import scrape_aqi_data; print('✓ Scraper ready')"
```

---

## 🖥️ سیستم‌های مختلف:

### **Ubuntu/Debian:**

```bash
sudo apt-get install -y libgconf-2-4 libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xfixes0 libxdamage1 libxfixes3 libxrandr2 libxss1 libxtst6 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libasound2
python3 -m playwright install chromium
```

### **CentOS/RHEL:**

```bash
sudo yum install -y https://packages.microsoft.com/rhel/7/prod/Packages/microsoft-edge-stable-*.rpm
python3 -m playwright install chromium
```

### **Fedora:**

```bash
sudo dnf install -y chromium
python3 -m playwright install chromium
```

### **Mac:**

```bash
# Playwright معمولا خودکار کار می‌کند
python3 -m playwright install chromium
```

### **Windows:**

```batch
REM Playwright معمولا خودکار کار می‌کند
python -m playwright install chromium

REM یا double-click install.bat
```

---

## 📝 توصیه‌ها:

✅ **شروع با `bash install.sh`** - تمام چیز خودکار است  
✅ **اگر مشکل داشتید** - `bash fix-playwright.sh` اجرا کنید  
✅ **بررسی TROUBLESHOOTING.md** - راهنمای مفصل  
✅ **Internet شما کافی است** - ~300MB برای download

---

## 🚀 بعد از حل:

```bash
# اجرا کنید:
python3 run.py

# یا مستقیم:
python3 scheduler.py
python3 api.py
```

---

**اگر مشکل حل نشد، README-ها بررسی کنید!** 📖
