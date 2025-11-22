from rest_framework import serializers
from products.serializers import ProductSerializer
from products.models import Product
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "created_at"]
        read_only_fields = ["id", "product", "created_at"]

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        
        quantity = self.initial_data.get("quantity", 1)
        try:
            q = int(quantity)
        except (TypeError, ValueError):
            q = 1
        if hasattr(product, "stock") and product.stock < q:
            raise serializers.ValidationError("Not enough stock available for this product.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "created_at"]
        read_only_fields = ["id", "created_at"]
