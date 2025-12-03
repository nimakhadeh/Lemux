# -*- coding: utf-8 -*-
"""مدیریت اتصال به دیتابیس"""

import psycopg2
from psycopg2.extras import RealDictCursor
from decouple import config
import logging

logger = logging.getLogger(__name__)

class Database:
    """کلاس مدیریت اتصال به دیتابیس"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """اتصال به دیتابیس"""
        try:
            self.connection = psycopg2.connect(
                host=config('POSTGRES_HOST', 'db'),
                database=config('POSTGRES_DB', 'propanalyzer_db'),
                user=config('POSTGRES_USER', 'propanalyst'),
                password=config('POSTGRES_PASSWORD', 'password'),
                port=config('POSTGRES_PORT', 5432),
                cursor_factory=RealDictCursor
            )
            self.cursor = self.connection.cursor()
            logger.info("اتصال به دیتابیس AI برقرار شد")
            return True
        except Exception as e:
            logger.error(f"خطا در اتصال به دیتابیس: {e}")
            return False
    
    def disconnect(self):
        """قطع اتصال از دیتابیس"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("اتصال به دیتابیس AI بسته شد")
    
    def execute_query(self, query, params=None):
        """اجرای کوئری و بازگشت نتایج"""
        try:
            if not self.connection or self.connection.closed:
                self.connect()
            
            self.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
                
        except Exception as e:
            logger.error(f"خطا در اجرای کوئری: {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def get_listings_data(self, limit=1000):
        """دریافت داده‌های املاک از دیتابیس"""
        query = """
        SELECT 
            id, title, price, area, rooms, year_built,
            city, district, property_type, condition
        FROM backend_propanalyzer_api_listing 
        WHERE price > 0 AND area > 0 AND is_active = true
        ORDER BY created_at DESC 
        LIMIT %s
        """
        
        results = self.execute_query(query, (limit,))
        return list(results) if results else []

# نمونه global از دیتابیس
db = Database()

def get_db():
    """دریافت نمونه دیتابیس برای dependency injection"""
    return db