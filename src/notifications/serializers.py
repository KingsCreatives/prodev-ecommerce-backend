from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id", "notif_type", "title", "message",
            "related_order_id", "related_product_id",
            "is_read", "created_at"
        ]
        read_only_fields = ["id", "is_read", "created_at"]
