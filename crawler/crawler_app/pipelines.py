# -*- coding: utf-8-
"""پایپلاین‌های پردازش داده کرالر"""

import psycopg2
import logging
from decouple import config
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)

class PostgresPipeline:
    """پایپلاین ذخیره در PostgreSQL"""
    
    def open_spider(self, spider):
        """اتصال به دیتابیس هنگام شروع اسپایدر"""
        try:
            self.connection = psycopg2.connect(
                host=config('POSTGRES_HOST', 'db'),
                database=config('POSTGRES_DB', 'propanalyzer_db'),
                user=config('POSTGRES_USER', 'propanalyst'),
                password=config('POSTGRES_PASSWORD', 'password'),
                port=config('POSTGRES_PORT', 5432)
            )
            self.cursor = self.connection.cursor()
            logger.info("اتصال به دیتابیس برقرار شد")
        except Exception as e:
            logger.error(f"خطا در اتصال به دیتابیس: {e}")
            raise
    
    def close_spider(self, spider):
        """بستن اتصال دیتابیس هنگام پایان اسپایدر"""
        self.cursor.close()
        self.connection.close()
        logger.info("اتصال به دیتابیس بسته شد")
    
    def process_item(self, item, spider):
        """پردازش و ذخیره هر آیتم در دیتابیس"""
        try:
            # بررسی تکراری نبودن داده
            if item.get('source_id'):
                self.cursor.execute(
                    "SELECT id FROM backend_propanalyzer_api_listing WHERE source_id = %s",
                    (item['source_id'],)
                )
                if self.cursor.fetchone():
                    logger.info(f"آیتم تکراری نادیده گرفته شد: {item['source_id']}")
                    raise DropItem("آیتم تکراری")
            
            # درج داده جدید
            self.cursor.execute("""
                INSERT INTO backend_propanalyzer_api_listing 
                (title, description, address, city, district, neighborhood,
                 price, area, rooms, year_built, property_type, condition,
                 contact_phone, contact_name, source, source_url, source_id,
                 is_active, created_at, updated_at, last_seen)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW())
            """, (
                item.get('title'),
                item.get('description', ''),
                item.get('address', ''),
                item.get('city', 'تهران'),
                item.get('district', ''),
                item.get('neighborhood', ''),
                self._parse_price(item.get('price')),
                self._parse_area(item.get('area')),
                self._parse_rooms(item.get('rooms')),
                item.get('year_built'),
                item.get('property_type', 'apartment'),
                item.get('condition', 'normal'),
                item.get('contact_phone', ''),
                item.get('contact_name', ''),
                spider.name,  # استفاده از نام اسپایدر به عنوان منبع
                item.get('source_url', ''),
                item.get('source_id', ''),
                True
            ))
            
            self.connection.commit()
            logger.info(f"آیتم جدید ذخیره شد: {item.get('title')}")
            
        except Exception as e:
            logger.error(f"خطا در ذخیره آیتم: {e}")
            self.connection.rollback()
            raise DropItem(f"خطا در ذخیره: {e}")
        
        return item
    
    def _parse_price(self, price_str):
        """تبدیل رشته قیمت به عدد"""
        if not price_str:
            return 0
        
        try:
            # حذف کاراکترهای غیرعددی و تبدیل به تومان
            price_str = str(price_str).replace(',', '').replace('تومان', '').strip()
            
            if 'میلیارد' in price_str:
                price = float(price_str.replace('میلیارد', '').strip()) * 1000000000
            elif 'میلیون' in price_str:
                price = float(price_str.replace('میلیون', '').strip()) * 1000000
            else:
                price = float(price_str)
            
            return int(price)
        except (ValueError, TypeError):
            return 0
    
    def _parse_area(self, area_str):
        """تبدیل رشته متراژ به عدد"""
        if not area_str:
            return 0
        
        try:
            area_str = str(area_str).replace('متر', '').replace(',', '').strip()
            return float(area_str)
        except (ValueError, TypeError):
            return 0
    
    def _parse_rooms(self, rooms_str):
        """تبدیل رشته تعداد اتاق به عدد"""
        if not rooms_str:
            return 1
        
        try:
            rooms_str = str(rooms_str).replace('اتاق', '').strip()
            return int(rooms_str)
        except (ValueError, TypeError):
            return 1

class DataCleaningPipeline:
    """پایپلاین پاکسازی داده"""
    
    def process_item(self, item, spider):
        """پاکسازی و اعتبارسنجی داده‌ها"""
        
        # پاکسازی عنوان
        if item.get('title'):
            item['title'] = item['title'].strip()
        
        # اعتبارسنجی قیمت
        price = item.get('price')
        if not price or self._parse_price(price) < 1000000:
            raise DropItem("قیمت نامعتبر")
        
        # اعتبارسنجی متراژ
        area = item.get('area')
        if not area or self._parse_area(area) < 1:
            raise DropItem("متراژ نامعتبر")
        
        return item
    
    def _parse_price(self, price_str):
        """تبدیل قیمت برای اعتبارسنجی"""
        try:
            price_str = str(price_str).replace(',', '').replace('تومان', '').strip()
            return float(price_str)
        except:
            return 0
    
    def _parse_area(self, area_str):
        """تبدیل متراژ برای اعتبارسنجی"""
        try:
            area_str = str(area_str).replace('متر', '').strip()
            return float(area_str)
        except:
            return 0