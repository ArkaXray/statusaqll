#!/bin/bash

# Fix Playwright Issue
# این اسکریپت مشکل Playwright رو حل می‌کند

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\n${BLUE}╔═════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Fix Playwright Browsers                           ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════════╝${NC}\n"

# Step 1: حذف cache
echo -e "${YELLOW}Step 1: Removing Playwright cache...${NC}"
rm -rf ~/.cache/ms-playwright/ 2>/dev/null || true
echo -e "${GREEN}[✓] Cache removed${NC}"

# Step 2: نصب system dependencies
echo -e "\n${YELLOW}Step 2: Installing system dependencies...${NC}"

if command -v apt-get &> /dev/null; then
    echo "Detected: Ubuntu/Debian"
    echo "This may require sudo password..."
    
    sudo apt-get update -qq 2>/dev/null || true
    
    echo "Installing dependencies..."
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
    
    echo -e "${GREEN}[✓] Dependencies installed${NC}"
else
    echo -e "${YELLOW}[!] Manual system dependencies required${NC}"
    echo "Please install: libgconf-2-4 libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xfixes0 libxdamage1 libxfixes3 libxrandr2 libxss1 libxtst6 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libasound2"
fi

# Step 3: نصب Playwright
echo -e "\n${YELLOW}Step 3: Installing Playwright browsers...${NC}"
echo "This will download ~300MB, please wait..."
echo ""

python3 -m playwright install chromium

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}[✓] Playwright installed successfully!${NC}"
else
    echo -e "\n${RED}[✗] Playwright installation failed${NC}"
    echo "Try running: python3 -m playwright install chromium --verbose"
    exit 1
fi

# Step 4: نصب additional browsers (optional)
echo -e "\n${YELLOW}Step 4: Install additional browsers? (y/n)${NC}"
read -p ">>> " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m playwright install
    echo -e "${GREEN}[✓] All browsers installed${NC}"
fi

# Final
echo -e "\n${BLUE}╔═════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}[✓] Fix Complete!${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════════╝${NC}"
echo ""
echo "You can now run:"
echo "  python3 run.py"
echo "  python3 scheduler.py"
echo "  python3 api.py"
echo ""
