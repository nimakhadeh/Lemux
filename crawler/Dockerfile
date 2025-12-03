# استفاده از image پایه پایتون
FROM python:3.11-slim

# تنظیم محیط
WORKDIR /app

# نصب کتابخانه‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی پروژه
COPY . .

# اجرای کرالر
CMD ["scrapy", "crawl", "divar"]