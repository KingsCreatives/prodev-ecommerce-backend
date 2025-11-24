from drf_yasg import openapi

# --- Parameters ---

product_form_parameters = [
    openapi.Parameter(
        name="title",
        in_=openapi.IN_FORM,
        description="Product title",
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        name="slug",
        in_=openapi.IN_FORM,
        description="URL slug (optional, auto-generated if empty)",
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name="category",
        in_=openapi.IN_FORM,
        description="Category ID or slug",
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name="description",
        in_=openapi.IN_FORM,
        description="Product description",
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name="price",
        in_=openapi.IN_FORM,
        description="Price (decimal)",
        type=openapi.TYPE_NUMBER,
        required=True,
    ),
    openapi.Parameter(
        name="discount_percent",
        in_=openapi.IN_FORM,
        description="Discount percent (0-100)",
        type=openapi.TYPE_NUMBER,
        required=False,
    ),
    openapi.Parameter(
        name="stock",
        in_=openapi.IN_FORM,
        description="Available stock",
        type=openapi.TYPE_INTEGER,
        required=False,
    ),
    openapi.Parameter(
        name="image",
        in_=openapi.IN_FORM,
        description="Primary image file (multipart upload)",
        type=openapi.TYPE_FILE,
        required=False,
    ),
]

# --- Summaries & Descriptions ---

list_summary = "List products"
list_description = (
    "Returns a paginated list of products. Supports search, filtering and ordering.\n\n"
    "**Query parameters:**\n"
    "- `search`: full-text search against title and description\n"
    "- `price_min`: minimum price\n"
    "- `price_max`: maximum price\n"
    "- `category`: filter by category slug\n"
    "- `in_stock`: true/false\n"
    "- `ordering`: comma-separated fields, e.g. `ordering=-price`\n"
)

retrieve_summary = "Retrieve a product"
retrieve_description = "Return details for a single product by ID."

create_summary = "Create a new product (admin only)"
create_description = "Create a product using multipart/form-data. Admin users only."

update_summary = "Update a product (admin only)"
update_description = "Update a product using multipart/form-data. Admins only."

partial_update_summary = "Partially update a product (admin only)"
partial_update_description = "Partially update a product. Admins only."

delete_summary = "Delete a product (admin only)"
delete_description = "Permanently delete a product."


# Reusable schema for responses to ensure consistency
product_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
        'title': openapi.Schema(type=openapi.TYPE_STRING),
        'price': openapi.Schema(type=openapi.TYPE_NUMBER),
        # Add other relevant fields for documentation display purposes
    }
)

list_responses = {
    200: openapi.Response(
        description="A paginated list of products",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                'next': openapi.Schema(type=openapi.TYPE_STRING, format='uri', nullable=True),
                'previous': openapi.Schema(type=openapi.TYPE_STRING, format='uri', nullable=True),
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=product_schema 
                )
            }
        )
    )
}

retrieve_responses = {
    200: openapi.Response(description="Product details", schema=product_schema),
    404: openapi.Response(description="Not Found")
}

create_responses = {
    201: openapi.Response(description="Product created", schema=product_schema),
    400: openapi.Response(description="Validation error"),
    403: openapi.Response(description="Forbidden - admin only")
}

update_responses = {
    200: openapi.Response(description="Product updated", schema=product_schema),
    400: openapi.Response(description="Validation error"),
    403: openapi.Response(description="Forbidden - admin only")
}

partial_update_responses = update_responses

delete_responses = {
    204: openapi.Response(description="Deleted"),
    403: openapi.Response(description="Forbidden - admin only"),
    404: openapi.Response(description="Not Found")
}