from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .config import payload, sample_book


BASE_URL = reverse("core:book-list")


class TestUnAuthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user_allow_list_books(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_forbid_create_book(self):
        response = self.client.post(BASE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test1234"
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_allow_list_books(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_forbid_create_book(self):
        response = self.client.post(BASE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_retrieve_book(self):
        book = sample_book()
        url = reverse("core:book-detail", args=[book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
