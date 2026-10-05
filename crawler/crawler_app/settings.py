# -*- coding: utf-8 -*-
"""تنظیمات Scrapy"""

from decouple import config

BOT_NAME = 'propanalyzer_crawler'
SPIDER_MODULES = ['crawler_app.spiders']
NEWSPIDER_MODULE = 'crawler_app.spiders'
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 1
COOKIES_ENABLED = False
USER_AGENT = 'PropAnalyzer/1.0 (+https://github.com/nimakhadeh/Lemux)'
ITEM_PIPELINES = {
    'crawler_app.pipelines.DataCleaningPipeline': 100,
    'crawler_app.pipelines.PostgresPipeline': 800,
}
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(levelname)s: %(message)s'
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600

POSTGRES_HOST = config('POSTGRES_HOST', 'db')
POSTGRES_DB = config('POSTGRES_DB', 'propanalyzer_db')
POSTGRES_USER = config('POSTGRES_USER', 'propanalyst')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_PORT = config('POSTGRES_PORT', 5432)
