import sys
import os
from datetime import datetime
import pytz
import subprocess
import threading
import time

TEHRAN_TZ = pytz.timezone('Asia/Tehran')

# برای ذخیره processes
processes = {
    'scheduler': None,
    'api': None
}


def print_banner():
    print("\n" + "="*80)
    print("🌍 AQI Iran System")
    print("="*80)
    print(f"Time: {datetime.now(TEHRAN_TZ).isoformat()}")
    print(f"Timezone: Asia/Tehran (UTC+03:30)")
    print("="*80 + "\n")


def show_menu():
    print("\n📋 Menu:\n")
    print("  1. Start Scheduler (auto collect every 30 minutes)")
    print("  2. Start API Server (port 5000)")
    print("  3. Start Both (Scheduler + API)")
    print("  4. Manual Collection")
    print("  5. View Logs (last 50)")
    print("  6. View Stats")
    print("  0. Exit")
    print("\n" + "="*80)


def stop_process(name):
    """متوقف کردن process"""
    if processes.get(name):
        try:
            processes[name].terminate()
            processes[name].wait(timeout=5)
            print(f"✅ {name} stopped")
        except:
            processes[name].kill()
            print(f"✅ {name} killed")
        processes[name] = None


def start_scheduler():
    """شروع Scheduler"""
    if processes['scheduler']:
        print("❌ Scheduler already running!")
        return
    
    print("\n▶️  Starting Scheduler...\n")
    processes['scheduler'] = subprocess.Popen(
        [sys.executable, 'scheduler.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"✅ Scheduler started (PID: {processes['scheduler'].pid})")


def start_api():
    """شروع API"""
    if processes['api']:
        print("❌ API already running!")
        return
    
    print("\n▶️  Starting API Server...\n")
    processes['api'] = subprocess.Popen(
        [sys.executable, 'api.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)  # منتظر بمانید تا شروع شود
    print(f"✅ API started (PID: {processes['api'].pid})")
    print("📌 API available at: http://localhost:5000/api/aqi")


def start_both():
    """شروع Scheduler و API همزمان"""
    print("\n▶️  Starting Scheduler + API (Background)...\n")
    
    start_scheduler()
    start_api()
    
    print("\n" + "="*80)
    print("✅ Both services are running in background!")
    print("="*80)
    print("\nYou can:")
    print("  - View logs: option 5")
    print("  - Check stats: option 6")
    print("  - Visit API: http://localhost:5000/api/aqi")
    print("  - Press Ctrl+C to stop all")
    print("="*80 + "\n")
    
    # منتظر بمانید
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...\n")
        stop_process('scheduler')
        stop_process('api')
        print("✅ All services stopped\n")


def main():
    print_banner()
    
    while True:
        show_menu()
        ch = input("Choose (0-6): ").strip()
        
        if ch == '1':
            start_scheduler()
        elif ch == '2':
            start_api()
        elif ch == '3':
            start_both()
        elif ch == '4':
            print("\n▶️  Manual Collection...\n")
            subprocess.run([sys.executable, 'scraper.py'])
        elif ch == '5':
            print("\n▶️  Logs (last 50):\n")
            if os.path.exists('logs/scraper.log'):
                with open('logs/scraper.log', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[-50:]:
                        print(line.rstrip())
            else:
                print("No logs yet")
        elif ch == '6':
            print("\n▶️  Stats:\n")
            if os.path.exists('data/aqi_data.json'):
                import json
                with open('data/aqi_data.json', 'r', encoding='utf-8') as f:
                    dt = json.load(f)
                    vals = [i.get('aqi', 0) for i in dt.values()]
                    if vals:
                        print(f"States: {len(dt)}")
                        print(f"Average AQI: {sum(vals)/len(vals):.1f}")
                        print(f"Min AQI: {min(vals)}")
                        print(f"Max AQI: {max(vals)}")
                        print(f"Last update: {datetime.now(TEHRAN_TZ).isoformat()}")
                    else:
                        print("No data")
            else:
                print("No data collected yet")
        elif ch == '0':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid choice!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped.\n")

