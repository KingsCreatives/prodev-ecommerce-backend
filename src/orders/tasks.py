from celery import shared_task
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Order
from products.models import Product
from notifications.tasks import send_order_confirmation

@shared_task
def fulfill_order_task(order_id):
    """
    Handles post-payment logic: stock reduction, invoice marking, 
    and triggering notifications.
    """
    with transaction.atomic():
        order = get_object_or_404(Order.objects.select_for_update(), id=order_id)
        
        if order.status != 'paid':
            order.status = 'paid'
            order.save()

        for item in order.items.all():
            product = item.product
            if hasattr(product, 'stock'):
                product.stock -= item.quantity
                product.save()

    send_order_confirmation.delay(str(order.id))

    return f"Order {order_id} fulfilled successfully."