# from django.urls import reverse, resolve
# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient
# from django.test import TestCase
# from .models import Weather
# from .views import WeatherViewSet


# # TEST FOR VIEWS
# class WeatherViewSetTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.create_weather_url = reverse('weather-create')
#         self.city_weather_url = lambda city: reverse('weather-detail', kwargs={'city': city})
        
#         self.valid_payload = {
#             'city': 'Lagos',
#             'date': '2024-08-04',
#             'temperature': 25.5,
#             'description': 'Sunny with clear skies'
#         }
        
#         self.invalid_payload = {
#             'city': '',
#             'date': 'invalid-date',
#             'temperature': 'invalid-temperature',
#             'description': ''
#         }
        
#         self.weather = Weather.objects.create(
#             city='Lagos',
#             date='2024-08-04',
#             temperature=25.5,
#             description='Sunny with clear skies'
#         )

#     def test_create_city_weather_valid_payload(self):
#         response = self.client.post(self.create_weather_url, data=self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['city'], self.valid_payload['city'])
#         self.assertEqual(response.data['date'], self.valid_payload['date'])
#         self.assertEqual(response.data['temperature'], self.valid_payload['temperature'])
#         self.assertEqual(response.data['description'], self.valid_payload['description'])

#     def test_create_city_weather_invalid_payload(self):
#         response = self.client.post(self.create_weather_url, data=self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_view_city_weather_exists(self):
#         response = self.client.get(self.city_weather_url('Lagos'), format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['city'], self.weather.city)
#         self.assertEqual(response.data['date'], str(self.weather.date))
#         self.assertEqual(response.data['temperature'], self.weather.temperature)
#         self.assertEqual(response.data['description'], self.weather.description)

#     def test_view_city_weather_not_exists(self):
#         response = self.client.get(self.city_weather_url('Nonexistent City'), format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['status'], 'failed')
#         self.assertEqual(response.data['message'], 'City not found')


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