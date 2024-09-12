from django.urls import path, include
from App_Library.views import *
from rest_framework.routers import DefaultRouter



urlpatterns = [
   path('add-book/', LibraryViewSets.as_view({"post": "add_new_book"}), name='book-add'),
   path('books/', LibraryViewSets.as_view({"get": "books"}), name='all-books'),
   path('view-book/<str:book_id>/', LibraryViewSets.as_view({"get": "view_book"}), name='book-view'),
   path('filter-books/', LibraryViewSets.as_view({"get": "filter_books"}), name='books-filters'),

   path('enroll-user/', LibraryViewSets.as_view({"post": "enroll_user"}), name='user-enroll'),
]