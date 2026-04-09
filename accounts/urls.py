from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AddressViewSet,
    ConfirmAccountView,
    CustomerAdminViewSet,
    FavoriteMenuItemViewSet,
    LoginView,
    ProfileView,
    RegisterView,
    ResendConfirmationView,
)

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="address")
router.register("favorites", FavoriteMenuItemViewSet, basename="favorite")
router.register("customers", CustomerAdminViewSet, basename="customer-admin")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("confirm-account/", ConfirmAccountView.as_view(), name="confirm-account"),
    path("resend-confirmation/", ResendConfirmationView.as_view(), name="resend-confirmation"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", include(router.urls)),
]
