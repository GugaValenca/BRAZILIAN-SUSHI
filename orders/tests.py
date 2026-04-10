from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menu.models import Category, MenuItem
from orders.models import Order, OrderStatusEvent

User = get_user_model()


class OrderStatusWorkflowTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@braziliansushi.com",
            username="admin",
            password="StrongPass123!",
        )
        self.customer = User.objects.create_user(
            email="customer@braziliansushi.com",
            username="customer",
            password="StrongPass123!",
        )
        category = Category.objects.create(name="Rolls", slug="rolls")
        self.menu_item = MenuItem.objects.create(
            category=category,
            name="Salmon Roll",
            slug="salmon-roll",
            short_description="Fresh salmon roll",
            price=Decimal("18.00"),
        )
        self.client.force_authenticate(self.admin)

    def test_customer_becomes_verified_after_five_successful_orders(self):
        update_url_name = "order-update-status"

        for index in range(5):
            order = Order.objects.create(
                customer=self.customer,
                order_type=Order.OrderType.DELIVERY,
                subtotal=Decimal("18.00"),
                total=Decimal("18.00"),
            )
            order.items.create(
                menu_item=self.menu_item,
                quantity=1,
                unit_price=Decimal("18.00"),
                line_total=Decimal("18.00"),
            )

            response = self.client.post(
                reverse(update_url_name, args=[order.id]),
                {"status": Order.Status.DELIVERED, "note": f"Delivered order {index + 1}"},
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            order.refresh_from_db()
            self.assertEqual(order.status, Order.Status.DELIVERED)
            self.assertTrue(OrderStatusEvent.objects.filter(order=order, status=Order.Status.DELIVERED).exists())

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.loyalty_completed_orders, 5)
        self.assertTrue(self.customer.is_verified_customer)
        self.assertEqual(self.customer.verified_reason, User.VerificationReason.ORDER_HISTORY)


class GuestOrderSecurityTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="Nigiri", slug="nigiri")
        self.menu_item = MenuItem.objects.create(
            category=category,
            name="Salmon Nigiri",
            slug="salmon-nigiri",
            short_description="Fresh salmon",
            price=Decimal("12.00"),
        )
        self.order = Order.objects.create(
            order_type=Order.OrderType.PICKUP,
            guest_name="Guest Customer",
            guest_email="guest@braziliansushi.com",
            guest_phone="5551234567",
            subtotal=Decimal("12.00"),
            total=Decimal("12.00"),
        )
        self.order.items.create(
            menu_item=self.menu_item,
            quantity=1,
            unit_price=Decimal("12.00"),
            line_total=Decimal("12.00"),
        )

    def test_guest_cannot_list_all_orders(self):
        response = self.client.get(reverse("order-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_guest_can_track_order_with_valid_token(self):
        response = self.client.get(
            reverse("order-track"),
            {"order_id": self.order.id, "token": str(self.order.tracking_token)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order.id)
        self.assertEqual(response.data["tracking_token"], str(self.order.tracking_token))


class AuthenticatedCheckoutTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            email="member@braziliansushi.com",
            username="member",
            password="StrongPass123!",
            first_name="Gustavo",
            last_name="Valenca",
            phone_number="8135550101",
            notification_preference=User.NotificationPreference.EMAIL,
        )
        category = Category.objects.create(name="Combos", slug="combos")
        self.menu_item = MenuItem.objects.create(
            category=category,
            name="Date Night Combo",
            slug="date-night-combo-checkout",
            short_description="Shareable combo",
            price=Decimal("36.00"),
        )
        self.client.force_authenticate(self.customer)

    def test_authenticated_checkout_uses_profile_contact_details(self):
        response = self.client.post(
            reverse("order-list"),
            {
                "order_type": Order.OrderType.PICKUP,
                "notes": "Please include extra napkins.",
                "allergy_notes": "Shellfish allergy.",
                "items": [
                    {
                        "menu_item_id": self.menu_item.id,
                        "quantity": 1,
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.guest_name, "Gustavo Valenca")
        self.assertEqual(order.guest_email, self.customer.email)
        self.assertEqual(order.guest_phone, self.customer.phone_number)
        self.assertEqual(order.notification_preference, User.NotificationPreference.EMAIL)
        self.assertTrue(response.data["has_kitchen_notes"])
        self.assertTrue(response.data["has_allergy_alert"])
