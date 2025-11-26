from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountTests(APITestCase):

    def setUp(self):
        try:
            self.register_url = reverse('register')
            self.me_url = reverse('me')
        except:
            self.register_url = '/api/auth/register/'
            self.me_url = '/api/auth/me/'

        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testShatta@2025'
        }

    def test_registration_success(self):
        """
        Ensure we can create a new user object.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_registration_auto_username(self):
        """
        Ensure the username is auto-generated from email if not provided.
        """
        data_no_username = {
            'email': 'autogen@example.com',
            'password': 'Shatta@2025'
        }
        response = self.client.post(self.register_url, data_no_username, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='autogen@example.com')
        self.assertEqual(user.username, 'autogen')

    def test_registration_missing_password(self):
        """
        Ensure registration fails without a password.
        """
        data = {'email': 'fail@example.com'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_view_authenticated(self):
        """
        Ensure authenticated user can see their own profile.
        """
        user = User.objects.create_user(**self.user_data)
        
        self.client.force_authenticate(user=user)
        
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)

    def test_me_view_unauthenticated(self):
        """
        Ensure unauthenticated user cannot access profile.
        """
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)