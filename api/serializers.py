from rest_framework import serializers
from api.models import Movie, Genre, Actor, Rating, Comment


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = ('name',)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('source', 'value')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    ratings = RatingSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'
        depth = 3


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'body', 'posting_date')
