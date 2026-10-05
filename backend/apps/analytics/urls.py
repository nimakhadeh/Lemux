# -*- coding: utf-8 -*-
"""URL routes for market analytics."""

from django.urls import path
from .views import CityAnalysisView, DistrictAnalysisView, OverviewView, PropertyTypeAnalysisView

app_name = "analytics"

urlpatterns = [
    path("overview/", OverviewView.as_view(), name="overview"),
    path("cities/", CityAnalysisView.as_view(), name="cities"),
    path("property-types/", PropertyTypeAnalysisView.as_view(), name="property-types"),
    path("districts/", DistrictAnalysisView.as_view(), name="districts"),
]
