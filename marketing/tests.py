from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Review
from orders.models import Order

User = get_user_model()


class ReviewSubmissionTests(APITestCase):
    def test_customer_without_completed_order_cannot_submit_review(self):
        user = User.objects.create_user(
            email="guest-review@braziliansushi.com",
            username="guestreview",
            password="StrongPass123!",
        )
        self.client.force_authenticate(user)

        response = self.client.post(
            reverse("review-list"),
            {
                "rating": 5,
                "title": "Amazing dinner",
                "content": "Great sushi and fast delivery.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Review.objects.count(), 0)

    def test_customer_with_completed_order_review_starts_pending_approval(self):
        user = User.objects.create_user(
            email="verified-review@braziliansushi.com",
            username="verifiedreview",
            password="StrongPass123!",
        )
        Order.objects.create(
            customer=user,
            order_type=Order.OrderType.DELIVERY,
            status=Order.Status.DELIVERED,
            guest_name="Verified Review",
            guest_email=user.email,
            guest_phone="8135550002",
            total="25.00",
            subtotal="25.00",
            completed_at=timezone.now(),
        )
        self.client.force_authenticate(user)

        response = self.client.post(
            reverse("review-list"),
            {
                "rating": 5,
                "title": "Premium experience",
                "content": "Presentation, flavor, and timing were excellent.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get()
        self.assertEqual(review.user, user)
        self.assertEqual(review.approval_status, Review.ApprovalStatus.PENDING)
