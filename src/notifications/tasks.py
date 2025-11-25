from celery import shared_task
from celery.exceptions import Retry
from .models import Notification
from products.models import Product


@shared_task(bind=True, max_retries=3)
def send_new_product_notification(self, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise self.retry(countdown=3, exc=Retry("Product not found yet"))

    Notification.objects.create(
        user=None,  # placeholder until we add user targeting
        message=f"New product added: {product.title}"
    )

    return "created"