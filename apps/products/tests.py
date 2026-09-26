from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product

User = get_user_model()


class ProductTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Ноутбук', description='Игровой ноутбук', price=Decimal('999.99'), stock=5,
        )
        self.admin = User.objects.create_superuser(username='admin', password='AdminPass123', email='a@a.com')
        self.user = User.objects.create_user(username='user', password='UserPass123')

    def test_anonymous_can_list_products(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_product(self):
        response = self.client.post(reverse('product-list'), {
            'name': 'Мышь', 'price': '19.99', 'stock': 10,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_create_product(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('product-list'), {
            'name': 'Мышь', 'price': '19.99', 'stock': 10,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('product-list'), {
            'name': 'Мышь', 'price': '19.99', 'stock': 10,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_and_delete_product(self):
        self.client.force_authenticate(user=self.admin)
        detail_url = reverse('product-detail', args=[self.product.id])

        response = self.client.patch(detail_url, {'stock': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock'], 3)

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
