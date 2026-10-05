# -*- coding: utf-8 -*-
"""URL routes for dashboard and health checks."""

from django.urls import path
from .views import DashboardSummaryView, health_check

app_name = "dashboard"

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="summary"),
    path("health/", health_check, name="health"),
]
