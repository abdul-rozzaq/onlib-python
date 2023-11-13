from django.urls import path

from .views import (
    BookViewSet, 
    CardItemViewSet,
    wish,
)

from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'book', BookViewSet)
router.register(r'card', CardItemViewSet)

urlpatterns = [
    path('wish/', wish),
]
urlpatterns += router.urls