#!/usr/bin/env python3#!/usr/bin/env python3

""""""

AQI Iran - Service Starter (Non-Interactive)AQI Iran - Service Starter (Non-Interactive)

برای استفاده در systemd serviceبرای استفاده در systemd service

""""""



import sysimport sys

import osimport os

import subprocessimport subprocess

import timeimport time

import signalimport signal

import loggingimport logging

import threadingfrom datetime import datetime

from datetime import datetimeimport pytz

import pytz

TEHRAN_TZ = pytz.timezone('Asia/Tehran')

TEHRAN_TZ = pytz.timezone('Asia/Tehran')LOG_FILE = os.path.expanduser('~/.aqi-service.log')

LOG_FILE = os.path.expanduser('~/.aqi-service.log')

# Setup logging

# Setup logginglogging.basicConfig(

logging.basicConfig(    level=logging.DEBUG,

    level=logging.DEBUG,    format='[%(asctime)s] %(levelname)s: %(message)s',

    format='[%(asctime)s] %(levelname)s: %(message)s',    datefmt='%Y-%m-%d %H:%M:%S',

    datefmt='%Y-%m-%d %H:%M:%S',    handlers=[

    handlers=[        logging.FileHandler(LOG_FILE, encoding='utf-8'),

        logging.FileHandler(LOG_FILE, encoding='utf-8'),        logging.StreamHandler()

        logging.StreamHandler()    ]

    ])

)logger = logging.getLogger('AQI-Service')

logger = logging.getLogger('AQI-Service')

# برای ذخیره processes

# برای ذخیره processesprocesses = {

processes = {    'scheduler': None,

    'scheduler': None,    'api': None

    'api': None}

}



def signal_handler(sig, frame):

def signal_handler(sig, frame):    """مدیریت Ctrl+C"""

    """مدیریت Ctrl+C"""    log_message("🛑 Shutting down...")

    logger.info("🛑 Shutting down...")    stop_all_processes()

    stop_all_processes()    sys.exit(0)

    sys.exit(0)



def stop_all_processes():

def stop_all_processes():    """متوقف کردن همه processes"""

    """متوقف کردن همه processes"""    for name in ['scheduler', 'api']:

    for name in ['scheduler', 'api']:        if processes.get(name) and processes[name]:

        if processes.get(name) and processes[name]:            try:

            try:                log_message(f"Stopping {name}...")

                logger.info(f"Stopping {name}...")                processes[name].terminate()

                processes[name].terminate()                processes[name].wait(timeout=5)

                try:                log_message(f"✅ {name} stopped")

                    processes[name].wait(timeout=5)            except subprocess.TimeoutExpired:

                except subprocess.TimeoutExpired:                processes[name].kill()

                    processes[name].kill()                log_message(f"✅ {name} killed")

                    logger.info(f"✅ {name} killed")            except Exception as e:

                logger.info(f"✅ {name} stopped")                log_message(f"⚠️  Error stopping {name}: {e}")

            except Exception as e:            processes[name] = None

                logger.error(f"⚠️  Error stopping {name}: {e}")

            processes[name] = None

def start_scheduler():

    """شروع Scheduler"""

def read_process_output(process, name):    try:

    """خواندن خروجی process و ثبت آن"""        log_message("▶️  Starting Scheduler...")

    try:        processes['scheduler'] = subprocess.Popen(

        for line in process.stdout:            [sys.executable, 'scheduler.py'],

            if line.strip():            stdout=sys.stdout,

                logger.info(f"[{name.upper()}] {line.rstrip()}")            stderr=sys.stderr,

    except Exception as e:            text=True,

        logger.error(f"Error reading {name} output: {e}")            bufsize=1

        )

        log_message(f"✅ Scheduler started (PID: {processes['scheduler'].pid})")

def start_scheduler():        return True

    """شروع Scheduler"""    except Exception as e:

    try:        log_message(f"❌ Failed to start Scheduler: {e}")

        logger.info("▶️  Starting Scheduler...")        return False

        processes['scheduler'] = subprocess.Popen(

            [sys.executable, 'scheduler.py'],

            stdout=subprocess.PIPE,def start_api():

            stderr=subprocess.STDOUT,    """شروع API"""

            text=True,    try:

            bufsize=1,        log_message("▶️  Starting API Server...")

            universal_newlines=True        processes['api'] = subprocess.Popen(

        )            [sys.executable, 'api.py'],

        logger.info(f"✅ Scheduler started (PID: {processes['scheduler'].pid})")            stdout=sys.stdout,

                    stderr=sys.stderr,

        # Read output in background            text=True,

        thread = threading.Thread(            bufsize=1

            target=read_process_output,        )

            args=(processes['scheduler'], 'scheduler'),        log_message(f"✅ API started (PID: {processes['api'].pid})")

            daemon=True        time.sleep(2)  # منتظر بمانید تا شروع شود

        )        return True

        thread.start()    except Exception as e:

                log_message(f"❌ Failed to start API: {e}")

        return True        return False

    except Exception as e:

        logger.error(f"❌ Failed to start Scheduler: {e}")

        return Falsedef monitor_processes():

    """نگاه‌داری بر روی processes"""

    while True:

def start_api():        try:

    """شروع API"""            # بررسی Scheduler

    try:            if processes['scheduler'] and processes['scheduler'].poll() is not None:

        logger.info("▶️  Starting API Server...")                log_message("⚠️  Scheduler died, restarting...")

        processes['api'] = subprocess.Popen(                start_scheduler()

            [sys.executable, 'api.py'],                time.sleep(5)

            stdout=subprocess.PIPE,            

            stderr=subprocess.STDOUT,            # بررسی API

            text=True,            if processes['api'] and processes['api'].poll() is not None:

            bufsize=1,                log_message("⚠️  API died, restarting...")

            universal_newlines=True                start_api()

        )                time.sleep(5)

        logger.info(f"✅ API started (PID: {processes['api'].pid})")            

        time.sleep(2)            time.sleep(10)  # بررسی هر 10 ثانیه

                except KeyboardInterrupt:

        # Read output in background            break

        thread = threading.Thread(        except Exception as e:

            target=read_process_output,            log_message(f"❌ Monitor error: {e}")

            args=(processes['api'], 'api'),            time.sleep(5)

            daemon=True

        )

        thread.start()def main():

            """نقطه شروع"""

        return True    log_message("="*60)

    except Exception as e:    log_message("🚀 AQI Iran Service Started")

        logger.error(f"❌ Failed to start API: {e}")    log_message(f"   Timezone: Asia/Tehran (UTC+03:30)")

        return False    log_message(f"   Python: {sys.version}")

    log_message("="*60)

    

def monitor_processes():    # تعریف signal handlers

    """نگاه‌داری بر روی processes"""    signal.signal(signal.SIGINT, signal_handler)

    consecutive_failures = {    signal.signal(signal.SIGTERM, signal_handler)

        'scheduler': 0,    

        'api': 0    # شروع Scheduler و API

    }    if not start_scheduler():

            log_message("❌ Failed to start Scheduler")

    while True:        sys.exit(1)

        try:    

            # بررسی Scheduler    time.sleep(2)

            if processes['scheduler']:    

                if processes['scheduler'].poll() is not None:    if not start_api():

                    logger.warning("⚠️  Scheduler died!")        log_message("❌ Failed to start API")

                    consecutive_failures['scheduler'] += 1        stop_all_processes()

                            sys.exit(1)

                    if consecutive_failures['scheduler'] <= 3:    

                        logger.info(f"🔄 Restarting Scheduler (attempt {consecutive_failures['scheduler']})...")    log_message("✅ All services started successfully")

                        start_scheduler()    log_message("="*60)

                        time.sleep(5)    

                    else:    # نگاه‌داری بر روی processes

                        logger.error(f"❌ Scheduler failed {consecutive_failures['scheduler']} times! Giving up for 5 minutes...")    try:

                        time.sleep(300)        monitor_processes()

                        consecutive_failures['scheduler'] = 0    except KeyboardInterrupt:

                else:        signal_handler(signal.SIGINT, None)

                    consecutive_failures['scheduler'] = 0

            

            # بررسی APIif __name__ == '__main__':

            if processes['api']:    main()

                if processes['api'].poll() is not None:
                    logger.warning("⚠️  API died!")
                    consecutive_failures['api'] += 1
                    
                    if consecutive_failures['api'] <= 3:
                        logger.info(f"🔄 Restarting API (attempt {consecutive_failures['api']})...")
                        start_api()
                        time.sleep(5)
                    else:
                        logger.error(f"❌ API failed {consecutive_failures['api']} times! Giving up for 5 minutes...")
                        time.sleep(300)
                        consecutive_failures['api'] = 0
                else:
                    consecutive_failures['api'] = 0
            
            time.sleep(10)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"💥 Monitor error: {e}", exc_info=True)
            time.sleep(5)


def main():
    """نقطه شروع"""
    logger.info("="*70)
    logger.info("🚀 AQI Iran Service Started")
    logger.info(f"   Timezone: Asia/Tehran (UTC+03:30)")
    logger.info(f"   Python: {sys.version.split()[0]}")
    logger.info(f"   Log file: {LOG_FILE}")
    logger.info("="*70)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if not start_scheduler():
        logger.error("❌ Failed to start Scheduler")
        sys.exit(1)
    
    time.sleep(2)
    
    if not start_api():
        logger.error("❌ Failed to start API")
        stop_all_processes()
        sys.exit(1)
    
    logger.info("✅ All services started successfully")
    logger.info("="*70)
    
    try:
        monitor_processes()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


if __name__ == '__main__':
    main()
