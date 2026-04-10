from django.contrib import admin
from django.utils import timezone

from accounts.models import User
from .models import DeliveryZone, Order, OrderItem, OrderStatusEvent


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("menu_item",)
    readonly_fields = ("unit_price", "line_total")


class OrderStatusEventInline(admin.TabularInline):
    model = OrderStatusEvent
    extra = 0
    readonly_fields = ("created_at",)
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guest_name",
        "customer_email",
        "customer_priority",
        "kitchen_attention",
        "order_type",
        "status",
        "total",
        "notification_preference",
        "created_at",
    )
    list_filter = ("order_type", "status", "notification_preference", "created_at")
    search_fields = ("id", "customer__email", "guest_email", "guest_phone", "guest_name", "tracking_token")
    readonly_fields = (
        "tracking_token",
        "subtotal",
        "discount_amount",
        "total",
        "items_preview",
        "kitchen_notes_preview",
        "allergy_alert_preview",
        "average_delivery_time_display",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = ("customer", "delivery_address", "coupon", "delivery_zone")
    date_hierarchy = "created_at"
    list_per_page = 30
    inlines = [OrderItemInline, OrderStatusEventInline]
    fieldsets = (
        (
            "Order overview",
            {
                "fields": ("customer", "order_type", "status", "tracking_token", "notification_preference", "items_preview"),
            },
        ),
        (
            "Guest details",
            {
                "fields": ("guest_name", "guest_email", "guest_phone"),
            },
        ),
        (
            "Fulfillment",
            {
                "fields": ("delivery_address", "delivery_zone", "scheduled_for"),
            },
        ),
        (
            "Pricing",
            {
                "fields": ("coupon", "subtotal", "delivery_fee", "discount_amount", "total"),
            },
        ),
        (
            "Kitchen notes",
            {
                "fields": ("notes", "allergy_notes", "kitchen_notes_preview", "allergy_alert_preview"),
            },
        ),
        (
            "Timeline",
            {
                "fields": ("confirmed_at", "preparation_started_at", "dispatched_at", "completed_at", "average_delivery_time_display", "created_at", "updated_at"),
            },
        ),
    )
    actions = ("mark_confirmed", "mark_preparing", "mark_ready", "mark_out_for_delivery", "mark_delivered", "mark_cancelled")

    @admin.display(description="Customer email", ordering="customer__email")
    def customer_email(self, obj):
        return obj.customer.email if obj.customer else obj.guest_email or "-"

    @admin.display(description="Priority")
    def customer_priority(self, obj):
        if obj.customer and obj.customer.is_verified_customer:
            return "Verified priority"
        return "Standard"

    @admin.display(description="Items in order")
    def items_preview(self, obj):
        items = list(obj.items.select_related("menu_item").all())
        if not items:
            return "No items added yet."
        return ", ".join(f"{item.quantity}x {item.menu_item.name}" for item in items)

    @admin.display(description="Kitchen attention")
    def kitchen_attention(self, obj):
        if obj.allergy_notes:
            return "Allergy alert"
        if obj.notes:
            return "Kitchen notes"
        return "Standard"

    @admin.display(description="Kitchen notes")
    def kitchen_notes_preview(self, obj):
        return obj.notes or "No special order notes."

    @admin.display(description="Allergy / dietary restriction")
    def allergy_alert_preview(self, obj):
        return obj.allergy_notes or "No allergy or dietary restriction."

    @admin.display(description="Average delivery time")
    def average_delivery_time_display(self, obj):
        if obj.average_delivery_time is None:
            return "Not available yet"
        return f"{obj.average_delivery_time} min"

    def _apply_status_transition(self, order, next_status):
        order.status = next_status
        now = timezone.now()
        updated_fields = ["status", "updated_at"]

        if next_status == Order.Status.CONFIRMED and not order.confirmed_at:
            order.confirmed_at = now
            updated_fields.append("confirmed_at")
        elif next_status == Order.Status.PREPARING and not order.preparation_started_at:
            order.preparation_started_at = now
            updated_fields.append("preparation_started_at")
        elif next_status == Order.Status.OUT_FOR_DELIVERY and not order.dispatched_at:
            order.dispatched_at = now
            updated_fields.append("dispatched_at")
        elif next_status == Order.Status.DELIVERED and not order.completed_at:
            order.completed_at = now
            updated_fields.append("completed_at")

        order.save(update_fields=updated_fields)
        OrderStatusEvent.objects.create(order=order, status=next_status, note="Updated from admin queue")

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

    def _bulk_transition(self, queryset, next_status):
        for order in queryset:
            self._apply_status_transition(order, next_status)

    @admin.action(description="Mark selected orders as confirmed")
    def mark_confirmed(self, request, queryset):
        self._bulk_transition(queryset, Order.Status.CONFIRMED)

    @admin.action(description="Mark selected orders as preparing")
    def mark_preparing(self, request, queryset):
        self._bulk_transition(queryset, Order.Status.PREPARING)

    @admin.action(description="Mark selected orders as ready")
    def mark_ready(self, request, queryset):
        self._bulk_transition(queryset, Order.Status.READY)

    @admin.action(description="Mark selected orders as out for delivery")
    def mark_out_for_delivery(self, request, queryset):
        self._bulk_transition(queryset, Order.Status.OUT_FOR_DELIVERY)

    @admin.action(description="Mark selected orders as delivered")
    def mark_delivered(self, request, queryset):
        self._bulk_transition(queryset, Order.Status.DELIVERED)

    @admin.action(description="Mark selected orders as cancelled")
    def mark_cancelled(self, request, queryset):
        self._bulk_transition(queryset, Order.Status.CANCELLED)


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "postal_code", "fee", "minimum_order", "average_minutes", "active")
    list_filter = ("active",)
    list_editable = ("fee", "minimum_order", "average_minutes", "active")
    search_fields = ("name", "postal_code")
