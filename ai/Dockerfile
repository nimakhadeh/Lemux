# استفاده از image پایه پایتون
FROM python:3.11-slim

# تنظیم محیط
WORKDIR /app

# کپی و نصب requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی پروژه
COPY . .

# اجرای سرور
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]