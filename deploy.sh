#!/bin/bash

# AQI Iran - Production Deployment Script for Ubuntu
# This script sets up everything for production

set -e

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  AQI Iran - Production Deployment Setup          ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}\n"
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

print_header

# بررسی اگر root است
if [ "$EUID" -eq 0 ]; then
    print_warning "این اسکریپت نباید به عنوان root اجرا شود!"
    exit 1
fi

# بررسی Python3
if ! command -v python3 &> /dev/null; then
    print_error "Python3 یافت نشد!"
    print_info "برای نصب: sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi
print_success "Python3 یافت شد: $(python3 --version)"

# دریافت مسیر پروژه
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
print_success "مسیر پروژه: $PROJECT_DIR"

# بررسی و نصب requirements
print_info "\n📦 بررسی و نصب Python packages..."
python3 -m pip install -q -r "$PROJECT_DIR/requirements.txt"
print_success "Python packages نصب شدند"

# ایجاد دایرکتوری‌های لازم
print_info "\n📁 ایجاد دایرکتوری‌های پروژه..."
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/data"
mkdir -p "$PROJECT_DIR/data/backups"
chmod 755 "$PROJECT_DIR/logs"
chmod 755 "$PROJECT_DIR/data"
print_success "دایرکتوری‌ها آماده‌اند"

# انتخاب روش اتوموشن
print_info "\n🔧 انتخاب روش خودکارسازی:\n"
echo "  1) Cron Job (سادگی: 10/10)"
echo "  2) Systemd Service (قابلیت‌اعتماد: 10/10) ⭐ پیشنهاد"
echo "  3) Systemd Timer (دقت: 10/10)"
echo "  0) خروج"
echo ""

read -p "انتخاب (0-3): " choice

case $choice in
    1)
        print_info "\n🔧 نصب Cron Job...\n"
        
        CRON_FILE="/tmp/aqi_cron_$$.txt"
        crontab -l > "$CRON_FILE" 2>/dev/null || true
        
        grep -v "AQI_Scheduler" "$CRON_FILE" > "$CRON_FILE.tmp" 2>/dev/null || true
        mv "$CRON_FILE.tmp" "$CRON_FILE"
        
        PYTHON_PATH=$(which python3)
        cat >> "$CRON_FILE" << EOF

# AQI_Scheduler - هر 30 دقیقه جمع‌آوری داده AQI
*/30 * * * * cd $PROJECT_DIR && $PYTHON_PATH scheduler.py >> logs/cron.log 2>&1

EOF
        
        crontab "$CRON_FILE"
        rm "$CRON_FILE" 2>/dev/null || true
        
        print_success "Cron Job نصب شد!"
        print_info "\n📋 جزئیات Cron Job:"
        print_info "  زمان: هر 30 دقیقه (*/30 * * * *)"
        print_info "  لاگ: $PROJECT_DIR/logs/cron.log"
        print_info "\n📝 فرمان‌های کاربردی:"
        echo "  crontab -l               # نمایش cron jobs"
        echo "  crontab -e               # ویرایش cron jobs"
        echo "  tail -f $PROJECT_DIR/logs/cron.log  # مشاهده لاگ"
        ;;
    
    2)
        print_info "\n🔧 نصب Systemd Service...\n"
        
        SERVICE_DIR="$HOME/.config/systemd/user"
        mkdir -p "$SERVICE_DIR"
        
        cat > "$SERVICE_DIR/aqi-scheduler.service" << EOF
[Unit]
Description=AQI Iran Scheduler Service
Documentation=https://github.com/your-repo/AQI_Iran
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=$(which python3) scheduler.py

Restart=always
RestartSec=30

StandardOutput=journal
StandardError=journal

Environment="PYTHONUNBUFFERED=1"
Environment="TZ=Asia/Tehran"

[Install]
WantedBy=default.target
EOF
        
        systemctl --user daemon-reload
        systemctl --user enable aqi-scheduler.service
        systemctl --user start aqi-scheduler.service
        
        print_success "Systemd Service نصب شد!"
        print_info "\n📋 جزئیات Service:"
        print_info "  فایل: $SERVICE_DIR/aqi-scheduler.service"
        print_info "  حالت: Enabled و Running"
        print_info "\n📝 فرمان‌های کاربردی:"
        echo "  systemctl --user status aqi-scheduler         # وضعیت"
        echo "  systemctl --user restart aqi-scheduler        # راه‌اندازی مجدد"
        echo "  systemctl --user stop aqi-scheduler           # متوقف کردن"
        echo "  journalctl --user -u aqi-scheduler -f         # لاگ زنده"
        ;;
    
    3)
        print_info "\n🔧 نصب Systemd Timer...\n"
        
        SERVICE_DIR="$HOME/.config/systemd/user"
        mkdir -p "$SERVICE_DIR"
        
        cat > "$SERVICE_DIR/aqi-scheduler.service" << EOF
[Unit]
Description=AQI Iran Scheduler
After=network.target

[Service]
Type=oneshot
WorkingDirectory=$PROJECT_DIR
ExecStart=$(which python3) scheduler.py

StandardOutput=journal
StandardError=journal

Environment="PYTHONUNBUFFERED=1"
Environment="TZ=Asia/Tehran"
EOF
        
        cat > "$SERVICE_DIR/aqi-scheduler.timer" << EOF
[Unit]
Description=AQI Iran Scheduler Timer

[Timer]
OnBootSec=2min
OnUnitActiveSec=30min
Persistent=true
AccuracySec=1min

[Install]
WantedBy=timers.target
EOF
        
        systemctl --user daemon-reload
        systemctl --user enable aqi-scheduler.timer
        systemctl --user start aqi-scheduler.timer
        
        print_success "Systemd Timer نصب شد!"
        print_info "\n📋 جزئیات Timer:"
        print_info "  فایل: $SERVICE_DIR/aqi-scheduler.timer"
        print_info "  فاصله: هر 30 دقیقه"
        print_info "  حالت: Enabled و Running"
        print_info "\n📝 فرمان‌های کاربردی:"
        echo "  systemctl --user list-timers                    # لیست تایمرها"
        echo "  systemctl --user status aqi-scheduler.timer     # وضعیت"
        echo "  journalctl --user -u aqi-scheduler.service -f   # لاگ زنده"
        ;;
    
    0)
        print_info "خروج..."
        exit 0
        ;;
    
    *)
        print_error "انتخاب نامعتبر!"
        exit 1
        ;;
esac

# نصب API (اختیاری)
read -p "آیا می‌خواهید API server را نیز نصب کنید؟ (y/n): " install_api

if [ "$install_api" = "y" ] || [ "$install_api" = "Y" ]; then
    print_info "\n🔧 نصب API Service...\n"
    
    SERVICE_DIR="$HOME/.config/systemd/user"
    
    cat > "$SERVICE_DIR/aqi-api.service" << EOF
[Unit]
Description=AQI Iran API Server
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=$(which python3) api.py

Restart=always
RestartSec=10

StandardOutput=journal
StandardError=journal

Environment="PYTHONUNBUFFERED=1"
Environment="TZ=Asia/Tehran"

[Install]
WantedBy=default.target
EOF
    
    systemctl --user daemon-reload
    systemctl --user enable aqi-api.service
    systemctl --user start aqi-api.service
    
    print_success "API Service نصب شد!"
    print_info "🌐 API در دسترس است: http://localhost:5000"
    echo ""
fi

# خلاصه
print_info "\n═══════════════════════════════════════════════════════"
print_success "Setup تکمیل شد!"
print_info "═══════════════════════════════════════════════════════\n"

print_info "✨ پروژه AQI Iran اکنون آماده برای تولید است!\n"

print_info "📝 نکات مهم:"
echo "  • لاگ‌ها در $PROJECT_DIR/logs/ ذخیره می‌شوند"
echo "  • داده‌ها در $PROJECT_DIR/data/ ذخیره می‌شوند"
echo "  • بک‌آپ‌ها به‌طور خودکار ایجاد می‌شوند"
echo "  • تمام زمان‌ها در تایم‌زون تهران (UTC+03:30) هستند"
echo ""

print_info "🔗 لینک‌های مفید:"
echo "  README: $PROJECT_DIR/README.md"
echo "  RETRY_LOGIC: $PROJECT_DIR/RETRY_LOGIC.md"
echo "  INSTALL_UBUNTU: $PROJECT_DIR/INSTALL_UBUNTU.md"
echo ""

print_success "سیستم شما آماده است! 🚀\n"
