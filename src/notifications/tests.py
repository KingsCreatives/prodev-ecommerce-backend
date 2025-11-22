from uuid import uuid4
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from notifications.models import Notification

User = get_user_model()


class NotificationsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", username="user", password="password123")
        self.other = User.objects.create_user(email="other@test.com", username="other", password="password123")

        Notification.objects.create(id=uuid4(), user=self.user, notif_type="order", title="Order placed", message="Order #1")
        Notification.objects.create(id=uuid4(), user=self.user, notif_type="system", title="Welcome", message="Welcome msg")
        Notification.objects.create(id=uuid4(), user=self.other, notif_type="product", title="Sale", message="Sale msg")

    def test_list_user_notifications(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/notifications/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [n["id"] for n in resp.data.get("results", [])]
        self.assertTrue(len(ids) >= 2)

    def test_mark_read_single(self):
        self.client.force_authenticate(user=self.user)
        notif = Notification.objects.filter(user=self.user).first()
        resp = self.client.post(f"/api/notifications/{notif.id}/mark-read-single/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_mark_read_bulk(self):
        self.client.force_authenticate(user=self.user)
        notifs = Notification.objects.filter(user=self.user).values_list("id", flat=True)
        resp = self.client.post("/api/notifications/mark-read/", {"ids": list(notifs)}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("updated", None), len(list(notifs)))
