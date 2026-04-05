from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import ContactMessage, Coupon, Promotion, Review
from .serializers import ContactMessageSerializer, CouponSerializer, PromotionSerializer, ReviewSerializer


class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PromotionSerializer

    def get_queryset(self):
        now = timezone.now()
        return Promotion.objects.filter(active=True, starts_at__lte=now, ends_at__gte=now)


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CouponSerializer

    def get_queryset(self):
        now = timezone.now()
        return Coupon.objects.filter(active=True, starts_at__lte=now, ends_at__gte=now)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Review.objects.select_related("user")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(approval_status=Review.ApprovalStatus.APPROVED)

    def perform_create(self, serializer):
        if not self.request.user.is_verified_customer:
            raise PermissionDenied("Only verified customers can submit reviews.")
        serializer.save(user=self.request.user)


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve", "update", "partial_update"}:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
