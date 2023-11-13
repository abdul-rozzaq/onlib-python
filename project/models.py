from django.db import models
from accounts.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    
    count = models.IntegerField(default=1)
    
    wishes = models.ManyToManyField(User, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs) -> None:       
        if self.pk is None:
            self.notify()
            
        super().save(*args, **kwargs)
        
        
    
        
    def notify(self) -> None:
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(
            "public_room",
            {
                "type": "send_notification",
                "message": {
                    "message": "NEW_BOOK",
                    "author": f"{self.author.fullname}"
                },
            },
        )

        
        
    
   
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.comment


class CardItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    count = models.IntegerField(default=1)
    
    
    def __str__(self) -> str:
        return self.user.username
    
