import time
import logging
import os
import requests
from datetime import datetime, timedelta
import pytz
from config import (
    SCHEDULE_INTERVAL_MINUTES, MAX_RETRIES, RETRY_DELAY_MINUTES,
    LOG_FILE, LOG_DIR, DATA_DIR, BACKUP_DIR
)
from scraper import scrape_aqi_data, get_tehran_time

TEHRAN_TZ = pytz.timezone('Asia/Tehran')

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

lg = logging.getLogger('AQI_Scheduler')
lg.setLevel(logging.DEBUG)

if not lg.handlers:
    fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    
    lg.addHandler(fh)
    lg.addHandler(ch)

lt_time = None
cf = 0
retry_times = {}


def check_site_health():
    """بررسی سایت آیا UP است یا DOWN"""
    try:
        response = requests.get('https://aqms.doe.ir/App/', timeout=5)
        return response.status_code == 200
    except:
        return False


def schedule_scraper():
    global lt_time, cf, retry_times
    
    lg.info("="*80)
    lg.info("🚀 AQI Scheduler started")
    lg.info(f"📅 Schedule Interval: {SCHEDULE_INTERVAL_MINUTES} minutes")
    lg.info(f"🔄 Retry Logic: 3 attempts with 10-min intervals")
    lg.info(f"🌍 Timezone: Asia/Tehran (UTC+03:30)")
    lg.info("="*80)
    
    while True:
        try:
            now = get_tehran_time()
            
            # تعیین اگر باید اجرا شود
            should_scrape = False
            if lt_time is None:
                should_scrape = True
            else:
                time_diff = (now - lt_time).total_seconds() / 60
                should_scrape = time_diff >= SCHEDULE_INTERVAL_MINUTES
            
            if should_scrape:
                lg.info("="*80)
                lg.info(f"⏰ [Main] Starting main scrape at {now.isoformat()}")
                lg.info("="*80)
                
                # بررسی سایت
                site_healthy = check_site_health()
                if not site_healthy:
                    lg.warning(f"🚨 [Main] Site is DOWN at {now.isoformat()}")
                else:
                    lg.info(f"✅ [Main] Site is UP at {now.isoformat()}")
                
                success = False
                for attempt in range(1, MAX_RETRIES + 1):
                    attempt_time = get_tehran_time()
                    
                    if attempt == 1:
                        lg.info(f"📍 [Main] Attempt {attempt} at {attempt_time.isoformat()}")
                    else:
                        lg.info(f"🔄 [Retry] Attempt {attempt} at {attempt_time.isoformat()}")
                    
                    # تلاش برای جمع‌آوری داده
                    result = scrape_aqi_data(attempt=attempt, max_attempts=MAX_RETRIES)
                    
                    if result and len(result) >= 20:
                        lg.info(f"✅ [Main] Success: {len(result)} states collected at {attempt_time.isoformat()}")
                        success = True
                        cf = 0
                        lt_time = now
                        break
                    else:
                        if attempt < MAX_RETRIES:
                            # زمان retry
                            retry_wait = RETRY_DELAY_MINUTES * 60
                            next_retry = attempt_time + timedelta(minutes=RETRY_DELAY_MINUTES)
                            lg.warning(f"⚠️  [Retry] Attempt {attempt} failed. Retrying in {RETRY_DELAY_MINUTES} minutes at {next_retry.isoformat()}")
                            
                            # خواب کردن و دوباره بررسی
                            time.sleep(retry_wait)
                        else:
                            lg.error(f"❌ [Retry] All {MAX_RETRIES} attempts failed at {attempt_time.isoformat()}")
                
                if not success:
                    cf += 1
                    lg.error(f"🔴 Consecutive failures: {cf}/{3}")
                    
                    if cf >= 3:
                        lg.critical(f"⚠️⚠️⚠️ {cf} consecutive failures! Site appears to be DOWN. Will retry at next scheduled time.")
            
            # خواب 60 ثانیه‌ای برای بررسی‌های تناوبی
            time.sleep(60)
        
        except KeyboardInterrupt:
            lg.info("🛑 Scheduler stopped (Ctrl+C)")
            break
        except Exception as e:
            lg.error(f"💥 Error: {e}", exc_info=True)
            time.sleep(60)



if __name__ == '__main__':
    schedule_scraper()
