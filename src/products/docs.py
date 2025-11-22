from drf_yasg import openapi
from .serializers import ProductSerializer

list_summary = "List products"
list_description = (
    "Returns a paginated list of products. Supports search, filtering and ordering.\n\n"
    "Query parameters:\n"
    "- search: full-text search against title and description\n"
    "- price_min: minimum price\n"
    "- price_max: maximum price\n"
    "- category: filter by category slug\n"
    "- in_stock: true/false\n"
    "- ordering: comma-separated fields, e.g. ordering=-price\n"
)

list_responses = {
    200: openapi.Response(
        description="A paginated list of products",
        schema=ProductSerializer(many=True)
    )
}

retrieve_summary = "Retrieve a product"
retrieve_description = "Return details for a single product by ID."
retrieve_responses = {
    200: ProductSerializer(),
    404: openapi.Response(description="Not Found")
}

create_summary = "Create a new product (admin only)"
create_description = (
    "Create a product. Admin users only.\n\n"
    "Example request body:\n"
    "{\n"
    "  \"title\": \"New Product\",\n"
    "  \"slug\": \"new-product\",\n"
    "  \"category\": \"<category-id>\",\n"
    "  \"price\": \"99.99\",\n"
    "  \"stock\": 10\n"
    "}"
)
create_responses = {
    201: ProductSerializer(),
    400: openapi.Response(description="Validation error"),
    403: openapi.Response(description="Forbidden - admin only")
}


update_summary = "Update a product (admin only)"
update_description = "Update a product. Admins only."
update_responses = {
    200: ProductSerializer(),
    400: openapi.Response(description="Validation error"),
    403: openapi.Response(description="Forbidden - admin only")
}

partial_update_summary = "Partially update a product (admin only)"
partial_update_description = "Partially update a product. Admins only."
partial_update_responses = update_responses

delete_summary = "Delete a product (admin only)"
delete_description = "Permanently delete a product."
delete_responses = {
    204: openapi.Response(description="Deleted"),
    403: openapi.Response(description="Forbidden - admin only"),
    404: openapi.Response(description="Not Found")
}
