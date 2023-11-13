from django.contrib import admin

from .models import (
    Author,
    Genre,
    Book,
    Comment,
    CardItem
)

class BookAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Book._meta.fields if x.name not in ['id', 'image']] + ['image']
    list_editable = ['rate', ]
    list_filter = ['author', 'genres']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Comment._meta.fields if x.name not in ['id']]

class CardItemAdmin(admin.ModelAdmin):
    list_display = [x.name for x in CardItem._meta.fields if x.name not in ['id']]

admin.site.register(Author)
admin.site.register(CardItem, CardItemAdmin)
admin.site.register(Genre)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Book, BookAdmin)