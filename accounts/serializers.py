from rest_framework import serializers 
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'groups', 'user_permissions', 'date_joined', 'is_superuser', 'last_login']
    
