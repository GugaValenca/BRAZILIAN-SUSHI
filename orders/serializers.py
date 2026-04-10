from rest_framework import serializers

from menu.models import MenuItem, MenuOption

from .models import DeliveryZone, Order, OrderItem, OrderItemSelection, OrderStatusEvent


class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = "__all__"


class OrderItemWriteSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    option_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    special_request = serializers.CharField(required=False, allow_blank=True)


class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "delivery_address",
            "coupon",
            "delivery_zone",
            "order_type",
            "guest_name",
            "guest_email",
            "guest_phone",
            "scheduled_for",
            "notes",
            "allergy_notes",
            "notification_preference",
            "items",
        )
        read_only_fields = ("customer",)

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user if request.user.is_authenticated else None

        if user:
            attrs["guest_name"] = user.get_full_name().strip() or user.username
            attrs["guest_email"] = user.email
            attrs["guest_phone"] = user.phone_number
            attrs["notification_preference"] = user.notification_preference
            return attrs

        missing_fields = [
            field_name
            for field_name in ("guest_name", "guest_email", "guest_phone", "notification_preference")
            if not attrs.get(field_name)
        ]
        if missing_fields:
            raise serializers.ValidationError(
                {field_name: "This field is required for guest checkout." for field_name in missing_fields}
            )

        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        request = self.context["request"]
        user = request.user if request.user.is_authenticated else None
        order = Order.objects.create(customer=user, **validated_data)
        subtotal = 0
        for item_data in items_data:
            menu_item = MenuItem.objects.get(pk=item_data["menu_item_id"])
            option_ids = item_data.get("option_ids", [])
            selected_options = list(MenuOption.objects.filter(id__in=option_ids))
            extra_cost = sum(option.price_delta for option in selected_options)
            unit_price = menu_item.price + extra_cost
            line_total = unit_price * item_data["quantity"]
            order_item = OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item_data["quantity"],
                unit_price=unit_price,
                line_total=line_total,
                special_request=item_data.get("special_request", ""),
            )
            for option in selected_options:
                OrderItemSelection.objects.create(order_item=order_item, option=option, price_delta=option.price_delta)
            subtotal += line_total

        if order.delivery_zone and order.order_type == Order.OrderType.DELIVERY:
            order.delivery_fee = order.delivery_zone.fee
            order.estimated_minutes = order.delivery_zone.average_minutes

        order.subtotal = subtotal
        order.total = subtotal + order.delivery_fee - order.discount_amount
        order.save()
        OrderStatusEvent.objects.create(order=order, status=order.status, note="Order created")
        return order


class OrderItemSelectionSerializer(serializers.ModelSerializer):
    option_name = serializers.CharField(source="option.name", read_only=True)

    class Meta:
        model = OrderItemSelection
        fields = ("id", "option", "option_name", "price_delta")


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source="menu_item.name", read_only=True)
    selections = OrderItemSelectionSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "menu_item", "menu_item_name", "quantity", "unit_price", "line_total", "special_request", "selections")


class OrderStatusEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusEvent
        fields = ("id", "status", "note", "created_at")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_events = OrderStatusEventSerializer(many=True, read_only=True)
    average_delivery_time = serializers.ReadOnlyField()
    has_kitchen_notes = serializers.SerializerMethodField()
    has_allergy_alert = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_has_kitchen_notes(self, obj):
        return bool((obj.notes or "").strip() or (obj.allergy_notes or "").strip())

    def get_has_allergy_alert(self, obj):
        return bool((obj.allergy_notes or "").strip())
