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
        self._add_comment_with_date(12, '2014-12-04')
        self._add_comment_with_date(31, '2015-01-04')
        self._add_comment_with_date(66, '2016-02-28')
        self._add_comment_with_date(31, '2018-12-01')
        self._add_comment_with_date(66, '2019-01-01')

    @staticmethod
    def _add_comment_with_date(movie_id, date):
        comment = Comment(movie_id=movie_id, body='This is pre-added comment.')
        comment.save()
        comment.posting_date = date
        comment.save()

    def test_requests_without_dates_returns_error(self):
        response = self.client.get('/top')
        assert json.loads(response.content).get('Error')
        response = self.client.get('/top', {'from': '2012-10-10'})
        assert json.loads(response.content).get('Error')
        response = self.client.get('/top', {'to': '2021-10-10'})
        assert json.loads(response.content).get('Error')

    def test_all_comments_should_be_counted(self):
        response = self.client.get('/top', {'from': '2012-10-10', 'to': '2020-10-10'})
        expected_stats = [{'movie_id': 31, 'total_comments': 2, 'rank': 1},
                          {'movie_id': 66, 'total_comments': 2, 'rank': 1},
                          {'movie_id': 12, 'total_comments': 1, 'rank': 2},
                          {'movie_id': 78, 'total_comments': 0, 'rank': 3}]
        stats = json.loads(response.content)
        assert stats == expected_stats

    def test_some_comments_should_be_counted(self):
        response = self.client.get('/top', {'from': '2015-01-04', 'to': '2016-02-28'})
        expected_stats = [{'movie_id': 31, 'total_comments': 1, 'rank': 1},
                          {'movie_id': 66, 'total_comments': 1, 'rank': 1},
                          {'movie_id': 12, 'total_comments': 0, 'rank': 2},
                          {'movie_id': 78, 'total_comments': 0, 'rank': 2}]
        stats = json.loads(response.content)
        assert stats == expected_stats

    def test_no_comments_should_be_counted(self):
        response = self.client.get('/top', {'from': '2015-01-05', 'to': '2016-02-27'})
        expected_stats = [{'movie_id': 12, 'total_comments': 0, 'rank': 1},
                          {'movie_id': 31, 'total_comments': 0, 'rank': 1},
                          {'movie_id': 66, 'total_comments': 0, 'rank': 1},
                          {'movie_id': 78, 'total_comments': 0, 'rank': 1}]
        stats = json.loads(response.content)
        assert stats == expected_stats
