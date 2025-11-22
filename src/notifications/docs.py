from drf_yasg import openapi
from .serializers import NotificationSerializer

list_summary = "List notifications"
list_description = (
    "List all notifications for the authenticated user. "
    "Notifications are ordered by newest first and returned as paginated results."
)
list_responses = {200: openapi.Response("List of notifications", schema=NotificationSerializer(many=True))}

mark_read_bulk_summary = "Mark notifications as read (bulk)"
mark_read_bulk_description = (
    "Bulk mark notifications as read. Body: {\"ids\": [\"uuid1\", \"uuid2\"]}. "
    "Only notifications belonging to the current user will be updated."
)
mark_read_bulk_responses = {200: openapi.Response("Count of notifications updated"), 400: "Invalid payload"}

single_mark_read_summary = "Mark a single notification as read"
single_mark_read_description = "Mark the specified notification as read. Only the owner may perform this action."
single_mark_read_responses = {200: openapi.Response("Notification marked as read"), 403: "Forbidden", 404: "Not Found"}
