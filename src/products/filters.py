from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = filters.CharFilter(field_name="category__slug", lookup_expr="iexact")
    in_stock = filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        fields = ["category", "price_min", "price_max", "in_stock"]

    def filter_in_stock(self, queryset, name, value):
        if value in (True, "true", "1"):
            return queryset.filter(stock__gt=0)
        if value in (False, "false", "0"):
            return queryset.filter(stock__lte=0)
        return queryset
