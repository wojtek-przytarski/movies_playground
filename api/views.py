from venv import logger

from django.core.exceptions import ValidationError
from django.db.models import Count, Window, F, IntegerField, Case, When
from django.db.models.functions import DenseRank
from django.http import JsonResponse
from rest_framework import viewsets

from api.exceptions import OmdbApiResponseException
from api.externalapihandler.movie_proxy import MovieProxy
from api.externalapihandler.omdb_api_handler import OmdbApiHandler
from api.models import Movie, Actor, Genre, Comment, Trailer
from api.serializers import MovieSerializer, GenreSerializer, ActorSerializer, CommentSerializer, TrailerSerializer
from movies_playground.settings import OMDB_API_KEY


def top(request):
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    if not date_from or not date_to:
        return JsonResponse({'Error': 'Invalid request. Please provide \'from\' and \'to\' in request.'})
    if date_from > date_to:
        return JsonResponse({'Error': 'Invalid request. \'from\' should be less or equal than \'to\' in request.'})
    date_range = [date_from, date_to]
    try:
        queryset = Movie.objects.values('id', 'comment__id')
        comments_count = Count(Case(When(comment__posting_date__range=date_range, then=1), output_field=IntegerField()))
        dense_rank = Window(expression=DenseRank(), order_by=F('total_comments').desc())
        statistics = queryset.values('id').annotate(movie_id=F('id'), total_comments=comments_count).annotate(
            rank=dense_rank).values('movie_id', 'total_comments', 'rank')
        return JsonResponse(list(statistics), safe=False)
    except ValidationError:
        return JsonResponse(
            {'Error': 'Invalid parameters type.\'from\' and \'to\' should be date in format YYYY-MM-DD.'})


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get']


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    http_method_names = ['get']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['post', 'get']

    def create(self, request, **kwargs):
        movie_id = request.data.get('movie_id')
        body = request.data.get('body')
        if not movie_id or not body:
            return JsonResponse({'Error': 'Invalid request. Please provide \'movie_id\' and \'body\' in request.'})
        try:
            comment = Comment(movie=Movie.objects.get(id=movie_id), body=body)
            comment.save()
            return JsonResponse(CommentSerializer(comment, context={'request': request}).data)
        except Movie.DoesNotExist:
            return JsonResponse({'Error': 'Movie with id = {} does not exist.'.format(movie_id)})

    def get_queryset(self):
        movie_id = self.request.query_params.get('movie_id')
        queryset = Comment.objects.filter(movie_id=movie_id) if movie_id else Comment.objects.all()
        return queryset


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    http_method_names = ['post', 'get']

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


class TrailerViewSet(viewsets.ModelViewSet):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    http_method_names = ['post', 'get']
