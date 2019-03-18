from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.utils import json

from api.models import Movie, Comment


class CommentsEndpointTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        Movie(id=12, title='Testing IT').save()
        Movie(id=31, title='Testing IT 2').save()
        Comment(id=1, movie_id=12, body='This is pre-added comment.').save()
        Comment(id=2, movie_id=31, body='This is pre-added comment.').save()

    def test_post_comment_and_check_if_added(self):
        response = self.client.post('/comments', {'movie_id': 12, 'body': 'This is comment!'})
        assert response.status_code == 200
        assert Comment.objects.filter(movie_id=12).count() == 2

    def test_post_comment_returns_error_if_no_movie(self):
        response = self.client.post('/comments', {'movie_id': 555, 'body': 'This is comment!'})
        response_dict = json.loads(response.content)
        assert response_dict.get('Error') == 'Movie with id = 555 does not exist.'

    def test_post_invalid_comment(self):
        response = self.client.post('/comments', {'movie_id': 31})
        response_dict = json.loads(response.content)
        assert response_dict.get('Error') == 'Invalid request. Please provide \'movie_id\' and \'body\' in request.'
        response = self.client.post('/comments', {'body': 'This is comment!'})
        response_dict = json.loads(response.content)
        assert response_dict.get('Error') == 'Invalid request. Please provide \'movie_id\' and \'body\' in request.'

    def test_get_comments_returns_expected_dict(self):
        expected_data = [{'id': 1, 'movie_id': 12, 'body': 'This is pre-added comment.'},
                         {'id': 2, 'movie_id': 31, 'body': 'This is pre-added comment.'}]
        response = self.client.get('/comments')
        data = json.loads(response.content)
        assert data == expected_data

    def test_get_comments_by_movie_id_returns_expected_dict(self):
        expected_data = [{'id': 1, 'movie_id': 12, 'body': 'This is pre-added comment.'}]
        response = self.client.get('/comments', {'movie_id': 12})
        data = json.loads(response.content)
        assert expected_data == data
