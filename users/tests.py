from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
from django.contrib.auth.models import User  # Import the User model
from .models import UserProfile

class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        # Create user first
        User.objects.create_user(**self.user_data)
        
        # Attempt login
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_profile_update(self):
        # Create and authenticate user
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        
        # Update profile
        profile_data = {
            'profile': {
                'bio': 'Test bio',
                'location': 'Test location'
            }
        }
        response = self.client.patch(self.profile_url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.profile.bio, 'Test bio')

