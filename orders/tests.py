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
