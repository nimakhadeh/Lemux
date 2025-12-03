# -*- coding: utf-8 -*-
"""اسپایدر برای سایت شیپور"""

import scrapy
import re
from urllib.parse import urljoin
from crawler_app.items import PropertyItem

class SheypoorSpider(scrapy.Spider):
    """اسپایدر جمع‌آوری داده از شیپور"""
    
    name = "sheypoor"
    allowed_domains = ["sheypoor.com"]
    
    # شهرهای هدف
    CITIES = [
        "%D8%AA%D9%87%D8%B1%D8%A7%D9%86",  # تهران
        "مشهد",
        "اصفهان", 
        "شیراز",
        "تبریز"
    ]
    
    def start_requests(self):
        """شروع درخواست‌ها"""
        for city in self.CITIES:
            url = f"https://www.sheypoor.com/s/{city}/املاک-مسکن/آپارتمان-خانه-فروش"
            yield scrapy.Request(
                url=url,
                callback=self.parse_city_page,
                meta={'city': city}
            )
    
    def parse_city_page(self, response):
        """پارس کردن صفحه شهر"""
        city = response.meta['city']
        
        # استخراج لینک‌های آگهی‌ها
        post_links = response.css('a.serp-item::attr(href)').getall()
        
        for link in post_links:
            absolute_url = urljoin('https://www.sheypoor.com', link)
            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse_property_page,
                meta={'city': city}
            )
        
        # صفحه بعدی
        next_page = response.css('a.pagination-next::attr(href)').get()
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
        item['title'] = response.css('h1.title::text').get()
        item['description'] = response.css('.description::text').get()
        
        # آدرس
        item['city'] = self._normalize_city(response.meta['city'])
        address_element = response.css('.location::text').get()
        if address_element:
            item['address'] = address_element.strip()
        
        # استخراج قیمت
        price_element = response.css('.price::text').get()
        if price_element:
            item['price'] = price_element.strip()
        
        # استخراج مشخصات از لیست اطلاعات
        specs = {}
        for spec_row in response.css('.specs tr'):
            label = spec_row.css('th::text').get()
            value = spec_row.css('td::text').get()
            if label and value:
                specs[label.strip()] = value.strip()
        
        # نگاشت مشخصات به فیلدهای ما
        if 'متراژ' in specs:
            item['area'] = specs['متراژ']
        if 'اتاق' in specs:
            item['rooms'] = specs['اتاق']
        if 'سال ساخت' in specs:
            item['year_built'] = specs['سال ساخت']
        if 'محله' in specs:
            item['neighborhood'] = specs['محله']
        
        # اطلاعات تماس
        contact_name = response.css('.contact-name::text').get()
        if contact_name:
            item['contact_name'] = contact_name.strip()
        
        contact_phone = response.css('.phone::text').get()
        if contact_phone:
            item['contact_phone'] = contact_phone.strip()
        
        # منبع
        item['source'] = 'sheypoor'
        item['source_url'] = response.url
        item['source_id'] = response.url.split('/')[-1]
        
        # نوع ملک
        item['property_type'] = 'apartment'
        
        yield item
    
    def _normalize_city(self, city_url):
        """نرمال‌سازی نام شهر"""
        city_map = {
            '%D8%AA%D9%87%D8%B1%D8%A7%D9%86': 'تهران',
            'مشهد': 'مشهد',
            'اصفهان': 'اصفهان',
            'شیراز': 'شیراز', 
            'تبریز': 'تبریز'
        }
        return city_map.get(city_url, city_url)