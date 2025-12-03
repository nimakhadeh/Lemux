# -*- coding: utf-8 -*-
"""مسیرهای مربوط به املاک"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, listing_stats_api

router = DefaultRouter()
router.register('', ListingViewSet, basename='listing')

urlpatterns = [
    path('stats/', listing_stats_api, name='listing-stats'),
    path('', include(router.urls)),
]