from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from .models import *
from .views import LibraryViewSets


# TEST FOR VIEWS
class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.add_book_url = reverse('book-add')
        self.books_url = reverse('all-books')
        self.get_book_url = lambda book_id: reverse('get-book-detail', kwargs={'book_id': book_id})
        self.enroll_user_url = reverse('user-enroll')
        
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
            description='Sunny with clear skies'
        )
        self.book_id = str(self.book.book_id)

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

    def test_view_book_detail_exists(self):
        response = self.client.get(self.get_book_url(self.book_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book_data = response.data['data']
        self.assertEqual(book_data['title'], self.book.title)
        self.assertEqual(book_data['author'], str(self.book.author))
        self.assertEqual(book_data['publication_date'], self.book.publication_date)
        self.assertEqual(book_data['publisher'], self.book.publisher)
        self.assertEqual(book_data['language'], str(self.book.language))
        self.assertEqual(book_data['category'], self.book.category)
        self.assertEqual(book_data['description'], self.book.description)

    def test_view_book_detail_not_exists(self):
        response = self.client.get(self.get_book_url('hdhdjfjjf'), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'book not found')


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




# TEST FOR URLS
class LibraryURLTestCase(APITestCase):
    # Books
    def test_add_book_url(self):
        url = reverse('book-add')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'post': 'add_new_book'}).__name__)

    def test_all_book_url(self):
        url = reverse('all-books')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'books'}).__name__)

    def test_get_book_url(self):
        url = reverse('get-book-detail', kwargs={'book_id': 'Test City'})
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'get_a_book'}).__name__)
    
    def test_filter_books_url(self):
        url = reverse('books-filters')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'get': 'filter_books'}).__name__)


    # Users
    def test_enroll_user_url(self):
        url = reverse('user-enroll')
        self.assertEqual(resolve(url).func.__name__, LibraryViewSets.as_view({'post': 'enroll_user'}).__name__)




#  TEST FOR MODEL
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

    # Book
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


    # User
    def test_user_creation(self):
        self.assertEqual(self.user.first_name, 'Gbolahan')
        self.assertEqual(self.user.last_name, 'Alaba')
        self.assertEqual(self.user.email, 'gbolahan@gmail.com')

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'Gbolahan')