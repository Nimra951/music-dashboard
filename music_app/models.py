from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)

    genre = models.CharField(max_length=100, default="Unknown")  # ✅ FIX

    def __str__(self):
        return self.title