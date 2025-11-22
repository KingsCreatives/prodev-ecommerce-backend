from uuid import uuid4
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from products.models import Product
from orders.models import Order, OrderItem

User = get_user_model()


class OrdersAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", username="user", password="password123")
        self.other = User.objects.create_user(email="other@test.com", username="other", password="password123")
        self.admin = User.objects.create_superuser(email="admin@test.com", username="admin", password="password123")

        self.cat = Category.objects.create(id=uuid4(), name="Electronics", slug="electronics")
        self.p1 = Product.objects.create(id=uuid4(), title="Prod A", slug="prod-a", category=self.cat, price=100, stock=10)
        self.p2 = Product.objects.create(id=uuid4(), title="Prod B", slug="prod-b", category=self.cat, price=200, stock=5)

        self.order1 = Order.objects.create(id=uuid4(), user=self.user)
        self.order2 = Order.objects.create(id=uuid4(), user=self.other)

        OrderItem.objects.create(order=self.order1, product=self.p1, quantity=1, unit_price=self.p1.price)
        OrderItem.objects.create(order=self.order2, product=self.p2, quantity=2, unit_price=self.p2.price)

    def test_user_sees_own_orders_only(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/orders/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [o["id"] for o in resp.data.get("results", [])]
        self.assertIn(str(self.order1.id), ids)
        self.assertNotIn(str(self.order2.id), ids)

    def test_admin_sees_all_orders(self):
        self.client.force_authenticate(user=self.admin)
        resp = self.client.get("/api/orders/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [o["id"] for o in resp.data.get("results", [])]
        self.assertIn(str(self.order1.id), ids)
        self.assertIn(str(self.order2.id), ids)

    def test_add_order_item_snapshots_price_and_updates_total(self):
        self.client.force_authenticate(user=self.user)

        order = Order.objects.create(user=self.user)
        data = {"order_id": str(order.id), "product_id": str(self.p1.id), "quantity": 2}
        resp = self.client.post("/api/order-items/", data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        order.refresh_from_db()
        self.assertGreater(order.total_amount, 0)

    def test_cannot_add_item_to_another_users_order(self):
        self.client.force_authenticate(user=self.user)
        data = {"order_id": str(self.order2.id), "product_id": str(self.p1.id), "quantity": 1}
        resp = self.client.post("/api/order-items/", data, format="json")
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST))
