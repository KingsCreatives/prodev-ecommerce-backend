from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer

User = get_user_model()

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = {
            "id" : str(user.id),
            "email" : user.email,
            "username" : getattr(user, "username", None)
        }
        return Response(data, status=status.HTTP_200_OK)