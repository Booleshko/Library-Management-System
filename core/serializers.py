from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Book, Loan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "pages", "available"]


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "pages"]


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = BookListSerializer.Meta.fields + ["available"]


class LoanReadSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)
    user = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Loan
        fields = ("id", "user", "book", "return_date", "is_active")
        read_only_fields = ("is_active", "return_date")


class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["book", "user"]

    def validate(self, data):
        book = data.get("book")
        user = data.get("user")

        existing_loan = Loan.objects.filter(
            book=book, user=user, return_date__isnull=True
        ).exists()

        if existing_loan:
            raise ValidationError(
                "This book is already loaned to the user and has not been returned."
            )

        return data


class LoanReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ("id", "is_active")

    def validate(self, attrs):
        data = super(LoanReturnSerializer, self).validate(attrs)
        loan = self.instance

        if loan.return_date:
            raise ValidationError(f"Loan {loan.id} already returned")
        return data

    def update(self, instance, validated_data):
        instance.return_date = datetime.today().date()

        instance.book.available = True
        instance.book.save()
        instance.is_active = False
        instance.save()
        return instance
