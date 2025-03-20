from datetime import datetime

from core.models import Book, Loan

payload =  {
            "title": "Sample book",
            "author": "Sample author",
            "isbn": "234342411",
            "pages": 100,
            "available": True,
        }

def sample_book(**params):
    defaults = {
        "title": "Sample book",
        "author": "Sample author",
        "isbn": "234342411",
        "pages": 100,
        "available": True,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)

def sample_loan(**params):
    defaults = {
        "book": sample_book(**payload),
        "created_at": datetime.now(),
        "is_active": True,
    }

    defaults.update(params)
    return Loan.objects.create(**defaults)
