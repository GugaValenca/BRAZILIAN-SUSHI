from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Address, FavoriteMenuItem, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "phone_number", "is_verified_customer", "verified_reason", "is_staff")
    list_filter = ("is_verified_customer", "verified_reason", "is_staff", "is_superuser")
    ordering = ("email",)
    search_fields = ("email", "username", "first_name", "last_name", "phone_number")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Customer settings",
            {
                "fields": (
                    "phone_number",
                    "notification_preference",
                    "sms_opt_in",
                    "email_opt_in",
                    "is_verified_customer",
                    "verified_reason",
                    "loyalty_completed_orders",
                )
            },
        ),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "city", "state", "postal_code", "is_default")
    list_filter = ("state", "is_default")
    search_fields = ("user__email", "line_1", "postal_code")


@admin.register(FavoriteMenuItem)
class FavoriteMenuItemAdmin(admin.ModelAdmin):
    list_display = ("user", "menu_item", "created_at")
    search_fields = ("user__email", "menu_item__name")
