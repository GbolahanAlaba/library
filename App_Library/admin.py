from django.contrib import admin
from . models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_date', 'publisher', 'language', 'category', 'description']
    list_filter = ['title']
    search_fields = ['title']
    ordering = ['-created_at']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    list_filter = ['first_name']
    search_fields = ['first_name']
    ordering = ['-created_at']


@admin.register(BorrowedBook)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'borrow_date']
    list_filter = ['user']
    search_fields = ['user']
    ordering = ['-borrow_date']