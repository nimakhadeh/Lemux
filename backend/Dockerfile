# استفاده از image پایه پایتون
FROM python:3.11-slim

# تنظیم محیط
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# ایجاد مسیر کاری
WORKDIR /app

# کپی و نصب requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی پروژه
COPY . .

# ایجاد volume برای توسعه
VOLUME /app

# اجرای migrations و سرور
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]