from drf_yasg import openapi
from .serializers import AddressSerializer

list_summary = "List addresses"
list_description = "Return addresses for the authenticated user. Admins can list all addresses."
list_responses = {200: openapi.Response("A list of addresses", AddressSerializer(many=True))}

retrieve_summary = "Retrieve address"
retrieve_description = "Return a single address. Only the owner or admin can access."
retrieve_responses = {200: AddressSerializer(), 404: openapi.Response("Not found")}

create_summary = "Create address"
create_description = "Create an address for the authenticated user. User will be set server-side."
create_responses = {201: AddressSerializer(), 400: openapi.Response("Validation error")}

update_summary = "Update address"
update_description = "Update an address. Only the owner or admin may update."
update_responses = {200: AddressSerializer(), 403: openapi.Response("Forbidden")}

delete_summary = "Delete address"
delete_description = "Delete an address. Only the owner or admin may delete."
delete_responses = {204: openapi.Response("Deleted"), 403: openapi.Response("Forbidden")}
