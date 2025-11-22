from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from .models import Product
from .serializers import ProductSerializer
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
