# -*- coding: utf-8 -*-
"""مسیرهای اصلی پروژه"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    """صفحه اصلی API"""
    return JsonResponse({
        'message': 'خوش آمدید به PropAnalyzer API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'listings': '/api/listings/',
            'users': '/api/users/',
            'analytics': '/api/analytics/',
            'dashboard': '/api/dashboard/',
        }
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/listings/', include('apps.listings.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
]