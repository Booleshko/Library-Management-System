from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .config import payload, sample_book


BASE_URL = reverse('core:book-list')


class TestAuthenticatedAdminUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="test@test.com",
            password="test1234",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.admin)


    def test_admin_allow_list_books(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_admin_allow_create_book(self):
        response = self.client.post(BASE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_admin_allow_delete_book(self):
        book = sample_book()
        url = reverse("core:book-detail", args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
