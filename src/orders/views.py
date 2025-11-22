from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from django.shortcuts import get_object_or_404
from utils.pagination import StandardResultsSetPagination
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from products.models import Product
from .docs import (
    list_summary, list_description, list_responses,
    retrieve_summary, retrieve_description, retrieve_responses,
    create_summary, create_description, create_responses,
    order_item_create_summary, order_item_create_description, order_item_create_responses,
    update_summary, update_description, update_responses
)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = Order.objects.select_related("user").prefetch_related("items", "items__product")
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = getattr(self.request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return qs.none()
        if user.is_staff:
            return qs.all()
        return qs.filter(user=user)


    @swagger_auto_schema(operation_summary=list_summary, operation_description=list_description, responses=list_responses, tags=["Orders"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=retrieve_summary, operation_description=retrieve_description, responses=retrieve_responses, tags=["Orders"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=create_summary, operation_description=create_description, request_body=OrderSerializer, responses=create_responses, tags=["Orders"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=update_summary, operation_description=update_description, request_body=OrderSerializer, responses=update_responses, tags=["Orders"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = OrderItem.objects.select_related("order", "product")
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = getattr(self.request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return qs.none()
        if user.is_staff:
            return qs.all()
        return qs.filter(order__user=user)


    def perform_create(self, serializer):
        order_id = serializer.validated_data.pop("order_id")
        product_id = serializer.validated_data.pop("product_id")
        quantity = serializer.validated_data.get("quantity", 1)

        with transaction.atomic():
            order = get_object_or_404(Order.objects.select_for_update(), pk=order_id)
            if not self.request.user.is_staff and order.user != self.request.user:
                raise PermissionDenied("Cannot add items to another user's order.")

            product = get_object_or_404(Product.objects.select_for_update(), pk=product_id)

            if hasattr(product, "stock") and product.stock < quantity:
                raise ValidationError({"quantity": "Not enough stock available."})

            unit_price = product.price

            item = OrderItem(order=order, product=product, quantity=quantity, unit_price=unit_price)
            item.save()  # OrderItem.save computes total_price

            order.update_total()

        return None

    def perform_update(self, serializer):
        instance = serializer.instance
        new_quantity = serializer.validated_data.get("quantity", instance.quantity)

        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=instance.order_id)

            if hasattr(instance.product, "stock") and instance.product.stock < new_quantity:
                raise ValidationError({"quantity": "Not enough stock available."})

            serializer.save()
            order.update_total()

    def perform_destroy(self, instance):
        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=instance.order_id)
            instance.delete()
            order.update_total()

    @swagger_auto_schema(operation_summary=order_item_create_summary, operation_description=order_item_create_description, request_body=OrderItemSerializer, responses=order_item_create_responses, tags=["Orders"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update order item", operation_description="Update an order item quantity", request_body=OrderItemSerializer, responses={200: OrderItemSerializer()}, tags=["Orders"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
