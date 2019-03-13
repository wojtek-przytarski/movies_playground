from django.test import TestCase

from api.exceptions import OmdbApiResponseException
from api.externalapihandler.omdb_api_handler import OmdbApiHandler


class ExternalApiTestCase(TestCase):

    def setUp(self):
        self.api = OmdbApiHandler('c0b35c21')

    def test_omdb_api_handler_returns_valid_response(self):
        movie = self.api.get_movie('The Dark Knight')
        print(movie)
        assert movie.get('Released') == '18 Jul 2008'

    def test_request_with_invalid_movie_names(self):
        self.assertRaises(OmdbApiResponseException, self.api.get_movie, 'Dark Knigh')
        self.assertRaises(OmdbApiResponseException, self.api.get_movie, 'AsdgS')
