from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model, get_user

User = get_user_model()


class SessionAuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            phone='+999888777666',
            first_name='test'
        )

    def test_login(self):
        url = '/api/account/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.login(email='testuser@example.com', password='testpassword123')
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        self.client.login(email='testuser@example.com', password='testpassword123')

        url = '/api/account/logout/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('_auth_user_id', self.client.session)
