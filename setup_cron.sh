#!/bin/bash

# AQI Iran - Cron Job Setup Script
# این اسکریپت برای اجرای خودکار scheduler هر 30 دقیقه

set -e

# رنگ‌ها برای خروجی
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}AQI Iran - Cron Setup${NC}"
echo -e "${BLUE}================================${NC}\n"

# دریافت مسیر پروژه
PROJECT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH=$(which python3)

if [ -z "$PYTHON_PATH" ]; then
    echo -e "${RED}❌ Python3 یافت نشد!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 یافت شد:${NC} $PYTHON_PATH"
echo -e "${GREEN}✅ مسیر پروژه:${NC} $PROJECT_PATH\n"

# ایجاد فایل cron temp
CRON_FILE="/tmp/aqi_cron_$$.txt"

# دریافت cron فعلی
crontab -l > "$CRON_FILE" 2>/dev/null || true

# بررسی اگر job قبلا اضافه شده است
if grep -q "AQI_Scheduler" "$CRON_FILE"; then
    echo -e "${YELLOW}⚠️  Cron job قبلا وجود دارد${NC}"
    echo -e "${YELLOW}حذف می‌کنم...${NC}\n"
    grep -v "AQI_Scheduler" "$CRON_FILE" > "$CRON_FILE.tmp"
    mv "$CRON_FILE.tmp" "$CRON_FILE"
fi

# اضافه کردن cron job جدید
# هر 30 دقیقه: */30 * * * *
cat >> "$CRON_FILE" << EOF

# AQI_Scheduler - هر 30 دقیقه جمع‌آوری داده AQI
*/30 * * * * cd $PROJECT_PATH && $PYTHON_PATH scheduler.py >> logs/cron.log 2>&1

EOF

# نصب cron job
crontab "$CRON_FILE"

# پاک‌سازی
rm "$CRON_FILE"

echo -e "${GREEN}✅ Cron job با موفقیت نصب شد!${NC}\n"

echo -e "${BLUE}📋 جزئیات Cron:${NC}"
echo -e "   هر 30 دقیقه: */30 * * * *"
echo -e "   دستور: cd $PROJECT_PATH && $PYTHON_PATH scheduler.py"
echo -e "   لاگ: $PROJECT_PATH/logs/cron.log\n"

echo -e "${YELLOW}📝 فرمان‌های کاربردی:${NC}"
echo "   crontab -l           # نمایش تمام cron jobs"
echo "   crontab -e           # ویرایش cron jobs"
echo "   crontab -r           # حذف تمام cron jobs"
echo ""

# نمایش cron jobs
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Cron Jobs فعلی:${NC}"
echo -e "${BLUE}================================${NC}\n"
crontab -l | grep -v "^#" | grep -v "^$"

echo ""
echo -e "${GREEN}✅ Setup تکمیل شد!${NC}\n"
