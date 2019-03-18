from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.utils import json


class MoviesEndpointTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.post('/movies', {'title': 'True Detective'}, type='json')
        self.client.post('/movies', {'title': 'Bohemian Rhapsody'}, type='json')
        self.client.post('/movies', {'title': 'The Dark Knight'}, type='json')
        self.movies_in_db = [{'title_chunk': '"title":"True Detective"', 'genres': ['Crime'],
                              'actors': ['Matthew McConaughey', 'Colin Farrell']},
                             {'title_chunk': '"title":"Bohemian Rhapsody"', 'genres': ['Music', 'Drama'],
                              'actors': ['Rami Malek']},
                             {'title_chunk': '"title":"The Dark Knight"', 'genres': ['Crime', 'Thriller', 'Action'],
                              'actors': ['Christian Bale']}]

    def test_get_all_movies(self):
        response = self.client.get('/movies')
        for movie in self.movies_in_db:
            assert movie.get('title_chunk') in str(response.content)

    def test_get_movies_with_single_filtering(self):
        response = self.client.get('/movies', {'genre': 'Music'})
        self._check_movies_with_genre_in_content(response.content, 'Music')
        response = self.client.get('/movies', {'actor': 'Colin Farrell'})
        self._check_movies_with_actor_in_content(response.content, 'Colin Farrell')

    def test_get_movies_with_multiple_filters(self):
        response = self.client.get('/movies', {'genre': 'Crime', 'actor': 'Christian Bale'})
        self._check_movies_with_actor_in_content(response.content, 'Christian Bale')
        self._check_movies_with_genre_in_content(response.content, 'Thriller')

    def test_add_to_db_by_retrieving(self):
        with open('api/test/movies.txt') as file:
            for title in file:
                response = self.client.post('/movies', {'title': title.strip()}, type='json')
                response_dict = json.loads(response.content)
                assert not response_dict.get('Error')
        all_movies = self.client.get('/movies').content
        with open('api/test/movies.txt') as file:
            for title in file:
                assert title.strip() in str(all_movies)

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
