from celery import shared_task
from celery.exceptions import Retry
from .models import Notification
from products.models import Product
from orders.models import Order 
import time

@shared_task(bind=True, max_retries=3)
def send_new_product_notification(self, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise self.retry(countdown=3, exc=Retry("Product not found yet"))

    Notification.objects.create(
        user=None,
        message=f"New product added: {product.title}"
    )
    return "product_notification_sent"


@shared_task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise self.retry(countdown=3, exc=Retry("Order not found yet"))

    time.sleep(1)

    Notification.objects.create(
        user=order.user,
        message=f"Order {order.id} confirmed. Total: {order.total_amount}"
    )

    print(f"EMAIL SENT: Order confirmation for Order #{order.id} sent to user.")
    
    return "order_email_sent"