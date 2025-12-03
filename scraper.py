import timeimport time"""

import logging

import osimport loggingAir Quality Index (AQI) Scraper for Iran

import json

from datetime import datetime, timedeltaimport osScrapes data from https://aqms.doe.ir/A            logger.info("Opening website...")

import pytz

import shutilimport json            try:

import re

from playwright.sync_api import sync_playwrightfrom datetime import datetime, timedelta                page.goto('https://aqms.doe.ir                                        if state_btn:

from config import (

    DATA_DIR, DATA_FILE, BACKUP_DIR, BROWSER_TIMEOUT, PAGE_LOAD_TIMEOUT,import pytz                                            state_btn.click()

    LOG_FILE, LOG_DIR, AQI_MIN, AQI_MAX

)import shutil                                            page.wait_for_timeout(1500)  # Reduced timeout



TEHRAN_TZ = pytz.timezone('Asia/Tehran')from playwright.sync_api import sync_playwright                                            



os.makedirs(DATA_DIR, exist_ok=True)from config import (                                            # Extract AQI

os.makedirs(BACKUP_DIR, exist_ok=True)

os.makedirs(LOG_DIR, exist_ok=True)    DATA_DIR, DATA_FILE, BACKUP_DIR, BROWSER_TIMEOUT, PAGE_LOAD_TIMEOUT,                                            try:



logger = logging.getLogger('AQI_Scraper')    LOG_FILE, LOG_DIR, AQI_MIN, AQI_MAX                                                body_text = page.evaluate('() => document.body.innerText')

logger.setLevel(logging.DEBUG)

)                                            except:

if not logger.handlers:

    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')                                                logger.warning(f"  ! {state}: Could not evaluate body text")

    file_handler.setLevel(logging.DEBUG)

    TEHRAN_TZ = pytz.timezone('Asia/Tehran')                                                continue, timeout=90000, wait_until='load')

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)                page.wait_for_timeout(PAGE_LOAD_TIMEOUT)

    

    formatter = logging.Formatter(os.makedirs(DATA_DIR, exist_ok=True)                

        '[%(asctime)s] %(levelname)s: %(message)s',

        datefmt='%Y-%m-%d %H:%M:%S'os.makedirs(BACKUP_DIR, exist_ok=True)                # Wait for data to load dynamically

    )

    file_handler.setFormatter(formatter)os.makedirs(LOG_DIR, exist_ok=True)                logger.info("Waiting for data to load...")

    console_handler.setFormatter(formatter)

                    try:

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)logger = logging.getLogger('AQI_Scraper')                    page.wait_for_selector('table, [role="table"], .province, [data-province], tr, .data-row', timeout=30000)



logger.setLevel(logging.DEBUG)                    logger.info("Data container found!")

def get_tehran_time():

    return datetime.now(TEHRAN_TZ)                except:



if not logger.handlers:                    logger.warning("Could not wait for specific selector, continuing anyway...")

def backup_data():

    if os.path.exists(DATA_FILE):    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')                    page.wait_for_timeout(5000)ovinces

        timestamp = get_tehran_time().strftime('%Y%m%d_%H%M%S')

        backup_file = os.path.join(BACKUP_DIR, f'aqi_backup_{timestamp}.json')    file_handler.setLevel(logging.DEBUG)"""

        shutil.copy2(DATA_FILE, backup_file)

        logger.debug(f"Backup: {backup_file}")    



    console_handler = logging.StreamHandler()from playwright.sync_api import sync_playwright

def cleanup_old_backups(days=7):

    try:    console_handler.setLevel(logging.INFO)import json

        cutoff_time = time.time() - (days * 86400)

        for f in os.listdir(BACKUP_DIR):    import os

            if f.startswith('aqi_backup_') and f.endswith('.json'):

                path = os.path.join(BACKUP_DIR, f)    formatter = logging.Formatter(from datetime import datetime, timedelta

                if os.path.getmtime(path) < cutoff_time:

                    os.remove(path)        '[%(asctime)s] %(levelname)s: %(message)s',import pytz

                    logger.debug(f"Deleted old backup: {f}")

    except Exception as e:        datefmt='%Y-%m-%d %H:%M:%S'import time

        logger.error(f"Backup cleanup error: {e}")

    )import logging



def save_data(aqi_data):    file_handler.setFormatter(formatter)import shutil

    try:

        backup_data()    console_handler.setFormatter(formatter)from config import DATA_DIR, DATA_FILE, BACKUP_DIR, BROWSER_TIMEOUT, PAGE_LOAD_TIMEOUT

        with open(DATA_FILE, 'w', encoding='utf-8') as f:

            json.dump(aqi_data, f, indent=2, ensure_ascii=False)    

        logger.debug(f"Data saved: {len(aqi_data)} items")

        return True    logger.addHandler(file_handler)# Setup logging

    except Exception as e:

        logger.error(f"Save error: {e}")    logger.addHandler(console_handler)logging.basicConfig(

        return False

    level=logging.INFO,



def load_data():    format='[%(asctime)s] %(message)s',

    try:

        if os.path.exists(DATA_FILE):def get_tehran_time():    datefmt='%Y-%m-%d %H:%M:%S'

            with open(DATA_FILE, 'r', encoding='utf-8') as f:

                return json.load(f)    return datetime.now(TEHRAN_TZ))

    except Exception as e:

        logger.error(f"Load error: {e}")logger = logging.getLogger(__name__)

    return {}





def scrape_aqi_data(attempt=1, max_attempts=1):def backup_data():# Timezone

    logger.info(f"Scraping AQI data (attempt {attempt}/{max_attempts})")

        if os.path.exists(DATA_FILE):TEHRAN_TZ = pytz.timezone('Asia/Tehran')

    try:

        with sync_playwright() as p:        timestamp = get_tehran_time().strftime('%Y%m%d_%H%M%S')

            browser = p.chromium.launch(

                headless=True,        backup_file = os.path.join(BACKUP_DIR, f'aqi_backup_{timestamp}.json')# Ensure directories exist

                args=['--disable-blink-features=AutomationControlled']

            )        shutil.copy2(DATA_FILE, backup_file)os.makedirs(DATA_DIR, exist_ok=True)

            

            page = browser.new_page(        logger.debug(f"Backup: {backup_file}")os.makedirs(BACKUP_DIR, exist_ok=True)

                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

            )

            

            logger.info("Opening website...")

            page.goto('https://aqms.doe.ir/App/', timeout=BROWSER_TIMEOUT, wait_until='load')

            page.wait_for_timeout(PAGE_LOAD_TIMEOUT)def cleanup_old_backups(days=7):def get_tehran_time():

            

            aqi_data = {}    try:    """Get current time in Tehran timezone"""

            

            settings_button = page.query_selector('button.icon-button')        cutoff_time = time.time() - (days * 86400)    return datetime.now(TEHRAN_TZ).isoformat()

            if not settings_button:

                logger.error("Settings button not found")        for f in os.listdir(BACKUP_DIR):

                browser.close()

                return None            if f.startswith('aqi_backup_') and f.endswith('.json'):

            

            settings_button.click()                path = os.path.join(BACKUP_DIR, f)def backup_data():

            page.wait_for_timeout(1000)

                            if os.path.getmtime(path) < cutoff_time:    """Backup current data file"""

            menu_items = page.query_selector_all('mat-menu-item')

            state_options = None                    os.remove(path)    if os.path.exists(DATA_FILE):

            

            for item in menu_items:                    logger.debug(f"Deleted old backup: {f}")        timestamp = datetime.now(TEHRAN_TZ).strftime('%Y%m%d_%H%M%S')

                text = item.text_content().strip()

                if 'انتخاب استان' in text or 'استان' in text:    except Exception as e:        backup_file = os.path.join(BACKUP_DIR, f'aqi_data_{timestamp}.json')

                    item.click()

                    page.wait_for_timeout(1000)        logger.error(f"Backup cleanup error: {e}")        shutil.copy2(DATA_FILE, backup_file)

                    state_options = page.query_selector_all('mat-option')

                    break        logger.info(f"Data backed up to {backup_file}")

            

            if not state_options:        return backup_file

                logger.error("State options not found")

                browser.close()def save_data(aqi_data):    return None

                return None

                try:

            states = []

            for opt in state_options:        backup_data()

                state_text = opt.text_content().strip()

                if state_text and len(state_text) > 1:        with open(DATA_FILE, 'w', encoding='utf-8') as f:def cleanup_old_backups(days=7):

                    states.append(state_text)

                        json.dump(aqi_data, f, indent=2, ensure_ascii=False)    """Delete backups older than N days"""

            logger.info(f"Found {len(states)} states")

                    logger.debug(f"Data saved: {len(aqi_data)} items")    if not os.path.exists(BACKUP_DIR):

            for idx, state in enumerate(states):

                try:        return True        return

                    settings_button = page.query_selector('button.icon-button')

                    if settings_button:    except Exception as e:    

                        settings_button.click()

                        page.wait_for_timeout(500)        logger.error(f"Save error: {e}")    cutoff_time = time.time() - (days * 86400)

                    

                    menu_items = page.query_selector_all('mat-menu-item')        return False    deleted_count = 0

                    for item in menu_items:

                        if 'انتخاب استان' in item.text_content() or 'استان' in item.text_content():    

                            item.click()

                            page.wait_for_timeout(500)    for filename in os.listdir(BACKUP_DIR):

                            break

                    def load_data():        filepath = os.path.join(BACKUP_DIR, filename)

                    state_options = page.query_selector_all('mat-option')

                    for opt in state_options:    try:        if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time:

                        if opt.text_content().strip() == state:

                            opt.click()        if os.path.exists(DATA_FILE):            try:

                            page.wait_for_timeout(1500)

                            break            with open(DATA_FILE, 'r', encoding='utf-8') as f:                os.remove(filepath)

                    

                    body_text = page.evaluate('() => document.body.innerText')                return json.load(f)                deleted_count += 1

                    

                    numbers = re.findall(r'\d{2,3}', body_text)    except Exception as e:            except Exception as e:

                    aqi_value = None

                            logger.error(f"Load error: {e}")                logger.warning(f"Could not delete {filename}: {e}")

                    for num_str in numbers:

                        num = int(num_str)    return {}    

                        if AQI_MIN <= num <= AQI_MAX:

                            aqi_value = num    if deleted_count > 0:

                            break

                            logger.info(f"Cleaned up {deleted_count} old backups")

                    if aqi_value:

                        timestamp = get_tehran_time().isoformat()def scrape_aqi_data(attempt=1, max_attempts=1):

                        aqi_data[state] = {

                            'aqi': aqi_value,    logger.info(f"Scraping AQI data (attempt {attempt}/{max_attempts})")

                            'timestamp': timestamp

                        }    def scrape_aqi_data(attempt=1, max_attempts=1):

                        logger.info(f"✓ {state}: {aqi_value}")

                    else:    try:    """Scrape AQI data from AQMS website"""

                        logger.warning(f"⚠ {state}: AQI not found")

                        with sync_playwright() as p:    logger.info(f"Starting AQI scraper (attempt {attempt}/{max_attempts})...")

                except Exception as e:

                    logger.warning(f"Error processing {state}: {e}")            browser = p.chromium.launch(    logger.info("Target: https://aqms.doe.ir/App/")

                    continue

                            headless=True,    

            browser.close()

                            args=['--disable-blink-features=AutomationControlled']    aqi_data = {}

            if len(aqi_data) >= 20:

                logger.info(f"Success: {len(aqi_data)} provinces collected")            )    

                save_data(aqi_data)

                cleanup_old_backups()                try:

                return aqi_data

            else:            page = browser.new_page(        with sync_playwright() as p:

                logger.error(f"Only {len(aqi_data)} provinces (need 20+)")

                return None                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'            # Launch with additional options for better stability

    

    except Exception as e:            )            browser = p.chromium.launch(

        logger.error(f"Scraping error: {e}")

        return None                            headless=True,



            logger.info("Opening website...")                args=['--disable-blink-features=AutomationControlled']

if __name__ == '__main__':

    result = scrape_aqi_data()            page.goto('https://aqms.doe.ir/App/', timeout=BROWSER_TIMEOUT, wait_until='load')            )

    if result:

        logger.info(f"Collected {len(result)} provinces")            page.wait_for_timeout(PAGE_LOAD_TIMEOUT)            page = browser.new_page(

    else:

        logger.error("Scraping failed")                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


            aqi_data = {}            )

                        

            settings_button = page.query_selector('button.icon-button')            logger.info("Opening website...")

            if not settings_button:            try:

                logger.error("Settings button not found")                page.goto('https://aqms.doe.ir/App/', timeout=90000, wait_until='load')

                browser.close()                page.wait_for_timeout(7000)  # Wait for page to load

                return None                

                            # Wait for data to load dynamically

            settings_button.click()                logger.info("Waiting for data to load...")

            page.wait_for_timeout(1000)                try:

                                page.wait_for_selector('table, [role="table"], .province, [data-province], tr, .data-row', timeout=30000)

            menu_items = page.query_selector_all('mat-menu-item')                    logger.info("Data container found!")

            state_options = None                except:

                                logger.warning("Could not wait for specific selector, continuing anyway...")

            for item in menu_items:                    page.wait_for_timeout(3000)

                text = item.text_content().strip()                    

                if 'انتخاب استان' in text or 'استان' in text:            except Exception as goto_error:

                    item.click()                logger.warning(f"Navigation error: {goto_error}")

                    page.wait_for_timeout(1000)                # Try with different approach

                    state_options = page.query_selector_all('mat-option')                try:

                    break                    page.goto('https://aqms.doe.ir/App/', timeout=90000)

                            except:

            if not state_options:                    pass

                logger.error("State options not found")                page.wait_for_timeout(7000)

                browser.close()            

                return None            logger.info("Scraping province data...")

                        

            states = []            # Try multiple methods to find data

            for opt in state_options:            try:

                state_text = opt.text_content().strip()                # Method 0: Click on settings icon to open province menu

                if state_text and len(state_text) > 1:                logger.info("Looking for settings button...")

                    states.append(state_text)                try:

                                # Look for settings button (gear icon)

            logger.info(f"Found {len(states)} states")                    settings_button = page.query_selector('button.icon-button, button[aria-haspopup="true"]')

                                if settings_button:

            for idx, state in enumerate(states):                        logger.info("Found settings button, clicking...")

                try:                        settings_button.click()

                    settings_button = page.query_selector('button.icon-button')                        page.wait_for_timeout(1000)

                    if settings_button:                        

                        settings_button.click()                        # Now look for "انتخاب استان" button in menu

                        page.wait_for_timeout(500)                        menu_buttons = page.query_selector_all('button[role="menuitem"], button.mat-menu-item')

                                            logger.info(f"Found {len(menu_buttons)} menu items")

                    menu_items = page.query_selector_all('mat-menu-item')                        

                    for item in menu_items:                        prov_button = None

                        if 'انتخاب استان' in item.text_content() or 'استان' in item.text_content():                        for btn in menu_buttons:

                            item.click()                            btn_text = btn.text_content().strip()

                            page.wait_for_timeout(500)                            logger.debug(f"Menu item: {btn_text}")

                            break                            if 'استان' in btn_text:

                                                    prov_button = btn

                    state_options = page.query_selector_all('mat-option')                                logger.info(f"Found province menu: {btn_text}")

                    for opt in state_options:                                break

                        if opt.text_content().strip() == state:                        

                            opt.click()                        if prov_button:

                            page.wait_for_timeout(1500)                            prov_button.click()

                            break                            page.wait_for_timeout(1000)

                                                

                    body_text = page.evaluate('() => document.body.innerText')                            # Get all state options

                                                state_items = page.query_selector_all('button[role="menuitem"]')

                    import re                            logger.info(f"Found {len(state_items)} state options")

                    numbers = re.findall(r'\d{2,3}', body_text)                            

                    aqi_value = None                            states = []

                                                for item in state_items:

                    for num_str in numbers:                                state_name = item.text_content().strip()

                        num = int(num_str)                                # Filter out menu headers and checkboxes text

                        if AQI_MIN <= num <= AQI_MAX:                                if state_name and len(state_name) > 1 and 'استان' not in state_name and 'ایستگاه' not in state_name and 'داده' not in state_name and 'راهنمای' not in state_name and 'درباره' not in state_name:

                            aqi_value = num                                    if state_name not in states:

                            break                                        states.append(state_name)

                                                            logger.debug(f"State: {state_name}")

                    if aqi_value:                            

                        timestamp = get_tehran_time().isoformat()                            if states:

                        aqi_data[state] = {                                logger.info(f"Total states: {len(states)}")

                            'aqi': aqi_value,                                

                            'timestamp': timestamp                                # For each state, click and get AQI

                        }                                for idx, state in enumerate(states):  # Changed from states[:5]

                        logger.info(f"✓ {state}: {aqi_value}")                                    try:

                    else:                                        logger.info(f"Processing: {state} ({idx+1}/{len(states)})")

                        logger.warning(f"⚠ {state}: AQI not found")                                        

                                                        # Reopen settings menu

                except Exception as e:                                        settings_button = page.query_selector('button.icon-button, button[aria-haspopup="true"]')

                    logger.warning(f"Error processing {state}: {e}")                                        if settings_button and idx > 0:

                    continue                                            settings_button.click()

                                                        page.wait_for_timeout(500)

            browser.close()                                            

                                                        prov_button = None

            if len(aqi_data) >= 20:                                            for btn in page.query_selector_all('button[role="menuitem"], button.mat-menu-item'):

                logger.info(f"Success: {len(aqi_data)} provinces collected")                                                if 'استان' in btn.text_content():

                save_data(aqi_data)                                                    prov_button = btn

                cleanup_old_backups()                                                    break

                return aqi_data                                            

            else:                                            if prov_button:

                logger.error(f"Only {len(aqi_data)} provinces (need 20+)")                                                prov_button.click()

                return None                                                page.wait_for_timeout(500)

                                            

    except Exception as e:                                        # Click state

        logger.error(f"Scraping error: {e}")                                        state_items = page.query_selector_all('button[role="menuitem"]')

        return None                                        state_btn = None

                                        for item in state_items:

                                            if state in item.text_content():

if __name__ == '__main__':                                                state_btn = item

    result = scrape_aqi_data()                                                break

    if result:                                        

        logger.info(f"Collected {len(result)} provinces")                                        if state_btn:

    else:                                            state_btn.click()

        logger.error("Scraping failed")                                            page.wait_for_timeout(2000)

                                            
                                            # Extract AQI from rendered content
                                            try:
                                                # Try to get from visible text in gauge
                                                text_spans = page.query_selector_all('span, div, p, text')
                                                aqi_value = None
                                                
                                                for span in text_spans:
                                                    try:
                                                        text = span.text_content().strip()
                                                        if text and text.isdigit() and 50 <= int(text) <= 500:
                                                            aqi_value = int(text)
                                                            break
                                                    except:
                                                        pass
                                                
                                                # If not found in spans, try page text
                                                if not aqi_value:
                                                    body_text = page.evaluate('() => document.body.innerText')
                                                    
                                                    import re
                                                    numbers = re.findall(r'\d{2,3}', body_text)
                                                    if numbers:
                                                        for num_str in sorted(numbers, key=int, reverse=True):
                                                            num = int(num_str)
                                                            if 50 <= num <= 500:
                                                                aqi_value = num
                                                                break
                                                
                                                if aqi_value:
                                                    aqi_data[state] = {
                                                        'aqi': aqi_value,
                                                        'timestamp': get_tehran_time()
                                                    }
                                                    logger.info(f"  ✓ {state}: {aqi_value}")
                                                else:
                                                    logger.warning(f"  ✗ {state}: Could not extract AQI value")
                                            except Exception as extract_error:
                                                logger.warning(f"  ✗ {state}: Error extracting: {extract_error}")
                                    except Exception as e:
                                        logger.warning(f"Error processing {state}: {e}")
                                        continue
                        else:
                            logger.warning("Province menu item not found")
                    else:
                        logger.warning("Settings button not found")
                
                except Exception as e:
                    logger.warning(f"Settings menu error: {e}")
                    import traceback
                    logger.debug(traceback.format_exc())
                
                # If no data from states, try Method 1: Extract from JavaScript/API
                if not aqi_data:
                    logger.info("State method failed, attempting JavaScript extraction...")
                try:
                    js_result = page.evaluate('''
                        () => {
                            const data = {};
                            
                            // Try window variables
                            if (window.data) {
                                console.log('Found window.data');
                                return window.data;
                            }
                            if (window.__data) {
                                console.log('Found window.__data');
                                return window.__data;
                            }
                            if (window.aqi_data) {
                                console.log('Found window.aqi_data');
                                return window.aqi_data;
                            }
                            
                            // Try to find data in DOM
                            // Look for any element with text that looks like AQI
                            const allElements = document.querySelectorAll('*');
                            for (let el of allElements) {
                                const text = el.textContent;
                                if (text && text.includes('تهران') || text.includes('Tehran')) {
                                    console.log('Found potential data element:', el.outerHTML.substring(0, 100));
                                }
                            }
                            
                            // Try common selectors for data
                            const tables = document.querySelectorAll('table');
                            if (tables.length > 0) {
                                console.log('Found tables:', tables.length);
                                tables.forEach((table, idx) => {
                                    const rows = table.querySelectorAll('tr');
                                    console.log('Table', idx, 'has', rows.length, 'rows');
                                    rows.forEach((row, ridx) => {
                                        const cells = row.querySelectorAll('td, th');
                                        if (cells.length >= 2) {
                                            const province = cells[0].textContent.trim();
                                            const aqi = cells[1].textContent.trim();
                                            if (province && aqi && province.length > 1) {
                                                data[province] = aqi;
                                            }
                                        }
                                    });
                                });
                            }
                            
                            return data;
                        }
                    ''')
                    
                    if js_result and len(js_result) > 0:
                        logger.info(f"JavaScript extraction found {len(js_result)} items")
                        for province, aqi_val in js_result.items():
                            try:
                                aqi_numbers = ''.join(filter(str.isdigit, str(aqi_val)))
                                if aqi_numbers:
                                    aqi = int(aqi_numbers)
                                    aqi_data[province] = {
                                        'aqi': aqi,
                                        'timestamp': get_tehran_time()
                                    }
                                    logger.info(f"  ✓ {province}: {aqi}")
                            except Exception as e:
                                logger.debug(f"Error processing {province}: {e}")
                    else:
                        logger.info("JavaScript extraction returned empty")
                        
                except Exception as js_error:
                    logger.warning(f"JavaScript extraction failed: {js_error}")
                
                # Method 2: If JS failed, try DOM parsing
                if not aqi_data:
                    logger.info("Trying DOM parsing...")
                    rows = page.query_selector_all('table tr, [role="row"], .row, .province-row, tbody tr')
                    logger.info(f"Found {len(rows)} potential data rows")
                    
                    if rows:
                        for i, row in enumerate(rows):
                            try:
                                text = row.text_content().strip()
                                if text and len(text) > 2:
                                    cells = row.query_selector_all('td, span, div')
                                    
                                    if len(cells) >= 2:
                                        province = cells[0].text_content().strip()
                                        aqi_text = cells[1].text_content().strip() if len(cells) > 1 else ""
                                        
                                        aqi_numbers = ''.join(filter(str.isdigit, aqi_text))
                                        if province and aqi_numbers and len(province) > 1:
                                            aqi = int(aqi_numbers)
                                            if 0 <= aqi <= 500:  # Valid AQI range
                                                aqi_data[province] = {
                                                    'aqi': aqi,
                                                    'timestamp': get_tehran_time()
                                                }
                                                logger.info(f"  ✓ {province}: {aqi}")
                            except Exception as e:
                                logger.debug(f"Error parsing row {i}: {e}")
                                continue
                    else:
                        logger.warning("No rows found, page may not be fully loaded")
                        
                        # Try extracting from visible text (gauge data)
                        logger.info("Attempting to extract from page text...")
                        body_text = page.evaluate('() => document.body.innerText')
                        logger.info(f"Body text length: {len(body_text)}")
                        
                        # Look for province name "تهران" and AQI numbers
                        if 'تهران' in body_text or 'Tehran' in body_text:
                            logger.info("Found province reference in page text")
                            
                            # Try to find gauge data
                            # Look for high numbers that could be AQI
                            import re
                            numbers = re.findall(r'\d{2,3}', body_text)
                            if numbers:
                                logger.info(f"Found numbers in text: {numbers}")
                                # Take the largest reasonable AQI value (highest from gauges)
                                valid_aqi = None
                                for num_str in sorted(numbers, key=int, reverse=True):
                                    num = int(num_str)
                                    # AQI should be in reasonable range: 0-500
                                    # Skip time-related numbers (hours, minutes)
                                    if 50 <= num <= 500:
                                        valid_aqi = num
                                        break
                                
                                if valid_aqi:
                                    aqi_data['تهران'] = {
                                        'aqi': valid_aqi,
                                        'timestamp': get_tehran_time()
                                    }
                                    logger.info(f"  ✓ تهران: {valid_aqi}")
                        
                        # Save HTML for debugging
                        html_file = os.path.join(DATA_DIR, 'page_debug.html')
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(page.content())
                        logger.info(f"Page HTML saved to {html_file}")
                    
            except Exception as e:
                logger.error(f"Error during scraping: {e}")
                import traceback
                logger.error(traceback.format_exc())
            
            browser.close()
    
    except Exception as e:
        logger.error(f"Scraper error: {e}")
        return None
    
    if aqi_data:
        logger.info(f"Successfully scraped {len(aqi_data)} provinces")
        return aqi_data
    else:
        logger.warning("No data collected")
        return None


def save_data(aqi_data):
    """Save AQI data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(aqi_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Data saved to {DATA_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return False


def load_data():
    """Load AQI data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
    return {}


if __name__ == '__main__':
    # Scrape and save data
    data = scrape_aqi_data()
    if data:
        save_data(data)
        logger.info("Scraping completed successfully")
    else:
        logger.error("Scraping failed - no data collected")
