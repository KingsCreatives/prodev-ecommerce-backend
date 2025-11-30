from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterView, MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ProDev E-Commerce API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("api/admin/", admin.site.urls),

    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0)),

    path("api/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path("api/auth/register/", RegisterView.as_view(), name="auth-register"),
    path("api/auth/me/", MeView.as_view(), name="auth-me"),

    path("api/", include("api_urls")),
]
