from django.test import TestCase
from rest_framework.test import APIClient

from apps.listings.models import Listing


class AnalyticsAPITests(TestCase):
    def setUp(self):
        Listing.objects.create(
            title="A", address="Tehran A", city="تهران", district="الهیه",
            price=8_500_000_000, area=100, rooms=2, property_type="apartment"
        )
        Listing.objects.create(
            title="B", address="Tehran B", city="تهران", district="فرمانیه",
            price=12_000_000_000, area=120, rooms=3, property_type="apartment"
        )

    def test_overview_uses_listing_level_average(self):
        response = APIClient().get("/api/analytics/overview/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_listings"], 2)
        self.assertEqual(response.data["average_price_per_m2"], 92_500_000)

    def test_city_analysis(self):
        response = APIClient().get("/api/analytics/cities/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["city"], "تهران")
        self.assertEqual(response.data[0]["count"], 2)

    def test_district_filter(self):
        response = APIClient().get("/api/analytics/districts/?city=تهران")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
