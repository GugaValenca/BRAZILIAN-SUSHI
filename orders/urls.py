from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeliveryZoneViewSet, OrderViewSet

router = DefaultRouter()
router.register("zones", DeliveryZoneViewSet, basename="delivery-zone")
router.register("", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
