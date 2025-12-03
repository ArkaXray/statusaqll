#!/bin/bash

# AQI Iran - Update Script
# این اسکریپ برنامه را از GitHub آپدیت می‌کند

set -e

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}╔═════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  AQI Iran - Update from GitHub                    ║${NC}"
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

# شروع
print_header

# بررسی git
if ! command -v git &> /dev/null; then
    print_error "Git not found! Install with: sudo apt-get install git"
fi
print_ok "Git found"

# دریافت مسیر
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
print_ok "Project directory: $PROJECT_DIR"

# بررسی اگر git repo است
if [ ! -d "$PROJECT_DIR/.git" ]; then
    print_error "Not a git repository! Run: git clone https://github.com/ArkaXray/statusaqll.git"
fi
print_ok "Git repository found"

# مشاهده status قبل
print_info "\nCurrent status:"
cd "$PROJECT_DIR"
git status --short || true

# آپدیت
print_info "\nFetching updates from GitHub..."
git fetch origin

# بررسی اگر تغییرات هست
CURRENT=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$CURRENT" = "$REMOTE" ]; then
    print_ok "Already up to date!"
    echo ""
    exit 0
fi

# نمایش تغییرات
print_info "\nChanges to be downloaded:"
git log --oneline $CURRENT..$REMOTE

# پرسش برای آپدیت
echo ""
read -p "Download and apply these changes? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Update cancelled"
    exit 0
fi

# آپدیت
print_info "\nPulling changes..."
git pull origin main

if [ $? -eq 0 ]; then
    print_ok "Update successful!"
    
    # نصب packages اگر requirements تغییر کرد
    print_info "\nInstalling/updating Python packages..."
    pip3 install -q -r "$PROJECT_DIR/requirements.txt" 2>&1 | grep -v "already satisfied" || true
    print_ok "Packages updated"
    
    # نمایش تاریخ آخر آپدیت
    LATEST_COMMIT=$(git log --oneline -1)
    print_info "\nLatest commit: $LATEST_COMMIT"
    
    echo ""
    print_ok "All set! You can run:"
    echo "  python3 run.py"
    echo "  python3 scheduler.py"
    echo "  python3 api.py"
    echo ""
else
    print_error "Update failed! Try: git pull origin main"
fi
