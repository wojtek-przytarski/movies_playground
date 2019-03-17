from django.test import TestCase
from rest_framework.test import APIClient

from api.exceptions import OmdbApiResponseException
from api.externalapihandler.omdb_api_handler import OmdbApiHandler

client = APIClient()


class ExternalApiTestCase(TestCase):

    def setUp(self):
        self.api = OmdbApiHandler('c0b35c21')

    def test_omdb_api_handler_returns_valid_response(self):
        movie = self.api.get_movie('The Dark Knight')
        assert movie.get('Released') == '18 Jul 2008'

    def test_request_with_invalid_movie_names(self):
        self.assertRaises(OmdbApiResponseException, self.api.get_movie, 'Dark Knigh')
        self.assertRaises(OmdbApiResponseException, self.api.get_movie, 'AsdgS')


class MoviesApiTestCase(TestCase):

    def setUp(self):
        client.post('/movies', {'title': 'True Detective'}, type='json')
        client.post('/movies', {'title': 'Bohemian Rhapsody'}, type='json')
        client.post('/movies', {'title': 'The Dark Knight'}, type='json')
        self.movies_in_db = [{'title_chunk': '"title":"True Detective"', 'genres': ['Crime'],
                              'actors': ['Matthew McConaughey', 'Colin Farrell']},
                             {'title_chunk': '"title":"Bohemian Rhapsody"', 'genres': ['Music', 'Drama'],
                              'actors': ['Rami Malek']},
                             {'title_chunk': '"title":"The Dark Knight"', 'genres': ['Crime', 'Thriller', 'Action'],
                              'actors': ['Christian Bale']}]

    def test_get_all_movies(self):
        response = client.get('/movies')
        for movie in self.movies_in_db:
            assert movie.get('title_chunk') in str(response.content)

    def test_get_movies_with_single_filtering(self):
        response = client.get('/movies', {'genre': 'Music'})
        self._check_movies_with_genre_in_content(response.content, 'Music')
        response = client.get('/movies', {'actor': 'Colin Farrell'})
        self._check_movies_with_actor_in_content(response.content, 'Colin Farrell')

    def test_get_movies_with_multiple_filters(self):
        response = client.get('/movies', {'genre': 'Crime', 'actor': 'Christian Bale'})
        self._check_movies_with_actor_in_content(response.content, 'Christian Bale')
        self._check_movies_with_genre_in_content(response.content, 'Thriller')

    def _check_movies_with_genre_in_content(self, content, genre):
        for movie in self.movies_in_db:
            if genre in movie.get('genres'):
                assert movie.get('title_chunk') in str(content)
            else:
                assert movie.get('title_chunk') not in str(content)

    def _check_movies_with_actor_in_content(self, content, actor):
        for movie in self.movies_in_db:
            if actor in movie.get('actors'):
                assert movie.get('title_chunk') in str(content)
            else:
                assert movie.get('title_chunk') not in str(content)
