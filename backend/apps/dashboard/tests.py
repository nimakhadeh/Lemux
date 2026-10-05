from django.test import TestCase
from rest_framework.test import APIClient

from apps.listings.models import Listing


class DashboardAPITests(TestCase):
    def test_empty_dashboard(self):
        response = APIClient().get("/api/dashboard/summary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["stats"]["total_listings"], 0)
        self.assertEqual(response.data["latest_listings"], [])

    def test_dashboard_returns_latest_listings(self):
        Listing.objects.create(
            title="Newest", address="Tehran", city="تهران", district="الهیه",
            price=5_000_000_000, area=80, rooms=2,
        )
        response = APIClient().get("/api/dashboard/summary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["stats"]["total_listings"], 1)
        self.assertEqual(response.data["latest_listings"][0]["title"], "Newest")

    def test_health_check(self):
        response = APIClient().get("/api/dashboard/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")
