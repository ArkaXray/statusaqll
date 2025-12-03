import sys
import os
from datetime import datetime
import pytz
import json

TEHRAN_TZ = pytz.timezone('Asia/Tehran')
LOG_FILE = 'logs/scraper.log'


def print_header():
    print("="*80)
    print("📋 AQI System Logs")
    print("="*80)
    print(f"Timezone: Asia/Tehran (UTC+03:30)")
    print(f"Time: {datetime.now(TEHRAN_TZ).isoformat()}")
    print("="*80 + "\n")


def show_tail(lines=50):
    print_header()
    if not os.path.exists(LOG_FILE):
        print("No logs yet\n")
        return
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    for line in all_lines[-lines:]:
        print(line.rstrip())
    
    print(f"\n{'='*80}")
    print(f"Total logs shown: {min(lines, len(all_lines))}")
    print("="*80 + "\n")


def show_stats():
    print_header()
    
    if not os.path.exists('data/aqi_data.json'):
        print("No data collected yet\n")
        return
    
    with open('data/aqi_data.json', 'r', encoding='utf-8') as f:
        dt = json.load(f)
    
    vals = [i.get('aqi', 0) for i in dt.values()]
    
    print(f"Total States: {len(dt)}")
    print(f"Average AQI: {sum(vals)/len(vals):.1f}")
    print(f"Min AQI: {min(vals)}")
    print(f"Max AQI: {max(vals)}")
    print(f"Median: {sorted(vals)[len(vals)//2]}\n")
    
    print("Last Updated:")
    if dt:
        last_ts = list(dt.values())[0].get('timestamp', 'N/A')
        print(f"  {last_ts}\n")


def watch_logs():
    print_header()
    print("Watching logs... (Press Ctrl+C to stop)\n")
    
    if not os.path.exists(LOG_FILE):
        print("No logs yet")
        return
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        
        while True:
            ln = f.readline()
            if ln:
                print(ln.rstrip())
            else:
                import time
                time.sleep(1)


if __name__ == '__main__':
    act = sys.argv[1] if len(sys.argv) > 1 else 'tail'
    
    if act == 'tail':
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        show_tail(lines)
    elif act == 'stats':
        show_stats()
    elif act == 'watch':
        watch_logs()
    else:
        print("Usage:")
        print("  python log_viewer.py tail [lines]    - Show last N logs")
        print("  python log_viewer.py stats           - Show statistics")
        print("  python log_viewer.py watch           - Watch logs (real-time)")
