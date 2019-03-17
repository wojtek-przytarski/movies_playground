from venv import logger

from django.http import JsonResponse
from rest_framework import viewsets

from api.exceptions import OmdbApiResponseException
from api.externalapihandler.movie_proxy import MovieProxy
from api.externalapihandler.omdb_api_handler import OmdbApiHandler
from api.models import Movie, Actor, Genre, Rating
from api.serializers import MovieSerializer, GenreSerializer, ActorSerializer
from movies_playground.settings import OMDB_API_KEY


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def __init__(self, **kwargs):
        self.movie_proxy = MovieProxy(OmdbApiHandler(OMDB_API_KEY))
        super().__init__(**kwargs)

    def create(self, request, **kwargs):
        movie_title = request.data.get('title')
        if not movie_title:
            return JsonResponse({'Error': 'Invalid request. Please provide \'title\' in request.'})
        try:
            movie = self.movie_proxy.get_movie_details(movie_title)
            return JsonResponse(MovieSerializer(movie, context={'request': request}).data)
        except OmdbApiResponseException:
            return JsonResponse({'Error': 'Invalid movie title.'})
        except Exception as ex:
            logger.error('Unexpected error: {}'.format(ex))
            return JsonResponse({'Error': 'Error occured, please try again later.'})

    def get_queryset(self):
        filter_kwargs = {'genre': self.request.query_params.get('genre'),
                         'actor': self.request.query_params.get('actor'),
                         'director': self.request.query_params.get('director')}
        return self.movie_proxy.get_movie_queryset(**filter_kwargs)
