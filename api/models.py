from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    released = models.CharField(max_length=16)
    director = models.CharField(max_length=32)
    runtime = models.CharField(max_length=16)
    genre = models.ManyToManyField('Genre')
    rated = models.CharField(max_length=16)
    writer = models.CharField(max_length=128)
    actors = models.ManyToManyField('Actor')
    plot = models.CharField(max_length=512)
    languages = models.ManyToManyField('Language')
    countries = models.CharField(max_length=32)
    awards = models.CharField(max_length=128)
    poster = models.CharField(max_length=256)
    ratings = models.ManyToManyField('Rating')
    metascore = models.CharField(max_length=4)
    imdb_rating = models.CharField(max_length=4)
    imdb_votes = models.CharField(max_length=16)
    imdb_id = models.CharField(max_length=16)
    type = models.CharField(max_length=16)
    dvd = models.CharField(max_length=16)
    box_office = models.CharField(max_length=16)
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


class Language(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Rating(models.Model):
    source = models.ForeignKey('RatingSource', on_delete=models.CASCADE)
    value = models.CharField(max_length=32)


class RatingSource(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
