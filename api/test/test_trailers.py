from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.utils import json

from api.models import Movie, Comment, Trailer
from api.views import TrailerViewSet


class TrailersTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.trailer_view_set = TrailerViewSet()
        Movie(id=12, title='Testing IT').save()
        Movie(id=31, title='Testing IT 2').save()
        Movie(id=66, title='Testing IT 3').save()
        Movie(id=78, title='Testing IT 4').save()
        Trailer(movie_id=12, title='Testing trailer', description='tests', url='http://asdasd.asd/as').save()
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

    def test_add_trailer(self):
        response = self.client.post('/trailers', {'movie': 12, 'url': 'http://yt.sd/asd/asd',
                                                  'description': 'it will be nice movie!', 'title': 'Trailer'})
        assert Trailer.objects.all().count() == 2

    def test_get_trailers(self):
        response = self.client.get('/trailers')
        print(json.loads(response.content))
