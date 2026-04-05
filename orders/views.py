from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User

from .models import DeliveryZone, Order, OrderStatusEvent
from .serializers import CreateOrderSerializer, DeliveryZoneSerializer, OrderSerializer


class DeliveryZoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryZone.objects.filter(active=True)
    serializer_class = DeliveryZoneSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__selections", "status_events").select_related(
        "customer",
        "delivery_address",
        "coupon",
        "delivery_zone",
    )
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            queryset = queryset.filter(customer=self.request.user)
        return queryset

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def reorder(self, request, pk=None):
        original_order = self.get_object()
        if original_order.customer != request.user and not request.user.is_staff:
            return Response({"detail": "You cannot reorder this order."}, status=status.HTTP_403_FORBIDDEN)

        new_order = Order.objects.create(
            customer=request.user,
            delivery_address=original_order.delivery_address,
            coupon=original_order.coupon,
            delivery_zone=original_order.delivery_zone,
            order_type=original_order.order_type,
            notes=original_order.notes,
            allergy_notes=original_order.allergy_notes,
            notification_preference=original_order.notification_preference,
            delivery_fee=original_order.delivery_fee,
            estimated_minutes=original_order.estimated_minutes,
        )
        for item in original_order.items.all():
            cloned_item = new_order.items.create(
                menu_item=item.menu_item,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.line_total,
                special_request=item.special_request,
            )
            for selection in item.selections.all():
                cloned_item.selections.create(option=selection.option, price_delta=selection.price_delta)
        new_order.recalculate_totals()
        new_order.save()
        OrderStatusEvent.objects.create(order=new_order, status=new_order.status, note="Reordered from previous order")
        return Response(OrderSerializer(new_order, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAdminUser])
    def staff_queue(self, request):
        queue = self.get_queryset().filter(status__in=[Order.Status.RECEIVED, Order.Status.CONFIRMED, Order.Status.PREPARING, Order.Status.READY, Order.Status.OUT_FOR_DELIVERY])
        serializer = OrderSerializer(queue, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAdminUser])
    def summary(self, request):
        queryset = self.get_queryset()
        data = {
            "received": queryset.filter(status=Order.Status.RECEIVED).count(),
            "confirmed": queryset.filter(status=Order.Status.CONFIRMED).count(),
            "preparing": queryset.filter(status=Order.Status.PREPARING).count(),
            "ready": queryset.filter(status=Order.Status.READY).count(),
            "out_for_delivery": queryset.filter(status=Order.Status.OUT_FOR_DELIVERY).count(),
            "delivered": queryset.filter(status=Order.Status.DELIVERED).count(),
            "pickup_orders": queryset.filter(order_type=Order.OrderType.PICKUP).count(),
            "delivery_orders": queryset.filter(order_type=Order.OrderType.DELIVERY).count(),
        }
        return Response(data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        next_status = request.data.get("status")
        note = request.data.get("note", "")
        if next_status not in Order.Status.values:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = next_status
        now = timezone.now()
        if next_status == Order.Status.CONFIRMED:
            order.confirmed_at = now
        elif next_status == Order.Status.PREPARING:
            order.preparation_started_at = now
        elif next_status == Order.Status.OUT_FOR_DELIVERY:
            order.dispatched_at = now
        elif next_status in {Order.Status.DELIVERED, Order.Status.READY}:
            order.completed_at = now
        order.save()
        OrderStatusEvent.objects.create(order=order, status=next_status, note=note)

        customer = order.customer
        if customer and next_status == Order.Status.DELIVERED:
            customer.loyalty_completed_orders += 1
            if order.order_type == Order.OrderType.PICKUP and not customer.is_verified_customer:
                customer.is_verified_customer = True
                customer.verified_reason = User.VerificationReason.PICKUP
            elif customer.loyalty_completed_orders >= 5 and not customer.is_verified_customer:
                customer.is_verified_customer = True
                customer.verified_reason = User.VerificationReason.ORDER_HISTORY
            customer.save(update_fields=["loyalty_completed_orders", "is_verified_customer", "verified_reason"])

        return Response(OrderSerializer(order, context={"request": request}).data)
