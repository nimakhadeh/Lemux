# 1. CMD یا PowerShell را به عنوان Administrator باز کن
# 2. به پوشه docker برو
cd C:\PropAnalyzer\docker

# 3. اجرای پروژه
docker-compose up --build

# یا برای اجرای در background:
docker-compose up --build -d