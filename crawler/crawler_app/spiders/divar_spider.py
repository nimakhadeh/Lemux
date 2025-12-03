# -*- coding: utf-8-
"""اسپایدر برای سایت دیوار"""

import scrapy
import json
import re
from urllib.parse import urljoin
from crawler_app.items import PropertyItem

class DivarSpider(scrapy.Spider):
    """اسپایدر جمع‌آوری داده از دیوار"""
    
    name = "divar"
    allowed_domains = ["divar.ir"]
    
    # شهرهای هدف
    CITIES = [
        "tehran",
        "mashhad", 
        "isfahan",
        "shiraz",
        "tabriz"
    ]
    
    def start_requests(self):
        """شروع درخواست‌ها برای شهرهای مختلف"""
        for city in self.CITIES:
            url = f"https://divar.ir/s/{city}/apartments"
            yield scrapy.Request(
                url=url,
                callback=self.parse_city_page,
                meta={'city': city}
            )
    
    def parse_city_page(self, response):
        """پارس کردن صفحه شهر"""
        city = response.meta['city']
        
        # استخراج لینک‌های آگهی‌ها
        post_links = response.css('a.kt-post-card::attr(href)').getall()
        
        for link in post_links:
            absolute_url = urljoin(response.url, link)
            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse_property_page,
                meta={'city': city}
            )
        
        # صفحه بعدی
        next_page = response.css('a.kt-pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_city_page,
                meta={'city': city}
            )
    
    def parse_property_page(self, response):
        """پارس کردن صفحه جزئیات ملک"""
        item = PropertyItem()
        
        # اطلاعات اصلی
        item['title'] = response.css('h1.kt-page-title::text').get()
        item['description'] = ' '.join(response.css('.kt-description-row__text::text').getall())
        
        # آدرس
        item['city'] = response.meta['city']
        item['address'] = response.css('.kt-page-title__subtitle::text').get()
        
        # استخراج اطلاعات از داده‌های ساختاریافته
        script_data = response.css('script[type="application/ld+json"]::text').get()
        if script_data:
            try:
                data = json.loads(script_data)
                if 'address' in data:
                    item['address'] = data['address'].get('streetAddress', '')
            except json.JSONDecodeError:
                pass
        
        # استخراج مشخصات از کارت‌های اطلاعات
        for info_card in response.css('.kt-base-row__end'):
            label = info_card.css('.kt-base-row__title::text').get()
            value = info_card.css('.kt-base-row__value::text').get()
            
            if label and value:
                if 'قیمت' in label:
                    item['price'] = value
                elif 'متراژ' in label:
                    item['area'] = value
                elif 'اتاق' in label:
                    item['rooms'] = value
                elif 'ساخت' in label:
                    item['year_built'] = value
                elif 'محله' in label:
                    item['neighborhood'] = value
        
        # اطلاعات تماس
        item['contact_name'] = response.css('.kt-page-title__subtitle::text').get()
        
        # منبع
        item['source'] = 'divar'
        item['source_url'] = response.url
        item['source_id'] = response.url.split('/')[-1]
        
        # نوع ملک
        item['property_type'] = 'apartment'
        
        yield item

class DivarRentSpider(DivarSpider):
    """اسپایدر برای اجاره‌ای‌های دیوار"""
    
    name = "divar_rent"
    
    def start_requests(self):
        """شروع درخواست‌ها برای اجاره‌ای‌ها"""
        for city in self.CITIES:
            url = f"https://divar.ir/s/{city}/apartments-rent"
            yield scrapy.Request(
                url=url,
                callback=self.parse_city_page,
                meta={'city': city}
            )