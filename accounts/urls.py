from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('get-me/', get_me),
]