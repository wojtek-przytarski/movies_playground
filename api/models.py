from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=64)
    year = models.CharField(max_length=10)
    released = models.CharField(max_length=16)
    director = models.CharField(max_length=32)
    runtime = models.CharField(max_length=16)
    genre = models.ManyToManyField('Genre')
    rated = models.CharField(max_length=16)
    writer = models.CharField(max_length=128)
    actors = models.ManyToManyField('Actor')
    plot = models.CharField(max_length=512)
    languages = models.CharField(max_length=32)
    countries = models.CharField(max_length=32)
    awards = models.CharField(max_length=128)
    poster = models.CharField(max_length=256)
    ratings = models.ManyToManyField('Rating')
    metascore = models.CharField(max_length=4)
    imdbRating = models.CharField(max_length=4)
    imdbVotes = models.CharField(max_length=16)
    imdbID = models.CharField(max_length=16)
    totalSeasons = models.CharField(max_length=10, default='N/A')
    type = models.CharField(max_length=16)
    dvd = models.CharField(max_length=16)
    boxOffice = models.CharField(max_length=16)
    production = models.CharField(max_length=32)
    website = models.CharField(max_length=64)


class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    source = models.CharField(max_length=32)
    value = models.CharField(max_length=32)


class Comment(models.Model):
    body = models.CharField(max_length=1024)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    posting_date = models.DateField(auto_now_add=True, blank=True)


class Trailer(models.Model):
    title = models.CharField(max_length=64)
    url = models.URLField(max_length=256)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
