from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('user-register')
        data = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'StrongPass123',
            'password2': 'StrongPass123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='alice').exists())

    def test_register_password_mismatch(self):
        url = reverse('user-register')
        data = {
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'StrongPass123',
            'password2': 'DifferentPass123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_and_profile(self):
        User.objects.create_user(username='carl', password='StrongPass123')

        login_url = reverse('token_obtain_pair')
        response = self.client.post(login_url, {'username': 'carl', 'password': 'StrongPass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data['access']

        profile_url = reverse('user-profile')
        response = self.client.get(profile_url, HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'carl')

    def test_top_up_balance(self):
        user = User.objects.create_user(username='dave', password='StrongPass123')
        self.client.force_authenticate(user=user)

        url = reverse('user-top-up')
        response = self.client.post(url, {'amount': '100.00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.balance, Decimal('100.00'))
