from uuid import uuid4
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from products.models import Product
from carts.models import Cart, CartItem

User = get_user_model()


class CartAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", username="user", password="password123")
        self.other = User.objects.create_user(email="other@test.com", username="other", password="password123")
        self.admin = User.objects.create_superuser(email="admin@test.com", username="admin", password="password123")

        self.cat = Category.objects.create(id=uuid4(), name="Electronics", slug="electronics")
        self.p1 = Product.objects.create(id=uuid4(), title="Prod A", slug="prod-a", category=self.cat, price=50, stock=10)
        self.p2 = Product.objects.create(id=uuid4(), title="Prod B", slug="prod-b", category=self.cat, price=30, stock=2)

        self.list_url = "/api/carts/"

    def test_cart_auto_created_and_item_added(self):
        self.client.force_authenticate(user=self.user)
        data = {"product_id": str(self.p1.id), "quantity": 2}
        resp = self.client.post("/api/cart-items/", data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        cart = Cart.objects.get(user=self.user)
        self.assertTrue(cart.items.exists())
        item = cart.items.first()
        self.assertEqual(item.quantity, 2)

    def test_adding_duplicate_increments_quantity(self):
        self.client.force_authenticate(user=self.user)
        data = {"product_id": str(self.p1.id), "quantity": 1}
        resp1 = self.client.post("/api/cart-items/", data, format="json")
        self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)
        resp2 = self.client.post("/api/cart-items/", data, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        cart = Cart.objects.get(user=self.user)
        item = cart.items.get(product=self.p1)
        self.assertEqual(item.quantity, 2)

    def test_user_cannot_access_other_users_cart_items(self):
        
        other_cart = Cart.objects.create(user=self.other)
        CartItem.objects.create(cart=other_cart, product=self.p2, quantity=1)
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/cart-items/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        for it in resp.data.get("results", resp.data):
            if isinstance(it, dict):
                self.assertNotEqual(it.get("product", {}).get("id"), str(self.p2.id))
