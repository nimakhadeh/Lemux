#!/bin/bash

# اسکریپت راه‌اندازی پروژه PropAnalyzer
set -e

echo "🚀 شروع راه‌اندازی PropAnalyzer..."

# بررسی وجود Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker نصب نیست. لطفاً ابتدا Docker را نصب کنید."
    exit 1
fi

# بررسی وجود Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose نصب نیست. لطفاً ابتدا Docker Compose را نصب کنید."
    exit 1
fi

# ایجاد پوشه‌های لازم
echo "📁 ایجاد پوشه‌های مورد نیاز..."
mkdir -p logs
mkdir -p data

# کپی فایل محیطی
if [ ! -f .env ]; then
    echo "📝 کپی فایل محیطی..."
    cp .env.example .env
    echo "✅ فایل .env ایجاد شد. لطفاً مقادیر را تنظیم کنید."
fi

# ساخت و اجرای کانتینرها
echo "🐳 ساخت و اجرای کانتینرها..."
docker-compose up --build -d

# منتظر ماندن برای آماده شدن سرویس‌ها
echo "⏳ منتظر آماده شدن سرویس‌ها..."
sleep 30

# بررسی سلامت سرویس‌ها
echo "🔍 بررسی سلامت سرویس‌ها..."

# بررسی بک‌اند
if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
    echo "✅ سرویس بک‌اند آماده است"
else
    echo "❌ سرویس بک‌اند مشکل دارد"
fi

# بررسی AI
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ سرویس هوش مصنوعی آماده است"
else
    echo "❌ سرویس هوش مصنوعی مشکل دارد"
fi

# بررسی فرانت‌اند
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ سرویس فرانت‌اند آماده است"
else
    echo "❌ سرویس فرانت‌اند مشکل دارد"
fi

echo ""
echo "🎉 راه‌اندازی کامل شد!"
echo ""
echo "📊 دسترسی به سرویس‌ها:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   AI API: http://localhost:8001"
echo "   Database: localhost:5432"
echo ""
echo "🔧 دستورات مفید:"
echo "   مشاهده لاگ‌ها: docker-compose logs -f"
echo "   توقف سرویس‌ها: docker-compose down"
echo "   بروزرسانی: docker-compose up --build -d"
echo ""
echo "📚 مستندات:"
echo "   برای اطلاعات بیشتر فایل README.md را مطالعه کنید"