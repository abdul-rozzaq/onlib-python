from django.contrib import admin

from .models import (
    Author,
    Genre,
    Book
)

class BookAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Book._meta.fields if x.name not in ['id', 'image']] + ['image']
    list_editable = ['rate', ]
    list_filter = ['author', 'genres']
    

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)