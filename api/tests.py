from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from api.exceptions import OmdbApiResponseException
from api.externalapihandler.omdb_api_handler import OmdbApiHandler

factory = APIClient()


class ExternalApiTestCase(TestCase):

    def setUp(self):
        self.api = OmdbApiHandler('c0b35c21')

    def test_omdb_api_handler_returns_valid_response(self):
        movie = self.api.get_movie('The Dark Knight')
        assert movie.get('Released') == '18 Jul 2008'

    def test_request_with_invalid_movie_names(self):
        self.assertRaises(OmdbApiResponseException, self.api.get_movie, 'Dark Knigh')
        self.assertRaises(OmdbApiResponseException, self.api.get_movie, 'AsdgS')


class ApiTestCase(TestCase):

    def setUp(self):
        pass

    def test_invalid_movie_title_returns_error(self):
        response = factory.post('/movies', {'title': 'it_cant_existt?'}, format='json')
        assert False  # TODO: use api client for requests
