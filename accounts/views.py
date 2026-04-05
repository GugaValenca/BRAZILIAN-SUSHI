from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    AddressSerializer,
    AdminCustomerSerializer,
    FavoriteMenuItemSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def make_default(self, request, pk=None):
        self.get_queryset().update(is_default=False)
        address = self.get_object()
        address.is_default = True
        address.save(update_fields=["is_default"])
        return Response({"status": "default address updated"})


class FavoriteMenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteMenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorite_items.select_related("menu_item")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = AdminCustomerSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        customer = self.get_object()
        customer.is_verified_customer = True
        customer.verified_reason = User.VerificationReason.IDENTITY
        customer.save(update_fields=["is_verified_customer", "verified_reason"])
        return Response(self.get_serializer(customer).data)

    @action(detail=True, methods=["post"])
    def remove_verification(self, request, pk=None):
        customer = self.get_object()
        customer.is_verified_customer = False
        customer.verified_reason = User.VerificationReason.NONE
        customer.save(update_fields=["is_verified_customer", "verified_reason"])
        return Response(self.get_serializer(customer).data)
