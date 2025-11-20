from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from categories.models import Category

User = get_user_model()


class CategoryAPITestCase(APITestCase):

    def setUp(self):
        # Create normal user
        self.user = User.objects.create_user(
            email="user@test.com",
            username="user",
            password="password123"
        )

        # Create admin user
        self.admin = User.objects.create_superuser(
            email="admin@test.com",
            username="admin",
            password="password123"
        )

        # URLs
        self.list_url = "/api/categories/"
       
        # Create sample category
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )

    def test_list_categories_public(self):
        """
        Anyone should be able to list categories.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_non_admin_cannot_create_category(self):
        """
        Regular users should NOT be able to create categories.
        """
        # self.client.login(email="user@test.com", password="password123") ---- Will have to use session based auth in future
        self.client.force_authenticate(user=self.user)
        data = {"name": "Shoes", "slug": "shoes"}

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_category(self):
        """
        Admin users CAN create categories.
        """
        # self.client.login(email="admin@test.com", password="password123")
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Laptops", "slug": "laptops"}

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Laptops")

    def test_admin_can_update_category(self):
        """
        Admin should be able to update a category.
        """
        # self.client.login(email="admin@test.com", password="password123")
        self.client.force_authenticate(user=self.admin)

        url = f"/api/categories/{self.category.id}/"
        data = {"name": "Updated Electronics", "slug": "updated-electronics"}

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Electronics")

    def test_admin_can_delete_category(self):
        """
        Admin should be able to delete a category.
        """
        # self.client.login(email="admin@test.com", password="password123")
        self.client.force_authenticate(user=self.admin)

        url = f"/api/categories/{self.category.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
