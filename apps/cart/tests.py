from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Product

User = get_user_model()


class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='UserPass123')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Клавиатура', price=Decimal('49.99'), stock=10)

    def test_add_item_to_cart(self):
        response = self.client.post(reverse('cart-item-list'), {
            'product_id': self.product.id, 'quantity': 2,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 2)

    def test_view_cart(self):
        self.client.post(reverse('cart-item-list'), {'product_id': self.product.id, 'quantity': 3})
        response = self.client.get(reverse('cart-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(Decimal(response.data['total_price']), Decimal('149.97'))

    def test_update_item_quantity(self):
        add_response = self.client.post(reverse('cart-item-list'), {'product_id': self.product.id, 'quantity': 1})
        item_id = add_response.data['id']
        response = self.client.patch(reverse('cart-item-detail', args=[item_id]), {'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 5)

    def test_remove_item(self):
        add_response = self.client.post(reverse('cart-item-list'), {'product_id': self.product.id, 'quantity': 1})
        item_id = add_response.data['id']
        response = self.client.delete(reverse('cart-item-detail', args=[item_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
