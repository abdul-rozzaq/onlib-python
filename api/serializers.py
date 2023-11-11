


from rest_framework import serializers


from project.models import (
    Author,
    Genre,
    Book
)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
    
        
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    # genres = GenreSerializer(many=True)
    
    class Meta:
        model = Book
        fields = '__all__'

