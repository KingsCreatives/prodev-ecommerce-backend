from rest_framework import serializers
from products.serializers import ProductSerializer
from products.models import Product
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True, required=False) 
    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "created_at"]
        read_only_fields = ["id", "product", "created_at"]

    def validate(self, data):
        if self.instance:
            product = self.instance.product
        else:
            product_id = data.get("product_id")
            if not product_id:
                raise serializers.ValidationError({"product_id": "This field is required."})
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product_id": "Product does not exist."})
        
        quantity = data.get("quantity", 1)
        if hasattr(product, "stock") and product.stock < quantity:
            raise serializers.ValidationError({"quantity": "Not enough stock available."})
        
        data['product_obj'] = product 
        return data

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "created_at"]
        read_only_fields = ["id", "created_at"]