# -*- coding: utf-8-
"""تنظیمات Scrapy"""

import os
from decouple import config

# تنظیمات اصلی
BOT_NAME = 'propanalyzer_crawler'
SPIDER_MODULES = ['crawler_app.spiders']
NEWSPIDER_MODULE = 'crawler_app.spiders'

# ربات‌های txt
ROBOTSTXT_OBEY = False

# تنظیمات دانلود
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# کوکی‌ها
COOKIES_ENABLED = False

# کاربر-ایجنت
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# پایپلاین‌ها
ITEM_PIPELINES = {
    'crawler_app.pipelines.DataCleaningPipeline': 100,
    'crawler_app.pipelines.PostgresPipeline': 800,
}

# تنظیمات لاگ
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(levelname)s: %(message)s'

# تنظیمات ریت لیمیت
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# تنظیمات HTTP
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600

# تنظیمات دیتابیس
POSTGRES_HOST = config('POSTGRES_HOST', 'db')
POSTGRES_DB = config('POSTGRES_DB', 'propanalyzer_db')
POSTGRES_USER = config('POSTGRES_USER', 'propanalyst')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', 'password')
POSTGRES_PORT = config('POSTGRES_PORT', 5432)