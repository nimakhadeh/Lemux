# -*- coding: utf-8 -*-
"""پنل ادمین برای مدیریت املاک"""

from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """پیکربندی پنل ادمین برای مدل Listing"""
    
    list_display = [
        'title', 'city', 'district', 'price', 'area', 
        'rooms', 'property_type', 'is_active', 'created_at'
    ]
    
    list_filter = [
        'city', 'district', 'property_type', 'condition', 
        'is_active', 'is_verified', 'source'
    ]
    
    search_fields = ['title', 'address', 'district', 'contact_name']
    
    readonly_fields = ['created_at', 'updated_at', 'last_seen']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description', 'is_active', 'is_verified')
        }),
        ('آدرس', {
            'fields': ('address', 'city', 'district', 'neighborhood')
        }),
        ('مشخصات فنی', {
            'fields': ('price', 'area', 'rooms', 'year_built')
        }),
        ('نوع و وضعیت', {
            'fields': ('property_type', 'condition')
        }),
        ('اطلاعات تماس', {
            'fields': ('contact_name', 'contact_phone')
        }),
        ('منبع داده', {
            'fields': ('source', 'source_url', 'source_id')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at', 'last_seen')
        }),
    )
    
    actions = ['activate_listings', 'deactivate_listings']
    
    def activate_listings(self, request, queryset):
        """فعال کردن املاک انتخاب شده"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} ملک فعال شد')
    
    def deactivate_listings(self, request, queryset):
        """غیرفعال کردن املاک انتخاب شده"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} ملک غیرفعال شد')
    
    activate_listings.short_description = "فعال کردن املاک انتخاب شده"
    deactivate_listings.short_description = "غیرفعال کردن املاک انتخاب شده"