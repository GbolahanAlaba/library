from rest_framework import serializers
from App_Library.models import *
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'publication_date', 'publisher', 'language', 'category', 'description', 'available_copies']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'created_at']


class BorrowedBookSerializer(serializers.ModelSerializer):
    # return_date = serializers.DateField(format='%Y-%m-%d')
    user = serializers.CharField(source='user.first_name', read_only=True)  # Return user's full name
    book = serializers.CharField(source='book.title', read_only=True)  # Return book title
    borrow_date = serializers.SerializerMethodField()
    return_date = serializers.SerializerMethodField()

    class Meta:
        model = BorrowedBook
        fields = ['borrow_id', 'user', 'book', 'borrow_date', 'return_date']

    
    def get_borrow_date(self, obj):
        # Format borrow_date to date only (ignoring time)
        return obj.borrow_date.date() if isinstance(obj.borrow_date, datetime) else obj.borrow_date

    def get_return_date(self, obj):
        # Format return_date to date only (ignoring time)
        return obj.return_date.date() if isinstance(obj.return_date, datetime) else obj.return_date

class UserBorrowedBooksSerializer(serializers.ModelSerializer):
    borrowed_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'borrowed_books']

    def get_borrowed_books(self, obj):
        borrowed_books = BorrowedBook.objects.filter(user=obj)
        return BorrowedBookSerializer(borrowed_books, many=True).data