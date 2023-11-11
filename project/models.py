from django.db import models
from accounts.models import User


class Author(models.Model):
    fullname = models.CharField(max_length=256)
    
    def __str__(self) -> str:
        return self.fullname


class Genre(models.Model):
    title = models.CharField(max_length=256)
    
    def __str__(self) -> str:
        return self.title



class Book(models.Model):
    image = models.ImageField(upload_to='book-images')
    
    title = models.CharField(max_length=256)
    description = models.TextField(default='description')
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre, blank=False, related_name='books')
    
    price = models.IntegerField()
    rate = models.FloatField(default=3.5)
    
    wishes = models.ManyToManyField(User, blank=True)