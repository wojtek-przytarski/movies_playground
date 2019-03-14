from venv import logger

from django.core import serializers
from django.http import JsonResponse
from rest_framework import viewsets

from api.exceptions import OmdbApiResponseException
from api.externalapihandler.omdb_api_handler import OmdbApiHandler
from api.models import Movie, Actor, Genre, Rating
from api.serializers import MovieSerializer, GenreSerializer, ActorSerializer
from movies_playground.settings import OMDB_API_KEY

omdb_api = OmdbApiHandler(OMDB_API_KEY)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, **kwargs):
        movie_title = request.data.get('title')
        if not movie_title:
            return JsonResponse({'Error': 'Invalid request. Please provide \'title\' in request.'})
        try:
            return JsonResponse(
                MovieSerializer(Movie.objects.get(title=movie_title), context={'request': request}).data)
        except Movie.DoesNotExist:
            try:
                movie = self._add_new_movie(movie_title)
                return JsonResponse(MovieSerializer(movie, context={'request': request}).data)
            except OmdbApiResponseException as ex:
                logger.error(ex)
                return JsonResponse({'Error': 'Invalid movie title.'})

    def _add_new_movie(self, movie_title):
        movie_info = omdb_api.get_movie(movie_title)
        movie = self._get_movie_from_omdb_result(movie_info)
        return movie

    def _get_movie_from_omdb_result(self, omdb_result):
        # TODO: clean this mess and maybe move it to another place
        movie_args = {k[:1].lower() + k[1:]: v for k, v in omdb_result.items()}  # change keys to make it same as model
        foreign_key_action = {'actors': self._get_actor_set,
                              'genre': self._get_genre_set,
                              'ratings': self._get_rating_set}
        movie = Movie()
        for key, value in movie_args.items():
            action = foreign_key_action.get(key)
            if not action:
                movie.__setattr__(key, value)
        movie.save()  # object must be saved to add to manytomany fields
        for key, action in foreign_key_action.items():
            values_set = action(movie_args.get(key))
            for value in values_set:
                movie.__getattribute__(key).add(value)
        movie.save()
        return movie

    @staticmethod
    def _get_actor_set(omdb_actor):
        actor_set = set()
        for actor_name in omdb_actor.split(', '):
            try:
                actor_set.add(Actor.objects.get(name__icontains=actor_name))
            except Actor.DoesNotExist:
                a = Actor(name=actor_name)
                a.save()
                actor_set.add(a)
        return actor_set

    @staticmethod
    def _get_genre_set(omdb_genre):
        genre_set = set()
        for genre_name in omdb_genre.split(', '):
            try:
                genre_set.add(Genre.objects.get(name__icontains=genre_name))
            except Genre.DoesNotExist:
                g = Genre(name=genre_name)
                g.save()
                genre_set.add(g)
        return genre_set

    @staticmethod
    def _get_rating_set(omdb_ratings):
        rating_set = set()
        for rating in omdb_ratings:
            r = Rating(source=rating.get('Source'), value=rating.get('Value'))
            r.save()
            rating_set.add(r)
            r.save()
        return rating_set
