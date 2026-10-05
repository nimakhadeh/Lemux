from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):
    def test_register_and_login(self):
        response = self.client.post(
            "/api/users/register/",
            {
                "username": "nima",
                "email": "nima@example.com",
                "password": "StrongPass123!",
                "password_confirm": "StrongPass123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="nima").exists())

        response = self.client.post(
            "/api/users/login/",
            {"username": "nima", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_requires_authentication(self):
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, 401)
