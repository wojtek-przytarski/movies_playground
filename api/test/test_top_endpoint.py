from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.utils import json

from api.models import Movie, Comment


class TopEndpointTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        Movie(id=12, title='Testing IT').save()
        Movie(id=31, title='Testing IT 2').save()
        Movie(id=66, title='Testing IT 3').save()
        Movie(id=78, title='Testing IT 4').save()
        Comment(id=1, movie_id=12, body='This is pre-added comment.').save()
        Comment(id=2, movie_id=31, body='This is pre-added comment.').save()
        Comment(id=3, movie_id=31, body='This is pre-added comment.').save()
        Comment(id=4, movie_id=66, body='This is pre-added comment.').save()
        Comment(id=5, movie_id=66, body='This is pre-added comment.').save()

    def test_requests_without_dates_returns_error(self):
        response = self.client.get('/top')
        assert json.loads(response.content).get('Error')
        response = self.client.get('/top', {'from': '2012-10-10'})
        assert json.loads(response.content).get('Error')
        response = self.client.get('/top', {'to': '2021-10-10'})
        assert json.loads(response.content).get('Error')

    def test_get_returns_expected_statistics(self):
        response = self.client.get('/top', {'from': '2012-10-10', 'to': date.today()})
        expected_stats = [{'movie_id': 31, 'total_comments': 2, 'rank': 1},
                          {'movie_id': 66, 'total_comments': 2, 'rank': 1},
                          {'movie_id': 12, 'total_comments': 1, 'rank': 2},
                          {'movie_id': 78, 'total_comments': 0, 'rank': 3}]
        stats = json.loads(response.content)
        print(stats)
        assert stats == expected_stats
