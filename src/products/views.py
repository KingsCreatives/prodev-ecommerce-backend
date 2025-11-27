from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from core.permissions import IsAdminOrReadOnly
from utils.pagination import StandardResultsSetPagination
from .models import Product, ProductImage
from .filters import ProductFilter
from notifications.tasks import send_new_product_notification
from .serializers import (
    ProductSerializer, 
    ProductImageSerializer, 
    EmptySerializer
)
from .docs import (
    product_form_parameters,
    list_summary, list_description, list_responses,
    retrieve_summary, retrieve_description, retrieve_responses,
    create_summary, create_description, create_responses,
    update_summary, update_description, update_responses,
    partial_update_summary, partial_update_description, partial_update_responses,
    delete_summary, delete_description, delete_responses
)

class ProductViewSet(ModelViewSet):
    """
    Product endpoints using multipart/form-data for uploads.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "created_at", "stock"]
    ordering = ["-created_at"]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Product.objects.none()
    
        return Product.objects.filter(is_deleted=False)\
            .select_related("category")\
            .prefetch_related("images")

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @swagger_auto_schema(
        operation_summary=list_summary, 
        operation_description=list_description, 
        responses=list_responses, 
        tags=["Products"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=retrieve_summary, 
        operation_description=retrieve_description, 
        responses=retrieve_responses, 
        tags=["Products"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=create_summary,
        operation_description=create_description,
        request_body=EmptySerializer,
        manual_parameters=product_form_parameters,
        responses=create_responses,
        tags=["Products"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=update_summary,
        operation_description=update_description,
        request_body=EmptySerializer,
        manual_parameters=product_form_parameters,
        responses=update_responses,
        tags=["Products"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=partial_update_summary,
        operation_description=partial_update_description,
        request_body=EmptySerializer,
        manual_parameters=product_form_parameters,
        responses=partial_update_responses,
        tags=["Products"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=delete_summary, 
        operation_description=delete_description, 
        responses=delete_responses, 
        tags=["Products"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        product = serializer.save()
        transaction.on_commit(lambda: send_new_product_notification.delay(str(product.id)))


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.select_related("product").all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.request.query_params.get("product_id")
        if product_id:
            qs = qs.filter(product_id=product_id).order_by("-is_primary", "created_at")
        return qs

    def perform_create(self, serializer):
        is_primary = serializer.validated_data.get("is_primary", False)
        product_id = serializer.validated_data.get("product_id") or self.request.data.get("product_id")
        
        with transaction.atomic():
            instance = serializer.save()
            if is_primary:
                self._unset_other_primaries(product_id, instance.pk)
        return instance

    def perform_update(self, serializer):
        is_primary = serializer.validated_data.get("is_primary", None)
        with transaction.atomic():
            instance = serializer.save()
            if is_primary:
                self._unset_other_primaries(instance.product_id, instance.pk)
        return instance

    def _unset_other_primaries(self, product_id, current_image_pk):
        ProductImage.objects.filter(product_id=product_id)\
            .exclude(pk=current_image_pk)\
            .update(is_primary=False)