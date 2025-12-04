#!/usr/bin/env python3#!/usr/bin/env python3#!/usr/bin/env python3#!/usr/bin/env python3

"""

AQI Iran - Simple Service Starter"""

"""

AQI Iran - Service Starter (Non-Interactive)""""""

import sys

import osبرای استفاده در systemd service

import subprocess

import time"""AQI Iran - Service Starter (Non-Interactive)AQI Iran - Service Starter (Non-Interactive)



def main():

    print("[START] AQI Iran Service Starter")

    print("[INFO] Starting Scheduler...")import sysبرای استفاده در systemd serviceبرای استفاده در systemd service

    

    try:import os

        scheduler_proc = subprocess.Popen([sys.executable, 'scheduler.py'])

        print(f"[OK] Scheduler started (PID: {scheduler_proc.pid})")import subprocess""""""

    except Exception as e:

        print(f"[ERROR] Failed to start Scheduler: {e}")import time

        sys.exit(1)

    import signal

    time.sleep(2)

    import logging

    print("[INFO] Starting API Server...")

    try:import threadingimport sysimport sys

        api_proc = subprocess.Popen([sys.executable, 'api.py'])

        print(f"[OK] API Server started (PID: {api_proc.pid})")from datetime import datetime

    except Exception as e:

        print(f"[ERROR] Failed to start API: {e}")import pytzimport osimport os

        sys.exit(1)

    

    print("[OK] All services started successfully")

    print("[MONITOR] Watching processes...")TEHRAN_TZ = pytz.timezone('Asia/Tehran')import subprocessimport subprocess

    

    while True:LOG_FILE = os.path.expanduser('~/.aqi-service.log')

        time.sleep(60)

        import timeimport time

        if scheduler_proc.poll() is not None:

            print("[WARN] Scheduler process died!")# Setup logging

            scheduler_proc = subprocess.Popen([sys.executable, 'scheduler.py'])

            print(f"[OK] Scheduler restarted (PID: {scheduler_proc.pid})")logging.basicConfig(import signalimport signal

        

        if api_proc.poll() is not None:    level=logging.DEBUG,

            print("[WARN] API process died!")

            api_proc = subprocess.Popen([sys.executable, 'api.py'])    format='[%(asctime)s] %(levelname)s: %(message)s',import loggingimport logging

            print(f"[OK] API restarted (PID: {api_proc.pid})")

    datefmt='%Y-%m-%d %H:%M:%S',

if __name__ == '__main__':

    main()    handlers=[import threadingfrom datetime import datetime


        logging.FileHandler(LOG_FILE, encoding='utf-8'),

        logging.StreamHandler()from datetime import datetimeimport pytz

    ]

)import pytz

logger = logging.getLogger('AQI-Service')

TEHRAN_TZ = pytz.timezone('Asia/Tehran')

# برای ذخیره processes

processes = {TEHRAN_TZ = pytz.timezone('Asia/Tehran')LOG_FILE = os.path.expanduser('~/.aqi-service.log')

    'scheduler': None,

    'api': NoneLOG_FILE = os.path.expanduser('~/.aqi-service.log')

}

# Setup logging



def signal_handler(sig, frame):# Setup logginglogging.basicConfig(

    """مدیریت Ctrl+C"""

    logger.info("🛑 Shutting down...")logging.basicConfig(    level=logging.DEBUG,

    stop_all_processes()

    sys.exit(0)    level=logging.DEBUG,    format='[%(asctime)s] %(levelname)s: %(message)s',



    format='[%(asctime)s] %(levelname)s: %(message)s',    datefmt='%Y-%m-%d %H:%M:%S',

def stop_all_processes():

    """متوقف کردن همه processes"""    datefmt='%Y-%m-%d %H:%M:%S',    handlers=[

    for name in ['scheduler', 'api']:

        if processes.get(name) and processes[name]:    handlers=[        logging.FileHandler(LOG_FILE, encoding='utf-8'),

            try:

                logger.info(f"Stopping {name}...")        logging.FileHandler(LOG_FILE, encoding='utf-8'),        logging.StreamHandler()

                processes[name].terminate()

                try:        logging.StreamHandler()    ]

                    processes[name].wait(timeout=5)

                except subprocess.TimeoutExpired:    ])

                    processes[name].kill()

                    logger.info(f"✅ {name} killed"))logger = logging.getLogger('AQI-Service')

                logger.info(f"✅ {name} stopped")

            except Exception as e:logger = logging.getLogger('AQI-Service')

                logger.error(f"Error stopping {name}: {e}")

            processes[name] = None# برای ذخیره processes



# برای ذخیره processesprocesses = {

def read_process_output(process, name):

    """خواندن خروجی process و ثبت آن"""processes = {    'scheduler': None,

    try:

        for line in iter(process.stdout.readline, ''):    'scheduler': None,    'api': None

            if line.strip():

                logger.info(f"[{name.upper()}] {line.rstrip()}")    'api': None}

    except Exception as e:

        logger.error(f"Error reading {name} output: {e}")}





def start_scheduler():

    """شروع Scheduler"""def signal_handler(sig, frame):

    try:

        logger.info("▶️  Starting Scheduler...")def signal_handler(sig, frame):    """مدیریت Ctrl+C"""

        processes['scheduler'] = subprocess.Popen(

            [sys.executable, 'scheduler.py'],    """مدیریت Ctrl+C"""    log_message("🛑 Shutting down...")

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,    logger.info("🛑 Shutting down...")    stop_all_processes()

            text=True,

            bufsize=1,    stop_all_processes()    sys.exit(0)

            universal_newlines=True

        )    sys.exit(0)

        logger.info(f"✅ Scheduler started (PID: {processes['scheduler'].pid})")

        

        # Read output in background

        thread = threading.Thread(def stop_all_processes():

            target=read_process_output,

            args=(processes['scheduler'], 'scheduler'),def stop_all_processes():    """متوقف کردن همه processes"""

            daemon=True

        )    """متوقف کردن همه processes"""    for name in ['scheduler', 'api']:

        thread.start()

            for name in ['scheduler', 'api']:        if processes.get(name) and processes[name]:

        return True

    except Exception as e:        if processes.get(name) and processes[name]:            try:

        logger.error(f"❌ Failed to start Scheduler: {e}")

        return False            try:                log_message(f"Stopping {name}...")



                logger.info(f"Stopping {name}...")                processes[name].terminate()

def start_api():

    """شروع API"""                processes[name].terminate()                processes[name].wait(timeout=5)

    try:

        logger.info("▶️  Starting API Server...")                try:                log_message(f"✅ {name} stopped")

        processes['api'] = subprocess.Popen(

            [sys.executable, 'api.py'],                    processes[name].wait(timeout=5)            except subprocess.TimeoutExpired:

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,                except subprocess.TimeoutExpired:                processes[name].kill()

            text=True,

            bufsize=1,                    processes[name].kill()                log_message(f"✅ {name} killed")

            universal_newlines=True

        )                    logger.info(f"✅ {name} killed")            except Exception as e:

        logger.info(f"✅ API started (PID: {processes['api'].pid})")

        time.sleep(2)                logger.info(f"✅ {name} stopped")                log_message(f"⚠️  Error stopping {name}: {e}")

        

        # Read output in background            except Exception as e:            processes[name] = None

        thread = threading.Thread(

            target=read_process_output,                logger.error(f"⚠️  Error stopping {name}: {e}")

            args=(processes['api'], 'api'),

            daemon=True            processes[name] = None

        )

        thread.start()def start_scheduler():

        

        return True    """شروع Scheduler"""

    except Exception as e:

        logger.error(f"❌ Failed to start API: {e}")def read_process_output(process, name):    try:

        return False

    """خواندن خروجی process و ثبت آن"""        log_message("▶️  Starting Scheduler...")



def monitor_processes():    try:        processes['scheduler'] = subprocess.Popen(

    """نگاه‌داری بر روی processes"""

    consecutive_failures = {        for line in process.stdout:            [sys.executable, 'scheduler.py'],

        'scheduler': 0,

        'api': 0            if line.strip():            stdout=sys.stdout,

    }

                    logger.info(f"[{name.upper()}] {line.rstrip()}")            stderr=sys.stderr,

    while True:

        try:    except Exception as e:            text=True,

            # بررسی Scheduler

            if processes['scheduler']:        logger.error(f"Error reading {name} output: {e}")            bufsize=1

                if processes['scheduler'].poll() is not None:

                    logger.warning("⚠️  Scheduler died!")        )

                    consecutive_failures['scheduler'] += 1

                            log_message(f"✅ Scheduler started (PID: {processes['scheduler'].pid})")

                    if consecutive_failures['scheduler'] <= 3:

                        logger.info(f"🔄 Restarting Scheduler (attempt {consecutive_failures['scheduler']})...")def start_scheduler():        return True

                        start_scheduler()

                        time.sleep(5)    """شروع Scheduler"""    except Exception as e:

                    else:

                        logger.error(f"❌ Scheduler failed {consecutive_failures['scheduler']} times!")    try:        log_message(f"❌ Failed to start Scheduler: {e}")

                        time.sleep(300)

                        consecutive_failures['scheduler'] = 0        logger.info("▶️  Starting Scheduler...")        return False

                else:

                    consecutive_failures['scheduler'] = 0        processes['scheduler'] = subprocess.Popen(

            

            # بررسی API            [sys.executable, 'scheduler.py'],

            if processes['api']:

                if processes['api'].poll() is not None:            stdout=subprocess.PIPE,def start_api():

                    logger.warning("⚠️  API died!")

                    consecutive_failures['api'] += 1            stderr=subprocess.STDOUT,    """شروع API"""

                    

                    if consecutive_failures['api'] <= 3:            text=True,    try:

                        logger.info(f"🔄 Restarting API (attempt {consecutive_failures['api']})...")

                        start_api()            bufsize=1,        log_message("▶️  Starting API Server...")

                        time.sleep(5)

                    else:            universal_newlines=True        processes['api'] = subprocess.Popen(

                        logger.error(f"❌ API failed {consecutive_failures['api']} times!")

                        time.sleep(300)        )            [sys.executable, 'api.py'],

                        consecutive_failures['api'] = 0

                else:        logger.info(f"✅ Scheduler started (PID: {processes['scheduler'].pid})")            stdout=sys.stdout,

                    consecutive_failures['api'] = 0

                                stderr=sys.stderr,

            time.sleep(10)

        except KeyboardInterrupt:        # Read output in background            text=True,

            break

        except Exception as e:        thread = threading.Thread(            bufsize=1

            logger.error(f"💥 Monitor error: {e}", exc_info=True)

            time.sleep(5)            target=read_process_output,        )



            args=(processes['scheduler'], 'scheduler'),        log_message(f"✅ API started (PID: {processes['api'].pid})")

def main():

    """نقطه شروع"""            daemon=True        time.sleep(2)  # منتظر بمانید تا شروع شود

    logger.info("="*70)

    logger.info("🚀 AQI Iran Service Started")        )        return True

    logger.info(f"   Timezone: Asia/Tehran (UTC+03:30)")

    logger.info(f"   Python: {sys.version.split()[0]}")        thread.start()    except Exception as e:

    logger.info(f"   Log file: {LOG_FILE}")

    logger.info("="*70)                log_message(f"❌ Failed to start API: {e}")

    

    signal.signal(signal.SIGINT, signal_handler)        return True        return False

    signal.signal(signal.SIGTERM, signal_handler)

        except Exception as e:

    if not start_scheduler():

        logger.error("❌ Failed to start Scheduler")        logger.error(f"❌ Failed to start Scheduler: {e}")

        sys.exit(1)

            return Falsedef monitor_processes():

    time.sleep(2)

        """نگاه‌داری بر روی processes"""

    if not start_api():

        logger.error("❌ Failed to start API")    while True:

        stop_all_processes()

        sys.exit(1)def start_api():        try:

    

    logger.info("✅ All services started successfully")    """شروع API"""            # بررسی Scheduler

    logger.info("="*70)

        try:            if processes['scheduler'] and processes['scheduler'].poll() is not None:

    try:

        monitor_processes()        logger.info("▶️  Starting API Server...")                log_message("⚠️  Scheduler died, restarting...")

    except KeyboardInterrupt:

        signal_handler(signal.SIGINT, None)        processes['api'] = subprocess.Popen(                start_scheduler()



            [sys.executable, 'api.py'],                time.sleep(5)

if __name__ == '__main__':

    main()            stdout=subprocess.PIPE,            


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
