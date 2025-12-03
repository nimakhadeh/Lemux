# -*- coding: utf-8 -*-
"""ویوهای مربوط به املاک"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count, Min, Max
from django.http import JsonResponse

from .models import Listing, SAMPLE_LISTINGS
from .serializers import ListingSerializer, ListingAnalysisSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """ویوست کامل برای مدیریت املاک"""
    
    queryset = Listing.objects.all().order_by('-created_at')
    serializer_class = ListingSerializer
    
    # فیلترها و جستجو
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'district', 'property_type', 'rooms', 'condition']
    search_fields = ['title', 'address', 'district', 'neighborhood']
    ordering_fields = ['price', 'area', 'created_at', 'year_built']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """کوئری‌ست با فیلترهای پیشرفته"""
        queryset = super().get_queryset()
        
        # فیلترهای قیمت
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # فیلتر متراژ
        min_area = self.request.query_params.get('min_area')
        max_area = self.request.query_params.get('max_area')
        
        if min_area:
            queryset = queryset.filter(area__gte=min_area)
        if max_area:
            queryset = queryset.filter(area__lte=max_area)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """آمار کلی املاک"""
        stats = Listing.objects.aggregate(
            total_listings=Count('id'),
            avg_price=Avg('price'),
            min_price=Min('price'),
            max_price=Max('price'),
            avg_area=Avg('area'),
        )
        
        # آمار به تفکیک شهر
        city_stats = Listing.objects.values('city').annotate(
            count=Count('id'),
            avg_price=Avg('price'),
            avg_price_per_m2=Avg('price') / Avg('area')
        )
        
        return Response({
            'overall': stats,
            'by_city': list(city_stats)
        })
    
    @action(detail=False, methods=['get'])
    def analysis(self, request):
        """تحلیل قیمت‌ها"""
        analysis_data = Listing.objects.filter(area__gt=0).values(
            'city', 'district', 'property_type'
        ).annotate(
            count=Count('id'),
            avg_price=Avg('price'),
            avg_area=Avg('area'),
            avg_price_per_m2=Avg('price') / Avg('area'),
            min_price=Min('price'),
            max_price=Max('price')
        )
        
        serializer = ListingAnalysisSerializer(analysis_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def create_sample_data(self, request):
        """ایجاد داده‌های نمونه برای تست"""
        for listing_data in SAMPLE_LISTINGS:
            Listing.objects.create(**listing_data)
        
        return Response({
            'message': 'داده‌های نمونه با موفقیت ایجاد شدند',
            'count': len(SAMPLE_LISTINGS)
        }, status=status.HTTP_201_CREATED)

def listing_stats_api(request):
    """API ساده برای آمار"""
    total = Listing.objects.count()
    avg_price = Listing.objects.aggregate(avg=Avg('price'))['avg'] or 0
    cities = Listing.objects.values('city').annotate(count=Count('id'))
    
    return JsonResponse({
        'total_listings': total,
        'average_price': int(avg_price),
        'cities': list(cities)
    })