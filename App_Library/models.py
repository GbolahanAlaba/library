from django.db import models
import uuid
from django.utils import timezone


# Create your models here.


class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    available_copies = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BorrowedBook(models.Model):
    borrow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        # Reduce the number of available copies when a book is borrowed
        if not self.pk:
            self.book.available_copies -= 1
            self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} borrowed {self.book.title}'