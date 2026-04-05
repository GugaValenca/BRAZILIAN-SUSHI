from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from marketing.models import Coupon, Promotion
from menu.models import Category, MenuItem, MenuOption, MenuOptionGroup
from orders.models import DeliveryZone


class Command(BaseCommand):
    help = "Seed demo data for Brazilian Sushi"

    def handle(self, *args, **options):
        categories = [
            ("Nigiri", 1),
            ("Rolls", 2),
            ("Sashimi", 3),
            ("Combos", 4),
            ("Soups & Sides", 5),
            ("Beverages", 6),
        ]
        category_map = {}
        for name, order in categories:
            category, _ = Category.objects.get_or_create(
                slug=name.lower().replace(" & ", "-").replace(" ", "-"),
                defaults={"name": name, "sort_order": order},
            )
            category_map[name] = category

        items = [
            {
                "category": "Nigiri",
                "name": "Salmon Nigiri",
                "slug": "salmon-nigiri",
                "short_description": "Fresh Atlantic salmon over seasoned sushi rice.",
                "description": "Finished with a light citrus glaze.",
                "price": Decimal("8.99"),
                "allergens": "fish",
                "featured": True,
            },
            {
                "category": "Rolls",
                "name": "Brazilian Roll",
                "slug": "brazilian-roll",
                "short_description": "Cream cheese, mango, and grilled salmon.",
                "description": "Finished with a passion fruit drizzle.",
                "price": Decimal("18.99"),
                "allergens": "fish,dairy",
                "featured": True,
            },
            {
                "category": "Rolls",
                "name": "Spicy Tuna Roll",
                "slug": "spicy-tuna-roll",
                "short_description": "Diced spicy tuna with cucumber and sriracha mayo.",
                "description": "A spicy customer favorite.",
                "price": Decimal("14.99"),
                "allergens": "fish,egg",
                "spicy": True,
            },
            {
                "category": "Sashimi",
                "name": "Sashimi Deluxe",
                "slug": "sashimi-deluxe",
                "short_description": "Chef's selection of premium sashimi.",
                "description": "Tuna, salmon, yellowtail, and octopus.",
                "price": Decimal("24.99"),
                "allergens": "fish,shellfish",
                "featured": True,
            },
            {
                "category": "Combos",
                "name": "Sushi Party Box",
                "slug": "sushi-party-box",
                "short_description": "30 pieces of assorted nigiri, rolls, and sashimi.",
                "description": "Perfect for sharing.",
                "price": Decimal("49.99"),
                "allergens": "fish,shellfish,soy",
                "featured": True,
            },
            {
                "category": "Soups & Sides",
                "name": "Miso Soup",
                "slug": "miso-soup",
                "short_description": "Traditional dashi broth with tofu and wakame.",
                "description": "Light and comforting.",
                "price": Decimal("4.99"),
                "allergens": "soy",
                "vegetarian": True,
            },
        ]

        for item_data in items:
            category = category_map[item_data.pop("category")]
            item, _ = MenuItem.objects.get_or_create(slug=item_data["slug"], defaults={**item_data, "category": category})
            if item.slug == "brazilian-roll":
                group, _ = MenuOptionGroup.objects.get_or_create(menu_item=item, name="Protein upgrade", defaults={"required": False, "min_select": 0, "max_select": 1})
                MenuOption.objects.get_or_create(group=group, name="Extra salmon", defaults={"price_delta": Decimal("4.00")})
                MenuOption.objects.get_or_create(group=group, name="Add tuna", defaults={"price_delta": Decimal("3.50")})

        for postal_code, fee, avg in [("60601", Decimal("4.99"), 35), ("60602", Decimal("5.99"), 42), ("60603", Decimal("6.99"), 48)]:
            DeliveryZone.objects.get_or_create(
                postal_code=postal_code,
                defaults={
                    "name": f"Downtown Zone {postal_code[-1]}",
                    "fee": fee,
                    "minimum_order": Decimal("20.00"),
                    "average_minutes": avg,
                    "active": True,
                },
            )

        now = timezone.now()
        Promotion.objects.get_or_create(
            title="Verified Customer Miso Upgrade",
            defaults={
                "description": "Verified customers get a complimentary miso soup with combo orders.",
                "audience": Promotion.Audience.VERIFIED,
                "starts_at": now,
                "ends_at": now + timedelta(days=30),
                "active": True,
                "featured": True,
            },
        )
        Coupon.objects.get_or_create(
            code="WELCOME15",
            defaults={
                "description": "15% off the first order",
                "discount_type": Coupon.DiscountType.PERCENTAGE,
                "value": Decimal("15.00"),
                "minimum_order": Decimal("25.00"),
                "verified_only": False,
                "active": True,
                "starts_at": now,
                "ends_at": now + timedelta(days=60),
            },
        )

        self.stdout.write(self.style.SUCCESS("Brazilian Sushi demo data seeded successfully."))
