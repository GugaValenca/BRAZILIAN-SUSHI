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
    list_display = ("user", "title", "rating", "approval_status", "created_at")
    list_filter = ("approval_status", "rating")
    search_fields = ("user__email", "title", "content")
    autocomplete_fields = ("user",)
    list_editable = ("approval_status",)
    date_hierarchy = "created_at"
    actions = ("approve_reviews", "reject_reviews")

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
