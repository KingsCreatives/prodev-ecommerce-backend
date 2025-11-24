from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from utils.pagination import StandardResultsSetPagination
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .docs import (
    cart_list_summary, cart_list_description, cart_list_responses,
    cart_retrieve_summary, cart_retrieve_responses, cart_retrieve_description,
    cart_item_create_summary, cart_item_create_description, cart_item_create_responses,
    cart_item_update_summary, cart_item_update_description, cart_item_update_responses,
)


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = Cart.objects.select_related("user").prefetch_related("items__product")
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = getattr(self.request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return qs.none()
        if user.is_staff:
            return qs.all()
        return qs.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(operation_summary=cart_list_summary, operation_description=cart_list_description, responses=cart_list_responses, tags=["Carts"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=cart_retrieve_summary, operation_description=cart_retrieve_description, responses=cart_retrieve_responses, tags=["Carts"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Carts"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Carts"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Carts"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Carts"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = CartItem.objects.select_related("cart", "product")
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = getattr(self.request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return qs.none()
        if user.is_staff:
            return qs.all()
        return qs.filter(cart__user=user)

    @swagger_auto_schema(operation_summary=cart_item_create_summary, operation_description=cart_item_create_description, responses=cart_item_create_responses, tags=["Cart-Item"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = serializer.validated_data.pop("product_id")
        quantity = serializer.validated_data.get("quantity", 1)

        with transaction.atomic():
            try:
                product = Product.objects.select_for_update().get(pk=product_id)
            except Product.DoesNotExist:
                raise ValidationError({"product_id": "Product does not exist."})

            cart, _ = Cart.objects.select_for_update().get_or_create(user=user)

            if hasattr(product, "stock") and product.stock < quantity:
                raise ValidationError({"quantity": "Not enough stock available."})

            item_qs = CartItem.objects.select_for_update().filter(cart=cart, product=product)
            if item_qs.exists():
                item = item_qs.get()
                new_qty = item.quantity + quantity
                if hasattr(product, "stock") and product.stock < new_qty:
                    raise ValidationError({"quantity": "Not enough stock available for requested total quantity."})
                item.quantity = new_qty
                item.save()
                serializer.instance = item
            else:
                serializer.save(cart=cart, product=product)

    @swagger_auto_schema(operation_summary=cart_item_update_summary, operation_description=cart_item_update_description, responses=cart_item_update_responses, tags=["Cart-Item"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=cart_item_update_summary, operation_description=cart_item_update_description, responses=cart_item_update_responses, tags=["Cart-Item"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete cart item", operation_description="Remove an item from the cart.", responses={204: "Deleted"}, tags=["Cart-Item"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary="List cart items", operation_description="List cart items for the authenticated user", responses={200: CartItemSerializer(many=True)}, tags=["Cart-Item"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve cart item", operation_description="Get a single cart item by id", responses={200: CartItemSerializer()}, tags=["Cart-Item"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)