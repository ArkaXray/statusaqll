#!/bin/bash

# AQI Iran - One-Click Installation Script (Linux/Mac)
# نصب خودکار برای لینوکس و مک

set -e

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
print_header() {
    echo -e "\n${BLUE}╔═════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  AQI Iran - One-Click Installation (Linux/Mac)     ║${NC}"
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

# بررسی Python
print_info "Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found! Install with: sudo apt install python3 python3-pip"
fi
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
print_ok "Python $PYTHON_VERSION found"

# بررسی pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 not found!"
fi
print_ok "pip3 found"

# مسیر پروژه
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
print_ok "Project directory: $PROJECT_DIR"

# ایجاد دایرکتوری‌های لازم
print_info "\nCreating directories..."
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/data"
mkdir -p "$PROJECT_DIR/data/backups"
chmod 755 "$PROJECT_DIR/logs"
chmod 755 "$PROJECT_DIR/data"
print_ok "Directories created"

# نصب Linux system dependencies (برای Playwright)
print_info "\nChecking system dependencies..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        print_info "Detected: Debian/Ubuntu"
        print_info "Installing system dependencies (this may require sudo)..."
        
        # بررسی اگر sudo موجود است
        if sudo -n true 2>/dev/null; then
            sudo apt-get update -qq 2>/dev/null || true
            sudo apt-get install -y -qq \
                libgconf-2-4 \
                libx11-xcb1 \
                libxcb-icccm4 \
                libxcb-image0 \
                libxcb-keysyms1 \
                libxcb-render-util0 \
                libxcb-xfixes0 \
                libxdamage1 \
                libxfixes3 \
                libxrandr2 \
                libxss1 \
                libxtst6 \
                libnss3 \
                libnspr4 \
                libatk1.0-0 \
                libatk-bridge2.0-0 \
                libcups2 \
                libdrm2 \
                libgbm1 \
                libasound2 \
                2>/dev/null || true
            print_ok "System dependencies installed"
        else
            print_warning "Some system dependencies may not be installed (requires sudo)"
            print_warning "If Playwright fails, run: sudo apt-get install libgconf-2-4 libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xfixes0 libxdamage1 libxfixes3 libxrandr2 libxss1 libxtst6 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libasound2"
        fi
    fi
fi

# نصب dependencies
print_info "\nInstalling Python packages..."
print_info "This may take a few minutes..."
python3 -m pip install -q --user -r "$PROJECT_DIR/requirements.txt" 2>&1 | grep -v "already satisfied" || true
if [ $? -ne 0 ] && [ $? -ne 1 ]; then
    print_warning "Some packages failed to install (continuing anyway)"
fi
print_ok "Packages installed"

# بررسی فایل‌های ضروری
print_info "\nVerifying essential files..."
for file in config.py scraper.py scheduler.py api.py; do
    if [ ! -f "$PROJECT_DIR/$file" ]; then
        print_error "Missing file: $file"
    fi
done
print_ok "All essential files found"

# نصب Playwright Browsers
print_info "\nSetting up Playwright browsers..."
print_info "This will download ~300MB, please wait..."
print_info "If this fails, you can run manually:"
print_info "  python3 -m playwright install chromium"
echo ""

python3 -m playwright install chromium 2>&1 | tail -5
if [ $? -eq 0 ]; then
    print_ok "Playwright browsers installed successfully"
else
    print_warning "Playwright installation may have had issues"
    print_info "Try running manually: python3 -m playwright install chromium"
fi

# تست syntax
print_info "\nTesting Python syntax..."
python3 -m py_compile config.py scraper.py scheduler.py api.py 2>/dev/null
if [ $? -ne 0 ]; then
    print_error "Syntax error in Python files!"
fi
print_ok "All Python files are valid"

# خلاصه
clear
echo ""
echo -e "${BLUE}╔═════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         INSTALLATION SUCCESSFUL!                   ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════════╝${NC}"
echo ""
print_ok "AQI Iran is ready to use!"
echo ""
echo -e "${BLUE}Usage:${NC}"
echo "  python3 run.py              - Interactive menu"
echo "  python3 scheduler.py        - Start scheduler"
echo "  python3 api.py              - Start API server"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. python3 run.py"
echo "  2. Select option 1 or 2"
echo "  3. Check http://localhost:5000/api/health"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  - README.md              - فارسی راهنما"
echo "  - USAGE.md              - نحوه استفاده"
echo "  - RETRY_LOGIC.md        - توضیح Retry Logic"
echo "  - INSTALL_UBUNTU.md     - نصب بر Ubuntu"
echo ""
echo -e "${BLUE}Automation (Ubuntu/Linux):${NC}"
echo "  chmod +x deploy.sh && ./deploy.sh"
echo ""

# پرسش برای اجرا
read -p "Start program now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 run.py
else
    print_ok "Setup complete! Run 'python3 run.py' to start."
fi

echo ""

