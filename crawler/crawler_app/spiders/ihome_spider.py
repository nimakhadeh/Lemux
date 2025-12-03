# -*- coding: utf-8 -*-
"""اسپایدر برای سایت آی‌هوم"""

import scrapy
import json
from urllib.parse import urljoin
from crawler_app.items import PropertyItem

class IHomeSpider(scrapy.Spider):
    """اسپایدر جمع‌آوری داده از آی‌هوم"""
    
    name = "ihome"
    allowed_domains = ["ihome.ir"]
    
    def start_requests(self):
        """شروع درخواست‌ها"""
        cities = ["tehran", "mashhad", "isfahan", "shiraz", "tabriz"]
        
        for city in cities:
            # فروش
            yield scrapy.Request(
                url=f"https://ihome.ir/sell/{city}",
                callback=self.parse_city_page,
                meta={'city': city, 'type': 'sell'}
            )
            # اجاره
            yield scrapy.Request(
                url=f"https://ihome.ir/rent/{city}",
                callback=self.parse_city_page, 
                meta={'city': city, 'type': 'rent'}
            )
    
    def parse_city_page(self, response):
        """پارس کردن صفحه شهر"""
        city = response.meta['city']
        listing_type = response.meta['type']
        
        # استخراج لینک‌های آگهی‌ها
        property_cards = response.css('.property-card')
        
        for card in property_cards:
            link = card.css('a::attr(href)').get()
            if link:
                absolute_url = urljoin(response.url, link)
                yield scrapy.Request(
                    url=absolute_url,
                    callback=self.parse_property_page,
                    meta={'city': city, 'type': listing_type}
                )
        
        # صفحه بعدی
        next_page = response.css('.pagination-next a::attr(href)').get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_city_page,
                meta={'city': city, 'type': listing_type}
            )
    
    def parse_property_page(self, response):
        """پارس کردن صفحه جزئیات ملک"""
        item = PropertyItem()
        
        # اطلاعات اصلی
        item['title'] = response.css('h1.property-title::text').get()
        item['description'] = ' '.join(response.css('.property-description::text').getall())
        
        # آدرس
        item['city'] = self._normalize_city(response.meta['city'])
        address = response.css('.property-address::text').get()
        if address:
            item['address'] = address.strip()
        
        # استخراج اطلاعات از داده‌های ساختاریافته
        script_data = response.css('script[type="application/ld+json"]::text').get()
        if script_data:
            try:
                data = json.loads(script_data)
                if 'address' in data:
                    item['address'] = data['address'].get('streetAddress', '')
                if 'price' in data:
                    item['price'] = data['price']
            except json.JSONDecodeError:
                pass
        
        # استخراج مشخصات
        for detail in response.css('.property-details li'):
            text = detail.css('::text').get()
            if text:
                if 'متر' in text and 'متراژ' not in text:
                    item['area'] = text.replace('متر', '').strip()
                elif 'اتاق' in text:
                    item['rooms'] = text.replace('اتاق', '').strip()
                elif 'سال' in text and 'ساخت' in text:
                    item['year_built'] = text.replace('سال ساخت', '').strip()
        
        # قیمت
        price_element = response.css('.property-price::text').get()
        if price_element:
            item['price'] = price_element.strip()
        
        # اطلاعات تماس
        contact_info = response.css('.contact-info::text').get()
        if contact_info:
            item['contact_name'] = contact_info.strip()
        
        # منبع
        item['source'] = 'ihome'
        item['source_url'] = response.url
        item['source_id'] = response.url.split('/')[-1]
        
        # نوع ملک
        item['property_type'] = 'apartment'
        
        yield item
    
    def _normalize_city(self, city):
        """نرمال‌سازی نام شهر"""
        city_map = {
            'tehran': 'تهران',
            'mashhad': 'مشهد',
            'isfahan': 'اصفهان',
            'shiraz': 'شیراز',
            'tabriz': 'تبریز'
        }
        return city_map.get(city, city)