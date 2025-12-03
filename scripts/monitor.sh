#!/bin/bash

# اسکریپت مانیتورینگ سرویس‌ها
set -e

echo "📊 مانیتورینگ سرویس‌های PropAnalyzer..."

# تابع بررسی سلامت
check_service() {
    local name=$1
    local url=$2
    
    if curl -f -s "$url" > /dev/null; then
        echo "✅ $name: Healthy"
        return 0
    else
        echo "❌ $name: Unhealthy"
        return 1
    fi
}

# بررسی سرویس‌ها
echo ""
echo "🔍 بررسی سلامت سرویس‌ها:"

check_service "Frontend" "http://localhost:3000"
check_service "Backend API" "http://localhost:8000/api/health/"
check_service "AI Service" "http://localhost:8001/health"
check_service "Database" "http://localhost:8000/api/health/"

# بررسی منابع سیستم
echo ""
echo "💻 وضعیت منابع سیستم:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" propanalyzer_backend propanalyzer_ai propanalyzer_frontend propanalyzer_db

# بررسی لاگ‌های اخیر
echo ""
echo "📋 آخرین خطاهای سیستم (۵ خط آخر):"
docker logs propanalyzer_backend --tail 5 2>&1 | grep -i error || echo "هیچ خطایی یافت نشد"

# وضعیت دیتابیس
echo ""
echo "🗄️ وضعیت دیتابیس:"
docker exec propanalyzer_db psql -U propanalyst -d propanalyzer_db -c "
SELECT 
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as size,
    (SELECT count(*) FROM backend_propanalyzer_api_listing) as total_listings
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC
LIMIT 5;"