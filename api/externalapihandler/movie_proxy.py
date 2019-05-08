from api.models import Rating, Genre, Actor, Movie


class MovieProxy:

    def __init__(self, api):
        self.omdb_api = api

    def get_movie_details(self, title):
        try:
            return Movie.objects.get(title=title)
        except Movie.DoesNotExist:
            return self._add_new_movie(title)

    def _add_new_movie(self, title):
        omdb_result = self.omdb_api.get_movie(title)
        movie_args = {k[:1].lower() + k[1:]: v for k, v in omdb_result.items()}
        movie = self._add_movie_from_omdb_result(movie_args)
        return movie

    def get_movie_queryset(self, **kwargs):
        queryset = Movie.objects.all()
        director = kwargs.get('director')
        actor = kwargs.get('actor')
        genre = kwargs.get('genre')
        queryset = queryset.filter(director__icontains=director) if director else queryset
        queryset = queryset.filter(actors__name__icontains=actor) if actor else queryset
        queryset = queryset.filter(genre__name__iexact=genre) if genre else queryset
        return queryset

    def _add_movie_from_omdb_result(self, movie_args):
        foreign_key_values = {'actors': self._get_actor_set(movie_args.get('actors')),
                              'genre': self._get_genre_set(movie_args.get('genre')),
                              'ratings': self._get_rating_set(movie_args.get('ratings'))}
        movie = Movie()
        for key, value in movie_args.items():
            action = foreign_key_values.get(key)
            if not action:
                movie.__setattr__(key, value)
        movie.save()  # object must be saved to add values to manytomany fields
        for key, values_set in foreign_key_values.items():  # so add it after saving
            movie.__getattribute__(key).add(*values_set)
        movie.save()
        return movie

    @staticmethod
    def _get_actor_set(omdb_actor):
        actor_set = set()
        for actor_name in omdb_actor.split(', '):
            actor = Actor.objects.get_or_create(name=actor_name)
            actor.save()
            actor_set.add(actor)
        return actor_set

    @staticmethod
    def _get_genre_set(omdb_genre):
        genre_set = set()
        for genre_name in omdb_genre.split(', '):
            genre = Genre.objects.get_or_create(name=genre_name)
            genre.save()
            genre_set.add(genre)
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
