from drf_yasg import openapi
from .serializers import CategorySerializer

list_summary = "List all categories"
list_description = (
    "Returns a list of all product categories.\n\n"
    "Accessible to all users (no authentication required)."
)

list_responses = {
    200: CategorySerializer(many=True),
}

retrieve_summary = "Retrieve a single category"
retrieve_description = (
    "Returns detailed information for a specific category, given its ID.\n\n"
    "Accessible to all users (no authentication required)."
)

retrieve_responses = {
    200: CategorySerializer(),
    404: openapi.Response(description="Category not found"),
}

create_summary = "Create a new category (admin only)"
create_description = (
    "Creates a new product category.\n\n"
    "Only admin users can perform this action.\n\n"
    "Example request body:\n"
    "{\n"
    "  \"name\": \"Electronics\",\n"
    "  \"slug\": \"electronics\",\n"
    "  \"description\": \"Devices, gadgets, and appliances\"\n"
    "}"
)

create_responses = {
    201: CategorySerializer(),
    400: openapi.Response(description="Validation error"),
    403: openapi.Response(description="Forbidden – Admins only"),
}

update_summary = "Update an existing category (admin only)"
update_description = (
    "Updates all fields of a category.\n\n"
    "Only admin users are allowed."
)

update_responses = {
    200: CategorySerializer(),
    400: openapi.Response(description="Validation error"),
    403: openapi.Response(description="Forbidden – Admins only"),
}

partial_update_summary = "Partially update a category (admin only)"
partial_update_description = (
    "Updates one or more fields of the category.\n\n"
    "Only admin users allowed."
)

partial_update_responses = {
    200: CategorySerializer(),
    403: openapi.Response(description="Forbidden – Admins only"),
}

delete_summary = "Delete a category (admin only)"
delete_description = (
    "Deletes a category permanently.\n\n"
    "Only admin users may perform this action."
)

delete_responses = {
    204: openapi.Response(description="Category deleted"),
    403: openapi.Response(description="Forbidden – Admins only"),
    404: openapi.Response(description="Category not found"),
}
