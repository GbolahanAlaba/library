from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from .models import *
from .views import LibraryViewSets
from datetime import date, timedelta


# TEST FOR VIEWS
class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.enroll_user_url = reverse('user-enroll')
        self.books_url = reverse('all-books')
        self.view_book_url = lambda book_id: reverse('book-view', kwargs={'book_id': book_id})
        self.borrow_book_url = reverse('book-borrow')
        self.add_book_url = reverse('book-add')
        self.remove_book_url = lambda book_id: reverse('book-remove', kwargs={'book_id': book_id})
        self.users_url = reverse('library-users')
        self.unavailable_books_url = reverse('books-unavailable')

        self.valid_user_payload = {
            'first_name': 'Gbolahan',
            'last_name': 'Alaba',
            'email': 'gbolahan@gmal.com',
        }
        
        self.invalid_user_payload = {
            'first_name': 'Gbolahan',
            'last_name': 'Alaba',
            'email': "gotten",
        }

        self.user = User.objects.create(
            first_name='Gbolahan',
            last_name='Alaba',
            email='gbolahan@gmail.com',
        )
        self.user_id = str(self.user.user_id)


        self.valid_book_payload = {
            'title': 'Lagos Boy',
            'author': 'Vincent',
            'publication_date': '2024-09-12',
            'publisher': 'Mr Bone',
            'language': 'English',
            'category': "Lifestyle",
            'description': 'Sunny with clear skies'
        }
        
        self.invalid_book_payload = {
            'title': 'Lagos',
            'author': '2024-08-04',
            'publication_date': 25.5,
            'publisher': 'Sunny with clear skies',
            'language': 25.5,
            'category': 'Sunny with clear skies',
            'description': '2024-08-04'
        }
        
        self.book = Book.objects.create(
            title='Lagos Boy',
            author='Vincent',
            publication_date='2024-09-12',
            publisher='Mr Bone',
            language='English',
            category="Lifestyle",
            available_copies=0,
            description='Sunny with clear skies'
        )
        self.book_id = str(self.book.book_id)

        self.borrowed_book = BorrowedBook.objects.create(
        book=self.book,
        user=self.user,
        borrow_date='2024-09-12',
        return_date='2024-09-20'  # Set a future return date
    )


    """Test for enrolling users into the library"""
    def test_enroll_user_valid_payload(self):
        response = self.client.post(self.enroll_user_url, data=self.valid_user_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_data = response.data['data']
        self.assertEqual(user_data['first_name'], self.valid_user_payload['first_name'])
        self.assertEqual(user_data['last_name'], self.valid_user_payload['last_name'])
        self.assertEqual(user_data['email'], self.valid_user_payload['email'])
       
    def test_enroll_user_invalid_payload(self):
        response = self.client.post(self.enroll_user_url, data=self.invalid_user_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    """Test for listing all books in the library"""
    def test_get_all_books(self):
        response = self.client.get(self.books_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'All Books')

        books_data = response.data['data']
        self.assertEqual(len(books_data), Book.objects.count())

        # Checking data of the first book
        first_book = books_data[0]
        self.assertEqual(first_book['title'], self.book.title)
        self.assertEqual(first_book['author'], self.book.author)
        self.assertEqual(first_book['publication_date'], str(self.book.publication_date))
        self.assertEqual(first_book['publisher'], self.book.publisher)
        self.assertEqual(first_book['language'], self.book.language)
        self.assertEqual(first_book['category'], self.book.category)
        self.assertEqual(first_book['description'], self.book.description)

    """Test for viewing book details"""
    def test_view_book_details_exists(self):
        response = self.client.get(self.view_book_url(self.book_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book_data = response.data['data']
        self.assertEqual(book_data['title'], self.book.title)
        self.assertEqual(book_data['author'], str(self.book.author))
        self.assertEqual(book_data['publication_date'], self.book.publication_date)
        self.assertEqual(book_data['publisher'], self.book.publisher)
        self.assertEqual(book_data['language'], str(self.book.language))
        self.assertEqual(book_data['category'], self.book.category)
        self.assertEqual(book_data['description'], self.book.description)
    
    def test_view_book_details_not_exists(self):
        invalid_book_id = '00000000-0000-0000-0000-000000000000'
        response = self.client.get(self.view_book_url(invalid_book_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'Book not found')



    """Test for borrowing books"""
    def test_borrow_book_success(self):
        data = {
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrow_duration': 7  # Borrow for 7 days
        }
        response = self.client.post(self.borrow_book_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        borrowed_book_data = response.data
        self.assertEqual(borrowed_book_data['user'], self.user_id)
        self.assertEqual(borrowed_book_data['book'], self.book_id)
        self.assertEqual(borrowed_book_data['borrow_date'], (timezone.now().date()).isoformat())
        self.assertEqual(borrowed_book_data['return_date'], (timezone.now().date() + timedelta(days=7)).isoformat())

        # Check if available copies have decreased
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 4)

    def test_borrow_book_missing_parameters(self):
        data = {
            'user_id': self.user_id,
            'book_id': self.book_id
        }
        response = self.client.post(self.borrow_book_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'Please provide user_id, book_id, and borrow_duration.')

    def test_borrow_book_user_not_exists(self):
        data = {
            'user_id': '00000000-0000-0000-0000-000000000000',  # Invalid user ID
            'book_id': self.book_id,
            'borrow_duration': 7
        }
        response = self.client.post(self.borrow_book_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'User does not exist.')

    def test_borrow_book_book_not_exists(self):
        data = {
            'user_id': self.user_id,
            'book_id': '00000000-0000-0000-0000-000000000000',  # Invalid book ID
            'borrow_duration': 7
        }
        response = self.client.post(self.borrow_book_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'Book not available or out of stock.')

    def test_borrow_book_no_available_copies(self):
        # Set available copies to 0
        self.book.available_copies = 0
        self.book.save()

        data = {
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrow_duration': 7
        }
        response = self.client.post(self.borrow_book_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'Book not available or out of stock.')
        print(self.borrow_book_url)

    
    """Test for adding books to the library"""
    def test_add_book_valid_payload(self):
        response = self.client.post(self.add_book_url, data=self.valid_book_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_data = response.data['data']
        self.assertEqual(book_data['title'], self.valid_book_payload['title'])
        self.assertEqual(book_data['author'], self.valid_book_payload['author'])
        self.assertEqual(book_data['publication_date'], self.valid_book_payload['publication_date'])
        self.assertEqual(book_data['publisher'], self.valid_book_payload['publisher'])
        self.assertEqual(book_data['language'], self.valid_book_payload['language'])
        self.assertEqual(book_data['category'], self.valid_book_payload['category'])
        self.assertEqual(book_data['description'], self.valid_book_payload['description'])

    def test_add_book_invalid_payload(self):
        response = self.client.post(self.add_book_url, data=self.invalid_book_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    """Test for removing books from the library"""
    def test_remove_book_success(self):
        response = self.client.delete(self.remove_book_url(self.book_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], f"{self.book.title} book removed from catalogue")
        self.assertFalse(Book.objects.filter(book_id=self.book_id).exists())

    def test_remove_book_not_found(self):
        invalid_book_id = '00000000-0000-0000-0000-000000000000'
        response = self.client.delete(self.remove_book_url(invalid_book_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'Book not found')


    """Test for getting all users enrolled in the library"""
    def test_get_all_users(self):
        response = self.client.get(self.users_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'All library users')

        users_data = response.data['data']
        self.assertEqual(len(users_data), User.objects.count())

        first_user = users_data[0]
        self.assertEqual(first_user['first_name'], self.user.first_name)
        self.assertEqual(first_user['last_name'], self.user.last_name)
        self.assertEqual(first_user['email'], self.user.email)

   



# TEST FOR URLS
class LibraryURLTestCase(APITestCase):
    def test_enroll_user_url(self):
        url = reverse('user-enroll')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'post': 'enroll_user'}).__name__)

    def test_all_book_url(self):
        url = reverse('all-books')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'books'}).__name__)

    def test_view_book_url(self):
        url = reverse('book-view', kwargs={'book_id': 'book_id'})
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'view_book'}).__name__)
    
    def test_filter_books_url(self):
        url = reverse('books-filters')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'filter_books'}).__name__)

    def test_borrow_book_url(self):
        url = reverse('book-borrow')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'post': 'borrow_book'}).__name__)
    
    def test_add_book_url(self):
        url = reverse('book-add')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'post': 'add_new_book'}).__name__)

    def test_remove_book_url(self):
        url = reverse('book-remove', kwargs={'book_id': 'book_id'})
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'post': 'remove_book'}).__name__)

    def test_users_url(self):
        url = reverse('library-users')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'users'}).__name__)
    
    def test_borrowed_books_and_users_url(self):
        url = reverse('books-borrowed')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'unavailable_books'}).__name__)


    def test_unavailable_books_url(self):
        url = reverse('books-unavailable')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'borrowed_books'}).__name__)



# #  TEST FOR MODEL
class LibraryModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Lagos Boy',
            author='Vincent',
            publication_date='2024-09-12',
            publisher='Mr Bone',
            language='English',
            category="Lifestyle",
            description='Sunny with clear skies'
        )

        self.user = User.objects.create(
            first_name='Gbolahan',
            last_name='Alaba',
            email='gbolahan@gmail.com',
        )

        self.borrow_book = BorrowedBook.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=timezone.now(),
            return_date=timezone.now() + timezone.timedelta(days=7)
        )

    # Book Model
    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Lagos Boy')
        self.assertEqual(self.book.author, 'Vincent')
        self.assertEqual(self.book.publication_date, '2024-09-12')
        self.assertEqual(self.book.publisher, 'Mr Bone')
        self.assertEqual(self.book.language, 'English')
        self.assertEqual(self.book.category, 'Lifestyle')
        self.assertEqual(self.book.description, 'Sunny with clear skies')

    def test_book_str_representation(self):
        self.assertEqual(str(self.book), 'Lagos Boy')

    # User Model
    def test_user_creation(self):
        self.assertEqual(self.user.first_name, 'Gbolahan')
        self.assertEqual(self.user.last_name, 'Alaba')
        self.assertEqual(self.user.email, 'gbolahan@gmail.com')

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'Gbolahan')

    # Borrow Book Model
    def test_user_creation(self):
        self.assertEqual(self.borrow_book.user.first_name, 'Gbolahan')
        self.assertEqual(self.borrow_book.book.title, 'Lagos Boy')

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'Gbolahan Alaba')