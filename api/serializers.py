from rest_framework import serializers
from api.models import Movie, Genre, Actor, Language


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = ['name']


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ['name']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'
        depth = 3
