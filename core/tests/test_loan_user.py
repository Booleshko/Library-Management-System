from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Loan
from core.serializers import LoanReturnSerializer
from core.tests.config import sample_book, sample_loan
import io
from rest_framework.parsers import JSONParser

BASE_URL = reverse('core:loan-list')


class TestUnAuthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user_forbid_list_loans(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestAuthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test123',
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_allow_list_loans(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_allow_retrieve_loan(self):
        loan = sample_loan(user=self.user)
        url = reverse('core:loan-detail', args=[loan.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_allow_create_loan(self):

        payload = {
            "book": sample_book().id,
            "created_at": datetime.now(),
            "is_active": True,
            "user": self.user.id,
        }

        response = self.client.post(BASE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_allow_return_loan(self):
        loan = sample_loan(user=self.user)
        loans = Loan.objects.all()
        serializer = LoanReturnSerializer(loans, many=True)

        payload = {
            "id": loan.id,
            "return_date": datetime.now(),
        }

        url = reverse("core:return", args=[loan.id])
        response = self.client.post(url, payload)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data[0], data)
