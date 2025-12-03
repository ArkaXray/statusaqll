# 🔧 Troubleshooting & Common Issues

## ❌ مشکل: Playwright Browsers Not Installed

**علامت:**

```
Executable doesn't exist at /root/.cache/ms-playwright/chromium-1091/chrome-linux/chrome
```

### حل:

**1. دستی نصب کنید:**

```bash
python3 -m playwright install chromium
```

**2. یا برای تمام browsers:**

```bash
python3 -m playwright install
```

**3. اگر دوباره خطا داد:**

```bash
# پاک‌سازی و دوباره نصب
rm -rf ~/.cache/ms-playwright/
python3 -m playwright install chromium
```

---

## ❌ مشکل: Missing System Dependencies (Linux)

**علامت:**

```
Error: Executable doesn't exist
```

### حل:

**Ubuntu/Debian:**

```bash
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
```

**سپس:**

```bash
python3 -m playwright install chromium
```

---

## ❌ مشکل: "Python not found"

### حل:

**Linux:**

```bash
sudo apt-get install python3 python3-pip
```

**Mac:**

```bash
brew install python3
```

**Windows:**

- دانلود از: https://www.python.org/downloads/
- نصب با checkbox "Add Python to PATH"

---

## ❌ مشکل: "pip: command not found"

### حل:

**Linux:**

```bash
sudo apt-get install python3-pip
```

**Mac:**

```bash
python3 -m ensurepip --upgrade
```

**Windows:**

```batch
python -m pip install --upgrade pip
```

---

## ❌ مشکل: "Port 5000 already in use"

### حل:

**Mac/Linux:**

```bash
# بیابید کی استفاده می‌کند
lsof -i :5000

# کشتن process
kill -9 <PID>

# یا
pkill -f "api.py"
```

**Windows:**

```batch
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## ❌ مشکل: "Module not found"

**علامت:**

```
ModuleNotFoundError: No module named 'playwright'
```

### حل:

```bash
# دوباره نصب
pip install -r requirements.txt

# یا
pip3 install -r requirements.txt
```

---

## ❌ مشکل: "Permission denied" (Linux)

### حل:

```bash
chmod +x install.sh
chmod +x deploy.sh
chmod +x run.py

bash install.sh
```

---

## ❌ مشکل: Install Script مشکل دارد

### حل:

**دستی نصب:**

```bash
# 1. Clone
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 2. نصب Python packages
pip3 install -r requirements.txt

# 3. نصب Playwright
python3 -m playwright install chromium

# 4. نصب System dependencies (اگر لازم باشد)
sudo apt-get install libgconf-2-4 libx11-xcb1 ...

# 5. اجرا
python3 run.py
```

---

## ❌ مشکل: Scraper کار نمی‌کند

**علامت:**

```
Scraping error: ...
```

### حل:

**1. بررسی Site:**

```bash
curl https://aqms.doe.ir/App/
```

**2. بررسی Internet:**

```bash
ping google.com
```

**3. دستی تست:**

```bash
python3 -c "from scraper import scrape_aqi_data; print(scrape_aqi_data())"
```

**4. بررسی لاگ:**

```bash
tail -f logs/scraper.log
```

---

## ❌ مشکل: API کار نمی‌کند

### حل:

**1. بررسی port:**

```bash
netstat -tlnp | grep 5000
```

**2. دستی اجرا:**

```bash
python3 api.py
```

**3. تست:**

```bash
curl http://localhost:5000/api/health
```

---

## ✅ راهنمای Step-by-Step نصب کامل

```bash
# 1. نیازمندی‌های سیستم (اگر نیاز باشد)
sudo apt-get update
sudo apt-get install -y python3 python3-pip git

# 2. Clone
git clone https://github.com/ArkaXray/statusaqll.git
cd statusaqll

# 3. نصب Python packages
pip3 install -r requirements.txt

# 4. نصب Playwright (اهم!)
python3 -m playwright install chromium

# 5. اجرا
python3 run.py
```

---

## 📞 اگر هنوز کار نکند:

**آنلاین بررسی کنید:**

- Playwright: https://playwright.dev/python/docs/intro
- Playwright CI: https://playwright.dev/python/docs/ci

**لاگ‌ها بررسی کنید:**

```bash
tail -f logs/scraper.log
```

**دستور verbose استفاده کنید:**

```bash
python3 -m playwright install chromium --verbose
```

---

## ✨ نکات مهم:

✅ **Playwright MUST be installed properly**  
✅ **System dependencies لازم است (Linux)**  
✅ **Internet connection ضروری است**  
✅ **Port 5000 آزاد بودن لازم است**  
✅ **Sufficient disk space (300MB+ برای Playwright)**

---

**اگر مشکل حل نشد - لاگ‌های کامل را بررسی کنید!** 🔍
