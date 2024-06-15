from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model, get_user

User = get_user_model()


class TokenAuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            phone='+999888777666',
            first_name='test'
        )

    def test_token_get(self):
        url = '/auth/token/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)

    def test_authenticated_request(self):

        url = '/auth/token/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['auth_token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        url = '/auth/users/me/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        login_url = '/auth/token/login/'
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['auth_token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        me_url = '/auth/users/me/'
        me_response = self.client.get(me_url)
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)

        logout_url = '/auth/token/logout/'
        logout_response = self.client.post(logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

        me_response_after_logout = self.client.get(me_url)
        self.assertEqual(me_response_after_logout.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_credentials(self):
        url = '/auth/token/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertNotIn('auth_token', response.data)
