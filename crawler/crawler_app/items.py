# -*- coding: utf-8 -*-
"""آیتم‌های Scrapy برای داده‌های املاک"""

import scrapy

class PropertyItem(scrapy.Item):
    """آیتم برای ذخیره اطلاعات ملک"""
    
    # اطلاعات اصلی
    title = scrapy.Field()
    description = scrapy.Field()
    
    # آدرس
    address = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    neighborhood = scrapy.Field()
    
    # مشخصات فنی
    price = scrapy.Field()
    area = scrapy.Field()
    rooms = scrapy.Field()
    year_built = scrapy.Field()
    
    # نوع و وضعیت
    property_type = scrapy.Field()
    condition = scrapy.Field()
    
    # اطلاعات تماس
    contact_phone = scrapy.Field()
    contact_name = scrapy.Field()
    
    # منبع
    source = scrapy.Field()
    source_url = scrapy.Field()
    source_id = scrapy.Field()
    
    # متا داده
    crawled_at = scrapy.Field()
    is_active = scrapy.Field()