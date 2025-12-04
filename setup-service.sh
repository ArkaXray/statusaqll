#!/bin/bash

# AQI Iran - Auto-Start Service Setup
# این اسکریپ برنامه را خودکار شروع می‌کند

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}╔═════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  AQI Iran - Auto-Start Service Setup               ║${NC}"
    echo -e "${BLUE}╚═════════════════════════════════════════════════════╝${NC}\n"
}

print_ok() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
    exit 1
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_header

# بررسی systemd
if ! command -v systemctl &> /dev/null; then
    print_error "systemd not found! This setup requires systemd"
fi
print_ok "systemd found"

# مسیر پروژه
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
print_ok "Project directory: $PROJECT_DIR"

# بررسی فایل service
if [ ! -f "$PROJECT_DIR/aqi-full.service" ]; then
    print_error "aqi-full.service not found!"
fi
print_ok "Service file found"

# دایرکتوری service
SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"

# کپی کردن service
print_info "\nCopying service file..."
cp "$PROJECT_DIR/aqi-full.service" "$SERVICE_DIR/aqi-full.service"

# فقط %h و %u را ترک کنید - systemd خودش تبدیل می‌کند
# شاید نیازی به sed نباشد

print_ok "Service file configured"

# Reload systemd
print_info "\nReloading systemd..."
systemctl --user daemon-reload
print_ok "systemd reloaded"

# Enable service
print_info "\nEnabling service..."
systemctl --user enable aqi-full.service
print_ok "Service enabled"

# شروع service
print_info "\nStarting service..."
systemctl --user start aqi-full.service
sleep 2
print_ok "Service started"

# بررسی وضعیت
print_info "\nChecking status..."
if systemctl --user is-active --quiet aqi-full.service; then
    print_ok "Service is running!"
else
    print_warning "Service may not be running, checking logs..."
    journalctl --user -u aqi-full.service -n 10
fi

# خلاصه
echo -e "\n${BLUE}╔═════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}[✓] Setup Complete!${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Service commands:${NC}"
echo "  systemctl --user status aqi-full      # وضعیت"
echo "  systemctl --user start aqi-full       # شروع"
echo "  systemctl --user stop aqi-full        # متوقف"
echo "  systemctl --user restart aqi-full     # restart"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo "  journalctl --user -u aqi-full -f      # لاگ زنده"
echo "  journalctl --user -u aqi-full -n 50   # آخرین 50 لاگ"
echo ""
echo -e "${BLUE}API:${NC}"
echo "  http://localhost:5000/api/aqi"
echo ""
echo -e "${YELLOW}Notes:${NC}"
echo "  • Service is auto-started on login"
echo "  • Scheduler runs every 30 minutes"
echo "  • API available on port 5000"
echo "  • Logs in: journalctl --user -u aqi-full"
echo ""
