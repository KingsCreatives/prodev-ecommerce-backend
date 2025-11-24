from drf_yasg import openapi
from .serializers import CartSerializer, CartItemSerializer

cart_list_summary = "Get user cart"
cart_list_description = (
    "Return the authenticated user's cart including nested items and product info. "
    "If the user has no cart, it will be empty or created when the first item is added."
)
cart_list_responses = {
    200: openapi.Response("User cart", CartSerializer()),
    401: openapi.Response("Authentication credentials were not provided."),
}

cart_retrieve_summary = "Retrieve user cart"
cart_retrieve_description = (
    "Retrieve the authenticated user's cart including nested items, product details, "
    "totals, and quantities."
)
cart_retrieve_responses = {
    200: openapi.Response("User cart", CartSerializer()),
    401: openapi.Response("Authentication credentials were not provided."),
}


cart_item_create_summary = "Add item to cart"
cart_item_create_description = (
    "Add a product to the authenticated user's cart.\n\n"
    "Payload: {\"product_id\": \"<uuid>\", \"quantity\": n}.\n\n"
    "If the product already exists in the cart the server increments the quantity atomically "
    "and returns the updated CartItem. If the product does not exist, a new CartItem is created."
)
cart_item_create_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["product_id"],
    properties={
        "product_id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid", description="UUID of the product to add"),
        "quantity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of units to add (default 1)", default=1),
    },
)
cart_item_create_responses = {
    201: openapi.Response("Cart item created/updated", CartItemSerializer()),
    400: openapi.Response("Validation error"),
    401: openapi.Response("Authentication credentials were not provided."),
}


cart_item_update_summary = "Update cart item quantity"
cart_item_update_description = "Update the quantity of a cart item. Quantity must be an integer >= 1."
cart_item_update_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["quantity"],
    properties={
        "quantity": openapi.Schema(type=openapi.TYPE_INTEGER, description="New quantity for the cart item (>=1)"),
    },
)
cart_item_update_responses = {
    200: openapi.Response("Cart item updated", CartItemSerializer()),
    400: openapi.Response("Validation error"),
    401: openapi.Response("Authentication credentials were not provided."),
}

cart_examples = {
    "add_example": {
        "summary": "Add 2 units of a product",
        "value": {"product_id": "11111111-1111-1111-1111-111111111111", "quantity": 2},
    },
    "update_example": {
        "summary": "Set quantity to 3",
        "value": {"quantity": 3},
    },
}
