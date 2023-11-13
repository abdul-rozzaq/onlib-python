


from rest_framework import serializers
from accounts.serializers import UserSerializer


from project.models import (
    Author,
    CardItem,
    Comment,
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
    
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Comment
        fields = '__all__'
    
        
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comments = CommentSerializer(many=True)
    
    class Meta:
        model = Book
        fields = '__all__'


class CardItemSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)
        
    class Meta:
        model = CardItem
        fields = '__all__'

    def create(self, validated_data):
        data = validated_data.copy()
        data['user'] = self.context['request'].user
        return super().create(data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        data = {
            'id': instance.pk,
            'user': instance.user.pk,
            'book': BookSerializer(instance.book, context={'request': self.context['request']}).data
        }
        data['count'] = sum([x.count for x in CardItem.objects.filter(user=instance.user, book=instance.book)])
        
        return data