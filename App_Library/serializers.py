from rest_framework import serializers
from App_Library.models import *


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'publication_date', 'publisher', 'language', 'category', 'description', 'available_copies']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'created_at']


class BorrowedBookSerializer(serializers.ModelSerializer):
    return_date = serializers.DateField(format='%Y-%m-%d')
    
    class Meta:
        model = BorrowedBook
        fields = ['borrow_id', 'user', 'book', 'borrow_date', 'return_date']