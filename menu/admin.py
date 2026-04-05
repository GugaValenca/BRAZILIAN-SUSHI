from django.contrib import admin

from .models import Category, MenuItem, MenuOption, MenuOptionGroup


class MenuOptionInline(admin.TabularInline):
    model = MenuOption
    extra = 1
    min_num = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    list_editable = ("sort_order",)
    ordering = ("sort_order", "name")


@admin.register(MenuOptionGroup)
class MenuOptionGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "menu_item", "required", "min_select", "max_select")
    inlines = [MenuOptionInline]
    search_fields = ("name", "menu_item__name")
    autocomplete_fields = ("menu_item",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "featured", "spicy", "vegetarian", "availability")
    list_filter = ("category", "featured", "spicy", "vegetarian", "availability")
    search_fields = ("name", "short_description", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("featured", "availability")
    autocomplete_fields = ("category",)
    list_per_page = 30


@admin.register(MenuOption)
class MenuOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "price_delta", "is_default")
    search_fields = ("name", "group__name", "group__menu_item__name")
    autocomplete_fields = ("group",)
