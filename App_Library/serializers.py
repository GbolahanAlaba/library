from rest_framework import serializers
from App_Library.models import *


class LibrarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'publication_date', 'publisher', 'language', 'category', 'description']