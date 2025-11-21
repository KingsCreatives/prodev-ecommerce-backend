from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "title", "slug", "category", "description",
            "price", "discount_percent", "stock", "image",
            "primary_image",  
            "is_active", "is_deleted", "created_at", "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_primary_image(self, obj):
        return obj.primary_image_url
