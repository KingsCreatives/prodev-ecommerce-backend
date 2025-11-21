from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from core.permissions import IsAdminOrReadOnly
from .models import Product
from .serializer import ProductSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    
class ProductViewSet(ModelViewSet):
   queryset = Product.objects.filter(is_deleted=False).select_related("category").prefetch_related("images")
   permission_classes = [IsAdminOrReadOnly]
   serializer_class = ProductSerializer
   pagination_class = StandardResultsSetPagination
    
