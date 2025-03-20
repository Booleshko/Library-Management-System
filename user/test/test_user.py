from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

REGISTER_URL = reverse("user:register")
TOKEN_URL = reverse("token_obtain_pair")


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_register_allow(self):
        payload = {
            "email": "test123@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "test123",
        }
        response = self.client.post(REGISTER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_obtain_token(self):
        User.objects.create_user(
            email="test123@gmail.com",
            first_name="John",
            last_name="Doe",
            password="test123",
        )
        payload = {
            "email": "test123@gmail.com",
            "password": "test123",
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
