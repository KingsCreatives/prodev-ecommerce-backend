from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    order_id = serializers.UUIDField(write_only=True, required=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order_id", "order", "product", "product_id", "quantity", "unit_price", "total_price"]
        read_only_fields = ["id", "order", "product", "unit_price", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "total_amount", "currency", "status", "created_at", "updated_at", "items"]
        read_only_fields = ["id", "user", "created_at", "updated_at", "total_amount"]
