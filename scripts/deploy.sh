#!/bin/bash

# اسکریپت دپلوی برای production
set -e

echo "🚀 شروع دپلوی PropAnalyzer..."

# بررسی محیط
if [ -z "$DEPLOY_ENV" ]; then
    DEPLOY_ENV="production"
fi

echo "🔧 محیط دپلوی: $DEPLOY_ENV"

# متوقف کردن سرویس‌های قبلی
echo "🛑 متوقف کردن سرویس‌های قبلی..."
docker-compose down

# دریافت آخرین تغییرات
echo "📥 دریافت آخرین تغییرات..."
git pull origin main

# ساخت image های جدید
echo "🐳 ساخت image های جدید..."
docker-compose build --no-cache

# اجرای سرویس‌ها
echo "▶️ اجرای سرویس‌ها..."
docker-compose up -d

# اجرای migrations
echo "📦 اجرای migrations..."
docker exec propanalyzer_backend python manage.py migrate

# جمع‌آوری فایل‌های استاتیک
echo "📁 جمع‌آوری فایل‌های استاتیک..."
docker exec propanalyzer_backend python manage.py collectstatic --noinput

# آموزش مدل
echo "🤖 آموزش مدل با داده‌های جدید..."
curl -X POST http://localhost:8001/health/train

# بررسی سلامت سرویس‌ها
echo "🔍 بررسی سلامت سرویس‌ها..."
sleep 30

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ دپلوی با موفقیت انجام شد"
else
    echo "❌ خطا در دپلوی"
    exit 1
fi

echo ""
echo "🎉 دپلوی کامل شد!"
echo "📊 سرویس در دسترس است: http://localhost:3000"