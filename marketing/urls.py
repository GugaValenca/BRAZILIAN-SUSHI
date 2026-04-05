from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactMessageViewSet, CouponViewSet, PromotionViewSet, ReviewViewSet

router = DefaultRouter()
router.register("promotions", PromotionViewSet, basename="promotion")
router.register("coupons", CouponViewSet, basename="coupon")
router.register("reviews", ReviewViewSet, basename="review")
router.register("contact-messages", ContactMessageViewSet, basename="contact-message")

urlpatterns = [
    path("", include(router.urls)),
]
