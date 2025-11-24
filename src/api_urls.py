from rest_framework import routers
from addresses.views import AddressViewSet
from carts.views import CartViewSet, CartItemViewSet
from categories.views import CategoryViewSet
from notifications.views import NotificationViewSet
from orders.views import OrderViewSet, OrderItemViewSet
from products.views import ProductViewSet, ProductImageViewSet

router = routers.DefaultRouter()

router.register(r"addresses", AddressViewSet, basename="Addresses")
router.register(r"carts", CartViewSet, basename="Carts")
router.register(r"cart-items", CartItemViewSet, basename="Cart-Item")
router.register(r"categories", CategoryViewSet, basename="Categories")
router.register(r"notifications", NotificationViewSet, basename="Notifications")
router.register(r"orders", OrderViewSet, basename="Orders")
router.register(r"order-items", OrderItemViewSet, basename="Order-Item")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"product-images", ProductImageViewSet, basename="Product-Images")

urlpatterns = router.urls
