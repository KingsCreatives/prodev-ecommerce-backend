from django.db import models
import uuid
from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="products"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False) #for soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name="price_gte_0"),
            models.CheckConstraint(check=models.Q(stock__gte=0), name="stock_gte_0"),
            models.CheckConstraint(
                                check=models.Q(discount_percent__gte=0) & models.Q(discount_percent__lte=100),
                                name="discount_between_0_and_100"
                                )
        ]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            i = 0
            while Product.objects.filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def primary_image_url(self):
        primary = self.images.filter(is_primary=True).first()
        if primary and primary.image:
            return primary.image.url
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/images/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)  # 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_primary=True),
                name="unique_primary_image_per_product"
            )
    ]


    def __str__(self):
        return f"Image for {self.product.title} ({self.id})"
