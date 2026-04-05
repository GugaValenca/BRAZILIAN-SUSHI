from rest_framework import serializers

from .models import Category, MenuItem, MenuOption, MenuOptionGroup


class MenuOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuOption
        fields = ("id", "name", "price_delta", "is_default")


class MenuOptionGroupSerializer(serializers.ModelSerializer):
    options = MenuOptionSerializer(many=True, read_only=True)

    class Meta:
        model = MenuOptionGroup
        fields = ("id", "name", "required", "min_select", "max_select", "options")


class MenuItemSerializer(serializers.ModelSerializer):
    option_groups = MenuOptionGroupSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = MenuItem
        fields = (
            "id",
            "category",
            "category_name",
            "name",
            "slug",
            "short_description",
            "description",
            "price",
            "image",
            "spicy",
            "vegetarian",
            "featured",
            "allergens",
            "calories",
            "availability",
            "option_groups",
        )


class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "sort_order", "items")


class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "sort_order")


class AdminMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "short_description",
            "description",
            "price",
            "image",
            "spicy",
            "vegetarian",
            "featured",
            "allergens",
            "calories",
            "availability",
        )
