#!/bin/bash

# اسکریپت پاکسازی سیستم
set -e

echo "🧹 شروع پاکسازی سیستم..."

# توقف و حذف کانتینرها
echo "🛑 توقف و حذف کانتینرها..."
docker-compose down

# حذف volume ها
echo "🗑️ حذف volume ها..."
docker volume rm propanalyzer_postgres_data propanalyzer_redis_data propanalyzer_static_volume 2>/dev/null || true

# حذف image ها
echo "🗑️ حذف image ها..."
docker rmi propanalyzer_backend propanalyzer_ai propanalyzer_frontend propanalyzer_crawler 2>/dev/null || true

# پاکسازی کش Docker
echo "🧼 پاکسازی کش Docker..."
docker system prune -f

# حذف فایل‌های موقت
echo "📁 حذف فایل‌های موقت..."
rm -rf logs/* tmp/*

echo ""
echo "✅ پاکسازی کامل شد"
echo "💡 برای راه‌اندازی مجدد از اسکریپت setup.sh استفاده کنید"