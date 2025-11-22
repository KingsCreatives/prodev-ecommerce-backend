from drf_yasg import openapi
from .serializers import OrderSerializer, OrderItemSerializer

list_summary = "List orders"
list_description = (
    "Return paginated orders for the authenticated user. Admins can list all orders.\n\n"
    "Order detail includes nested items when available."
)
list_responses = {200: openapi.Response("A paginated list of orders", OrderSerializer(many=True))}

retrieve_summary = "Retrieve order"
retrieve_description = "Return a single order with nested items. Only the owner or admin can access."
retrieve_responses = {200: OrderSerializer(), 404: openapi.Response("Not found")}

create_summary = "Create order"
create_description = (
    "Create a new order. The authenticated user will be set as the order owner. "
    "Returned object contains order metadata. Use OrderItem endpoints to add items."
)
create_responses = {201: OrderSerializer(), 400: openapi.Response("Validation error")}

order_item_create_summary = "Create order item"
order_item_create_description = (
    "Add an item to an order. Payload: {\"order_id\": \"<order-uuid>\", \"product_id\": \"<product-uuid>\", \"quantity\": n}.\n\n"
    "Server snapshots the product price into unit_price and calculates total_price."
)
order_item_create_responses = {201: OrderItemSerializer(), 400: openapi.Response("Validation error")}

update_summary = "Update order"
update_description = "Update order fields (status) — admin-only for status changes."
update_responses = {200: OrderSerializer(), 403: openapi.Response("Forbidden")}
