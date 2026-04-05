from django.contrib import admin

from .models import Category, MenuItem, MenuOption, MenuOptionGroup


class MenuOptionInline(admin.TabularInline):
    model = MenuOption
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuOptionGroup)
class MenuOptionGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "menu_item", "required", "min_select", "max_select")
    inlines = [MenuOptionInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "featured", "spicy", "vegetarian", "availability")
    list_filter = ("category", "featured", "spicy", "vegetarian", "availability")
    search_fields = ("name", "short_description", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuOption)
class MenuOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "price_delta", "is_default")
