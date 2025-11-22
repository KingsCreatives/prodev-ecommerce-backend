from uuid import uuid4
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from addresses.models import Address

User = get_user_model()


class AddressesAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", username="user", password="password123")
        self.other = User.objects.create_user(email="other@test.com", username="other", password="password123")
        self.admin = User.objects.create_superuser(email="admin@test.com", username="admin", password="password123")

        Address.objects.create(id=uuid4(), user=self.user, full_name="User One", phone_number="123", street="S1", city="C1", country="Country")
        Address.objects.create(id=uuid4(), user=self.other, full_name="Other One", phone_number="321", street="S2", city="C2", country="Country")

    def test_list_addresses_user_only(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/addresses/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for addr in resp.data.get("results", resp.data):
            self.assertIn("full_name", addr)

    def test_user_cannot_see_others_addresses(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/addresses/")
        ids = [a["id"] for a in resp.data.get("results", [])]
        other_addr = Address.objects.filter(user=self.other).first()
        self.assertNotIn(str(other_addr.id), ids)

    def test_admin_can_see_all_addresses(self):
        self.client.force_authenticate(user=self.admin)
        resp = self.client.get("/api/addresses/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [a["id"] for a in resp.data.get("results", [])]
        self.assertTrue(len(ids) >= 2)

    def test_create_address_sets_user(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "full_name": "New Name",
            "phone_number": "999",
            "street": "New St",
            "city": "New City",
            "country": "Nowhere"
        }
        resp = self.client.post("/api/addresses/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data.get("full_name"), "New Name")

    def test_user_cannot_delete_others_address(self):
        other_addr = Address.objects.filter(user=self.other).first()
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(f"/api/addresses/{other_addr.id}/")
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))
