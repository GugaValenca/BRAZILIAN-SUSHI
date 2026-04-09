from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from .managers import UserManager


class User(AbstractUser):
    class NotificationPreference(models.TextChoices):
        SMS = "sms", "SMS"
        EMAIL = "email", "Email"
        BOTH = "both", "SMS and email"

    class VerificationReason(models.TextChoices):
        NONE = "none", "Not verified"
        IDENTITY = "identity", "Identity confirmed"
        PICKUP = "pickup", "Pickup verified"
        ORDER_HISTORY = "order_history", "Five successful orders"

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    notification_preference = models.CharField(max_length=10, choices=NotificationPreference.choices, default=NotificationPreference.BOTH)
    sms_opt_in = models.BooleanField(default=True)
    email_opt_in = models.BooleanField(default=True)
    account_confirmation_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    account_confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    account_confirmed_at = models.DateTimeField(null=True, blank=True)
    is_verified_customer = models.BooleanField(default=False)
    verified_reason = models.CharField(max_length=20, choices=VerificationReason.choices, default=VerificationReason.NONE)
    loyalty_completed_orders = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.get_full_name() or self.email


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=50)
    recipient_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=12)
    delivery_notes = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "label"]

    def __str__(self):
        return f"{self.label} - {self.line_1}"


class FavoriteMenuItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorite_items")
    menu_item = models.ForeignKey("menu.MenuItem", on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "menu_item")
