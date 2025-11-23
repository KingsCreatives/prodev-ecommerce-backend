from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from .filters import ProductFilter
from core.permissions import IsAdminOrReadOnly
from utils.pagination import StandardResultsSetPagination
from .docs import (
    list_summary, list_description, list_responses,
    retrieve_summary, retrieve_description, retrieve_responses,
    create_summary, create_description, create_responses,
    update_summary, update_description, update_responses,
    partial_update_summary, partial_update_description, partial_update_responses,
    delete_summary, delete_description, delete_responses
)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False).select_related("category").prefetch_related("images")
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "created_at", "stock"]
    ordering = ["-created_at"]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_summary=list_summary,
        operation_description=list_description,
        responses=list_responses,
        tags=["Products"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=retrieve_summary,
        operation_description=retrieve_description,
        responses=retrieve_responses,
        tags=["Products"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=create_summary,
        operation_description=create_description,
        request_body=ProductSerializer,
        responses=create_responses,
        tags=["Products"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=update_summary,
        operation_description=update_description,
        request_body=ProductSerializer,
        responses=update_responses,
        tags=["Products"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=partial_update_summary,
        operation_description=partial_update_description,
        request_body=ProductSerializer,
        responses=partial_update_responses,
        tags=["Products"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=delete_summary,
        operation_description=delete_description,
        responses=delete_responses,
        tags=["Products"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.select_related("product").all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  

    def get_queryset(self):
        """
        filter by ?product_id=<uuid>  fetch images
        for a single product.
        """
        qs = super().get_queryset()
        product_id = self.request.query_params.get("product_id")
        if product_id:
            qs = qs.filter(product_id=product_id).order_by("-is_primary", "created_at")
        return qs

    def perform_create(self, serializer):
        """
        is_primary=True, unset other primary images
        for uniqueness .
        """
        is_primary = serializer.validated_data.get("is_primary", False)
        product_id = serializer.validated_data.get("product_id") or self.request.data.get("product_id")

        with transaction.atomic():
            instance = serializer.save()
            if is_primary:
                ProductImage.objects.filter(product_id=product_id).exclude(pk=instance.pk).update(is_primary=False)
        return instance

    def perform_update(self, serializer):
        """
        If updating to is_primary=True, ensure others are cleared.
        """
        is_primary = serializer.validated_data.get("is_primary", None)
        with transaction.atomic():
            instance = serializer.save()
            if is_primary:
                ProductImage.objects.filter(product_id=instance.product_id).exclude(pk=instance.pk).update(is_primary=False)
        return instance
