from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from utils.pagination import StandardResultsSetPagination
from .models import Notification
from .serializers import NotificationSerializer
from .docs import (
    list_summary, list_description, list_responses,
    mark_read_bulk_summary, mark_read_bulk_description, mark_read_bulk_responses,
    single_mark_read_summary, single_mark_read_description, single_mark_read_responses,
)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = Notification.objects.select_related("user")
        if getattr(self, "swagger_fake_view", False):
            return qs.none()
        user = getattr(self.request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return qs.none()
        return qs.filter(user=user)

    @swagger_auto_schema(operation_summary=list_summary, operation_description=list_description, responses=list_responses, tags=["Notifications"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve notification", operation_description="Get a single notification", responses={200: NotificationSerializer()}, tags=["Notifications"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Notifications"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Notifications"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Notifications"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Notifications"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        if serializer.validated_data.get("user") is None:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    @action(detail=False, methods=["post"], url_path="mark-read", url_name="mark_read")
    @swagger_auto_schema(
        operation_summary=mark_read_bulk_summary,
        operation_description=mark_read_bulk_description,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))}
        ),
        responses=mark_read_bulk_responses,
        tags=["Notifications"],
    )
    def mark_read_bulk(self, request):
        ids = request.data.get("ids") or []
        if not isinstance(ids, (list, tuple)):
            return Response({"detail": "ids must be a list of UUIDs"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        with transaction.atomic():
            qs = Notification.objects.filter(user=user, id__in=ids, is_read=False).select_for_update()
            updated = qs.update(is_read=True)
        return Response({"updated": updated}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="mark-read-single", url_name="mark_read_single")
    @swagger_auto_schema(
        operation_summary=single_mark_read_summary,
        operation_description=single_mark_read_description,
        responses=single_mark_read_responses,
        tags=["Notifications"],
    )
    def mark_read_single(self, request, pk=None):
        notif = self.get_object()
        if notif.user_id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        notif.mark_read()
        return Response({"id": str(notif.id), "is_read": notif.is_read}, status=status.HTTP_200_OK)
