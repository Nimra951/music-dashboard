from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    year = models.IntegerField(default=2020)
    popularity = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    def __str__(self):
        return self.title