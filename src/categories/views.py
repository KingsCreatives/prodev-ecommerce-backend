from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from core.permissions import IsAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from .docs import (
    list_summary, list_description, list_responses,
    retrieve_summary, retrieve_description, retrieve_responses,
    create_summary, create_description, create_responses,
    update_summary, update_description, update_responses,
    partial_update_summary, partial_update_description, partial_update_responses,
    delete_summary, delete_description, delete_responses
)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_summary=list_summary,
        operation_description=list_description,
        responses=list_responses,
        tags=["Categories"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=retrieve_summary,
        operation_description=retrieve_description,
        responses=retrieve_responses,
        tags=["Categories"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=create_summary,
        operation_description=create_description,
        request_body=CategorySerializer,
        responses=create_responses,
        tags=["Categories"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=update_summary,
        operation_description=update_description,
        request_body=CategorySerializer,
        responses=update_responses,
        tags=["Categories"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=partial_update_summary,
        operation_description=partial_update_description,
        request_body=CategorySerializer,
        responses=partial_update_responses,
        tags=["Categories"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=delete_summary,
        operation_description=delete_description,
        responses=delete_responses,
        tags=["Categories"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
