from django.urls import path
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        url = '/auth/users/'
        data = {
            'email': 'testuser@example.com',
            'phone': '+999777888999',
            'password': 'testpassword123',
            'first_name': 'Test',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data['email']).exists())
