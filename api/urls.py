from django.urls import path

from .views import BookListAPIView



urlpatterns = [
    path('book/', BookListAPIView.as_view())
]