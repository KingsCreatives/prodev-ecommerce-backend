from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ["id","order", "product", "product_id", "quantity", "unit_price", "total_price"]
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

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
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