from datetime import timedelta

from django.utils import timezone

from orders.models import Order
from .models import Review


def get_eligible_review_order(user):
    now = timezone.now()
    delivered_orders = (
        user.orders.prefetch_related("items__menu_item")
        .filter(status=Order.Status.DELIVERED, completed_at__isnull=False)
        .order_by("-completed_at")
    )

    for order in delivered_orders:
        if order.completed_at + timedelta(hours=24) < now:
            continue
        if Review.objects.filter(order=order).exists():
            continue
        if user.orders.exclude(pk=order.pk).filter(created_at__gt=order.completed_at).exists():
            continue
        return order

    return None
