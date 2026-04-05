from rest_framework import filters, viewsets

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related("items__option_groups__options")
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.select_related("category").prefetch_related("option_groups__options")
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "short_description", "description", "allergens"]
    ordering_fields = ["price", "name", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        spicy = self.request.query_params.get("spicy")
        vegetarian = self.request.query_params.get("vegetarian")
        if category:
            queryset = queryset.filter(category__slug=category)
        if featured == "true":
            queryset = queryset.filter(featured=True)
        if spicy == "true":
            queryset = queryset.filter(spicy=True)
        if vegetarian == "true":
            queryset = queryset.filter(vegetarian=True)
        return queryset.exclude(availability=MenuItem.Availability.HIDDEN)
