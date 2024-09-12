from django.contrib import admin
from . models import *

@admin.register(Book)
class Reviewadmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_date', 'publisher', 'language', 'category', 'description']
    list_filter = ['title']
    search_fields = ['title']
    ordering = ['-created_at']