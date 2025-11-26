from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema
from .docs import (
    register_summary, register_description, register_responses,
    me_summary, me_description, me_parameters, me_responses
)


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary=register_summary,
        operation_description=register_description,
        request_body=RegisterSerializer,
        responses=register_responses,
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary=me_summary,
        operation_description=me_description,
        manual_parameters=me_parameters,
        responses=me_responses,
        tags=["Authentication"],
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)