from django.urls import path, include
from rest_framework import routers

from .views import BookListViewSet, LoanViewSet, LoanReturnAPIView

router = routers.DefaultRouter()
router.register("books", BookListViewSet)
router.register("loans", LoanViewSet)
app_name = "core"

urlpatterns = [
    path("", include(router.urls)),
    path("loan/<int:pk>/return/", LoanReturnAPIView.as_view(), name="return"),
]
