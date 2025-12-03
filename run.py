import sys
import os
from datetime import datetime
import pytz

TEHRAN_TZ = pytz.timezone('Asia/Tehran')


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
    print("  3. Manual Collection")
    print("  4. View Logs (last 50)")
    print("  5. View Stats")
    print("  0. Exit")
    print("\n" + "="*80)


def main():
    print_banner()
    
    while True:
        show_menu()
        ch = input("Choose (0-5): ").strip()
        
        if ch == '1':
            print("\n▶️  Starting Scheduler...\n")
            os.system(f'{sys.executable} scheduler.py')
        elif ch == '2':
            print("\n▶️  Starting API Server...\n")
            os.system(f'{sys.executable} api.py')
        elif ch == '3':
            print("\n▶️  Manual Collection...\n")
            os.system(f'{sys.executable} scraper.py')
        elif ch == '4':
            print("\n▶️  Logs (last 50):\n")
            if os.path.exists('logs/scraper.log'):
                os.system('powershell -Command "Get-Content logs/scraper.log | Select-Object -Last 50"')
            else:
                print("No logs yet")
        elif ch == '5':
            print("\n▶️  Stats:\n")
            if os.path.exists('data/aqi_data.json'):
                import json
                with open('data/aqi_data.json', 'r', encoding='utf-8') as f:
                    dt = json.load(f)
                    vals = [i.get('aqi', 0) for i in dt.values()]
                    if vals:
                        print(f"States: {len(dt)}")
                        print(f"Average: {sum(vals)/len(vals):.1f}")
                        print(f"Min: {min(vals)}")
                        print(f"Max: {max(vals)}")
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
