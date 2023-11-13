from django.shortcuts import render

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework import status

from project.models import *

from .serializers import BookSerializer, CardItemSerializer
   

   
class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = BookSerializer
    
 
class CardItemViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = CardItem.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = CardItemSerializer
        
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        book = serializer.validated_data.get('book')
        user = request.user
        _status = status.HTTP_201_CREATED
        
        queryset = self.queryset.filter(book=book, user=user)
        
        if queryset.exists():
            item = queryset.first()
            item.count += serializer.validated_data.get('count')            
            item.save()
            
            serializer = self.get_serializer(item)
            _status = status.HTTP_200_OK
        else:
            self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=_status, headers=headers)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def wish(request):
    
    user = request.user
    
    book = Book.objects.get(pk=request.data['book'])
        
    
    if user not in book.wishes.all():
        book.wishes.add(user)
    else:
        book.wishes.remove(user)
    
    return Response(status=200)
    
