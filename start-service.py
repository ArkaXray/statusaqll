#!/usr/bin/env python3
"""
AQI Iran - Service Starter (Non-Interactive)
برای استفاده در systemd service
"""

import sys
import os
import subprocess
import time
import signal
from datetime import datetime
import pytz

TEHRAN_TZ = pytz.timezone('Asia/Tehran')

# برای ذخیره processes
processes = {
    'scheduler': None,
    'api': None
}


def log_message(msg):
    """ثبت پیام با timestamp"""
    ts = datetime.now(TEHRAN_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')
    print(f"[{ts}] {msg}", flush=True)


def signal_handler(sig, frame):
    """مدیریت Ctrl+C"""
    log_message("🛑 Shutting down...")
    stop_all_processes()
    sys.exit(0)


def stop_all_processes():
    """متوقف کردن همه processes"""
    for name in ['scheduler', 'api']:
        if processes.get(name) and processes[name]:
            try:
                log_message(f"Stopping {name}...")
                processes[name].terminate()
                processes[name].wait(timeout=5)
                log_message(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                processes[name].kill()
                log_message(f"✅ {name} killed")
            except Exception as e:
                log_message(f"⚠️  Error stopping {name}: {e}")
            processes[name] = None


def start_scheduler():
    """شروع Scheduler"""
    try:
        log_message("▶️  Starting Scheduler...")
        processes['scheduler'] = subprocess.Popen(
            [sys.executable, 'scheduler.py'],
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
            bufsize=1
        )
        log_message(f"✅ Scheduler started (PID: {processes['scheduler'].pid})")
        return True
    except Exception as e:
        log_message(f"❌ Failed to start Scheduler: {e}")
        return False


def start_api():
    """شروع API"""
    try:
        log_message("▶️  Starting API Server...")
        processes['api'] = subprocess.Popen(
            [sys.executable, 'api.py'],
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
            bufsize=1
        )
        log_message(f"✅ API started (PID: {processes['api'].pid})")
        time.sleep(2)  # منتظر بمانید تا شروع شود
        return True
    except Exception as e:
        log_message(f"❌ Failed to start API: {e}")
        return False


def monitor_processes():
    """نگاه‌داری بر روی processes"""
    while True:
        try:
            # بررسی Scheduler
            if processes['scheduler'] and processes['scheduler'].poll() is not None:
                log_message("⚠️  Scheduler died, restarting...")
                start_scheduler()
                time.sleep(5)
            
            # بررسی API
            if processes['api'] and processes['api'].poll() is not None:
                log_message("⚠️  API died, restarting...")
                start_api()
                time.sleep(5)
            
            time.sleep(10)  # بررسی هر 10 ثانیه
        except KeyboardInterrupt:
            break
        except Exception as e:
            log_message(f"❌ Monitor error: {e}")
            time.sleep(5)


def main():
    """نقطه شروع"""
    log_message("="*60)
    log_message("🚀 AQI Iran Service Started")
    log_message(f"   Timezone: Asia/Tehran (UTC+03:30)")
    log_message(f"   Python: {sys.version}")
    log_message("="*60)
    
    # تعریف signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # شروع Scheduler و API
    if not start_scheduler():
        log_message("❌ Failed to start Scheduler")
        sys.exit(1)
    
    time.sleep(2)
    
    if not start_api():
        log_message("❌ Failed to start API")
        stop_all_processes()
        sys.exit(1)
    
    log_message("✅ All services started successfully")
    log_message("="*60)
    
    # نگاه‌داری بر روی processes
    try:
        monitor_processes()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


if __name__ == '__main__':
    main()
