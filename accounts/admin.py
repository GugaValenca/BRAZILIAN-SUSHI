from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Address, FavoriteMenuItem, User

admin.site.site_header = "Brazilian Sushi Admin"
admin.site.site_title = "Brazilian Sushi Admin"
admin.site.index_title = "Operations Dashboard"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "account_confirmed_at",
        "notification_preference",
        "is_verified_customer",
        "verified_reason",
        "is_staff",
    )
    list_filter = ("notification_preference", "is_verified_customer", "verified_reason", "is_staff", "is_superuser", "is_active", "account_confirmed_at")
    ordering = ("email",)
    search_fields = ("email", "username", "first_name", "last_name", "phone_number")
    list_per_page = 25
    readonly_fields = ("last_login", "date_joined", "account_confirmation_token", "account_confirmation_sent_at", "account_confirmed_at")
    actions = ("mark_verified", "remove_verification")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Customer settings",
            {
                "fields": (
                    "phone_number",
                    "notification_preference",
                    "sms_opt_in",
                    "email_opt_in",
                    "account_confirmation_token",
                    "account_confirmation_sent_at",
                    "account_confirmed_at",
                    "is_verified_customer",
                    "verified_reason",
                    "loyalty_completed_orders",
                )
            },
        ),
    )

    @admin.action(description="Mark selected customers as verified")
    def mark_verified(self, request, queryset):
        queryset.update(
            is_verified_customer=True,
            verified_reason=User.VerificationReason.IDENTITY,
        )

    @admin.action(description="Remove verified status from selected customers")
    def remove_verification(self, request, queryset):
        queryset.update(
            is_verified_customer=False,
            verified_reason=User.VerificationReason.NONE,
        )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Customer settings",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "notification_preference",
                    "sms_opt_in",
                    "email_opt_in",
                )
            },
        ),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "city", "state", "postal_code", "is_default")
    list_filter = ("state", "is_default")
    search_fields = ("user__email", "line_1", "postal_code")
    autocomplete_fields = ("user",)
    list_per_page = 25


@admin.register(FavoriteMenuItem)
class FavoriteMenuItemAdmin(admin.ModelAdmin):
    list_display = ("user", "menu_item", "created_at")
    search_fields = ("user__email", "menu_item__name")
    autocomplete_fields = ("user", "menu_item")
    list_per_page = 25
