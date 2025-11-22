from uuid import uuid4
from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_ORDER = "order"
    TYPE_PRODUCT = "product"
    TYPE_SYSTEM = "system"

    NOTIF_TYPE_CHOICES = [
        (TYPE_ORDER, "Order"),
        (TYPE_PRODUCT, "Product"),
        (TYPE_SYSTEM, "System"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES, default=TYPE_SYSTEM)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_order_id = models.UUIDField(null=True, blank=True)
    related_product_id = models.UUIDField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["user", "is_read"]),
        ]
        ordering = ["-created_at"]

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=["is_read"])

    def __str__(self):
        return f"Notification({self.user_id}) {self.title}"
