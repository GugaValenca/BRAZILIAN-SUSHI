from django.contrib import admin

from .models import DeliveryZone, Order, OrderItem, OrderStatusEvent


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderStatusEventInline(admin.TabularInline):
    model = OrderStatusEvent
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "order_type", "status", "total", "notification_preference", "created_at")
    list_filter = ("order_type", "status", "notification_preference")
    search_fields = ("id", "customer__email", "guest_email", "guest_phone")
    readonly_fields = ("subtotal", "total", "created_at", "updated_at")
    inlines = [OrderItemInline, OrderStatusEventInline]


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "postal_code", "fee", "minimum_order", "average_minutes", "active")
    list_filter = ("active",)
