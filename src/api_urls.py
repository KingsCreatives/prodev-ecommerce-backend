from rest_framework import routers
from categories.views import CategoryViewSet
from products.views import ProductViewSet
from carts.views import CartViewSet, CartItemViewSet
from orders.views import OrderViewSet, OrderItemViewSet
from addresses.views import AddressViewSet
from notifications.views import NotificationViewSet

router = routers.DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"carts", CartViewSet, basename="carts")
router.register(r"cart-items", CartItemViewSet, basename="cart-items")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"order-items", OrderItemViewSet, basename="order-items")
router.register(r"addresses", AddressViewSet, basename="addresses")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = router.urls
