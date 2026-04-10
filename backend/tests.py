from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class StaticAssetServingTests(TestCase):
    def test_admin_static_asset_is_served(self):
        response = self.client.get(reverse("static-asset", args=["admin/css/base.css"]))

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response["Content-Type"])


class AdminRenderingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="StrongPass123!",
        )

    def test_admin_dashboard_renders_for_superuser(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Operations Dashboard")

    def test_admin_pages_set_no_cache_headers(self):
        login_response = self.client.get(reverse("admin:login"))
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("no-store", login_response["Cache-Control"])

        self.client.force_login(self.user)
        index_response = self.client.get(reverse("admin:index"))
        self.assertEqual(index_response.status_code, 200)
        self.assertIn("no-store", index_response["Cache-Control"])
