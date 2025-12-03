# استفاده از image پایه Node.js
FROM node:18-alpine

# تنظیم محیط
WORKDIR /app

# کپی package.json و package-lock.json
COPY package*.json ./

# نصب وابستگی‌ها
RUN npm install

# کپی تمام فایل‌های پروژه
COPY . .

# ساخت برنامه
RUN npm run build

# اجرای برنامه
CMD ["npm", "start"]

# پورت اکسپوز
EXPOSE 3000