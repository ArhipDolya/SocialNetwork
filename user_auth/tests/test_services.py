from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIClient

from ..services_auth import AuthService


class RegisterUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_success(self):
        # Test data for successful registration
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        # Simulate a registration request
        response = AuthService.register_user(data)

        self.assertEqual(response, ({'message': 'User registered successfully'}, 201))

    def test_register_user_failure(self):
        # Test data for a registration failure
        data = {
            'username': 'testuser',
            'email': 'test',
            'password': 'testpassword'
        }

        response = AuthService.register_user(data)

        # Assert the expected response
        self.assertEqual(response[1], 400)
        self.assertIn('email', response[0])
        self.assertEqual(response[0]['email'][0].code, 'invalid')


class LoginUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_login_user_success(self):
        # Test data for successful login
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        # Simulate a login request
        response = AuthService.login_user(data['email'], data['password'])

        # Assert the expected response
        self.assertEqual(response[1], 200)
        self.assertIn('access_token', response[0])
        self.assertIn('refresh_token', response[0])

    def test_login_user_failure_incorrect_password(self):
        # Test data for a login failure (incorrect password)
        data = {
            'email': 'test@example.com',
            'password': 'incorrectpassword'
        }

        # Simulate a login request that should fail (incorrect password)
        with self.assertRaises(AuthenticationFailed) as context:
            AuthService.login_user(data['email'], data['password'])

        # Assert the expected response
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, 'Incorrect password!')