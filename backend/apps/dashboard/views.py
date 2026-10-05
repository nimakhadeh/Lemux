# -*- coding: utf-8 -*-
"""Dashboard and health-check endpoints."""

from django.db import connection
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.listings.models import Listing


class DashboardSummaryView(APIView):
    """Compact read-only payload for the dashboard UI."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Listing.objects.filter(is_active=True, price__gt=0, area__gt=0)
        stats = qs.aggregate(
            total=Count("id"),
            verified=Count("id", filter=Q(is_verified=True)),
            average_price=Avg("price"),
            average_area=Avg("area"),
            average_rooms=Avg("rooms"),
        )
        latest = list(
            qs.order_by("-created_at").values(
                "id", "title", "city", "district", "price", "area", "rooms"
            )[:10]
        )
        return Response({
            "stats": {
                "total_listings": stats["total"] or 0,
                "verified_listings": stats["verified"] or 0,
                "average_price": int(stats["average_price"] or 0),
                "average_area": round(float(stats["average_area"] or 0), 2),
                "average_rooms": round(float(stats["average_rooms"] or 0), 2),
            },
            "latest_listings": latest,
        })


def health_check(request):
    """Lightweight health endpoint for Docker and monitoring."""

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok", "database": "ok"})
    except Exception:
        return JsonResponse(
            {"status": "degraded", "database": "unavailable"},
            status=503,
        )
