from rest_framework import viewsets, permissions
from drf_yasg.utils import swagger_auto_schema

from .models import Address
from .serializers import AddressSerializer
from utils.pagination import StandardResultsSetPagination
from .docs import (
    list_summary, list_description, list_responses,
    retrieve_summary, retrieve_description, retrieve_responses,
    create_summary, create_description, create_responses,
    update_summary, update_description, update_responses,
    partial_update_summary, partial_update_description, parital_update_responses,
    delete_summary, delete_description, delete_responses,
)
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = Address.objects.select_related("user")
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

    @swagger_auto_schema(operation_summary=list_summary, operation_description=list_description, responses=list_responses, tags=["Addresses"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=retrieve_summary, operation_description=retrieve_description, responses=retrieve_responses, tags=["Addresses"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary=create_summary, 
            operation_description=create_description, 
            request_body=AddressSerializer, 
            responses=create_responses, 
            tags=["Addresses"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=update_summary, operation_description=update_description, request_body=AddressSerializer, responses=update_responses, tags=["Addresses"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=partial_update_summary,operation_description=partial_update_description,
     request_body=AddressSerializer,
     responses=parital_update_responses, tags=["Addresses"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary=delete_summary, operation_description=delete_description, responses=delete_responses, tags=["Addresses"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
