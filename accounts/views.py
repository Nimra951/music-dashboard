from django.shortcuts import render, redirect, get_object_or_404
from .models import Song

# HOME PAGE (THIS WAS MISSING)
def home(request):
    songs = Song.objects.all()
    return render(request, 'music_app/home.html', {'songs': songs})