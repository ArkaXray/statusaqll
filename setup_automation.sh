#!/bin/bash

# AQI Iran - Ubuntu Automation Setup
# این اسکریپت تمام چیزهای لازم برای خودکارسازی را نصب می‌کند

set -e

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# نسخه
VERSION="1.0.0"

print_header() {
    echo -e "\n${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  AQI Iran - Ubuntu Automation Setup v$VERSION  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# شروع
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

# بررسی requirements
print_info "بررسی Python packages..."
python3 -m pip install -q -r "$PROJECT_DIR/requirements.txt"
print_success "Python packages نصب شدند"

# ایجاد دایرکتوری‌های لازم
print_info "ایجاد دایرکتوری‌ها..."
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/data"
mkdir -p "$PROJECT_DIR/data/backups"
print_success "دایرکتوری‌ها آماده‌اند"

# انتخاب روش اتوموشن
print_info "\nکدام روش اتوموشن را می‌خواهید؟\n"
echo "  1) Cron Job (سادگی: بالا، قابلیت‌اعتماد: بالا)"
echo "  2) Systemd Service (سادگی: متوسط، قابلیت‌اعتماد: بسیار بالا)"
echo "  3) Systemd Timer (سادگی: متوسط، دقت: بالا)"
echo "  0) خروج"
echo ""

read -p "انتخاب (0-3): " choice

case $choice in
    1)
        print_info "\n🔧 نصب Cron Job...\n"
        
        # دریافت cron فعلی
        CRON_FILE="/tmp/aqi_cron_$$.txt"
        crontab -l > "$CRON_FILE" 2>/dev/null || true
        
        # حذف اگر موجود است
        grep -v "AQI_Scheduler" "$CRON_FILE" > "$CRON_FILE.tmp" 2>/dev/null || true
        mv "$CRON_FILE.tmp" "$CRON_FILE"
        
        # اضافه کردن cron جدید
        PYTHON_PATH=$(which python3)
        cat >> "$CRON_FILE" << EOF

# AQI_Scheduler - هر 30 دقیقه جمع‌آوری داده AQI
*/30 * * * * cd $PROJECT_DIR && $PYTHON_PATH scheduler.py >> logs/cron.log 2>&1

EOF
        
        # نصب cron
        crontab "$CRON_FILE"
        rm "$CRON_FILE" 2>/dev/null || true
        
        print_success "Cron Job نصب شد!"
        print_info "\n📋 جزئیات:"
        print_info "  زمان: هر 30 دقیقه (*/30 * * * *)"
        print_info "  دستور: python3 scheduler.py"
        print_info "  لاگ: $PROJECT_DIR/logs/cron.log"
        
        print_info "\n📝 فرمان‌های کاربردی:"
        echo "  crontab -l     # نمایش cron jobs"
        echo "  crontab -e     # ویرایش cron jobs"
        echo "  tail -f $PROJECT_DIR/logs/cron.log  # مشاهده لاگ زنده"
        ;;
    
    2)
        print_info "\n🔧 نصب Systemd Service...\n"
        
        SERVICE_DIR="$HOME/.config/systemd/user"
        mkdir -p "$SERVICE_DIR"
        
        # ایجاد service file
        cat > "$SERVICE_DIR/aqi-scheduler.service" << EOF
[Unit]
Description=AQI Iran Scheduler Service
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
        
        # فعال‌سازی service
        systemctl --user daemon-reload
        systemctl --user enable aqi-scheduler.service
        systemctl --user start aqi-scheduler.service
        
        print_success "Systemd Service نصب شد!"
        print_info "\n📋 جزئیات:"
        print_info "  Service: aqi-scheduler.service"
        print_info "  مسیر: $SERVICE_DIR/aqi-scheduler.service"
        print_info "  حالت: فعال و در حال اجرا"
        
        print_info "\n📝 فرمان‌های کاربردی:"
        echo "  systemctl --user status aqi-scheduler"
        echo "  systemctl --user restart aqi-scheduler"
        echo "  systemctl --user stop aqi-scheduler"
        echo "  journalctl --user -u aqi-scheduler -f"
        ;;
    
    3)
        print_info "\n🔧 نصب Systemd Timer...\n"
        
        SERVICE_DIR="$HOME/.config/systemd/user"
        mkdir -p "$SERVICE_DIR"
        
        # ایجاد service file
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

[Install]
WantedBy=default.target
EOF
        
        # ایجاد timer file
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
        
        # فعال‌سازی timer
        systemctl --user daemon-reload
        systemctl --user enable aqi-scheduler.timer
        systemctl --user start aqi-scheduler.timer
        
        print_success "Systemd Timer نصب شد!"
        print_info "\n📋 جزئیات:"
        print_info "  Timer: aqi-scheduler.timer"
        print_info "  فاصله: هر 30 دقیقه"
        print_info "  حالت: فعال و در حال اجرا"
        
        print_info "\n📝 فرمان‌های کاربردی:"
        echo "  systemctl --user list-timers"
        echo "  systemctl --user status aqi-scheduler.timer"
        echo "  journalctl --user -u aqi-scheduler.service -f"
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

print_info "\n✨ Setup تکمیل شد!"
print_info "پروژه شما الان خودکار اجرا می‌شود.\n"
