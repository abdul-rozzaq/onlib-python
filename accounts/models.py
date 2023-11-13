from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')
    

    def __int__(self) -> int:
        return self.pk