from django.contrib import admin

from .models import ContactMessage, Coupon, Promotion, Review


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "starts_at", "ends_at", "active", "featured")
    list_filter = ("audience", "active", "featured")
    search_fields = ("title", "description")
    list_editable = ("active", "featured")
    date_hierarchy = "starts_at"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "value", "minimum_order", "verified_only", "active")
    list_filter = ("discount_type", "verified_only", "active")
    search_fields = ("code", "description")
    list_editable = ("active",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("order_reference", "user", "order_items_preview", "rating", "approval_status", "created_at")
    list_filter = ("approval_status", "rating")
    search_fields = ("user__email", "title", "content", "order__id", "order__guest_name", "order__guest_email")
    autocomplete_fields = ("user", "order")
    list_editable = ("approval_status",)
    date_hierarchy = "created_at"
    readonly_fields = ("order_reference", "order_items_preview", "created_at")
    actions = ("approve_reviews", "reject_reviews")
    fieldsets = (
        (
            "Review details",
            {
                "fields": ("user", "order", "order_reference", "order_items_preview", "rating", "title", "content", "approval_status", "created_at"),
            },
        ),
    )

    @admin.display(description="Order")
    def order_reference(self, obj):
        if not obj.order_id:
            return "No order linked"
        return f"Order #{obj.order_id}"

    @admin.display(description="Ordered items")
    def order_items_preview(self, obj):
        if not obj.order_id:
            return "No linked order items."
        return ", ".join(item.menu_item.name for item in obj.order.items.select_related("menu_item").all())

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        queryset.update(approval_status=Review.ApprovalStatus.APPROVED)

    @admin.action(description="Reject selected reviews")
    def reject_reviews(self, request, queryset):
        queryset.update(approval_status=Review.ApprovalStatus.REJECTED)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "resolved")
    list_filter = ("resolved",)
    search_fields = ("name", "email", "message")
    list_editable = ("resolved",)
    date_hierarchy = "created_at"
