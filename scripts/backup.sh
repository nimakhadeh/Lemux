#!/bin/bash

# اسکریپت پشتیبان‌گیری از داده‌ها
set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="propanalyzer_backup_$TIMESTAMP.sql"

echo "💾 شروع پشتیبان‌گیری از داده‌ها..."

# ایجاد پوشه پشتیبان
mkdir -p $BACKUP_DIR

# پشتیبان‌گیری از دیتابیس
echo "📦 پشتیبان‌گیری از دیتابیس..."
docker exec propanalyzer_db pg_dump -U propanalyst propanalyzer_db > "$BACKUP_DIR/$BACKUP_FILE"

# فشرده‌سازی
echo "🗜️ فشرده‌سازی پشتیبان..."
gzip "$BACKUP_DIR/$BACKUP_FILE"

# حذف پشتیبان‌های قدیمی (بیش از ۷ روز)
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo ""
echo "✅ پشتیبان‌گیری با موفقیت انجام شد"
echo "📁 فایل پشتیبان: $BACKUP_DIR/${BACKUP_FILE}.gz"
echo "💡 برای بازگردانی از دستور زیر استفاده کنید:"
echo "   gunzip -c $BACKUP_DIR/${BACKUP_FILE}.gz | docker exec -i propanalyzer_db psql -U propanalyst propanalyzer_db"