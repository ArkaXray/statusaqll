# 🔄 Scheduler + API Simultaneous Running

## ✅ مشکل حل شد!

اکنون Scheduler و API می‌توانند **همزمان** اجرا شوند! 🎉

---

## 📋 منوی جدید:

```
1. Start Scheduler (auto collect every 30 minutes)
2. Start API Server (port 5000)
3. Start Both (Scheduler + API)    ⭐ جدید!
4. Manual Collection
5. View Logs (last 50)
6. View Stats
0. Exit
```

---

## 🚀 استفاده:

### **Option 1: فقط Scheduler**

```
Choose: 1
```

✅ جمع‌آوری هر 30 دقیقه
❌ API کار نمی‌کند

### **Option 2: فقط API**

```
Choose: 2
```

❌ جمع‌آوری کار نمی‌کند
✅ API در port 5000

### **Option 3: هر دو (بهترین!) ⭐**

```
Choose: 3
```

✅ جمع‌آوری هر 30 دقیقه
✅ API در port 5000
✅ هردو بصورت **background** اجرا می‌شوند

---

## 💡 کاری که تغییر کرد:

### قبل:

```
Choose 1 → Scheduler شروع می‌شود → منتظر اتمام
           API مسدود است
```

### بعد:

```
Choose 3 → Scheduler شروع (background)
        → API شروع (background)
        → هردو همزمان کار می‌کنند!
        → می‌تونید منوی رو دوباره ببینید
```

---

## 🎯 مثال کامل:

```
📋 Menu:
  1. Start Scheduler
  2. Start API Server
  3. Start Both (Scheduler + API)
  ...

Choose: 3

▶️  Starting Scheduler + API (Background)...

✅ Scheduler started (PID: 12345)
✅ API started (PID: 12346)

✅ Both services are running in background!

You can:
  - View logs: option 5
  - Check stats: option 6
  - Visit API: http://localhost:5000/api/aqi
  - Press Ctrl+C to stop all

```

---

## 📊 ویژگی‌های جدید:

✅ **همزمان اجرا** - Scheduler + API دستور تحت واحد  
✅ **Background** - هر دو بصورت خلفی اجرا می‌شوند  
✅ **Non-blocking** - منوی دوباره ظاهر می‌شود  
✅ **Ctrl+C** - همه سرویس‌ها بسته می‌شوند  
✅ **Log viewing** - حالا کار می‌کند  
✅ **Stats** - نمایش آمار بهتر

---

## 🔧 دستورات مفید:

```bash
# شروع منو
python3 run.py

# یا مستقیم
python3 scheduler.py      # فقط Scheduler
python3 api.py            # فقط API
```

---

## 🌐 بعد از اجرای Option 3:

```
# API Endpoints:
http://localhost:5000/api/health
http://localhost:5000/api/aqi
http://localhost:5000/api/aqi/Tehran
http://localhost:5000/api/stats

# Scheduler:
جمع‌آوری هر 30 دقیقه
لاگ‌های دقیق در logs/scraper.log
```

---

## 📝 نکات:

✅ Option 3 برای production بهترین است  
✅ هردو service مستقل هستند  
✅ Ctrl+C هردو را بسته می‌کند  
✅ Log viewing دستور 5 کار می‌کند

---

**حالا بدون مشکل کار می‌کند!** ✨
