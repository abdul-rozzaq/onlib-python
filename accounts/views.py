from django.shortcuts import render
from django.core import validators 
from django.core.exceptions import ValidationError

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, get_authorization_header

from accounts.serializers import UserSerializer

from .models import User



@api_view(['POST'])
def signup(request):
    
    data = request.data
    
    serializer = UserSerializer(data=data, context={'request': request})
        
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    
    return Response(serializer.errors, status=400)
    


@api_view(['POST'])
def login(request):
    key, password, user = request.data['key'], request.data['password'], None
    
    if validate_email(key):
        user = User.objects.get(email=key)
    else:
        user = User.objects.get(username=key)
        
           
    if user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key, 'user': UserSerializer(user, context={'request': request}).data})
    
    return Response(status=404)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def logout(request):
    _, token = get_authorization_header(request).split()
    
    Token.objects.get(key=token).delete()

    return Response(status=200)


def validate_email(email: str) -> bool:
    try:
        validators.validate_email(email)
        return True
    except ValidationError:
        return False
