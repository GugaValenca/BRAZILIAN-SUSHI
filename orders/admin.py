from django.contrib import admin

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
    list_display = ("id", "customer", "guest_name", "order_type", "status", "total", "notification_preference", "created_at")
    list_filter = ("order_type", "status", "notification_preference", "created_at")
    search_fields = ("id", "customer__email", "guest_email", "guest_phone", "guest_name", "tracking_token")
    readonly_fields = ("tracking_token", "subtotal", "discount_amount", "total", "created_at", "updated_at")
    autocomplete_fields = ("customer", "delivery_address", "coupon", "delivery_zone")
    date_hierarchy = "created_at"
    list_per_page = 30
    inlines = [OrderItemInline, OrderStatusEventInline]
    fieldsets = (
        (
            "Order overview",
            {
                "fields": ("customer", "order_type", "status", "tracking_token", "notification_preference"),
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
                "fields": ("notes", "allergy_notes"),
            },
        ),
        (
            "Timeline",
            {
                "fields": ("confirmed_at", "preparation_started_at", "dispatched_at", "completed_at", "created_at", "updated_at"),
            },
        ),
    )
    actions = ("mark_confirmed", "mark_preparing", "mark_ready", "mark_out_for_delivery", "mark_delivered")

    @admin.action(description="Mark selected orders as confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Order.Status.CONFIRMED)

    @admin.action(description="Mark selected orders as preparing")
    def mark_preparing(self, request, queryset):
        queryset.update(status=Order.Status.PREPARING)

    @admin.action(description="Mark selected orders as ready")
    def mark_ready(self, request, queryset):
        queryset.update(status=Order.Status.READY)

    @admin.action(description="Mark selected orders as out for delivery")
    def mark_out_for_delivery(self, request, queryset):
        queryset.update(status=Order.Status.OUT_FOR_DELIVERY)

    @admin.action(description="Mark selected orders as delivered")
    def mark_delivered(self, request, queryset):
        queryset.update(status=Order.Status.DELIVERED)


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "postal_code", "fee", "minimum_order", "average_minutes", "active")
    list_filter = ("active",)
    list_editable = ("fee", "minimum_order", "average_minutes", "active")
    search_fields = ("name", "postal_code")
