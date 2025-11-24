from django.db import transaction
from rest_framework import serializers
from .models import Product, ProductImage


class EmptySerializer(serializers.Serializer):
    """
    Used to bypass automatic request body generation in Swagger 
    for endpoints using manual parameters.
    """
    pass

class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image", "alt_text", "is_primary")

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ("id", "image_url", "alt_text", "is_primary", "created_at")
        read_only_fields = ("id", "image_url", "created_at")

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class ProductSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    images_upload = ProductImageCreateSerializer(many=True, write_only=True, required=False)
    images_delete = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "description",
            "price",
            "discount_percent",
            "stock",
            "image",
            "primary_image",
            "images",
            "images_upload",
            "images_delete",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "primary_image", "images", "created_at", "updated_at"]

    def get_primary_image(self, obj):
        return obj.primary_image_url

    def create(self, validated_data):
        images_data = validated_data.pop("images_upload", [])
        with transaction.atomic():
            product = super().create(validated_data)
            self._handle_images_ops(product, images_data, images_delete_uuids=None)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images_upload", [])
        images_delete_ids = validated_data.pop("images_delete", [])

        with transaction.atomic():
            product = super().update(instance, validated_data)
            self._handle_images_ops(product, images_data, images_delete_ids)
        return product

    def _handle_images_ops(self, product, images_upload_data, images_delete_uuids):
        """Orchestrates image creation, deletion, and primary flag updates."""
        created_imgs = []
        
        if images_upload_data:
            created_imgs = self._create_images(product, images_upload_data)
        if images_delete_uuids:
            self._delete_images_by_ids(product, images_delete_uuids)
        if any(getattr(i, "is_primary", False) for i in created_imgs):
            # If a new image is primary, unset others
            primary_ids = [i.pk for i in created_imgs if i.is_primary]
            ProductImage.objects.filter(product=product).exclude(pk__in=primary_ids).update(is_primary=False)
        self._ensure_primary_after_deletion(product)

    def _create_images(self, product, images_data):
        created_images = []
        for img in images_data:
            instance = ProductImage.objects.create(product=product, **img)
            created_images.append(instance)
        return created_images

    def _delete_images_by_ids(self, product, uuids):
        if not uuids:
            return
        
        to_delete_qs = ProductImage.objects.filter(product=product, id__in=uuids)
        for inst in to_delete_qs:
            if inst.image:
                try:
                    inst.image.delete(save=False)
                except Exception:
                    pass 
            inst.delete()

    def _ensure_primary_after_deletion(self, product):
        """If no primary image exists, set the latest one as primary."""
        if not product.images.filter(is_primary=True).exists():
            latest = product.images.order_by("-created_at").first()
            if latest:
                latest.is_primary = True
                latest.save(update_fields=["is_primary"])