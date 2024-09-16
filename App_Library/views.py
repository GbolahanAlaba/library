from django.http import JsonResponse
from django.shortcuts import render
from .models import Book
from . serializers import *
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from functools import wraps
from rest_framework.views import exception_handler
from rest_framework import filters
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from rest_framework.decorators import action
# from .utils import get_object_or_404_customized


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            response = exception_handler(e, context=None)
            if response is None:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return response
    return wrapper

       
class LibraryViewSets(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    book_serializer_class = BookSerializer
    user_serializer_class = UserSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['author', 'category']

    @handle_exceptions
    def enroll_user(self, request, *args, **kwargs):
        serializer = self.user_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success", "message": "User enrolled", "data": serializer.data}, status=status.HTTP_201_CREATED)
    

    @handle_exceptions
    def books(self, request, *args, **kwargs):
        books = Book.objects.all().order_by("-created_at")

        serializer = self.book_serializer_class(books, many=True)
        return Response({"status": "success", "message": "All Books", "data": serializer.data}, status=status.HTTP_200_OK)


    @handle_exceptions
    def view_book(self, request, book_id, *args, **kwargs):
        book = Book.objects.filter(book_id=book_id).first()

        if not book:
            return Response({"status": "failed", "message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.book_serializer_class(book)
            return Response({"status": "success", "message": f"{book.title}", "data": serializer.data}, status=status.HTTP_200_OK)
    

    # @action(detail=False, methods=['get'], url_path='filter-books')
    @handle_exceptions
    def filter_books(self, request, *args, **kwargs):
        author = request.query_params.get('author', None)
        category = request.query_params.get('category', None)


        if author:
            queryset = self.queryset.filter(author__icontains=author)
        if category:
            queryset = self.queryset.filter(category__icontains=category)

        serializer = BookSerializer(self.queryset, many=True)
        return Response(
            {"status": "success", "message": "Filtered books", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    

    @handle_exceptions
    def borrow_book(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        borrow_duration = request.data.get('borrow_duration')

        if not user_id or not book_id or not borrow_duration:
            return Response({"status": "failed", "message": "Please provide user_id, book_id, and borrow_duration."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"status": "failed", "message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            book = Book.objects.get(book_id=book_id, available_copies__gt=0)
        except Book.DoesNotExist:
            return Response({"status": "failed", "message": "Book not available or out of stock."}, status=status.HTTP_404_NOT_FOUND)

        borrow_days = int(borrow_duration)
        return_date = date.today() + timedelta(days=borrow_days)
        borrowed_book = BorrowedBook.objects.create(user=user, book=book, return_date=return_date)
        book.available_copies -= 1
        book.save()

        serializer = BorrowedBookSerializer(borrowed_book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @handle_exceptions
    def add_new_book(self, request, *args, **kwargs):
        serializer = self.book_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success", "message": "Book added", "data": serializer.data}, status=status.HTTP_201_CREATED)
    

    @handle_exceptions
    def remove_book(self, request, book_id, *args, **kwargs):
        book = Book.objects.filter(book_id=book_id).first()

        if not book:
            return Response({"status": "failed", "message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            book.delete()
            return Response({"status": "success", "message": f"{book.title} book removed from catalogue"}, status=status.HTTP_201_CREATED)


    @handle_exceptions
    def users(self, request, *args, **kwargs):
        users = User.objects.all().order_by("-created_at")

        serializer = self.user_serializer_class(users, many=True)
        return Response({"status": "success", "message": "All library users", "data": serializer.data}, status=status.HTTP_201_CREATED)
    

    def borrowed_books(self, request):
        queryset = User.objects.all()
        serializer = UserBorrowedBooksSerializer(queryset, many=True)
        return Response({"status": "success", "message": "Borrowed books and users", "data": serializer.data}, status=status.HTTP_200_OK)


    @handle_exceptions
    def unavailable_books(self, request, *args, **kwargs):
        unavailable_books = Book.objects.filter(available_copies=0)

        unavailable_books_with_return_date = []
        for book in unavailable_books:
            borrowed_book = BorrowedBook.objects.filter(book=book).order_by('-return_date').first()

            if borrowed_book:
                unavailable_books_with_return_date.append({
                    'book_title': book.title,
                    'author': book.author,
                    'return_date': borrowed_book.return_date
                })

        return Response({"status": "success", "message": "Unavailable books", "data": unavailable_books_with_return_date})
    


    