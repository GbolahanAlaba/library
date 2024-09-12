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
        
        self.valid_payload = {
            'title': 'Lagos Boy',
            'author': 'Vincent',
            'publication_date': '2024-09-12',
            'publisher': 'Mr Bone',
            'language': 'English',
            'category': "Lifestyle",
            'description': 'Sunny with clear skies'
        }
        
        self.invalid_payload = {
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
        self.book_id = str(self.book.book_id)  # Store the actual book ID

    def test_add_book_valid_payload(self):
        response = self.client.post(self.add_book_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_data = response.data['data']
        self.assertEqual(book_data['title'], self.valid_payload['title'])
        self.assertEqual(book_data['author'], self.valid_payload['author'])
        self.assertEqual(book_data['publication_date'], self.valid_payload['publication_date'])
        self.assertEqual(book_data['publisher'], self.valid_payload['publisher'])
        self.assertEqual(book_data['language'], self.valid_payload['language'])
        self.assertEqual(book_data['category'], self.valid_payload['category'])
        self.assertEqual(book_data['description'], self.valid_payload['description'])

    def test_add_book_invalid_payload(self):
        response = self.client.post(self.add_book_url, data=self.invalid_payload, format='json')
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
        response = self.client.get(self.get_book_url('Nonexistent City'), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'book not found')


# # TEST FOR URLS
# class WeatherURLTestCase(APITestCase):
#     def test_create_weather_url(self):
#         url = reverse('weather-create')
#         self.assertEqual(resolve(url).func.__name__, WeatherViewSet.as_view({'post': 'create'}).__name__)

#     def test_view_weather_url(self):
#         url = reverse('weather-detail', kwargs={'city': 'Test City'})
#         self.assertEqual(resolve(url).func.__name__, WeatherViewSet.as_view({'get': 'retrieve_city'}).__name__)



# #  TEST FOR MODEL
# class WeatherModelTest(TestCase):
#     def setUp(self):
#         self.weather = Weather.objects.create(
#             city='Test City',
#             date='2024-08-04',
#             temperature=25.5,
#             description='Sunny with clear skies'
#         )

#     def test_weather_creation(self):
#         self.assertEqual(self.weather.city, 'Test City')
#         self.assertEqual(str(self.weather.date), '2024-08-04')
#         self.assertEqual(self.weather.temperature, 25.5)
#         self.assertEqual(self.weather.description, 'Sunny with clear skies')

#     def test_weather_str_representation(self):
#         self.assertEqual(str(self.weather), 'Test City')