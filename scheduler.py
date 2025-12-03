import time
import logging
import os
from datetime import datetime
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

logger = logging.getLogger('AQI_Scheduler')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

last_scrape_time = None
consecutive_failures = 0


def schedule_scraper():
    global last_scrape_time, consecutive_failures
    
    logger.info("="*70)
    logger.info("AQI Scheduler شروع شد")
    logger.info(f"فاصله: {SCHEDULE_INTERVAL_MINUTES} دقیقه")
    logger.info(f"منطقه زمانی: Asia/Tehran (UTC+03:30)")
    logger.info("="*70)
    
    while True:
        try:
            now = get_tehran_time()
            
            if last_scrape_time is None:
                should_scrape = True
            else:
                time_diff = (now - last_scrape_time).total_seconds() / 60
                should_scrape = time_diff >= SCHEDULE_INTERVAL_MINUTES
            
            if should_scrape:
                logger.info(f"شروع دریافت AQI در {now.isoformat()}")
                
                success = False
                for attempt in range(1, MAX_RETRIES + 1):
                    logger.debug(f"تلاش {attempt}/{MAX_RETRIES}")
                    
                    result = scrape_aqi_data(attempt=attempt, max_attempts=MAX_RETRIES)
                    
                    if result and len(result) >= 20:
                        logger.info(f"✓ موفق: {len(result)} استان دریافت شد")
                        success = True
                        consecutive_failures = 0
                        last_scrape_time = now
                        break
                    else:
                        if attempt < MAX_RETRIES:
                            wait_time = RETRY_DELAY_MINUTES * 60
                            logger.warning(
                                f"⚠ تلاش {attempt} ناموفق، "
                                f"تلاش مجدد در {RETRY_DELAY_MINUTES} دقیقه..."
                            )
                            time.sleep(wait_time)
                        else:
                            logger.error(f"✗ تمام تلاش‌ها ناموفق شد")
                
                if not success:
                    consecutive_failures += 1
                    logger.error(f"شمارنده ناموفقیت پی‌درپی: {consecutive_failures}")
                    
                    if consecutive_failures >= 3:
                        logger.error(
                            f"⚠⚠⚠ {consecutive_failures} ناموفقیت پی‌درپی! "
                            f"بررسی سرور یا اینترنت لازم است"
                        )
            
            time.sleep(60)
        
        except KeyboardInterrupt:
            logger.info("Scheduler متوقف شد (Ctrl+C)")
            break
        except Exception as e:
            logger.error(f"خطا در scheduler: {str(e)}", exc_info=True)
            time.sleep(60)


if __name__ == '__main__':
    schedule_scraper()
