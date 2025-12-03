# -*- coding: utf-8-
"""سریالایزرهای مربوط به املاک"""

from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    """سریالایزر اصلی برای مدل Listing"""
    
    price_per_m2 = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'address', 'city', 'district', 'neighborhood',
            'price', 'area', 'rooms', 'year_built', 'property_type', 'property_type_display',
            'condition', 'condition_display', 'contact_phone', 'contact_name',
            'source', 'source_url', 'source_id', 'price_per_m2', 'age',
            'is_active', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'price_per_m2', 'age']
    
    def get_price_per_m2(self, obj):
        """محاسبه قیمت هر متر مربع"""
        return obj.price_per_m2()
    
    def get_age(self, obj):
        """محاسبه عمر ملک"""
        return obj.age()
    
    def validate_price(self, value):
        """اعتبارسنجی قیمت"""
        if value < 1000000:
            raise serializers.ValidationError("قیمت باید حداقل ۱,۰۰۰,۰۰۰ تومان باشد")
        return value
    
    def validate_area(self, value):
        """اعتبارسنجی متراژ"""
        if value < 1:
            raise serializers.ValidationError("متراژ باید حداقل ۱ متر باشد")
        return value

class ListingAnalysisSerializer(serializers.Serializer):
    """سریالایزر برای تحلیل داده‌ها"""
    
    city = serializers.CharField()
    district = serializers.CharField()
    property_type = serializers.CharField()
    count = serializers.IntegerField()
    avg_price = serializers.FloatField()
    avg_area = serializers.FloatField()
    avg_price_per_m2 = serializers.FloatField()
    min_price = serializers.FloatField()
    max_price = serializers.FloatField()