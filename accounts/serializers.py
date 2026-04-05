from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Address, FavoriteMenuItem

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "notification_preference",
            "sms_opt_in",
            "email_opt_in",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "notification_preference",
            "sms_opt_in",
            "email_opt_in",
            "is_verified_customer",
            "verified_reason",
            "loyalty_completed_orders",
            "is_staff",
        )
        read_only_fields = ("email", "is_verified_customer", "verified_reason", "loyalty_completed_orders", "is_staff")


class AdminCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "notification_preference",
            "sms_opt_in",
            "email_opt_in",
            "is_verified_customer",
            "verified_reason",
            "loyalty_completed_orders",
            "is_staff",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("date_joined",)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ("user",)


class FavoriteMenuItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source="menu_item.name", read_only=True)

    class Meta:
        model = FavoriteMenuItem
        fields = ("id", "menu_item", "menu_item_name", "created_at")
        read_only_fields = ("created_at",)
