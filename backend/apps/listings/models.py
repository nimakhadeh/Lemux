# -*- coding: utf-8 -*-
"""مدل‌های مربوط به املاک"""

from django.db import models
from django.core.validators import MinValueValidator

class Listing(models.Model):
    """مدل اصلی برای ذخیره اطلاعات ملک"""
    
    # اطلاعات اصلی
    title = models.CharField(max_length=200, verbose_name='عنوان آگهی')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    # آدرس
    address = models.TextField(verbose_name='آدرس کامل')
    city = models.CharField(max_length=100, verbose_name='شهر')
    district = models.CharField(max_length=100, verbose_name='محله')
    neighborhood = models.CharField(max_length=100, blank=True, verbose_name='محله')
    
    # مشخصات فنی
    price = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='قیمت (تومان)'
    )
    area = models.FloatField(
        validators=[MinValueValidator(1)],
        verbose_name='متراژ (متر مربع)'
    )
    rooms = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='تعداد اتاق'
    )
    year_built = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='سال ساخت'
    )
    
    # نوع ملک
    PROPERTY_TYPES = [
        ('apartment', 'آپارتمان'),
        ('villa', 'ویلا'),
        ('office', 'دفتر کار'),
        ('store', 'مغازه'),
        ('land', 'زمین'),
    ]
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
        default='apartment',
        verbose_name='نوع ملک'
    )
    
    # وضعیت ملک
    CONDITION_TYPES = [
        ('new', 'نوساز'),
        ('renovated', 'بازسازی شده'),
        ('normal', 'معمولی'),
        ('old', 'قدیمی'),
    ]
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_TYPES,
        default='normal',
        verbose_name='وضعیت ملک'
    )
    
    # اطلاعات تماس
    contact_phone = models.CharField(max_length=15, blank=True, verbose_name='تلفن تماس')
    contact_name = models.CharField(max_length=100, blank=True, verbose_name='نام تماس')
    
    # منبع داده
    SOURCE_TYPES = [
        ('divar', 'دیوار'),
        ('sheypoor', 'شیپور'),
        ('ihome', 'آی‌هوم'),
        ('manual', 'دستی'),
    ]
    source = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        default='manual',
        verbose_name='منبع داده'
    )
    source_url = models.URLField(blank=True, verbose_name='لینک منبع')
    source_id = models.CharField(max_length=100, blank=True, verbose_name='شناسه در منبع')
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    last_seen = models.DateTimeField(auto_now=True, verbose_name='آخرین مشاهده')
    
    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_verified = models.BooleanField(default=False, verbose_name='تأیید شده')
    
    class Meta:
        verbose_name = 'ملک'
        verbose_name_plural = 'املاک'
        ordering = ['-created_at']
        db_table = 'backend_propanalyzer_api_listing'
        indexes = [
            models.Index(fields=['city', 'district'], name='listing_city_district_idx'),
            models.Index(fields=['price'], name='listing_price_idx'),
            models.Index(fields=['created_at'], name='listing_created_idx'),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.price:,} تومان"
    
    def price_per_m2(self):
        """محاسبه قیمت هر متر مربع"""
        if self.area and self.area > 0:
            return int(self.price / self.area)
        return 0
    
    def get_absolute_url(self):
        """URL مطلق برای این ملک"""
        return f"/api/listings/{self.id}/"
    
    def age(self):
        """محاسبه عمر ملک"""
        if self.year_built:
            from datetime import datetime
            current_year = datetime.now().year
            return current_year - self.year_built
        return None

# نمونه داده‌های تستی
SAMPLE_LISTINGS = [
    {
        'title': 'آپارتمان ۸۵ متری نوساز در الهیه',
        'address': 'تهران، الهیه، خیابان فرشته',
        'city': 'تهران',
        'district': 'الهیه',
        'price': 8500000000,
        'area': 85,
        'rooms': 2,
        'year_built': 1400,
        'property_type': 'apartment',
        'condition': 'new',
        'source': 'manual'
    },
    {
        'title': 'ویلا ۲۰۰ متری در فرمانیه',
        'address': 'تهران، فرمانیه، خیابان باهنر',
        'city': 'تهران', 
        'district': 'فرمانیه',
        'price': 25000000000,
        'area': 200,
        'rooms': 4,
        'year_built': 1395,
        'property_type': 'villa',
        'condition': 'renovated',
        'source': 'manual'
    },
    {
        'title': 'آپارتمان ۱۲۰ متری در نیاوران',
        'address': 'تهران، نیاوران، خیابان یاسر',
        'city': 'تهران',
        'district': 'نیاوران', 
        'price': 12000000000,
        'area': 120,
        'rooms': 3,
        'year_built': 1398,
        'property_type': 'apartment',
        'condition': 'normal',
        'source': 'manual'
    }
]