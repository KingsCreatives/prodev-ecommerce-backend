from uuid import uuid4
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from addresses.models import Address

User = get_user_model()

class AddressesAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", username="user", password="StrongPassword123!")
        self.other = User.objects.create_user(email="other@test.com", username="other", password="StrongPassword123!")
        self.admin = User.objects.create_superuser(email="admin@test.com", username="admin", password="StrongPassword123!")

        self.addr1 = Address.objects.create(id=uuid4(), user=self.user, full_name="User One", phone_number="123", street="S1", city="C1", country="Country", is_default=True)
        self.addr2 = Address.objects.create(id=uuid4(), user=self.other, full_name="Other One", phone_number="321", street="S2", city="C2", country="Country")

    def test_list_addresses_user_only(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/addresses/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data.get("results", resp.data)), 1)

    def test_user_cannot_see_others_addresses(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/addresses/")
        ids = [a["id"] for a in resp.data.get("results", [])]
        self.assertNotIn(str(self.addr2.id), ids)

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
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(f"/api/addresses/{self.addr2.id}/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_setting_new_default_unchecks_old(self):
        """Test that creating a NEW default address sets the old one to False"""
        self.client.force_authenticate(user=self.user)
        self.assertTrue(Address.objects.get(id=self.addr1.id).is_default)

        payload = {
            "full_name": "New Default",
            "phone_number": "999",
            "street": "New St",
            "city": "New City",
            "country": "Nowhere",
            "is_default": True
        }
        self.client.post("/api/addresses/", payload, format="json")

        self.addr1.refresh_from_db()
        self.assertFalse(self.addr1.is_default)
        self.assertEqual(Address.objects.filter(user=self.user, is_default=True).count(), 1)