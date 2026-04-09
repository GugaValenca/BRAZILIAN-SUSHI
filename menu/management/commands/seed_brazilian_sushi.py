from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from marketing.models import Coupon, Promotion, Review
from menu.models import Category, MenuItem, MenuOption, MenuOptionGroup
from orders.models import DeliveryZone

User = get_user_model()


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
                "category": "Nigiri",
                "name": "Tuna Nigiri",
                "slug": "tuna-nigiri",
                "short_description": "Premium tuna over warm seasoned rice.",
                "description": "Finished with a precise touch of wasabi.",
                "price": Decimal("10.99"),
                "allergens": "fish",
                "featured": False,
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
                "category": "Rolls",
                "name": "Dragon Roll",
                "slug": "dragon-roll",
                "short_description": "Shrimp tempura inside, topped with avocado and eel sauce.",
                "description": "A generous signature roll with crisp texture and silky finish.",
                "price": Decimal("16.99"),
                "allergens": "shellfish,gluten",
                "featured": True,
            },
            {
                "category": "Rolls",
                "name": "Veggie Garden Roll",
                "slug": "veggie-garden-roll",
                "short_description": "Avocado, cucumber, carrot, and asparagus.",
                "description": "Bright, clean, and balanced with a light ponzu finish.",
                "price": Decimal("11.99"),
                "allergens": "",
                "vegetarian": True,
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
                "category": "Sashimi",
                "name": "Salmon Sashimi",
                "slug": "salmon-sashimi",
                "short_description": "Six slices of fresh salmon with pickled ginger.",
                "description": "Clean, buttery cuts prepared for purity and texture.",
                "price": Decimal("14.99"),
                "allergens": "fish",
                "featured": False,
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
                "category": "Combos",
                "name": "Date Night Combo",
                "slug": "date-night-combo",
                "short_description": "Chef-selected rolls with miso soup and edamame for two.",
                "description": "A polished, shareable set designed for an easy evening in.",
                "price": Decimal("36.99"),
                "allergens": "fish,soy",
                "featured": False,
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
            {
                "category": "Soups & Sides",
                "name": "Edamame",
                "slug": "edamame",
                "short_description": "Steamed young soybeans finished with sea salt.",
                "description": "Simple, warm, and ideal with rolls or sashimi.",
                "price": Decimal("5.99"),
                "allergens": "soy",
                "vegetarian": True,
            },
            {
                "category": "Beverages",
                "name": "Yuzu Sparkling Soda",
                "slug": "yuzu-sparkling-soda",
                "short_description": "Bright citrus soda with a crisp finish.",
                "description": "A refreshing pairing for sashimi, nigiri, and lighter rolls.",
                "price": Decimal("4.50"),
                "allergens": "",
                "vegetarian": True,
            },
        ]

        for item_data in items:
            item_data = item_data.copy()
            category = category_map[item_data.pop("category")]
            item, _ = MenuItem.objects.update_or_create(
                slug=item_data["slug"],
                defaults={**item_data, "category": category},
            )
            if item.slug == "brazilian-roll":
                group, _ = MenuOptionGroup.objects.update_or_create(
                    menu_item=item,
                    name="Protein upgrade",
                    defaults={"required": False, "min_select": 0, "max_select": 1},
                )
                MenuOption.objects.update_or_create(group=group, name="Extra salmon", defaults={"price_delta": Decimal("4.00")})
                MenuOption.objects.update_or_create(group=group, name="Add tuna", defaults={"price_delta": Decimal("3.50")})

        for postal_code, fee, avg in [("60601", Decimal("4.99"), 35), ("60602", Decimal("5.99"), 42), ("60603", Decimal("6.99"), 48)]:
            DeliveryZone.objects.update_or_create(
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
        Promotion.objects.update_or_create(
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
        Promotion.objects.update_or_create(
            title="First Order 15% Off",
            defaults={
                "description": "Enjoy 15% off your first online order when your cart reaches $25 or more.",
                "audience": Promotion.Audience.ALL,
                "starts_at": now,
                "ends_at": now + timedelta(days=45),
                "active": True,
                "featured": True,
            },
        )
        Coupon.objects.update_or_create(
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
        Coupon.objects.update_or_create(
            code="PICKUP10",
            defaults={
                "description": "$10 off pickup orders over $45",
                "discount_type": Coupon.DiscountType.FIXED,
                "value": Decimal("10.00"),
                "minimum_order": Decimal("45.00"),
                "verified_only": False,
                "active": True,
                "starts_at": now,
                "ends_at": now + timedelta(days=45),
            },
        )

        review_entries = [
            {
                "email": "maria.santos.review@braziliansushi.local",
                "username": "mariasantosreview",
                "first_name": "Maria",
                "last_name": "Santos",
                "rating": 5,
                "title": "Beautifully packed and consistently fresh",
                "content": "The rolls arrive neatly presented, the sashimi tastes pristine, and the entire order feels carefully prepared from start to finish.",
            },
            {
                "email": "james.lee.review@braziliansushi.local",
                "username": "jamesleereview",
                "first_name": "James",
                "last_name": "Lee",
                "rating": 5,
                "title": "A premium delivery experience",
                "content": "From checkout to delivery updates, everything feels polished. The nigiri and hand rolls arrive with the texture and balance you hope for.",
            },
            {
                "email": "ana.paula.review@braziliansushi.local",
                "username": "anapaulareview",
                "first_name": "Ana",
                "last_name": "Paula",
                "rating": 5,
                "title": "Reliable, refined, and easy to love",
                "content": "The menu has range, the combos are generous, and the flavors feel elevated without losing warmth. It is our go-to sushi night choice.",
            },
        ]

        for review_entry in review_entries:
            user, created = User.objects.get_or_create(
                email=review_entry["email"],
                defaults={
                    "username": review_entry["username"],
                    "first_name": review_entry["first_name"],
                    "last_name": review_entry["last_name"],
                    "is_verified_customer": True,
                    "verified_reason": User.VerificationReason.ORDER_HISTORY,
                    "email_opt_in": True,
                    "sms_opt_in": False,
                },
            )
            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])

            Review.objects.update_or_create(
                user=user,
                title=review_entry["title"],
                defaults={
                    "rating": review_entry["rating"],
                    "content": review_entry["content"],
                    "approval_status": Review.ApprovalStatus.APPROVED,
                },
            )

        self.stdout.write(self.style.SUCCESS("Brazilian Sushi demo data seeded successfully."))
