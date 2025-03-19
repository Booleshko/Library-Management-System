from rest_framework import viewsets, status
from rest_framework.response import Response

from core.models import Book, Loan
from core.serializers import BookSerializer, BookListSerializer, BookDetailSerializer, LoanSerializer


class BookListViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        if self.action == 'retrieve':
            return BookDetailSerializer

        return BookSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        return serializer.save()
