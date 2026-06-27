import pandas as pd
from django.core.management.base import BaseCommand
from music_app.models import Song, Artist, Genre

class Command(BaseCommand):
    help = 'Import songs from CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('dataset.csv')
        df = df.head(500)
        df = df.dropna(subset=['track_name', 'artists', 'track_genre'])

        imported = 0
        for _, row in df.iterrows():
            genre, _ = Genre.objects.get_or_create(name=row['track_genre'])
            artist, _ = Artist.objects.get_or_create(name=row['artists'])

            Song.objects.get_or_create(
                title=row['track_name'],
                defaults={
                    'artist': artist,
                    'genre': genre,
                    'year': 2020,
                    'popularity': float(row['popularity']),
                    'energy': float(row['energy']),
                }
            )
            imported += 1

        self.stdout.write(f"Done! {imported} songs imported.")