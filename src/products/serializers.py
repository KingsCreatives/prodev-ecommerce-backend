from rest_framework import serializers
from django.db import transaction
from .models import Product, ProductImage
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
    images_upload = ProductImageCreateSerializer(many=True, write_only=True, required=False) # For nested writes:
    images_delete = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    ) #list of image UUIDs to delete on update

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

    def _create_images(self, product, images_data):
        created_images = []
        for img in images_data:
            instance = ProductImage.objects.create(product=product, **img)
            created_images.append(instance)
        return created_images

    def _delete_images_by_ids(self, product, uuids):
        if not uuids:
            return []

        to_delete_qs = ProductImage.objects.filter(product=product, id__in=uuids)
        deleted_pks = []
        with transaction.atomic():
            for inst in list(to_delete_qs): 
                try:
                    if inst.image:
                        inst.image.delete(save=False)
                except Exception:
                    pass
                deleted_pks.append(inst.pk)
                inst.delete()
        return deleted_pks

    def _ensure_primary_after_deletion(self, product):
        if product.images.filter(is_primary=True).exists():
            return
        latest = product.images.order_by("-created_at").first()
        if latest:
            latest.is_primary = True
            latest.save(update_fields=["is_primary"])

    def _handle_images_ops(self, product, images_upload_data, images_delete_uuids):
        created = []
        if images_upload_data:
            created = self._create_images(product, images_upload_data)

        if images_delete_uuids:
            self._delete_images_by_ids(product, images_delete_uuids)

        if any(getattr(i, "is_primary", False) for i in created):
            primary_ids = [i.pk for i in created if i.is_primary]
            ProductImage.objects.filter(product=product).exclude(pk__in=primary_ids).update(is_primary=False)

        self._ensure_primary_after_deletion(product)

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
