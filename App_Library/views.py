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
    serializer_class = BookSerializer
    user_serializer_class = UserSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['author', 'category']

    @handle_exceptions
    def add_new_book(self, request, *args, **kwargs):
        serializer = self.book_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success", "message": "Book added", "data": serializer.data}, status=status.HTTP_201_CREATED)

    @handle_exceptions
    def books(self, request, *args, **kwargs):
        obj = Book.objects.all().order_by("-created_at")

        serializer = self.serializer_class(obj, many=True)
        return Response({"status": "success", "message": "All Books", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exceptions
    def view_book(self, request, book_id, *args, **kwargs):
        book = Book.objects.filter(book_id=book_id).first()

        if not book:
            return Response({"status": "failed", "message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(book)
            return Response({"status": "success", "message": f"{book.title}", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exceptions
    def filter_books(self, request, *args, **kwargs):
        author = request.query_params.get('author', None)
        category = request.query_params.get('category', None)

        if author:
            self.queryset = self.queryset.filter(author__icontains=author)
        if category:
            self.queryset = self.queryset.filter(category__icontains=category)
        
        serializer = self.serializer_class(self.queryset, many=True)
        return Response({"status": "success", "message": "All books", "data":serializer.data}, status=status.HTTP_200_OK)
    

    @handle_exceptions
    def enroll_user(self, request, *args, **kwargs):
        serializer = self.user_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success", "message": "User enrolled", "data": serializer.data}, status=status.HTTP_201_CREATED)
