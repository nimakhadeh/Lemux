# -*- coding: utf-8 -*-
"""Market analytics API backed by Django ORM."""

from django.db.models import Avg, Count, ExpressionWrapper, F, FloatField, Max, Min
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.listings.models import Listing


def active_listings():
    return Listing.objects.filter(is_active=True, price__gt=0, area__gt=0)


def price_per_m2():
    return ExpressionWrapper(F("price") / F("area"), output_field=FloatField())


class OverviewView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = active_listings().aggregate(
            total_listings=Count("id"),
            average_price=Avg("price"),
            min_price=Min("price"),
            max_price=Max("price"),
            average_area=Avg("area"),
            average_rooms=Avg("rooms"),
            average_price_per_m2=Avg(price_per_m2()),
        )
        return Response({
            "total_listings": data["total_listings"] or 0,
            "average_price": int(data["average_price"] or 0),
            "min_price": int(data["min_price"] or 0),
            "max_price": int(data["max_price"] or 0),
            "average_area": round(float(data["average_area"] or 0), 2),
            "average_rooms": round(float(data["average_rooms"] or 0), 2),
            "average_price_per_m2": int(data["average_price_per_m2"] or 0),
        })


class CityAnalysisView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        rows = active_listings().values("city").annotate(
            count=Count("id"),
            avg_price=Avg("price"),
            avg_area=Avg("area"),
            avg_price_per_m2=Avg(price_per_m2()),
            min_price=Min("price"),
            max_price=Max("price"),
        ).order_by("-count", "city")
        return Response([
            {
                "city": row["city"], "count": row["count"],
                "avg_price": int(row["avg_price"] or 0),
                "avg_area": round(float(row["avg_area"] or 0), 2),
                "avg_price_per_m2": int(row["avg_price_per_m2"] or 0),
                "min_price": int(row["min_price"] or 0),
                "max_price": int(row["max_price"] or 0),
            }
            for row in rows
        ])


class PropertyTypeAnalysisView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        labels = dict(Listing.PROPERTY_TYPES)
        rows = active_listings().values("property_type").annotate(
            count=Count("id"),
            avg_price=Avg("price"),
            avg_area=Avg("area"),
            avg_price_per_m2=Avg(price_per_m2()),
        ).order_by("-count", "property_type")
        return Response([
            {
                "property_type": row["property_type"],
                "property_type_display": labels.get(row["property_type"], row["property_type"]),
                "count": row["count"],
                "avg_price": int(row["avg_price"] or 0),
                "avg_area": round(float(row["avg_area"] or 0), 2),
                "avg_price_per_m2": int(row["avg_price_per_m2"] or 0),
            }
            for row in rows
        ])


class DistrictAnalysisView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = active_listings()
        city = request.query_params.get("city")
        if city:
            qs = qs.filter(city__iexact=city.strip())
        rows = qs.values("city", "district").annotate(
            count=Count("id"),
            avg_price=Avg("price"),
            avg_area=Avg("area"),
            avg_price_per_m2=Avg(price_per_m2()),
        ).order_by("-count", "city", "district")[:100]
        return Response([
            {
                "city": row["city"], "district": row["district"], "count": row["count"],
                "avg_price": int(row["avg_price"] or 0),
                "avg_area": round(float(row["avg_area"] or 0), 2),
                "avg_price_per_m2": int(row["avg_price_per_m2"] or 0),
            }
            for row in rows
        ])
