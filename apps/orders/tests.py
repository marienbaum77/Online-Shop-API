from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cart.services import CartService
from apps.products.models import Product

User = get_user_model()


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='UserPass123', balance=Decimal('1000.00'))
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Наушники', price=Decimal('100.00'), stock=3)

    def test_create_order_success(self):
        CartService(self.user).add_item(self.product.id, quantity=2)

        response = self.client.post(reverse('order-create'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], '200.00')

        self.product.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(self.user.balance, Decimal('800.00'))

        cart_response = self.client.get(reverse('cart-detail'))
        self.assertEqual(len(cart_response.data['items']), 0)

    def test_create_order_empty_cart(self):
        response = self.client.post(reverse('order-create'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_insufficient_stock(self):
        CartService(self.user).add_item(self.product.id, quantity=10)
        response = self.client.post(reverse('order-create'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_insufficient_balance(self):
        self.user.balance = Decimal('50.00')
        self.user.save()
        CartService(self.user).add_item(self.product.id, quantity=1)
        response = self.client.post(reverse('order-create'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
