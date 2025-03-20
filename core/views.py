from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import permissions
from core.models import Book, Loan
from core.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    LoanReadSerializer,
    LoanCreateSerializer,
    LoanReturnSerializer,
)


class BookListViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer

        return BookSerializer


class LoanViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Loan.objects.all().select_related("user", "book")
    serializer_class = LoanReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return LoanReadSerializer
        if self.action == "create":
            return LoanCreateSerializer

        return LoanReadSerializer


class LoanReturnAPIView(
    generics.CreateAPIView,
):
    serializer_class = LoanReturnSerializer
    queryset = Loan.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk=None) -> Response:
        loan = self.get_object()
        serializer = self.get_serializer(
            loan,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
