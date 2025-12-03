import time
import logging
import os
import json
import re
import shutil
from datetime import datetime, timedelta

import pytz
from playwright.sync_api import sync_playwright

from config import (
    DATA_DIR, DATA_FILE, BACKUP_DIR, BROWSER_TIMEOUT, PAGE_LOAD_TIMEOUT,
    LOG_FILE, LOG_DIR, AQI_MIN, AQI_MAX
)

TEHRAN_TZ = pytz.timezone('Asia/Tehran')

# ایجاد دایرکتوری‌های مورد نیاز
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# تنظیمات لاگینگ
logger = logging.getLogger('AQI_Scraper')
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # File handler
    fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', 
                          datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    
    logger.addHandler(fh)
    logger.addHandler(ch)


def get_tehran_time():
    """Get current time in Tehran timezone"""
    return datetime.now(TEHRAN_TZ)


def backup_data():
    """Backup current data file"""
    if os.path.exists(DATA_FILE):
        ts = get_tehran_time().strftime('%Y%m%d_%H%M%S')
        bk = os.path.join(BACKUP_DIR, f'aqi_backup_{ts}.json')
        shutil.copy2(DATA_FILE, bk)
        logger.debug(f"Backup: {bk}")
        return bk
    return None


def cleanup_old_backups(days=7):
    """Delete backups older than N days"""
    try:
        cutoff_time = time.time() - (days * 86400)
        deleted_count = 0
        
        for f in os.listdir(BACKUP_DIR):
            if f.startswith('aqi_backup_') and f.endswith('.json'):
                p = os.path.join(BACKUP_DIR, f)
                if os.path.getmtime(p) < cutoff_time:
                    os.remove(p)
                    logger.debug(f"Deleted: {f}")
                    deleted_count += 1
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old backups")
            
    except Exception as e:
        logger.error(f"Cleanup error: {e}")


def save_data(aqi_data):
    """Save AQI data to JSON file"""
    try:
        backup_data()
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(aqi_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved: {len(aqi_data)} items to {DATA_FILE}")
        return True
    except Exception as e:
        logger.error(f"Save error: {e}")
        return False


def load_data():
    """Load AQI data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Load error: {e}")
    return {}


def scrape_aqi_data(attempt=1, max_attempts=3):
    """Scrape AQI data from AQMS website"""
    logger.info(f"Scraping (attempt {attempt}/{max_attempts})")
    
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            page = browser.new_page(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            logger.info("Opening website...")
            page.goto('https://aqms.doe.ir/App/', timeout=BROWSER_TIMEOUT, wait_until='load')
            page.wait_for_timeout(PAGE_LOAD_TIMEOUT)
            
            aqi_data = {}
            
            # Find settings button
            settings_button = page.query_selector('button.icon-button, button[aria-haspopup="true"]')
            if not settings_button:
                logger.error("Settings button not found")
                browser.close()
                return None
            
            settings_button.click()
            page.wait_for_timeout(1000)
            
            # Find menu items
            menu_items = page.query_selector_all('mat-menu-item, button[role="menuitem"]')
            state_options = None
            
            for item in menu_items:
                text = item.text_content().strip()
                if 'انتخاب استان' in text or 'استان' in text:
                    item.click()
                    page.wait_for_timeout(1000)
                    state_options = page.query_selector_all('mat-option, button[role="menuitem"]')
                    break
            
            if not state_options:
                logger.error("State options not found")
                browser.close()
                return None
            
            # Extract state names
            states = []
            for opt in state_options:
                state_text = opt.text_content().strip()
                # Filter out menu headers
                if (state_text and len(state_text) > 1 and 
                    'استان' not in state_text and 
                    'ایستگاه' not in state_text and 
                    'داده' not in state_text and 
                    'راهنمای' not in state_text and 
                    'درباره' not in state_text):
                    states.append(state_text)
            
            logger.info(f"Found {len(states)} states")
            
            if not states:
                logger.error("No valid states found")
                browser.close()
                return None
            
            # Process each state
            for idx, state in enumerate(states):
                try:
                    logger.info(f"Processing: {state} ({idx+1}/{len(states)})")
                    
                    # Reopen settings menu for each state after the first one
                    if idx > 0:
                        settings_button = page.query_selector('button.icon-button, button[aria-haspopup="true"]')
                        if settings_button:
                            settings_button.click()
                            page.wait_for_timeout(500)
                    
                    # Find and click province selection
                    menu_items = page.query_selector_all('mat-menu-item, button[role="menuitem"]')
                    for item in menu_items:
                        if 'انتخاب استان' in item.text_content() or 'استان' in item.text_content():
                            item.click()
                            page.wait_for_timeout(500)
                            break
                    
                    # Find and click the specific state
                    state_options = page.query_selector_all('mat-option, button[role="menuitem"]')
                    state_clicked = False
                    for opt in state_options:
                        if opt.text_content().strip() == state:
                            opt.click()
                            page.wait_for_timeout(2000)  # Wait for data to load
                            state_clicked = True
                            break
                    
                    if not state_clicked:
                        logger.warning(f"Could not click state: {state}")
                        continue
                    
                    # Wait for data to load
                    logger.info(f"Waiting for data to load for {state}...")
                    try:
                        page.wait_for_selector('table, [role="table"], .province, [data-province], tr, .data-row', 
                                             timeout=30000)
                        logger.info("Data container found!")
                    except:
                        logger.warning("Could not wait for specific selector, continuing anyway...")
                        page.wait_for_timeout(3000)
                    
                    # Extract AQI from page
                    try:
                        # Try to extract from gauge elements
                        gauge_elements = page.query_selector_all('span, div, p, text, .aqi-value, .value, .gauge-value')
                        aqi_value = None
                        
                        for element in gauge_elements:
                            try:
                                text = element.text_content().strip()
                                if text and text.isdigit():
                                    num = int(text)
                                    if AQI_MIN <= num <= AQI_MAX:
                                        aqi_value = num
                                        break
                            except:
                                pass
                        
                        # If not found, try page text
                        if not aqi_value:
                            body_text = page.evaluate('() => document.body.innerText')
                            numbers = re.findall(r'\d{2,3}', body_text)
                            
                            for num_str in numbers:
                                num = int(num_str)
                                if AQI_MIN <= num <= AQI_MAX:
                                    aqi_value = num
                                    break
                        
                        if aqi_value:
                            timestamp = get_tehran_time().isoformat()
                            aqi_data[state] = {
                                'aqi': aqi_value,
                                'timestamp': timestamp
                            }
                            logger.info(f"✓ {state}: {aqi_value}")
                        else:
                            logger.warning(f"⚠ {state}: AQI not found")
                            
                    except Exception as extract_error:
                        logger.warning(f"Error extracting AQI for {state}: {extract_error}")
                        
                except Exception as e:
                    logger.warning(f"Error processing {state}: {e}")
                    continue
            
            browser.close()
            
            if len(aqi_data) >= 5:  # Reduced threshold for testing
                logger.info(f"Success: {len(aqi_data)} states collected")
                save_data(aqi_data)
                cleanup_old_backups()
                return aqi_data
            else:
                logger.error(f"Only {len(aqi_data)} states collected (need at least 5)")
                return None
                
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Retry logic
        if attempt < max_attempts:
            logger.info(f"Retrying... (attempt {attempt+1}/{max_attempts})")
            time.sleep(5)
            return scrape_aqi_data(attempt + 1, max_attempts)
        else:
            return None


def main():
    """Main function to run the scraper"""
    logger.info("=" * 50)
    logger.info("Starting AQI Scraper")
    logger.info("=" * 50)
    
    # Load existing data
    existing_data = load_data()
    if existing_data:
        logger.info(f"Loaded {len(existing_data)} existing records")
    
    # Scrape new data
    result = scrape_aqi_data()
    
    if result:
        logger.info(f"Successfully collected {len(result)} provinces")
        
        # Merge with existing data
        if existing_data:
            existing_data.update(result)
            final_data = existing_data
        else:
            final_data = result
            
        # Save final data
        if save_data(final_data):
            logger.info(f"Total records saved: {len(final_data)}")
        else:
            logger.error("Failed to save data")
    else:
        logger.error("Scraping failed - no data collected")
        if existing_data:
            logger.info(f"Using existing data with {len(existing_data)} records")
    
    logger.info("=" * 50)
    logger.info("AQI Scraper finished")
    logger.info("=" * 50)


if __name__ == '__main__':
    main()