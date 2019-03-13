from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from api.models import Movie
from api.serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        movie_title = request.data.get('title')
        if not movie_title:
            return JsonResponse({'Error': 'Invalid request. Please provide \'title\' in request.'})
        return HttpResponse(str(request))
