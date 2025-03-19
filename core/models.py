from django.db import models
from django.db.models import ForeignKey
from django.conf import settings
from rest_framework.exceptions import ValidationError


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    pages = models.IntegerField()
    available = models.BooleanField(default=True)
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books",
        null=True,
    )

    def __repr__(self):
        return f"{self.title} by {self.author}"

    def __str__(self):
        return f"{self.title} by {self.author}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="loans"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __repr__(self):
        return f"{self.book.title} loaned by {self.user}"
