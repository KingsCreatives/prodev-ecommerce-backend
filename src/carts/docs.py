from drf_yasg import openapi
from .serializers import CartSerializer, CartItemSerializer

cart_list_summary = "Get user cart"
cart_list_description = (
    "Return the authenticated user's cart including nested items and product info. "
    "If the user has no cart, it will be empty or created when the first item is added."
)
cart_list_responses = {200: openapi.Response("User cart", CartSerializer())}

cart_item_create_summary = "Add item to cart"
cart_item_create_description = (
    "Add a product to the authenticated user's cart. Payload: {\"product_id\": \"<uuid>\", \"quantity\": n}.\n\n"
    "If the product already exists in cart, the server increments the quantity atomically."
)
cart_item_create_responses = {201: CartItemSerializer(), 400: openapi.Response("Validation error")}

cart_item_update_summary = "Update cart item quantity"
cart_item_update_description = "Update the quantity of a cart item. Quantity must be >= 1."
cart_item_update_responses = {200: CartItemSerializer(), 400: openapi.Response("Validation error")}
