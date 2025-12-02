from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "product_id", "quantity", "unit_price", "total_price"]
        read_only_fields = ["id", "order", "product", "unit_price", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    order_items = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=True
    )

    class Meta:
        model = Order
        fields = ["id", "user", "total_amount", "currency", "status", "created_at", "updated_at", "items", "order_items"]
        read_only_fields = ["id", "user", "created_at", "updated_at", "total_amount"]

    def validate_order_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
            
        for item in value:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if not product_id:
                raise serializers.ValidationError("Each item must have a 'product_id'.")
            
            if not quantity or int(quantity) < 1:
                raise serializers.ValidationError("Quantity must be at least 1.")

            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")
                
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        user = validated_data.pop('user', None) 
        
        if user is None:
            user = self.context['request'].user
    
        order = Order.objects.create(user=user, **validated_data)

        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.get('quantity', 1),
                unit_price=product.price
            )
        
        order.update_total()
        
        return order