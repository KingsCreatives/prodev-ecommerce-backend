from drf_yasg import openapi

register_summary = "Register a new user"

register_description = (
    "Creates a new user account.\n\n"
    "Example request body:\n"
    "{\n"
    "  \"email\": \"user@example.com\",\n"
    "  \"username\": \"myusername\",\n"
    "  \"password\": \"strongpassword123\"\n"
    "}\n\n"
    "A successful registration returns a confirmation message."
)

register_responses = {
    201: openapi.Response(
        description="User created successfully",
        examples={
            "application/json": {"message": "User created successfully."}
        },
    ),
    400: openapi.Response(description="Validation error"),
}



me_summary = "Get current authenticated user"

me_description = (
    "Returns the profile information of the authenticated user.\n\n"
    "Requires a valid JWT access token.\n\n"
    "Example response:\n"
    "{\n"
    "  \"id\": \"uuid\",\n"
    "  \"email\": \"user@example.com\",\n"
    "  \"username\": \"myusername\"\n"
    "}"
)

me_parameters = [
    openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description="JWT access token: Bearer <token>",
        type=openapi.TYPE_STRING,
        required=True,
    )
]

me_responses = {
    200: openapi.Response(
        description="Authenticated user profile",
        examples={
            "application/json": {
                "id": "uuid",
                "email": "user@example.com",
                "username": "myusername",
            }
        },
    ),
    401: openapi.Response(description="Unauthorized"),
}
