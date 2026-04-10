from django.test import TestCase
from django.urls import reverse


class StaticAssetServingTests(TestCase):
    def test_admin_static_asset_is_served(self):
        response = self.client.get(reverse("static-asset", args=["admin/css/base.css"]))

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response["Content-Type"])
