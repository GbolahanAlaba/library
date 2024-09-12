from django.urls import path, include
from App_Library.views import *
from rest_framework.routers import DefaultRouter



urlpatterns = [
   path('add-book/', LibraryViewSets.as_view({"post": "add_new_book"}), name='book-add'),
   path('books/', LibraryViewSets.as_view({"get": "books"}), name='all-books'),
   path('get_book/<str:book_id>/', LibraryViewSets.as_view({"get": "get_a_book"}), name='get-book-detail'),
   path('filter-books/', LibraryViewSets.as_view({"get": "filter_books"}), name='books-filters'),

   path('enroll-user/', LibraryViewSets.as_view({"post": "enroll_user"}), name='user-enroll'),
]