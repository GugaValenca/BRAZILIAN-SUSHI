from rest_framework import serializers

from .models import ContactMessage, Coupon, Promotion, Review


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="user.get_full_name", read_only=True)
    is_verified_customer = serializers.BooleanField(source="user.is_verified_customer", read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "customer_name",
            "is_verified_customer",
            "rating",
            "title",
            "content",
            "customer_photo",
            "approval_status",
            "created_at",
        )
        read_only_fields = ("user", "approval_status", "created_at")


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ("resolved", "created_at")
