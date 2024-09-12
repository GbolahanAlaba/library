from rest_framework import serializers
from App_Library.models import *


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'publication_date', 'publisher', 'language', 'category', 'description']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']