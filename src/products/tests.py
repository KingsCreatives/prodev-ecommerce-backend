from uuid import uuid4
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from products.models import Product

User = get_user_model()


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            username="user",
            password="StrongPassword123!"
        )

        self.admin = User.objects.create_superuser(
            email="admin@test.com",
            username="admin",
            password="StrongPassword123!"
        )

        self.cat_electronics = Category.objects.create(
            id=uuid4(), name="Electronics", slug="electronics"
        )

        self.cat_fashion = Category.objects.create(
            id=uuid4(), name="Fashion", slug="fashion"
        )

        Product.objects.create(
            id=uuid4(),
            title="MacBook Pro 14",
            slug="macbook-pro-14",
            category=self.cat_electronics,
            description="Apple M1 Pro laptop",
            price=2200.00,
            discount_percent=10,
            stock=15,
        )

        Product.objects.create(
            id=uuid4(),
            title="Dell XPS 13",
            slug="dell-xps-13",
            category=self.cat_electronics,
            description="Ultrabook with Intel CPU",
            price=1500.00,
            discount_percent=5,
            stock=22,
        )

        Product.objects.create(
            id=uuid4(),
            title="Men's Sneakers",
            slug="mens-sneakers",
            category=self.cat_fashion,
            description="Comfort running shoes",
            price=120.00,
            discount_percent=15,
            stock=50,
        )
        
        Product.objects.create(
            id=uuid4(),
            title="Budget Laptop",
            slug="budget-laptop",
            category=self.cat_electronics,
            description="Cheap laptop",
            price=300.00,
            discount_percent=0,
            stock=0,
        )

        self.list_url = "/api/products/"

    def test_list_products_paginated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIsInstance(response.data["results"], list)

    def test_search_title_matches(self):
        response = self.client.get(self.list_url, {"search": "MacBook"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [p["title"] for p in response.data["results"]]
        self.assertTrue(any("MacBook" in t for t in titles))

    def test_filter_by_price_range(self):
        response = self.client.get(self.list_url, {"price_min": "1000", "price_max": "2000"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(p["price"]) for p in response.data["results"]]
       
        for price in prices:
            self.assertGreaterEqual(price, 1000.0)
            self.assertLessEqual(price, 2000.0)

    def test_filter_by_category_slug(self):
        response = self.client.get(self.list_url, {"category": "electronics"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for p in response.data["results"]:
            self.assertIn("category", p)

    def test_in_stock_filter(self):
        response = self.client.get(self.list_url, {"in_stock": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for p in response.data["results"]:
            self.assertGreater(int(p.get("stock", 0)), 0)

    def test_ordering_by_price_desc(self):
        response = self.client.get(self.list_url, {"ordering": "-price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(p["price"]) for p in response.data["results"]]
        sorted_prices = sorted(prices, reverse=True)
        self.assertEqual(prices, sorted_prices)

    def test_non_admin_cannot_create_product(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Product",
            "slug": "new-product",
            "category": str(self.cat_electronics.id),
            "price": "99.99",
            "stock": 10
        }
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertIn(response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "title": "Admin Product",
            "slug": "admin-product",
            "category": str(self.cat_electronics.id),
            "price": "199.99",
            "stock": 5
        }
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Admin Product")

    def test_soft_delete(self):
        self.client.force_authenticate(user=self.admin)
        product = Product.objects.first()
        url = f"{self.list_url}{product.id}/"
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        product.refresh_from_db()
        self.assertTrue(product.is_deleted)
        
        resp = self.client.get(self.list_url)
        ids = [r["id"] for r in resp.data["results"]]
        self.assertNotIn(str(product.id), ids)